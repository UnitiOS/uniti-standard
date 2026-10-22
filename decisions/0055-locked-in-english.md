# 0055. v0.1 is locked in English, in its own directory

Date: 2026-10-20
Status: accepted

**Context**
According to 0052 item 3, stage 8 locks, translates, and packages v0.1.
‹root› must be decided, and `keputusan/`, `kajian/`, and `uji/` remain in
Indonesian. The quick test added one more thing that the owner must decide:
the language for names read by machines
(Indonesian archive, `uji/03-uji-singkat.md`
§6.2).

Three things mean that the plan of 0052 needs to be made firm:

- **The domain for the root does not exist yet.** The first system must not
  wait for that domain.
- **Examples that can be run are written with the notation.** If names read
  by machines become English, the examples change too, although according to
  0052 `uji/` remains in Indonesian.
- **The standard must stand on its own.** The first system must not depend on
  the prototype repository.

**Decision**
1. **Temporary root.** Until the real domain exists, the root is
   `https://uniti.example`. Addresses are stored and written without the
   root. The root is attached only when an address is written in full. The
   root may be replaced once, before v0.1 is stable. After that the root must
   not change ([`form/02-addresses.md`](../form/02-addresses.md) §2.5,
   ADDRESS-13 to ADDRESS-15).
2. **Names read by machines use English.** This includes:
   - notation keywords;
   - choices of the form, for example direction and the kinds of numbers;
   - reserved owner names and the addresses of parts of the form;
   - names of modules, concepts, and properties in the vocabulary and the
     library;
   - names of card parts, kinds of example, and kinds of reason.

   All of them are set in one name table that the owner reviews before
   anything is translated. The words are chosen to be simple, so that people
   and agents can understand them easily. Where a term is already common in
   its field, that term is used.

   Names written by module makers remain free, as long as they use basic
   Latin letters. Labels remain per language, for example `label.en` and
   `label.id`. Notation in Indonesian is not kept. Notation in another
   language with exactly the same meaning may be added later
   ([`appendix/A-notation.md`](../appendix/A-notation.md) §8 item 2).
3. **One language, one text.** The English text becomes the only normative
   text, and the contents of the new directory are entirely in English.

   | Part | Fate |
   |---|---|
   | `00-principles`, `01-glossary`, `form/`, `appendix/`, `content/` | Translated |
   | Examples that can be run (`conformance/`) | Translated, and become conformance tests |
   | `decisions/` | Translated |
   | The reference calculator, including the names in its code | Translated |
   | Reports in `uji/` and `uji/periksa/` | Stay in the archive |
   | `kajian/` | Stays in the archive. Translated when v0.2 starts |
   | `PERUBAHAN.md` | Stays in the archive. Replaced by a new change log that starts from v0.1 |
4. **A translation does not correct.** The meaning must be exactly the same,
   and no information is lost. Every document is checked in two ways:
   - **Mechanical check.** Rule numbers, sections, tables and their rows,
     examples, and code blocks must be the same. All links must be alive.
   - **Comparison reading.** Done by an agent who is not the translator, and
     it looks only for meaning that changed or was lost.

   All examples are run again, and the results must be exactly the same.
   Findings are filtered with H1 to H4 (0052). What is not a blocker goes
   into the after-v0.1 list.
5. **A directory of its own.** The English standard is made in a git
   repository of its own, beside the prototype, and links to nothing outside
   itself. That repository starts clean. The old history stays in the
   prototype repository, and this folder is frozen as an archive.
6. **The package contains technical parts**, because this standard will
   become the reference for implementations:
   - **Implementation guide.** The data model and the steps in pseudocode for
     the rules that exist: reading facts, checking actions, and calculating.
     This guide only explains. If it differs, the normative text is correct.
   - **Conformance tests.** Grouped per level (`08` §2.9), with inputs,
     expected results, and a clear meaning of pass.
   - **Reference calculator** as an example implementation that can be run.
     It remains not part of the standard.
   - The machine exchange format (appendix A §8 item 3) remains postponed,
     because it is a new capability.

**Alternatives**
- *Wait for the domain before locking.* Rejected: the first system is delayed
  without limit. Because addresses are written without the root, replacing
  the root later is cheap.
- *Use an existing permanent address service, for example w3id.org, as a
  temporary root.* Rejected for now: it needs registration with an outside
  party, and if an own domain is used in the end, the root must still be
  replaced.
- *Names read by machines stay in Indonesian, and only the text is
  translated.* Rejected: this standard is for a cross-country ecosystem, and
  those names become permanent as soon as a fact records them.
- *Indonesian and English texts are maintained side by side.* Rejected: two
  normative texts mean two ways of reading (H1).
- *Test reports and studies are translated too.* Rejected for now: their
  content is history and discussion material, not rules. The living proof is
  in the conformance tests.
- *The old git history is carried into the new repository.* Rejected: that
  history is in Indonesian, and remains available in the prototype
  repository.

**Consequences**
- 0052 item 3 is partly replaced. `decisions/` is translated too, examples
  move to the conformance tests, while the `uji/` reports and `kajian/` stay
  in the archive.
- 0010: the root now exists, although temporary.
- `form/02-addresses.md`: §2.2, §2.5, ADDRESS-13 to ADDRESS-15, §6, and §8.
  `01-glossary`: Root. `README.md`: the [provisional] marker, the status
  **locked**, and the language.
- The tidy-ups R1, R2, R4, and R5
  (Indonesian archive, `uji/03-uji-singkat.md`
  §6.3) are done together with this decision, before translation:
  - **R1.** References to `09-ownership` become v0.2.
  - **R2.** The `uniti/*` modules become v1.
  - **R4.** The appendix A §4 example uses `item` from the vocabulary.
  - **R5.** 00 §7 follows 0052.
- The order of stage 8:
  1. this decision and the tidy-ups;
  2. the name table and the translation guide, reviewed by the owner;
  3. names in the notation, examples, and the reference calculator are
     replaced, and all tests must give the same results;
  4. translation;
  5. mechanical check and comparison reading;
  6. packaging;
  7. locked.
