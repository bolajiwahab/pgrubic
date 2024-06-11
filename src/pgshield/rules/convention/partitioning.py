"""Convention for partitioning."""

from datetime import datetime

from pglast import ast, enums  # type: ignore[import-untyped]
from dateutil import relativedelta  # type: ignore[import-untyped]

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
        partitioning_resolution: list[int] = []

        statement_index: int = linter.get_statement_index(ancestors)

        if (
            not node.is_default
            and node.strategy == enums.PartitionStrategy.PARTITION_STRATEGY_RANGE
        ):

            # get the difference in hours, days, months, years
            lower_bound = datetime.fromisoformat(node.lowerdatums[-1].val.sval)
            upper_bound = datetime.fromisoformat(node.upperdatums[-1].val.sval)

            difference_in_hours = relativedelta.relativedelta(
                upper_bound, lower_bound,
            ).hours
            difference_in_days = relativedelta.relativedelta(
                upper_bound, lower_bound,
            ).days
            difference_in_months = relativedelta.relativedelta(
                upper_bound, lower_bound,
            ).months
            difference_in_years = relativedelta.relativedelta(
                upper_bound, lower_bound,
            ).years

            partitioning_resolution.append(difference_in_hours)
            partitioning_resolution.append(difference_in_days)
            partitioning_resolution.append(difference_in_months)
            partitioning_resolution.append(difference_in_years)

            print(partitioning_resolution)

            # check if any resolution is not 1
            if all(resolution != 1 for resolution in partitioning_resolution):
                self.violations.append(
                    linter.Violation(
                        location=ancestors[statement_index].stmt_location,
                        statement=ancestors[statement_index],
                        description="Gap in range partition bound",
                    ),
                )
