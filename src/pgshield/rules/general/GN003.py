"""Checker for SQL_ASCII encoding."""

import re

from pglast import ast, stream

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
    is_auto_fixable: bool = False

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreatedbStmt,
    ) -> None:
        """Visit CreatedbStmt."""
        options: dict[str, str] = (
            {
                re.sub(r"\s*", "", stream.RawStream()(option), flags=re.UNICODE)
                .split("=")[0]: re.sub(
                    r"\s*",
                    "",
                    stream.RawStream()(option),
                    flags=re.UNICODE,
                )
                .split("=")[1]
                .strip("'")
                for option in node.options
            }
            if node.options is not None
            else {}
        )

        if options.get("encoding") == "sql_ascii":

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer non sql_ascii encoding",
                ),
            )
