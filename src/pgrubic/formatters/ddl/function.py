"""Formatter for function/procedure."""

from pglast import ast, enums, stream, printers

from pgrubic.core import Formatter, noqa, config

_config: config.Config = config.parse_config()


@printers.node_printer(ast.CreateFunctionStmt, override=True)
def create_function_stmt(
    node: ast.CreateFunctionStmt,
    output: stream.RawStream,
) -> None:
    """Printer for CreateFunctionStmt."""
    output.write("CREATE")
    output.space()

    if node.replace:
        output.write("OR REPLACE")
        output.space()

    if node.is_procedure:
        output.write("PROCEDURE")
    else:
        output.write("FUNCTION")

    output.space()
    output.print_name(node.funcname)
    output.space()

    if node.parameters:
        actual_parameters = node.parameters
        # When returning table, the column definitions are mixed with
        # the usual parameters, so we need to extract the column definitions
        table_definition = []

        if node.returnType and node.returnType.setof:
            # Recreate the actual parameters
            actual_parameters = []

            for param in node.parameters:
                if param.mode == enums.FunctionParameterMode.FUNC_PARAM_TABLE:
                    table_definition.append(param)
                else:
                    actual_parameters.append(param)
    else:
        actual_parameters = []
        table_definition = []

    with output.push_indent(relative=False):
        output.write("(")

        if actual_parameters:
            output.newline()
            output.space(4)
            output.print_list(actual_parameters)
            output.newline()

        output.write(")")

    if node.returnType:
        output.newline()
        output.writes("RETURNS")
        if node.returnType.setof and table_definition:
            # Do not treat them as arguments
            output.write("TABLE")
            output.space()

            with output.push_indent(relative=False):
                output.write("(")
                output.newline()
                output.space(4)
                output.print_list(table_definition)
                output.newline()
                output.write(")")
        else:
            output.print_node(node.returnType)

    if node.options:
        # Move "AS" to the end
        options = [x for x in node.options if x.defname.upper() != "AS"] + [
            x for x in node.options if x.defname.upper() == "AS"
        ]

        output.newline()

        for i, option in enumerate(options):
            output.print_node(option)
            # Add newline until the last option
            if i < len(options) - 1:
                output.newline()

    if node.sql_body:
        if node.is_procedure:
            output.newline()
            output.write("BEGIN ATOMIC")
            output.newline()
            if node.sql_body:
                output.space(4)
                with output.push_indent():
                    for i, stmt in enumerate(node.sql_body[0]):
                        output.print_node(stmt)

                        if not _config.format.new_line_before_semicolon:
                            output.write(noqa.SEMI_COLON)
                        else:  # pragma: no cover
                            output.write(noqa.NEW_LINE + noqa.SEMI_COLON)

                        # Add newline until the last statement
                        if i < len(node.sql_body[0]) - 1:
                            for _ in range(_config.format.lines_between_statements + 1):
                                output.newline()

            output.newline()
            output.write("END")
        else:
            output.newline()
            output.print_node(node.sql_body)


@printers.node_printer(
    (ast.AlterFunctionStmt, ast.CreateFunctionStmt, ast.DoStmt),
    ast.DefElem,
    override=True,
)
def create_function_option(  # noqa: PLR0911
    node: ast.CreateFunctionStmt | ast.AlterFunctionStmt | ast.DoStmt,
    output: stream.RawStream,
) -> None:
    """Printer for function options."""
    option = node.defname

    if option.upper() == "AS":
        if isinstance(node.arg, tuple) and len(node.arg) > 1:
            # This form of the AS clause is used for dynamically loadable C language
            # functions when the function name in the C language source code is not the
            # same as the name of the SQL function.
            # https://www.postgresql.org/docs/current/sql-createfunction.html#:~:text=obj_file%2C%20link_symbol
            output.write("AS")
            output.space()
            output.print_list(node.arg, standalone_items=False)
            return

        if isinstance(abs(node.ancestors).node, ast.CreateFunctionStmt):
            # We could use (abs(node.ancestors).node.sql_body) to check if it is a
            # sql function but sql_body is only populated for the new syntax
            # https://www.postgresql.org/docs/14/sql-createfunction.html#:~:text=a%20new%20session.-,sql_body,-The%20body%20of
            is_sql_function = False

            for ancestor in node.ancestors.node:
                if (
                    ancestor.defname.upper() == "LANGUAGE"
                    and ancestor.arg.sval.upper() == "SQL"
                ):
                    is_sql_function = True
                    break

            output.write("AS")
            output.space()

        function_body: str = (
            node.arg[0].sval if isinstance(node.arg, tuple) else node.arg.sval
        )

        function_body = (
            function_body + noqa.SEMI_COLON
            if not function_body.strip().endswith(noqa.SEMI_COLON)
            else function_body
        )

        output.write("$BODY$")

        if is_sql_function:
            # We do not need to track errors here as the whole SQL function is already
            # parsed by the parser
            formatted_function_body, _ = Formatter.run(
                source_code=function_body,
                source_file="function_body",
                config=_config,
            )

            # indent the non empty lines of the formatted function body by 4 spaces
            formatted_function_body = noqa.NEW_LINE.join(
                (noqa.SPACE * 4 + line if line.strip() else "")
                for line in formatted_function_body.splitlines()
            )
            output.newline()
            output.write(formatted_function_body)
            output.newline()
        else:
            output.newline()
            output.write(function_body.strip(noqa.NEW_LINE))
            output.newline()

        output.write("$BODY$")
        return

    if option.upper() == "SECURITY":
        if node.arg.boolval:
            output.swrite("SECURITY DEFINER")
        else:
            output.swrite("SECURITY INVOKER")
        return

    if option.upper() == "STRICT":
        output.swrite(
            (
                "RETURNS NULL ON NULL INPUT"
                if node.arg.boolval
                else "CALLED ON NULL INPUT"
            ),
        )
        return

    if option.upper() == "VOLATILITY":
        output.separator()
        output.write(node.arg.sval.upper())
        return

    if option.upper() == "PARALLEL":
        output.swrite("PARALLEL")
        output.space()
        output.print_symbol(node.arg.sval.upper())
        return

    if option.upper() == "LEAKPROOF":
        if not node.arg.boolval:
            output.swrite("NOT")
        output.swrite("LEAKPROOF")
        return

    if option.upper() == "SET":
        output.separator()
        output.print_node(node.arg)
        return

    if option.upper() == "WINDOW":
        output.write("WINDOW")
        return

    if option.upper() == "LANGUAGE":
        output.write("LANGUAGE")
        output.space()
        if node.arg.sval.upper() in ("SQL", "C"):
            output.print_symbol(node.arg.sval.upper())
        else:
            output.print_symbol(node.arg.sval)
        return

    output.write(node.defname.upper())
    output.space()
    output.print_symbol(node.arg)


@printers.node_printer(ast.AlterFunctionStmt, override=True)
def alter_function_stmt(node: ast.AlterFunctionStmt, output: stream.RawStream) -> None:
    """Printer for AlterFunctionStmt."""
    output.write("ALTER")
    output.space()
    if node.objtype == enums.ObjectType.OBJECT_PROCEDURE:
        output.write("PROCEDURE")
        output.space()
    else:
        output.write("FUNCTION")
        output.space()
    output.print_node(node.func)
    with output.push_indent(relative=False):
        output.newline()
        output.space(4)
        output.print_list(node.actions, noqa.SPACE, standalone_items=True)
