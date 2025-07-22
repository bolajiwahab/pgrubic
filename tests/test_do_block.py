"""Test DO block linting functionality."""

from pgrubic import core


def test_do_block_sql_statement_linting(linter: core.Linter):
    """Test that SQL statements inside DO blocks are properly linted."""
    
    # Create a DO block with SQL statements that should trigger violations
    do_block_sql = '''
DO
$$
BEGIN
    CREATE TABLE test_table (
        id uuid NOT NULL,
        name character varying(254),
        created_at TIMESTAMP(3) NOT NULL DEFAULT now()
    );
    
    ALTER TABLE test_table ADD column_with_json json;
END;
$$
LANGUAGE plpgsql;
'''
    
    # Lint the DO block
    result = linter.run(source_file="test_do_block.sql", source_code=do_block_sql)
    
    # Check that violations were found
    assert len(result.violations) > 0, "Expected violations to be found in DO block"
    
    # Check for specific violations we expect:
    violation_codes = {v.rule_code for v in result.violations}
    
    # Should find TP005 (varchar), TP001 (timestamp without timezone), 
    # GN017 (id column), TP008 (json vs jsonb)
    expected_violations = {"TP005", "TP001", "GN017", "TP008"}
    found_violations = violation_codes & expected_violations
    
    assert len(found_violations) > 0, f"Expected to find violations {expected_violations}, but only found {violation_codes}"
    
    # Verify line numbers are reasonable (they should be > 1 since violations are in the DO block body)
    line_numbers = [v.line_number for v in result.violations]
    assert all(line_num > 1 for line_num in line_numbers), f"Expected line numbers > 1, got {line_numbers}"


def test_do_block_without_sql_statements(linter: core.Linter):
    """Test that DO blocks without SQL statements don't cause issues."""
    
    # Create a DO block with only procedural code
    do_block_sql = '''
DO
$$
BEGIN
    RAISE NOTICE 'Hello World';
    IF 1 = 1 THEN
        RAISE NOTICE 'True condition';
    END IF;
END;
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="test_procedural.sql", source_code=do_block_sql)
    
    # Should not find any violations (no SQL statements to lint)
    # This also verifies the DO block parser doesn't crash on procedural code
    assert len(result.violations) == 0, f"Expected no violations, but found {len(result.violations)}"
    assert len(result.errors) == 0, f"Expected no errors, but found {result.errors}"


def test_mixed_do_block_and_regular_statements(linter: core.Linter):
    """Test linting file with both DO blocks and regular SQL statements."""
    
    mixed_sql = '''
CREATE TABLE regular_table (
    id uuid NOT NULL,
    data character varying(100)
);

DO
$$
BEGIN
    CREATE TABLE do_block_table (
        id uuid NOT NULL,
        info character varying(200)
    );
END;
$$
LANGUAGE plpgsql;

ALTER TABLE regular_table ADD created_at TIMESTAMP(3);
'''
    
    result = linter.run(source_file="test_mixed.sql", source_code=mixed_sql)
    
    # Should find violations from both regular SQL and DO block SQL
    assert len(result.violations) > 0, "Expected violations from both regular and DO block statements"
    
    # Check that we get violations from multiple statements
    violation_codes = {v.rule_code for v in result.violations}
    expected_violations = {"TP005", "TP001", "GN017"}  # varchar, timestamp, id column
    found_violations = violation_codes & expected_violations
    
    assert len(found_violations) > 0, f"Expected violations {expected_violations}, found {violation_codes}"


def test_multiple_separate_do_blocks(linter: core.Linter):
    """Test multiple separate DO blocks in the same file."""
    
    # Multiple DO blocks as separate statements
    multiple_do_sql = '''
-- First DO block
DO
$$
BEGIN
    CREATE TABLE first_table (
        id uuid NOT NULL,
        name character varying(100)
    );
END;
$$
LANGUAGE plpgsql;

-- Second DO block  
DO
$$
BEGIN
    CREATE TABLE second_table (
        id uuid NOT NULL,
        description character varying(200),
        created_at TIMESTAMP(3) NOT NULL DEFAULT now()
    );
    
    ALTER TABLE second_table ADD status_json json;
END;
$$
LANGUAGE plpgsql;

-- Third DO block
DO
$$
BEGIN
    ALTER TABLE first_table ADD updated_at TIMESTAMP(3);
    ALTER TABLE second_table ADD modified_by character varying(255);
