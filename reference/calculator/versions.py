"""Compares two versions of a module (07 §2.2, 08 §2.7).

The kinds of change are computed by comparing the two versions address by
address (CHANGE-5): addition, modification, and a removed address (CHANGE-6).
Deprecation is not visible here, because the deprecation marker is a
statement by the owner outside the version (07 §2.4).

An example has an address, so the new version holds the examples of the old
version. An example that is active in the old version and marked replaced in
the new version is run again with the new version; if it fails, it is
reported as a behavior change (PROOF-22).

To run, from the reference folder:

    python -m calculator.versions ../content/calc.md ../conformance/15-change.md uniti/depreciation@v3 uniti/depreciation@v4
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field, fields, is_dataclass

from .reader import Rule, Example, ChoiceList, ContentItem, Concept, Module, Property
from .examples import read_files, run_example
from .values import NotationError
from .module_set import ModuleSet


@dataclass(frozen=True)
class BehaviorChange:
    example: str
    old: str
    new: str
    reason: str


@dataclass
class Comparison:
    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)        # violates CHANGE-6
    meaning_changed: list[str] = field(default_factory=list)  # violates CHANGE-7 (04 §2.9)
    became_required: list[str] = field(default_factory=list)    # reported separately (04 §2.9)
    uses: list[str] = field(default_factory=list)
    behavior_changes: list[BehaviorChange] = field(default_factory=list)


def _version_number(version: str) -> int:
    m = re.fullmatch(r"v(\d+)", version)
    if not m:
        raise NotationError(f"version {version!r} is not v‹number›")
    return int(m.group(1))


def _signature(x: object) -> object:
    """The content of the writing without line numbers, to see whether something changed."""
    if isinstance(x, Module):
        return x.full_name
    if is_dataclass(x) and not isinstance(x, type):
        return (type(x).__name__,) + tuple(
            (f.name, _signature(getattr(x, f.name))) for f in fields(x)
            if f.name not in ("lineno", "module"))
    if isinstance(x, (list, tuple)):
        return tuple(_signature(y) for y in x)
    if isinstance(x, dict):
        return tuple(sorted((k, _signature(v)) for k, v in x.items()))
    return x


def _applies_to_by_property(m: Module) -> dict[str, dict[str, bool]]:
    """`applies to` by property, because that relation belongs to the property
    (05 §2.2): property → {concept: required}."""
    result: dict[str, dict[str, bool]] = {}
    for b in m.applies_to:
        for prop, required in b.properties:
            result.setdefault(prop, {})[b.concept] = required
    return result


def _meaning_changed(old: ContentItem, new: ContentItem) -> bool:
    """A change that MUST use a new address (04 §2.9)."""
    if type(old) is not type(new):
        return True
    if isinstance(old, Property):
        a, b = old.value_type, new.value_type
        return ((a.type_name, a.to, a.quantity, a.direction, a.many)
                != (b.type_name, b.to, b.quantity, b.direction, b.many)
                or (old.personal is True and new.personal is False))
    if isinstance(old, Concept):
        return old.parent != new.parent
    if isinstance(old, ChoiceList):
        return old.is_open and not new.is_open
    if isinstance(old, Rule) and old.kind == "computed":
        return ((old.is_open and not new.is_open) or _signature(old.result) != _signature(new.result)
                or old.parameters != new.parameters)
    return False


def _example_status(c: Example) -> str:
    return next((b.text() for b in c.parts if b.keyword == "status"), "active")


def compare_versions(module_set: ModuleSet, old: Module, new: Module) -> Comparison:
    if old.address != new.address:
        raise NotationError(f"{old.full_name} and {new.full_name} are not the same module")
    if _version_number(new.version) != _version_number(old.version) + 1:  # CHANGE-2
        raise NotationError(f"{new.full_name} is not the version after {old.full_name} (CHANGE-2)")
    h = Comparison()
    a = f"{old.address}/"

    for name, entry in old.content.items():
        if name not in new.content:
            h.removed.append(a + name)
        elif _meaning_changed(entry, new.content[name]):
            h.meaning_changed.append(a + name)
        elif _signature(entry) != _signature(new.content[name]):
            h.modified.append(a + name)
    h.added += [a + name for name in new.content if name not in old.content]

    bl, bb = _applies_to_by_property(old), _applies_to_by_property(new)
    for prop in dict.fromkeys(list(bl) + list(bb)):
        x, y = bl.get(prop, {}), bb.get(prop, {})
        for concept in dict.fromkeys(list(x) + list(y)):
            if x.get(concept) == y.get(concept):
                continue
            # A property or concept that is required for later actions (04 §2.9).
            if y.get(concept) and not x.get(concept):
                h.became_required.append(f"{prop} for {concept}")
            # A new property together with its `applies to` already counts as an addition.
            if not (concept not in x and prop in new.content and prop not in old.content):
                h.modified.append(f"{a}applies to {concept}: {prop}")

    pl, pb = dict(old.uses), dict(new.uses)
    for address in dict.fromkeys(list(pl) + list(pb)):
        if pl.get(address) != pb.get(address):
            h.uses.append(f"{address}: {pl.get(address, '—')} → {pb.get(address, '—')}")

    for name, entry in old.content.items():
        current = new.content.get(name)
        if not (isinstance(entry, Example) and isinstance(current, Example)):
            continue
        if _example_status(entry) != "active" or _example_status(current) != "replaced":
            continue
        # The old example, with the rules of the new version.
        report = run_example(module_set, Example(entry.name, new, entry.lineno, parts=entry.parts))
        if report.status == "failed":
            reason = next(b.text() for b in current.parts if b.keyword == "reason")
            h.behavior_changes.append(BehaviorChange(entry.address, report.expected, report.result, reason))
    return h


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 3:
        print("usage: python -m calculator.versions file.md … address@vA address@vB")
        return 2
    *file, x, y = args
    module_set = read_files(*file)
    module = {m.full_name: m for m in module_set.all_modules()}
    h = compare_versions(module_set, module[x], module[y])
    for heading, entries in (("addition", h.added), ("modification", h.modified), ("removed (CHANGE-6)", h.removed),
                             ("meaning changed (CHANGE-7)", h.meaning_changed),
                             ("became required", h.became_required), ("used modules", h.uses)):
        for d in entries:
            print(f"{heading:<22} {d}")
    for p in h.behavior_changes:
        print(f"{'behavior change':<22} {p.example}: {p.old} → {p.new}. Reason: {p.reason}")
    return 1 if h.removed or h.meaning_changed else 0


if __name__ == "__main__":
    sys.exit(main())
