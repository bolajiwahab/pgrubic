"""Linter."""
from pglast import ast, enums, prettify, split  # type: ignore
from pglast.stream import RawStream, IndentedStream
from pglast.visitors import Delete, Visitor, Ancestor
from pglast.parser import parse_sql_json, parse_sql

class DropNullConstraint(Visitor):
    def visit_Constraint(self, ancestors, node):
        if node.contype == enums.ConstrType.CONSTR_NULL:
            return Delete

raw = parse_sql("""create table foo (
                a integer null,
                b integer not null
            )""")

DropNullConstraint()(raw)

# print(RawStream()(raw))
# print(prettify('delete from sometable where value is null'))

class EnsureConcurrentIndex(Visitor):
    def visit_IndexStmt(self, ancestors, node):
        if not node.concurrent:
            raise ValueError('concurrent is not set')

sql = "alter table tble add column a text default a, add column b text default 'a'"
raw = parse_sql(sql)
EnsureConcurrentIndex()(raw)

class EnsureNoNotNullOnExistingColumn(Visitor):  # type: ignore[misc]
    """Not Null constraint should not be set directly on an existing column."""

    def visit_AlterTableCmd(
        self, ancestors, node: ast.Node,  # noqa: ARG002, ANN401
    ) -> None:
        """Visit Alter Table Command."""
        print(node)
        if ast.AlterTableStmt in ancestors and node.subtype == enums.AlterTableType.AT_SetNotNull:
            raise ValueError("Hello1")


class EnsureConstantDefaultForExistingColumn(Visitor): # type: ignore[misc]
    """Constants are safe for default for existing columns."""

    def visit_AlterTableCmd(self, ancestors, node: ast.Node) -> None:  # noqa: ARG002, ANN401
        """Visit Constraint Definition."""
        # print(node)
        # print("hello")
        if node.subtype == enums.AlterTableType.AT_ColumnDefault and not isinstance(node.def_, ast.A_Const):
            raise ValueError('Not allowed --222- ')

class EnsureNoNotNullNonConstantDefaultOnNewColumn(Visitor): # type: ignore[misc]
    """Constants are safe for default for new columns."""

    def visit_ColumnDef(self, ancestors, node: ast.Node) -> None:  # noqa: ARG002, ANN401
        """Visit AlterTableCmd and Constraint Definition."""
        if ast.AlterTableStmt in ancestors:
            is_not_null = False
            has_default = False

            for constraint in (node.constraints):
                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True
                if constraint.contype == enums.ConstrType.CONSTR_DEFAULT and isinstance(constraint.raw_expr, ast.A_Const):
                    has_default = True

            if is_not_null and not has_default:
                raise ValueError('Not allowed --232- ')


class EnsureConstantDefaultForNewColumn(Visitor): # type: ignore[misc]
    """Constants are safe for default for new columns."""

    def visit_Constraint(self, ancestors, node: ast.Node) -> None:  # noqa: ARG002, ANN401
        """Visit AlterTableCmd and Constraint Definition."""
        print(node)
        print("happy")
        if ast.AlterTableStmt in ancestors and node.contype == enums.ConstrType.CONSTR_DEFAULT and not isinstance(node.raw_expr, ast.A_Const):
            raise ValueError('Not allowed --242- ')


#         if not isinstance(node.raw_expr, ast.A_Const):
#             print("hello")

sql = "alter table tble alter column a set default null, alter column b set not null, add column b text default 'a' not null, add column b text not null;"
# sql = "alter table tble add column b text default 'a'"
# sql = "create table tble (a text default a)"
# raw1 = parse_sql("""create table foo (
#                 a integer null,
#                 b integer not null
#             )""")
# print(raw1)
# contype=<ConstrType.CONSTR_DEFAULT: 2> deferrable=False initdeferred=False is_no_inherit=False raw_expr=<ColumnRef fields=(<String sval='a'>,)>
raw = parse_sql(sql)
# print(raw)
# print(raw)
# EnsureNoNotNullOnExistingColumn()(raw)
EnsureNoNotNullOnExistingColumn()(raw)
EnsureConstantDefaultForExistingColumn()(raw)
EnsureConstantDefaultForNewColumn()(raw)
EnsureNoNotNullNonConstantDefaultOnNewColumn()(raw)

# AlterTableMoveAllStmt
# ClusterStmt
# vacuum full
# RefreshMatViewStmt
# ReindexStmt

# ColumnDef