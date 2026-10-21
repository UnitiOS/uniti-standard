# 0039. Data in examples

Date: 2026-10-19
Status: accepted

**Context**
Examples are shared with a module to anyone who installs it, and are run in
many places. An example must not leak data, and must not mix with real
records.

**Decision**
- An entity inside an example uses a **local id**, for example `tent` or
  `r1`. When it is run, every local id is given a new identifier that is
  never used outside the example.
- An example is run in a space of its own, separate from real facts.
- An example must not contain real personal data.
- Inside an example, the recorded time is written, so that reading at two
  times can be tested.
- The parts of an action that are unimportant may be shortened to the default
  example action.

**Alternatives**
- *Real identifiers with a special marker.* Rejected: easier to leak into
  real records, and harder for people to read.
- *Real data that is disguised.* Rejected as a default method: disguises can
  often be reversed.

**Consequences**
- Examples may be shared freely together with their module.
