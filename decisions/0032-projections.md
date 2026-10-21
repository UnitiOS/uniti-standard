# 0032. Projections: stored calculation results

Date: 2026-10-19
Status: accepted

**Context**
Decision 0008 allows calculation results to be stored to speed up reading,
without becoming a source of truth. Its form needs to be detailed.

**Decision**
- A **projection** is a stored calculation result. It names the computed
  property, the entity, the parameters, T, R, the module set used, and the
  last fact that was taken into account.
- A projection may be thrown away and rebuilt at any time.
- When a projection differs from a recalculation from the facts, the
  calculation from the facts is correct.
- A reader must be able to tell whether the result being viewed is current.
- How to store, and when to update, is left to the implementation.
- A projection for an R that has already passed never becomes stale. The
  exception is redaction [provisional]: a projection that uses a value that
  was later redacted must be thrown away.

**Alternatives**
- *Projections recorded as facts.* Rejected by decision 0008.
- *Projections without a note of when they were calculated.* Rejected: a
  reader cannot tell that the number being viewed is already out of date.

**Consequences**
- Because the operation list is closed, the machine knows the kind of every
  summary and can choose the most economical way to update a projection.
