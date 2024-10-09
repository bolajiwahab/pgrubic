"""DDL formatter."""

from pglast import ast, enums, stream, printers

IF_NOT_EXISTS: str = "IF NOT EXISTS"
IF_EXISTS: str = "IF EXISTS"


@printers.node_printer(ast.IndexStmt, override=True)
def index_stmt(node: ast.IndexStmt, output: stream.RawStream) -> None:
    """Printer for IndexStmt."""
    output.write("CREATE")
    output.space(1)
    if node.unique:
        output.write("UNIQUE")
        output.space(1)
    output.write("INDEX")
    output.space(1)
    if node.concurrent:
        output.write("CONCURRENTLY")
        output.space(1)
    if node.if_not_exists:
        output.write(IF_NOT_EXISTS)
        output.space(1)
    if node.idxname:
        output.print_name(node.idxname)
    output.newline()
    with output.push_indent(4):
        output.write("ON")
        output.space(1)
        output.print_node(node.relation)
        if node.accessMethod != "btree":
            output.write("USING")
            output.space(1)
            output.print_name(node.accessMethod)
        output.space(1)
        output.swrite("(")
        output.print_list(node.indexParams, standalone_items=False)
        output.swrite(")")
        if node.indexIncludingParams:
            output.newline()
            output.write("INCLUDE")
            output.space(1)
            output.swrite("(")
            output.print_list(node.indexIncludingParams, standalone_items=False)
            output.swrite(")")
        if node.options:
            output.newline()
            output.write("WITH")
            output.space(1)
            with output.expression(need_parens=True):
                output.print_list(node.options)
        if node.tableSpace:
            output.newline()
            output.write("TABLESPACE")
            output.space(1)
            output.print_name(node.tableSpace)
        if node.whereClause:
            output.newline()
            output.write("WHERE")
            output.space(1)
            output.print_node(node.whereClause)
        if node.nulls_not_distinct:
            output.newline()
            output.write("NULLS NOT DISTINCT")


@printers.node_printer(ast.AlterTableStmt, override=True)
def alter_table_stmt(node: ast.AlterTableStmt, output: stream.RawStream) -> None:
    """Printer for AlterTableStmt."""
    output.write("ALTER")
    output.space(1)
    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])
    if node.missing_ok:
        output.write(IF_EXISTS)
    output.space(1)
    output.print_node(node.relation)
    output.newline()
    output.space(4)
    if len(node.cmds) > 1:
        with output.push_indent():
            output.print_list(node.cmds, ",")
    else:
        output.print_list(node.cmds, ",", standalone_items=True)


@printers.node_printer(ast.CreateEnumStmt, override=True)
def create_enum_stmt(node: ast.Node, output: stream.RawStream) -> None:
    """Printer for CreateEnumStmt."""
    output.write("CREATE TYPE")
    output.space(1)
    output.print_name(node.typeName)
    output.write("AS ENUM")
    output.space(1)
    output.write("")
    with output.expression(need_parens=True):
        output.newline()
        output.space(4)
        output.print_list(node.vals, standalone_items=True)
        output.newline()


@printers.node_printer(ast.AlterEnumStmt, override=True)
def alter_enum_stmt(node: ast.AlterEnumStmt, output: stream.RawStream) -> None:
    """Printer for AlterEnumStmt."""
    output.write("ALTER TYPE")
    output.space(1)
    output.print_name(node.typeName)
    output.newline()
    output.space(4)
    if node.newVal:
        if node.oldVal:
            output.write("RENAME VALUE")
            output.space(1)
            output.write_quoted_string(node.oldVal)
            output.write("TO")
            output.space(1)
        else:
            output.write("ADD VALUE")
            if node.skipIfNewValExists:
                output.space(1)
                output.write(IF_NOT_EXISTS)
            output.space(1)
        output.write_quoted_string(node.newVal)
    if node.newValNeighbor:
        if node.newValIsAfter:
            output.space(1)
            output.write("AFTER")
            output.space(1)
        else:
            output.space(1)
            output.write("BEFORE")
            output.space(1)
        output.write_quoted_string(node.newValNeighbor)


