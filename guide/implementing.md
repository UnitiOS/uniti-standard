# Implementing the standard

Status: guide; not normative

> [Uniti Standard](../README.md) › Guide · For a developer who builds the first
> system that conforms to the standard

This guide says what to build, in which order, and how to know it is right. It
points to the rules by ID and never replaces them. When this guide and the
normative text differ, the normative text wins. Rule IDs link to the index in
[`rules.md`](../rules.md); terms are explained in the
[glossary](../01-glossary.md).

## 1. What an implementation does

Software conforms to the standard if it accepts content that conforms, rejects
content that does not, and upholds all the rules of part A for the facts it
stores ([`00-principles.md`](../00-principles.md) §7). Four jobs follow:

1. **Store facts** that follow [`form/01-facts.md`](../form/01-facts.md), and
   never change or delete one (FACT-3).
2. **Read facts** at two times, valid time *T* and as of *R* (FACT-17).
3. **Check content and actions**: reject content that breaks the form, and
   reject an action as a whole when a rule says so (CONCEPT-19, CALC-38).
4. **Calculate** the rules in installed modules at a stated level, and prove it
   with the conformance examples ([`form/08-proof.md`](../form/08-proof.md)
   §2.9).

An implementation states the level it supports: 1, 2, or 3 (PROOF-26). It may
say "conforms to the Uniti Standard" only when it passes the conformance
examples for that level (PROOF-27).

## 2. The data model

The standard fixes what a fact means. It does not fix how you store it. It does
not choose a database, and it has no exchange format yet: the reference
notation is for writing content and examples
([`appendix/A-notation.md`](../appendix/A-notation.md) §2.1), and a JSON or RDF
format for exchange is an open question there (§8, item 3), postponed by
[`decisions/0055`](../decisions/0055-locked-in-english.md). Store facts in any
shape that keeps the parts below.

### 2.1 The fact record

Every fact has these parts ([`01-facts.md`](../form/01-facts.md) §2.1, FACT-1,
FACT-2, FACT-9):

| Part | Notes |
|---|---|
| `id` | Identifier of the fact |
| `subject` | Identifier of an entity |
| `property` | An address, stored without the root (ADDRESS-13) |
| `value` | One value when the kind is statement, replacement, or correction; none otherwise (FACT-2) |
| `valid_time` | A date or an instant (VALUE-9) |
| `kind` | One of six (FACT-8) |
| `target` | Exactly one earlier fact with the same subject and property, when the kind is not statement (FACT-9) |
| `version_used` | The module version used when the fact was stated (FACT-1) |
| `action` | The action that recorded it (FACT-18) |

```
Fact:   id, subject, property, value?, valid_time, kind, target?,
        version_used, action
Action: id, actor, approver?, recorded_time, source,
        action_name?, reason?           # FACT-19..22
```

There is no end time on a fact: a fact ends when another fact replaces or ends
it ([`decisions/0005`](../decisions/0005-facts-without-end-time.md)).

### 2.2 Entities and identifiers

An entity identifier is unique in the world, permanent, meaningless, and never
reused (FACT-5). Codes that mean something to people, such as a customer
number, are properties (FACT-6). Every entity has a `type` fact (FACT-7), and
the value of `type` is the address of a concept
([`03-values.md`](../form/03-values.md) §2.1). A role such as customer is a
reference from another entity, not a type (CONCEPT-13). The standard says
"random" in [`01-facts.md`](../form/01-facts.md) §2.2 and leaves the way you
generate identifiers to you.

### 2.3 The six kinds and their targets

| Kind | Value | Target | Extra rules |
|---|---|---|---|
| statement | yes | no | |
| replacement | yes | yes | valid time later than the target (FACT-10) |
| ending | no | yes | valid time later than the target (FACT-10) |
| correction | yes | yes | target has a value (FACT-11); same subject and property (FACT-12) |
| retraction | no | yes | not on another retraction (FACT-13) |
| redaction | no | yes | provisional; see below |

A property with one value takes a replacement or correction, never a second
statement for the same entity and valid time (FACT-14). A type fact is never
replaced or ended (CONCEPT-14).

### 2.4 Actions and provenance

One action records many facts, all together or not at all (FACT-18). It needs
an actor, a recorded time, and a source (FACT-19), an approver when the actor
is not responsible alone (FACT-20), and a reason when it corrects, retracts, or
redacts (FACT-21). The recorded time comes from the recorder at the moment of
recording, never from the actor (FACT-15). The valid time may be past or future
(FACT-16).

