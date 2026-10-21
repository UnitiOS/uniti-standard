# 0010. The address structure now, its root later

Date: 2026-10-17
Status: accepted

**Context**
The address is the most permanent part of the form, because every fact in every
organization points to an address. Uniti is imagined as an ecosystem of its
own whose content is wealth owned by that ecosystem. Who holds the root of the
address, under which domain, and with which license, concerns law and
governance, and needs a discussion of its own.

**Decision**
- The **address structure** is fixed now: `‹root›/‹owner›/‹module›/‹name›`.
  This structure supports one ecosystem with all its content under one root.
- The owner names `standard`, `uniti`, and `example` are reserved.
- **‹root›** is written as an empty placeholder marked **[provisional]**.
  Determining it is a **condition before v0.1 is frozen**.

**Alternatives**
- *Deciding the domain now.* Rejected: that decision depends on discussions
  about the ecosystem, ownership, and license that have not yet been held.

**Consequences**
- The discussion about Uniti as an ecosystem, its intellectual property, and
  its license is scheduled before stage 4 (ownership).
