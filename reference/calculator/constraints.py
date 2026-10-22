"""Checking an action: accepted or rejected.

Two kinds of rejection: by a form rule (04 §2.7: CONCEPT-6, CONCEPT-18,
VALUE-16) and by a constraint (06 §2.12). The initial facts of an example
are not checked (PROOF-30); only the action is checked.

The entities and times at which a constraint is read: 06 §2.12 steps 1 to 3,
CALC-38 and CALC-57 (decision 0047).
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass

from .reader import Rule, Special, Concept, Module, Call, Property, Fixed
from .compute import VALUE_KINDS, TYPE_PROPERTY, Action, Fact, FactStore, Evaluator
from .values import Entity, NotationError, NotComputable
from .module_set import ModuleSet


@dataclass(frozen=True)
class Rejection:
    """One rejection (06 §2.12, CALC-41)."""

    by: str                 # address of the constraint, or number of the form rule
    entity: Entity
    at: object              # valid time at which the action fails
    module: str | None = None  # the module the constraint comes from, with its exact version
    message: str | None = None
    reason: str | None = None  # reason kind, if the constraint is not computable

    def __str__(self) -> str:
        text = f"rejected by {self.by}, entity {self.entity!r}, at {self.at}"
        if self.reason:
            text += f" (not computable: {self.reason})"
        return text


class Checker:
    def __init__(self, module_set: ModuleSet, installed: list[Module], before: FactStore,
                 action_facts: list[Fact], action: Action):
        self.module_set = module_set
        self.installed = installed
        self.action = action
        self.action_facts = action_facts
        self.before_store = before
        self.after = before.with_facts(action_facts)
        self.evaluator_before = Evaluator(module_set, installed, before, action.recorded)
        self.evaluator = Evaluator(module_set, installed, self.after, action.recorded,
                                   action=action, before=self.evaluator_before)
        # `before_action(…)` inside a constraint is read with the evaluator
        # without the facts of the action, but it MAY still read `this_action`.
        self.evaluator_before.action = action

    def check(self) -> list[Rejection]:
        """All rejections; the action is accepted if the list is empty."""
        return self._form_rules() + self._check_constraints()

    # Form rules (04 §2.7)

    def _types(self, entity: Entity, T: object) -> list[str]:
        return [f.value for f in self.evaluator.type_facts(entity, T)]

    def _ancestors_of(self, types: list[str]) -> list[str]:
        result: list[str] = []
        for j in types:
            result += [k for k in self.module_set.ancestors(j, self.installed) if k not in result]
        return result

    def _applies_to_for(self, concept: list[str]) -> dict[str, bool]:
        """The properties that apply to those concepts, and whether they are required."""
        result: dict[str, bool] = {}
        for m in self.installed:
            for b in m.applies_to:
                if self.module_set.find(m, b.concept, (Concept,)).address in concept:
                    for name, required in b.properties:
                        address = self.module_set.find(m, name, (Property,)).address
                        result[address] = result.get(address, False) or required
        return result

    def _form_rules(self) -> list[Rejection]:
        # CONCEPT-6 and VALUE-16 are only for facts that state a value, and
        # are read at the valid time of that fact (decision 0054).
        rejected: list[Rejection] = []
        for f in self.action_facts:
            if f.prop == TYPE_PROPERTY or f.fact_kind not in VALUE_KINDS:
                continue
            prop = self._applies_to_for(self._ancestors_of(self._types(f.entity, f.valid)))
            if f.prop not in prop:  # CONCEPT-6
                rejected.append(Rejection("CONCEPT-6", f.entity, f.valid))
            card = self._card(f.prop)
            if card is not None and card.value_type.type_name == "reference" and f.value is not None:
                destination = self.module_set.find(card.module, card.value_type.to, (Concept,)).address
                if not self.evaluator.is_a(f.value, destination, f.valid):  # VALUE-16
                    rejected.append(Rejection("VALUE-16", f.entity, f.valid))
        for entity, T in dict.fromkeys(_touched(self.action_facts)):
            required = self._applies_to_for(self._ancestors_of(self._types(entity, T)))
            # 0057 T11c: the types the entity already had at T before the action
            required_before = self._applies_to_for(self._ancestors_of(
                [f.value for f in self.evaluator_before.type_facts(entity, T)]))
            for address, w in required.items():  # CONCEPT-18
                card = self._card(address)
                single = card is not None and not card.value_type.many
                if w and not self.after.valid_facts(entity, address, T, self.action.recorded, single):
                    # An old gap does not block (CONCEPT-18, 04 §2.7): required
                    # before the action too, and already without a value at T.
                    if required_before.get(address) and not self.before_store.valid_facts(
                            entity, address, T, self.action.recorded, single):
                        continue
                    rejected.append(Rejection("CONCEPT-18", entity, T))
                    break
        return rejected

    def _card(self, address: str) -> Property | None:
        module_address, _, name = address.rpartition("/")
        for m in self.installed:
            if m.address == module_address and isinstance(m.content.get(name), Property):
                return m.content[name]
        return None

    # Constraints (06 §2.12)

    def _check_constraints(self) -> list[Rejection]:
        # CALC-38 and CALC-57 (A18, A31). A constraint that reads the action
        # is read only for the entities the action touches, at the valid time
        # of the action. Any other constraint is read for every entity of its
        # concept, at the valid time of the action and at every later valid
        # time of a fact; an entity whose result does not change never rejects
        # (step 3).
        rejected: list[Rejection] = []
        action_times = list(dict.fromkeys(T for _, T in _touched(self.action_facts)))
        start = min(action_times, key=self.after.instant_of)
        touched = {f.entity for f in self.action_facts}
        other_times = action_times + [
            f.valid for f in self.after.facts
            if f.recorded <= self.action.recorded
            and self.after.instant_of(f.valid) > self.after.instant_of(start)]
        other_times = sorted(dict.fromkeys(other_times), key=self.after.instant_of)
        for m in self.installed:
            for s in m.content.values():
                if not (isinstance(s, Rule) and s.kind == "constraint"):
                    continue
                concept = self.module_set.find(s.module, s.concept, (Concept,)).address
                if reads_action(s.expression):
                    for T in sorted(action_times, key=self.after.instant_of):
                        rejected += self._check_constraint_at(s, concept, T, touched)
                else:
                    for T in other_times:
                        rejected += self._check_constraint_at(s, concept, T)
        return rejected

    def _check_constraint_at(self, s: Rule, concept: str, T: object,
                             only: set[Entity] | None = None) -> list[Rejection]:
        rejected = []
        existed_before = set(self.evaluator_before.entities_of(concept, T))
        for h in self.evaluator.entities_of(concept, T):
            if only is not None and h not in only:
                continue
            after, reason = self._evaluate(self.evaluator, s, h, T)
            if after:
                continue
            # Rejected if before the action it was yes or did not exist yet
            # (step 3). A constraint that reads the action has no value before
            # the action, so it counts as not existing yet (CALC-57).
            if (h in existed_before and only is None
                    and not self._evaluate(self.evaluator_before, s, h, T)[0]):
                continue
            rejected.append(Rejection(s.address, h, T, s.module.full_name,
                                      s.messages.get("en"), reason))
        return rejected

    @staticmethod
    def _evaluate(evaluator: Evaluator, s: Rule, h: Entity, T: object) -> tuple[bool, str | None]:
        """A constraint that is not computable is not satisfied (CALC-39)."""
        try:
            return evaluator.compute(s, h, [], T), None
        except NotComputable as e:
            return False, e.kind


def _touched(facts: list[Fact]) -> list[tuple]:
    """The entities and valid times the action touches: the valid time of each
    fact, and the valid time of the target of a correction, retraction, and
    redaction (04 §2.7, decision 0053). A replacement and an ending only
    change the situation from their own valid time."""
    result = []
    for f in facts:
        result.append((f.entity, f.valid))
        if f.fact_kind in ("correction", "retraction", "redaction"):
            result.append((f.entity, f.target.valid))
    return result


def reads_action(n: object) -> bool:
    """Whether the constraint expression uses `before_action(…)` or `this_action`."""
    if isinstance(n, Call) and n.name == "before_action":
        return True
    if isinstance(n, Special) and n.keyword == "this_action":
        return True
    if isinstance(n, (list, tuple)):
        return any(reads_action(x) for x in n)
    if is_dataclass(n) and not isinstance(n, (Fixed, type)):
        return any(reads_action(getattr(n, f.name)) for f in fields(n))
    return False


def check(module_set: ModuleSet, installed: list[Module], before: FactStore,
          action_facts: list[Fact], action: Action) -> list[Rejection]:
    if not action_facts:
        raise NotationError("action without facts")
    return Checker(module_set, installed, before, action_facts, action).check()
