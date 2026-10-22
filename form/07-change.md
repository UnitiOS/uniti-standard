# Change

Status: draft

> [Uniti Standard](../README.md) › Part A: form, 7 of 8
> · Previous: [Calculation rules](06-calculation-rules.md)
> · Next: [Proof](08-proof.md) · [Rules CHANGE-n](../rules.md#change)

## 1. Purpose

Content always evolves: modules get new concepts, calculation rules are
corrected, old concepts are replaced. The change form makes sure content can
keep changing without ever breaking facts that are already recorded and
without breaking other content that uses it.

This document governs changes to **content**. Changes to **facts** are
governed in [`01-facts.md`](01-facts.md) §2.3.

## 2. Definitions

### 2.1 Draft and version

A module has two states:

| State | Meaning |
|---|---|
| **Draft** | Content that is being written. Not yet part of the ecosystem: it must not be referred to and must not be used to record facts |
| **Version** | Content that has been **frozen**. It never changes again, forever |

Versions are given a simple sequence number: 1, 2, 3, and so on. Every version
records its number, when it was frozen, by whom, and the previous version.

### 2.2 Kinds of change between versions

The kind of change between two versions is **computed by a machine**, by
comparing the two address by address. Authors do not state it themselves.

| Kind | Meaning | Example |
|---|---|---|
| **Addition** | An address that did not exist in the previous version | a new property "promised return date" |
| **Modification** | The same address, with a different remark or rule, without changing its meaning | a new label, a clearer description, a corrected calculation rule |
| **Deprecation** | An address that is marked as no longer recommended | an old concept with its replacement |

**There is no kind "delete".** An address that has been frozen stays in every
later version, at most marked deprecated. When the meaning of an address
changes fundamentally, a new address is made
([`02-addresses.md`](02-addresses.md), ADDRESS-9). Which changes to concepts,
properties, and choice lists change the meaning is detailed in
[`04-concepts.md`](04-concepts.md) §2.9.

The kind of change shows **what** changed. Its **effect** on numbers is shown
by examples: examples from the old version are run again, and those that do
not pass are reported as a **behavior change**
([`08-proof.md`](08-proof.md) §2.7).

### 2.3 Deprecated

A concept, property, choice, or a whole module may be marked **deprecated**,
naming its replacement if there is one. Facts already recorded with it can
still be read. New content is directed to the replacement.

### 2.4 Withdrawn

A version may be marked **withdrawn** if a serious error is found, for example
a calculation rule that produces wrong numbers. A withdrawn version:

- can no longer be used by new content, and can no longer be installed;
- can still be read, and so can all facts already recorded with it.

Marking as deprecated and withdrawing are **recorded statements by the
owner**, not edits to the version. The version itself stays unchanged.

### 2.5 Using other modules

A module that uses another module names its **exact version**. A new version
of the module that is used changes nothing until its user itself freezes a new
version that names that version.

An organization installs **one version of each module**, counting the modules
that its installed modules use. If the cashier module uses `uniti/item@v2`
while the warehouse module still uses `uniti/item@v1`, it is not clear which
version calculates a property of an item, so the installation that would make
two versions is refused, naming both. The organization waits until both
modules use the same version.

A module whose content is used by facts that are already recorded **cannot be
uninstalled**, because those facts must stay readable, for example for an
audit. The organization may move to another version of it, or keep it
installed and stop recording with it
([`decisions/0057`](../decisions/0057-closure-before-lock.md)).

### 2.6 Facts and versions

Every fact names the version used when it was stated (*version used*,
[`01-facts.md`](01-facts.md)). Because addresses do not change between
versions, facts recorded with an old version are still read by the new version
without having to be moved or changed.

## 3. Rules

**Versions**

- **CHANGE-1.** A version that has been frozen MUST NOT be changed or deleted.
- **CHANGE-2.** Version numbers MUST be in sequence starting from 1, without
  gaps, and MUST NOT be reused.
- **CHANGE-3.** Every version MUST record its number, the time it was frozen,
  who froze it, and the previous version.
- **CHANGE-4.** A draft MUST NOT be referred to by other content and MUST NOT
  be used to record facts.

**Kinds of change**

- **CHANGE-5.** The kind of change between two versions MUST be computed by
  comparing the two, not stated by the author.
- **CHANGE-6.** Every address that exists in a version MUST still exist in
  every later version.
- **CHANGE-7.** A change that changes the meaning of an address MUST NOT be
  made at that address. A new address MUST be made.

**Deprecated and withdrawn**

- **CHANGE-8.** The markers for deprecated and withdrawn MUST be recorded
  statements by the owner, and MUST NOT change the content of the version.
- **CHANGE-9.** A deprecation marker SHOULD name its replacement.
- **CHANGE-10.** New content SHOULD NOT use a deprecated address.
- **CHANGE-11.** A withdrawn version MUST NOT be used by new content and MUST
  NOT be installed again.
- **CHANGE-12.** The withdrawal of a version MUST state its reason.
- **CHANGE-13.** Facts recorded with a deprecated or withdrawn version MUST
  stay readable.

**Using other modules**

- **CHANGE-14.** A module MUST name the exact version of every module it uses.
- **CHANGE-15.** A new version of a module that is used MUST NOT change the
  behavior of its users until the user freezes a new version that names it.
- **CHANGE-16.** An organization MUST have at most one version of each module
  installed, counting the modules that its installed modules use. An
  installation that would make two versions MUST be refused, naming both.
- **CHANGE-17.** A module whose content is used by recorded facts MUST NOT be
  uninstalled.

## 4. Examples

**Equipment rental.**
- Alex freezes `alex/rental` version 2, which adds the property "promised
  return date". The machine computes: one **addition**.
- The Happy Camp shop still uses version 1, and nothing changes for it. When
  the shop itself freezes a new version that names version 2, the old rentals
  can still be read, with the new property empty.

**Clinic.**
- The schedule module has a concept `Visit` that turns out to mix two things:
  an appointment and the arrival of a patient.
- Version 5 adds two new concepts, `Appointment` and `Arrival`, and marks
  `Visit` as **deprecated**, naming both as its replacements.
- Old visit records can still be read. New records use the new concepts.

**A withdrawn version.**
- Version 7 of the bookkeeping module turns out to add up tax twice.
- Its owner withdraws version 7 with the reason "tax counted twice", and then
  freezes version 8.
- An organization that has not installed version 7 cannot install it anymore.
  An organization that has installed it can still read its records, and is
  told that its version is withdrawn.

## 5. Non-examples

- **Fixing a typo in version 3, which has been frozen.** The fix becomes
  version 4.
- **Deleting a property that is no longer used from a later version.** The
  property stays and is marked deprecated.
- **Changing the meaning of the property "price" from price before tax to
  price after tax at the same address.** That is a new address.
- **Using the "latest version" of another module.** What is named is always the
  exact version.

## 6. Rationale

- **Sequence numbers, kinds of change computed by a machine.** Authors can be
  wrong in stating whether their change is safe; the result of a machine
  computation cannot. Sequence numbers are also easy for anyone to understand.
  ([`decisions/0012`](../decisions/0012-versions-deprecated-withdrawn.md))
- **No delete.** Other content and facts already recorded depend on existing
  addresses. Deleting them means breaking something outside the author's
  control.
- **Deprecated and withdrawn as statements.** The version stays unchanged, but
  the ecosystem can still be told that something is no longer recommended.
- **Exact version.** An organization must not experience a change in behavior
  that it never agreed to.

## 7. Outside standards

| Part | Counterpart |
|---|---|
| A version that does not change | tagged releases in software package systems |
| Deprecated with a replacement | `owl:deprecated` (W3C), the *deprecated* marker in npm |
| Withdrawn without being deleted | *yank* in Cargo (Rust) and *yanked release* in PyPI (Python) |
| Kinds of change | *Semantic Versioning*, but here computed by a machine, not stated by the author |

## 8. Open questions

1. **Where the deprecated and withdrawn markers are recorded.** These
   statements need a record owned by the ecosystem, not by one organization.
   Discussed together with ownership in v0.2 ([`decisions/0048`](../decisions/0048-ownership-to-v02.md)) and the discussion about the ecosystem.
2. **Change of the form itself.** How the Uniti Standard changes its version is
   governed in v0.2 ([`decisions/0048`](../decisions/0048-ownership-to-v02.md)).
