# 0002. Fixed form, free content; three layers

Date: 2026-10-17
Status: accepted

**Context**
Uniti wants to be followable by open source communities, companies, and any
domain, and wants its standard not to need to change when needs grow. The
experience of the prototype shows two things:
- the part that is only form (how to record facts) stayed stable while the
  content above it changed many times;
- content concepts that were put into the base layer (for example "flow" and
  "event") turned out to be unused and had to be torn down.

Other standards that last a long time use the same pattern: shipping
containers, web addresses, and Unicode standardize the form, while the content
grows without limit.

**Decision**
- What is standardized strictly is the **form**. The **content** is free, as
  long as it is written in the form.
- There are three layers:
  - **Form** (the grammar): contains not a single domain concept;
  - **Vocabulary** (shared words): content that many organizations need;
  - **Module** (the story): the content of one field or one organization.
- The base layer that was previously called "core" now means **form only**. It
  no longer contains concepts.
- The form may only grow, very rarely, and never changes or removes what is
  already there.

**Alternatives**
- *A core containing the form plus a few universal concepts* (for example
  "entity", "event", "resource"). Rejected: concepts that look universal turn
  out to be interpreted differently by each author, and once they are in the
  base layer no one can replace them.
- *A complete standard for all needs from the start.* Rejected: its scope is
  too wide, and every wrong guess becomes permanent.

**Consequences**
- Concepts that used to be in the core move to the vocabulary, or are dropped
  if they are not needed.
- The form is tested with several domains outside the enterprise before it is
  declared stable (`00-principles` P12).
- The vocabulary starts small and grows through the rules for entering the
  vocabulary.
