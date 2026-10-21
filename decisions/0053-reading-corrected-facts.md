# 0053. Reading facts whose history has been corrected

Date: 2026-10-20
Status: accepted

**Context**
Quick test 7.3 (`uji/03-uji-singkat.md` <!-- ARCHIVE-LINK: uji/03-uji-singkat.md -->
§6) found three blockers in the way facts are read. The emergency brake of
0052 applies because all three are in `01-facts`. All three were proven with
examples that can be run, and all failed with the earlier reference
calculator:

- **P1. A correction of a replacement.** Rate 150 is replaced by 175, then
  175 is corrected to 180. 01 §2.5 step 3 only said that a replacement of a
  target also replaces its corrections, not the reverse. As a result rate 150
  comes back to life next to 180: two rates at once. The same happens with a
  property that has many values.
- **P2. A change in the middle of a history that is learned later.** Rate 100
  from January, replaced by 150 from November. Later it is learned that the
  rate was already 120 from June. A reasonable writer would record it as a
  replacement of the January rate, and FACT-14 does not reject it. The result
  is a December rate of both 120 and 150. The only correct way under the old
  rule is to end and then replace again, and no writer would find that way on
  their own.
- **P3. A correction that shifts a date.** A goods receipt on 1 October is
  corrected to 12 October. The sale on 10 October now makes the stock
  negative, but the action is accepted, because CONCEPT-18 and constraints
  are read only at the valid times of the facts in that action, that is, 12
  October. The time 1 October, where the value disappears, is not checked.

None of the three is an added capability. A corrected history is the core of
this standard, and the rule produces two values at once, or accepts an action
that violates a constraint. This is a design mistake in the reading rule.

The root is the same for P1 and P2: a property with one value is read through
a chain of targets. The target of a replacement can become stale when the
history is corrected, while its valid time does not.

**Decision**
1. **A property with one value is read as one timeline.** The value at *T* is
   the valued fact or ending that remains with the latest valid time that is
   not after *T*. If the valid time is the same, the one recorded last. If
   that last one is an ending, there is no value. The target of a replacement
   must still be written, but is not used to read a property like this.
2. **A property with many values is still read per value**, through targets,
   because several values may validly hold at the same time.
3. **A correction takes the place of its target completely**, in both
   directions. A correction of a replacement also replaces the target of that
   replacement.
4. **FACT-14 is sharpened.** A replacement targets the value that is valid at
   its own valid time. A correction targets the fact that is wrong, including
   when that correction moves its date earlier. One action must not record
   two values for a property with one value, at the same entity and valid
   time.
5. **The times touched by an action** are the valid time of each of its
   facts, plus the valid time of the target of each correction, retraction,
   and redaction. These three change the state at the time of their target;
   a replacement and an ending do not. CONCEPT-18 and constraints are read at
   those times, and a constraint only for entities that belong to its
   concept at that time.
6. The valid time of a retraction and a redaction is not read, because their
   target is thrown away or redacted at every time. Writers SHOULD use the
   valid time of the target.

**Alternatives**
- *Keep reading through targets, then reject a replacement whose target is
  stale, and write the guidance "end, then replace again".* Rejected: the
  rule would still be correct, but writers are forced to write two unnatural
  facts for one change. The rejection would also need a new rule per action.
  The timeline solves P1 and P2 together, without a new rejection rule.
- *A timeline for all properties, including those with many values.*
  Rejected: two phone numbers that hold at the same time would overwrite each
  other.
- *Require the valid time of a retraction to equal its target.* Rejected: that
  time is not read, so the required rule would add nothing.
- *The target time of every fact is touched too, including replacements.*
  This was the first wording, and the confirming reading rejected it: an
  ordinary price replacement would read constraints again from the first
  price recorded, years earlier, although the state at that time did not
  change.

**Consequences**
- `01-facts`: §2.5 step 3 is rewritten with three examples, a note on the
  valid time of a retraction, FACT-14 is sharpened, and one reason is added
  in §6.
- `04-concepts`: §2.7 explains the times touched, and CONCEPT-18 uses them.
- `06-calculation-rules`: §2.12 steps 1 and 2, CALC-38, and CALC-57 use the
  times touched.
- The examples in 0044 still apply with the same results.
- The reference calculator: `FactStore.valid_facts` reads the timeline for a
  property with one value, and the check per action uses the times touched.
  Its examples are in
  [`conformance/19-reading-facts.md`](../conformance/19-reading-facts.md).
  Six examples for P1 to P3 failed with the earlier program. One more example
  proves that a replacement does not read the time of its target.
