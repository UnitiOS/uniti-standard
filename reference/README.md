# Reference calculator

Status: step 6 of 6 done, plus the stage 5 tests (decision 0049) and the stage 6 content (decisions 0050 and 0051); A18, A30, and A31 were decided in decision 0047; findings A1 to A20 were decided in decision 0044, except A18; the program follows decision 0045; findings that are not yet decided are classified according to decision 0046

A small program that runs the calculation rules **exactly** according to
[`form/06-calculation-rules.md`](../form/06-calculation-rules.md), reads the
rules and examples in the reference notation
([`appendix/A-notation.md`](../appendix/A-notation.md)), and checks examples
according to [`form/08-proof.md`](../form/08-proof.md).

Like the other tests, the reference calculator is **not part of the
standard**. If this program and the standard differ, the standard is right.

## Purpose

1. To prove that the text of the standard is clear enough for a machine to run.
2. To prove the numbers in the paper test with a machine, including the
   boundary points that were not tested yet (review of the paper test §5,
   Indonesian archive, `uji/periksa/01-hitung.md`).
3. To serve as a comparison for a second implementation.

Speed is not a goal.

## How it works

- **Python 3, with no extra libraries.** Numbers are computed with exact
  fractions (`fractions.Fraction`).
- **No guessing.** A situation whose meaning the standard has not defined
  raises `NotDefined`. The calculator stops, and the situation is recorded as
  a finding below. A proposal for a finding may be run provisionally so that
  the result can be seen, and it is marked as such in the program and in the
  list of findings, until it is decided in the standard.
- **Not every finding changes the standard.** A finding may change the form
  only if it comes from a case and is about the form. The others become
  content, a fix of an example, or are postponed
  ([`decision 0046`](../decisions/0046-findings-gate.md)).
- **Three kinds of failure are told apart:** not computable (a legitimate
  result under 06 §2.9), not defined (a gap in the standard), and notation
  error (a rule or example that is written wrongly).
- Each part of the program points to the rule it runs, for instance
  `CALC-23`.
- No AI model is called.

## Running

From this folder, all tests:

```
python -I -m unittest discover -t . -s . -p "test_*.py"
```

Running the examples in a case file, with a report per example:

```
python -m calculator.examples ../conformance/00-form-examples.md
```

A case file that uses content, that is the calculation library or the code
lists, is run together with those files:
`python -m calculator.examples ../content/calc.md ../content/code-lists.md ../conformance/….md`.

Each example is reported with one of these statuses: **passed**, **failed**
(the result differs from the expected one), **not defined** (it depends on a
finding below), **notation error**, or **replaced** (PROOF-21).

## Layout

