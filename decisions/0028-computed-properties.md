# 0028. Computed properties are read like properties

Date: 2026-10-19
Status: accepted

**Context**
A number derived from facts, such as the total due or the stock, must be
readable by people, AI, and other rules. The form of a calculation rule and
the way its result is read must be decided.

**Decision**
- Every calculation rule has an address, and is one of: a **computed
  property**, a **helper**, a **constraint**, or a **contribution**.
- A computed property uses the same property card, plus a rule, parameters if
  any, and a statement that it is open or closed. It applies to exactly one
  concept, together with its child concepts.
- A computed property is read in the same way as a recorded property, at
  (T, R). Its value must never be recorded as a fact.
- A helper is an intermediate result. It may be an intermediate value
  (collection, record, range), is used only by rules, and is not read as a
  property.

**Alternatives**
- *A rule stands on its own, and its result appears only in reports.*
  Rejected: data and calculation results would be read in two different ways,
  and a calculation on top of a calculation would need its own mechanism.
- *One computed property with different rules for different concepts.*
  Rejected for now: one address could quietly have several meanings. A special
  rule for a child concept becomes an open question.

**Consequences**
- A calculation on top of a calculation works by itself.
- The property card for a computed property has the same parts as other
  properties, including the direction and the personal data marker.
