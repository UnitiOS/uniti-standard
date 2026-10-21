# 0021. Concept cards and property cards

Date: 2026-10-17
Status: accepted

**Context**
Concepts are read by humans and machines from many organizations. A meaning
that exists only in its author's head cannot be shared.

**Decision**
- Every concept has a **concept card**. Required: address, a label in at least
  one language, definition, at least one **includes**, and at least one
  **excludes**. Allowed: parent, properties, bridges, note.
- For a concept in the vocabulary, the includes and excludes are taken from at
  least two different domains.
- Every property has a **property card**. Required: address, label,
  definition, value type, number of values, personal data marker, and,
  according to its value type, the referenced concept or its choice list.
- They are called "includes" and "excludes", not "examples", so that they are
  not confused with examples as proof (`form/08-proof.md`).

**Alternatives**
- *Only a definition, without includes and excludes.* Rejected: the meaning of
  a concept is most often wrong at its boundaries, and the boundaries are best
  shown with real examples.
- *The same strict requirement for modules and the vocabulary.* Rejected: a
  module owned by one organization does not always have examples from other
  domains.

**Consequences**
- The templates for the concept card and the property card are contained in
  `content/` (stage 6).