### 2.5 Redaction (provisional)

A redaction targets a fact whose property is marked as personal data
(FACT-23), and cannot itself be retracted or corrected (FACT-24). Afterwards
nobody can read the value, but the other parts of the fact stay readable
(FACT-25). How you make a value unreadable is left to you
([`01-facts.md`](../form/01-facts.md) §2.6). The section is provisional and may
change.

### 2.6 What is not a fact

A computed value is never recorded as a fact (FACT-4, CALC-5). A rejection
record is not a fact either (CALC-43).

## 3. Reading facts at (T, R)

This is the core of the store ([`01-facts.md`](../form/01-facts.md) §2.5; why:
[`decisions/0053`](../decisions/0053-reading-corrected-facts.md)). The rule
for a property with many values below is only an outline of the text; the
examples in
[`conformance/19-reading-facts.md`](../conformance/19-reading-facts.md) are the
contract.

```
def read(S, P, T, R):
    F = [f for f in facts(S, P) if f.action.recorded_time <= R]      # step 1
    F = [f for f in F if not targeted_by_correction_or_retraction(f, F)]  # step 2
    # retractions and redactions are not read as timeline entries:
    # their valid time is not read (01 §2.5)
    live = [f for f in F if f.kind in (statement, replacement,
                                        ending, correction)
            and f.valid_time <= T]                                    # step 3
    if P.number_of_values == "one":                                   # card, CONCEPT-3
        if not live: return EMPTY
        # latest valid time wins; same valid time: recorded last wins
        w = max(live, key=lambda f: (f.valid_time, f.action.recorded_time))
        if w.kind == ending: return EMPTY
        return value_or_redacted(w, R)                                # step 4
    else:
        # per value: a fact with a value applies unless another fact in
        # `live` replaced or ended it; a correction takes its target's place
        # completely, and a correction of a replacement also replaces the
        # target of that replacement (01 §2.5 step 3, third bullet)
        return [value_or_redacted(f, R) for f in applying(live)]

def value_or_redacted(f, R):
    # a fact redacted by a redaction recorded at or before R still counts,
    # but its value reads "redacted"   (FACT-25, 01 §2.5 step 4)
    return REDACTED if redacted_as_of(f, R) else f.value
```

Points to get right:

- **Date and instant.** To compare a date with an instant, read the date as the
  start of that day in the organization's default time zone (VALUE-10).
- **Same valid time.** The fact recorded last wins. If it is an ending, there is
  no value at *T* (01 §2.5 step 3).
- **Reading is deterministic.** Two readers asking the same question get the
  same answer, so store nothing that changes the answer.
- **Time touched by an action** (used in section 7) comes from the same
  reading: see [`04-concepts.md`](../form/04-concepts.md) §2.7.

Conformance examples: `typo_in_new_rate`, `rate_change_moved_earlier`,
`june_change_learned_late`, `correction_of_old_rate`, `subscription_ended`, and
`typo_in_new_number` in
[`conformance/19-reading-facts.md`](../conformance/19-reading-facts.md); the
rental cases in [`conformance/00-form-examples.md`](../conformance/00-form-examples.md).

## 4. Values

The seven value types are closed (VALUE-1, VALUE-3); every value matches its
property's type (VALUE-2). See [`03-values.md`](../form/03-values.md).

| Topic | What to build | Rules |
|---|---|---|
| Numbers | Store and compute exact numbers, with no binary floating point. Round only where a calculation rule says so | VALUE-4, CALC-20 |
| Units | If the property sets a quantity, every value carries a unit of it. If not, no unit. Never convert silently | VALUE-5, VALUE-7 |
| Direction | Every number property states one of increase, decrease, no direction, position. No direction cannot be negative | VALUE-17, VALUE-18 |
| Dates | A date is a calendar day. An instant always has a time zone, and one without is refused | VALUE-8 |
| Valid time | A date or an instant, following the property if it sets one | VALUE-9 |
| Default zone | One default time zone per organization | VALUE-10 |
| Text | A language code, if any, follows BCP 47 | VALUE-11 |
| Choices | A list is open, closed, or a code list. A value is the address of a choice in the property's list, from an installed module | VALUE-12 to VALUE-15, VALUE-19 |
| References | The identifier of an entity that belongs to the concept referred to (or a child) at the valid time of the fact | VALUE-16 |