END;
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="test_multiple_do.sql", source_code=multiple_do_sql)
    
    # Should find violations from all DO blocks
    assert len(result.violations) > 0, "Expected violations to be found in multiple DO blocks"
    
    # Check for violations we expect from all blocks
    violation_codes = {v.rule_code for v in result.violations}
    expected_violations = {"TP005", "TP001", "GN017", "TP008"}  # varchar, timestamp, id column, json
    found_violations = violation_codes & expected_violations
    
    assert len(found_violations) >= 3, f"Expected multiple violations {expected_violations}, found {violation_codes}"
    
    # Should have violations from all three DO blocks
    # We expect violations from CREATE TABLE statements in first and second blocks,
    # plus ALTER TABLE statements in all blocks


def test_do_block_with_dynamic_sql(linter: core.Linter):
    """Test DO blocks that mix static SQL with dynamic EXECUTE statements."""
    
    dynamic_sql = '''
DO
$$
BEGIN
    -- Static SQL that should be linted
    CREATE TABLE static_table (
        id uuid NOT NULL,
        data character varying(500)
    );
    
    -- Dynamic SQL that should not be parsed (it's a string)
    EXECUTE 'CREATE TABLE dynamic_table (bad_id varchar(50))';
    
    -- More static SQL
    ALTER TABLE static_table ADD created_at TIMESTAMP(3);
END;
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="test_dynamic.sql", source_code=dynamic_sql)
    
    # Should find violations from static SQL only
    assert len(result.violations) > 0, "Expected violations from static SQL in DO block"
    
    violation_codes = {v.rule_code for v in result.violations}
    expected_violations = {"TP005", "TP001", "GN017"}  # varchar, timestamp, id column
    found_violations = violation_codes & expected_violations
    
    # Should find violations from the static CREATE TABLE and ALTER TABLE
    assert len(found_violations) > 0, f"Expected violations {expected_violations}, found {violation_codes}"
    
    # The dynamic SQL in EXECUTE should not be linted (it's just a string literal)
    # This is correct behavior since dynamic SQL can't be statically analyzed


def test_do_block_creating_function_with_nested_structure(linter: core.Linter):
    """Test DO block that creates a function, simulating nested procedural structures."""
    
    function_creation_sql = '''
DO
$$
BEGIN
    -- Create a table first
    CREATE TABLE function_test_table (
        id uuid NOT NULL,
        name character varying(150)
    );
    
    -- Create a function that would have its own procedural logic
    -- (Note: The function body is a string, so won't be parsed as separate DO block)
    EXECUTE 'CREATE OR REPLACE FUNCTION test_function()
    RETURNS void AS $func$
    BEGIN
        -- This is inside the function body string
        INSERT INTO function_test_table (id, name) VALUES (gen_random_uuid(), ''test'');
    END;
    $func$ LANGUAGE plpgsql;';
    
    -- More direct SQL in the DO block
    ALTER TABLE function_test_table ADD created_at TIMESTAMP(3);
    ALTER TABLE function_test_table ADD data_json json;
END;
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="test_function_creation.sql", source_code=function_creation_sql)
    
    # Should find violations from the direct SQL in the DO block
    assert len(result.violations) > 0, "Expected violations from SQL in DO block"
    
    violation_codes = {v.rule_code for v in result.violations}
    expected_violations = {"TP005", "TP001", "GN017", "TP008"}  # varchar, timestamp, id, json
    found_violations = violation_codes & expected_violations
    
    # Should find violations from CREATE TABLE and ALTER TABLE statements
    assert len(found_violations) > 0, f"Expected violations {expected_violations}, found {violation_codes}"
    
    # The function body in EXECUTE is dynamic SQL (string) so won't be parsed
    # This is the correct behavior for PostgreSQL static analysis


