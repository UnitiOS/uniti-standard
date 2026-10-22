# Conformance

Status: not normative; the cases themselves are run as tests

> [Uniti Standard](../README.md) › Conformance · for implementers who want to
> know what to pass, and for anyone looking for a worked example

This page explains the files in this folder. The normative text wins when this
page and the text differ.

## 1. What these files are

The files here are the **conformance tests** of
[`form/08-proof.md`](../form/08-proof.md) §2.9: examples owned by the
standard, in the same form as the examples in a module (PROOF-25). The
modules inside them are example data and may use any owner
([`decisions/0056`](../decisions/0056-conformance-test-owners-and-known-gap.md)).
Each example has facts, a question, and an expected result. The reference
calculator (see [`reference/README.md`](../reference/README.md)) runs every
one of them and compares the result exactly (PROOF-5).

An implementation states the level it supports, 1, 2, or 3 (PROOF-26). The
three levels are described in
[`form/06-calculation-rules.md`](../form/06-calculation-rules.md) §2.5. An
implementation may say that it conforms to the Uniti Standard only if it
passes all conformance examples for its level and the levels below it, plus
all groups outside calculation. The statement names the version of the
standard and the level (PROOF-27; 08 §2.9). An implementation also refuses to
install a module that holds a rule above its level, naming which rule
(PROOF-28).

The seven groups used in the tables below are the groups in the table of
08 §2.9. Each example is placed in the group it mainly tests. Some examples
show a level of "—": no calculation rule ran in them, so they test facts,
values, or notation only. The levels were measured by running the reference
calculator: 3 if a rule ran recursively, 2 if a rule it reached uses `fold`
(directly or through a library helper such as `median`), 1 if only level 1
operations were used.

The examples in [`content/calc.md`](../content/calc.md) are in section 5. They
are run together with every file here, always.

## 2. How to run

Run the commands from the root of the repository (the folder that holds
`README.md`). The reference calculator needs Python 3.

The test runner `reference/tests/test_cases.py` reads the environment
variable `CASES`. It is a comma-separated list of file names, without spaces
and without folders. When `CASES` is set, only those files in this folder are
run. The content library (`content/`) is always run with them. File names must
be exact: a name that does not exist selects no file, and the run still
reports OK.

### 2.1 All tests

The whole test suite of the reference calculator, including all conformance
files (194 tests):

```
python -m unittest discover -s reference/tests -t reference
```

The same command works in a POSIX shell and in Windows PowerShell.

To run only the conformance runner (3 tests), add `-p test_cases.py`:

```
python -m unittest discover -s reference/tests -t reference -p test_cases.py
```

### 2.2 One file

POSIX shell:

```
CASES="15-change.md" python -m unittest discover -s reference/tests -t reference -p test_cases.py
```

Windows PowerShell:

```
$env:CASES = "15-change.md"; python -m unittest discover -s reference/tests -t reference -p test_cases.py; Remove-Item Env:CASES
```

For several files, join the names with commas: `"03-rental.md,04-payroll.md"`.

### 2.3 Per level

Each list holds the files whose highest level is that level or lower (see the
table in section 3). `13-outside-calculation.md` has no calculation, so it is
in every list.

Two things to keep in mind. The lists work by whole files: a file whose
highest level is 2 also holds examples of level 1, and it is left out of the
level 1 list. Also, some examples outside calculation (for example
constraints in `00-form-examples.md` and `10-organization.md`) sit in files
of a higher level. The groups outside calculation are part of what an
implementation must pass (08 §2.9), so for a conformance statement run all
files, as in section 2.1, or the list of the level above.

**Level 1**

POSIX shell:

```
CASES="03-rental.md,04-payroll.md,05-subscription.md,08-school.md,12-logistics.md,13-outside-calculation.md,14-backdated-constraints.md,16-relations.md,17-vocabulary.md,18-module-swap.md,19-reading-facts.md,21-closure.md" python -m unittest discover -s reference/tests -t reference -p test_cases.py
```

Windows PowerShell:

```
$env:CASES = "03-rental.md,04-payroll.md,05-subscription.md,08-school.md,12-logistics.md,13-outside-calculation.md,14-backdated-constraints.md,16-relations.md,17-vocabulary.md,18-module-swap.md,19-reading-facts.md,21-closure.md"; python -m unittest discover -s reference/tests -t reference -p test_cases.py; Remove-Item Env:CASES
```

**Level 2** (adds `00`, `01`, `07`, `11`, `15`, `20`)