Units and currencies come from the code list `uniti/unit/Unit`, defined in
[`content/code-lists.md`](../content/code-lists.md) (VALUE-6). A code from an
outside standard is written exactly, including case (ADDRESS-2, and
[`02-addresses.md`](../form/02-addresses.md) §2.4). Your code needs the unit
table in that file to know which units share a quantity and which have a fixed
factor for `convert`.

Two numeric limits to remember. Inside a rule, numbers are exact fractions
(CALC-20). The value of a computed property that is a number must be a
terminating decimal; otherwise the result is not computable because it needs rounding
(CALC-21). Where and how to round is content (VALUE-4, and the library in
[`content/calc.md`](../content/calc.md)).

## 5. Modules, addresses, versions

Read [`02-addresses.md`](../form/02-addresses.md), [`05-relations.md`](../form/05-relations.md)
and [`07-change.md`](../form/07-change.md). The standard requires content to
conform (00 §7), so an installer is where much of the checking lives. When a
module is installed, check at least the following.

| Check | Rules |
|---|---|
| Addresses use the allowed letters; names are unique inside the module; no version number inside an address; owners `standard`, `uniti`, `example` are reserved | ADDRESS-2, ADDRESS-3, ADDRESS-4, ADDRESS-7 |
| The module is a frozen version, not a draft; versions run 1, 2, 3 without gaps | CHANGE-4, CHANGE-2 |
| The version is not withdrawn | CHANGE-11 |
| Every module it uses is named with one exact version, no range | CHANGE-14, ADDRESS-11 |
| Cards have their required parts; labels carry a language code; one main label per language | CONCEPT-1, CONCEPT-3, CONCEPT-4, CONCEPT-16, CONCEPT-17, CONCEPT-20, VALUE-19 |
| Number properties state a direction; others do not | CONCEPT-5 |
| A concept has at most one parent and no loop of parents | CONCEPT-9, CONCEPT-10 |
| Only the owner of a concept declares a property required for it | CONCEPT-8 |
| Every relation is in the closed list, stated by the allowed party, with matching sides and the exact version of its target | RELATION-1, RELATION-3, RELATION-6, RELATION-7, RELATION-12 |
| Every rule has an address and uses only core operations and rules from its own module or modules it names | CALC-3, CALC-9, CALC-17 |
| Contributions go only to open computations and match type, quantity, and direction | CALC-32, CALC-33, CALC-34 |
| No rule needs a level above the one you support: refuse the module and name the rule | PROOF-28, CALC-11 |

Things to keep in mind:

- A relation or "applies to" statement only holds for organizations that
  install its module (RELATION-5, CONCEPT-7, CALC-35).
- Facts keep working across versions because addresses never change
  (ADDRESS-4, CHANGE-6). Store `version_used` on each fact.
- A deprecated or withdrawn marker is a statement by the owner, not an edit of
  the version (CHANGE-8). Facts under them stay readable (CHANGE-13).
- The kind of change between two versions is computed, not declared
  (CHANGE-5). Making a property required is reported separately (CONCEPT-22).
- The root `https://uniti.example` is stored once and put in front of an
  address only when it is written in full (ADDRESS-14, ADDRESS-15).

The text does not say whether installing a module also installs the modules it
uses. That choice is yours.

## 6. Calculation, by level

The core operations are listed in [`06-calculation-rules.md`](../form/06-calculation-rules.md)
§2.5. Build in three levels. The level of a rule is computed from the
operations it uses, including those in rules it reads (CALC-11). An
implementation may calculate in any way that gives exactly the same result,
including the kind of reason (CALC-19). The files in `conformance/` are listed
in the [conformance README](../conformance/README.md).

### 6.1 Level 1: basic

Operations: get (`this`, `x.s`, `T`, `unit_of`), collect (`all`, `single`,
`each`, `each_merged`, `group`), summarize, calculate (including `power` and
`floor_multiple`), time (`range`, `difference`, `span`, `overlap`, `split`,
`in`, `at`, `history`), choose, `convert`, records and collections, and the
constraint-only operations.

Hard points:

- **Three results.** Every expression gives a value, empty, or not computable
  (06 §2.9). Not computable carries a reason kind, a description, and a
  location (CALC-28). It never becomes 0 or empty (CALC-29), and it spreads
  (CALC-30).
