# 0025. Three kinds of numbers: derived, decided, estimated

Date: 2026-10-19
Status: accepted

**Context**
An earlier experiment tried to make one way of calculating that holds all the
complexity of organizations, and every new business pattern demanded a new
calculation machine. Yet the numbers in an organization come from different
sources, and not all of them can or need to be calculated.

**Decision**
Every number or value that is not recorded directly belongs to one of three
kinds:

| Kind | Trait | Where it belongs |
|---|---|---|
| **Derived** | From the same facts, rules, and times, the result is always the same | Calculation rules; the result is not a fact |
| **Decided** | A choice taken by someone | A fact, recorded through an action |
| **Estimated** | The result of a model, a guess, or a solution search | A fact, recorded through an action with a machine or AI actor and a confidence level |

Calculation rules only handle derived numbers. Decided and estimated numbers
are always recorded in full with their provenance, but are not calculated by
the standard.

**Alternatives**
- *One calculation language that holds everything.* Rejected: it would have to
  become a complete programming language, which cannot be guaranteed to
  finish, cannot be analyzed, and cannot be tested for conformance.
- *Decided numbers calculated with default rules.* Rejected: a human choice,
  for example which invoice this payment is for, cannot be derived from other
  facts. If there is a fixed policy ("oldest first"), that policy becomes
  derived.

**Consequences**
- The standard does not need to become a complete programming language to hold
  all of reality.
- The kind is called "decided" ("penetapan"), not "decision" ("keputusan"), so
  that it is not confused with the decisions of the standard in this folder.
