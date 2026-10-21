# 0035. Rejection records

Date: 2026-10-19
Status: accepted

**Context**
A rejected action records no fact at all. But business owners, auditors, and
AI need to know what was attempted and why it was rejected.

**Decision**
- Every rejected action, whether rejected by a constraint or by a rule of the
  form, is recorded as a **rejection record**: the attempted action with its
  facts, the actor and the approver, when it was attempted, and each of its
  rejections.
- A rejection record is not a fact. It is never read when facts are read and
  never affects calculation results, but it can be read back.

**Alternatives**
- *Not recorded.* Rejected: rejections cannot be examined, and the business
  owner does not know why a transaction was rejected.
- *Recorded as facts.* Rejected: a rejected action never happened, and it
  would mix with the reading of facts.

**Consequences**
- A rejection record can contain personal data from the attempted action. Its
  retention period is still an open question, together with study D2.
