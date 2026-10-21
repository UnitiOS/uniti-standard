"""Runs examples and compares their results exactly (08 §2.4).

Examples are read according to appendix/A-notation.md §2.9. Each example is
run in a fact store of its own (PROOF-8), with its own module set (PROOF-6).
A local id becomes the identifier of the entity inside that example, so the
tie-breaker orders entities by local id (PROOF-31).

To run, from the reference folder:

    python -m calculator.examples ../conformance/00-form-examples.md
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from . import operations as op
from .reader import Rule, Line, Part, Example, ChoiceList, Concept, Name, ChoiceItem, Property, Dot, read, parse_text
from .compute import VALUE_KINDS, TYPE_PROPERTY, Action, Fact, FactStore, Env, Evaluator
from .values import (
    EMPTY, REASON_KINDS, UTC, Number, NotDefined, Entity, NotationError,
    Collection, Choice, Record, Text, NotComputable, parse_number, to_instant, parse_time, parse_zone,
    parse_unit,
)
from .module_set import ModuleSet
from .constraints import Rejection, check

# 08 §2.3: an action part that is not written is filled by the default example action.
EXAMPLE_ACTOR = Entity("‹example actor›", "example actor")

KIND_WORDS = {"replaces": "replacement", "ends": "ending", "corrects": "correction",
              "retracts": "retraction", "redacts": "redaction"}

_LOCAL_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_FACT_LINE = re.compile(r"^(?:([a-z][a-z0-9_]*):\s+)?([a-z][a-z0-9_]*)\s+(\S+)\s*(.*)$")
_FACT_TAIL = re.compile(
    r"^(.*?)(?:\s+recorded\s+(.*?))?(?:\s+(" + "|".join(KIND_WORDS) + r")\s+([a-z][a-z0-9_]*))?\s*$")
_ASK_RE = re.compile(r"^(.*?)\s+T:\s+(.*?)\s+R:\s+(.*)$")
_SINGLE_PARTS = ("kind", "title", "explanation", "domain", "zone", "status", "reason",
                 "replaced_by", "facts")


@dataclass(frozen=True)
class Report:
    example: str
    status: str        # passed, failed, not defined, notation error, calculator limit, replaced
    detail: str = ""
    version: str = ""
    expected: str = ""  # if failed: the result written in the example
    result: str = ""       # if failed: the result obtained


def _normalize(text: str) -> str:
    return " ".join(text.split())


class _Run:
    """One example being run. `facts as in` reads another example with the
    same local ids and labels."""

    def __init__(self, module_set: ModuleSet, example: Example, parent: _Run | None = None):
        self.module_set = module_set
        self.example = example
        self.module = example.module
        self.installed = module_set.installed_modules(example.module)
        self.entities: dict[str, Entity] = parent.entities if parent else {}
        self.label: dict[str, Fact] = parent.label if parent else {}
        self.order: list[int] = parent.order if parent else [0]
        self.visited: list[str] = (parent.visited if parent else []) + [example.address]
        self.parts: dict[str, Part] = {}
        self.following: list[Part] = []
        for b in example.parts:
            if b.keyword in ("ask", "result", "action"):
                self.following.append(b)
            elif b.keyword in _SINGLE_PARTS:
                if b.keyword in self.parts:
                    raise NotationError(f"line {b.lineno}: part {b.keyword} is written twice")
                self.parts[b.keyword] = b
            else:
                raise NotationError(f"line {b.lineno}: unknown example part: {b.keyword}")
        z = self.parts.get("zone")
        self.zone = parse_zone(z.text()) if z else UTC  # PROOF-29

    # Facts

    def _to_instant(self, text: str) -> dt.datetime:
        """A date used as an instant is read as the start of the day in the
        zone of the example (appendix A §2.9)."""
        return to_instant(parse_time(_normalize(text), self.zone), self.zone)

    def _entity_named(self, name: str) -> Entity:
        if not _LOCAL_ID_RE.match(name):
            raise NotationError(f"local id is not valid: {name!r}")
        return self.entities.setdefault(name, Entity(name, name))

    def facts(self) -> list[Fact]:
        b = self.parts.get("facts")
        if b is None:
            raise NotationError(f"{self.example.address}: example without facts (PROOF-2)")
        result: list[Fact] = []
        recorded = None
        if b.content.startswith("as in "):
            other = self.module_set.find(self.module, b.content[len("as in "):].strip(), (Example,))
            if other.address in self.visited:
                raise NotationError(f"facts as in loops at {other.address}")
            result += _Run(self.module_set, other, self).facts()
        elif b.content.startswith("recorded "):
            recorded = self._to_instant(b.content[len("recorded "):])
        elif b.content:
            raise NotationError(f"line {b.lineno}: write facts recorded … or facts as in …")
        for line in b.continuation:
            result.append(self._fact_line(line, recorded, None))
        return result

    def _fact_line(self, line: Line, recorded: dt.datetime | None, action: Action | None) -> Fact:
        """One fact per line (appendix A §2.9, NOTATION-18)."""
        where = f"line {line.lineno}"
        m = _FACT_LINE.match(line.content)
        if not m:
            raise NotationError(f"{where}: fact line cannot be read")
        label, entity_name, property_name, remaining = m.groups()
        value_text = ""
        if remaining.startswith('"'):
            mq = re.match(r'"(?:[^"]|"")*"(?:@\S+)?', remaining)
            if not mq:
                raise NotationError(f"{where}: quotation mark is not closed")
            value_text, remaining = mq.group(), remaining[mq.end():]
        mb = re.search(r"(?:^|\s)valid\s+", remaining)
        if not mb:
            raise NotationError(f"{where}: a fact MUST name its valid time (NOTATION-18)")
        if value_text and remaining[:mb.start()].strip():
            raise NotationError(f"{where}: there is writing after the text")
        value_text = (value_text or remaining[:mb.start()]).strip()
        valid_text, recorded_text, kind_word, target_label = _FACT_TAIL.match(remaining[mb.end():]).groups()

        entity = self._entity_named(entity_name)
        valid = parse_time(_normalize(valid_text), self.zone)
        if action is not None:
            if recorded_text:
                raise NotationError(f"{where}: an action fact uses the recorded time of its action")
            recorded = action.recorded
        elif recorded_text:
            recorded = self._to_instant(recorded_text)
        elif recorded is None:
            raise NotationError(f"{where}: a fact MUST name its recorded time (NOTATION-18)")
        action = action or Action(recorded, EXAMPLE_ACTOR)

        fact_kind = KIND_WORDS[kind_word] if kind_word else "statement"
        target = None
        if target_label:
            if target_label not in self.label:  # NOTATION-19
                raise NotationError(f"{where}: target {target_label} is not known; give it a label")
            target = self.label[target_label]
        if (fact_kind in VALUE_KINDS) != bool(value_text):  # FACT-2
            raise NotationError(f"{where}: {fact_kind} {'requires' if fact_kind in VALUE_KINDS else 'takes no'} a value")

        if property_name == "type":
            address = TYPE_PROPERTY
            value = self.module_set.find(self.module, value_text, (Concept,)).address if value_text else None
        else:
            prop = self.module_set.find(self.module, property_name, (Property,))  # CALC-5
            address = prop.address
            value = self._parse_value(value_text, prop, where) if value_text else None
        if target is not None and (target.entity != entity or target.prop != address):  # FACT-9
            raise NotationError(f"{where}: target {target_label} is about another entity or property")
        if (fact_kind in ("replacement", "ending")  # FACT-10
                and to_instant(valid, self.zone) <= to_instant(target.valid, self.zone)):
            raise NotationError(f"{where}: {fact_kind} MUST be valid after its target; "
                                f"if the valid time of its target is wrong, use a correction")

        self.order[0] += 1
        f = Fact(entity, address, value, valid, recorded, action, fact_kind, target, label, self.order[0])
        if label:
            if label in self.label:
                raise NotationError(f"{where}: label {label} is used twice")
            self.label[label] = f
        return f

    def _parse_value(self, text: str, prop: Property, where: str) -> object:
        """The value is read according to the value type of its property (appendix A §2.9)."""
        j = prop.value_type
        if j.type_name == "number":
            return parse_number(text)
        if j.type_name == "text":
            m = re.fullmatch(r'"((?:[^"]|"")*)"(?:@([A-Za-z]+(?:-[A-Za-z0-9]+)*))?', text)
            if not m:
                raise NotationError(f"{where}: text is written between quotation marks")
            return Text(m.group(1).replace('""', '"'), m.group(2))
        if j.type_name == "yes_no":
            if text not in ("yes", "no"):
                raise NotationError(f"{where}: write yes or no")
            return text == "yes"
        if j.type_name in ("date", "instant"):
            t = parse_time(_normalize(text), self.zone)
            if isinstance(t, dt.datetime) != (j.type_name == "instant"):
                raise NotationError(f"{where}: {prop.name} has value type {j.type_name}")
            return t
        if j.type_name == "choice":
            if self.module_set.find_optional(self.module, text) is None:
                try:  # a unit is written as in the reference notation: day for d
                    text = op.unit_as_choice(parse_unit(text)).address
                except NotationError:
                    pass
            p = self.module_set.find(self.module, text, (ChoiceItem,))
            if self.module_set.choice_list_of(p) is not self.module_set.find(prop.module, j.to, (ChoiceList,)):
                raise NotationError(f"{where}: {text} is not a choice of {j.to} (VALUE-14)")
            return Choice(p.address)
        return self._entity_named(text)  # reference

    # Running

    def run(self) -> Report:
        address = self.example.address
        for keyword in ("kind", "title", "explanation"):  # PROOF-2
            if keyword not in self.parts:
                raise NotationError(f"{address}: example without {keyword} (PROOF-2)")
        status = self.parts["status"].text() if "status" in self.parts else "active"
        if status == "replaced":
            if "reason" not in self.parts:
                raise NotationError(f"{address}: a replaced example MUST name its reason (PROOF-20)")
            return Report(address, "replaced", self.parts["reason"].text(), self.module.version)
        if status != "active":
            raise NotationError(f"{address}: status active or replaced")
        kind = self.parts["kind"].text()
        if kind not in ("compute", "accept", "reject"):  # PROOF-1
            raise NotationError(f"{address}: kind compute, accept, or reject")

        store = FactStore(self.facts(), self.zone)
        keywords = [b.keyword for b in self.following]
        if kind == "compute" and keywords != ["ask", "result"]:
            raise NotationError(f"{address}: a compute example holds one ask and one result")
        if kind == "reject" and keywords != ["action", "result"]:
            raise NotationError(f"{address}: a reject example holds one action and one result")
        if kind == "accept" and (keywords[:2] != ["action", "result"]
                                 or keywords[2:] != ["ask", "result"] * ((len(keywords) - 2) // 2)):
            raise NotationError(f"{address}: an accept example holds an action and a result, "
                                f"then pairs of ask and result")

        k = 0
        if kind != "compute":
            action, action_facts = self._action(self.following[0])
            rejections = check(self.module_set, self.installed, store, action_facts, action)
            diff = self._compare_action(self.following[1], rejections)
            if diff:
                return self._failed(diff)
            store = store.with_facts(action_facts)
            k = 2
        while k < len(self.following):
            result = self._ask(self.following[k], store)
            diff = self._compare_result(self.following[k + 1], result)
            if diff:
                return self._failed(diff)
            k += 2
        return Report(address, "passed", version=self.module.version)

    def _failed(self, diff: tuple[str, str]) -> Report:
        expected, result = diff
        return Report(self.example.address, "failed", f"expected {expected}, got {result}",
                      self.module.version, expected, result)

    def _action(self, b: Part) -> tuple[Action, list[Fact]]:
        """`action recorded …, actor x, approver y` (appendix A §2.9)."""
        recorded, actor, approver = None, EXAMPLE_ACTOR, EMPTY
        for part_text in b.content.split(","):
            keyword, _, content = part_text.strip().partition(" ")
            if keyword == "recorded":
                recorded = self._to_instant(content)
            elif keyword == "actor":
                actor = self._entity_named(content.strip())
            elif keyword == "approver":
                approver = self._entity_named(content.strip())
            else:
                raise NotationError(f"line {b.lineno}: unknown action part: {keyword}")
        if recorded is None:
            raise NotationError(f"line {b.lineno}: an action MUST name its recorded time")
        action = Action(recorded, actor, approver)
        return action, [self._fact_line(x, None, action) for x in b.continuation]

    def _ask(self, b: Part, store: FactStore) -> object:
        """The result of a question, or NotComputable as a result."""
        m = _ASK_RE.match(b.text())
        if not m:
            raise NotationError(f"line {b.lineno}: write ask entity.property  T: …  R: …")
        n = parse_text(m.group(1), self.zone, b.lineno)
        if not (isinstance(n, Dot) and isinstance(n.base, Name) and n.base.name in self.entities):
            raise NotationError(f"line {b.lineno}: a question is written entity.property with a local id")
        T = parse_time(_normalize(m.group(2)), self.zone)
        evaluator = Evaluator(self.module_set, self.installed, store, self._to_instant(m.group(3)))
        env = Env(T, self.module, names=dict(self.entities))
        try:
            args = None if n.arguments is None else [evaluator.evaluate(a, env) for a in n.arguments]
            return evaluator.read_property(self.entities[n.base.name], n.name, args, T, self.module, query=True)
        except NotComputable as e:
            return e

    # Comparing (08 §2.4, PROOF-5)

    def _expected(self, text: str) -> object:
        n = parse_text(text, self.zone)
        evaluator = Evaluator(self.module_set, self.installed, FactStore([], self.zone),
                              dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc))
        return evaluator.evaluate(n, Env(None, self.module, names=dict(self.entities)))

    def _compare_result(self, b: Part, result: object) -> tuple[str, str] | None:
        if b.keyword != "result":
            raise NotationError(f"line {b.lineno}: expected result")
        text = b.text()
        written = _render(result)
        if text.startswith("not computable:"):
            kind = text.split(":", 1)[1].strip()
            if kind not in REASON_KINDS:  # NOTATION-20
                raise NotationError(f"line {b.lineno}: unknown reason kind: {kind}")
            if isinstance(result, NotComputable) and result.kind == kind:
                return None
        elif isinstance(result, NotComputable):
            pass
        elif text == "empty":
            if result is EMPTY:
                return None
        elif _same(self._expected(text), result):
            return None
        return text, written

    def _compare_action(self, b: Part, rejections: list[Rejection]) -> tuple[str, str] | None:
        """A reject example passes if all rejections are by the constraint named,
        and the entity and time named are among them (PROOF-32)."""
        if b.keyword != "result":
            raise NotationError(f"line {b.lineno}: expected result")
        text = b.text()
        written = "; ".join(map(str, rejections)) or "accepted"
        if text == "accepted":
            return None if not rejections else (text, written)
        parts = [x.strip() for x in text.split(",")]
        if not parts[0].startswith("rejected by "):
            raise NotationError(f"line {b.lineno}: write accepted, or rejected by …")
        by = parts[0][len("rejected by "):].strip()
        if not re.fullmatch(r"[A-Z]+-\d+", by):
            constraint = self.module_set.find(self.module, by, (Rule,))
            if constraint.kind != "constraint":
                raise NotationError(f"line {b.lineno}: {by} is not a constraint")
            by = constraint.address
        entity = at = None
        for x in parts[1:]:
            keyword, _, content = x.partition(" ")
            if keyword == "entity":
                entity = self._entity_named(content.strip())
            elif keyword == "at":
                at = parse_time(_normalize(content), self.zone)
            else:
                raise NotationError(f"line {b.lineno}: write entity … or at …")
        matches = (rejections and all(p.by == by for p in rejections)
                   and any((entity is None or p.entity == entity)
                           and (at is None or op.equals(p.at, at, self.zone))
                           for p in rejections))
        return None if matches else (text, written)


def _same(a: object, b: object) -> bool:
    """Exactly equal: a number with its unit; a collection regardless of order."""
    if type(a) is not type(b):
        return False
    if isinstance(a, Collection):
        remaining = list(b.members)
        for x in a.members:
            k = next((i for i, y in enumerate(remaining) if _same(x, y)), None)
            if k is None:
                return False
            remaining.pop(k)
        return not remaining
    if isinstance(a, Record):
        return (a.part_names() == b.part_names()
                and all(_same(a.get(n), b.get(n)) for n in a.part_names()))
    return a == b


def _render(x: object) -> str:
    if isinstance(x, NotComputable):
        return f"not computable: {x.kind} ({x.detail})"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, Collection):
        return "[" + ", ".join(map(_render, x.members)) + "]"
    if isinstance(x, (Number, Entity)) or x is EMPTY:
        return str(x) if isinstance(x, Number) else repr(x)
    return repr(x)


def run_example(module_set: ModuleSet, example: Example) -> Report:
    version = example.module.version
    try:
        return _Run(module_set, example).run()
    except NotDefined as e:
        return Report(example.address, "not defined", str(e), version)
    except NotationError as e:
        return Report(example.address, "notation error", str(e), version)
    except NotImplementedError as e:
        return Report(example.address, "calculator limit", str(e), version)


def read_files(*paths: str | Path) -> ModuleSet:
    modules = []
    for path in paths:
        text = Path(path).read_text(encoding="utf-8")
        modules += read(text, markdown=str(path).endswith(".md"))
    return ModuleSet(modules)


def run_all(module_set: ModuleSet) -> list[Report]:
    return [run_example(module_set, content)
            for m in module_set.all_modules() for content in m.content.values()
            if isinstance(content, Example)]


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    paths = sys.argv[1:] if argv is None else argv
    if not paths:
        print("usage: python -I -m calculator.examples file.md …")
        return 2
    module_set = read_files(*paths)
    reports = run_all(module_set)
    addresses = [m.address for m in module_set.all_modules()]
    for report in reports:
        # The address of an example does not hold a version (02 §2.3); the
        # version is shown if its module was read in more than one version.
        version = f" ({report.version})" if addresses.count(report.example.rpartition("/")[0]) > 1 else ""
        print(f"{report.status:<18} {report.example}{version}")
        if report.status != "passed" and report.detail:
            print(f"{'':<18}   {report.detail}")
    passed = sum(report.status == "passed" for report in reports)
    print(f"\n{passed} of {len(reports)} examples passed")
    return 0 if all(report.status in ("passed", "replaced") for report in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
