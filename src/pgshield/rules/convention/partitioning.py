"""Convention for partitioning."""

import typing
from datetime import datetime

from pglast import ast, enums
from dateutil import relativedelta

from pgshield.core import linter


# class GapInRangePartitionBound(linter.Checker):
#     """Gap in range partition bound."""

#     name: str = "convention.gap_in_range_partition_bound"
#     code: str = "CVP001"

#     is_auto_fixable: bool = False

#     def visit_PartitionBoundSpec(
#         self,
#         ancestors: ast.Node,
#         node: ast.PartitionBoundSpec,
#     ) -> None:
#         """Visit PartitionBoundSpec."""
#         partitioning_resolution: list[int] = []

#         if (
#             not node.is_default
#             and node.strategy == enums.PartitionStrategy.PARTITION_STRATEGY_RANGE
#         ):

#             # get the difference in hours, days, months, years
#             lower_bound = datetime.fromisoformat(node.lowerdatums[-1].val.sval)
#             upper_bound = datetime.fromisoformat(node.upperdatums[-1].val.sval)

#             # ensure we only have of days, months, years, hours, weeks in the difference
#             # e.g. (months=+1, days=+1)

#             difference_in_hours = relativedelta.relativedelta(
#                 upper_bound,
#                 lower_bound,
#             ).hours

#             difference_in_days = relativedelta.relativedelta(
#                 upper_bound,
#                 lower_bound,
#             ).days

#             difference_in_weeks = relativedelta.relativedelta(
#                 upper_bound,
#                 lower_bound,
#             ).weeks

#             difference_in_months = relativedelta.relativedelta(
#                 upper_bound,
#                 lower_bound,
#             ).months

#             difference_in_years = relativedelta.relativedelta(
#                 upper_bound,
#                 lower_bound,
#             ).years

#             partitioning_resolution.append(difference_in_hours)
#             partitioning_resolution.append(difference_in_days)
#             partitioning_resolution.append(difference_in_weeks)
#             partitioning_resolution.append(difference_in_months)
#             partitioning_resolution.append(difference_in_years)

#             # check if any resolution is not 1
#             if all(resolution != 1 for resolution in partitioning_resolution):
#                 self.violations.append(
#                     linter.Violation(
#                         statement_location=self.statement_location,
#                         statement_length=self.statement_length,
#                         node_location=self.node_location,
#                         description="Gap in range partition bound",
#                     ),
#                 )


class PartitionStrategiesWhitelisted(linter.Checker):
    """Only whitelisted partition strategies are allowed."""

    name: str = "convention.whitelisted_partition_strategies"
    code: str = "CVP002"

    is_auto_fixable: bool = False

    strategy: typing.ClassVar[dict[str, str]] = {
        enums.PartitionStrategy.PARTITION_STRATEGY_LIST: "list",
        enums.PartitionStrategy.PARTITION_STRATEGY_RANGE: "range",
        enums.PartitionStrategy.PARTITION_STRATEGY_HASH: "hash",
    }

    def visit_PartitionSpec(
        self,
        ancestors: ast.Node,
        node: ast.PartitionSpec,
    ) -> None:
        """Visit PartitionSpec."""
        if (
            self.config.partition_strategies
            and self.strategy[node.strategy]
            not in self.config.partition_strategies
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Partitioning strategy '{self.partition_strategies_mapping[node.strategy]}' is not whitelisted",  # noqa: E501
                ),
            )


class PreferPartitioningByOneKey(linter.Checker):
    """Prefer partitioning by one key."""

    name: str = "convention.prefer_partitioning_by_one_key"
    code: str = "CVP003"

    is_auto_fixable: bool = False

    def visit_PartitionSpec(
        self,
        ancestors: ast.Node,
        node: ast.PartitionSpec,
    ) -> None:
        """Visit PartitionSpec."""
        max_partition_elements = 1

        if len(node.partParams) > max_partition_elements:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer partitioning by one key",
                ),
            )
