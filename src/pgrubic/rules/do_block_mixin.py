"""Mixin to add DO block support to checkers."""

import logging
from typing import Optional

from pglast import ast, visitors

from pgrubic.core import linter
from pgrubic.core.do_block import lint_do_block

logger = logging.getLogger(__name__)


class DoBlockMixin:
    """Mixin that adds DO block support to checkers.
    
    Any checker that wants to lint SQL statements inside DO blocks should
    inherit from both BaseChecker and this mixin.
    """
    
    def visit_DoStmt(
        self: linter.BaseChecker,
        ancestors: visitors.Ancestor,
        node: ast.DoStmt,
    ) -> None:
        """Visit DO statement and lint SQL statements within it."""
        # Create a temporary linter instance with just this checker
        temp_linter = linter.Linter(
            config=self.config,
            formatters=lambda: set()  # No formatters needed for nested linting
        )
        temp_linter.checkers = {self.__class__()}
        
        # Lint the DO block and collect violations
        for violation in lint_do_block(
            linter=temp_linter,
            do_stmt=node,
            source=self.source_code,
            filename=self.source_file,
            base_line=self.line_number
        ):
            # Add the violation directly as it's already in the correct format
            self.violations.add(violation)