@printers.node_printer(ast.PartitionSpec, override=True)
def partition_spec(node: ast.PartitionSpec, output: stream.RawStream) -> None:
    """Printer for PartitionSpec."""
    strategy = {
        enums.PartitionStrategy.PARTITION_STRATEGY_LIST: "LIST",
        enums.PartitionStrategy.PARTITION_STRATEGY_RANGE: "RANGE",
        enums.PartitionStrategy.PARTITION_STRATEGY_HASH: "HASH",
    }[node.strategy]
    output.print_symbol(strategy)
    output.space(1)
    with output.expression(need_parens=True):
        output.print_list(node.partParams)


@printers.node_printer(ast.CreateTableAsStmt, override=True)
def create_table_as_stmt(node: ast.CreateTableAsStmt, output: stream.RawStream) -> None:
    """Printer for CreateTableAsStmt."""
    output.writes("CREATE")
    if node.into.rel.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.writes("TEMPORARY")
    elif node.into.rel.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.writes("UNLOGGED")
    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])
    if node.if_not_exists:
        output.writes(IF_NOT_EXISTS)
    output.print_node(node.into)
    output.space(4)
    output.write("AS")
    output.space(1)
    with output.push_indent():
        output.print_node(node.query)
    if node.into.skipData:
        output.newline()
        output.write("WITH NO DATA")


@printers.node_printer(ast.CreateStmt, override=True)
def create_stmt(
    node: ast.CreateStmt,
    output: stream.RawStream,
) -> None:
    """Printer for CreateStmt."""
    output.writes("CREATE")
    if isinstance(node.ancestors[0], ast.CreateForeignTableStmt):
        output.writes("FOREIGN")
    elif node.relation.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.writes("TEMPORARY")
    elif node.relation.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.writes("UNLOGGED")
    output.writes("TABLE")
    if node.if_not_exists:
        output.writes(IF_NOT_EXISTS)
    output.print_node(node.relation)
    if node.ofTypename:
        output.swrites("OF")
        output.print_name(node.ofTypename)
    if node.partbound:
        output.swrites("PARTITION OF")
        output.print_list(node.inhRelations)
    if node.tableElts:
        output.space(1)
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.tableElts)
            output.newline()
    elif node.partbound:
        output.newline()
        output.space(1)
    elif not node.ofTypename:
        output.space(1)
        output.swrites("()")
    with output.push_indent(-1):
        first = True
        if node.inhRelations and not node.partbound:
            output.swrites("INHERITS")
            output.space(1)
            with output.expression(need_parens=True):
                output.print_list(node.inhRelations)
            first = False
        if node.partbound:
            if first:
                first = False
            else:  # pragma: no cover
                output.newline()
            output.space(2)
            output.print_node(node.partbound)
        if node.partspec:
            if first:
                first = False
            else:
                output.newline()
            output.newline()
            output.writes("PARTITION BY")
            output.print_node(node.partspec)
        if node.options:
            if first:
                first = False
            else:
                output.newline()
            output.newline()
            output.swrites("WITH")
            output.space(1)
            with output.expression(need_parens=True):
                output.newline()
                output.space(4)
                output.print_list(node.options)
                output.newline()
        if node.oncommit != enums.OnCommitAction.ONCOMMIT_NOOP:
            if first:
                first = False
            else:
                output.newline()
            output.swrites("ON COMMIT")
            if node.oncommit == enums.OnCommitAction.ONCOMMIT_PRESERVE_ROWS:
                output.write("PRESERVE ROWS")
            elif node.oncommit == enums.OnCommitAction.ONCOMMIT_DELETE_ROWS:
                output.write("DELETE ROWS")
            elif node.oncommit == enums.OnCommitAction.ONCOMMIT_DROP:
                output.write("DROP")
        if node.tablespacename:
            if first:
                first = False
            else:
                output.newline()
            output.write(" TABLESPACE ")
            output.print_name(node.tablespacename)
    if node.accessMethod:
        output.write(" USING ")
        output.print_name(node.accessMethod)