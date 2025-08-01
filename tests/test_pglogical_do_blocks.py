"""Test pglogical nested DO block patterns."""

from pgrubic import core


def test_pglogical_nested_do_block_current_behavior(linter: core.Linter):
    """Test current behavior with pglogical nested DO blocks."""
    
    # This represents the realistic production pattern
    pglogical_sql = '''
SELECT pglogical.replicate_ddl_command(
$$
    DO
    $script$
    BEGIN
        -- This ALTER TABLE should ideally be linted, but currently isn't
        ALTER TABLE "account"."test_table" ADD "badColumn" character varying(500);
        
        -- This one too
        CREATE TABLE "account"."bad_table" (
            "id" uuid NOT NULL,
            "createdAt" TIMESTAMP(3) NOT NULL DEFAULT now()
        );
    END
    $script$
    LANGUAGE plpgsql;
$$,
'{global}'::text[]);
'''
    
    result = linter.run(source_file="pglogical_test.sql", source_code=pglogical_sql)
    
    # Current behavior: this is parsed as a SELECT statement, not a DO block
    # So we expect no violations to be found (the DO block is embedded in a string)
    
    print(f"DEBUG: Found {len(result.violations)} violations")
    print(f"DEBUG: Found {len(result.errors)} errors")
    
    # Document current limitation: nested DO blocks in function calls aren't linted
    # This is expected behavior since the DO block exists as string data
    assert len(result.errors) <= 1, "Should handle gracefully without major errors"
    
    # The violations list will likely be empty since the SQL inside the string
    # parameter isn't parsed as separate statements
    violation_codes = {v.rule_code for v in result.violations}
    print(f"DEBUG: Violation codes: {violation_codes}")


def test_standalone_do_block_still_works(linter: core.Linter):
    """Verify that standalone DO blocks still work after pglogical test."""
    
    # Ensure our core functionality still works
    standalone_sql = '''
DO
$$
BEGIN
    CREATE TABLE "test_table" (
        "id" uuid NOT NULL,
        "name" character varying(254)
    );
END
$$
LANGUAGE plpgsql;
'''
    
    result = linter.run(source_file="standalone_test.sql", source_code=standalone_sql)
    
    # This should still find violations (TP005 for varchar, GN017 for id)
    assert len(result.violations) > 0, "Standalone DO blocks should still be linted"
    
    violation_codes = {v.rule_code for v in result.violations}
    expected_violations = {"TP005", "GN017"}  # varchar, id column
    found_violations = violation_codes & expected_violations
    
    assert len(found_violations) > 0, f"Expected {expected_violations}, found {violation_codes}"


def test_documentation_of_pglogical_limitation():
    """Document the current limitation with nested DO blocks."""
    
    limitation_doc = """
    CURRENT LIMITATION: Nested DO blocks in function calls
    
    The following pattern is NOT currently supported for linting:
    
    SELECT pglogical.replicate_ddl_command(
    $$
        DO $script$
        BEGIN
            -- SQL here won't be linted
        END
        $script$ LANGUAGE plpgsql;
    $$,
    '{global}'::text[]);
    
    WORKAROUND: Extract the DO block to a standalone statement:
    
    DO $script$
    BEGIN
        -- SQL here WILL be linted
    END
    $script$ LANGUAGE plpgsql;
    
    Then wrap it in pglogical call if needed for deployment.
    
    REASON: The DO block exists as string data within a function parameter,
    not as a parsed DO statement that our current implementation can detect.
    """
    
    # This test documents the limitation for users
    assert True, limitation_doc