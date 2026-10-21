# 0005. Facts have no end time

Date: 2026-10-17
Status: accepted

**Context**
A fact can stop being valid: a price changes, a membership ends. The question
is whether every fact stores a start time and an end time, or only a start
time.

**Decision**
A fact has only a **valid time** (since when it is true). A fact ends when
another fact replaces it or ends it, with its own valid time. When an
organization needs to record an end date that is known in advance, for example
"contract ends 31 December", it is recorded as content (a property), not as
part of the form of a fact.

**Alternatives**
- *Every fact has a start time and an end time.* Rejected: when something
  ends, the end time of the old fact has to be edited, yet facts must not be
  edited.

**Consequences**
- The fact kinds replacement and ending are in the form of a fact (decision
  0006).
- Every fact is connected to the fact that follows it, like a sentence that
  refers to the previous sentence.