POSIX shell:

```
CASES="00-form-examples.md,01-finance.md,03-rental.md,04-payroll.md,05-subscription.md,07-clinic.md,08-school.md,11-loyalty.md,12-logistics.md,13-outside-calculation.md,14-backdated-constraints.md,15-change.md,16-relations.md,17-vocabulary.md,18-module-swap.md,19-reading-facts.md,20-written-choices.md,21-closure.md" python -m unittest discover -s reference/tests -t reference -p test_cases.py
```

Windows PowerShell:

```
$env:CASES = "00-form-examples.md,01-finance.md,03-rental.md,04-payroll.md,05-subscription.md,07-clinic.md,08-school.md,11-loyalty.md,12-logistics.md,13-outside-calculation.md,14-backdated-constraints.md,15-change.md,16-relations.md,17-vocabulary.md,18-module-swap.md,19-reading-facts.md,20-written-choices.md,21-closure.md"; python -m unittest discover -s reference/tests -t reference -p test_cases.py; Remove-Item Env:CASES
```

**Level 3** (adds `02`, `06`, `09`, `10`): this is every file, so it is the
command in section 2.1 (or the conformance runner alone, without `CASES`):

```
python -m unittest discover -s reference/tests -t reference -p test_cases.py
```

## 3. Files

| File | What it tests | Groups of 08 §2.9 | Highest level | Examples |
|---|---|---|---|---|
| [`00-form-examples.md`](00-form-examples.md) | Examples told in the form documents (08, 06, appendix A), written in full | Calculation level 1; Calculation level 2; Constraints | 2 | 16 |
| [`01-finance.md`](01-finance.md) | Cash balance, revenue, journals, depreciation, cost sharing, revenue recognition (K1 to K6) | Calculation level 1; Calculation level 2; Constraints | 2 | 21 |
| [`02-inventory.md`](02-inventory.md) | Stock from several modules, first-in-first-out cost, stock checks (P1 to P4) | Calculation level 1; Calculation level 3; Constraints | 3 | 14 |
| [`03-rental.md`](03-rental.md) | Rental total, rate at a time, overlap check, late fees (S1 to S4) | Calculation level 1; Constraints | 1 | 7 |
| [`04-payroll.md`](04-payroll.md) | Progressive tax, overtime, monthly salary (G1 to G3) | Calculation level 1 | 1 | 3 |
| [`05-subscription.md`](05-subscription.md) | Plan change in mid-period, usage price (L1, L2) | Calculation level 1 | 1 | 3 |
| [`06-loans.md`](06-loans.md) | Compound interest, monthly interest, payments that settle loans (J1 to J3) | Calculation level 1; Calculation level 3 | 3 | 6 |
| [`07-clinic.md`](07-clinic.md) | Insurance cap, median and average of visits (C1, C2) | Calculation level 1; Calculation level 2 | 2 | 7 |
| [`08-school.md`](08-school.md) | Weighted grade, rank, attendance (E1 to E3) | Calculation level 1 | 1 | 7 |
| [`09-manufacturing.md`](09-manufacturing.md) | Multi-level parts lists and costs, including a cycle (M1, M2) | Calculation level 3 | 3 | 7 |
| [`10-organization.md`](10-organization.md) | Cost by chart, approval limits, state changes (O1 to O3) | Calculation level 3; Constraints | 3 | 12 |
| [`11-loyalty.md`](11-loyalty.md) | Points with expiry, used oldest first (R1) | Calculation level 2 | 2 | 4 |
| [`12-logistics.md`](12-logistics.md) | Shipping cost with volume weight and units (X1) | Calculation level 1 | 1 | 1 |
| [`13-outside-calculation.md`](13-outside-calculation.md) | Decisions and estimates recorded as facts, not calculated (B1 to B4) | Facts | — | 4 |
| [`14-backdated-constraints.md`](14-backdated-constraints.md) | Constraints checked when a correction is made far in the past | Constraints | 1 | 6 |
| [`15-change.md`](15-change.md) | New versions, exact-version binding, behavior change and replaced examples (U1 to U3) | Change and proof | 2 | 10 |
| [`16-relations.md`](16-relations.md) | Two modules' choices declared the same, read in one report (U4) | Calculation level 1 | 1 | 1 |
| [`17-vocabulary.md`](17-vocabulary.md) | One shared vocabulary used by a rental shop and a school | Values and concepts; Calculation level 1 | 1 | 3 |
| [`18-module-swap.md`](18-module-swap.md) | Moving to another module without breaking old records | Values and concepts; Change and proof | 1 | 4 |
| [`19-reading-facts.md`](19-reading-facts.md) | Reading at two times after corrections, retractions, and late reports | Facts; Values and concepts; Constraints | 1 | 15 |
| [`20-written-choices.md`](20-written-choices.md) | Calendar months, split, two types of one entity, empty collections, empty constraint checks | Calculation level 1; Calculation level 2; Constraints | 2 | 12 |
| [`21-closure.md`](21-closure.md) | Situations closed before the lock: one action at a time, `unit_of`, `history`, unit powers, an old gap in a required property (decision 0057) | Values and concepts; Calculation level 1; Constraints | 1 | 12 |

