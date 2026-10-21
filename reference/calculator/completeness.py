"""Check of the full form: the cards required for a module that is about to
be frozen (appendix A §2.8).

Only the required card parts are checked. The content of the sentences, for
instance whether the includes are taken from two domains (CONCEPT-2), is
checked by reading.

To run:

    python -m calculator.completeness ../content/calc.md
"""

from __future__ import annotations

import sys
from pathlib import Path

from .reader import Rule, ChoiceList, ContentItem, Concept, Module, Property, read

# The required card parts, by kind of content, and their rule.
_REQUIRED: dict[str, tuple[tuple[str, ...], str]] = {
    "concept": (("label", "definition", "includes", "excludes"), "CONCEPT-1"),
    "property": (("label", "definition", "personal"), "CONCEPT-3"),
    "computed": (("label", "definition", "personal"), "CALC-4"),
    "constraint": (("label", "definition", "message"), "CALC-37"),
    "choice_list": (("label", "definition"), "VALUE-19"),
}


def _kind_of(entry: ContentItem) -> str | None:
    if isinstance(entry, Concept):
        return "concept"
    if isinstance(entry, Property):
        return "property"
    if isinstance(entry, ChoiceList):
        return "choice_list"
    if isinstance(entry, Rule) and entry.kind in ("computed", "constraint"):
        return entry.kind
    return None


def check(module: Module) -> list[str]:
    """What a module lacks of the full form; empty if it is complete."""
    missing = []
    for entry in module.content.values():
        if isinstance(entry, Rule) and entry.short_form:
            missing.append(f"{entry.address}: written in short form (NOTATION-17)")
            continue
        kind = _kind_of(entry)
        if kind is None:
            continue
        present = {keyword.partition(".")[0] for keyword, _ in entry.card}
        required, rule_id = _REQUIRED[kind]
        for keyword in required:
            if keyword not in present:
                missing.append(f"{entry.address}: {kind} without {keyword} ({rule_id})")
    return missing


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    incomplete = 0
    for path in argv:
        for module in read(Path(path).read_text(encoding="utf-8"), markdown=True):
            missing = check(module)
            print(f"{'complete' if not missing else 'incomplete':<14} {module.full_name}")
            for k in missing:
                print(f"  {k}")
            incomplete += bool(missing)
    return 1 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
