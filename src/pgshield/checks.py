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

    print(statement)

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

            comment = statement[token.start : (token.end + 1)]
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
                    print(comment_remainder)
                    print(beginning_of_line_offset)

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

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        print(node)
        print(node.typeName.names)
        for option in node.typeName.names:
            print(stream.RawStream()(option))
        # if node.subtype == enums.AlterTableType.AT_AddColumn:
        if "bigserial" in node.def_.typeName.names:
            print("okay")
            # print(node.def_.typeName.names)
            raise ValueError("nay")


# sql = """ALTER TABLE transaction ADD COLUMN "transactionDate" timestamp without time zone GENERATED ALWAYS AS ("dateTime"::date) STORED;"""
sql = """
DROP database tbl;
ALTER TABLE public.ecdict ADD COLUMN id serial --noqa: UNS01 /* hello */
; /* hello */
/* hello */ ALTER TABLE /*one*/ public.ecdict ADD COLUMN id serial --noqa: UNS02
;
-- ALTER TABLE public.ecdict ADD COLUMN id serial;
"""

# sql = "alter index tble set tablespace col"
# sql = "alter table tble add column b text default 'a'"
# sql = "create table tble (a text default a)"
# raw1 = parse_sql("""create table foo (
#                 a integer null,
#                 b integer not null
#             )""")
# print(raw1)
# contype=<ConstrType.CONSTR_DEFAULT: 2> deferrable=False initdeferred=False is_no_inherit=False raw_expr=<ColumnRef fields=(<String sval='a'>,)>
sql_no_comment = re.sub(r"^\s*--.*\n|^\s*\/[*][\S\s]*?[*]\/", "", sql, flags=re.MULTILINE)
# print(sql_no_comment)
print(_extract_comments(sql))
raw = parse_sql(sql_no_comment)

print(raw)
print(raw[2].stmt_location)
# raw2 = scan(sql)
# print(raw)
# print(raw2)
print(_extract_comments(sql))
# for a in raw2:
#     if a.name == "SQL_COMMENT":
#         print(a)
# DropColumn()(raw)
print(stream.RawStream()(raw))
# print(raw)
# print(raw)
# EnsureNoNotNullOnExistingColumn()(raw)
# EnsureNoNotNullOnExistingColumn()(raw)
# EnsureConstantDefaultForExistingColumn()(raw)
# EnsureConstantDefaultForNewColumn()(raw)
# EnsureNoNotNullNonConstantDefaultOnNewColumn()(raw)

# removing a column
# changing the type of a column
# renaming a column
# renaming a table
# adding an auto-incrementing column
# adding a stored generated column
# adding a check constraint
