"""Checker for drop cascade."""

from pglast import ast, enums, visitors

from pgrubic import get_full_qualified_name
from pgrubic.core import linter


class DropCascade(linter.BaseChecker):
    """## **What it does**
    Checks for usage of cascade update.

    ## **Why not?**
    Database schema should follow the principle of least surprise which
    says that every component in a system should behave in a way that most users
    expect it to behave, and therefore not surprise or astonish them.

    Cascading drops should not cause unexpected loss of data. It is certainly
    dangerous if dropping a single table can wipe out half your database.

    Are you certain you want cascade drop thus dropping every dependent objects?

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Restrict
    """

    is_auto_fixable: bool = True

    def _register_violation(
        self,
        object_name: str,
        line_number: int,
        column_offset: int,
        source_text: str,
        statement_location: int,
    ) -> None:
        """Register violation."""
        self.violations.add(
            linter.Violation(
                line_number=line_number,
                column_offset=column_offset,
                source_text=source_text,
                statement_location=statement_location,
                description=f"Drop cascade on `{object_name}` detected",
            ),
        )

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        for obj in node.objects:
            object_names = getattr(obj, "names", getattr(obj, "objname", obj))

            if node.behavior == enums.DropBehavior.DROP_CASCADE:
                self._register_violation(
                    object_name=get_full_qualified_name(object_names),
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                )

                self._fix_drop(node)

    def _fix_drop(self, node: ast.DropStmt) -> None:
        """Fix violation."""
        node.behavior = enums.DropBehavior.DROP_RESTRICT

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype
            in (
                enums.AlterTableType.AT_DropConstraint,
                enums.AlterTableType.AT_DropColumn,
            )
            and node.behavior == enums.DropBehavior.DROP_CASCADE
        ):
            self._register_violation(
                object_name=node.name,
                line_number=self.line_number,
                column_offset=self.column_offset,
                source_text=self.source_text,
                statement_location=self.statement_location,
            )

            self._fix_alter(node)

    def _fix_alter(self, node: ast.AlterTableCmd) -> None:
        """Fix violation."""
        node.behavior = enums.DropBehavior.DROP_RESTRICT
