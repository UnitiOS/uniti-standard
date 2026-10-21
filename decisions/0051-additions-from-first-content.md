# 0051. Additions from the first content

Date: 2026-10-20
Status: accepted

**Context**
Stage 6 wrote the first content ([`content/README.md`](../content/README.md)):
card templates, code lists, the calculation library, and the first
vocabulary. This is the first time modules were written in the full form,
that is, the form for modules that will be frozen (NOTATION-17). The
reference calculator gained a check of the full form,
`calculator/completeness.py`.

The code list was decided in 0050. While writing the other content, one gap
was found that passed the findings gate (0046):

- **I5. The required parts of a choice list card are not stated.** The
  required parts of the concept card, property card, computed property, and
  constraint are already stated (CONCEPT-1, CONCEPT-3, CALC-4, and CALC-37).
  For choice lists no rule states them. This gap appeared when writing
  `PaymentMethod` in the vocabulary and `RoundingMode` and `RemainderRule`
  in the library. As a result, two implementations could disagree about
  whether a module may be frozen.

**Decision**
1. A **choice list card** must contain an address, a label, and a definition,
   like a property card. The rule is VALUE-19. A choice written inside its
   list has no card, so it has no required parts.
2. The reference calculator now checks two rules that already exist:
   - a choice from another module may enter only an open list (VALUE-13);
   - a property may be declared required only by the owner of its concept
     (CONCEPT-8).
3. Postponed under 0046, because no case needs them yet:
   - bridges for choice lists. Appendix A provides bridges for concept
     cards, property cards, and choices with the header line
     `choice … to …`, but not for lists. RELATION-11 is only a
     recommendation, so nothing is held up;
   - the version of content modules. All content modules have version v0
     until they are frozen in stage 7.

The following findings are content, and are written directly in the
vocabulary:
- the amount of a payment is **no direction**, because the same payment is
  money going out for the payer and money coming in for the recipient. The
  loan cases write it `decrease`, while the clinic cases write it
  `increase`;
- Item is **one kind of item**, not one physical thing. All the inventory,
  rental, and manufacturing cases use it that way.

One example fix (I3): the vocabulary addresses in the form documents are
made the same as the first vocabulary, `uniti/item/Item` and
`uniti/common/name`.

**Alternatives**
- *A list card needs only a label.* Rejected: the definition is the part that
  readers from other organizations need most, and the property card already
  requires both.
- *Every choice must also have a label.* Rejected: a choice inside a list has
  no card, and adding a way to write it would mean adding to the form (see
  0049, L3).

**Consequences**
- `form/03-values.md` §2.6 and §3: VALUE-19.
- `content/card-templates.md`: the choice list card.
- `content/calc.md`: the library is written in the full form, and its lists
  are given definitions.
- `form/06-calculation-rules.md` §2.11 and `appendix/A-notation.md` §2.5:
  vocabulary addresses in the examples.
