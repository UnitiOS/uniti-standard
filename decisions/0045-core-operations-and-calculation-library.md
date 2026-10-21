# 0045. Core operations and calculation library

Date: 2026-10-19
Status: accepted

**Context**
Decision 0026 set the operation list as a closed form. New operations can
only be added through standard versions. As a result, every new way of
calculating that a domain needs changes the form, for example rounding to
even or a percentile with interpolation. This conflicts with P1 and P3: what
should grow is the content, while the form stays fixed.

The symptom appears in the findings of the reference calculator. Many
findings are not about the grammar of calculation, but about the method
inside one operation:
- rounding negative numbers;
- the remainder of allocate;
- the method of the percentile;
- the median for dates.

The experiment in `uji/acuan/percobaan/`<!-- ARCHIVE-LINK: uji/acuan/percobaan/ -->
wrote `average`, `median`, `percentile`, `round`, `allocate`, and currency
conversion as helpers without a concept, using only other operations. The
result: 23 examples pass, and out of 6,400 random inputs not one gave a
result different from the built-in operations.

**Decision**

*Two parts*
1. The calculation operations are divided in two:
   - The **core operations** are the form: a closed list in `06` §2.5, the
     same in all implementations, and very rarely changed.
   - The **calculation library** is content: helpers without a concept in a
     vocabulary module. Like other content, it has an address, has versions,
     and carries examples. Anyone may write a library in their own module.
2. **The entry test for the core.** An operation enters the core only if it
   meets both:
   - it cannot be written from other core operations at the same level; and
   - it does not contain a choice of method that other domains might take
     differently.

   An operation that fails either one is written in the library.
3. **An implementation may calculate library helpers in its own way,** as
   long as the result is exactly the same, including the kind of reason
   (CALC-19). The level of a rule that uses a library helper is calculated
   from the operations inside that helper (CALC-11). `median` and
   `percentile`, for example, become level 2 because they use `fold`.

*What leaves the core*

4. **`average`, `median`, `percentile`, `round`, and `allocate` leave the
   core.** The meaning already set for these operations in 0041 and 0044 is
   not lost: it becomes the first content of the calculation library, with
   its examples.
5. **`convert` stays in the core for units with a fixed factor,** for example
   kg to g. Converting currency needs an exchange rate, which is a fact, so
   in the core the result is not computable because of unit mismatch. How to
   convert currency is written in the library.
6. **`power` stays in the core, only for whole-number exponents,** because it
   cannot be written with other operations: the core has no repetition *n*
   times.

   Fractional power leaves the list until there is a real case. It needs a
   choice of method of rounding, and also cannot be written with the core.
   The paper test uses only whole-number powers.
7. **The kind of reason *invalid weight* is removed.** A failure checked by
   the library itself uses `not_computable` with its description, so its
   kind of reason is *declared by rule*. The list of kinds of reason is only
   for core failures.

*What is added or clarified in the core*

8. **`floor_multiple(n, of: k)`**: the greatest multiple of `k` that is not
   more than `n`. Without this operation there is no way to round at all. All
   rounding methods in the library are written from this operation. Rule
   CALC-56.
9. **Helper arguments are calculated only if used,** like `let`. Without
   this, the exchange rate for a price that is already in rupiah would still
   be looked up, and could make the result fail. CALC-51.
10. **An entity may be an `order_by` key,** and is ordered by tie-breaker.
    With this, the library user writes their own order, for example sorting
    the rooms from `all` before their rental is divided. CALC-18.
11. **Members that tie but are exactly the same do not need a
    tie-breaker,** because the order does not change the result. This
    corrects 0044 item 10. According to that decision, ordering the numbers 7
    and 7 from a collection with no order is not computable because of
    undefined order. CALC-18.

*Rules*

12. **CALC-22, 23, and 50 are revoked,** because their content now belongs to
    the library. Their numbers are not reused. CALC-9, 10, 18, and 51 are
    adjusted.

**Alternatives**
- *The operation list stays as in 0026, and new operations are added through
  standard versions.* Rejected: every need of a domain changes the form, and
  the form slowly becomes a full programming language.
- *Content may add its own operations to the list.* Rejected: every
  implementation would have to know every new operation, and the meaning of
  that operation is not proven by examples.
- *A helper accepts a binding (`x: u`) as an argument, like an operation.*
  Postponed: the core becomes stronger and harder to check. For now, the user
  writes `median(each(k, x: x.duration))`.
- *`allocate` in the library chooses its own order, like the old operation:
  the order of the collection if it has an order, tie-breaker if not.*
  Rejected: the core cannot tell an ordered collection from an unordered one,
  and an order that changes quietly is hard to check. The user writes their
  own order.
- *`power` leaves entirely.* Rejected: whole-number power is used in the
  paper test, for installments, and cannot be written with the core.

**Consequences**
- `06-calculation-rules`:
  - §2.5 to §2.9: the operation list becomes the core, plus the calculation
    library;
  - §3: rule CALC-56 is added, CALC-22, 23, and 50 are revoked;
  - §5 to §8.
- `appendix/A-notation` §2.7 and §5.
- `01-glossary`: core operations and calculation library.
- Decisions 0026, 0041, and 0044 are partly replaced by this decision.
- The **first calculation library** is written in `content/` in stage 6.
  Until then, its draft is in `uji/acuan/pustaka/hitung.md`<!-- ARCHIVE-LINK: uji/acuan/pustaka/hitung.md -->,
  and that draft is not part of the standard.
- `uji/01-hitung.md`<!-- ARCHIVE-LINK: uji/01-hitung.md --> stays written with
  the old operations, as a record of the paper test. Its cases are rewritten
  with the core and the library in step 4 of the reference calculator.
- The reference calculator follows this decision. Tests for operations that
  leave the core become library tests, with the same numbers.
- Four new open questions in `06` §8:
  - examples for helpers without a concept;
  - the kinds of parameters and results of helpers;
  - bindings and named arguments for helpers;
  - the calendar month.