Level "—" means that no calculation rule ran in any example of the file.
There are 175 examples in these files, and 7 more in `content/calc.md`
(section 5).

## 4. Every example

One table per file. The address is the example address
([`form/02-addresses.md`](../form/02-addresses.md)). The level is the one
measured by the reference calculator; "—" means that no calculation rule ran,
so the example tests facts, values, or notation only.

Choice of group: a compute example is in a Calculation group of its level,
except in `15-change.md` and `18-module-swap.md` (change) and
`19-reading-facts.md` (reading facts). Accept and reject examples of a
constraint are in Constraints; those that test the form of facts or values are
in Facts or Values and concepts.

### 00-form-examples.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `alex/rental/three_night_rental` | compute | Calculation level 1 | 1 |
| `alex/rental/rate_rise_after_rental` | compute | Calculation level 1 | 1 |
| `alex/rental/one_day_overlap` | reject | Constraints | 1 |
| `alex/rental/adjoining_no_overlap` | accept | Constraints | 1 |
| `example/rate/rate_on_start_day` | compute | Calculation level 1 | 1 |
| `example/rate/rate_every_day` | compute | Calculation level 1 | 1 |
| `example/clinic/cap_partly_left` | compute | Calculation level 2 | 2 |
| `example/clinic/first_claim_in_full` | compute | Calculation level 2 | 2 |
| `example/clinic/cap_exhausted` | compute | Calculation level 2 | 2 |
| `example/clinic/cap_not_recorded` | compute | Calculation level 2 | 2 |
| `example/school/tied_scores` | compute | Calculation level 1 | 1 |
| `example/school/highest_score` | compute | Calculation level 1 | 1 |
| `example/school/after_tied_scores` | compute | Calculation level 1 | 1 |
| `example/organization/self_approved` | reject | Constraints | 1 |
| `example/organization/approved_by_other_manager` | accept | Constraints | 1 |
| `example/organization/small_purchase` | accept | Constraints | 1 |

### 01-finance.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/k1/balance_per_records_7_oct` | compute | Calculation level 1 | 1 |
| `paper/k1/balance_per_records_8_oct` | compute | Calculation level 1 | 1 |
| `paper/k1/balance_10_oct` | compute | Calculation level 1 | 1 |
| `paper/k2/october_revenue` | compute | Calculation level 1 | 1 |
| `paper/k2/september_revenue` | compute | Calculation level 1 | 1 |
| `paper/k3/balanced_journal` | accept | Constraints | 1 |
| `paper/k3/unbalanced_journal` | reject | Constraints | 1 |
| `paper/k4/accumulated_march` | compute | Calculation level 2 | 2 |
| `paper/k4/book_value_june` | compute | Calculation level 2 | 2 |
| `paper/k4/first_month_depreciation` | compute | Calculation level 2 | 2 |
| `paper/k4/last_month_depreciation` | compute | Calculation level 2 | 2 |
| `paper/k5/department_a_share` | compute | Calculation level 2 | 2 |
| `paper/k5/department_b_share` | compute | Calculation level 2 | 2 |
| `paper/k5/department_c_share` | compute | Calculation level 2 | 2 |
| `paper/k5/no_remainder_lost` | compute | Calculation level 2 | 2 |
| `paper/k5/tie_remainder_to_earlier` | compute | Calculation level 2 | 2 |
| `paper/k5/tie_other_gets_no_remainder` | compute | Calculation level 2 | 2 |
| `paper/k6/recognized_june` | compute | Calculation level 2 | 2 |
| `paper/k6/unrecognized_june` | compute | Calculation level 2 | 2 |
| `paper/k6/ordinary_month_revenue` | compute | Calculation level 2 | 2 |
| `paper/k6/last_month_revenue` | compute | Calculation level 2 | 2 |

