"""Formatter for CREATE TABLE statements."""

from pglast import ast, enums, stream, printers

from pgrubic.formatters.ddl import IF_NOT_EXISTS


@printers.node_printer(ast.PartitionSpec, override=True)
def partition_spec(node: ast.PartitionSpec, output: stream.RawStream) -> None:
    """Printer for PartitionSpec."""
    strategy = {
        enums.PartitionStrategy.PARTITION_STRATEGY_LIST: "LIST",
        enums.PartitionStrategy.PARTITION_STRATEGY_RANGE: "RANGE",
        enums.PartitionStrategy.PARTITION_STRATEGY_HASH: "HASH",
    }[node.strategy]
    output.print_symbol(strategy)
    output.space()
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
    output.space()
    output.write("AS")
    output.newline()
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
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.tableElts)
            output.newline()
    elif node.partbound:
        output.newline()
        output.space()
    elif not node.ofTypename:
        output.space()
        output.swrites("()")
    with output.push_indent(-1):
        first = True
        if node.inhRelations and not node.partbound:
            output.swrites("INHERITS")
            output.space()
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
            output.space()
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
