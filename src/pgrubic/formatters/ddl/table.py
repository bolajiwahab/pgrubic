"""Formatter for table."""

from pglast import ast, enums, stream, printers

from pgrubic.formatters.ddl import IF_EXISTS, IF_NOT_EXISTS


@printers.node_printer(ast.IntoClause, override=True)
def into_clause(node: ast.IntoClause, output: stream.RawStream) -> None:
    """Printer for IntoClause."""
    output.print_node(node.rel)

    if node.colNames:
        output.space()
        with output.expression(need_parens=True):
            output.print_name(node.colNames, ",")

    if node.accessMethod:
        output.newline()
        output.writes("USING")
        output.print_name(node.accessMethod)

    if node.options:
        output.newline()
        output.write("WITH")
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.options)
            output.newline()

    if node.onCommit != enums.OnCommitAction.ONCOMMIT_NOOP:
        output.space()
        output.write("ON COMMIT")
        output.space()
        if node.onCommit == enums.OnCommitAction.ONCOMMIT_PRESERVE_ROWS:
            output.write("PRESERVE ROWS")
        elif node.onCommit == enums.OnCommitAction.ONCOMMIT_DELETE_ROWS:
            output.write("DELETE ROWS")
        elif node.onCommit == enums.OnCommitAction.ONCOMMIT_DROP:
            output.write("DROP")

    if node.tableSpaceName:
        output.newline()
        output.write("TABLESPACE")
        output.space()
        output.print_name(node.tableSpaceName)


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
        output.print_list(nodes=node.partParams, standalone_items=False)


@printers.node_printer(ast.CreateTableAsStmt, override=True)
def create_table_as_stmt(node: ast.CreateTableAsStmt, output: stream.RawStream) -> None:
    """Printer for CreateTableAsStmt."""
    output.writes("CREATE")
    output.space()

    if node.into.rel.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.writes("TEMPORARY")
    elif node.into.rel.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.writes("UNLOGGED")

    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])

    if node.if_not_exists:
        output.writes(IF_NOT_EXISTS)

    output.print_node(node.into)
    output.swrite("AS")
    output.newline()
    output.print_node(node.query)

    if node.into.skipData:
        output.newline()
        output.space(2)
        output.write("WITH NO DATA")


@printers.node_printer(ast.CreateForeignTableStmt, override=True)
def create_foreign_table_stmt(
    node: ast.CreateForeignTableStmt,
    output: stream.RawStream,
) -> None:
    """Printer for CreateForeignTableStmt."""
    output.print_node(node.base)
    output.newline()

    if node.base.partbound:
        output.space(4)

    output.write("SERVER")
    output.space()
    output.print_name(node.servername)

    if node.options:
        output.newline()
        if node.base.partbound:
            output.space(4)
        with output.push_indent():
            output.write("OPTIONS")
            output.space()
            with output.expression(need_parens=True):
                output.newline()
                output.space(4)
                output.print_list(node.options)
                output.newline()


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
        output.space()
        output.write("OF")
        output.space()
        output.print_name(node.ofTypename)

    if node.partbound:
        output.newline()
        output.space(4)
        output.write("PARTITION OF")
        output.space()
        output.print_list(node.inhRelations)

    if node.tableElts:
        # move table constraints to the end
        columns = [x for x in node.tableElts if not isinstance(x, ast.Constraint)] + [
            x for x in node.tableElts if isinstance(x, ast.Constraint)
        ]
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(columns)
            output.newline()
    elif node.partbound:
        output.write("")
    elif not node.ofTypename:
        output.space()
        output.write("()")

    if node.inhRelations and not node.partbound:
        output.newline()
        output.write("INHERITS")
        output.space()
        with output.expression(need_parens=True):
            output.print_list(node.inhRelations)

    if node.partbound:
        output.newline()
        output.space(4)
        output.print_node(node.partbound)

    if node.partspec:
        output.newline()
        output.writes("PARTITION BY")
        output.print_node(node=node.partspec)

    if node.oncommit != enums.OnCommitAction.ONCOMMIT_NOOP:
        output.newline()
        output.write("ON COMMIT")
        output.space()
        if node.oncommit == enums.OnCommitAction.ONCOMMIT_PRESERVE_ROWS:
            output.write("PRESERVE ROWS")
        elif node.oncommit == enums.OnCommitAction.ONCOMMIT_DELETE_ROWS:
            output.write("DELETE ROWS")
        elif node.oncommit == enums.OnCommitAction.ONCOMMIT_DROP:
            output.write("DROP")

    if node.accessMethod:
        output.newline()
        output.writes("USING")
        output.print_name(node.accessMethod)

    if node.options:
        output.newline()
        output.write("WITH")
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.options)
            output.newline()

    if node.tablespacename:
        output.newline()
        output.write("TABLESPACE")
        output.space()
        output.print_name(node.tablespacename)


@printers.node_printer(ast.AlterTableStmt, override=True)
def alter_table_stmt(node: ast.AlterTableStmt, output: stream.RawStream) -> None:
    """Printer for AlterTableStmt."""
    output.write("ALTER")
    output.space()
    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])

    if node.missing_ok:
        output.write(IF_EXISTS)

    output.space()
    output.print_node(node.relation)
    output.newline()
    output.space(4)
    output.print_list(nodes=node.cmds, standalone_items=True)
