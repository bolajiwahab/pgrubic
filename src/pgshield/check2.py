from pglast import parse_sql, enums
from pglast.visitors import Visitor

class ColumnDefVisitor(Visitor):
    def visit_ColumnDef(self, ancestors, node):
        column_name = node.colname
        is_not_null = False
        has_default = False
        # is_not_null = node.is_not_null
        print(node)
        for constraint in (node.constraints or []):
            if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                is_not_null = True
            if constraint.contype == enums.ConstrType.CONSTR_DEFAULT:
                has_default = True

        print(has_default)

        # Check if the column has a DEFAULT value
        # has_default = node.raw_default is not None
        # print(node.raw_default)

        if node.constraints:
            # print(1)
            # if enums.ConstrType.CONSTR_NOTNULL in node.constraints.contype and enums.ConstrType.CONSTR_DEFAULT not in node.constraints.contype:
            #     raise ValueError("Not today")
            for constraint in node.constraints:
                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True
                    break
        print(f"Column: {column_name}, is_not_null: {is_not_null}")

# Define a function to create the visitor and parse the SQL query
# def check_column_constraints(sql_query):
#     parsed_query = parse_sql(sql_query)
#     visitor = ColumnDefVisitor()
#     visit(parsed_query, visitor)

# Example usage
sql_query = """
CREATE TABLE my_table (
    id text PRIMARY KEY not null default 'a',
    name VARCHAR(255) default 'a' NOT NULL,
    age INTEGER
);
"""
raw = parse_sql(sql_query)
# print(raw)
ColumnDefVisitor()(raw)
# check_column_constraints(sql_query)
