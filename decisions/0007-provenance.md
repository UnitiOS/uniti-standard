# 0007. Provenance: its parts are form, its choices are content

Date: 2026-10-17
Status: accepted

**Context**
Every fact must be able to answer who stated it, through what, from where, and
when. But the kinds of sources and reasons in the real world are unlimited:
typed in, imported, a sensor, another system, AI, and so on.

**Decision**
- A fact is recorded by an **action**. The action carries the provenance: the
  **actor**, the **approver** (when the actor is not responsible alone), the
  **recorded time**, the **source**, the **action name**, the **reason**, and
  also a confidence level and a basis of authority that may be filled in.
- Those parts are **form**. The choices for them (the kinds of source, the
  list of reasons, the confidence levels) are **content** in the vocabulary,
  and can keep growing.
- An actor is an entity. Whether it is a person, an AI, or a machine is a fact
  about that actor, not part of the form.
- The approver is required when the actor acts for someone else, so that it is
  always clear which human is responsible for what an AI or a machine records.

**Alternatives**
- *A fixed list of sources in the form.* Rejected: it would always fall short
  and force the form to change.
- *All provenance as free content.* Rejected: there would be no guarantee that
  every fact can be traced.

**Consequences**
- The vocabulary provides an initial list of kinds of source and reasons.
