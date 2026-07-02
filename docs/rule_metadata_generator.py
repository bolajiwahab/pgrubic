"""Generate documentation for rules metadata."""

import pathlib
from collections import defaultdict

from caseconverter import kebabcase

from pgrubic import core

rules = core.load_rules(
    config=core.parse_config(),
    include_deprecated=True,
)

rule_metadata_file = pathlib.Path.cwd() / "docs/docs/rules.md"

# remove existing documentation
rule_metadata_file.unlink(missing_ok=True)

categories: dict[str, str] = {
    "constraint": "Rules for constraints",
    "general": "Rules for best practices",
    "query": "Rules for queries",
    "naming": "Rules for naming",
    "schema": "Rules for schema",
    "security": "Rules for security",
    "typing": "Rules for typing",
    "unsafe": "Rules for unsafe schema migrations",
}

grouped_rules: dict[str, list[type[core.BaseChecker]]] = defaultdict(list)

for rule in sorted(rules, key=lambda rule: rule.code):
    grouped_rules[rule.category].append(rule)

with pathlib.Path.open(
    rule_metadata_file,
    "a",
) as file:
    file.write("# Rules\n\n")
    file.write(
        f"""There are **{len(rules)}** rules, all enabled by default except deprecated
ones, which are not part of the active rule set.
\nRules are divided into {len(categories)} categories:\n\n""",
    )

for index, (category, description) in enumerate(categories.items(), start=1):
    with pathlib.Path.open(
        rule_metadata_file,
        "a",
    ) as file:
        file.write(f"{index}. **{category}**: {description}\n")

for category in categories:
    with pathlib.Path.open(
        rule_metadata_file,
        "a",
    ) as file:
        file.write(f"\n## {category} ({grouped_rules[category][0].code[:2]})\n\n")
        file.write("| Code | Name | Status | Auto-fixable |\n")
        file.write("| ---- | ---- | ------ | ------------ |\n")

    for rule in grouped_rules[category]:
        name = kebabcase(rule.__name__)

        status = (
            ":warning: Deprecated" if rule.deprecation else ":white_check_mark: Stable"
        )

        autofix = ":white_check_mark:" if rule.is_auto_fixable else ":x:"

        with pathlib.Path.open(
            rule_metadata_file,
            "a",
        ) as file:
            file.write(
                f"| {rule.code} "
                f"| [{name}](rules/{category}/{name}.md) "
                f"| {status} "
                f"| {autofix} |\n",
            )
