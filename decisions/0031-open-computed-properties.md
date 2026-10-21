# 0031. Open computed properties and contributions

Date: 2026-10-19
Status: accepted

**Context**
One number is often formed by modules from different makers. The stock of an
item increases through the purchasing module, decreases through the sales
module, and decreases while rented through Rudi's rental module. The owner of
the calculation in the vocabulary cannot possibly know all those modules.

**Decision**
- The owner of a computed property states whether its calculation is **open**
  or **closed**, like a choice list.
- In an open computed property, anyone may add a **contribution** in their
  own module, with their own address.
- A contribution must produce the same value type, quantity, and direction as
  the computed property.
- The owner's rule states how contributions are combined, in a way that does
  not depend on order: sum, min, max, all_match, or any_match.
- A contribution applies only to organizations that install the contributing
  module.
- A closed computed property may be opened in a later version. An open
  computed property must not be closed.

**Alternatives**
- *No contributions; the owner must know all the sources.* Rejected: the
  vocabulary cannot know modules made after it.
- *Others may replace the whole rule.* Rejected: one organization would have
  two meanings of stock, and the owner would lose control over the
  calculation.

**Consequences**
- The same pattern as extra properties and open lists: adding without asking
  permission and without changing what belongs to someone else.
- One event recorded in two modules is still counted twice. That is a data
  problem, and the form cannot prevent it.
