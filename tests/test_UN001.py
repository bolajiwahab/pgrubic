"""Test UN001."""
from pgshield import core
from pgshield.rules.unsafe import UN001


def test_UN001() -> None:
    """Test UN001."""
    sql = """
    ALTER TABLE public.ecdict DROP COLUMN id;
    """
    linter: core.Linter = core.Linter()
    linter.checkers.add(UN001())
    linter.run(sql)
