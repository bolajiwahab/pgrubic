"""Linter."""

from pglast import ast, enums, prettify, stream, printers  # type: ignore
from pglast.stream import RawStream, IndentedStream
from pglast.visitors import Delete, Visitor, Ancestor
from pglast.parser import parse_sql_json, parse_sql, scan
from typing import NamedTuple
from collections import namedtuple

# from pgshield import errors

import dataclasses


@dataclasses.dataclass(kw_only=True)
class Comment:
    """Representation of an SQL comment."""

    statement_location: int
    text: str


# Comment = namedtuple('Comment', ('location', 'text'))
"A structure to carry information about a single SQL comment."

import re

def _extract_comments(statement: str) -> Comment:

    lines: list[tuple[int, int, str]] = []
    line_offset = 0

    # by = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # r"^\s*--.*\n?|/\*.*?\*/"
    statement = re.sub(r"^\s*--.*\n", "", statement, flags=re.MULTILINE)

    # print(statement)

    for line in statement.split(";"):

        line_length = len(line)
        lines.append((line_offset, line_offset + line_length, line))
        line_offset += line_length + 1

    comments: list[Comment] = []
    # continue_previous = False  # noqa: ERA001
    for token in scan(statement):

        if token.name == "SQL_COMMENT":
            for beginning_of_line_offset, end_of_line_offset, _ in lines:
                if beginning_of_line_offset <= token.start < end_of_line_offset:
                    break

            print(statement[token.start:(token.end + 1)])

        if token.name == "SQL_COMMENT":

            for beginning_of_line_offset, end_of_line_offset, _ in lines:
                if beginning_of_line_offset <= token.start < end_of_line_offset:
                    break

            comment = statement[token.start : (token.end + 1)]
            # print(comment)
            # Normal comment lines can also have noqa e.g.
            # --new table -- noqa: UNS05
            # Therefore extract last possible inline ignore.
            comment = [c.strip() for c in comment.split("--")][-1]
            if comment.startswith("noqa"):
                # This is an ignore identifier
                comment_remainder = comment[4:]
                if comment_remainder:
                    # if not comment_remainder.startswith(":"):
                    #     msg = f"Malformed 'noqa' section in line {token.start}. Expected 'noqa: <rule>[,...]"
                    #     raise errors.SQLParseError(
                    #         msg,
                    #     )
                    comment_remainder = comment_remainder[1:].strip()
                    # print(comment_remainder)
                    # print(beginning_of_line_offset)

            # if comment.startswith("")
            comments.append(
                Comment(statement_location=beginning_of_line_offset, text=comment),
            )

    # for c in comments:
    #     print(c.statement_location)
    return comments


class DropColumn(Visitor):  # type: ignore[misc]
    """Drop column."""

    name = "unsafe.drop_column"
    code = "US015"

    def visit_JoinExpr(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit JoinExpr."""
        print(node)
    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""


# sql = """ALTER TABLE transaction ADD COLUMN "transactionDate" timestamp without time zone GENERATED ALWAYS AS ("dateTime"::date) STORED;"""
sql = """
select * from tble join tble2 on tble.id = tble2.id;
select * from tble join tble2 on true;
select * from tble join tble2 on 1 = 1;
select * from tble join tble2 on tble.id > tble2.id;
select * from tble join tble2 on tble.id is not null;
select * from tble join tble2 on tble.id > 1;
delete from tble using tble2 where tble.id = tble2.id;
"""

sql = """delete from tble using tble2, tble3 where tble.id = tble2.id and tble.id = tble3.id;"""

# print(raw1)
# contype=<ConstrType.CONSTR_DEFAULT: 2> deferrable=False initdeferred=False is_no_inherit=False raw_expr=<ColumnRef fields=(<String sval='a'>,)>
sql_no_comment = re.sub(r"^\s*--.*\n|^\s*\/[*][\S\s]*?[*]\/", "", sql, flags=re.MULTILINE)
# print(sql_no_comment)
# print(_extract_comments(sql))
_extract_comments(sql)
raw = parse_sql_json(sql_no_comment)
print(raw)
# raw = parse_sql(sql_no_comment)
raw2 = scan(sql)
# print(raw2)

#         print(a)
DropColumn()(raw)

sql = 'update translations set italian=$2 where word=$1'
print(prettify(sql))
from pglast.printers import node_printer

@node_printer(ast.ParamRef, override=True)
def replace_param_ref(node, output):
    output.write(repr(args[node.number - 1]))

args = ["Hello", "Ciao"]
print(prettify(sql, safety_belt=False))

clone = ast.SelectStmt(stmt())
clone is stmt
