# Uniti in plain words

Status: guide; not normative

> [Uniti Standard](../README.md) › Guide · for anyone who wants to understand
> the idea, with no notation and no rule numbers

This guide explains the Uniti Standard in everyday words. It adds no rule.
When this guide and the standard's own text (the *normative* text) differ,
the normative text wins.

It takes about ten minutes to read. When you want to see the same ideas in
the real notation, read the [tour](tour.md) next.

## 1. Why it exists

Every organization keeps **facts**, what happened, and **logic**, how its
numbers are worked out. A shop records sales and works out its stock. A
clinic records visits and works out what a patient owes. A school records
enrollments and works out who has paid.

Today the two are usually mixed inside one piece of software, written by one
builder. That causes three familiar problems:

- **Parts do not fit together.** A cashier system and a warehouse system made
  by different people disagree about what "stock" means.
- **History breaks.** When the software changes, old records are moved,
  converted, or lost.
- **Knowledge is locked in.** How the organization really works is hidden
  inside code that only its builder can read.

The Uniti Standard gives facts and logic **one shared form**, the same in
every domain. Anyone who writes in that form can combine their work with the
work of others, without asking them and without conflict.

## 2. Eight ideas

### Idea 1: only facts are recorded

A **fact** is one small statement about one thing: "the tent costs
50,000 IDR a day", "rental r1 starts on 6 October". Everything that can be
worked out from facts, such as a balance, a total due, or a stock level, is
**not** recorded. It is calculated when it is asked for.

So two people who read the same facts with the same rule always get the
same total: there is no stored total to fall out of date.

### Idea 2: a fact has two clocks

Every fact keeps two times:

- **when it is true** in the world, called the *valid time*;
- **when it was recorded**, called the *recorded time*.

On 20 October, Alex records that the tent costs 60,000 IDR a day **from
1 November**. The fact is recorded on 20 October but is true from 1 November.

With both clocks, any question can be asked "as it was known on" a day: what
did we know on 15 October about the price in November? This matters for
audits, disputes, and reports that must not change after they were sent.

### Idea 3: nothing is erased

A fact is never edited or deleted. A change is a **new fact** that points to
the old one. The standard tells two situations apart:

- **The world changed.** The price really rose. The new fact *replaces* the
  old one from a certain day, and the old price stays true for the days
  before.
- **The record was wrong.** The price was typed as 5,000 instead of 50,000.
  The new fact *corrects* the old one: the old one was never true.

It works like an accountant's ledger. A mistake is fixed with a correcting
entry, never by rubbing out the old line, so the books always show what
happened and who did it.

### Idea 4: numbers come from written rules

A **calculation rule** says how a number is worked out from facts, for
example "the total due is the daily rate times the number of days". It is a
little like a spreadsheet formula, but it is written once, next to the facts
it reads, with a name and a definition that people can read.

Some rules say **no**. A *constraint* such as "one tent is not rented twice on
the same day" checks every new recording: one act of writing facts down,
which may hold several facts at once. If the recording breaks the rule, the
whole recording is refused, with a message that says why.

When a number cannot be worked out, for example because a price is missing,
the answer says so and why. It never quietly becomes 0.

### Idea 5: every word has a card

Every kind of thing (a *concept*, such as "Rental") and every piece of
information about it (a *property*, such as "start date") has a **card**,
like a dictionary entry: a name, a definition, what it includes, and what it
does not. So "Rental" means the same to everyone who reads it, person or
machine.

Words that many organizations need, such as party, item, and payment, are
written once in a **shared vocabulary**, so that different builders use the
same words for the same things.

### Idea 6: every name carries its owner

Everything has an **address** that starts with its owner, a little like a web
address or a family name. Alex's concept is `alex/rental/Rental`. If another
builder also makes a concept called "Rental", its address starts with that
builder's name, so the two never collide. Each owner writes only under their
own name; how this is checked between organizations is settled in
version 0.2.

### Idea 7: change by new versions, never by editing

Content is grouped in a **module**, such as Alex's `alex/rental`. A module is
published in **versions**, like editions of a book. Once a version is frozen,
it never changes.

Whoever uses Alex's module names the exact version. When Alex publishes a new
version, nothing changes for them until they choose to move. Facts recorded
with the old version can still be read by the new one, without being moved or
converted.

### Idea 8: every rule proves itself

Every rule comes with **examples**: some facts, a question, and the answer
that must come out. It is like a worked exercise with the answer printed next
to it. A machine runs the examples. A rule is accepted only when all its
examples pass, and a version cannot be frozen until they do.