| File | Contents | Step |
|---|---|---|
| `calculator/values.py` | Exact numbers and units, time, ranges, records, collections, empty, not computable | 2 |
| `calculator/operations.py` | The core operations of 06 §2.5 that do not read facts | 2 |
| `calculator/reader.py` | The reader of the reference notation: lines, tokens, expressions, modules, cards, rules, examples | 3 |
| `calculator/module_set.py` | The modules in use, and the lookup of short names and full addresses | 3 |
| `calculator/compute.py` | The evaluator: facts at (*T*, *R*) with the six fact kinds, `all`, `at`, `history`, `fold`, recursion, contributions, the check of the result of a computed property | 3 |
| `calculator/constraints.py` | The check of an action by the form rules and constraints: accept or reject | 3 and 6 |
| `calculator/examples.py` | Runs examples and compares results exactly | 3 |
| `calculator/versions.py` | Compares two versions of a module: addition, modification, removed addresses, meaning changed, properties that became required, and behavior change | stage 5 |
| `calculator/completeness.py` | Checks the full form: the required card parts, and rules still written in short form (NOTATION-17) | stage 6 |
| `tests/` | Small tests per CALC and NOTATION rule, including boundary points, the tests of the calculation library, the tests of the version comparer and bridges, and the tests of the content | 2, 3, stage 5, and stage 6 |
| [`../content/`](../content/README.md) | The calculation library with 7 examples, the code lists, and the first vocabulary. Always read together with the cases. The calculation library was first drafted in a separate drafts folder | 3 and stage 6 |
| `../conformance/00-form-examples.md` | Examples from `06` §4, `08` §4, and appendix A §4 | 3 |
| `../conformance/01-finance.md` to `13-outside-calculation.md` | 38 paper-test cases from 12 domains, rewritten in the reference notation with the core and the calculation library, one module per case | 4 |
| `../conformance/14-backdated-constraints.md` | A constraint with backdated corrections, and a constraint that reads the action | 6 |
| `../conformance/15-change.md`, `../conformance/16-relations.md` | A new version, a user that moves to another version, behavior change, and a combined report across modules | stage 5 (cross-domain test, Indonesian archive, `uji/02-lintas-domain.md`) |
| `../conformance/17-vocabulary.md` | The first vocabulary used by a rental shop and a school | stage 6 ([`content/README.md`](../content/README.md)) |
| `../conformance/18-module-swap.md` | A shop changes cashier: the old and the new rentals are computed together, and the old rental is returned through the new cashier | stage 7, 7.1 (quick test, Indonesian archive, `uji/03-uji-singkat.md`) |
| `../conformance/19-reading-facts.md` | A corrected history: a correction of a replacement, a change that became known later, a correction that moves a date, and a retraction | stage 7, 7.3 ([decision 0053](../decisions/0053-reading-corrected-facts.md)) |
| `../conformance/20-written-choices.md` | Calendar month, `split`, an entity with two types, a property with many values, and a constraint whose result is empty | stage 7, 7.3 ([decision 0054](../decisions/0054-reference-choices-into-text.md)) |
| `tests/test_cases.py` | Every example in the cases and the content passes, and fails if its expected result is changed | 3 |
| `tools/rules_index.py`, `tests/test_rules_index.py` | Makes [`../rules.md`](../rules.md), the index of all rules, from the form documents and appendix A; the test fails when the index no longer matches them. Run `python -m tools.rules_index` after a rule changes | stage 8 |

The old experiments folder (`percobaan/`: the computation core and the
calculation library on which decision 0045 is based, with the old operations
as a comparison, run separately with `python -m percobaan.inti`) is not
included in this repository (Indonesian archive, `uji/acuan/percobaan/`).

## Steps

| Step | Contents | Status |
|---|---|---|
| 1 | Notation: `appendix/A-notation.md` | done |
| 2 | Values and operations, with small tests | done: 79 tests pass |
| 3 | Reader and evaluator; examples in `08` §4 | done: 16 examples pass, 128 tests pass after the proposals were run. After decision 0045: 23 examples and 143 tests pass |
| 4 | 38 paper-test cases in the reference notation | done: 86 examples pass. In total 109 examples and 145 tests pass |
| 5 | Extra boundary examples | done: 10 boundary examples pass. In total 119 examples and 145 tests pass |
| 6 | Constraints and backdated changes | done: 6 examples pass after the proposals A18 and A31 were run, and then decided in decision 0047. In total 125 examples and 145 tests pass |

In step 3, the examples that are only told in the form document were written
out in full: the accept example `adjoining_no_overlap`, the reject and accept
examples for `approved_if_large`, and the clinic example that is not
computable. Each example is run once more with a result that was changed on
purpose, and it must fail, so that passing is meaningful.

What the calculator does not run yet: the direction report before a rule is
frozen (CALC-31), the level of a rule (CALC-11), and the checks of a card that
do not affect the result, such as a required label. All of them are checks
before freezing, not computations.

In step 4, the 38 paper-test cases are rewritten in
`../conformance/01-finance.md` to `../conformance/13-outside-calculation.md`,
one module per case, with the core and the calculation library: 86 examples.
The expected results are taken from the paper test. All of them pass, and no
case could not be written.

What differs from the writing of the paper test, because that writing does not
follow the standard or because of decision 0045:

| Case | In the paper test | Here |
|---|---|---|
| K1 | Receipts and expenditures are both `sum`, with different directions | Two properties, because the direction is written on the property card |
| K3 | Every line has a debit and a credit. A field not filled is empty, and an empty value that is summed is not computable | Every line has a side and an amount |
| P2 | `m.type` for in or out | `m.kind`, because `type` is a base property |
| S4, G2 | A duration is compared and multiplied with a number without a unit | `÷ 1 day`, `8 hours`, and rates with units |
| O1 | `u.parent_unit = this`, although the parent of the top unit is empty | `exists(u.parent_unit) and …` (A32) |
| O3 | The pair `(draft, submitted)` | The record `{from: draft, to: submitted}` |
| K4, K5, K6, G3, J1, J2, C2, E1, E3, X1 | The old operations with named arguments and binders, for instance `round(n, to: 1 IDR, mode: nearest)` | Library helpers: `round(n, 1 IDR, nearest)`, `median(each(k, x: …))` |

P3, J3, R1, E1, and E3 are only told in the paper test; here their rules are
written out in full. Case P1 without the rental module cannot hold rental
facts, because a concept of a module that is not installed cannot be named.

**The level changed because of the library.** The level is computed from the
operations inside the library helpers (CALC-11), and `allocate`, `by_member`,
and `median` use `fold`. So K4, K5, K6, and C2 are now level 2, not level 1
as in the paper test: 22 cases of level 1, 9 of level 2, and 3 of level 3.
Decision 0045 only mentions this for `median` and `percentile`. This level is
computed by reading the rule, because the calculator does not compute levels
yet.

**Two errors in the program, found by the cases.**

- `max(0, h.hours − 8 hours)` gave 0 without a unit, although a zero without a
  unit takes the unit of the number used with it (06 §2.8). After it is
  multiplied by the wage per hour, that zero became 0 IDR/hour, which cannot
  be summed with IDR (G2). Now `min` and `max` give that zero its unit.
- Since a helper argument is computed only when used (decision 0045), the
  argument is computed inside the helper that receives it. As a result
  `scale(b.component.base_material, …)`, which calls `scale` again through
  recursion, was read as a helper that uses itself (CALC-12), although that
  argument belongs to its caller (M1). Now an argument is computed with the
  rule stack of its caller.

In step 5, the five boundary points of the review report
(review of the paper test §5, Indonesian archive, `uji/periksa/01-hitung.md`),
which were already tested as small tests in step 2, were written as full
examples in the file of their case. This step was limited to those five points
on purpose.

| Boundary point | Case | Examples | Result |
|---|---|---|---|
| Equal fractions in `allocate` | K5 | `tie_remainder_to_earlier`, `tie_other_gets_no_remainder` | The remainder of 1 rupiah goes to the department that became valid earlier (06 §2.6), not by name |
| Median for an even number of data points | C2 | `median_six_visits` | 22.5 minutes |
| Exactly half | E3 | `attended_77_of_80` | 96.25% becomes 96.3%. Rounding to even would give 96.2% |
| Boundary day of a range | P1, R1 | `available_on_start_day`, `available_on_end_day`, `balance_day_before_expiry`, `balance_on_expiry_day` | The start date is included, the end date is not |
| The `≤` boundary | O2 | `exactly_at_limit_without_approver`, `over_limit_without_approver` | 10,000,000 is accepted, 10,000,001 is rejected |

Two adjustments to the reviewer's proposal. In E3, 0.125 rounded to 0.01 was
replaced by 96.25% to 0.1%, because the case rounds to 0.1%; what is tested is
the same: exactly half with an even previous digit. In R1, the January points
were already used up before 15 Jan 2027, so the balance on that date does not
change. The boundary was tested on the expiry of the March points, 10 Mar
2027.

All examples pass without changing the program or the standard, and there are
no new findings.

In step 6, 06 §2.12 steps 2 and 3 were tested with six examples in
`../conformance/14-backdated-constraints.md`. With the previous program, three
examples failed:

| Example | Expected | Previous program | Finding |
|---|---|---|---|
| `violating_backdated_correction` | The receipt of 1 October is corrected, stock is negative at the sale of 5 October: rejected at 5 October | Accepted, because the sale is not touched by the correction, so 5 October is not read | A18 |
| `correction_far_in_the_past` | A correction of January, stock is negative at the third sale after it: rejected at 20 September | Accepted, for the same reason | A18 |
| `small_after_old_large` | A small purchase without an approver is accepted, even though there is an old large purchase | Rejected by that old purchase, because the constraint is read for every purchase, with the approver of this action | A18 and A31 |

