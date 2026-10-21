"""The module set and the lookup of names.

Follows form/02-addresses.md and appendix/A-notation.md §2.5: a short name is
looked up in the module where the writing is and in the modules it uses; a
full address MAY point only to that module itself or to a module it uses,
with its exact version (CALC-17).
"""

from __future__ import annotations

from .reader import ChoiceList, ContentItem, Concept, Module, ChoiceItem
from .values import NotationError, Choice


class ModuleSet:
    """All the modules that were read, from one writing or more."""

    def __init__(self, modules: list[Module]):
        self._modules: dict[tuple[str, str], Module] = {}
        for m in modules:
            if (m.address, m.version) in self._modules:
                raise NotationError(f"module {m.full_name} is written twice")
            self._modules[(m.address, m.version)] = m
        self._check_bridges()
        self._check_added_choices()
        self._check_required()

    def _check_required(self) -> None:
        """A property MAY be declared required only by the owner of its concept
        (CONCEPT-8). A concept in a module that was not read is skipped."""
        for m in self._modules.values():
            owner = m.address.partition("/")[0]
            for b in m.applies_to:
                if not any(required for _, required in b.properties):
                    continue
                try:
                    concept = self.find(m, b.concept, (Concept,))
                except NotationError:
                    continue
                if concept.module.address.partition("/")[0] != owner:
                    raise NotationError(
                        f"{m.full_name}: required property for {concept.address}, "
                        f"although that concept belongs to another party (CONCEPT-8)")

    def _check_added_choices(self) -> None:
        """A choice from another module MAY enter only an open choice list
        (VALUE-13). A code list is always closed (03 §2.6)."""
        for m in self._modules.values():
            for entry in m.content.values():
                if isinstance(entry, ChoiceItem) and "/" in entry.choice_list:
                    choice_list = self.choice_list_of(entry)
                    if choice_list.module.address != m.address and not choice_list.is_open:
                        raise NotationError(
                            f"{entry.address}: {choice_list.address} is closed (VALUE-13)")

    def _check_bridges(self) -> None:
        """A bridge to Uniti content whose module was read: the content MUST
        exist, and be of the same kind (RELATION-12). A bridge to a module that
        was not read, and to an outside standard, cannot be checked here."""
        for m in self._modules.values():
            for entry in m.content.values():
                for relation, destination in entry.bridges:
                    if "://" in destination:
                        continue
                    address, _, name = destination.rpartition("/")
                    candidates = [x for x in self._modules.values() if x.address == address]
                    if not candidates:
                        continue
                    other = [x.content[name] for x in candidates if name in x.content]
                    if not other:
                        raise NotationError(f"{entry.address}: {relation} {destination} does not exist")
                    if any(type(x) is not type(entry) for x in other):
                        raise NotationError(
                            f"{entry.address}: {relation} {destination} is not content of the same kind (RELATION-12)")

    def all_modules(self) -> list[Module]:
        return list(self._modules.values())

    def used_modules(self, m: Module) -> list[Module]:
        result = []
        for address, version in m.uses:
            if (address, version) not in self._modules:
                raise NotationError(
                    f"{m.full_name} uses {address}@{version}, which was not read")
            result.append(self._modules[(address, version)])
        return result

    def installed_modules(self, m: Module) -> list[Module]:
        """Module `m` together with all the modules it uses, directly or
        not (08 §2.2: the module set of an example)."""
        result: list[Module] = []

        def visit(x: Module) -> None:
            if x in result:
                return
            for other in result:
                if other.address == x.address:
                    raise NotationError(
                        f"two versions of {x.address} in one module set: {other.version} and {x.version}")
            result.append(x)
            for y in self.used_modules(x):
                visit(y)

        visit(m)
        return result

    # Name lookup

    def find(self, m: Module, writing: str, kinds: tuple[type, ...] = (ContentItem,)) -> ContentItem:
        entry = self.find_optional(m, writing)
        if entry is None:
            raise NotationError(f"unknown name from {m.address}: {writing}")
        if not isinstance(entry, kinds):
            names = " or ".join(k.__name__.lower() for k in kinds)
            raise NotationError(f"{writing} is not {names}")
        return entry

    def find_optional(self, m: Module, writing: str) -> ContentItem | None:
        if "/" in writing:
            address, _, name = writing.rpartition("/")
            for x in [m] + self.used_modules(m):
                if x.address == address:
                    return x.content.get(name)
            raise NotationError(
                f"{writing}: module {address} is not used by {m.address} (CALC-17)")
        found = [x.content[writing] for x in [m] + self.used_modules(m) if writing in x.content]
        if len(found) > 1:
            raise NotationError(
                f"{writing} is in more than one module; write its full address (NOTATION-9)")
        return found[0] if found else None

    def choice_named(self, m: Module, name: str) -> Choice | None:
        """The choice visible from module `m`, or None."""
        entry = self.find_optional(m, name)
        return Choice(entry.address) if isinstance(entry, ChoiceItem) else None

    def choice_list_of(self, p: ChoiceItem) -> ChoiceList:
        return self.find(p.module, p.choice_list, (ChoiceList,))

    # Child concepts (04 §2.4)

    def concept_at(self, address: str, installed: list[Module]) -> Concept | None:
        module_address, _, name = address.rpartition("/")
        for m in installed:
            if m.address == module_address:
                entry = m.content.get(name)
                return entry if isinstance(entry, Concept) else None
        return None

    def is_a(self, type_address: str, concept: str, installed: list[Module]) -> bool:
        """Whether the concept at address `type_address` is the same as `concept`, or a
        child of it (CONCEPT-12)."""
        seen = []
        while type_address is not None:
            if type_address == concept:
                return True
            if type_address in seen:
                raise NotationError(f"parent chain loops: {' → '.join(seen)} (CONCEPT-10)")
            seen.append(type_address)
            k = self.concept_at(type_address, installed)
            if k is None or k.parent is None:
                return False
            type_address = self.find(k.module, k.parent, (Concept,)).address
        return False

    def ancestors(self, type_address: str, installed: list[Module]) -> list[str]:
        """The concept at address `type_address` together with all its parents."""
        result = [type_address]
        k = self.concept_at(type_address, installed)
        while k is not None and k.parent is not None:
            parent = self.find(k.module, k.parent, (Concept,))
            if parent.address in result:
                raise NotationError(f"parent chain loops at {parent.address} (CONCEPT-10)")
            result.append(parent.address)
            k = parent
        return result
