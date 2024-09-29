"""Checker for non snake case identifiers."""

from pglast import stream

from pgrubic.core import linter
from pgrubic.rules.naming import CheckIdentifier


class NonSnakeCaseIdentifier(CheckIdentifier):
    """## **What it does**
    Check if identifier is not in snake case.

    ## **Why not?**
    PostgreSQL folds all names - of tables, columns, functions and everything else - to
    lower case unless they're "double quoted".
    So `create table Foo()` will create a table called foo, while `create table "Bar"()`
    will create a table called Bar.

    These select commands will work: `select * from Foo`, `select * from foo`,
    `select * from "Bar"`.

    These will fail with "no such table": `select * from "Foo"`, `select * from Bar`,
    `select * from bar`.

    This means that if you use uppercase characters in your table or column names you
    have to either always double quote them or never double quote them.
    That's annoying enough by hand, but when you start using other tools to access the
    database, some of which always quote all names and some don't, it gets very confusing.

    ## **When should you?**
    Never ... almost.
    If it is important that "pretty" names are displaying in report output then you might
    want to use them. But you can also use column aliases to use lower case names in a
    table and still get pretty names in the output of a query:
    > select character_name as "Character Name" from foo.

    ## **Use instead:**
    Stick to using a-z, 0-9 and underscore for names and you never have to worry about
    quoting them.
    """

    is_auto_fixable: bool = False

    def _check_identifier(
        self,
        identifier: str,
        line_number: int,
        column_offset: int,
        source_text: str,
        statement_location: int,
    ) -> None:
        """Check if identifier is not in snake case."""
        if identifier and not stream.is_simple_name(identifier):

            self.violations.add(
                linter.Violation(
                    line_number=line_number,
                    column_offset=column_offset,
                    source_text=source_text,
                    statement_location=statement_location,
                    description=f"Identifier `{identifier}` should be in snake case",
                ),
            )
