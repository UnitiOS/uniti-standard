# 0048. Ownership moves to v0.2

Date: 2026-10-20
Status: partly replaced by 0052. Item 4: the scale test and the second
implementation move to the first system.

**Context**
According to decision 0004, stage 4 contains the calculation rules, the
proof, and ownership. `06-calculation-rules` and `08-proof` are already
drafts and have been tested by the reference calculator. `09-ownership` was
postponed from the start, because it waits for `kajian/01-ekosistem`. Its
content is the registration of owners, governance, and how the form itself
changes, which concern law and governance more than the form.

The other forms do not need 09 to be usable and testable. Only a few open
questions wait for it.

**Decision**
1. `09-ownership` is not part of v0.1. That document is written for v0.2,
   after `kajian/01-ekosistem`.
2. The parts of v0.1 that point to 09 stay as they are, and are read as open
   questions for v0.2:
   - how to register and hold owner names (`02` ADDRESS-5). v0.1 only
     requires owner names to be unique;
   - where the deprecated and withdrawn markers are recorded, and how the
     form itself changes (`07` §8);
   - when a module counts as installed (`06` §8 question 8);
   - the terms module, owner, and install in `01-glossary`, which are marked
     provisional.
3. Stage 4 is finished for v0.1 with `06` and `08`. The order of stages stays:
   5, then 6, then 7.
4. The scale test and the second implementation test (`uji/01-hitung.md`<!-- ARCHIVE-LINK: uji/01-hitung.md -->
   §7) are done in stage 7, together with the comparison with the system.
   Uniti's own implementation could become the second implementation by
   running the same examples as the reference calculator.

**Alternatives**
- *Write the ecosystem study and then 09 before stage 5.* Rejected: v0.1 is
  held up by legal and governance questions, although the form does not
  change because of them.
- *Remove ownership from the scope of the standard.* Rejected: who may write
  what remains part of the form. Only the timing is postponed.

**Consequences**
- `README.md`: the status of 09 becomes "postponed to v0.2".
- Decision 0004 is partly replaced: ownership moves from stage 4 to v0.2.
- `uji/01-hitung.md`<!-- ARCHIVE-LINK: uji/01-hitung.md --> §7: the scale test and the second implementation in stage 7.
