# Content

Status: locked (v0.1.0)
Opened: 2026-10-20

Part B of the standard: content that is used in common. Its form follows part
A, and its content may keep growing without changing the form
([`decisions/0002`](../decisions/0002-fixed-form-free-content.md)).

## 1. Purpose

Part B holds the first content that everyone shares: the card templates, the
code lists, the calculation library, and the first vocabulary. It is also the
first content written as modules in the **full form**, the form a module has
when it is frozen.

The scope is deliberately narrow. The first vocabulary holds only content that
cases from at least two domains already need. More content enters through the
vocabulary entry rules (§3).

This content was written in stage 6 of shaping the standard
([`decisions/0004`](../decisions/0004-how-to-write.md)). §5, §7, and §8
record how it was written and checked.

## 2. Map of the content

| No | File | Contents | Module |
|---|---|---|---|
| B1 | `content/README.md` | This file: the map of the content and the vocabulary entry rules | — |
| B2 | [`card-templates.md`](card-templates.md) | Templates for the concept card, property card, choice list, computed property, constraint, and helper, in the reference notation | — |
| B3 | [`code-lists.md`](code-lists.md) | The external code lists in use: currencies (ISO 4217), units (UCUM, only those in use), and languages (BCP 47), plus the list of quantities | `uniti/unit@v1` |
| B4 | [`calc.md`](calc.md) | The calculation library, moved from the paper test (Indonesian archive, `uji/acuan/pustaka/hitung.md`) and written in the full form. Its rules do not change | `uniti/calc@v1` |
| B5 | [`vocabulary/`](vocabulary/) | The first vocabulary: three modules in §4 | `uniti/party@v1`, `uniti/item@v1`, `uniti/payment@v1` |
| B6 | Tests | The reference calculator checks the full form, reads the code lists, and runs the cases of [`17-vocabulary.md`](../conformance/17-vocabulary.md) | — |

All content modules were frozen as v1 when v0.1 was locked
([`CHANGELOG.md`](../CHANGELOG.md), v0.1.0). A change makes a new version
([`form/07-change.md`](../form/07-change.md)).

## 3. Vocabulary entry rules

The requirements already exist in part A. This section only gathers them in
one place, plus one requirement from the findings gate
([`decisions/0046`](../decisions/0046-findings-gate.md)):

1. **Needed, not imagined.** A concept or property enters the vocabulary only
   if modules from at least two different domains already need it.
2. **Complete card.** The includes and the excludes are taken from at least
   two domains (CONCEPT-2).
3. **Examples from two domains** for every computed property, contribution,
   and constraint (PROOF-16).
4. **Bridge** to an external standard if a counterpart exists (RELATION-11).

Who decides whether a proposal enters the vocabulary is part of governance,
and is deferred to v0.2 together with `09-ownership`
([`decisions/0048`](../decisions/0048-ownership-to-v02.md)).

## 4. The first vocabulary

Only content that passes requirement 1 according to the cases that already
exist in [`conformance/`](../conformance/):

| Module | Contents | Cases that need it |
|---|---|---|
| [`uniti/party`](vocabulary/party.md) | Party, Person, Organization | organization (o2), finance (k2), clinic (c2), and roles in payroll, subscription, school, and loyalty, for example employee, customer, and student |
| [`uniti/item`](vocabulary/item.md) | Item, property `item` | inventory (p1 to p4), rental (s1, s4), manufacturing (m1) |
| [`uniti/payment`](vocabulary/payment.md) | Payment, properties `amount`, `date`, and `method`, list PaymentMethod | loans (j2, j3), clinic and pharmacy (16), invoice (13) |

Properties for these three concepts enter the vocabulary only if the same
property is used by cases from two domains. Other properties stay in the module
that uses them, through "applies to" (04 §2.3). For this reason Party does not
have any property yet: no case yet records the name or any other property of a
party.

What does **not** enter the first vocabulary:
- `uniti/common` with the properties `name` and `note`: mentioned as an example
  in 04 and 05, but no case needs it yet;
- `Transaction`: mentioned as an example parent in 04, but there is no case
  yet;
- `Class` and the list of reasons are absent: mentioned as vocabulary examples
  in 03, 04, and 05, but only one domain needs them so far.

## 5. Gaps

I1 to I3 were visible before the content was written. I4 to I7 were found
while writing it.

