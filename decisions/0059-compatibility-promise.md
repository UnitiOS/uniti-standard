# 0059. The compatibility promise

Date: 2026-10-22
Status: accepted

**Context**
v0.1 is about to be locked ([`decisions/0052`](0052-quick-test-then-lock.md)),
and the first system will be built from it. Whoever builds on v0.1 must know
what later versions may change. A promise that the meaning of rules does not
change ("stable", README) cannot be checked by a machine. A promise about
results can: every conformance example has a result.

The closure before the lock ([`decisions/0057`](0057-closure-before-lock.md))
already chose the strictest answer, not computable or refused, wherever no
practical case was known, so that a later version can relax it. That choice
only helps if the relaxation is promised to be the only kind of change.

**Decision**
1. **What a result is.** For the same facts, the same modules, and the same
   question, the standard gives one of these results:
   - a **defined result**: a value, or empty;
   - **not computable**, with its reason kind;
   - for an action: **accepted**, or **rejected** by a rule or a constraint;
   - **refused**: a module, an installation, or a notation that the form does
     not allow.
2. **The promise.** From v0.1 on, a later version of the standard:
   - never changes a defined result, and never turns it into not computable,
     a rejection, or a refusal;
   - never rejects an action that v0.1 accepts;
   - may turn a not computable result, a rejection by a rule of the standard,
     or a refusal into a defined result or an acceptance. This is called
     **relaxing**, and it happens only for a practical case, with a decision
     of its own.
   A not computable result that is not relaxed keeps its reason kind, and a
   rejection that is not relaxed keeps its rule.
3. **What the promise does not cover.**
   - Parts marked **[provisional]** (README, the list of provisional parts).
   - Content: constraints, rules, and examples inside modules change by the
     versions of those modules
     ([`form/07-change.md`](../form/07-change.md)), not by the version of the
     standard.
   - Texts that are not normative: `guide/`, `rules.md`, `decisions/`,
     `reference/`.
   - **While v0.1 is locked and not yet stable**, a blocker found while
     building the first system (0052 item 4) may change a defined result, but
     only where the text could be read two ways (H1) or contradicts itself
     (H4), each time with its own decision and an entry in the change log.
     From stable on, there is no such exception.
4. **Version numbers.**
   - **v0.1.0** is the version that is locked.
   - **v0.1.1, v0.1.2, …** fix blockers, words, and links, and add examples
     and guides. They relax nothing.
   - **v0.2, v0.3, …** add: new rules, new operations, relaxing, and the
     parts that are postponed, such as ownership
     ([`decisions/0048`](0048-ownership-to-v02.md)).
   - The step to v1.0 is decided later.
5. **Conformance per version.** An implementation states the version of the
   standard it conforms to, together with its level (PROOF-26, PROOF-27), for example
   "Uniti Standard v0.1, level 1". When a later version relaxes a result, the
   conformance example that expected the old result is marked replaced in
   that version (08 §2.7). It stays readable, and it is still the test for
   the older version.
6. **Change log.** Every version lists its changes in `CHANGELOG.md`, and
   names every relaxing separately.

**Alternatives**
- *Promise only that the meaning of rules does not change.* Rejected: it
  cannot be checked, and two people read "meaning" differently.
- *Promise that no result changes at all.* Rejected: then the strictest
  answers of 0057 could never be relaxed, and the standard could only grow by
  new operations, never by covering a case that is now not computable.
- *Allow a defined result to change when it is clearly wrong.* Rejected after
  stable: someone may already rely on it. Before stable, the blocker rule of
  0052 covers it.

**Consequences**
- `README.md`: a section "Versions and compatibility".
- `CHANGELOG.md` is started when v0.1 is locked.
- `GOVERNANCE.md` names this promise as a limit on every later decision.
