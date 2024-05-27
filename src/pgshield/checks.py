"""Linter."""
from pglast import ast, enums, prettify, stream, printers  # type: ignore
from pglast.stream import RawStream, IndentedStream
from pglast.visitors import Delete, Visitor, Ancestor
from pglast.parser import parse_sql_json, parse_sql, scan
from typing import NamedTuple
from collections import namedtuple


Comment = namedtuple('Comment', ('location', 'text', 'at_start_of_line', 'continue_previous'))
"A structure to carry information about a single SQL comment."

def _extract_comments(statement):
    lines = []
    lofs = 0
    print(statement.splitlines(True))
    for line in statement.splitlines(True):
        print(len(line))
        llen = len(line)
        lines.append((lofs, lofs+llen, line))
        lofs += llen
    comments = []
    continue_previous = False
    for token in scan(statement):
        if token.name in ('C_COMMENT', 'SQL_COMMENT'):
            for bol_ofs, eol_ofs, line in lines:
                if bol_ofs <= token.start < eol_ofs:
                    break
            else:  # pragma: no cover
                raise RuntimeError('Uhm, logic error!')

            print(bol_ofs)
            print(line[:token.start - bol_ofs].strip())
            at_start_of_line = not line[:token.start - bol_ofs].strip()
            text = statement[token.start:token.end+1]
            comments.append(Comment(token.start, text, at_start_of_line, continue_previous))
            continue_previous = True
        else:
            continue_previous = False
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
            print( stream.RawStream()(option))
        # if node.subtype == enums.AlterTableType.AT_AddColumn:
        if "bigserial" in node.def_.typeName.names:
            print("okay")
            # print(node.def_.typeName.names)
            raise ValueError("nay")

# sql = """ALTER TABLE transaction ADD COLUMN "transactionDate" timestamp without time zone GENERATED ALWAYS AS ("dateTime"::date) STORED;"""
sql = """ALTER TABLE public.ecdict
ADD COLUMN id serial --noqa: UNS01
;
ALTER TABLE public.ecdict ADD COLUMN id serial;"""

# sql = "alter index tble set tablespace col"
# sql = "alter table tble add column b text default 'a'"
# sql = "create table tble (a text default a)"
# raw1 = parse_sql("""create table foo (
#                 a integer null,
#                 b integer not null
#             )""")
# print(raw1)
# contype=<ConstrType.CONSTR_DEFAULT: 2> deferrable=False initdeferred=False is_no_inherit=False raw_expr=<ColumnRef fields=(<String sval='a'>,)>
raw = parse_sql(sql)
print(raw[0].stmt_location)
raw2 = scan(sql)
# print(raw)
print(raw2)
print(_extract_comments(sql))
for a in raw2:
    if a.name == "SQL_COMMENT":
        print(a)
DropColumn()(raw)
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