from pglast import stream, parse_sql, enums, visitors, ast

from pglast.visitors import Delete, Visitor

import itertools

class DropColumn(visitors.Visitor):
    def visit_AlterTableCmd(
            self,
            ancestors: ast.Node,
            node: ast.Node,
    ) -> None:
        # print(len(ancestors))
        # print(ancestors)
        # cnt = 0
        mem: list[str] = []
        mem = list(itertools.takewhile(lambda n: n is not None, ancestors))
        for n in ancestors:
            print(n)
            if n is None:
                break
            mem.append(n)
        print(len(mem))
        print(ancestors[len(mem) - 1])
            # if isinstance(n, ast.RawStmt):
            #     print("we are here.")
        #     print(n)
        # if node.subtype == enums.AlterTableType.AT_DropColumn:
        #     # pass
        #     # print(node)
        #     print(stream.RawStream()(ancestors[3]))


# class DropNullConstraint(Visitor):
#     def visit_Constraint(self, ancestors, node):
#         if node.contype == enums.ConstrType.CONSTR_NULL:
#             return Delete

# raw = parse_sql("""create table foo (
#                 a integer null,
#                 b integer not null
#             )""")

sql = "alter table tbl drop column a;"
raw = parse_sql(sql)
# (parse_sql('SELECT foo FROM bar'))
# stream.RawStream()(raw)

raw2 = DropColumn()(raw)

# print(stream.RawStream()(raw2))