- **Laziness.** `if`, `and`, `or`, and `let` calculate only what they need;
  `all_match` and `any_match` calculate every member. A part never calculated
  cannot spoil the result (CALC-51).
- **Which reason is reported.** The first part in calculation order. In a
  collection with no order, whose members are not entities, the topmost kind
  in the table of 06 §2.9 (CALC-52).
- **Empty versus a collection with no members.** A property with many values
  gives a collection, not empty; check it with `count` (CALC-8, 06 §2.9). A
  computed property asked for an entity that is not of its concept at *T* is
  empty (CALC-54).
- **Time.** Ranges are half open (CALC-26). Months are calendar months, shifted
  directly from the start date (CALC-53, 06 §2.7). `split` pieces are counted
  from the start of the range.
- **Units.** Add, subtract, and compare need the same unit; different units do
  not cancel even if the quantity is the same (CALC-24). A unitless zero as the
  final result of a quantity property is not computable (CALC-55).
- **Rounding.** Only `floor_multiple` is in the core (CALC-56); other rounding
  and `allocate` are library content.

Conformance files: most files hold level 1 examples. The files whose highest
level is 1 are `03-rental`, `04-payroll`, `05-subscription`, `08-school`,
`12-logistics`, `14-backdated-constraints`, `16-relations`, `17-vocabulary`,
`18-module-swap`, and `19-reading-facts`. The level of every example, measured
by the reference calculator, is in the
[conformance README](../conformance/README.md#4-every-example). Contributions to open
computed properties (CALC-32 to CALC-35, CALC-49) are in
[`02-inventory`](../conformance/02-inventory.md) P1.

### 6.2 Level 2: order and fold

One new operation, `fold`. The hard point is order.

- A collection from `all` or `group` has no order, so `fold` names `order_by`
  (CALC-18).
- Members that tie are ordered by the tie-breaker: valid time of the type
  fact, then its recorded time, then the identifier compared as text by Unicode
  number (06 §2.6). An entity with several valid type facts uses the earliest.
- An entity may be an `order_by` key (CALC-18).
- Tied members that are not entities and are not exactly the same make the
  result not computable because of undefined order (CALC-18).

Conformance files: [`01-finance`](../conformance/01-finance.md) (K4 to K6),
[`07-clinic`](../conformance/07-clinic.md) (C1, and the medians of C2),
[`11-loyalty`](../conformance/11-loyalty.md), the depreciation module in
[`15-change`](../conformance/15-change.md), the clinic cap in
[`00-form-examples`](../conformance/00-form-examples.md), `split` and the
entity with two types in
[`20-written-choices`](../conformance/20-written-choices.md), and the
`median`, `percentile`, and `allocate` examples in
[`content/calc.md`](../content/calc.md).

### 6.3 Level 3: bounded recursion

A rule may use itself for another entity at the same *T* and *R* with the same
parameters (CALC-12). A helper without a concept never uses itself. If a
calculation returns to an entity before it finishes, the result is not
computable because of a cycle, with its chain (CALC-13). Keep a stack of
(rule, entity, parameters) while you calculate.

Conformance files: [`09-manufacturing`](../conformance/09-manufacturing.md)
(including `cyclic_structure`),
[`10-organization`](../conformance/10-organization.md) O1, where `total_cost`
uses itself for child units, [`02-inventory`](../conformance/02-inventory.md)
P2 and P3, and [`06-loans`](../conformance/06-loans.md) J3.

### 6.4 Results as values

A computed value names where it came from (CALC-44): the computed property,
entity, parameters, *T*, *R*, module set, result, and a trace you can show on
request. A projection (a stored result) names the last fact it took into
account and may be thrown away at any time; the calculation from the facts
decides if they differ (CALC-45, CALC-46). How you store projections is yours
to choose (06 §2.15).

## 7. Constraints and rejection records

Read [`06-calculation-rules.md`](../form/06-calculation-rules.md) §2.12 and
§2.13, [`04-concepts.md`](../form/04-concepts.md) §2.7, and decisions
[0047](../decisions/0047-constraints-and-backdated-changes.md) and
[0053](../decisions/0053-reading-corrected-facts.md).

```
def check_action(action, facts, store):
    rejections = []
    rejections += form_rules(action, facts)          # FACT-9..14, 23, 24,
                                                     # VALUE-8, CONCEPT-14
    times = touched_times(facts)                     # 04 §2.7, 0053
    rejections += scope_rules(facts, times)          # CONCEPT-6, VALUE-16,
                                                     # CONCEPT-18
    for c in installed_constraints:
        if reads_action(c):                          # CALC-57, step 1
            targets = entities_touched_directly(facts)
            read_at = times
        else:                                        # step 2
            targets = all_entities_of(c.concept)
            read_at = times + later_valid_times(targets, facts)
        for e in targets:
            for t in read_at:
                if not belongs_to(e, c.concept, t): continue     # CALC-54
                after  = evaluate(c, e, t, store + facts)
                before = None if reads_action(c) else evaluate(c, e, t, store)
                if after is not YES and before in (YES, None):   # step 3
                    rejections.append(reject(c, e, t))           # CALC-41
                # not computable or empty counts as "not met"   # CALC-39
    if rejections:
        record_rejection(action, facts, rejections)              # CALC-42
        return REJECTED          # whole action, nothing recorded (CALC-38)
    return ACCEPTED

def touched_times(facts):
    # valid time of each fact, plus the valid time of the target of every
    # correction, retraction, and redaction. Not replacement or ending.
    ...
```

Hard points:

- **Per action, as a whole.** Check after all facts in the action are in place
  (CONCEPT-19). If any check fails, record none of its facts (FACT-18).
- **Value-stating facts only.** CONCEPT-6 and VALUE-16 apply to statements,
  replacements, and corrections, at the valid time of that fact, so a whole
  wrong record can be retracted in one action (04 §2.7, decision 0054).
- **Backdated corrections.** A constraint that does not read the action is read
  for every entity of its concept at the times touched and at every later valid
  time of a fact. This catches a sale that becomes negative stock after an
  earlier receipt is corrected (decision 0047).
- **Reading the action.** `before_action`, `this_action.actor`, and
  `this_action.approver` appear only in constraints (CALC-40). The value of
  such a constraint before the action counts as not existing (CALC-57).
- **Old violations do not block.** A constraint already no before the action
  does not reject it (06 §2.12 step 4).
- **Skipping.** You may skip entities and times whose result is the same
  before and after, if you can prove it (06 §2.12, decision 0047 item 3).
- **Rejection content.** Name the constraint address, its source module with
  exact version, the entity and valid time, and the message (CALC-41). A
  rejection record holds the action with its facts, actor, approver, time
  tried, and every rejection (CALC-42), and never counts as a fact or affects a
  computed value (CALC-43).
- **Which R.** The text does not say which *R* to read before and after an
  action. The reference calculator uses the recorded time of the action.

Conformance files:
[`14-backdated-constraints`](../conformance/14-backdated-constraints.md),
[`10-organization`](../conformance/10-organization.md) O2 and O3,
[`02-inventory`](../conformance/02-inventory.md) P4,
[`19-reading-facts`](../conformance/19-reading-facts.md) (the touched-time
cases), and the empty-result cases in
[`20-written-choices`](../conformance/20-written-choices.md).

## 8. Examples and conformance

Examples are contracts ([`08-proof.md`](../form/08-proof.md)). There are three
kinds: compute, accept, reject (PROOF-1). To run them you need a reader for
the reference notation or a translator to your own format
([`appendix/A-notation.md`](../appendix/A-notation.md) §2.1 and §2.9).

To run an example (PROOF-6 to PROOF-10, PROOF-29 to PROOF-31):

1. Make a space of its own that never mixes with real facts (PROOF-8).
2. Give each local id a fresh identifier. Their order follows the local ids
   compared by Unicode code point (PROOF-7, PROOF-31).
3. Load the starting facts as already recorded, with the written recorded time.
   Do not check them (PROOF-30). Fill unwritten action parts from the default
   example action (PROOF-10).
4. Use the example's default time zone, or UTC if none (PROOF-29).
5. Compute the question, or check the action, with the module set of the
   example's own version.
6. Compare exactly (PROOF-5): same number and unit, same members regardless of
   order for many values, references by local id, and for not computable the
   kind of reason only. A reject example passes only if every rejection comes
   from the named constraint or form rule, and, if an entity or valid time is
   named, at least one is there (PROOF-32).

The `status` of an example is active or replaced (08 §2.2). A replaced example
is not run again (PROOF-21). The reference calculator reports its own run
result as passed, failed, not defined, notation error, or replaced
([`reference/README.md`](../reference/README.md)).

**Claiming a level.** State the level and the version of the standard, for
example "conforms to the Uniti Standard v0.1, level 2" (PROOF-27, 08 §2.9). To
claim a level, pass all the examples for that level and below, plus every group
outside calculation. Refuse modules above your level (PROOF-28).

The freeze gate, version contracts, and behavior change reports (PROOF-18 to
PROOF-24) concern a tool that freezes modules. They need the same example
runner, so build them after the runner works.

## 9. Build order

Do these in order. Each step names its rules and what proves it.

1. **Fact store.** Append-only; the parts in section 2.1; atomic actions.
   FACT-1 to FACT-3, FACT-15, FACT-18 to FACT-22. Proof: your own tests that
   nothing is changed or deleted; the conformance examples start their facts
   as already recorded (PROOF-30), so they do not test this step.
2. **Form checks on facts.** Kinds, targets, valid-time order, the one-value
   rule. FACT-8 to FACT-14, CONCEPT-14. Proof: your own tests. The conformance files have
   no example yet that rejects a fact of a wrong form (see the
   [conformance README](../conformance/README.md) for the current list).
3. **Reading at (T, R).** Section 3. FACT-17. Proof:
   [`19-reading-facts`](../conformance/19-reading-facts.md),
   [`00-form-examples`](../conformance/00-form-examples.md).
4. **Values and exact numbers.** Section 4. VALUE-1 to VALUE-11, CALC-20.
   Proof: [`20-written-choices`](../conformance/20-written-choices.md), the
   rental and finance cases.
5. **Module reader and installer.** Notation reader, addresses, cards,
   versions, relations. Section 5. Proof:
   [`15-change`](../conformance/15-change.md),
   [`16-relations`](../conformance/16-relations.md),
   [`17-vocabulary`](../conformance/17-vocabulary.md),
   [`18-module-swap`](../conformance/18-module-swap.md).
6. **Example runner.** Section 8. PROOF-5 to PROOF-10. Proof: it runs
   [`00-form-examples`](../conformance/00-form-examples.md) with the expected
   results.
7. **Level 1 calculation.** Section 6.1, CALC-8 to CALC-30, CALC-51 to
   CALC-56. Proof: the level 1 files in section 6.1.
8. **Per-action checks.** CONCEPT-6, CONCEPT-18, CONCEPT-19, VALUE-16, then
   constraints, rejection, and rejection records (CALC-37 to CALC-43,
   CALC-57). Proof: section 7 files.
9. **Open computed properties.** Contributions, CALC-32 to CALC-36, CALC-49.
   Proof: [`02-inventory`](../conformance/02-inventory.md) P1.
10. **Level 2.** `fold`, tie-breaker, CALC-18. Proof: section 6.2 files.
    Claim level 1 or 2 here if you stop.
11. **Level 3.** Recursion and cycles, CALC-12, CALC-13. Proof: section 6.3
    files.
12. **Computed value details and projections.** CALC-44 to CALC-48.
13. **Redaction** (provisional). FACT-23 to FACT-25.
14. **Run everything.** All conformance files for your level, then state the
    level (PROOF-26, PROOF-27).

## 10. Using the reference calculator as a map

The program in [`reference/`](../reference/README.md) is a reference for
comparison. It is not part of the standard, and it is not a library to ship;
if it and the text differ, the text is right. It is slow on purpose and does
not guess: a situation the text does not define raises an error. Use it to
see what a step looks like and to compare answers.

| Step | File in `reference/calculator/` |
|---|---|
| Exact numbers, units, time, empty, not computable | `values.py` |
| Operations that do not read facts | `operations.py` |
| Reading the notation (modules, cards, rules, examples) | `reader.py` |
| Module set, name lookup, installed modules | `module_set.py` |
| Fact store, reading at (T, R), evaluator, recursion, contributions | `compute.py` |
| Checking an action, rejection | `constraints.py` |
| Running examples and exact comparison | `examples.py` |
| Comparing versions, behavior change | `versions.py` |
| Required card parts before freezing | `completeness.py` |

To run all its tests, from the repository root:
`python -m unittest discover -s reference/tests -t reference`.
