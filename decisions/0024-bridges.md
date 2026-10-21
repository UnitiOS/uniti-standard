# 0024. Bridges by anyone, as annotations

Date: 2026-10-17
Status: accepted

**Context**
Uniti concepts need to be connected to their equivalents in outside standards
and to similar concepts in other modules. It must be decided who may state
them and what the consequence is.

**Decision**
- Anyone may make a bridge, **in their own module**, to any address.
- A bridge is recorded in the name of its maker, and applies only to
  organizations that install its module.
- A bridge is an **annotation**: it does not change the meaning of the content
  it points to, and does not create, change, or reject facts. Combining facts
  across bridged content is a calculation rule.

**Alternatives**
- *Only the owner of the vocabulary may make bridges.* Rejected: the owner of
  the vocabulary becomes a bottleneck, and organizations cannot connect their
  own content.
- *A "same as" bridge automatically unifies facts.* Rejected: one statement
  from one party could silently change the numbers of another organization.

**Consequences**
- Bridges that contradict each other from different modules are still an open
  question.