The proposal that was run in `constraints.Checker._check_constraints`, and
then decided in [`decision 0047`](../decisions/0047-constraints-and-backdated-changes.md):

- **A constraint that reads the action** (`before_action`, `this_action`) is
  about the action itself. It is read only for the entities the action
  touches, at the valid time of the action, and before the action it counts as
  not existing yet (A31).
- **Any other constraint** is read for every entity of its concept, at every
  valid time of the action and every later valid time of a fact (A18). An
  entity or a time whose result is the same before and after the action never
  rejects (step 3), so an implementation may skip it if it can prove the
  result is the same.

With that proposal the six examples and all the old cases pass. A time without
a change of facts is still not read; a constraint for days like that is
written with `split`, like P4. There are no new findings. The reject example
in 06 §2.12 was also fixed (A30), and the reject example of P4 now names its
time.

## Findings

Situations that the standard has not defined, found while writing the program.
A1 to A14 come from step 2, A15 to A20 from step 3, A21 to A27 after the
proposals were run, A28 while writing decision 0044, and A29 to A32 from
step 4.

**Findings gate (2026-10-20).** Findings that are not yet decided are
classified according to [`decision 0046`](../decisions/0046-findings-gate.md). A finding may
change the form only if it comes from a case and is about the form. A18 and
A31 pass, and were decided in step 6, together with the fix of the example
for A30. A22 to A28 are postponed, because no case needs them. A29 is content,
for stage 6, and was decided in [`decision 0050`](../decisions/0050-code-lists.md) together
with the code lists. The classification is also written in the "Program"
column.

**Decided (2026-10-19).** The proposals A1 to A20 were first run provisionally
in the program, so that the result could be seen before they were decided: 128
tests and 16 examples still passed. After that, all of them were decided in
[`decision 0044`](../decisions/0044-additions-from-reference-calculator.md), except A18. The "Program" column states
the current state of the program:

- **decided**: the program follows the rule named.
- **not yet decided**: the program uses its own choice, without `NotDefined`.
- **not defined**: the program still raises `NotDefined`.

**Decision 0045 (2026-10-19).** After 0044, some of the findings turned out
not to be about the grammar of calculation, but about the way inside one
operation. An operation like that was moved out of the operation list into the
calculation library, that is, content
([`decision 0045`](../decisions/0045-core-operations-and-calculation-library.md)). The experiment is not included in this
repository (see above).

After that decision, the program uses the core, and the old ways of computing
are run from the calculation library, now
[`content/calc.md`](../content/calc.md). The tests for the old operations now
test the library helpers, with the same numbers
([`tests/test_library.py`](tests/test_library.py)). When it was moved, one
shortcoming was seen in the library draft: `convert_money` did not check the
unit of the rate, so 100 USD with a rate of 16,200 without a unit became
1,620,000 USD. Now the result is not computable if the unit is not the target
currency.

One consequence that was seen when the proposals were run: in
`cap_not_recorded`, the time *R* was once written `20 Mar 2026`, before the
claim was recorded at 09:00. That example used to stop as not defined; with
A19 its result is empty, and the example fails clearly. The *R* of that
example stays `20 Mar 2026 12:00`.

