"""Linter."""
from pglast import ast, enums, prettify, stream, printers  # type: ignore
from pglast.stream import RawStream, IndentedStream
from pglast.visitors import Delete, Visitor, Ancestor
from pglast.parser import parse_sql_json, parse_sql

class DropColumn(Visitor):  # type: ignore[misc]
    """Drop column."""

    name = "unsafe.drop_column"
    code = "US015"

    def visit_ColumnDef(
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

sql = """ALTER TABLE transaction ADD COLUMN "transactionDate" timestamp without time zone GENERATED ALWAYS AS ("dateTime"::date) STORED;"""
# sql = "alter table tble add column b text default 'a'"
# sql = "create table tble (a text default a)"
# raw1 = parse_sql("""create table foo (
#                 a integer null,
#                 b integer not null
#             )""")
# print(raw1)
# contype=<ConstrType.CONSTR_DEFAULT: 2> deferrable=False initdeferred=False is_no_inherit=False raw_expr=<ColumnRef fields=(<String sval='a'>,)>
raw = parse_sql(sql)
DropColumn()(raw)
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