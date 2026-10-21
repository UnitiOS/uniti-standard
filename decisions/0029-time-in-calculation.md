# 0029. Time in calculation: two times, no "now", half-open ranges

Date: 2026-10-19
Status: accepted

**Context**
Facts are read at two times (`form/01-facts.md` §2.5). A calculation result
must be readable again in the same way, and must be the same in every
implementation.

**Decision**
- The result of a computed property is always asked at (T, R). Every property
  inside a rule is read at T according to the facts known as of R.
- R never changes inside a rule. T may be replaced for part of an expression
  with `at`, and the values along a range are read with `history`.
- A rule cannot read "now". When the question is about the state today, the
  asker supplies T = today. A rule may use T as a value.
- A rule may accept a period as a parameter.
- A range is always **half-open**: from its start up to, but not including,
  its end.
- `all(K, …)` takes only the entities whose type fact is valid at T.

**Alternatives**
- *"Now" is available inside a rule.* Rejected: the result changes without
  any fact changing, and cannot be read back as the state was then.
- *Ranges closed at both ends.* Rejected: rentals 10–13 and 13–15 would count
  as overlapping, and a day could be counted twice
  (`uji/01-hitung.md`<!-- ARCHIVE-LINK: uji/01-hitung.md -->, S2 and S3).
- *A rule may read facts as of another R.* Rejected: what was known then is
  read by giving R, and what was reported then is recorded as a fact
  (decision 0033).

**Consequences**
- A fact about an event should be valid from the time of the event. The
  guidance for each concept is in the vocabulary.