The standard uses the same idea for software. It comes with a set of
examples of its own, the **conformance tests**. The standard has three levels of
calculation, from basic to advanced, and software says which level it
supports. It may say it follows the Uniti Standard only when it gives the
expected answer to every example for that level.

## 3. Who does what

| Who | What they make | Freedom |
|---|---|---|
| The standard | The **form**: how anything is written | Fixed. It only grows, rarely |
| The shared vocabulary | **Shared words** that many organizations need | Grows when modules from at least two domains need the same word |
| Each organization or builder | **Modules**: the words and rules of one field or one organization | Free. Anyone may write one |
| Software makers | **Implementations**: software that stores facts and runs the rules | Free, as long as it passes the conformance tests |

The form is the grammar, the vocabulary is the words, and a module is a story
written with them. The standard fixes only the grammar.

A small business does not usually write any of this itself. It uses software
that follows the standard and modules that others have published, and writes
its own module only for what is special about it.

## 4. Twelve words to know first

| Word | In plain words |
|---|---|
| **Fact** | One small statement about one thing, with its two times |
| **Entity** | Anything a fact can be about: a person, an item, an event, a document |
| **Property** | What a fact says about an entity: its name, price, start date |
| **Valid time** | When a fact is true in the world |
| **Recorded time** | When a fact was recorded |
| **Concept** | A kind of entity, such as Rental or Patient, described by a card |
| **Module** | A package of concepts, properties, and rules, with one owner and frozen versions |
| **Computed property** | A number worked out by a rule, never recorded |
| **Constraint** | A rule that refuses a recording that breaks it |
| **Example** | Facts plus the answer that must come out: the proof of a rule |
| **Conformance tests** | The standard's own examples, which software must pass |
| **Normative** | Part of the standard itself, which software is measured against |

Every term has exactly one meaning, listed in the
[glossary](../01-glossary.md).

## 5. Questions people ask

**Is this a programming language?**
No. Rules are written with a small set of operations that the standard
defines, closer to spreadsheet formulas than to a program. When a domain
needs a new way of calculating, it is added to a shared calculation library
as content; the form itself stays small.

**Is it software, or a database?**
Neither. It says what must be recorded and what must come out, not how to
build it. Any software may follow it, with any database. When software and
the standard differ, the standard is right.

**How is it different from a database design or a spreadsheet?**
A database design says which columns exist. The Uniti Standard also says what
each word means, how every number is worked out, how things change over time
without losing history, and it proves all of that with examples.

**Do I have to be a programmer to write content?**
Cards are mostly plain sentences: a name, a definition, what is included and
what is not. Rules and examples are written in the standard's notation, which
takes some care to learn. Software built on the standard may offer forms or
an assistant to help; the standard does not require either.

**What happens when I record something wrong?**
You record a correction, with a reason. The wrong fact stays, and the
correction points to it, so you can always see what was recorded, when, by
whom, and why it was changed.

**Can a fact ever be removed, for example personal data?**
Facts are not deleted. For personal data, the standard has a way to hide a
value while the fact itself stays, called *redaction*. That part is not
final yet (it is marked *provisional*), because it waits for a review of data
protection law.

**Does it fit my domain?**
The standard has been tested on rental, finance, inventory, payroll,
subscriptions, loans, a clinic, a school, manufacturing, the units of an
organization, loyalty points, and logistics. It does not claim to fit
everything: a domain that does not fit is a finding, and findings are how the
standard improves.

**Can I rely on it? It says "locked".**
Locked means version 0.1 is complete and no longer added to. Until it is
declared stable, it changes only when building the first real system shows a
real problem in the text. And there is a promise: an answer the standard
gives today will not change in a later version, and a recording it accepts
stays accepted. Only a refusal, or an "I cannot work this out", may later
become an answer. The few exceptions are listed under "Versions and
compatibility" in the [README](../README.md#versions-and-compatibility).

**Why is it in English?**
English is the one language of the standard text, so that everyone reads the
same words. The content you write is not limited to English: every concept
and property can have names and definitions in any language, for example
Indonesian.

**Who looks after it?**
For now, the owner of the standard decides every change, until shared
ownership is settled in version 0.2. Anyone may propose a change by writing a
*finding*: a short report of a real case where the standard falls short. See
[`GOVERNANCE.md`](../GOVERNANCE.md).

## 6. Where to go next

- [Tour](tour.md): the same ideas on one small story, in the real notation.
- [Overview](overview.md): a map of the whole standard, document by document.
- [Implementing](implementing.md): for people who build software.
- [Principles](../00-principles.md): the first document of the standard itself.
