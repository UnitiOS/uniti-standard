# 0012. Versions in sequence; deprecated and withdrawn without deleting

Date: 2026-10-17
Status: accepted

**Context**
Content changes from version to version. It must be decided how to number
versions, how to know how large a change is, and how to retire something
without breaking what depends on it.

**Decision**
- Versions get a **simple sequence number** (1, 2, 3, ...). The **kind of
  change** (addition, modification, deprecation) is computed by a machine by
  comparing two versions.
- **There is no deletion.** An address that has been frozen remains in every
  later version.
- A concept, property, choice, or module may be marked **deprecated**, naming
  its replacement.
- A version may be marked **withdrawn** when there is a serious error. That
  version can no longer be used or installed, but it remains readable.
- Deprecated and withdrawn are recorded statements by the owner, not edits of
  the version itself.

**Alternatives**
- *A semantic number (1.2.0) declared by the author.* Rejected: the author can
  misjudge the change, while the machine's computation cannot.
- *Allowing deletion.* Rejected: it breaks other content and the facts that
  depend on that address.

**Consequences**
- A record owned by the ecosystem is needed to store the deprecated and
  withdrawn markers (discussed together with ownership).