### 02-inventory.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/p1-shop/available_while_rented` | compute | Calculation level 1 | 1 |
| `paper/p1-shop/available_after_return` | compute | Calculation level 1 | 1 |
| `paper/p1-shop/available_on_start_day` | compute | Calculation level 1 | 1 |
| `paper/p1-shop/available_on_end_day` | compute | Calculation level 1 | 1 |
| `paper/p1-shop-without-rental/without_rental_module` | compute | Calculation level 1 | 1 |
| `paper/p2/cogs_first_issue` | compute | Calculation level 3 | 3 |
| `paper/p2/cogs_after_two_issues` | compute | Calculation level 3 | 3 |
| `paper/p2/remaining_inventory_value` | compute | Calculation level 3 | 3 |
| `paper/p3/cogs_after_issue_15` | compute | Calculation level 3 | 3 |
| `paper/p3/final_cogs` | compute | Calculation level 3 | 3 |
| `paper/p3/final_value` | compute | Calculation level 3 | 3 |
| `paper/p3/final_stock` | compute | Calculation level 3 | 3 |
| `paper/p4/stock_sufficient` | accept | Constraints | 1 |
| `paper/p4/stock_short_one_day` | reject | Constraints | 1 |

### 03-rental.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/s1/three_nights` | compute | Calculation level 1 | 1 |
| `paper/s2/rate_at_start_day` | compute | Calculation level 1 | 1 |
| `paper/s2/rate_every_day` | compute | Calculation level 1 | 1 |
| `paper/s3/overlapping_12_oct` | reject | Constraints | 1 |
| `paper/s3/adjoining_13_oct` | accept | Constraints | 1 |
| `paper/s4/six_days_late` | compute | Calculation level 1 | 1 |
| `paper/s4/twelve_days_late` | compute | Calculation level 1 | 1 |

### 04-payroll.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/g1/tax_three_brackets` | compute | Calculation level 1 | 1 |
| `paper/g2/overtime_one_week` | compute | Calculation level 1 | 1 |
| `paper/g3/october_salary` | compute | Calculation level 1 | 1 |

### 05-subscription.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/l1/november_charge` | compute | Calculation level 1 | 1 |
| `paper/l1/november_shortfall` | compute | Calculation level 1 | 1 |
| `paper/l2/usage_25_thousand` | compute | Calculation level 1 | 1 |

### 06-loans.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/j1/compound_one_year` | compute | Calculation level 1 | 1 |
| `paper/j2/interest_october` | compute | Calculation level 1 | 1 |
| `paper/j3/c1_paid_off` | compute | Calculation level 3 | 3 |
| `paper/j3/c2_remaining_after_first_payment` | compute | Calculation level 3 | 3 |
| `paper/j3/c2_paid_off_after_second_payment` | compute | Calculation level 3 | 3 |
| `paper/j3/c3_remaining_after_second_payment` | compute | Calculation level 3 | 3 |

### 07-clinic.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/c1/claim_february` | compute | Calculation level 2 | 2 |
| `paper/c1/claim_may` | compute | Calculation level 2 | 2 |
| `paper/c1/claim_august` | compute | Calculation level 2 | 2 |
| `paper/c1/claim_october` | compute | Calculation level 2 | 2 |
| `paper/c2/median_five_visits` | compute | Calculation level 2 | 2 |
| `paper/c2/average_five_visits` | compute | Calculation level 1 | 1 |
| `paper/c2/median_six_visits` | compute | Calculation level 2 | 2 |

### 08-school.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/e1/final_grade_85` | compute | Calculation level 1 | 1 |
| `paper/e2/rank_sam` | compute | Calculation level 1 | 1 |
| `paper/e2/rank_maria` | compute | Calculation level 1 | 1 |
| `paper/e2/rank_nina` | compute | Calculation level 1 | 1 |
| `paper/e2/rank_leo` | compute | Calculation level 1 | 1 |
| `paper/e3/attended_90_of_96` | compute | Calculation level 1 | 1 |
| `paper/e3/attended_77_of_80` | compute | Calculation level 1 | 1 |

### 09-manufacturing.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/m1/pipes_for_ten_bicycles` | compute | Calculation level 3 | 3 |
| `paper/m1/tires_for_ten_bicycles` | compute | Calculation level 3 | 3 |
| `paper/m1/spokes_for_ten_bicycles` | compute | Calculation level 3 | 3 |
| `paper/m1/cyclic_structure` | compute | Calculation level 3 | 3 |
| `paper/m2/wheel_cost` | compute | Calculation level 3 | 3 |
| `paper/m2/frame_cost` | compute | Calculation level 3 | 3 |
| `paper/m2/bicycle_cost` | compute | Calculation level 3 | 3 |

