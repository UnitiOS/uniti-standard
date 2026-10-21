# 0026. Calculation operations that are closed, layered, and always finish

Date: 2026-10-19
Status: partly replaced by 0045. The operation list becomes the core
operations, and calculation methods that contain a choice of method are written
in the calculation library, not added through standard versions.

**Context**
Calculation rules must be writable by anyone, readable by machines, checkable,
comparable between versions, and run by different implementations with the
same result. A language that is too free loses all of these properties; a
language that is too narrow cannot hold reality.

**Decision**
- Calculation rules are written with a **closed list of operations** fixed by
  the standard, not with a free programming language.
- The operation list is built from **building blocks**, not from business
  patterns: fetch, collect, summarize, compute, time, select, unit, order and
  fold, bounded recursion.
- The operations are **layered**:
  - **level 1**: all operations except order-fold and recursion;
  - **level 2**: plus order and fold;
  - **level 3**: plus bounded recursion.
  An implementation states the level it supports and is tested according to
  that level.
- Every rule **surely finishes**. A recursion that loops produces "not
  computable", not a hang.
- The result is **the same in any implementation**: exact numbers, declared
  rounding, a definite order together with its tie-breaker, and no silent
  "now".
- New operations are added through standard versions, based on real cases that
  have been tested.
- Before `06-calculation-rules` is frozen, the operation list is tested with
  hard cases from many domains (`uji/01-hitung.md`<!-- ARCHIVE-LINK: ../uji/01-hitung.md -->),
  then with the reference calculator, a scale test, and a second
  implementation.

**Alternatives**
- *Free program code.* Rejected: it cannot be checked, cannot be compared
  between versions, and only runs on one system.
- *Using an existing formula language* (FEEL, SQL, CEL). Rejected as a
  foundation, because each of those languages brings many things beyond the
  need and was not designed to read facts at two times. They may be bridged in
  an appendix.
- *One level only.* Rejected: it forces every implementation to support the
  hardest operations from the start.

**Consequences**
- The paper test becomes a condition for writing `06-calculation-rules` and
  `08-proof`.
- The conformance level becomes the technical basis of the conformance tests
  (`kajian/01-ekosistem.md`<!-- ARCHIVE-LINK: ../kajian/01-ekosistem.md -->, B7).
