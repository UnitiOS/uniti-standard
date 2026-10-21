# 0047. The entities and times at which a constraint is read

Date: 2026-10-20
Status: accepted

**Context**
06 §2.12 step 2 reads a constraint "at every valid time afterwards at which
a fact about an affected entity changes". But the affected entity has not
been defined in a way that can be calculated (finding A18). The value of a
constraint before the action also has no meaning when the constraint uses
`before_action` or `this_action` (A31). All three passed the findings gate
(0046).

Step 6 of the reference calculator tested this with six examples in
`conformance/14-backdated-constraints.md`. With the previous program, three
examples failed:
- a receipt that was corrected backwards makes the stock negative at a later
  sale, but the action is accepted, because that sale is not touched by the
  correction;
- the same for a correction nine months backwards;
- a small purchase without an approver is rejected, because an old large
  purchase is also read with the approver of this action.

The rejection example in 06 §2.12 also does not match its rule (A30): it
says "tent T4, 21 October", although that constraint applies to rentals, and
21 October exists only inside its expression.

**Decision**
1. **A constraint that reads the action**, that is, one that uses
   `before_action` or `this_action`, is about the action itself. It is read
   only for the entities directly touched by the action, at every valid time
   that the action states. Its value before the action is taken as not yet
   existing, so the action is rejected if after it that constraint is no.
   Rule CALC-57.
2. **Other constraints** are read for every entity of their concept, at every
   valid time that the action states and at every valid time of later facts.
   This way a backdated correction is also checked at later events.
3. Entities and times whose result is the same before and after the action
   never reject (step 3), so an implementation may skip them if it can prove
   the result is the same.
4. Between those times the constraint is not read. A constraint for days
   without a change of facts is still written with `split`, as is already in
   §2.12.
5. **The rejection example in §2.12 is fixed:** its entity and time are
   "rental R2, 15 October", and its message is the fixed sentence from the
   constraint card.

**Alternatives**
- *Read the constraint again only at the valid times of the facts that the
  constraint reads.* Rejected: the implementation would have to record which
  facts were read, and the text explaining it is long. The result would also
  depend on how `and` and `or` stop calculating.
- *Read the constraint only at the valid time of the action.* Rejected: a
  backdated correction that makes the stock negative at a later event would
  be accepted.
- *A constraint that reads the action is read for every entity of its
  concept, like other constraints.* Rejected: an old purchase that is not
  touched would reject an action that has nothing to do with it.

**Consequences**
- `06-calculation-rules`:
  - §2.12 steps 1 to 3, the part *Reading the action*, and the rejection
    example;
  - CALC-38 is adjusted, and CALC-57 is added;
  - §8 question 4 is answered.
- The P4 reject example in the reference calculator names its time, 15
  October.
- The reference calculator has run this decision since step 6, as a
  proposal. It is now settled.
- The cost of reading constraints again for a correction very far backwards
  remains §8 question 6.
