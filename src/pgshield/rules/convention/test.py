"""Test."""



from typing import ClassVar

from pglast import ast, enums, stream, keywords, visitors, parse_sql  # type: ignore[import-untyped]

# from pgshield import utils, linter

# from ...linter import Checker

class UnusedVariableInScopeChecker(visitors.Visitor):
    """Checks if any variables are unused in this node's scope."""

    def __init__(self) -> None:
        # super().__init__()
        # unused_names is a dictionary that stores variable names, and
        # whether or not they've been found in a "Load" context yet.
        # If it's found to be used, its value is turned to False.
        self.identifiers: list[tuple[int, str]] = []
        # self.unused_names: dict[str, bool] = {}

        # name_nodes holds the first occurences of variables.
        # self.name_nodes: dict[str, ast.Node] = {}

    def visit(self, ancestors, node: ast.Node) -> None:  # noqa: ANN401
        """Visit the node."""

    def visit_RawStmt(self, ancestors, node: ast.Node) -> None:
        """Find all nodes that only exist in `Store` context"""
        var_name = node

        print("I am here.")

        # if isinstance(node.ctx, ast.Store):
        #     # If it's a new name, save the node for later
        #     if var_name not in self.name_nodes:
        #         self.name_nodes[var_name] = node

        #     # If we've never seen it before, it is unused.
        #     if var_name not in self.unused_names:
        #         self.unused_names[var_name] = True

        # else:
        #     # It's used somewhere.
        #     self.unused_names[var_name] = False


class UnusedVariableChecker(visitors.Visitor):
    def check_for_unused_variables(self, ancestors, node: ast.Node) -> None:
        """Find unused variables in the local scope of this node."""
        visitor = UnusedVariableInScopeChecker()
        # visitor.visit(ancestors, node)
        visitor.identifiers.append(("statement_index", "node.relation.relname"))
        print(visitor.identifiers)

        # for name, unused in visitor.unused_names.items():
        #     if unused:
        #         node = visitor.name_nodes[name]
        #         self.violations.add(Violation(node, f"Unused variable: {name!r}"))

    # def visit_Module(self, ancestors, node: ast.Node) -> None:
    #     self.check_for_unused_variables(ancestors, node)
    #     # super().generic_visit(ancestors, node)

    def visit_CreateStmt(self, ancestors, node: ast.Node) -> None:
        print("hello")
        self.check_for_unused_variables(ancestors, node)
        print("bye")
        # super().visit(ancestors, node)

    def visit_AlterTableStmt(self, ancestors, node: ast.Node) -> None:
        print("hello1")
        self.check_for_unused_variables(ancestors, node)
        print("bye1")

    # def visit_RawStmt(self, ancestors, node: ast.Node) -> None:
    #     """Find all nodes that only exist in `Store` context"""
    #     var_name = node

    #     print("I am herehjhj.")
    # def visit_FunctionDef(self, ancestors, node: ast.Node) -> None:
    #     self.check_for_unused_variables(ancestors, node)
    #     # super().generic_visit(node)

sql = """
create table foo (id serial primary key, name varchar(20));
alter table boo add column name varchar(20);
"""

raw = parse_sql(sql)

UnusedVariableChecker()(raw)
