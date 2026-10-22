# 0034. Constraints: yes/no rules checked per action

Date: 2026-10-19
Status: accepted

**Context**
An organization has business rules about calculation results: stock must not
be negative, an item that is being rented cannot be rented out again, a large
purchase needs manager approval. The required property (decision 0020) is not
enough to write them.

**Decision**
- A **constraint** is a calculation rule whose result is yes or no, written
  for one concept, with a card that holds a rejection message.
- Anyone may write a constraint in their own module, for a concept owned by
  anyone. A constraint applies only to organizations that install that
  module.
- A constraint is checked per action, for every entity whose result can
  change because of that action.
- An action is rejected entirely if any constraint is no after the action,
  although before it was yes or did not exist yet. A violation that already
  existed before the action does not block the action, but is reported.
- Only a constraint may read the state before the action (`before_action`)
  and the provenance of the action (`this_action.actor`,
  `this_action.approver`).
- Every rejection names the constraint and its address, the module it came
  from with the exact version, the entity and the valid time where the
  constraint failed, and its rejection message.

**Alternatives**
- *Only the owner of a concept may write constraints.* Rejected: Alex needs
  Alex's own business rules over vocabulary concepts.
- *Every constraint must be met for all entities after every action.*
  Rejected: installing a new constraint over old data would lock every
  action.
- *Permissions and status transitions as a separate machine*, as in the PoC.
  Rejected: both can be written as constraints that read the action
  (`uji/01-hitung.md`<!-- ARCHIVE-LINK: uji/01-hitung.md -->, O2 and O3).

**Consequences**
- How to check constraints after a correction whose valid time is far in the
  past still needs to be tested with the reference calculator.