### 10-organization.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/o1/sales_cost` | compute | Calculation level 3 | 3 |
| `paper/o1/company_cost` | compute | Calculation level 3 | 3 |
| `paper/o2/small_without_approver` | accept | Constraints | 1 |
| `paper/o2/large_without_approver` | reject | Constraints | 1 |
| `paper/o2/large_approved_by_staff` | reject | Constraints | 1 |
| `paper/o2/large_approved_by_manager` | accept | Constraints | 1 |
| `paper/o2/large_approved_by_self` | reject | Constraints | 1 |
| `paper/o2/exactly_at_limit_without_approver` | accept | Constraints | 1 |
| `paper/o2/over_limit_without_approver` | reject | Constraints | 1 |
| `paper/o3/draft_submitted` | accept | Constraints | 1 |
| `paper/o3/draft_straight_to_posted` | reject | Constraints | 1 |
| `paper/o3/posted_back_to_draft` | reject | Constraints | 1 |

### 11-loyalty.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/r1/balance_february_2027` | compute | Calculation level 2 | 2 |
| `paper/r1/balance_april_2027` | compute | Calculation level 2 | 2 |
| `paper/r1/balance_day_before_expiry` | compute | Calculation level 2 | 2 |
| `paper/r1/balance_on_expiry_day` | compute | Calculation level 2 | 2 |

### 12-logistics.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/x1/volumetric_weight` | compute | Calculation level 1 | 1 |

### 13-outside-calculation.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `paper/b/b1_sales_forecast` | accept | Facts | — |
| `paper/b/b2_invoice_number` | accept | Facts | — |
| `paper/b/b3_customer_chooses_invoice` | accept | Facts | — |
| `paper/b/b4_shift_schedule` | accept | Facts | — |

### 14-backdated-constraints.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `reference/backdated-stock/safe_backdated_correction` | accept | Constraints | 1 |
| `reference/backdated-stock/violating_backdated_correction` | reject | Constraints | 1 |
| `reference/backdated-stock/correction_far_in_the_past` | reject | Constraints | 1 |
| `reference/backdated-stock/old_violation_does_not_block` | accept | Constraints | 1 |
| `reference/backdated-permission/small_after_old_large` | accept | Constraints | 1 |
| `reference/backdated-permission/old_large_changed` | reject | Constraints | 1 |

### 15-change.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `alex/rental/three_night_rental`, module `alex/rental@v1` | compute | Change and proof | 1 |
| `alex/rental/three_night_rental`, module `alex/rental@v2` | compute | Change and proof | 1 |
| `happy-camp/shop/weekend_rental`, module `happy-camp/shop@v1` | compute | Change and proof | 1 |
| `happy-camp/shop/weekend_rental`, module `happy-camp/shop@v2` | compute | Change and proof | 1 |
| `happy-camp/shop/promised_return_old_rental`, module `happy-camp/shop@v2` | compute | Change and proof | — |
| `uniti/depreciation/march_accumulated`, module `uniti/depreciation@v3` | compute | Change and proof | 2 |
| `uniti/depreciation/february_depreciation`, module `uniti/depreciation@v3` | compute | Change and proof | 2 |
| `uniti/depreciation/march_accumulated`, module `uniti/depreciation@v4` | compute | Change and proof | — (replaced; not run as a condition, PROOF-21) |
| `uniti/depreciation/february_depreciation`, module `uniti/depreciation@v4` | compute | Change and proof | 2 |
| `uniti/depreciation/march_accumulated_remainder_first`, module `uniti/depreciation@v4` | compute | Change and proof | 2 |

### 16-relations.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `healthy-clinic/report/combined_national_insurance_october` | compute | Calculation level 1 | 1 |

### 17-vocabulary.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `happy-camp/rental/rental_paid` | compute | Calculation level 1 | 1 |
| `happy-camp/rental/payment_without_amount` | reject | Values and concepts | — |
| `bright-future/tuition/tuition_october` | compute | Calculation level 1 | 1 |

### 18-module-swap.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `happy-camp/shop/tents_out_two_modules` | compute | Change and proof | 1 |
| `happy-camp/shop/return_through_new_cashier` | accept | Values and concepts | — |
| `happy-camp/shop/tents_out_after_return` | compute | Change and proof | 1 |
| `happy-camp/shop/return_through_other_cashier` | reject | Values and concepts | — |

