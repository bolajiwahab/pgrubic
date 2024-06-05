"""Convention around naming."""

from typing import ClassVar

from pglast import ast, enums, stream, keywords  # type: ignore[import-untyped]

from pgshield import utils, linter
from pgshield.rules.convention import test_

class NoUpperCaseNameForIdentifiers(linter.Checker):  # type: ignore[misc]
    """No upper case name for identifiers."""

    name = "convention.no_upper_case_name_for_identifiers"
    code = "CVN011"

    # identifiers: ClassVar[list[tuple[int, str]]] = []

    attributes = test_.Identifiers()

    # print(attributes.identifiers)

    # def visit_CreateStmt(
    #     self,
    #     ancestors: ast.Node,
    #     node: ast.Node,
    # ) -> None:
    #     """Visit CreateStmt."""
    #     print("okay")
    #     statement_index: int = utils.get_statement_index(ancestors)

    #     self.identifiers.append((statement_index, node.relation.relname))
    #     print(self.identifiers)

    # print(identifiers)

    # if (
    #     any(ele.isupper() for _, ele in identifiers)
    #     # and (ancestors[statement_index].stmt_location, self.code)
    #     # not in self.ignore_rules
    # ):
        
    #     raise ValueError("hmmm")

        # self.violations.append(
        #     linter.Violation(
        #         location=ancestors[statement_index].stmt_location,
        #         statement=ancestors[statement_index],
        #         description="Upper case name for table",
        #     ),
        # )


# class NoUpperCaseNameForTable(linter.Checker):  # type: ignore[misc]
#     """No upper case name for table."""

#     name = "convention.no_upper_case_name_for_table"
#     code = "CVN001"

#     def visit_CreateStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.CreateStmt,
#     ) -> None:
#         """Visit CreateStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             any(ele.isupper() for ele in node.relation.relname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for table",
#                 ),
#             )


    # def visit_RawStmt(
    #     self,
    #     ancestors: ast.Node,
    #     node: ast.CreateStmt,
    # ) -> None:
    #     """Visit CreateStmt."""
    #     print("RawStmt")
    #     # print(node)

# class NoUpperCaseNameForColumn(linter.Checker):  # type: ignore[misc]
#     """No upper case name for column."""

#     name = "convention.no_upper_case_name_for_column"
#     code = "CVN002"

#     def visit_ColumnDef(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit ColumnDef."""
#         if ast.CreateStmt in ancestors:

#             statement_index: int = utils.get_statement_index(ancestors)

#             if (
#                 any(ele.isupper() for ele in node.colname)
#                 and (ancestors[statement_index].stmt_location, self.code)
#                 not in self.ignore_rules
#             ):

#                 self.violations.append(
#                     linter.Violation(
#                         location=ancestors[statement_index].stmt_location,
#                         statement=ancestors[statement_index],
#                         description="Upper case name for column",
#                     ),
#                 )


# class NoUpperCaseNameForView(linter.Checker):
#     """No upper case name for view."""

#     name = "convention.no_upper_case_name_for_view"
#     code = "CVN003"

#     def visit_ViewStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit ViewStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             any(ele.isupper() for ele in node.view.relname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for view",
#                 ),
#             )


# class NoUpperCaseNameForMaterializedView(linter.Checker):
#     """No upper case name for materialized view."""

#     name = "convention.no_upper_case_name_for_materialized_view"
#     code = "CVN004"

#     def visit_CreateTableAsStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit CreateTableAsStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             node.objtype == enums.ObjectType.OBJECT_MATVIEW
#             and any(ele.isupper() for ele in node.into.rel.relname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for materialized view",
#                 ),
#             )


# class NoUpperCaseNameForCTAS(linter.Checker):
#     """No upper case name for CTAS table."""

#     name = "convention.no_upper_case_name_for_ctas_table"
#     code = "CVN005"

#     def visit_CreateTableAsStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit CreateTableAsStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             node.objtype == enums.ObjectType.OBJECT_TABLE
#             and any(ele.isupper() for ele in node.into.rel.relname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for CTAS table",
#                 ),
#             )


# class NoUpperCaseNameForIndex(linter.Checker):  # type: ignore[misc]
#     """No upper case name for index."""

#     name = "convention.no_upper_case_name_for_index"
#     code = "CVN006"

#     def visit_IndexStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit IndexStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             any(ele.isupper() for ele in node.idxname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for index",
#                 ),
#             )


# class NoUpperCaseNameForSequence(linter.Checker):  # type: ignore[misc]
#     """No upper case name for sequence."""

#     name = "convention.no_upper_case_name_for_sequence"
#     code = "CVN007"

#     def visit_CreateSeqStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit CreateSeqStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             any(ele.isupper() for ele in node.sequence.relname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for sequence",
#                 ),
#             )


# class NoUpperCaseNameForSchema(linter.Checker):  # type: ignore[misc]
#     """No upper case name for schema."""

#     name = "convention.no_upper_case_name_for_schema"
#     code = "CVN008"

#     def visit_CreateSchemaStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit CreateSchemaStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if (
#             any(ele.isupper() for ele in node.schemaname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for schema",
#                 ),
#             )


# class NoUpperCaseNameForFunction(linter.Checker):  # type: ignore[misc]
#     """No upper case name for function."""

#     name = "convention.no_upper_case_name_for_function"
#     code = "CVN009"

#     def visit_CreateFunctionStmt(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit CreateFunctionStmt."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         func_name = [
#             stream.RawStream()(data_type).strip("'") for data_type in node.funcname
#         ]

#         if (
#             any(ele.isupper() for ele in func_name[-1])
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for function",
#                 ),
#             )


# class NoUpperCaseNameForConstraint(linter.Checker):  # type: ignore[misc]
#     """No upper case name for function."""

#     name = "convention.no_upper_case_name_for_constraint"
#     code = "CVN010"

#     def visit_Constraint(
#         self,
#         ancestors: ast.Node,
#         node: ast.Node,
#     ) -> None:
#         """Visit Constraint."""
#         statement_index: int = utils.get_statement_index(ancestors)

#         if node.conname is not None and (
#             any(ele.isupper() for ele in node.conname)
#             and (ancestors[statement_index].stmt_location, self.code)
#             not in self.ignore_rules
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     location=ancestors[statement_index].stmt_location,
#                     statement=ancestors[statement_index],
#                     description="Upper case name for constraint",
#                 ),
#             )

# # trigger
# # rule
# # type
# # database
# # tablespace