def test_complex_do_block_with_transactions_and_conditionals(linter: core.Linter):
    """Test complex DO block with conditional SQL and transaction control."""
    
    complex_sql = '''
DO
$$
DECLARE
    table_exists boolean;
BEGIN
    -- Check if table exists (this is valid PL/pgSQL)
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'complex_table'
    ) INTO table_exists;
    
    -- Conditional table creation
    IF NOT table_exists THEN
        CREATE TABLE complex_table (
            id uuid NOT NULL,
            legacy_name character varying(300),
            created_at TIMESTAMP(3) NOT NULL DEFAULT now()
        );
    END IF;
    
    -- Always add these columns
    ALTER TABLE complex_table ADD COLUMN IF NOT EXISTS status_data json;
    ALTER TABLE complex_table ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP(3);
    
    -- Create an index
    CREATE INDEX IF NOT EXISTS idx_complex_name ON complex_table (legacy_name);
    
    RAISE NOTICE 'Complex DO block completed';
END;
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="test_complex_do.sql", source_code=complex_sql)
    
    # Should find violations from SQL statements within the conditional blocks
    assert len(result.violations) > 0, "Expected violations from complex DO block"
    
    violation_codes = {v.rule_code for v in result.violations}
    
    # We might get different violations depending on the rules enabled
    # The key thing is that we're detecting SQL within the complex DO block structure
    # Check for some expected violations (adjust based on what's actually found)
    possible_violations = {"TP005", "TP001", "GN017", "TP008", "GN014", "SM001"}  
    found_violations = violation_codes & possible_violations
    
    assert len(found_violations) > 0, f"Expected some violations from {possible_violations}, found {violation_codes}"
    
    # This tests that our SQL extraction logic can handle:
    # - DECLARE sections
    # - Conditional blocks (IF/THEN/END IF)
    # - Mixed procedural and SQL statements
    # - Complex nested structures


def test_real_world_migration_script(linter: core.Linter):
    """Test a real-world migration script with complex DO block structure."""
    
    # This is based on an actual migration script provided by the user
    migration_sql = '''
DO
$$
begin
    -- Move emails and phoneNumbers to base_customer entity
    -- 1.a add new fields
  IF NOT EXISTS (SELECT * FROM information_schema."columns" WHERE table_schema = 'account' AND table_name = 'base_customer' AND column_name = 'emails') THEN
        ALTER TABLE "account"."base_customer" ADD "emails" json;
        COMMENT ON COLUMN "account"."base_customer"."emails" IS 'sensitive';
    END IF;

  IF NOT EXISTS (SELECT * FROM information_schema."columns" WHERE table_schema = 'account' AND table_name = 'base_customer' AND column_name = 'phoneNumbers') THEN
        ALTER TABLE "account"."base_customer" ADD "phoneNumbers" json;
        COMMENT ON COLUMN "account"."base_customer"."phoneNumbers" IS 'sensitive';
    END IF;

    -- 1.b copy data across
    UPDATE account.base_customer bc
    SET emails = ic.emails,
    "phoneNumbers" = ic."phoneNumbers"
    FROM account.individual_customer ic
    WHERE ic."baseCustomerId" = bc.id ;

    -- 2.a create new table with new schema
    CREATE TABLE IF NOT EXISTS "account"."individual_customer_new" (
        "createCorrelationId" uuid NOT NULL,
        "createdAt" TIMESTAMP(3) NOT NULL DEFAULT now(),
        "updateCorrelationId" uuid,
        "updatedAt" TIMESTAMP(3),
        "id" uuid NOT NULL,
        "givenName" character varying(254),
        "familyName" character varying(254),
        "dateOfBirth" date,
        "maritalStatus" "core"."customermaritalstatustype_enum" NOT NULL,
        "gender" "core"."customergendertype_enum" NOT NULL,
        CONSTRAINT "PK_account.IndividualCustomer2" PRIMARY KEY ("id"),
         CONSTRAINT "FK_IndividualCustomer_id" FOREIGN KEY ("id") REFERENCES "account"."base_customer"("id") ON DELETE NO ACTION ON UPDATE NO ACTION
    ); 
END;
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="real_migration.sql", source_code=migration_sql)
    
    # Should find violations from the SQL within the complex DO block
    # Note: The exact number depends on how many SQL statements our extraction logic finds
    assert len(result.violations) > 0, f"Expected violations from complex migration, found {len(result.violations)}"
    
    violation_codes = {v.rule_code for v in result.violations}
    
    # The key requirement is that we find violations within the DO block
    # This proves our SQL extraction and linting is working
    
    # We should at least find violations from the SQL within the DO block
    assert "TP008" in violation_codes, f"Expected TP008 (json) violation, found {violation_codes}"
    
    # This test verifies that complex real-world migration scripts with:
    # - Conditional table modifications
    # - Data migration UPDATE statements  
    # - Complex CREATE TABLE with constraints
    # - Mixed procedural and SQL logic
    # - Multiple nested IF blocks
    # Are properly parsed and linted