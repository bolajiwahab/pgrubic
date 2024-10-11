"""Checker for SQL_ASCII encoding."""

from pglast import ast, visitors

from pgrubic.core import linter


class SqlAsciiEncoding(linter.BaseChecker):
    """## **What it does**
    Checks for SQL_ASCII encoding.

    ## **Why not?**
    SQL_ASCII means "no conversions" for the purpose of all encoding conversion functions.
    That is to say, the original bytes are simply treated as being in the new encoding,
    subject to validity checks, without any regard for what they mean. Unless extreme care
    is taken, an SQL_ASCII database will usually end up storing a mixture of many
    different encodings with no way to recover the original characters reliably.

    ## **When should you?**
    If your input data is already in a hopeless mixture of unlabelled encodings, such as
    IRC channel logs or non-MIME-compliant emails, then SQL_ASCII might be useful as a
    last resort—but consider using bytea first instead, or whether you could autodetect
    UTF8 and assume non-UTF8 data is in some specific encoding such as WIN1252.

    ## **Use instead:**
    UTF8.
    """

    is_auto_fixable: bool = True

    def visit_DefElem(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DefElem,
    ) -> None:
        """Visit DefElem."""
        if node.defname == "encoding" and node.arg.sval.lower() == "sql_ascii":
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="SQL_ASCII encoding detected",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.DefElem) -> None:
        """Fix violation."""
        node.arg.sval = "utf8"
