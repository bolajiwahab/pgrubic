"""Unsafe table operations."""

from pglast import ast, stream

from pgshield.core import linter


class VacuumFull(linter.Checker):
    """Vacuum full."""

    name: str = "unsafe.vacuum_full"
    code: str = "UST006"

    is_auto_fixable: bool = False

    def visit_VacuumStmt(self, ancestors: ast.Node, node: ast.VacuumStmt) -> None:
        """Visit VacuumStmt."""
        options = (
            [stream.RawStream()(option) for option in node.options]
            if node.options is not None
            else []
        )

        if options and "full" in options:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Vacuum full",
                ),
            )
