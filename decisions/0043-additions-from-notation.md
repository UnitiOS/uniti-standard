# 0043. Seven additions in meaning found while writing the notation

Date: 2026-10-19
Status: accepted

**Context**
Writing the notation (`appendix/A-notation.md`) forced every operation to be
read as exactly as a machine reads it. It turned out that seven things were
used in the paper test or in the form documents, but their meaning had not
yet been set.

**Decision**
1. **The result of `allocate`** is an ordered collection of records
   `{member, share}`, one for each member, in the order of the collection
   being divided, or by tie-breaker if that collection has no order.
2. **The parts of a range** are read with `r.start` and `r.end`.
3. **Same as for intermediate values.** Two records are the same if the names
   of their parts are the same and each part is the same. Two ordered
   collections are the same if their members are the same, in the same
   order.
4. **`contributions`** becomes an operation in the Get group, only for the
   rule of an open computed property: the collection of the results of all
   contributions from the installed modules. Rule CALC-49.
5. **Units as values.** Every unit is a choice from the unit code list.
   `unit_of(n)` produces that choice, so it can be compared with a property
   such as the original currency of an exchange rate.
6. **The default time zone of an example** becomes a part of an example that
   may be written. If it is not written, it is UTC. Rule PROOF-29.
7. **The initial facts in an example** are not checked by constraints or by
   required properties. Only the action in the accept example and the reject
   example is checked. Rule PROOF-30.

**Alternatives**
- *The result of `allocate` with part names written by the user*, such as
  `{department, amount}` in the paper test. Rejected: fixed part names make
  the result readable by any rule.
- *The default time zone of an example follows the organization that owns the
  module.* Rejected: the result of an example would depend on who runs it.
- *Initial facts checked like an action.* Rejected: every example would have
  to contain all required properties, including those unrelated to what is
  being exemplified.

**Consequences**
- `06-calculation-rules` §2.5, §2.6, §2.11; `08-proof` §2.2, §2.3;
  `03-values` §2.3.
- Paper test cases K4, K5, and O3 are rewritten with this form when they are
  run by the reference calculator.
