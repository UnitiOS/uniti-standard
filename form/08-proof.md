# Proof

Status: draft

## 1. Purpose

Every piece of content that holds logic must prove itself
([`00-principles.md`](../00-principles.md), P9). The proof form sets how a
module shows, with examples that a machine can run and a person can read, that
its calculation rules and constraints work as intended. The same examples
become a **contract**: users know exactly what changes when a module, or a
module it uses, changes version.

## 2. Definitions

### 2.1 Example

An **example** is a set of facts, plus one question or one action, and the
result that must come out of them. Its form is always "if these facts exist,
then ...".

There are three kinds of example, and only three:

| Kind | Form | Example |
|---|---|---|
| **Compute example** | facts + question at (*T*, *R*) → expected result | Rental of three nights × 50,000 → total 150,000 |
| **Accept example** | facts + action → action accepted | Stock 5, rented 2 → accepted |
| **Reject example** | facts + action → action rejected by a certain constraint or rule | Stock 1, rented 2 → rejected by `enough_stock` |

An example is content, written in a module, and has an address
([`02-addresses.md`](02-addresses.md)).

### 2.2 Parts of an example

| Part | Meaning | Required? |
|---|---|---|
| **Address** | Its permanent name | required |
| **Kind** | Compute, accept, or reject | required |
| **Title** | A short heading in human language | required |
| **Explanation** | What this example shows and why the result is what it is, in language a business owner can read | required |
| **Facts** | The starting facts, each with its valid time and recorded time | required |
| **Question** | For a compute example: the computed property, entity, parameters if any, *T*, and *R* | required for a compute example |
| **Action** | For accept and reject examples: the action that is tried, with its facts | required for accept and reject examples |
| **Expected result** | See §2.4 | required |
| **Domain** | The domain the example comes from, for example rental or clinic | required for the vocabulary |
| **Default time zone** | The zone used to read a date as an instant inside the example ([`03-values.md`](03-values.md), VALUE-10). If it is not written, UTC | optional |
| **Status** | Active or replaced (§2.7) | required |

An example is run with **the module set of its own version**: the module in
which the example is written, plus the exact version of every module it uses
([`07-change.md`](07-change.md) §2.5).

### 2.3 Entities and actions inside an example

**Local id.** An entity inside an example does not use a real identifier. It
is given a **local id**, for example `tent`, `r1`, or `sari`, which is valid
only inside that example. When the example is run, the machine gives each
local id a new identifier that has never been used outside the example. The
order of these identifiers follows the order of their local ids, compared
character by character by Unicode code point, so `r10` comes before `r2`. This
order is needed because the tie-breaker uses the identifier as the last order
([`06-calculation-rules.md`](06-calculation-rules.md) §2.6). In this way the
result of an example is the same every time it is run.

**Separate from real facts.** An example is run in a space of its own. The
facts of an example never mix with the real facts of an organization, and real
facts are never read by an example.

**Recorded time is written.** Outside an example, the recorded time is always
given by the recorder ([`01-facts.md`](01-facts.md), FACT-15). Inside an
example, the recorded time is written, because an example describes what has
already happened. In this way an example can test a reading at two times, for
example an expense that was recorded late.

**Starting facts are not checked.** The starting facts are taken as already
recorded. They are not checked by constraints or by required properties, so an
example only needs to hold the facts it needs. Only the action in an accept
example and in a reject example is checked.

**An action may be abbreviated.** The parts of an action that are not
important for an example may be left out. They are filled in with the
**default example action**: actor "example actor", source "example". The parts
that a rule checks, for example the approver in an approval constraint, must be
written.

### 2.4 Expected result

| Kind | Expected result |
|---|---|
| Compute example | One value; empty; or not computable with its kind of reason ([`06-calculation-rules.md`](06-calculation-rules.md) §2.9) |
| Accept example | The action is accepted. A compute question after the action, with its result, may be added |
| Reject example | The action is rejected, with the constraint or form rule that rejects it. The entity and valid time where the constraint fails may be added |

The result is compared **exactly**:

- a number is exactly the same, including its unit, with no "approximately";
- for a property with many values, the members of the collection are the same,
  regardless of order;
- references are compared by local id;
- for not computable, what is compared is the kind of reason, not the
  explanatory sentence.

A reject example passes only if the action is rejected **by the constraint
that is named**. An action rejected by something else, for example a required
property forgotten in the example, makes the example fail.

One action can be rejected several times by the same constraint, for different
entities or valid times. A reject example passes if **every** rejection comes
from the constraint or form rule that is named, and, if an entity or valid
time is named, at least one rejection is at that entity and time. Other
rejections do not need to be written.

### 2.5 When examples are required

