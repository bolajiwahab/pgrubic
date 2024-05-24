"""Entry point."""
import sys
from collections import abc

from pgshield import rules
from pgshield import linter as lint


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths = argv[1:]

    linter = lint.Linter()
    linter.checkers.add(rules.EnsureConcurrentIndex(issue_code="W001"))
    linter.checkers.add(rules.EnsureForeignKeyConstraintNotValidatingExistingRows(issue_code="W002"))

    for source_path in source_paths:
        linter.run(source_path)

if __name__ == "__main__":
    cli()
