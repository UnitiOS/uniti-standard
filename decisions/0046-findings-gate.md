# 0046. Findings gate: when a finding may change the form

Date: 2026-10-20
Status: accepted

**Context**
Every test finds states that the standard does not yet regulate. The
reference calculator alone has already recorded 32 findings, A1 to A32. If
every finding is answered with a new rule, the form keeps growing and slowly
becomes a programming language. That is against decision 0002: the form is
fixed, the content grows.

Most of those findings are not shortcomings of the form:
- some are content, for example the unit code list that does not yet have an
  address (A29);
- some are mistakes in writing an example, for example the rejection example
  in 06 §2.12 (A30);
- many only came to mind while writing the program, with no case that needs
  them, for example units with a power greater than 3 (A22).

By contrast, all 38 paper test cases from 12 domains and its five boundary
points run in the reference calculator without new operations or forms
(steps 4 and 5).

**Decision**
1. A finding may change the form only if it meets **both** conditions:
   - **It arises from a case.** The finding was found while writing or
     running an example for the need of a domain, not only thought of as a
     possibility.
   - **It is about the form.** The text of the standard does not say what
     must be done, so the machine cannot run, or two implementations that
     both follow the text could give different results.
2. A finding that does not meet both conditions goes into one of these
   groups, and does not change the form:
   - **Content.** Written in the vocabulary, the library, or the code lists,
     starting in stage 6.
   - **Example fix.** An example or explanation in a form document that does
     not match its rule is fixed. The rule does not change.
   - **Postponed.** Still recorded in the list of findings, but not decided.
3. **A postponed state is not guaranteed.** Its result may differ between
   implementations, and the reference calculator still stops with
   `NotDefined` in that state. Examples are contracts (0038), so an example
   must not depend on a postponed state. If an example turns out to need it,
   the finding now arises from a case and is examined again under item 1.
4. A finding that passes the gate is answered with the smallest possible
   change. What is tried first is writing it with the form that already
   exists. A new operation must still pass the core entry test (0045).
5. The grouping of findings not yet decided:

   | Finding | Group | Reason |
   |---|---|---|
   | A18 | Passes, decided in step 6 | The constraints in cases P4 and O2 depend on it |
   | A22 to A28 | Postponed | No case needs them |
   | A29 | Content, stage 6 | The unit code list is content. Until then the exchange rate is written as two numbers with units, as in K2 |
   | A30 | Example fix, in step 6 | The rule is clear; only the example in 06 §2.12 does not match |
   | A31 | Passes, decided in step 6 | Arises from O3, and without an answer the machine stops |
   | A32 | Already set in 06 §2.9 | Reporting before freezing is postponed |

**Alternatives**
- *Every finding is decided in the standard.* Rejected: the form grows
  without limit, and every implementation must follow every one of those
  decisions.
- *The form is frozen now, and all findings are rejected.* Rejected: A31
  shows that there is a real case that makes the machine stop without an
  answer from the standard.
- *Only the condition "about the form", without "arises from a case".*
  Rejected: almost every finding from the program passes that condition,
  because a program can always imagine a new state.

**Consequences**
- `reference/README.md`: the gate is mentioned in how it works, and every
  finding not yet decided is given its group.
- Step 6 of the reference calculator decides A18 and A31, and fixes the
  example for A30.
- New findings from later tests are grouped at once according to this
  decision.
