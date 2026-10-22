# Principles

Status: draft

> [Uniti Standard](README.md) › Principles · Next: [Glossary](01-glossary.md)

This document binds the whole standard. Every form in part A and every piece of
content in part B must be explainable by the principles here. When a rule
contradicts a principle, the rule is what gets fixed.

---

## 1. Purpose

Every organization (a business, clinic, school, institution) keeps two things:

- **facts**: what happened and what is true, for example "Sam rents two tents
  on 6 October";
- **logic**: what is recorded and how its numbers are calculated, for example
  "the number of tents currently rented is the number that went out minus the
  number that came back".

In most systems, the two are mixed together inside code and tables made by one
builder. As a result, parts made by different people are hard to combine, old
data breaks when the system changes, and an organization's knowledge is locked
into one piece of software.

The Uniti Standard separates the two and gives both **one shared form**, so
that:

1. content made by anyone can be used together with content made by others
   without conflict;
2. facts are never lost and never corrupted, whatever changes;
3. humans and machines, including AI, can read, check, and compose content
   from any domain in the same way.

This standard starts from the needs of the **enterprise**, but its form is not
limited to the enterprise. The direction is one form for the knowledge of any
organization.

## 2. Scope

**What this standard governs:**
- the form of facts, addresses, values, concepts, relations, calculation
  rules, change, proof, and ownership (part A);
- the rules for entry into the shared vocabulary, the form of concept cards,
  and the outside code lists that are used (part B);
- the content of the first shared vocabulary (part B).

**What it does not govern:**
- content specific to one domain or one organization (that belongs to
  modules);
- software, databases, programming languages, and storage formats;
- display, screens, and the way people interact;
- security, access rights, and how to enter the system (to be covered later,
  separately).

## 3. Three layers

| Layer | Analogy | Contents | Nature |
|---|---|---|---|
| **Form** | Grammar | The way to record anything. Contains no domain concept at all | Fixed. Only grows, very rarely |
| **Vocabulary** | Shared words | Concepts needed by many organizations in many domains, for example party and transaction | Flexible. Grows according to the rules for entry into the vocabulary |
| **Module** | Story | The concepts and logic of one field or one organization, for example equipment rental or a clinic schedule | Free. Written by anyone |

The form is the only layer that is standardized strictly. The vocabulary and
modules are **content**, and content is always written in the form.

## 4. Principles

**P1. Fixed form, free content.**
What is standardized is the form. The content may be anything: following an
outside standard, made by oneself, or both, as long as it is written in this
form.

**P2. The form contains no content.**
No concept belonging to one domain is in part A, however small. If an idea
makes sense only for some domains, its place is in the vocabulary or a module.

**P3. The smallest possible form.**
Something enters the form only if, without it, facts cannot be recorded
correctly, or content from different builders cannot be used together. The
smaller the form, the smaller the chance of error, and the longer it lasts.

**P4. Grow only by adding.**
The form, the vocabulary, and modules change only by adding: a new version, a
new rule, a new concept. What already exists is never edited or deleted. An old
meaning stays valid for everything recorded with that meaning.

**P5. Facts are never lost.**
Facts are only added. A correction and a retraction are new facts that point to
the old fact. What was known on any day can always be read back.

**P6. No conflicts, because it is designed that way.**
Every entity has a unique address that contains its owner. Two builders who use
the same name never collide. Two different pieces of content for the same
entity can live side by side and be connected, without one of them having to
lose.

**P7. Every piece of content has an owner.**
Only the owner can write content under its address. Others who need a change
can propose it, copy it to their own address, or add a note in their own
module.

**P8. Use what exists before making your own.**
Code lists that are already standard are used directly. A concept that has an
equivalent in an outside standard names that equivalent. A new concept is made
only when nothing suitable exists. (Details in §5.)

**P9. Every piece of content proves itself.**
Logic carries examples: some facts and the results that must come out of them.
Content is accepted only when all its examples are proven.

**P10. Readable by humans and machines.**
Every concept has a definition in human language and a label in the language
of its users. Every rule, where possible, can be checked by a machine. A form
that only one of the two can understand is considered unfinished.

**P11. Independent of implementation.**
The standard does not depend on any software, database, or storage format.
Software that conforms to the standard can be made by anyone.

**P12. Universal must be tested, not claimed.**
Every form is tested with several different domains before it is declared
stable. A form that fits only one domain is not yet universal.

## 5. Three ways to relate to outside standards

| Kind | Stance | Example |
|---|---|---|
| A **code list** that is already standard | **Used directly**, not made again | currency, unit, country, and language codes |
| A **concept** that has an equivalent | **Owned by Uniti**, with a **bridge** to its equivalent | the concept "party" names its equivalent in another standard |
| A **thing that has no standard yet** | **Owned entirely by Uniti**, explained in this standard | the form of versioned change, examples as contracts |

A bridge does not make Uniti depend on the outside standard. If the outside
standard changes or disappears, the Uniti concept still means the same.

## 6. Requirement keywords

The rules in this standard use the following five words, written in capital
letters when used as rules:

| Word | Meaning |
|---|---|
| **MUST** | Must be met, without exception |
| **MUST NOT** | Forbidden, without exception |
| **SHOULD** | Met unless there is a strong reason that is recorded |
| **SHOULD NOT** | Avoided unless there is a strong reason that is recorded |
| **MAY** | Permitted, not required |

The words follow the convention of international standard documents (RFC
2119).

## 7. Conforming to the standard

- **Content** (a vocabulary or a module) conforms to the Uniti Standard if it
  is written in the form of part A and meets all the MUST and MUST NOT rules
  there.
- **Software** conforms to the Uniti Standard if it accepts content that
  conforms to the standard, rejects content that does not, and upholds all the
  rules of part A for the facts it stores.

The way to prove conformance, a set of tests that anyone can run, is set in
[`form/08-proof.md`](form/08-proof.md) §2.9. The content of the tests is
written when v0.1 is locked
([`decisions/0052-quick-test-then-lock.md`](decisions/0052-quick-test-then-lock.md)).
