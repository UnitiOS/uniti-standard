# 0054. Choices of the reference calculator moved into the text

Date: 2026-10-20
Status: accepted

**Context**
Quick test 7.3 (Indonesian archive, `uji/03-uji-singkat.md`
§6) found seven blockers, P4 to P10, that are not design mistakes. The text
could be read two ways, and the reference calculator had already chosen one
of them without writing it down. Two implementations that read only the text
could give different results (blocker H1 in 0052). In two places, P7 for
collections without order and P9, the reference calculator itself had not yet
given one definite result.

While fixing them, two more things were found:

- CONCEPT-6 is also checked for retractions. As a result, a wrong record
  cannot be retracted completely in one action, because its type is retracted
  along with it and its properties then no longer apply to any type.
- The reference calculator did not yet check FACT-10. The example in
  `conformance/14-backdated-constraints.md` uses a replacement with the same
  valid time as its target. That should be a correction.

**Decision**
1. **P4. CONCEPT-6 and VALUE-16** are only for facts that state a value, read
   at the valid time of that fact. Retraction, ending, and redaction are not
   checked. It is enough for the property to apply to one type of its
   subject; an entity that has no type at that time has no applicable
   properties.
2. **P5. `difference` in months** is the greatest *n* such that
   `a + n months` is not after `b`, with `a + n months` shifted directly from
   `a`, not month by month. If `b` is before `a`, the result is
   −`difference(b, a, month)`.
3. **P6. The pieces of `split`** are counted from the start of the range, and
   the last piece stops at the end of the range.
4. **P7. Order and reasons.**
   - An entity with several type facts that are valid uses the earliest one
     for the tie-breaker, whatever concept is asked.
   - Identifiers are compared as text, character by character by Unicode
     number, like PROOF-31.
   - A collection without order whose members are not entities, for example
     the result of `contributions`, has no calculation order. All its members
     are calculated, and what is reported is the kind of reason that is
     highest in the table of 06 §2.9.
5. **P8. A property with many values** produces a collection. Without values,
   the result is a collection with no members, not empty. It is checked with
   `count`, not `exists`. For an entity that at *T* does not belong to its
   concept, CALC-54 still applies: the result is empty.
6. **P9. Different units do not cancel each other**, even if the quantity is
   the same. IDR/day × hour does not have the unit IDR, and a money
   calculation with a result like that is a writing mistake.
7. **P10. A constraint whose result is empty** is treated as not met, with
   the kind of reason empty value.
8. The reference calculator checks FACT-10 when reading examples, and case 14
   uses a correction.

**Alternatives**
- *Leave these choices in the program only, because the program is the
  reference.* Rejected: the reference calculator is not part of the standard
  ([`reference/README.md`](../reference/README.md)). Other implementations
  read only the text and the examples.
- *P7: use the written order of the module for contributions.* Rejected: the
  order of installing modules is not part of the form, and can differ between
  organizations.
- *P9: let hour and day cancel each other, because the quantity is the
  same.* Rejected: the machine would have to convert hours to days without
  being written, although according to 06 §2.8, even 1 kg + 500 g is not
  computable unless converted first in the rule.
- *P10: an empty constraint is taken as met.* Rejected: an action would pass
  exactly when the value being checked does not exist yet.

**Consequences**
- `01-facts`: FACT-10 does not change, but is now checked.
- `03-values`: VALUE-16.
- `04-concepts`: §2.7 and CONCEPT-6.
- `06-calculation-rules`: §2.6 tie-breaker, §2.7 time units, §2.8 units, §2.9
  empty and reasons, §2.12 step 5, CALC-8, CALC-24, CALC-39, and CALC-52.
- The reference calculator changes only for P4, the P7 part about
  collections without order, P9, and FACT-10. The other choices it already
  ran.
- Their examples are in
  [`conformance/19-reading-facts.md`](../conformance/19-reading-facts.md)
  (P4), [`conformance/20-written-choices.md`](../conformance/20-written-choices.md),
  and two tests in `uji/acuan/operasi/uji_hitung.py` (Indonesian archive),
  for contributions and units.