### 19-reading-facts.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `reference/rate/typo_in_new_rate` | compute | Facts | 1 |
| `reference/rate/rate_change_moved_earlier` | compute | Facts | 1 |
| `reference/rate/typo_does_not_touch_old_rate` | compute | Facts | 1 |
| `reference/rate/june_change_learned_late` | compute | Facts | 1 |
| `reference/rate/june_change_does_not_overwrite_november` | compute | Facts | 1 |
| `reference/rate/june_change_before_it_was_known` | compute | Facts | 1 |
| `reference/rate/correction_of_old_rate` | compute | Facts | 1 |
| `reference/rate/subscription_ended` | compute | Facts | 1 |
| `reference/phone/typo_in_new_number` | compute | Facts | 1 |
| `reference/corrected-stock/receipt_date_moved` | reject | Constraints | 1 |
| `reference/corrected-stock/receipt_retracted` | reject | Constraints | 1 |
| `reference/corrected-stock/wrong_record_retracted_entirely` | accept | Constraints | 1 |
| `reference/corrected-stock/replacement_does_not_read_the_past` | accept | Constraints | 1 |
| `reference/corrected-stock/reference_to_item_not_yet_there` | reject | Values and concepts | 1 |
| `reference/corrected-stock/reference_after_item_exists` | accept | Values and concepts | 1 |

### 20-written-choices.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `reference/month/end_of_month_to_end_of_month` | compute | Calculation level 1 | 1 |
| `reference/month/mid_month` | compute | Calculation level 1 | 1 |
| `reference/month/not_yet_a_month` | compute | Calculation level 1 | 1 |
| `reference/month/two_months_from_end_of_month` | compute | Calculation level 1 | 1 |
| `reference/month/backwards_like_a_mirror` | compute | Calculation level 1 | 1 |
| `reference/month/split_from_start_of_range` | compute | Calculation level 2 | 2 |
| `reference/two-types/customer_who_was_a_supplier_first` | compute | Calculation level 2 | 2 |
| `reference/many/no_phone` | compute | Calculation level 1 | 1 |
| `reference/many/exists_over_collection_without_members` | compute | Calculation level 1 | 1 |
| `reference/many/count_to_check` | compute | Calculation level 1 | 1 |
| `reference/empty-constraint/purchase_without_check_mark` | reject | Constraints | 1 |
| `reference/empty-constraint/purchase_with_check_mark` | accept | Constraints | 1 |

### 21-closure.md

| Example | Kind | Group | Level |
|---|---|---|---|
| `reference/closure-rental/last_tent_same_moment` | reject | Constraints | 1 |
| `reference/closure-history/item_not_filled_in` | compute | Calculation level 1 | 1 |
| `reference/closure-history/total_without_item_is_not_zero` | compute | Calculation level 1 | 1 |
| `reference/closure-history/item_filled_in` | compute | Calculation level 1 | 1 |
| `reference/closure-unit/number_without_unit` | compute | Calculation level 1 | 1 |
| `reference/closure-unit/rate_has_two_codes` | compute | Calculation level 1 | 1 |
| `reference/closure-power/four_lengths` | compute | Calculation level 1 | 1 |
| `reference/closure-power/three_lengths` | compute | Calculation level 1 | 1 |
| `reference/closure-many/three_records` | compute | Calculation level 1 | 1 |
| `reference/required-later/correct_name_of_old_record` | accept | Values and concepts | — |
| `reference/required-later/new_customer_without_phone` | reject | Values and concepts | — |
| `reference/required-later/retract_phone_of_customer` | reject | Values and concepts | — |

## 5. Examples in the content library

The file [`content/calc.md`](../content/calc.md) holds examples for the
calculation library (`uniti/calc`). They are not in this folder, but they are
run every time, even when `CASES` is set.

| Example | Kind | Group | Level |
|---|---|---|---|
| `example/user/median_with_equal_values` | compute | Calculation level 2 | 2 |
| `example/user/percentile_90` | compute | Calculation level 2 | 2 |
| `example/user/average_five_point_five` | compute | Calculation level 1 | 1 |
| `example/user/median_empty` | compute | Calculation level 2 | 2 |
| `example/user/rupiah_without_rate` | compute | Calculation level 1 | 1 |
| `example/user/dollar_with_rate` | compute | Calculation level 1 | 1 |
| `example/user/building_rent_split_by_area` | compute | Calculation level 2 | 2 |
