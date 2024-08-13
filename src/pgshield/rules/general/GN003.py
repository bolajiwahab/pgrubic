"""Checker for SQL_ASCII encoding."""

from pglast import ast

from pgshield.core import linter


class SqlAsciiEncoding(linter.Checker):
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
        ancestors: ast.Node,
        node: ast.DefElem,
    ) -> None:
        """Visit DefElem."""
        if node.defname == "encoding" and node.arg.sval == "sql_ascii":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Found SQL_ASCII encoding",
                ),
            )

            if self.is_fix_applicable:

                node.arg.sval = "utf8"
