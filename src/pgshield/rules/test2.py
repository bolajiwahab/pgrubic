from pglast import parse_sql, SqlNode

class ConstraintVisitor:
    def __init__(self, rules_to_skip=None):
        self.rules_to_skip = rules_to_skip or []

    def visit_Constraint(self, node):
        if 'L001' not in self.rules_to_skip:
            # Example linting rule for Constraint
            print(f"Avoid using constraints on line {node.location.line}")

class SelectVisitor:
    def __init__(self, rules_to_skip=None):
        self.rules_to_skip = rules_to_skip or []

    def visit_Select(self, node):
        if 'L002' not in self.rules_to_skip:
            # Example linting rule for Select
            print(f"Avoid using SELECT * on line {node.location.line}")

def extract_skip_rules_per_line(sql):
    parsed = parse_sql(sql)
    skip_rules_per_line = {}

    for node in parsed:
        if isinstance(node, SqlNode) and node.tag == 'T_Comment':
            comment_text = node.str.upper().strip()
            if comment_text.startswith('-- NOQA:'):
                rules = comment_text[len('-- NOQA:'):].strip().split(',')
                lineno = node.location.line
                skip_rules_per_line[lineno] = [rule.strip() for rule in rules]

    return skip_rules_per_line

def lint_sql(sql):
    skip_rules_per_line = extract_skip_rules_per_line(sql)
    parsed = parse_sql(sql)

    for node in parsed:
        lineno = node.location.line
        rules_to_skip = skip_rules_per_line.get(lineno, [])
        
        constraint_visitor = ConstraintVisitor(rules_to_skip)
        select_visitor = SelectVisitor(rules_to_skip)

        if isinstance(node, SqlNode) and node.tag == 'T_Constraint':
            constraint_visitor.visit_Constraint(node)
        elif isinstance(node, SqlNode) and node.tag == 'T_SelectStmt':
            select_visitor.visit_Select(node)

# Example usage
sql_example = """
-- NoQA: L001
CREATE TABLE example_table (
    id SERIAL PRIMARY KEY
);

SELECT * FROM table1;

SELECT column1, column2 FROM table2; -- NoQA: L002
"""

lint_sql(sql_example)
