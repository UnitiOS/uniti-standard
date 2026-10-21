# 0020. Required properties are checked per action

Date: 2026-10-17
Status: accepted

**Context**
Every property states its number of values, and some properties are required
for a concept. Facts are recorded one by one, so "required" cannot be checked
on each fact separately.

**Decision**
- Every property states its **number of values**: one or many.
- The requirement is checked **per action**: after all the facts in one action
  are taken into account, every entity touched by that action must have a
  value for every property that is required for its type.
- At the same time it is also checked that every property applies to the type
  of its subject, and that every reference points to an entity with the right
  concept.
- An action that fails is rejected entirely.

**Alternatives**
- *Required checked per fact.* Rejected: the first fact about an entity would
  always fail, because its other facts have not been recorded yet.
- *Required only as a warning.* Rejected: incomplete data gets in silently,
  and "required" loses its meaning.
- *Checking all entities after every action.* Rejected: one old entity that is
  not yet complete, for example after a new property is made required, would
  stop all other recording.

**Consequences**
- Making a property required does not change the meaning, but it must be
  reported separately by the machine that computes the kinds of change.
