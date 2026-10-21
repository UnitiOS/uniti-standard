# 0019. One parent

Date: 2026-10-17
Status: accepted

**Context**
A concept may be a child of another concept ("Rental is a subtype of
Transaction"). It must be decided whether a concept may have more than one
parent.

**Decision**
- A concept has **at most one parent**.
- A child inherits all the properties of its parent, including the required
  ones.
- The need to "belong to two groups" is met by adding properties to a concept
  (decision 0017) and by separating type from role (decision 0018).

**Alternatives**
- *Many parents.* Rejected for now: the meaning and required properties
  inherited from two directions are easily confusing.

**Consequences**
- If it is later proven necessary, this rule can be relaxed to many parents in
  a later version of the standard without breaking existing content. The
  opposite direction would break it, which is why the stricter one is chosen.