| # | Finding | Location | Proposal | Program |
|---|---|---|---|---|
| A1 | `average` over an empty collection has two kinds of reason in 06 §2.9: the example "division by zero" is the average of zero students, although `average` is also listed under "empty collection". The program uses **empty collection** | `operations.average` | Replace the example "division by zero", for instance with a price per unit for zero units | decided: 06 §2.9 |
| A2 | `up` and `down` for a negative number | `operations.round` | `up` goes to the larger number, `down` to the smaller | decided: CALC-22, then library content (0045) |
| A3 | `allocate` with a total that is not a multiple of `to`, for instance 10.5 IDR with `to: 1 IDR`: the sum of the shares cannot be exactly equal to the total | `operations.allocate` | Not computable, needs rounding | decided: CALC-23, then library content (0045) |
| A4 | How to round a `power` that is not a whole number to the precision `to` | `operations.power` | Rounded normally to a multiple of `to` | no longer applies: a fractional power is out of the core (0045) |
| A5 | `percentile` with `p` outside 0 < p ≤ 1 | `operations.percentile` | `p` must be a fixed value, so that it is checked before the rule is frozen | decided: CALC-50, then library content (0045) |
| A6 | `range(a, b)` with `b` before `a` | `operations.range` | Not computable, with a new reason kind **reversed time** | decided: 06 §2.5, reason kind reversed time |
| A7 | Shifting a date by less than one day, shifting an instant by months, and the difference of two instants in months | `operations.shift`, `operations.difference` | Month and year are only for dates. A date is only shifted by whole days, weeks, months, and years | decided: CALC-53 |
| A8 | Median with an even number of data points for values that are not numbers, for instance dates | `operations.median` | `median` is only for numbers | decided: 06 §2.5, then library content (0045) |
| A9 | Equal for collections that are not ordered | `operations.equals` | Equal if the members are equal, regardless of order, like the result of many values in 08 §2.4 | decided: 06 §2.5 |
| A10 | The tie-breaker for members that are not entities in an unordered collection, for instance the result of `group` or `contributions` | `operations.sort_by_key`, `compute.Evaluator.tie_key` | Not computable, with a new reason kind **undefined order** | decided: CALC-18, fixed in 0045 for exactly identical members |
| A11 | When several parts are not computable with different reasons, which reason is reported. An example compares reason kinds, so this affects the result of an example | `compute` | The first part by computation order; an unordered collection is computed by tie-breaker | decided: CALC-52. See A28 |
| A12 | `all_match` and `any_match` over a member that is `no` and a member that is not computable. The program computes all members, so the result is not computable | `operations.all_match` | Write in 06: a summary always computes all members, unlike `and` and `or` | decided: 06 §2.5 |
| A13 | The `rate` of `convert` is computed only if the currency differs. Paper test K2 depends on this, but 06 does not write it yet | `operations.convert` | Write it in 06, like the branch of an `if` that is not chosen | decided: CALC-51, then `convert_money` in the library (0045) |
| A14 | The identifier in an example is created new and at random (PROOF-7), although the tie-breaker uses the identifier as its last order. The result of an example could differ from one run to the next | `examples` | Inside an example, identifiers are ordered by local id | decided: PROOF-31 |
| A15 | When `let` is computed: first and in order, or only when used. The difference shows when the value of a `let` is not computable but not used, for instance a rate that is only needed for another currency, or when two parts fail with different reasons (A11) | `compute.Evaluator._let` | Only when used, like the branch of an `if` and the `rate` in `convert` (A13) | decided: CALC-51 |
| A16 | One action can be rejected several times by the same constraint. In `one_day_overlap`, the new rental `r2` fails, but `r1` fails too, because there is now another overlapping rental. 08 §2.4 does not say yet when a reject example passes if there is more than one rejection. Program: passes if all rejections are by the constraint named, and the entity and time named are among those rejections | `examples._compare_action` | Write this rule of the program in 08 §2.4 | decided: PROOF-32, with `one_day_overlap` as its example in 08 §4 |
| A17 | A replacement or an ending whose target is corrected later. Example: a rate of 100 from 1 Oct, replaced by 150 from 1 Nov, then the rate of 1 Oct is corrected to 120. Taken as written in 01 §2.5, that correction is never replaced, so in November there are two rates | `compute.FactStore.valid_facts` | A correction takes the place of its target: a replacement and an ending of that target also apply to its correction | decided: 01 §2.5 step 3 |
| A18 | 06 §2.12 step 2 reads the constraint again at the valid time after the action, "where the facts about the affected entity change", but the affected entity is not defined in a way that can be computed. The program uses a wider set: the entities the action touches and all entities of the concept of that constraint | `constraints.Checker._check_constraints` | A constraint that does not read the action is read for every entity of its concept, at the valid time of the action and every later valid time of a fact. Tested in step 6 | decided: 06 §2.12 step 2, CALC-38 (0047) |
| A19 | A computed property is asked for an entity that at *T* does not yet belong to its concept, for instance the total of a rental at *T* before the type fact of that rental is valid | `compute.Evaluator.compute` | The result is empty, like a property without facts | decided: CALC-54 |
| A20 | The result of a computed property with a quantity that is a zero without a unit, for instance `sum` over an empty collection for a total in money. The unit cannot be determined | `compute.Evaluator._check_single` | Not computable because of a unit mismatch; the author of the rule writes `0 IDR` if an empty result is possible, and the machine reports it before freezing | decided: CALC-55. The report before freezing is not run yet |
| A21 | A `power` that is not a whole number for a negative number, for instance (−2)^0.5, and for a number with a unit, for instance the root of 4 m² | `operations.power` | Negative number: not computable, with a new reason kind or a notation error. With a unit: allowed if the power of each unit becomes a whole number | no longer applies: a fractional power is out of the core (0045) |
| A22 | A unit with a power above 3 or below −3, for instance the result of cm × cm × cm × cm, has no way of being written in appendix A | `values.Unit.__str__` | Write ⁴, ⁵, and so on in appendix A §2.3 | not defined; postponed (0046) |
| A23 | `unit_of(n)` for a compound unit number, for instance `IDR/night`: the unit code list only holds single codes | `operations.unit_as_choice` | `unit_of` is only for a unit of one code; anything else is not computable, unit mismatch | not defined; postponed (0046) |
| A24 | `unit_of(n)` for a pure number | `operations.unit_of` | The result is empty | not defined; postponed (0046) |
| A25 | The tie-breaker for an entity that at *T* has no type fact, for instance a reference to an entity that has already ended, inside `fold` with `order_by` | `compute.Evaluator.tie_key` | Not computable, undefined order (A10) | not defined; postponed (0046) |
| A26 | `history(x.s, in: r)` if `x` is empty | `compute.Evaluator._op_history` | Empty collection, like `x.s` of an empty reference, which gives empty | not defined; postponed (0046) |
| A27 | `history` for a property with many values: the order of values valid at the same time | `compute.Evaluator._op_history` | By valid time, then recorded time, like the reading of facts in 01 §2.5 | not defined; postponed (0046) |
| A28 | CALC-52 reports the reason of the first part, but the result of `contributions` is unordered and not an entity, so it has no tie-breaker. If two contributions are not computable with different reasons, which reason is reported is not determined yet. The program computes contributions in the order of the installed modules | `compute.Evaluator._contributions` | Contributions are computed by the address of their module, then the address of the contribution | not yet decided; postponed (0046) |
| A29 | A property whose value is a unit code, for instance the source currency of a rate, cannot be written yet. `unit_of(n)` gives a choice from the unit code list, but that list has no address yet, so a property card and an example cannot name it (K2) | `examples._parse_value`, `operations.unit_as_choice` | The unit code list gets the address `uniti/unit/Unit` ([`content/code-lists.md`](../content/code-lists.md)). K2 is back as in the paper test: the source and target currency of a rate are choices | decided (0050) |
| A30 | A constraint that checks the coming days with `split` and `at` is rejected at the valid time of the action, not at the day that fails. The reject example in 06 §2.12 names "tent T4, 21 October", and paper test P4 also expects 21 October. But the entity that fails is the rental, and 21 October only exists inside the expression of the constraint. Another rental that uses that day fails too | `constraints.Checker._check_constraint_at` | The example in 06 §2.12 is fixed: the rental and the valid time of the action. The reader of a rejection can find the failing day by computing the constraint per day | decided: the reject example in 06 §2.12 is fixed (0047) |
| A31 | The value of a constraint before the action (06 §2.12 step 3), for a constraint that uses `before_action` or `this_action`. Without an action, both have no meaning. The program used to stop with a notation error (O3) | `constraints.Checker._check_constraint_at` | A constraint that reads the action is read as not existing before the action, so the action is rejected if it is not satisfied afterwards. A large purchase that already exists and is then changed without an approver is still rejected. Step 6: a constraint like this is read only for the entities the action touches, at the valid time of the action | decided: 06 §2.12 steps 1 and 3, CALC-57 (0047) |
| A32 | A reference that may be empty compared with `=`, for instance `u.parent_unit = this` for the top unit. Under 06 §2.9 the result is not computable, so the whole `all` fails (O1) | — | Stays: an empty value that is silently treated as different could hide data that has not been recorded, for instance a receipt without cash. The author uses `exists(…) and …`. A machine SHOULD report a comparison of a property that is not required without `exists` before the rule is frozen, like CALC-55 | decided: 06 §2.9. The report before freezing is not run yet |
