# 0027. Every number states its direction

Date: 2026-10-19
Status: accepted

**Context**
In the earlier experiment, the numbers that were wrong without being noticed
most often came from the meaning of a sign that was never written down: the
quantity of items going out recorded as positive and then summed as an
addition, or a balance summed like a movement.

**Decision**
- Every number property **must** state one direction:
  - **increase**: a change; positive means that afterward there is more;
  - **decrease**: a change; positive means that afterward there is less;
  - **no direction**: a change that is never negative; its direction is stated
    by another property of the same entity;
  - **position**: not a change, but how much there is at one instant.
- Changing the direction changes the meaning, so a new address is required.
- A calculation rule that mixes directions in a way that makes no sense is
  reported by the machine (detailed in `06-calculation-rules`).

**Alternatives**
- *The direction is not stated; the reader guesses from the property name.*
  Rejected: that is the very source of the errors that were found.
- *The direction is only recommended.* Rejected: the most dangerous numbers are
  exactly the numbers whose author does not feel the need to explain them.

**Consequences**
- The number property card gains one required part.
- The fourth direction was originally called "tingkat". Its name was changed
  to "posisi" (`position`) so that it is not confused with the level of
  calculation operations (decision 0026).
