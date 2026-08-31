"""Formatter for table."""

import typing

from pglast import ast, enums, printers

from pgrubic.core import formatter
from pgrubic.formatters.ddl import IF_EXISTS, IF_NOT_EXISTS


@printers.node_printer(ast.IntoClause, override=True)
def into_clause(node: ast.IntoClause, output: formatter.PrinterOutput) -> None:
    """Printer for IntoClause."""
    output.print_node(node.rel)

    if node.colNames:
        output.space()
        with output.expression(need_parens=True):
            output.print_name(node.colNames, ",")

    if node.accessMethod:
        output.newline()
        output.write("USING")
        output.space()
        output.print_name(node.accessMethod)

    if node.options:
        output.newline()
        output.write("WITH")
        output.space()
        output.print_parenthesized_list(
            node.options,
            closing_indent=0,
            continuation_indent=4,
        )

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
def partition_spec(node: ast.PartitionSpec, output: formatter.PrinterOutput) -> None:
    """Printer for PartitionSpec."""
    strategy_type = typing.cast(enums.PartitionStrategy, node.strategy)
    part_params = typing.cast(tuple[ast.PartitionElem, ...], node.partParams)
    strategy = {
        enums.PartitionStrategy.PARTITION_STRATEGY_LIST: "LIST",
        enums.PartitionStrategy.PARTITION_STRATEGY_RANGE: "RANGE",
        enums.PartitionStrategy.PARTITION_STRATEGY_HASH: "HASH",
    }[strategy_type]

    output.print_symbol(strategy)
    output.space()
    with output.expression(need_parens=True):
        output.print_list(nodes=part_params, standalone_items=False)


@printers.node_printer(ast.CreateTableAsStmt, override=True)
def create_table_as_stmt(
    node: ast.CreateTableAsStmt,
    output: formatter.PrinterOutput,
) -> None:
    """Printer for CreateTableAsStmt."""
    into = typing.cast(ast.IntoClause, node.into)
    relation = typing.cast(ast.RangeVar, into.rel)
    output.writes("CREATE")
    output.space()

    if relation.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.writes("TEMPORARY")
    elif relation.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.writes("UNLOGGED")

    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])

    if node.if_not_exists:
        output.writes(IF_NOT_EXISTS)

    output.print_node(into)
    output.swrite("AS")
    output.newline()
    output.print_node(node.query)

    if into.skipData:
        output.newline()
        output.space(2)
        output.write("WITH NO DATA")


@printers.node_printer(ast.CreateForeignTableStmt, override=True)
def create_foreign_table_stmt(
    node: ast.CreateForeignTableStmt,
    output: formatter.PrinterOutput,
) -> None:
    """Printer for CreateForeignTableStmt."""
    base = typing.cast(ast.CreateStmt, node.base)
    output.print_node(base)
    output.newline()

    if base.partbound:
        output.space(4)

    output.write("SERVER")
    output.space()
    output.print_name(node.servername)

    if node.options:
        output.newline()
        if base.partbound:
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
    output: formatter.PrinterOutput,
) -> None:
    """Printer for CreateStmt."""
    relation = typing.cast(ast.RangeVar, node.relation)
    clause_indent = 4 if node.partbound else 0

    output.writes("CREATE")

    if isinstance(node.ancestors[0], ast.CreateForeignTableStmt):
        output.writes("FOREIGN")
    elif relation.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.writes("TEMPORARY")
    elif relation.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.writes("UNLOGGED")

    output.writes("TABLE")

    if node.if_not_exists:
        output.writes(IF_NOT_EXISTS)

    output.print_node(relation)

    if node.ofTypename:
        output.space()
        output.write("OF")
        output.space()
        output.print_name(node.ofTypename)

    if node.partbound:
        inherited_relations = typing.cast(tuple[ast.RangeVar, ...], node.inhRelations)
        output.newline()
        output.space(4)
        output.write("PARTITION OF")
        output.space()
        output.print_list(inherited_relations)

    if node.tableElts:
        # move table constraints to the end
        columns = [x for x in node.tableElts if not isinstance(x, ast.Constraint)] + [
            x for x in node.tableElts if isinstance(x, ast.Constraint)
        ]
        output.space(force=True)

        with output.expression(need_parens=True):
            output.newline()
            output.space(clause_indent + 4)
            output.print_list(columns)
            output.newline()
            output.space(clause_indent)
    elif node.partbound:
        output.write_empty_string()
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
        output.space(clause_indent)
        output.write("USING")
        output.space()
        output.print_name(node.accessMethod)

    if node.options:
        output.newline()
        output.space(clause_indent)
        output.write("WITH")
        output.space()
        output.print_parenthesized_list(
            node.options,
            closing_indent=clause_indent,
            continuation_indent=clause_indent + 4,
        )

    if node.tablespacename:
        output.newline()
        output.space(clause_indent)
        output.write("TABLESPACE")
        output.space()
        output.print_name(node.tablespacename)


@printers.node_printer(ast.AlterTableStmt, override=True)
def alter_table_stmt(
    node: ast.AlterTableStmt,
    output: formatter.PrinterOutput,
) -> None:
    """Printer for AlterTableStmt."""
    commands = typing.cast(tuple[ast.AlterTableCmd, ...], node.cmds)
    output.write("ALTER")
    output.space()
    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])

    if node.missing_ok:
        output.write(IF_EXISTS)

    output.space()
    output.print_node(node.relation)
    output.newline()
    output.space(4)
    output.print_list(nodes=commands, standalone_items=True)
