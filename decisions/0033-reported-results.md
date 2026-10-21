# 0033. Reported results are recorded as facts about the report

Date: 2026-10-19
Status: accepted

**Context**
The October tax report was sent with the number 12 million. Then a fact was
corrected, and the recalculation became 12.5 million. The number that was
sent must still be remembered, without making a calculation result a fact.

**Decision**
- A calculation result remains not a fact.
- What is recorded as a fact is the **act of reporting it**, with that report
  as its subject: the number that was reported, when it was sent, and from
  which computed property, parameters, T, and R the number was calculated.
- The properties for a report like this are content, provided in the
  vocabulary.

**Alternatives**
- *The result is recorded as a fact when it is reported.* Rejected: there
  would be two truths about the same tax.
- *Not recorded; just recalculate as of the R of the sending date.* Rejected:
  what was sent is an event of its own. The number could have been adjusted
  before sending, and the module set could already have been different.

**Consequences**
- The difference between what was reported and the current calculation can
  always be found.
