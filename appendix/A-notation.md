# Appendix A. Notation

Status: locked (v0.1.0)

> [Uniti Standard](../README.md) › Appendix
> · Previous: [Proof](../form/08-proof.md)
> · Next: [Content](../content/README.md)
> · [Rules NOTATION-n](../rules.md#appendix-a-notation)

**Contents**

- [1. Purpose](#1-purpose)
- [2. Definitions](#2-definitions)
  - [2.1 Standing of this appendix](#21-standing-of-this-appendix)
  - [2.2 Characters, lines, and comments](#22-characters-lines-and-comments)
  - [2.3 Fixed values](#23-fixed-values)
  - [2.4 Units, quantities, and time zones](#24-units-quantities-and-time-zones)
  - [2.5 Names and addresses](#25-names-and-addresses)
  - [2.6 Expressions](#26-expressions)
  - [2.7 Calls and bindings](#27-calls-and-bindings)
  - [2.8 Modules, cards, and rules](#28-modules-cards-and-rules)
  - [2.9 Examples](#29-examples)
  - [2.10 Inside other files](#210-inside-other-files)
  - [2.11 Compact grammar for machines](#211-compact-grammar-for-machines)
- [3. Rules](#3-rules)
- [4. Examples](#4-examples)
- [5. Not examples](#5-not-examples)
- [6. Reasons](#6-reasons)
- [7. Outside standards](#7-outside-standards)
- [8. Open questions](#8-open-questions)

## 1. Purpose

The form documents define **what** a rule, an example, or a card means. This
appendix defines **how to write it** in the **reference notation**, so that
the same writing is read exactly the same way by every person and every
machine. It answers the open questions about notation in
[`06-calculation-rules.md`](../form/06-calculation-rules.md) §8 and
[`08-proof.md`](../form/08-proof.md) §8.

## 2. Definitions

### 2.1 Standing of this appendix

The **reference notation** is the way of writing used in the standard
documents, in examples, and in conformance tests.

- What is standardized remains the **form and its meaning**, in the documents
  in `form/`. This appendix adds no new meaning. If this appendix and a form
  document differ, the form document is correct.
- An implementation may store content in another format, for example JSON or
  RDF, if its meaning is exactly the same as the writing in the reference
  notation ([`06-calculation-rules.md`](../form/06-calculation-rules.md)
  §2.4).
- Conformance tests are written in the reference notation. An implementation
  that wants to run them reads this notation itself or through a translator.
  How is free; the meaning must be the same.

### 2.2 Characters, lines, and comments

**Characters.** Writing uses UTF-8. Calculation symbols are written with
mathematical symbols:

| Symbol | Meaning | Not |
|---|---|---|
| `×` | times | `*`, `x` |
| `÷` | divided by | `/`, `:` |
| `−` | minus, and the negative sign | `-` (hyphen) |
| `≠` `≤` `≥` | not equal, at most, at least | `!=`, `<=`, `>=` |
| `+` `=` `<` `>` | plus, equals, less than, greater than | |

The hyphen `-` is used only inside owner and module names, for example
`happy-camp`. The slash `/` is used only inside addresses and inside units,
for example `IDR/day`.

**Lines.** Writing consists of **sections**: a module, a card, a rule, or an
example. Each section starts with a keyword at the start of a line, with no
spaces in front of it. Its content is written on the following lines, which
are indented with spaces. Tabs are not used.

**Comments.** The sign `#` starts a comment for people, up to the end of the
line, except inside text in quotation marks. Machines do not read comments.

### 2.3 Fixed values

Values written directly, in rules and in examples:

| Value | How to write | Example |
|---|---|---|
| **Number** | A point for decimals. A comma as thousands separator, which may be used or not; if used, at every three digits | `150,000`, `150000`, `0.8`, `1,234.5` |
| **Negative number** | The sign `−` in front | `−5,000 IDR` |
| **Percent** | `%` after the number. It means that number divided by 100, without a unit | `5%` equals `0.05` |
| **Number with a unit** | A number, one space, then a unit (§2.4) | `150,000 IDR`, `2.5 kg`, `3 days`, `50,000 IDR/day` |
| **Text** | Enclosed in double quotation marks. A quotation mark inside the text is written twice. A language code may be written after it | `"Large tent"`, `"Tent ""dome"""`, `"Tent"@en` |
| **Yes/no** | `yes` or `no` | `yes` |
| **Date** | Day, month name, four-digit year. The year is always written | `6 Oct 2026`, `6 October 2026` |
| **Instant** | Date, time with colons, and time zone | `6 Oct 2026 09:00 WIB`, `6 Oct 2026 09:00:30 UTC+7` |
| **Choice** | Name of a choice (§2.5) | `manager`, `paid` |
| **Duration** | A number with a duration unit | `1 month`, `36 months`, `90 minutes` |

**Month names.** January, February, March, April, May, June, July, August,
September, October, November, December. They may be abbreviated to three
letters: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec.

**Thousands comma and separating comma.** A comma between two digits without a
space is a thousands comma, and exactly three digits follow it; `1,5` is not a
number. A comma that separates arguments is always followed by a space: `min(1, 500)` is two arguments, while `min(1,500)` is one
number.

A **reference** has no fixed value in rules, because the identifier of an
entity has no meaning. In examples, a reference is written with a local id
(§2.9).

### 2.4 Units, quantities, and time zones

Unit codes, their quantities, and the relations between units are content, in
the code list `uniti/unit/Unit`
([`content/code-lists.md`](../content/code-lists.md);
[`decisions/0050`](../decisions/0050-code-lists.md)).

**How to write a unit.** A unit is one code, or several codes joined with `/`
(per) or `·` (times). A code may be given the power `²` or `³`. Examples:
`IDR`, `kg`, `m²`, `IDR/day`, `cm³/kg`.

A unit is written with its code, except the five duration units, which are
written with their English names:

| Written | UCUM code |
|---|---|
| `second`, `seconds` | `s` |
| `minute`, `minutes` | `min` |
| `hour`, `hours` | `h` |
| `day`, `days` | `d` |
| `week`, `weeks` | `wk` |

Calendar months and years are written `month` and `year`, which are also their
codes, or in the plural `months` and `years`.

A quantity is written with its name in the code list, and a derived quantity
is written the same way as its unit: `length²` for area, `money/duration`
for a rate.

A **time zone** is written `WIB` (UTC+7), `WITA` (UTC+8), `WIT` (UTC+9),
`UTC`, or an offset from UTC in hours and minutes: `UTC+7`, `UTC+5:30`,
`UTC−3`.

### 2.5 Names and addresses

**The form of a name** follows [`02-addresses.md`](../form/02-addresses.md)
§2.4: concepts and choice lists start with a capital letter (`Rental`);
properties, choices, rules, examples, parameters, and local names use
lowercase letters (`daily_rate`).

**Short name and full address.** A piece of content may be named by its short
name (`Rental`) or by its full address (`alex/rental/Rental`). A short name is
looked up in the module where the writing is and in the modules it uses. If a
short name is found in more than one module, the full address must be used.
‹root› is not written.

**A name after a dot.** In `x.s`, the name `s` is read according to the value
of `x`:

| If `x` is | `s` is |
|---|---|
| An entity | A property, computed property, or helper that applies to its concept. May be a full address: `this.uniti/common/name` |
| A record | The name of its part |
| A range | `start` or `end` ([`06-calculation-rules.md`](../form/06-calculation-rules.md) §2.5) |

**A name without a dot** inside an expression is looked up in this order:

1. A **local name**, that is, a name that applies only inside one rule: a
   binding (§2.7), `let`, or a parameter of the rule.
2. A **choice** from a choice list visible from this module.
3. A **unit**, for example `IDR` in `k.to_unit = IDR`.

A local name must not be the same as the name of a visible choice. If a choice
and a unit have the same name, the choice must be written with its full
address.

**Keywords.** The following words have a fixed meaning, and must not be used
as a local name or a rule name:

- `this`, `T`, `this_action`, `contributions`, `yes`, `no`;
- `if`, `then`, `else`, `and`, `or`, `not`, `in`, `let`, `with`;
- the name of each operation in
  [`06-calculation-rules.md`](../form/06-calculation-rules.md) §2.5.

A keyword may still be used as a property name, because a property name is
always written after a dot: `p.sum` is the property `sum`, not the operation
`sum`.

### 2.6 Expressions

**Reading order.** When there are no parentheses, an expression is read
according to this table, from the tightest:

| Order | Operation | Read |
|---|---|---|
| 1 | `x.s`, `x.s(…)`, call `f(…)`, parentheses `(…)` | from the left |
| 2 | `−` in front (negative) | |
| 3 | `×`, `÷` | from the left |
| 4 | `+`, `−` | from the left |
| 5 | `=`, `≠`, `<`, `≤`, `>`, `≥`, `in` | not chained |
| 6 | `not` | |
| 7 | `and` | from the left |
| 8 | `or` | from the left |
| 9 | `r with a = u` | from the left |
| 10 | `if … then … else …` | |

So `a + b × c` equals `a + (b × c)`, and `not a = b` equals `not (a = b)`. A
comparison must not be chained: `a < b < c` is written `a < b and b < c`.

**`if`** always uses `else`. The part after `else` extends as far as
possible, so an `if` in the middle of another expression is written inside
parentheses: `max(0, (if exists(b) then b else a) − c)`.

**`with`** makes a copy of a record with one part replaced. To replace two
parts, `with` is written twice: `r with a = 1 with b = 2`.

**`let`** always occupies its own line. Its expression ends at the end of
that line, unless a parenthesis is still open. The expression after the `let`
lines is the result:

```
let ti = this.taxable_income
let limit = 60,000,000 IDR
min(ti, limit) × 5%
```

**Records and collections.** A record is written `{a: …, b: …}`. An ordered
collection is written `[…]`, with its members separated by commas; `[]` is a
collection without members.

**New line.** Inside an expression, a line break is the same as a space,
except for `let`. The expression of a rule ends before the first line that is
not indented further than its heading line (short form) or than the word
`rule:` (full form).

### 2.7 Calls and bindings

A **binding** gives a local name to each member of a collection: `s: s.amount`
means "for each member, call it `s`, compute `s.amount`". A binding with two
names is written `(a, k): …`, and is used only in the `step` of `fold`.

**Named arguments** are written `name: value`, for example `of: 1 IDR`.
Because the core operations are closed, each operation has a fixed call form.
From that form a machine knows whether `x:` is a named argument or a binding.
Named arguments are written after plain arguments, in the order of the table.

| Operation | Call form |
|---|---|
| `all` | `all(K)`, `all(K, x: condition)` |
| `single`, `count`, `exists`, `unit_of`, `before_action` | `single(u)` |
| `each`, `each_merged` | `each(k, x: u)` |
| `group` | `group(k, by: x: u)` |
| `sum` | `sum(k)`, `sum(k, x: u)` |
| `min`, `max` | `min(k)`, `min(k, x: u)`, `min(a, b)` |
| `all_match`, `any_match` | `all_match(k, x: condition)` |
| `power` | `power(a, n)` |
| `floor_multiple` | `floor_multiple(n, of: q)` |
| `range`, `overlap`, `at`, `append` | Two plain arguments: `range(a, b)`, `at(t, u)` |
| `difference` | `difference(a, b, unit)` |
| `span` | `span(r, unit)` |
| `split` | `split(r, step: duration)` |
| `history` | `history(x.s, in: r)` |
| `convert` | `convert(n, to: unit)` |
| `not_computable` | `not_computable(text)` |
| `fold` | `fold(k, order_by: x: u, initial: a, step: (s, x): u)`. `order_by` may be omitted for a collection that is already ordered |

A summary without a binding, for example `sum(k)`, summarizes the members of
its collection themselves. It means the same as `sum(k, x: x)`.

**Unit places.** The third argument of `difference`, the second argument of
`span`, and `to:` of `convert` are always read as a unit, not as a local name.
So `span(month, day)` with a parameter named `month` stays clear: the first
is the parameter, the second is the unit.

**Other rules.** A computed property and a helper of a concept are called like
a property: `this.term`, `this.salary(period)`. A helper without a concept is
called by its name: `scale(list, 2)`. Arguments for rules are never named, and
are never bindings.

A helper in the calculation library is called the same way, for example
`median(each(k, x: x.duration))` and `round(n, 1 IDR, nearest)`
([`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).
The name of a choice such as `nearest` is looked up in the modules in use, like
the name of any other choice.

### 2.8 Modules, cards, and rules

**Module.** Every content writing starts with its module. The modules in use
are written with their exact version
([`02-addresses.md`](../form/02-addresses.md), ADDRESS-11):

```
module alex/rental@v3
  uses uniti/item@v1
```

All sections after it belong to that module, until the next `module`.

**Two forms.** Every card and rule can be written in two forms:

| Form | Mark | Used in |
|---|---|---|
| **Full form** | A heading line, then the card parts line by line | A module that will be frozen |
| **Short form** | Only the heading line, and for a rule, its expression. The heading line of a rule ends with `:` | Excerpts in standard documents and in tests |

The short form does not contain the label, the definition, and the other
required card parts, so it is not enough for a module that is frozen.

**Card parts** are written one per line: the part word, a space, then its
content. Long content may be continued on the next line, indented further
than the part word. Content that is free text needs no quotation marks. The
language code is written after the part word with a dot: `label.en`,
`definition.en`.

| Part | Part word |
|---|---|
| Label, definition, includes, excludes, note | `label.‹lang›`, `definition.‹lang›`, `includes.‹lang›`, `excludes.‹lang›`, `note.‹lang›` |
| Parent of a concept | `parent` |
| Personal data marker **[provisional]** | `personal yes` or `personal no` |
| Rejection message of a constraint | `message.‹lang›` |
| Bridge | `same_as`, `broader`, `narrower`, or `similar`, then the full address of Uniti content or a full IRI |
| Rule, in the full form | `rule:`, then its expression on the following lines |

A part that may appear more than once, such as `includes`, is written
repeatedly.

A **bridge** ([`05-relations.md`](../form/05-relations.md) §2.5) is written on
the content card it starts from: a concept card, a property card, or a choice
written with the heading line `choice … to …`. Its target is a full address,
because it is usually content in a module that is not in use, or a full IRI
for an outside standard (RELATION-8):

```
choice national_insurance to uniti/payment/PaymentMethod
  label.en     National health insurance
  same_as      city-pharmacy/cashier/national_insurance

concept Class
  similar      https://schema.org/Course
  note.en      In schema.org, Course is a school subject; here Class
               is a group of students.
```

**Heading lines:**

| Part | Heading line |
|---|---|
| Concept | `concept Rental` |
| Property | `property daily_rate : number (money/duration, position)` |
| Property with many values | `property phone : text, many` |
| Choice list | `choice_list Position, closed` |
| Code list | `choice_list Unit, code` |
| Choice for an open list owned by someone else | `choice qr_payment to uniti/payment/PaymentMethod` |
| Applies to | `applies to Rental:` |
| Computed property | `computed Rental.total_due : number (money, increase), closed` |
| Computed property with a parameter | `computed Employee.salary(month) : number (money, increase), closed` |
| Helper | `helper Rental.term : range` |
| Helper without a concept | `helper scale(list, n) : collection` |
| Constraint | `constraint Rental.no_overlap` |
| Contribution | `contribution being_rented to Item.available` |
| Example | `example three_night_rental` (§2.9) |

**The value type** is written with its name: `text`, `number`, `yes_no`,
`date`, `instant`, `choice ‹List›`, or `reference ‹Concept›`. For a number, the
quantity and the direction are written in parentheses: `number (money,
increase)`. A number without a quantity writes only its direction: `number
(position)`. A property and a computed property with many values write `many`
after the value type: `computed Item.supplier : reference Party, many,
closed`. The result of a helper may also be an intermediate value:
`collection`, `record`, or `range`.

**In the heading line of a rule**, the name before the dot is the concept the
rule applies to, which may be a full address. The name after the dot is the
name of the rule itself, and its address is always in the module where it is
written. So `computed uniti/item/Item.rental_value` in the module
`alex/rental` creates the computed property `alex/rental/rental_value` for a
concept owned by `uniti`.

In the heading line of a contribution, `to Item.available` points to an
existing open computed property, and is looked up like `x.s`.

The **choices** of a list are written one per line under `choices:`.
**Applies to** is written one property per line, plus `required` if the
property is required:

```
choice_list Position, closed
  label.en     Position
  definition.en  A person's position in an organization.
  choices:
    manager
    staff

applies to Rental:
  item         required
  start_date   required
  end_date     required
  note
```

### 2.9 Examples

An example is written as an `example` section, with the parts in
[`08-proof.md`](../form/08-proof.md) §2.2:

| Part | How to write |
|---|---|
| Kind | `kind compute`, `kind accept`, or `kind reject` |
| Title, explanation | `title …`, `explanation …`, free text |
| Domain | `domain rental` |
| Default time zone | `zone WIB`. If not written: `UTC` ([`08-proof.md`](../form/08-proof.md), PROOF-29) |
| Facts | `facts`, then one fact per line |
| Question | `ask r1.total_due  T: 6 Oct 2026  R: 6 Oct 2026 12:00` |
| Action | `action`, then one fact per line |
| Expected result | `result …` |
| Status | `status active` (if not written), or `status replaced`, plus `reason …` and `replaced_by ‹example›` |

**One fact per line:**

```
‹label›: ‹entity› ‹property› ‹value› valid ‹time› recorded ‹instant› ‹kind› ‹target›
```

| Part of the line | Required? | Description |
|---|---|---|
| `‹label›:` | If this fact is the target of another fact | The name of the fact inside the example, for example `f1:` |
| `‹entity›` | required | A local id: lowercase letters, digits, and underscores, starting with a letter, for example `r1`, `big_tent` |
| `‹property›` | required | A short name or a full address; `type` for the base property type |
| `‹value›` | If its kind has a value | Read according to the value type of its property. A reference is written with a local id; a type value is written with the name of a concept |
| `valid ‹time›` | required | A date or an instant |
| `recorded ‹instant›` | If not on the `facts` line | See below |
| `‹kind› ‹target›` | If not a statement | `replaces f1`, `ends f1`, `corrects f1`, `retracts f1`, `redacts f1` **[provisional]** |

**Recorded time.** The `facts` line may state the recorded time for all the
facts below it: `facts recorded 6 Oct 2026 10:00`. A fact line that states
`recorded` itself uses its own time. All initial facts are recorded by the
default example action.

**Time inside examples.** An instant written without a zone is read according
to the default time zone of that example. A date used as an instant, for
example `recorded 6 Oct 2026` or `R: 7 Oct 2026`, is read as the start of that
day in the same zone ([`03-values.md`](../form/03-values.md), VALUE-10).

**The same facts for several examples.** `facts as in ‹example›` uses all the
facts of another example, plus the lines written below it. It means the same
as copying those lines.

**Question.** `ask ‹entity›.‹property›`, plus parameters in parentheses if
there are any, then `T:` and `R:`. A parameter is written as an expression:
`ask org.revenue(range(1 Oct 2026, 1 Nov 2026))  T: 31 Oct 2026  R: 1 Nov 2026`.

**Action.** The `action` line states its recorded time, and the actor and the
approver if a rule checks them: `action recorded 12 Oct 2026 09:00, actor eva,
approver eva`. A part that is not written is filled by the default example
action. The facts of the action are written below it, without `recorded`.

**Expected result:**

| Kind | How to write | Example |
|---|---|---|
| Value | A fixed value; a reference with a local id | `result 150,000 IDR`, `result tent` |
| Many values | Inside `[…]`; the order is not compared | `result [tent, stove]` |
| Empty | `empty` | `result empty` |
| Not computable | `not computable:` and its reason kind | `result not computable: not single` |
| Action accepted | `accepted` | `result accepted` |
| Action rejected | `rejected by` and the constraint or the form rule number, plus the entity and the valid time if needed | `result rejected by no_overlap, entity r2, at 12 Oct 2026` |

An accept example may add questions after the action: after `result
accepted`, write the next pair of `ask` and `result`.

### 2.10 Inside other files

Writing in the reference notation may be placed inside a Markdown file, in a
code block tagged `uniti`. All `uniti` blocks in one file are read in order as
one writing. Text outside those blocks is not read by machines.

A code block without the `uniti` tag, like the examples in the form documents,
is an excerpt to be read by people.

### 2.11 Compact grammar for machines

This summary is for implementers. It means the same as §2.2 to §2.7. It is
written in EBNF (ISO/IEC 14977): `[ ]` may be absent, `{ }` may repeat, `|`
is one of.

```
expression   = { "let" name "=" expression END-OF-LINE } conditional ;
conditional  = "if" expression "then" expression "else" expression
             | replace ;
replace      = or_expr { "with" name "=" or_expr } ;
or_expr      = and_expr { "or" and_expr } ;
and_expr     = not_expr { "and" not_expr } ;
not_expr     = "not" not_expr | comparison ;
comparison   = addition [ ( "=" | "≠" | "<" | "≤" | ">" | "≥" | "in" ) addition ] ;
addition     = product { ( "+" | "−" ) product } ;
product      = negation { ( "×" | "÷" ) negation } ;
negation     = "−" negation | postfix ;
postfix      = primary { "." content-name [ "(" expression { "," expression } ")" ] } ;
primary      = fixed-value | "this" | "T" | "this_action" | "contributions"
             | name [ "(" [ argument { "," argument } ] ")" ]
             | "(" expression ")" | record | collection ;
argument     = [ argument-name ":" ] ( binding | expression | unit ) ;
binding      = ( name | "(" name "," name ")" ) ":" expression ;
record       = "{" [ name ":" expression { "," name ":" expression } ] "}" ;
collection   = "[" [ expression { "," expression } ] "]" ;

fixed-value  = number [ "%" | unit ] | text [ "@" language-code ]
             | "yes" | "no" | date [ time zone ] ;
number       = digit { digit | "," digit digit digit } [ "." digit { digit } ] ;
unit         = element { ( "/" | "·" ) element } ;
element      = unit-code [ "²" | "³" ] ;
date         = digit [ digit ] month-name digit digit digit digit ;
time         = digit digit ":" digit digit [ ":" digit digit ] ;
```

What is not written in this summary, and is set in the text:

- which arguments are a binding, a unit, or an expression, according to the
  call forms in §2.7;
- a name after a number is a unit, except a month name or a keyword;
- `END-OF-LINE` applies only when no parenthesis is still open;
- a number written with thousands commas must have a comma at every three
  digits, and a `date` with a time inside a rule must name the zone.

## 3. Rules

**Standing**

- **NOTATION-1.** Rules, examples, and cards in the standard documents and in
  the conformance tests MUST be written in the reference notation.
- **NOTATION-2.** Another format MAY be used if its meaning is exactly the same
  as the writing in the reference notation.
- **NOTATION-3.** If this appendix differs from a form document, the form
  document MUST be followed.

**Characters and fixed values**

- **NOTATION-4.** Writing MUST use UTF-8, and calculation symbols MUST be
  written with the symbols in §2.2. The hyphen MUST NOT be used as a minus
  sign.
- **NOTATION-5.** Decimals MUST be written with a point. A thousands comma, if
  used, MUST be at every three digits.
- **NOTATION-6.** A date MUST state its year.
- **NOTATION-7.** An instant inside a rule MUST state its time zone. An
  instant inside an example that does not state a zone MUST be read according
  to the default time zone of that example.
- **NOTATION-8.** A unit MUST be written with a code from the code list or a
  name in §2.4, singular or plural. The duration codes `s`, `min`, `h`, `d`,
  and `wk` are not written.

**Names**

- **NOTATION-9.** A short name found in more than one module MUST be replaced
  with the full address.
- **NOTATION-10.** A keyword in §2.5 MUST NOT be used as a local name or a rule
  name.
- **NOTATION-11.** A local name MUST NOT be the same as the name of a choice
  visible from its module.

**Expressions**

- **NOTATION-12.** An expression MUST be read according to the order in §2.6.
  A comparison MUST NOT be chained.
- **NOTATION-13.** `if` MUST use `else`.
- **NOTATION-14.** `let` MUST occupy its own line.
- **NOTATION-15.** Every operation call MUST follow its call form in §2.7.

**Modules and cards**

- **NOTATION-16.** Every content writing MUST start with `module`, and MUST
  name every module it uses with its exact version.
- **NOTATION-17.** A module that will be frozen MUST use the full form for
  every card and rule. The short form MAY be used in excerpts.

**Examples**

- **NOTATION-18.** Every fact in an example MUST be written on one line
  according to §2.9, with a valid time and a recorded time.
- **NOTATION-19.** A fact that is the target of another fact MUST be given a
  label.
- **NOTATION-20.** The expected result MUST be written in one of the ways in
  §2.9.

**Files**

- **NOTATION-21.** Writing inside Markdown that machines read MUST be in a
  code block tagged `uniti`.

## 4. Examples

**Rental: a module in the full form.**

```
module alex/rental@v3
  uses uniti/item@v1

concept Rental
  label.en     Rental
  definition.en  Use of an item by a renter for a certain term, for a fee.
  includes.en  Rental of a tent for three nights.
  excludes.en  Sale of a tent, because the item changes owner.

property start_date : date
  label.en     Start
  definition.en  The first day of the rental term.
  personal     no

property end_date : date
  label.en     End
  definition.en  The day the item is returned. This day is not counted.
  personal     no

property daily_rate : number (money/duration, position)
  label.en     Daily rate
  definition.en  The rental price of an item for one day.
  personal     no

applies to Rental:
  item         required
  start_date   required
  end_date     required

applies to Item:
  daily_rate

helper Rental.term : range
  rule:
    range(this.start_date, this.end_date)

computed Rental.total_due : number (money, increase), closed
  label.en     Total due
  definition.en  The daily rate of the item times the number of days in the
               rental term.
  personal     no
  rule:
    this.item.daily_rate × span(this.term, day)

constraint Rental.no_overlap
  label.en     No overlap
  definition.en  One item is not rented out twice on the same day.
  message.en   This item is already rented for part of that term.
  rule:
    count(all(Rental, s: s ≠ this and s.item = this.item
                            and exists(overlap(s.term, this.term)))) = 0

example three_night_rental
  kind         compute
  title        Three-night rental
  explanation  A tent at a rate of 50,000 a day is rented from 6 to 9 October.
               Three nights, so the total is 150,000.
  zone         WIB
  facts        recorded 6 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    f1: tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 6 Oct 2026
    r1    item        tent            valid 6 Oct 2026
    r1    start_date  6 Oct 2026      valid 6 Oct 2026
    r1    end_date    9 Oct 2026      valid 6 Oct 2026
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR

example rate_rise_after_rental
  kind         compute
  title        Rate rise after the rental is recorded
  explanation  The rate rises to 60,000 from 1 November. The October rental
               still uses the rate valid at T.
  zone         WIB
  facts        as in three_night_rental
    f2: tent  daily_rate  60,000 IDR/day  valid 1 Nov 2026  recorded 20 Oct 2026  replaces f1
  ask          r1.total_due   T: 6 Oct 2026   R: 21 Oct 2026
  result       150,000 IDR
```

The second example uses all the facts of the first example, then adds one
replacement with the target `f1`. The rate line in the first example is
labeled precisely because it is a target.

**Rental: a reject example.**

```
example one_day_overlap
  kind         reject
  title        Overlap of one day
  explanation  The tent is already booked for 10 to 13 October. The new rental
               of 12 to 14 October overlaps on 12 October.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    tent   type        Item          valid 1 Oct 2026
    r1     type        Rental        valid 1 Oct 2026
    r1     item        tent          valid 1 Oct 2026
    r1     start_date  10 Oct 2026   valid 1 Oct 2026
    r1     end_date    13 Oct 2026   valid 1 Oct 2026
  action       recorded 5 Oct 2026 15:00
    r2     type        Rental        valid 5 Oct 2026
    r2     item        tent          valid 5 Oct 2026
    r2     start_date  12 Oct 2026   valid 5 Oct 2026
    r2     end_date    14 Oct 2026   valid 5 Oct 2026
  result       rejected by no_overlap, entity r2
```

**School: the short form, for excerpts.**

```
module example/school@v1

concept Class
concept Student
property class : reference Class
property average_score : number (position)

applies to Student:
  class          required
  average_score

computed Student.rank : number (position), closed:
  1 + count(all(Student, s: s.class = this.class
                               and s.average_score > this.average_score))

example tied_scores
  kind         compute
  title        Two students with the same score
  explanation  Sam 88, Maria and Nina both 84.9, Leo 70. Maria and Nina are
               both at rank 2, and Leo is at rank 4.
  facts        recorded 1 Dec 2026
    k7a    type           Class     valid 1 Jul 2026
    sam   type           Student   valid 1 Jul 2026
    sam   class          k7a       valid 1 Jul 2026
    sam   average_score  88        valid 1 Dec 2026
    maria    type           Student   valid 1 Jul 2026
    maria    class          k7a       valid 1 Jul 2026
    maria    average_score  84.9      valid 1 Dec 2026
    nina  type           Student   valid 1 Jul 2026
    nina  class          k7a       valid 1 Jul 2026
    nina  average_score  84.9      valid 1 Dec 2026
    leo   type           Student   valid 1 Jul 2026
    leo   class          k7a       valid 1 Jul 2026
    leo   average_score  70        valid 1 Dec 2026
  ask          nina.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       2
```

The date `recorded 1 Dec 2026` is read as the start of the day in the zone
`UTC`, because this example does not state a zone.

**Reading order.**

| Written | Read |
|---|---|
| `a + b × c` | `a + (b × c)` |
| `− sum(k) + 5` | `(− sum(k)) + 5` |
| `not exists(x) or x = 0` | `(not exists(x)) or (x = 0)` |
| `x with amount = x.amount × n` | a copy of `x`, with `amount` replaced by `x.amount × n` |
| `s.item = this and T in s.term` | `(s.item = this) and (T in s.term)` |

## 5. Not examples

- **`1,5` for one and a half.** Not a number: a thousands comma is followed by
  three digits. Written `1.5`.
- **`price - discount`** with a hyphen. Written `price − discount`.
- **`min(1,500)` for two numbers.** That is one number. Written `min(1, 500)`.
- **`6 Oct` in an example**, without a year. Written `6 Oct 2026`.
- **`if a then b`** without `else`.
- **`0 < x < 10`.** Written `0 < x and x < 10`.
- **`let x = 1, x + 1`** on one line.
- **`median(k, x: x.duration)`** for a library helper. A helper does not accept
  a binding: `median(each(k, x: x.duration))`.
- **`(draft, submitted)`** as a pair. There is no pair in the operation list;
  a record is used: `{from: draft, to: submitted}`.
- **`let sum = …`.** `sum` is a keyword.

## 6. Reasons

- **Mathematical symbols, not ASCII letters.** `×`, `÷`, and `−` are read the
  same by everyone, and do not collide with the hyphen in module names or the
  slash in addresses and units.
- **Decimal point, colon in times, and English month names.** The reference
  notation is read by business owners in the examples, and is written with the
  same conventions as the whole standard. A machine format that uses ISO 8601
  may be made in another appendix.
- **Fixed call forms.** Because the core operations are closed, `x:` can always
  be told apart as a named argument or a binding, without an extra sign.
- **`let` per line.** It is the easiest to read, and needs no new separator
  sign.
- **Full form and short form.** Standard documents can quote a rule without a
  long card, while a frozen module stays complete.
- **One fact per line.** An example can be read as a table by people, and by
  machines without another format.

The decision: [`decisions/0042`](../decisions/0042-reference-notation.md).

## 7. Outside standards

| Part | Counterpart |
|---|---|
| Grammar summary | EBNF (ISO/IEC 14977) |
| Characters | UTF-8 (RFC 3629), Unicode |
| Units | UCUM; currencies ISO 4217 |
| Language code | BCP 47 |
| Date and instant for machine formats | ISO 8601 |
| Expressions | FEEL in DMN (OMG); CEL |
| Examples of "if … then …" | Gherkin (*Given*, *When*, *Then*) |
| Code block in a file | *fenced code block* in CommonMark |

## 8. Open questions

The seven gaps of meaning in `06` and `08` that were found while writing this
appendix have been settled in their form documents
([`decisions/0043`](../decisions/0043-additions-from-notation.md)).

1. **ASCII equivalents.** May `*`, `<=`, and the like be accepted as
   equivalents of the symbols, for people who type without a special
   keyboard? If so, `-` and `/` still cannot be used, because they are already
   used in names and addresses.
2. **Keywords in other languages.** The reference notation uses English words:
   `if`, `all`, `sum`. Is a notation in another language with exactly the same
   meaning needed, so that the standard can be used in other countries?
3. **Machine format.** A JSON or RDF format with the same meaning, for
   exchange between implementations. If needed, it is written as appendix B.
4. **List of units and time zones.** Answered: the list of units moved to
   `content/code-lists`, and time zone names remain a way of writing
   ([`decisions/0050`](../decisions/0050-code-lists.md)).
