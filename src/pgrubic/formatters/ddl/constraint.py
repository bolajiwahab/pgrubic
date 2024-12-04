"""Formatter for CONSTRAINT."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.Constraint, override=True)
def constraint(node: ast.AlterEnumStmt, output: stream.RawStream) -> None:
    """Printer for Constraint."""
    if node.conname:
        output.swrite("CONSTRAINT ")
        output.print_name(node.conname)
        output.newline()
        output.space(6)

    printers.ddl.constr_type_printer(node.contype, node, output)

    if node.indexname:
        output.write(" USING INDEX ")
        output.print_name(node.indexname)
    # Common to UNIQUE & PRIMARY_KEY
    if node.keys:
        output.write(" ")
        with output.expression(need_parens=True):
            output.print_name(node.keys, ",")
    if node.including:
        output.write(" INCLUDE ")
        with output.expression(need_parens=True):
            output.print_list(node.including, ",", are_names=True)
    if node.deferrable:
        output.swrite("DEFERRABLE")
        if node.initdeferred:
            output.swrite("INITIALLY DEFERRED")
    with output.push_indent():
        first = True
        if node.options and node.contype == enums.ConstrType.CONSTR_UNIQUE:
            output.write(" WITH ")
            with output.expression(need_parens=True):
                first_option = True
                for option in node.options:
                    if first_option:
                        first_option = False
                    else:
                        output.write(", ")
                    output.print_name(option.defname)
                    output.write(" = ")
                    output.print_node(option.arg)
            first = False
        if node.indexspace:
            if first:
                first = False
            else:
                output.newline()
            output.write(" USING INDEX TABLESPACE ")
            output.print_name(node.indexspace)
        if node.skip_validation:
            output.write(" NOT VALID")