| Content | Required examples |
|---|---|
| Every computed property | At least one compute example |
| Every contribution | At least one compute example of the computed property it contributes to, which shows that contribution |
| Every constraint | At least one accept example and one reject example by that constraint |
| In the vocabulary | The above, from at least two different domains |

The accept example and the reject example together prove that a constraint
does not always reject and never forgets to reject.

There should also be an example for a not computable result, if the rule can
fail, for example because it uses `single`, `÷`, or an exchange rate.

**Examples do not prove that the rule is right** by the standards of
accounting, law, or the custom of a domain. Examples prove that the rule
produces what its author states. For this reason the expected result should be
computed **without running the rule**, for example by hand or by another
person. A result copied from the output of the rule itself proves nothing.

### 2.6 The freeze gate

A version **cannot be frozen** ([`07-change.md`](07-change.md) §2.1) unless:

1. every piece of content that requires examples has examples according to
   §2.5;
2. every one of its active examples is **proven**: run with the module set of
   that version, and the result is exactly the same as expected;
3. every example from the previous version has been run again according to
   §2.7.

Examples are run by an implementation that conforms to the standard at a level
sufficient for their rules (§2.9). The freeze record should name the
implementation that ran them.

### 2.7 Contract between versions

When a new version of a module is prepared, every active example from the
previous version is **run again** with the new version.

- If all of them pass, the behavior of the module has not changed for anything
  that was ever exemplified.
- If any fails, the owner chooses one of two:
  - fix the rule until the example passes again; or
  - mark the old example **replaced**, with a reason, and preferably with a
    replacement example.

An example is **never deleted**. A replaced example can still be read, is not
run again, and still shows how the module used to behave.

Every example that is replaced because it failed is reported by the machine as
a **behavior change**, together with the kind of change between versions
(addition, modification, deprecation; [`07-change.md`](07-change.md) §2.2).
The report names the example, the old result, the new result, and the owner's
reason. Anyone who is about to install the new version can read it
**before** installing.

Example: vocabulary version 4 changes the rounding of depreciation from
"remainder to the last month" to "remainder to the first month". The old
example "accumulation as of 31 March 999,999" fails, because the new result is
1,000,011. The owner of the vocabulary marks it replaced with the reason
"following the new policy", and adds a new example. Every user of the
vocabulary sees one behavior change line, complete with both numbers.

### 2.8 Contract between modules

Rudi's module uses vocabulary version 3. Rudi's own examples have been proven
with vocabulary version 3.

Before Rudi moves to vocabulary version 4, all of Rudi's examples are **run
again** with vocabulary version 4. Those that fail are treated as in §2.7:
Rudi fixes the module, or marks the example replaced. In this way Rudi knows
exactly whether the move is safe, **before** freezing the version that uses
it.

The result in an organization can differ from the result of an example,
because the organization has installed other modules that also contribute. An
example proves the logic in the module set that it names. An organization that
wants to bind its own module set may write examples in its own module, using
the modules it has installed.

### 2.9 Conformance tests

The standard also proves itself in the same way. The **conformance tests** are
a set of examples owned by the standard, in the same form as the examples in a
module, to test **implementations**:

| Group | What is tested |
|---|---|
| Facts | Reading at two times, all six fact kinds, rejection of facts with a wrong form |
| Values and concepts | Value types, units, default time zone, per-action checks, derived values |
| Calculation level 1 | Every basic operation, empty and not computable, exact numbers, units |
| Calculation level 2 | Sort and fold, including the tie-breaker |
| Calculation level 3 | Recursion and cycles |
| Constraints | Per-action checks, rejection, rejection records |
| Change and proof | Versions, replaced examples, behavior change reports |

The conformance tests are addressed under the owner `standard` and are kept in
[`conformance/`](../conformance/00-form-examples.md).

- An implementation states the **level** it supports: 1, 2, or 3.
- An implementation may state that it **conforms to the Uniti Standard** only
  if it passes all conformance test examples for its level and the levels
  below it, plus all groups outside calculation.
- The statement always names the version of the standard and the level, for
  example "conforms to the Uniti Standard v0.1, level 2".
- An implementation refuses to install a module that holds a rule above its
  level, naming which rule. It must not run part of it and then quietly give a
  different result.

Who may use the Uniti name for a statement like this, and whether there is
certification, has not been decided
(`kajian/01-ekosistem.md`, B7)
<!-- ARCHIVE-LINK: kajian/01-ekosistem.md -->. The conformance tests are the
technical basis, whatever that decision is.

## 3. Rules

**Form of an example**

- **PROOF-1.** Every example MUST be one of three kinds: compute, accept, or
  reject.
- **PROOF-2.** Every example MUST have an address, kind, title, explanation,
  facts, expected result, and status.
- **PROOF-3.** A compute example MUST name the computed property, entity,
  parameters if any, *T*, and *R*.