| No | Gap | Kind according to 0046 | Proposal |
|---|---|---|---|
| I1 | Codes from external standards use capital letters and signs that must not be in a choice name (ADDRESS-2), for example `IDR`, `Cel`, and `[in_i]`. UCUM also distinguishes capital and small letters, so its codes cannot be changed to small letters. As a result a choice from a code list cannot be given an address (A29) | **Passes.** It came from case K2 (exchange rate), and the machine cannot decide whether such an address is valid | A choice from a code list uses its original code, exactly. Its address is the module address, then the code: `uniti/unit/IDR`. One word is added in the head line: `choice_list Unit, code`. Decided in [`decisions/0050`](../decisions/0050-code-lists.md) |
| I2 | Appendix A §2.4 names the UCUM `mo` and `a` as counterparts of `month` and `year`. But in UCUM both are average lengths, 30.4375 days and 365.25 days, while the Uniti month and year are the calendar month and year | Content: code lists | `month` and `year` become Uniti-owned codes in the code list, with a note about UCUM |
| I3 | The form documents use vocabulary addresses that are not uniform: `uniti/item/Item` and `uniti/inventory/Item`, `uniti/item/name` and `uniti/common/name` | Fix of examples | Made the same as the first vocabulary |
| I4 | The version of the code list that applies to a module that writes a unit without using `uniti/unit` | Deferred | Examples use only the codes in the first version |
| I5 | The required parts of the choice list card are not named, so two implementations could differ on whether a module may be frozen | **Passes.** It came up while writing `PaymentMethod`, `RoundingMode`, and `RemainderRule` | Label and definition required, like the property card (VALUE-19) |
| I6 | A bridge for a choice list has no way to be written | Deferred: RELATION-11 is only a recommendation | — |
| I7 | The direction of the payment amount differs between cases: `decrease` in loans, `increase` in clinic | Content | In the vocabulary the amount has no direction |

External code lists are used directly, not made again (P8). Uniti only chooses
the codes in use and names how to write them in the reference notation, for
example `day` for the UCUM `d`. The factors between units are taken from UCUM.
If the list grows, what changes is the content, not the form.

## 6. What the first content does not hold

- A list of countries, and time zones by region (IANA). No case needs them yet.
  Time zones are still written as an offset from UTC in appendix A.
- The process and the decider for vocabulary proposals: v0.2.
- English translation: done in stage 8
  ([`decisions/0055`](../decisions/0055-locked-in-english.md)).
- Vocabulary concepts other than those in §4.

## 7. Completion criteria

§7 and §8 are a record of stage 6: what had to be true before the first
content was done, and what was found. The counts in §8 are those of that
time.

1. B1 to B5 are written. Every vocabulary module and the library pass the
   full-form card check by the reference calculator.
2. Every vocabulary concept card holds the includes and the excludes from two
   domains. This is checked by reading, because the machine does not know the
   domain of a sentence.
3. One case with two domains that uses the first vocabulary passes, and all old
   examples still pass.
4. A29 is done, and appendix A §2.4 is no longer marked [provisional].
5. Every finding has been classified according to 0046.

## 8. Result

All five criteria are met.

1. The four `uniti/*` modules in the content pass the full-form check
   (`calculator/completeness.py`). The calculation library was rewritten in the
   full form because of NOTATION-17. Its rules do not change, and 6,400 random
   comparisons with the old operations are still the same.
2. Every vocabulary concept card holds the includes and the excludes from two
   domains. The domain is written at the start of the sentence, and a small test
   checks that the prefixes differ.
3. Case [`17-vocabulary.md`](../conformance/17-vocabulary.md) passes: the
   rental shop and the school use the same vocabulary. Case 16 now uses the
   real payment vocabulary. In all, 139 examples and 172 tests pass.
4. A29 is done. K2 is back as in the paper test, with the source and target
   currencies of the exchange rate as choices. Appendix A §2.4 is no longer
   marked [provisional].
5. The findings are in §5. Two pass the gate: I1 is decided in
   [`decisions/0050`](../decisions/0050-code-lists.md), and I5 in
   [`decisions/0051`](../decisions/0051-additions-from-first-content.md). The
   rest are content, fixes of examples, or deferred.

The reference calculator also now checks two rules that already existed:
VALUE-13, a choice from another module enters only an open list, and
CONCEPT-8, a property owned by another party must not be declared required.
