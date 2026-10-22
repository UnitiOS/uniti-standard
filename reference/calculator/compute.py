"""Evaluator: computes rules at (T, R), according to form/06-calculation-rules.md.

Facts are read according to form/01-facts.md §2.5. The computing part of each
operation is in operations.py; here are the operations that read facts, use a
binder, or call other rules.

Not computable is an exception, so it spreads by itself (CALC-30), and a part
that is not computed never raises it. The computation order is the order of
writing, from the left; the members of an unordered collection are computed
by tie-breaker (CALC-52).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field, replace

from . import operations as op
from .reader import (
    Rule, WithRecord, Binary, Conditional, ValueType, Special, Concept, CollectionLiteral,
    Let, Module, Name, Call, HelperCall, Binder, RecordLiteral,
    Unary, Property, Fixed, Dot, render,
)
from .values import (
    EMPTY, UTC, Number, NotDefined, Entity, NotationError, Collection, Choice,
    Record, Range, Text, NotComputable, is_time, terminates,
    REASON_ORDER, quantity_of, to_instant, parse_unit,
)
from .module_set import ModuleSet

# The base property type, owned by the form (02 §2.1).
TYPE_PROPERTY = "standard/type"

FACT_KINDS = ("statement", "replacement", "ending", "correction", "retraction",
              "redaction")
VALUE_KINDS = ("statement", "replacement", "correction")  # FACT-2

# Operation name in the notation -> the evaluator method that computes it.
_OP_METHODS = {
    "all": "_op_all", "single": "_op_single", "count": "_op_count",
    "exists": "_op_exists", "unit_of": "_op_unit_of", "before_action": "_op_before_action",
    "each": "_op_each", "each_merged": "_op_each_merged", "group": "_op_group",
    "sum": "_op_sum", "min": "_op_min", "max": "_op_max",
    "all_match": "_op_all_match", "any_match": "_op_any_match",
    "power": "_op_power", "floor_multiple": "_op_floor_multiple",
    "range": "_op_range", "overlap": "_op_overlap", "at": "_op_at",
    "append": "_op_append", "difference": "_op_difference", "span": "_op_span",
    "split": "_op_split", "history": "_op_history", "convert": "_op_convert",
    "not_computable": "_op_not_computable", "fold": "_op_fold",
}


# --- Facts ------------------------------------------------------------------

@dataclass(frozen=True)
class Action:
    """An action that records facts, with its provenance (01 §2.4)."""

    recorded: dt.datetime
    actor: Entity
    approver: object = EMPTY
    source: str = "example"


@dataclass(eq=False)
class Fact:
    entity: Entity
    prop: str
    value: object
    valid: object
    recorded: dt.datetime
    action: Action
    fact_kind: str = "statement"
    target: Fact | None = None
    label: str | None = None
    order: int = 0

    def __repr__(self) -> str:
        return self.label or f"{self.entity!r}.{self.prop.rpartition('/')[2]}#{self.order}"


class FactStore:
    """The facts that were recorded. A fact is never changed (FACT-3)."""

    def __init__(self, facts: list[Fact] = (), default_zone: dt.timezone = UTC):
        self.facts = list(facts)
        self.default_zone = default_zone
        self._index: dict[tuple[Entity, str], list[Fact]] = {}
        for f in self.facts:
            self._index.setdefault((f.entity, f.prop), []).append(f)

    def with_facts(self, facts: list[Fact]) -> FactStore:
        return FactStore(self.facts + list(facts), self.default_zone)

    def entities(self) -> list[Entity]:
        """Every entity that has a type fact, in the order it was written."""
        result: dict[Entity, None] = {}
        for f in self.facts:
            if f.prop == TYPE_PROPERTY:
                result[f.entity] = None
        return list(result)

    def instant_of(self, t: object) -> dt.datetime:
        return to_instant(t, self.default_zone)

    def _not_after(self, a: object, b: object) -> bool:
        a, b = op._uniform(a, b, self.default_zone)
        return a <= b

    def valid_facts(self, entity: Entity, prop: str, T: object, R: dt.datetime,
                    single: bool = False) -> list[Fact]:
        """The facts valid at T, according to what is known as of R
        (01 §2.5, FACT-17). Ordered by valid time and recorded time.

        A property with one value is read as one timeline; a property with
        many values, including type, is read per value (decision 0053)."""
        known = [f for f in self._index.get((entity, prop), []) if f.recorded <= R]
        discarded = {id(f.target) for f in known if f.fact_kind in ("correction", "retraction")}
        remaining = [f for f in known if id(f) not in discarded
                     and self._not_after(f.valid, T)]
        if single:
            timeline = [f for f in remaining if f.fact_kind in VALUE_KINDS or f.fact_kind == "ending"]
            if not timeline:
                return []
            key = lambda f: (self.instant_of(f.valid), f.recorded)
            latest = max(key(f) for f in timeline)
            # Two values with the same valid time and recorded time are only
            # possible from one action; its caller rejects it (FACT-14).
            return [f for f in timeline if key(f) == latest and f.fact_kind in VALUE_KINDS]
        ended = set()
        for g in remaining:
            # A correction takes the place of its target entirely: a correction
            # of a replacement also replaces the target of that replacement.
            origin = _root_target(g)
            if origin.fact_kind in ("replacement", "ending"):
                ended.add(id(_root_target(origin.target)))
        result = [f for f in remaining if f.fact_kind in VALUE_KINDS and id(_root_target(f)) not in ended]
        return sorted(result, key=lambda f: (self.instant_of(f.valid), f.recorded, f.order))

    def is_redacted(self, f: Fact, R: dt.datetime) -> bool:
        return any(g.target is f and g.fact_kind == "redaction" and g.recorded <= R
                   for g in self._index.get((f.entity, f.prop), []))

    def value_of(self, f: Fact, R: dt.datetime) -> object:
        """The value of a valid fact. A redacted value cannot be used
        (01 §2.5 step 4)."""
        if self.is_redacted(f, R):
            raise NotComputable("redacted", f"the value of {f!r} has been redacted")
        return f.value

    def history(self, entity: Entity, prop: str, r: Range, R: dt.datetime,
                many: bool = False) -> Collection:
        """`history(x.s, in: r)`: each value with the range it was valid for,
        cut to r (06 §2.5). A property with one value gives a collection
        ordered by time. A property with many values gives a collection with
        no order, each value read as in 01 §2.5 (0057 T7)."""
        known = [f for f in self._index.get((entity, prop), []) if f.recorded <= R]
        points = [r.start, r.end] + [f.valid for f in known]
        if any(isinstance(t, dt.datetime) for t in points):
            points = [self.instant_of(t) for t in points]
        start, end, valid = points[0], points[1], points[2:]
        points = sorted({start} | {t for t in valid if start < t < end})
        slices: list[tuple[object, object, list[Fact]]] = []
        if many:
            open_: dict[int, list] = {}  # fact id → [start, end, fact]
            records: list[list] = []
            for i, t in enumerate(points):
                slice_end = points[i + 1] if i + 1 < len(points) else end
                for f in self.valid_facts(entity, prop, t, R):
                    if id(f) in open_ and open_[id(f)][1] == t:
                        open_[id(f)][1] = slice_end
                    else:
                        open_[id(f)] = entry = [t, slice_end, f]
                        records.append(entry)
            return Collection(tuple(
                Record({"value": self.value_of(f, R), "range": Range(a, b)})
                for a, b, f in records), False)
        for i, t in enumerate(points):
            slice_end = points[i + 1] if i + 1 < len(points) else end
            facts = self.valid_facts(entity, prop, t, R, single=True)
            if slices and [id(f) for f in slices[-1][2]] == [id(f) for f in facts]:
                slices[-1] = (slices[-1][0], slice_end, facts)
            else:
                slices.append((t, slice_end, facts))
        return Collection(tuple(
            Record({"value": self.value_of(f, R), "range": Range(a, b)})
            for a, b, facts in slices for f in facts), True)


def _report_topmost(failed: list[NotComputable]) -> None:
    """If any failed, report the topmost reason kind in 06 §2.9."""
    if failed:
        raise min(failed, key=lambda e: REASON_ORDER.index(e.kind))


def _root_target(f: Fact) -> Fact:
    """A correction takes the place of its target: a replacement and an ending
    of that target apply to the correction too (01 §2.5 step 3)."""
    while f.fact_kind == "correction" and f.target is not None:
        f = f.target
    return f


# --- Evaluator --------------------------------------------------------------

@dataclass(frozen=True)
class Env:
    """The environment of an expression: the valid time, the module where its
    names are looked up, the entity asked about, the local names, and the rule
    being computed."""

    T: object
    module: Module
    this: object = None
    names: dict = field(default_factory=dict)
    rule: Rule | None = None


class _Deferred:
    """The value of a `let` or a helper argument, computed when first used
    (CALC-51).

    Its expression belongs to the rule that wrote it, so it is computed with
    the rule stack as it was when it was written, not when it is used.
    Without that, `scale(b.component.base_material, …)` used inside `scale`
    would read as `scale` using itself (CALC-12).
    """

    def __init__(self, evaluator: Evaluator, expression: object, env: Env):
        self.evaluator, self.expression, self.env = evaluator, expression, env
        self.stack = list(evaluator._stack)
        self.done = False
        self.result: object = None
        self.failed: NotComputable | None = None

    def force(self) -> object:
        if not self.done:
            saved, self.evaluator._stack = self.evaluator._stack, list(self.stack)
            try:
                self.result = self.evaluator.evaluate(self.expression, self.env)
            except NotComputable as e:
                self.failed = e
            finally:
                self.evaluator._stack = saved
            self.done = True
        if self.failed is not None:
            raise self.failed
        return self.result


def _forced(args: list) -> list:
    return [x.force() if isinstance(x, _Deferred) else x for x in args]


class Evaluator:
    """Computes expressions with the facts known as of R.

    `action` and `before` are filled only when a constraint is checked:
    `before` is the same evaluator without the facts of that action
    (06 §2.12).
    """

    def __init__(self, module_set: ModuleSet, installed: list[Module], store: FactStore,
                 R: dt.datetime, *, action: Action | None = None,
                 before: Evaluator | None = None):
        self.module_set = module_set
        self.installed = installed
        self.store = store
        self.R = R
        self.zone = store.default_zone
        self.action = action
        self.before = before
        self._stack: list[tuple[Rule, object, list]] = []

    # Entities and type

    def type_facts(self, entity: Entity, T: object) -> list[Fact]:
        return self.store.valid_facts(entity, TYPE_PROPERTY, T, self.R)

    def is_a(self, entity: Entity, concept: str, T: object) -> bool:
        return any(self.module_set.is_a(f.value, concept, self.installed)
                   for f in self.type_facts(entity, T))

    def _tie_key(self, f: Fact) -> tuple:
        """The tie-breaker (06 §2.6): the valid time of the earliest type fact
        at T, its recorded time, then the identifier of the entity. In an
        example, identifiers are ordered by local id (PROOF-31)."""
        return (self.store.instant_of(f.valid), f.recorded, f.entity.identifier)

    def tie_key(self, entity: Entity, T: object) -> tuple:
        type_facts = self.type_facts(entity, T)
        if not type_facts:
            # 0057 T5 (A25), 06 §2.6: no place in the tie-breaker
            raise NotComputable("undefined order",
                                f"{entity!r} has no type fact valid at {T}, so it has no place in the order")
        return self._tie_key(type_facts[0])

    def entities_of(self, concept: str, T: object) -> list[Entity]:
        """The entities whose type fact is valid at T and which belong to that
        concept or its children (06 §2.7), ordered by tie-breaker."""
        result = []
        for h in self.store.entities():
            type_facts = self.type_facts(h, T)
            if any(self.module_set.is_a(f.value, concept, self.installed) for f in type_facts):
                # An entity with two types uses the earliest type fact,
                # whatever concept is asked about (06 §2.6).
                result.append((self._tie_key(type_facts[0]), h))
        return [h for _, h in sorted(result, key=lambda p: p[0])]

    # Reading properties

    def read_property(self, entity: Entity, name: str, args: list | None, T: object, module: Module,
                      query: bool = False) -> object:
        """`x.s` for an entity: a recorded property, a computed property, or a
        helper (appendix A §2.5)."""
        entry = self.module_set.find(module, name, (Property, Rule))
        if isinstance(entry, Property):
            if args is not None:
                raise NotationError(f"property {name} has no parameters")
            return self.property_value(entity, entry, T)
        if entry.kind not in ("computed", "helper") or entry.concept is None:
            raise NotationError(f"{name} is not a property, a computed property, or a helper of a concept")
        if query and entry.kind == "helper":
            raise NotationError(f"helper {name} MUST NOT be read as a property (CALC-7)")
        if entry.kind != "helper":  # only helper arguments are deferred (CALC-51)
            args = _forced(args or [])
        return self.compute(entry, entity, args or [], T)

    def property_value(self, entity: Entity, prop: Property, T: object) -> object:
        facts = self.store.valid_facts(entity, prop.address, T, self.R, single=not prop.value_type.many)
        value = [self.store.value_of(f, self.R) for f in facts]
        if prop.value_type.many:
            return Collection(tuple(value), False)
        if len(value) > 1:
            raise NotationError(
                f"{entity!r}.{prop.name} has {len(value)} values at {T}, although "
                f"its property has one value: {facts} (FACT-14)")
        return value[0] if value else EMPTY

    # Computing rules

    def compute(self, rule: Rule, entity: object, args: list, T: object) -> object:
        """The result of a rule for an entity, at T (06 §2.3)."""
        if len(args) != len(rule.parameters):
            raise NotationError(
                f"{rule.address} requires {len(rule.parameters)} parameters, given {len(args)}")
        if rule.concept is not None:
            concept = self.module_set.find(rule.module, rule.concept, (Concept,))
            if not self.is_a(entity, concept.address, T):  # CALC-54
                return EMPTY
        if entity is None and any(a is rule for a, _, _ in self._stack):
            raise NotationError(f"helper without a concept {rule.name} uses "
                                f"itself (CALC-12)")
        for i, (a, h, p) in enumerate(self._stack):
            if a is rule and h == entity and _forced(p) == _forced(args):
                chain = [repr(x[1]) for x in self._stack[i:]] + [repr(entity)]
                raise NotComputable("cycle", f"{rule.address}: {' → '.join(chain)}")
        self._stack.append((rule, entity, args))
        try:
            env = Env(T, rule.module, entity, dict(zip(rule.parameters, args)), rule)
            return self._check_result(rule, self.evaluate(rule.expression, env))
        except NotComputable as e:
            e.where.append(f"{rule.address}, entity {entity!r}, T {T}")
            raise
        finally:
            self._stack.pop()

    def _check_result(self, rule: Rule, x: object) -> object:
        if rule.kind == "constraint":
            return op.as_yes_no(x, f"constraint {rule.name}")
        if rule.kind == "contribution":
            return x
        return self._check_type(rule.result, x, rule.address,
                                final=rule.kind == "computed")

    def _check_type(self, value_type: ValueType, x: object, what: str, final: bool) -> object:
        """The result matches its card (CALC-8, CALC-24). For a computed
        property, also CALC-21 and direction (06 §2.10)."""
        if x is EMPTY:
            return x
        if value_type.many:
            if not isinstance(x, Collection):
                raise NotationError(f"{what}: the result is {op._type_name(x)}, although it has many values")
            return Collection(tuple(self._check_single(value_type, m, what, final)
                                    for m in x.members), False)
        return self._check_single(value_type, x, what, final)

    def _check_single(self, value_type: ValueType, x: object, what: str, final: bool) -> object:
        j = value_type.type_name
        if j == "date":
            matches = isinstance(x, dt.date) and not isinstance(x, dt.datetime)
        elif j == "instant":
            matches = isinstance(x, dt.datetime)
        else:
            matches = isinstance(x, {"text": Text, "number": Number, "yes_no": bool,
                                     "choice": Choice, "reference": Entity, "collection": Collection,
                                     "record": Record, "range": Range}[j])
        if not matches:
            raise NotationError(f"{what}: the result is {op._type_name(x)}, although its card says {j} (CALC-8)")
        if j != "number" or value_type.direction is None:
            return x
        if value_type.quantity is None:
            if not x.unit.dimensionless:
                raise NotationError(f"{what}: the result {x} has a unit, although it has no quantity")
        elif x.unit.dimensionless:
            if x.value == 0:  # CALC-55
                raise NotComputable("unit mismatch", f"{what}: the result is zero without "
                                    f"a unit, although its card has a quantity")
            raise NotationError(f"{what}: the result {x} has no unit, although it has a quantity (CALC-24)")
        elif quantity_of(x.unit) != value_type.quantity:
            raise NotationError(f"{what}: unit {x.unit} does not match its quantity (CALC-24)")
        if final and not terminates(x.value):
            raise NotComputable("needs rounding", f"{what}: {x} does not terminate (CALC-21)")
        if final and value_type.direction == "no_direction" and x.value < 0:
            raise NotComputable("direction violated", f"{what}: {x} is negative, although it has no direction")
        return x

    # Expressions

    def evaluate(self, n: object, env: Env) -> object:
        if isinstance(n, Fixed):
            return n.value
        if isinstance(n, Name):
            return self._name(n, env)
        if isinstance(n, Special):
            return self._special(n, env)
        if isinstance(n, Dot):
            return self._dot(n, env)
        if isinstance(n, Call):
            return getattr(self, _OP_METHODS[n.name])(n, env)
        if isinstance(n, HelperCall):
            return self._helper_call(n, env)
        if isinstance(n, Unary):
            x = self.evaluate(n.x, env)
            return op.negate(x) if n.op == "−" else op.negate_bool(x)
        if isinstance(n, Binary):
            return self._binary(n, env)
        if isinstance(n, Conditional):
            pick = op.as_yes_no(self.evaluate(n.condition, env), "if")
            return self.evaluate(n.then if pick else n.otherwise, env)
        if isinstance(n, WithRecord):
            return op.with_part(self.evaluate(n.record, env), n.name, self.evaluate(n.value, env))
        if isinstance(n, Let):
            return self._let(n, env)
        if isinstance(n, RecordLiteral):
            return Record({k: self.evaluate(v, env) for k, v in n.parts})
        if isinstance(n, CollectionLiteral):
            return Collection(tuple(self.evaluate(a, env) for a in n.members), True)
        raise NotationError(f"cannot be computed here: {render(n)}")

    def _binary(self, n: Binary, env: Env) -> object:
        if n.op in ("and", "or"):  # the right side only if needed (06 §2.5)
            left = op.as_yes_no(self.evaluate(n.a, env), n.op)
            if left == (n.op == "or"):
                return left
            return op.as_yes_no(self.evaluate(n.b, env), n.op)
        a, b = self.evaluate(n.a, env), self.evaluate(n.b, env)
        z = self.zone
        if n.op == "+":
            return op.add(a, b, z)
        if n.op == "−":
            return op.subtract(a, b, z)
        if n.op == "×":
            return op.multiply(a, b)
        if n.op == "÷":
            return op.divide(a, b)
        if n.op == "in":
            return op.within(a, b, z)
        return op.compare(n.op, a, b, z)

    def _name(self, n: Name, env: Env) -> object:
        """A local name, then a choice, then a unit (appendix A §2.5)."""
        choice = self.module_set.choice_named(env.module, n.name)
        if n.name in env.names:
            if choice is not None:
                raise NotationError(f"local name {n.name} equals a choice name (NOTATION-11)")
            x = env.names[n.name]
            return x.force() if isinstance(x, _Deferred) else x
        if choice is not None:
            return choice
        try:
            s = parse_unit(n.name)
        except NotationError:
            raise NotationError(f"line {n.lineno}: unknown name: {n.name}") from None
        return op.unit_as_choice(s)

    def _special(self, n: Special, env: Env) -> object:
        if n.keyword == "T":
            return env.T
        if n.keyword == "this":
            if env.this is None:
                raise NotationError("this exists only in a rule of a concept")
            return env.this
        if n.keyword == "this_action":
            self._constraint_only(env, "this_action")
            return Record({"actor": self.action.actor, "approver": self.action.approver})
        return self._contributions(env)

    def _constraint_only(self, env: Env, keyword: str) -> None:
        if env.rule is None or env.rule.kind != "constraint":
            raise NotationError(f"{keyword} MAY be used only in a constraint (CALC-40)")
        if self.action is None:
            raise NotationError(f"{keyword} can only be read while an action is checked")

    def _dot(self, n: Dot, env: Env) -> object:
        x = self.evaluate(n.base, env)
        if x is EMPTY:
            return EMPTY
        if isinstance(x, Entity):
            args = None if n.arguments is None else [_Deferred(self, a, env) for a in n.arguments]
            return self.read_property(x, n.name, args, env.T, env.module)
        if n.arguments is not None:
            raise NotationError(f"{render(n)}: only computed properties and helpers take parameters")
        return op.get_part(x, n.name)

    def _helper_call(self, n: HelperCall, env: Env) -> object:
        rule = self.module_set.find(env.module, n.name, (Rule,))
        if rule.kind != "helper" or rule.concept is not None:
            raise NotationError(f"line {n.lineno}: {n.name}(…) is not a helper without a concept")
        return self.compute(rule, None, [_Deferred(self, a, env) for a in n.arguments], env.T)

    def _let(self, n: Let, env: Env) -> object:
        """A `let` is computed only when used, like the branch of an `if` that
        is not chosen (CALC-51)."""
        names = dict(env.names)
        while isinstance(n, Let):
            names[n.name] = _Deferred(self, n.value, replace(env, names=dict(names)))
            n = n.body
        return self.evaluate(n, replace(env, names=names))

    def _bind(self, p: Binder, env: Env, *values: object) -> object:
        names = dict(env.names)
        names.update(zip(p.names, values))
        return self.evaluate(p.body, replace(env, names=names))

    def _members(self, n: Call, env: Env, binder: Binder | None,
                 use_value: bool = False) -> tuple[Collection, list]:
        """The members of a collection, after its binder is computed. An
        unordered collection whose members are not entities has no computation
        order: all its members are computed, and if several fail, the reason
        kind reported is the topmost one in 06 §2.9 (decision 0054)."""
        k = op._as_collection(self.evaluate(n.positional[0], env), n.name)
        unordered = not k.ordered and not all(isinstance(m, Entity) for m in k.members)
        if binder is None:
            value = list(k.members)
        elif not unordered:
            value = [self._bind(binder, env, m) for m in k.members]
        else:
            value, failed = [], []
            for m in k.members:
                try:
                    value.append(self._bind(binder, env, m))
                except NotComputable as e:
                    failed.append(e)
            _report_topmost(failed)
        if use_value and unordered and any(x is EMPTY for x in value):
            raise NotComputable("empty value", f"empty value used for {n.name}")
        return k, value

    def _second_binder(self, n: Call) -> Binder | None:
        if len(n.positional) > 1 and isinstance(n.positional[1], Binder):
            return n.positional[1]
        return None

    def _contributions(self, env: Env) -> Collection:
        """The result of all contributions for `this`, from the installed
        modules (06 §2.11). Unordered."""
        computed_rule = env.rule
        if computed_rule is None or computed_rule.kind != "computed" or not computed_rule.is_open:
            raise NotationError("contributions only in the rule of an open computed property (CALC-49)")
        result, failed = [], []
        for m in self.installed:
            for s in m.content.values():
                if isinstance(s, Rule) and s.kind == "contribution" \
                        and self._destination_rule(s) is computed_rule:
                    try:
                        x = self.compute(s, env.this, [], env.T)
                        result.append(self._check_type(computed_rule.result, x, s.address, final=False))
                    except NotComputable as e:
                        failed.append(e)
        _report_topmost(failed)  # contributions have no computation order
        return Collection(tuple(result), False)

    def _destination_rule(self, s: Rule) -> Rule:
        concept = self.module_set.find(s.module, s.to[0], (Concept,))
        destination = self.module_set.find(s.module, s.to[1], (Rule,))
        if destination.kind != "computed" or not destination.is_open:
            raise NotationError(f"{s.address} contributes to {destination.address}, which is not "
                                f"an open computed property (CALC-32)")
        if self.module_set.find(destination.module, destination.concept, (Concept,)) is not concept:
            raise NotationError(f"{s.address}: {destination.name} does not belong to {concept.name}")
        return destination

    # Operations (06 §2.5). Their call forms were already checked by the reader.

    def _op_all(self, n: Call, env: Env) -> Collection:
        concept = self.module_set.find(env.module, n.positional[0].name, (Concept,))
        entity = self.entities_of(concept.address, env.T)
        p = self._second_binder(n)
        if p is not None:
            entity = [h for h in entity if op.as_yes_no(self._bind(p, env, h), "all")]
        return Collection(tuple(entity), False)

    def _op_single(self, n, env):
        return op.single(self.evaluate(n.positional[0], env))

    def _op_count(self, n, env):
        return op.count(self.evaluate(n.positional[0], env))

    def _op_exists(self, n, env):
        return op.exists(self.evaluate(n.positional[0], env))

    def _op_unit_of(self, n, env):
        return op.unit_of(self.evaluate(n.positional[0], env))

    def _op_before_action(self, n, env):
        self._constraint_only(env, "before_action")
        if self.before is None:
            raise NotationError("before_action(…) MUST NOT be inside before_action(…)")
        return self.before.evaluate(n.positional[0], env)

    def _op_each(self, n, env):
        k, value = self._members(n, env, n.positional[1])
        return Collection(tuple(value), k.ordered)

    def _op_each_merged(self, n, env):
        k, value = self._members(n, env, n.positional[1])
        return op.merge(value, k.ordered)

    def _op_group(self, n, env):
        k, key = self._members(n, env, n.arg("by"))
        return op.group_by(list(zip(k.members, key)), k.ordered, self.zone)

    def _op_sum(self, n, env):
        return op.sum_values(self._members(n, env, self._second_binder(n), True)[1])

    def _two_or_collection(self, n: Call, env: Env) -> list:
        if len(n.positional) == 2 and not isinstance(n.positional[1], Binder):
            return [self.evaluate(n.positional[0], env), self.evaluate(n.positional[1], env)]
        return self._members(n, env, self._second_binder(n), True)[1]

    def _op_min(self, n, env):
        return op.smallest(self._two_or_collection(n, env), self.zone)

    def _op_max(self, n, env):
        return op.largest(self._two_or_collection(n, env), self.zone)

    def _op_all_match(self, n, env):
        return op.all_match(self._members(n, env, n.positional[1], True)[1])

    def _op_any_match(self, n, env):
        return op.any_match(self._members(n, env, n.positional[1], True)[1])

    def _op_power(self, n, env):
        return op.power(self.evaluate(n.positional[0], env), self.evaluate(n.positional[1], env))

    def _op_floor_multiple(self, n, env):
        return op.floor_multiple(self.evaluate(n.positional[0], env), self.evaluate(n.arg("of"), env))

    def _op_range(self, n, env):
        return op.make_range(self.evaluate(n.positional[0], env), self.evaluate(n.positional[1], env), self.zone)

    def _op_overlap(self, n, env):
        return op.overlap(self.evaluate(n.positional[0], env), self.evaluate(n.positional[1], env), self.zone)

    def _op_append(self, n, env):
        return op.append_item(self.evaluate(n.positional[0], env), self.evaluate(n.positional[1], env))

    def _op_at(self, n, env):
        """If the time is a range, it is read at its start (06 §2.7)."""
        t = op.require_value(self.evaluate(n.positional[0], env), "at")
        if isinstance(t, Range):
            t = t.start
        if not is_time(t):
            raise NotationError(f"at requires a time or a range, not {op._type_name(t)}")
        return self.evaluate(n.positional[1], replace(env, T=t))

    def _op_difference(self, n, env):
        return op.difference(self.evaluate(n.positional[0], env), self.evaluate(n.positional[1], env),
                             n.positional[2].unit, self.zone)

    def _op_span(self, n, env):
        return op.span(self.evaluate(n.positional[0], env), n.positional[1].unit, self.zone)

    def _op_split(self, n, env):
        return op.split(self.evaluate(n.positional[0], env), self.evaluate(n.arg("step"), env), self.zone)

    def _op_history(self, n, env):
        """Only for a recorded property (06 §2.7). Each member is a record
        `{value, range}`."""
        x_s = n.positional[0]
        x = self.evaluate(x_s.base, env)
        r = op._as_range(self.evaluate(n.arg("in"), env), "history")
        if x_s.arguments is not None:
            raise NotationError("history only for a recorded property (06 §2.7)")
        if x is EMPTY:  # 0057 T6 (A26), 06 §2.5: empty, like x.s
            return EMPTY
        if not isinstance(x, Entity):
            raise NotationError(f"history requires a property of an entity, not {op._type_name(x)}")
        prop = self.module_set.find(env.module, x_s.name, (Property, Rule))
        if not isinstance(prop, Property):
            raise NotationError("history only for a recorded property (06 §2.7)")
        # 0057 T7 (A27): many values give a collection with no order
        return self.store.history(x, prop.address, r, self.R, many=prop.value_type.many)

    def _op_convert(self, n, env):
        return op.convert(self.evaluate(n.positional[0], env), n.arg("to").unit)

    def _op_not_computable(self, n, env):
        text = self.evaluate(n.positional[0], env)
        if not isinstance(text, Text):
            raise NotationError("not_computable requires a text detail")
        raise NotComputable("declared by rule", text.content)

    def _op_fold(self, n, env):
        """Level 2. An unordered collection MUST name `order_by` (CALC-18); a
        key that is an entity, and members that tie, are ordered by
        tie-breaker (06 §2.6)."""
        k = op._as_collection(self.evaluate(n.positional[0], env), "fold")
        order_by = n.arg("order_by")
        if order_by is not None:
            pairs = [(m, self._bind(order_by, env, m)) for m in k.members]
            members = op.sort_by_key(
                pairs, k.ordered,
                lambda h: self.tie_key(h, env.T) if isinstance(h, Entity) else None, self.zone)
        elif not k.ordered:
            raise NotationError("fold over an unordered collection MUST name order_by (CALC-18)")
        else:
            members = list(k.members)
        state = self.evaluate(n.arg("initial"), env)
        for m in members:
            state = self._bind(n.arg("step"), env, state, m)
        return state
