# 0052. Stage 7 becomes a quick test, then v0.1 is locked, and the first system is built new

Date: 2026-10-20
Status: accepted

**Context**
According to 0004, stage 7 freezes v0.1, then compares it with the system.
According to 0048 item 4, the scale test and the second implementation are
also done in stage 7. There are three problems:

- **The prototype was built with another model.** Every difference from the
  prototype provokes the question "which one is right", and the answer proves
  nothing about the standard.
- **A large test is the same as building a second system** only to test the
  standard. A scale test also needs a fast implementation, and the reference
  calculator is deliberately slow.
- **A large test always produces many findings.** Without a firm limit, this
  stage never ends and turns into endless small refinements.

After v0.1, the owner will immediately build a **new system** from the
standard. The prototype is not changed. Its components that already work are
taken, but must follow the standard. That system is the real second
implementation.

**Decision**
1. **Stage 7 is a quick test**, mostly on paper. Its purpose is to make sure
   that the standard makes sense, and is logically better than the
   prototype. There are three questions, and the results are written in
   `uji/03-uji-singkat.md` (Indonesian archive):
   - **7.1** Does the standard solve the problems found in the prototype? The
     list is closed, plus one module swap case run by the reference
     calculator.
   - **7.2** Is anything missing? What already works well in the prototype
     and falls within the scope of the standard must have a place in the
     standard.
   - **7.3** Does the standard make sense as a whole? What is looked for is
     contradictions between documents, its size, and the reach of changes.
     Plus one comparison reading by a separate agent that reads only the
     standard.
2. **The rules of play for stages 7 and 8.** Only **blockers** are fixed. A
   finding is called a blocker only if it meets one of four conditions:
   - **H1.** The text can be read two ways, so two implementations could
     differ in result.
   - **H2.** A real case cannot be written with the form. A shortage of
     content does not count.
   - **H3.** The form forces recalculating everything in ordinary
     circumstances.
   - **H4.** Two documents of the standard contradict each other.

   Other findings are written in one line in the `after-v0.1` list, without
   analysis. Each blocker gets at most two rounds of fixing; after that the
   owner decides. **Emergency brake:** if there are more than five blockers,
   or one blocker in facts, addresses, or change, the test is stopped and its
   foundation is evaluated, not patched. Every step ends with a short report
   to the owner.
3. **Stage 8: locked, translated, packaged.**
   - ‹root› is decided.
   - The normative documents are translated into English: `00-principles`,
     `01-glossary`, `form/`, `appendix/`, and `content/`. `keputusan/`,
     `kajian/`, and `uji/` remain in Indonesian.
   - The package: an explanation for people, one entry file for agents, and
     conformance tests from the examples that already exist.
4. **Locked is not the same as stable.**
   - **Locked:** v0.1 has the status proposed, and there are no more
     additions. Changes are allowed only for blockers found while building
     the first system, each with a decision of its own.
   - **Stable:** v0.1 becomes stable after the first system passes the level
     1 conformance tests (`08` §2.9), or before the ecosystem is opened to
     outside parties, whichever comes first.
5. **The first system is built new from the standard.** The prototype is not
   changed. Its components that already work may be taken, on condition that
   they follow the standard. The scale test and the second implementation
   are done in that system, and the measure is the conformance tests. The
   technology and details of that system are decided later, outside the
   standard.

**Alternatives**
- *The second implementation written blind by an agent, plus three public
  rules and a scale test, before freezing.* Rejected: it is the same as
  building a second system only to test, when the new system will do it.
- *Compare with the running prototype.* Rejected: the models of the two
  differ, and the comparison draws attention to other things.
- *Stable immediately when locked.* Rejected: form mistakes found by the
  first system could only be patched by adding, not fixed.
- *Change the prototype so that it follows the standard.* Rejected: every
  change bargains with the old form of the prototype.

**Consequences**
- 0001 is partly replaced. The result of comparison with the system is no
  longer a list of changes for the prototype, but a new system built from the
  standard.
- 0004 is partly replaced. Stage 7 becomes a quick test, and stage 8 (locked,
  translated, packaged) is added.
- 0048 item 4 is replaced. The scale test and the second implementation move
  to the first system.
- `uji/01-hitung.md` §7 (Indonesian archive) and
  `uji/README.md` (Indonesian archive) follow this decision.
- `README.md`: the meaning of the status "locked" is written in stage 8, when
  v0.1 is locked.
