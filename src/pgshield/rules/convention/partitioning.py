"""Convention for partitioning."""

import re
from datetime import datetime
from pglast import ast, stream, enums  # type: ignore[import-untyped]

from pgshield.core import linter


class GapInRangePartitionBound(linter.Checker):  # type: ignore[misc]
    """Gap in range partition bound."""

    name = "convention.gap_in_range_partition_bound"
    code = "CVP001"

    def visit_PartitionBoundSpec(
        self,
        ancestors: ast.Node,
        node: ast.PartitionBoundSpec,
    ) -> None:
        """Visit PartitionBoundSpec."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            not node.is_default
            and node.strategy == enums.PartitionStrategy.PARTITION_STRATEGY_RANGE
        ):
            print(node)
            # print(datetime.fromisoformat(node.upperdatums[0].val.sval))
            print(datetime.fromisoformat(node.upperdatums[-1].val.sval) - datetime.fromisoformat(node.lowerdatums[-1].val.sval))
        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "json"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Gap in range partition bound",
                ),
            )
