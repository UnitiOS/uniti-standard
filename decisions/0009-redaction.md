# 0009. Redaction of personal data [provisional]

Date: 2026-10-17
Status: accepted as provisional; reviewed again after discussion with parties
who understand data protection law

**Context**
Data protection law in many countries (for example the GDPR in the European
Union, and similar laws in other countries) gives a person the right to ask
for their personal data to be deleted. The Uniti principles state that facts
are never lost (`00-principles` P5). The two collide.

**Decision**
- A middle point is made in the form of the fact kind **redaction**. The fact
  remains (what it is about, when, by whom), but its value can no longer be
  read by anyone. The redaction itself is recorded as a fact together with its
  reason.
- Only a property marked **personal data** may be redacted, so that numbers
  such as the value of a transaction cannot change silently.
- The technical method is left to the implementation.
- This whole part is marked **[provisional]**: its form is written now, but it
  can still change.

**Alternatives**
- *Truly deleting the fact.* Rejected: it violates the principle, and the
  history is no longer honest.
- *Ignoring the right to deletion.* Rejected: it cannot be used by
  organizations that are subject to data protection law.

**Consequences**
- The concept form and the property form need a place to mark personal data
  (stage 3).