- **PROOF-4.** Accept and reject examples MUST name the action that is tried.
  A reject example MUST name the constraint or form rule that rejects it.
- **PROOF-5.** The expected result MUST be compared exactly according to §2.4.
- **PROOF-32.** A reject example MUST pass only if every rejection comes from
  the constraint or form rule that is named, and, if an entity or valid time is
  named, at least one rejection is at that entity and time.
- **PROOF-6.** An example MUST be run with the module set of its own version.

**Entities and data inside an example**

- **PROOF-7.** Entities inside an example MUST use local ids. When the example
  is run, every local id MUST be given an identifier that has never been used
  outside the example.
- **PROOF-31.** The identifiers given to local ids MUST be in the order of
  their local ids, compared character by character by Unicode code point.
- **PROOF-8.** The facts of an example MUST NOT mix with real facts, and real
  facts MUST NOT be read by an example.
- **PROOF-9.** An example MUST NOT hold real personal data.
- **PROOF-10.** Facts inside an example MUST name their valid time and
  recorded time. Parts of an action that are not written MUST be read as the
  default example action.
- **PROOF-11.** The explanation of an example SHOULD be understandable to a
  person who is not a programmer.
- **PROOF-12.** The expected result SHOULD be computed without running the rule
  that is exemplified.
- **PROOF-29.** An example that does not name a default time zone MUST be run
  with the UTC zone.
- **PROOF-30.** The starting facts of an example MUST NOT be checked by
  constraints or required properties. Only the action in an accept example and
  in a reject example is checked.

**Obligation to have examples**

- **PROOF-13.** Every computed property MUST have at least one compute
  example.
- **PROOF-14.** Every contribution MUST have at least one compute example that
  shows that contribution.
- **PROOF-15.** Every constraint MUST have at least one accept example and at
  least one reject example by that constraint.
- **PROOF-16.** In the vocabulary, the examples for every computed property,
  contribution, and constraint MUST come from at least two different domains.
- **PROOF-17.** A rule that can produce not computable SHOULD have an example
  for that result.

**Freezing and between versions**

- **PROOF-18.** A version MUST NOT be frozen unless it meets §2.6.
- **PROOF-19.** An active example from the previous version MUST be run again
  with the new version. Any that fails MUST be fixed or marked replaced before
  the new version is frozen.
- **PROOF-20.** An example that is marked replaced MUST name a reason, and
  SHOULD name its replacement example.
- **PROOF-21.** An example MUST NOT be deleted. A replaced example MUST remain
  readable, and MUST NOT be run again as a condition of freezing.
- **PROOF-22.** The machine MUST report every example that is replaced because
  it failed as a behavior change, with the old result, the new result, and its
  reason.
- **PROOF-23.** The behavior change report SHOULD be shown to an organization
  before it installs the new version.

**Between modules**

- **PROOF-24.** Before a module freezes a version that uses a new version of
  another module, all of its examples MUST be run with that new version.

**Conformance tests**

- **PROOF-25.** Conformance tests MUST be written in the form of examples
  according to this document, under the owner `standard`.
- **PROOF-26.** An implementation MUST state the level it supports.
- **PROOF-27.** An implementation MAY state that it conforms to the Uniti
  Standard only if it passes all conformance test examples according to §2.9.
  The statement MUST name the version of the standard and the level.
- **PROOF-28.** An implementation MUST refuse to install a module that holds a
  rule above its level, naming which rule.

## 4. Examples

**Rental: a compute example.**

```
example rudi/rental/three_night_rental
  kind         compute
  title        Three-night rental
  explanation  A tent at a rate of 50,000 a day is rented from 6 to 9 October.
               Three nights, so the total is 150,000.
  zone         WIB
  facts        recorded 6 Oct 2026 10:00
    tent  type         Item            valid 1 Oct 2026
    tent  daily_rate   50,000 IDR/day  valid 1 Oct 2026
    r1    type         Rental          valid 6 Oct 2026
    r1    item         tent            valid 6 Oct 2026
    r1    start_date   6 Oct 2026      valid 6 Oct 2026
    r1    end_date     9 Oct 2026      valid 6 Oct 2026
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR
```

The starting facts are recorded by the default example action. How to write
examples is detailed in
[`appendix/A-notation.md`](../appendix/A-notation.md) §2.9.

**Rental: a reject example and an accept example** for the constraint
`no_overlap`. The facts are the same: a unique tent is already rented by `r1`
for 10 to 13 October.

| Example | Action | Result |
|---|---|---|
| `one_day_overlap` (reject) | Record rental `r2`, tent, 12 to 14 October | Rejected by `rudi/rental/no_overlap`, entity `r2` |
| `adjoining_no_overlap` (accept) | Record rental `r2`, tent, 13 to 15 October | Accepted, because the first rental ends before 13 October |

