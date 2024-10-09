"""Checker for multi-column partitioning."""

from pglast import ast, visitors

from pgrubic.core import linter


class MultiColumnPartitioning(linter.BaseChecker):
    """## **What it does**
    Checks for partitioning with more than one column.

    ## **Why not?**
    One of the main reasons to use partitioning is the improved performance achieved by
    partition pruning. Pruning in a multi-column partitioned table can easily be
    sub-optimal, leading to scanning of unnecessary partitions.

    ## **When should you?**
    If you know what you are doing and have a good reason to do so. Just don't
    use multi-column partitioning without deep consideration and knowledge of its
    intrinsics. An example of what could go wrong is
    [why-isnt-postgres-multicolumn-partition-pruning-smarter-than-this](https://stackoverflow.com/questions/69662835/why-isnt-postgres-multicolumn-partition-pruning-smarter-than-this){:target="_blank"}

    ## **Use instead:**
    Sub-partitioning.
    """

    def visit_PartitionSpec(
        self,
        ancestors: visitors.Ancestor,
        node: ast.PartitionSpec,
    ) -> None:
        """Visit PartitionSpec."""
        if len(node.partParams) > 1:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Prefer partitioning by one key",
                ),
            )
