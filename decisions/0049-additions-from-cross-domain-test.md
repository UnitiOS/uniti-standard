# 0049. Additions from the cross-domain test

Date: 2026-10-20
Status: accepted

**Context**
Stage 5 tested the parts of the form that the 125 examples of the reference
calculator had not touched: `07-change`, bridges and cross-module choices in
`05-relations`, and the contract between versions and between modules in
`08` §2.7 and §2.8 (`uji/02-lintas-domain.md`<!-- ARCHIVE-LINK: ../uji/02-lintas-domain.md -->).
All four tests, U1 to U4, passed without a new form.

The contract between versions also needs no new form. An example has an
address (02 §2.1), and every address of a version still exists in the next
version (CHANGE-6), so a new version always contains the examples of the old
version.

One gap passed the findings gate (0046). The reference notation has no way to
write a bridge, although a bridge is a part of a card (`04` §2.1). As a
result, the clinic and pharmacy example in `05` §4 cannot be written in a
module.

**Decision**
1. **A bridge is written as a part of a card** in appendix A §2.8: its
   relation word (`same_as`, `broader`, `narrower`, or `similar`), then the
   full address of the Uniti content, or the full IRI for an outside
   standard. A bridge is written on the card of the content it starts from,
   so it is always in the owner's module (RELATION-3).
2. Postponed under 0046, because no case needs them:
   - notation for the deprecated and withdrawn markers. Both are statements
     of the owner outside the version (`07` §2.4), and their place is
     postponed to v0.2 (0048);
   - bridges for choices written inside their own list, because such choices
     have no card;
   - the meaning of removing `applies to` in the next version.

**Alternatives**
- *A header line of its own, `bridge ‹address› same_as ‹address›`.* Rejected:
  `04` already makes a bridge a part of a card, and a line of its own would
  allow a bridge from content owned by someone else.

**Consequences**
- `appendix/A-notation.md` §2.8: the bridge card part, with an example.
- The reference calculator reads bridges, checks RELATION-8 and RELATION-12,
  and compares two versions of a module (`calculator/versions.py`).