In `one_day_overlap`, the constraint fails twice: for `r2`, and also for `r1`,
because there is now another rental that overlaps it. The example still
passes, because both rejections are by the constraint that is named, and one
of them is at entity `r2` (PROOF-32).

**Organization: a reject example with an approver.** The constraint
`approved_if_large` ([`06-calculation-rules.md`](06-calculation-rules.md)
§2.12). Facts: `sari` has a contract with the job title manager. Action: record
a purchase of 12,000,000 IDR, actor `sari`, approver `sari`. Result: rejected
by `approved_if_large`, because the approver is the same as the actor. Here the
action must not be abbreviated, because the actor and the approver are exactly
what is tested.

**Clinic: a compute example for not computable.** A claim of 5,000,000 with a
policy whose cap has not been recorded. Ask: `claim1.paid`, a computed property
that reads the share of that claim from `Policy.payments`
([`06-calculation-rules.md`](06-calculation-rules.md) §4). Result: not
computable, kind of reason **empty value**.

More examples, from 12 domains, are in `uji/01-hitung.md`
<!-- ARCHIVE-LINK: uji/01-hitung.md -->. Every case there will later be
rewritten in this form.

## 5. Not an example

- **An example with the name and phone number of a real customer**, copied
  from a database.
- **A result of "approximately 150,000".** Results are compared exactly.
- **An example that is deleted** because it no longer passes in the new
  version. Such an example is marked replaced.
- **An expected result filled in by running the rule and copying its
  output.**
- **An example that uses the "latest version" of a vocabulary.** An example is
  always run with the exact version.
- **An "example" that is a description without facts**, for example "the total
  due is the rate times the length of the rental". That is a definition, not a
  proof.

## 6. Reasons

- **Three kinds of example**, because content has only two kinds of logic: the
  kind that computes and the kind that rejects. A constraint needs two kinds of
  example so that it is proven in both directions.
  ([`decisions/0036`](../decisions/0036-three-kinds-of-examples.md))
- **Examples are required, and they are the freeze gate**, so that P9 is
  guarded by the machine, not just recommended.
  ([`decisions/0037`](../decisions/0037-required-examples.md))
- **Examples as a contract between versions and between modules.** The kind of
  change from stage 2 only shows **what** changed; examples show **the effect**
  on the numbers.
  ([`decisions/0038`](../decisions/0038-examples-as-contracts.md))
- **Local ids, and no real personal data**, so that an example may be shared
  with anyone, and never mixes with real records.
  ([`decisions/0039`](../decisions/0039-data-in-examples.md))
- **Conformance tests in the same form**, so that the standard is tested in the
  same way as content, and anyone can build an implementation and prove it.
  ([`decisions/0040`](../decisions/0040-conformance-tests.md))

## 7. Outside standards

| Part | Counterpart |
|---|---|
| An example as "if ... then ..." | *Given–When–Then* in Gherkin; *golden test* |
| Examples that a person reads and a machine runs | *doctest* in Python; *Specification by Example* |
| Contract between modules | *consumer-driven contract testing* |
| Behavior change between versions | *Semantic Versioning*, but here the effect is computed from examples |
| Conformance tests | the W3C test suites for RDF and SHACL; the DMN TCK; the XBRL conformance suites |
| No real personal data | synthetic data; ISO/IEC 20889 on de-identification |

## 8. Open questions

1. **Who runs the examples at freeze time.** If freezing happens on a machine
   owned by the module's author, how can others trust that the examples are
   really proven? Depends on the list of ecosystem modules
   (`kajian/01-ekosistem.md`, C4)
   <!-- ARCHIVE-LINK: kajian/01-ekosistem.md -->.
2. **Large examples.** Scale tests need millions of generated facts. May an
   example be a data generator instead of a list of facts?
3. **Examples for bridges.** Does a "same as" bridge between two modules need
   to be proven with an example?
4. **Storage format of examples.** The written form in §4 is the reference
   notation, detailed in
   [`appendix/A-notation.md`](../appendix/A-notation.md) §2.9. The default time
   zone of an example and the unchecked starting facts were added when the
   notation was written
   ([`decisions/0043`](../decisions/0043-additions-from-notation.md)). The
   order of identifiers in an example and reject examples with several
   rejections were added from the reference calculator
   ([`decisions/0044`](../decisions/0044-additions-from-reference-calculator.md)).
5. **Who marks a behavior change in the vocabulary.** For the vocabulary, does
   marking an example replaced need the approval of more than one party?
   Discussed together with governance
   (`kajian/01-ekosistem.md`, A2)
   <!-- ARCHIVE-LINK: kajian/01-ekosistem.md -->.
