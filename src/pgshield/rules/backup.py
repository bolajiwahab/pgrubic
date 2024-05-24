class EnsureConstantDefaultForExistingColumn(visitors.Visitor): # type: ignore[misc]
    """Constants are safe for default for existing columns."""

    def visit_AlterTableCmd(self, ancestors: typing.Any, node: ast.Node) -> None:  # noqa: ARG002, ANN401
        """Visit AlterTableCmd and Constraint Definition."""
        if node.subtype == enums.AlterTableType.AT_ColumnDefault and not isinstance(node.def_, ast.A_Const):
            raise errors.UniqueConstraintShouldNotCreateUniqueIndexError
