# Rules index

Status: generated; not normative

221 rules in 9 documents.

Every rule of the form documents and of appendix A, in reading order.
Each line shows the rule's ID, the requirement keywords it uses, and its
first sentence, with "…" when the rule says more. The rule itself is
the text in its document, which may hold more sentences, exceptions,
and examples: read it there before relying on a rule.

This file is made by `reference/tools/rules_index.py`. Do not edit it by
hand; a test fails when it no longer matches the documents.

## [Facts](form/01-facts.md#3-rules)

25 rules.

**Facts**

| Rule | Keywords | First sentence |
|---|---|---|
| FACT-1 | MUST | A fact MUST have an identifier, subject, property, valid time, fact kind, version used, and action. |
| FACT-2 | MUST, MUST NOT | A fact MUST state exactly one value when its kind is statement, replacement, or correction, and MUST NOT state a value when its kind is ending, retraction, or redaction. |
| FACT-3 | MUST, MUST NOT | A fact that is already recorded MUST NOT be changed or deleted. … |
| FACT-4 | MUST NOT | A computed value MUST NOT be recorded as a fact. |

**Entity**

| Rule | Keywords | First sentence |
|---|---|---|
| FACT-5 | MUST, MUST NOT | The identifier of an entity MUST be unique in the whole world, permanent, and meaningless. … |
| FACT-6 | MUST | A code that has meaning for humans MUST be recorded as a property, not as an identifier. |
| FACT-7 | MUST | Every entity MUST have a type fact that states the concept it belongs to. |

**Fact kind and target**

| Rule | Keywords | First sentence |
|---|---|---|
| FACT-8 | MUST | The fact kind MUST be one of: statement, replacement, ending, correction, retraction, redaction. |
| FACT-9 | MUST | A fact whose kind is not statement MUST name exactly one target, which is a fact that is already recorded before it, with the same subject and property. |
| FACT-10 | MUST | The valid time of a replacement or ending MUST be later than the valid time of its target. … |
| FACT-11 | MUST | A correction MUST target a fact that has a value. … |
| FACT-12 | MUST, MUST NOT | If the subject or property of a fact is wrong, that fact MUST be retracted and the right fact recorded as a new statement. … |
| FACT-13 | MUST NOT | A retraction MUST NOT target another retraction. … |
| FACT-14 | MUST, MUST NOT | For a property that holds only one value at one time, a new value MUST be a replacement that targets the value in force at the valid time of that replacement, or a correction of the wrong fact, not a second statement. … |

**Time**

| Rule | Keywords | First sentence |
|---|---|---|
| FACT-15 | MUST, MUST NOT | The recorded time MUST be given by the recorder at the moment the action is recorded, and MUST NOT be filled in by the actor. |
| FACT-16 | MAY | The valid time MAY be in the past or in the future. |
| FACT-17 | MUST | Reading at two times MUST follow the steps in §2.5. |

**Action and provenance**

| Rule | Keywords | First sentence |
|---|---|---|
| FACT-18 | MUST | Every fact MUST be recorded by exactly one action, and all facts in one action MUST be recorded together or not at all. |
| FACT-19 | MUST | Every action MUST have an actor, recorded time, and source. |
| FACT-20 | MUST | If the actor is not responsible alone for its action, for example an AI or a machine acting for someone else, the action MUST name an approver. |
| FACT-21 | MUST | An action that corrects, retracts, or redacts MUST name a reason. |
| FACT-22 | SHOULD | An action SHOULD have an action name in human words. |

**Redaction [provisional]**

| Rule | Keywords | First sentence |
|---|---|---|
| FACT-23 | MUST, MUST NOT | A redaction MUST target a fact whose property is marked as personal data. … |
| FACT-24 | MUST NOT | A redaction MUST NOT be retracted or corrected. |
| FACT-25 | MUST, MUST NOT | After a redaction, the value of its target MUST NOT be readable by anyone, while the other parts of that fact MUST remain readable. |

## [Addresses](form/02-addresses.md#3-rules)

15 rules.

**Structure**

| Rule | Keywords | First sentence |
|---|---|---|
| ADDRESS-1 | MUST | Every module, concept, property, choice list, choice, calculation rule, and example MUST have an address with the structure `‹root›/‹owner›/‹module›/‹name›`, except the addresses of an owner and of a module, which stop at their own part. |
| ADDRESS-2 | MUST | The parts of an address MUST use letters according to §2.4. |
| ADDRESS-3 | MUST | Within one module, every ‹name› MUST be unique among all of its concepts, properties, choice lists, choices, calculation rules, and examples. |
| ADDRESS-4 | MUST NOT | An address MUST NOT contain a version number. |

**Uniqueness and ownership**

| Rule | Keywords | First sentence |
|---|---|---|
| ADDRESS-5 | MUST | The name of an owner MUST be unique in the whole ecosystem. … |
| ADDRESS-6 | MAY | Only the owner MAY create addresses under its name. |
| ADDRESS-7 | MUST NOT | The owner names `standard`, `uniti`, and `example` are reserved, and MUST NOT be registered by other parties. |

**Permanence**

| Rule | Keywords | First sentence |
|---|---|---|
| ADDRESS-8 | MUST NOT | An address that is already frozen in a version MUST NOT be deleted, and MUST NOT be reused for another meaning. |
| ADDRESS-9 | MUST, MAY | If the meaning of a concept or property changes fundamentally, a new address MUST be created. … |
| ADDRESS-10 | MUST | Changing how a concept or property is called by humans MUST be done through a label, not by changing its address. |

**Version reference**

| Rule | Keywords | First sentence |
|---|---|---|
| ADDRESS-11 | MUST, MUST NOT | A reference to a version MUST be a module address and one exact version number. … |

**Opening an address**

| Rule | Keywords | First sentence |
|---|---|---|
| ADDRESS-12 | SHOULD | An address SHOULD be openable, by humans and by machines, to show the card of its content: definition, label, owner, and its versions. |

**Root**

| Rule | Keywords | First sentence |
|---|---|---|
| ADDRESS-13 | MUST | Addresses in facts, modules, and the vocabulary MUST be stored and written without the ‹root›. |
| ADDRESS-14 | MUST | An implementation MUST treat the ‹root› as one value for the whole ecosystem, and put it on only when an address is written in full. |
| ADDRESS-15 | MUST NOT, MAY | **[provisional]** The ‹root› is `https://uniti.example`. … |

## [Values](form/03-values.md#3-rules)

19 rules.

**Value types**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-1 | MUST | Every value MUST be one of the seven value types in §2.1. |
| VALUE-2 | MUST | Every value MUST match the value type of its property. |
| VALUE-3 | MUST, MUST NOT | The list of value types MUST NOT be extended by content. … |

**Numbers**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-4 | MUST, MUST NOT | Numbers MUST be stored and computed as exact numbers. … |
| VALUE-5 | MUST, MUST NOT | When a number property sets a quantity, every one of its values MUST carry a unit of that quantity. … |
| VALUE-6 | MUST | Quantities and units MUST be taken from a code list. … |
| VALUE-7 | MUST, MUST NOT | Conversion between units MUST NOT be done silently. … |

**Time**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-8 | MUST, MUST NOT | An instant MUST contain its time zone. … |
| VALUE-9 | MUST | A valid time MUST be a date or an instant. … |
| VALUE-10 | MUST | Every organization that records facts MUST have one default time zone. … |

**Text**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-11 | MUST | A language code, when used, MUST follow BCP 47. |

**Choices**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-12 | MUST | Every choice list MUST be declared open, closed, or a code list. … |
| VALUE-13 | MUST NOT | A choice MUST NOT be added by other parties to a closed list. |
| VALUE-14 | MUST | The value of a choice MUST be the address of a choice that goes into the list used by its property, from an installed module. |
| VALUE-15 | MUST NOT, MAY | A closed list MAY be opened in a later version. … |
| VALUE-19 | MUST | Every choice list MUST have a card with an address, label, and definition. |

**References**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-16 | MUST | A reference value MUST be the identifier of an entity, and that entity MUST belong to the concept that its property refers to, or to a child concept of it, at the valid time of the reference fact, according to what is known when the action is recorded. … |

**Direction**

| Rule | Keywords | First sentence |
|---|---|---|
| VALUE-17 | MUST | Every number property MUST state one direction: increase, decrease, no direction, or position. |
| VALUE-18 | MUST NOT | The value of a property whose direction is no direction MUST NOT be negative. |

## [Concepts and properties](form/04-concepts.md#3-rules)

22 rules.

**Cards**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-1 | MUST | Every concept MUST have a concept card with an address, a label, a definition, at least one include, and at least one exclude. |
| CONCEPT-2 | MUST | A concept in the vocabulary MUST give includes and excludes from at least two different domains. |
| CONCEPT-3 | MUST | Every property MUST have a property card with an address, a label, a definition, a value type, a number of values, and a personal data marker. |
| CONCEPT-4 | MUST | A reference property MUST name exactly one concept referred to. … |
| CONCEPT-5 | MUST, MUST NOT, MAY | A quantity MAY be stated only for number properties. … |

**Applies to**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-6 | MUST NOT | A fact that states a value MUST NOT use a property that does not apply to any type of its subject at the valid time of that fact, or to its parent, except the base property of type. … |
| CONCEPT-7 | MAY | The statement that a property applies to a concept MAY be written by anyone in their own module, and only applies to an organization that installs that module. |
| CONCEPT-8 | MAY | A property MAY be declared required for a concept only by the owner of that concept. |

**Child concepts**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-9 | MAY | A concept MAY have at most one parent. |
| CONCEPT-10 | MUST NOT | The chain of parents MUST NOT loop back to its original concept. |
| CONCEPT-11 | MUST | Every property that applies to the parent MUST also apply to its child, and a property that is required at the parent MUST stay required at its child. |
| CONCEPT-12 | MUST | An entity that belongs to a concept MUST be considered to belong also to all its parents. |

**Type and role**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-13 | SHOULD, SHOULD NOT | A role SHOULD NOT be made a concept that becomes the type of an entity. … |
| CONCEPT-14 | MUST NOT, MAY | A type fact MUST NOT be replaced or ended. … |
| CONCEPT-15 | MUST NOT, SHOULD | An entity SHOULD have one type. … |

**Label**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-16 | MUST | Every label MUST carry a language code. |
| CONCEPT-17 | MUST | For each language, a concept, property, choice list, or choice MUST have at most one main label. |

**Check per action**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-18 | MUST | After all facts in an action are taken into account, every entity that is the subject of a fact in that action MUST have a valid value for every property that is required for its type, at every time that the action touches for that entity (§2.7), unless at that time the entity already had that type and no value for that property before the action. |
| CONCEPT-19 | MUST | An action that does not meet CONCEPT-6, CONCEPT-18, or VALUE-16 MUST be rejected as a whole. |

**Personal data [provisional]**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-20 | MUST | Every property card MUST state whether its value is personal data. |

**Change**

| Rule | Keywords | First sentence |
|---|---|---|
| CONCEPT-21 | MUST NOT | A change that changes the meaning according to §2.9 MUST NOT be made at the same address. |
| CONCEPT-22 | MUST | Making a property required MUST be reported separately by the machine that computes the kinds of change. |

## [Relations](form/05-relations.md#3-rules)

12 rules.

**The relation list**

| Rule | Keywords | First sentence |
|---|---|---|
| RELATION-1 | MUST | Every relation between content MUST be one of the relations in §2.2. |
| RELATION-2 | MUST NOT | Content MUST NOT add to the relation list. |

**Who may state them**

| Rule | Keywords | First sentence |
|---|---|---|
| RELATION-3 | MUST | A relation MUST be stated by the party named in §2.3, in their own module. |
| RELATION-4 | MUST NOT | A relation MUST NOT change the content it points to. |
| RELATION-5 | MUST | A relation MUST apply only to an organization that installs the module in which the relation is written. |

**Structural**

| Rule | Keywords | First sentence |
|---|---|---|
| RELATION-6 | MUST | The source side and the target side of a structural relation MUST match the "from → to" column in §2.2. |
| RELATION-7 | MUST | A structural relation MUST point to the exact version of the module that owns its target content (`07-change.md`, CHANGE-14). |

**Bridges**

| Rule | Keywords | First sentence |
|---|---|---|
| RELATION-8 | MUST | A bridge MUST point to a permanent address. … |
| RELATION-9 | MUST NOT | A bridge MUST NOT be used to create, change, or reject facts. |
| RELATION-10 | SHOULD | A bridge SHOULD come with a note about the difference in meaning if its kind is similar, broader, or narrower. |
| RELATION-11 | SHOULD | Content in the vocabulary SHOULD have a bridge to an outside standard if a counterpart exists (`00-principles.md`, P8). |
| RELATION-12 | MUST | A bridge MUST connect content of the same kind: concept with concept, property with property, or choice with choice. |

## [Calculation rules](form/06-calculation-rules.md#3-rules)

58 rules.

**Kinds**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-1 | MUST | A calculation rule MUST produce only derived numbers. … |
| CALC-2 | SHOULD | An action that records an estimate SHOULD state the confidence level. |

**Kinds of rules**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-3 | MUST | Every calculation rule MUST be a computed property, helper, constraint, or contribution, and MUST have an address. |
| CALC-4 | MUST | A computed property MUST have a property card, exactly one rule, and a declaration of open or closed. … |
| CALC-5 | MUST NOT | The value of a computed property MUST NOT be stated as a fact. |
| CALC-6 | MUST | A computed property MUST be readable in the same way as a recorded property, at (*T*, *R*). |
| CALC-7 | MUST NOT, MAY | A helper MUST NOT be read as a property. … |
| CALC-8 | MUST, MUST NOT | The value of a computed property MUST be one of the seven value types, according to its property card. … |

**Operations and levels**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-9 | MUST | A rule MUST use only the core operations in §2.5 and other calculation rules, including helpers in the calculation library. |
| CALC-10 | MUST NOT | The core operations MUST NOT be added to by content. … |
| CALC-11 | MUST | The level of a rule MUST be calculated by the machine from the operations it uses, including operations in other rules that it reads. |
| CALC-12 | MUST, MUST NOT | A rule that uses itself, directly or through other rules, MUST do so only for another entity, at the same *T* and *R*, with the same parameters. … |
| CALC-13 | MUST | Recursion that returns to the same entity before it is finished MUST produce not computable because of a cycle, together with its chain. |

**Certainty**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-14 | MUST | From the same facts, module set, parameters, *T*, and *R*, the result of a rule MUST always be the same. |
| CALC-15 | MUST NOT | A rule MUST NOT read any time other than *T*, a time derived from *T* or from facts, and a time written in the rule. |
| CALC-16 | MUST NOT | A rule MUST NOT read facts as of another *R*, and MUST NOT record or change facts. |
| CALC-17 | MUST | A rule MUST use only content from its own module and from the modules it uses with an exact version. |
| CALC-18 | MUST | `fold` over a collection with no order MUST name `order_by`. … |
| CALC-19 | MAY | An implementation MAY calculate in any way, as long as the result is exactly the same as the result according to this document. |

**Numbers and units**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-20 | MUST | Inside a rule, numbers MUST be calculated as exact fractions. |
| CALC-21 | MUST | The value of a computed property that is a number MUST be writable as a terminating decimal. … |
| CALC-22 | — | *Revoked (`decisions/0045`). The way of rounding is now content of the calculation library.* |
| CALC-23 | — | *Revoked (`decisions/0045`). Dividing without a remainder is now content of the calculation library.* |
| CALC-24 | MUST, MUST NOT | Addition, subtraction, and comparison MUST be only for numbers with the same unit. … |
| CALC-25 | MUST | An exchange rate MUST be taken from facts. |
| CALC-50 | — | *Revoked (`decisions/0045`). `percentile` is now content of the calculation library.* |
| CALC-55 | MUST, SHOULD | If the result of a computed property that has a quantity is a zero without a unit, the result MUST be not computable because of unit mismatch. … |
| CALC-56 | MUST | `floor_multiple(n, of: k)` MUST produce the largest multiple of `k` that is not more than `n`. `k` MUST be more than zero. … |

**Time**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-26 | MUST | A range MUST be read as half open: from its start up to before its end. |
| CALC-27 | SHOULD | A fact about an event SHOULD be valid from the time of the event. |
| CALC-53 | MUST | Months and years MUST be used only to shift a date and for the difference of two dates. … |
| CALC-54 | MUST | A computed property that is asked for an entity that at *T* does not belong to its concept MUST produce empty. |

**Empty and not computable**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-28 | MUST | A result that is not computable MUST name one reason kind from §2.9, a description in human language, and its location. |
| CALC-29 | MUST NOT | A result that is not computable MUST NOT be replaced with 0 or empty. |
| CALC-30 | MUST | If part of an expression that is calculated is not computable, the whole expression MUST be not computable, with the reason of that part. |
| CALC-51 | MUST, MUST NOT | `let` MUST be calculated only if its name is used, and a helper argument MUST be calculated only if it is used inside that helper. … |
| CALC-52 | MUST | If several parts are not computable, the reason reported MUST be the reason of the first part in calculation order in §2.9. … |

**Direction**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-31 | MUST, SHOULD | The machine MUST report a mixing of directions according to §2.10 before a rule is frozen. … |

**Open and contributions**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-32 | MUST NOT | A contribution MUST NOT be added to a closed computation. |
| CALC-33 | MUST | A contribution MUST produce the same value type, quantity, and direction as the computation it contributes to. |
| CALC-34 | MUST | The way of combining contributions MUST be one of: `sum`, `min`, `max`, `all_match`, `any_match`. |
| CALC-35 | MUST | A contribution MUST apply only to organizations that install the module of its contributor. |
| CALC-36 | MUST NOT | An open computation MUST NOT be closed. |
| CALC-49 | MUST NOT | `contributions` MUST NOT be used outside the rule of an open computed property. |

**Constraints**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-37 | MUST | A constraint MUST have a card with an address, a label, a definition, the one concept it applies to, a yes/no rule, and a rejection message. |
| CALC-38 | MUST | A constraint MUST be checked per action, for the entities and at the times in §2.12 steps 1 and 2. … |
| CALC-39 | MUST | A constraint that is not computable, or whose result is empty, MUST be treated as not met. |
| CALC-40 | MUST NOT | `before_action`, `this_action.actor`, and `this_action.approver` MUST NOT be used outside constraints. |
| CALC-57 | MUST | A constraint that uses `before_action` or `this_action` MUST be read only for the entities touched by the action, at the times touched by the action, and its value before the action MUST be taken as not existing. |
| CALC-58 | MUST | Actions MUST be checked and recorded one at a time, in the order in which they are recorded. … |
| CALC-41 | MUST | Every rejection MUST name the constraint and its address, its source module with the exact version, the entity and valid time where the constraint failed, and its rejection message. |

**Rejection record**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-42 | MUST | Every action that is rejected MUST be recorded as a rejection record with the parts in §2.13. |
| CALC-43 | MUST NOT | A rejection record MUST NOT be read as a fact and MUST NOT affect a computed value. |

**Computed value and projection**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-44 | MUST | Every computed value MUST name the parts in §2.14, and its trace MUST be possible to show on request. |
| CALC-45 | MUST, MAY | A projection MUST name the last fact that has been taken into account. … |
| CALC-46 | MUST | If a projection differs from a recalculation from the facts, the calculation from the facts MUST be the one used. |
| CALC-47 | MUST, SHOULD | The reader of a projection MUST be able to know its *R*, and SHOULD be told if any fact has been recorded after it. |

**Reported results**

| Rule | Keywords | First sentence |
|---|---|---|
| CALC-48 | SHOULD | A result reported outside SHOULD be recorded as a fact about the report, naming the computed property, parameters, *T*, and *R* it came from. |

## [Change](form/07-change.md#3-rules)

17 rules.

**Versions**

| Rule | Keywords | First sentence |
|---|---|---|
| CHANGE-1 | MUST NOT | A version that has been frozen MUST NOT be changed or deleted. |
| CHANGE-2 | MUST, MUST NOT | Version numbers MUST be in sequence starting from 1, without gaps, and MUST NOT be reused. |
| CHANGE-3 | MUST | Every version MUST record its number, the time it was frozen, who froze it, and the previous version. |
| CHANGE-4 | MUST NOT | A draft MUST NOT be referred to by other content and MUST NOT be used to record facts. |

**Kinds of change**

| Rule | Keywords | First sentence |
|---|---|---|
| CHANGE-5 | MUST | The kind of change between two versions MUST be computed by comparing the two, not stated by the author. |
| CHANGE-6 | MUST | Every address that exists in a version MUST still exist in every later version. |
| CHANGE-7 | MUST, MUST NOT | A change that changes the meaning of an address MUST NOT be made at that address. … |

**Deprecated and withdrawn**

| Rule | Keywords | First sentence |
|---|---|---|
| CHANGE-8 | MUST, MUST NOT | The markers for deprecated and withdrawn MUST be recorded statements by the owner, and MUST NOT change the content of the version. |
| CHANGE-9 | SHOULD | A deprecation marker SHOULD name its replacement. |
| CHANGE-10 | SHOULD NOT | New content SHOULD NOT use a deprecated address. |
| CHANGE-11 | MUST NOT | A withdrawn version MUST NOT be used by new content and MUST NOT be installed again. |
| CHANGE-12 | MUST | The withdrawal of a version MUST state its reason. |
| CHANGE-13 | MUST | Facts recorded with a deprecated or withdrawn version MUST stay readable. |

**Using other modules**

| Rule | Keywords | First sentence |
|---|---|---|
| CHANGE-14 | MUST | A module MUST name the exact version of every module it uses. |
| CHANGE-15 | MUST NOT | A new version of a module that is used MUST NOT change the behavior of its users until the user freezes a new version that names it. |
| CHANGE-16 | MUST | An organization MUST have at most one version of each module installed, counting the modules that its installed modules use. … |
| CHANGE-17 | MUST NOT | A module whose content is used by recorded facts MUST NOT be uninstalled. |

## [Proof](form/08-proof.md#3-rules)

32 rules.

**Form of an example**

| Rule | Keywords | First sentence |
|---|---|---|
| PROOF-1 | MUST | Every example MUST be one of three kinds: compute, accept, or reject. |
| PROOF-2 | MUST | Every example MUST have an address, kind, title, explanation, facts, expected result, and status. |
| PROOF-3 | MUST | A compute example MUST name the computed property, entity, parameters if any, *T*, and *R*. |
| PROOF-4 | MUST | Accept and reject examples MUST name the action that is tried. … |
| PROOF-5 | MUST | The expected result MUST be compared exactly according to §2.4. |
| PROOF-32 | MUST | A reject example MUST pass only if every rejection comes from the constraint or form rule that is named, and, if an entity or valid time is named, at least one rejection is at that entity and time. |
| PROOF-6 | MUST | An example MUST be run with the module set of its own version. |

**Entities and data inside an example**

| Rule | Keywords | First sentence |
|---|---|---|
| PROOF-7 | MUST | Entities inside an example MUST use local ids. … |
| PROOF-31 | MUST | The identifiers given to local ids MUST be in the order of their local ids, compared character by character by Unicode code point. |
| PROOF-8 | MUST NOT | The facts of an example MUST NOT mix with real facts, and real facts MUST NOT be read by an example. |
| PROOF-9 | MUST NOT | An example MUST NOT hold real personal data. |
| PROOF-10 | MUST | Facts inside an example MUST name their valid time and recorded time. … |
| PROOF-11 | SHOULD | The explanation of an example SHOULD be understandable to a person who is not a programmer. |
| PROOF-12 | SHOULD | The expected result SHOULD be computed without running the rule that is exemplified. |
| PROOF-29 | MUST | An example that does not name a default time zone MUST be run with the UTC zone. |
| PROOF-30 | MUST NOT | The starting facts of an example MUST NOT be checked by constraints or required properties. … |

**Obligation to have examples**

| Rule | Keywords | First sentence |
|---|---|---|
| PROOF-13 | MUST | Every computed property MUST have at least one compute example. |
| PROOF-14 | MUST | Every contribution MUST have at least one compute example that shows that contribution. |
| PROOF-15 | MUST | Every constraint MUST have at least one accept example and at least one reject example by that constraint. |
| PROOF-16 | MUST | In the vocabulary, the examples for every computed property, contribution, and constraint MUST come from at least two different domains. |
| PROOF-17 | SHOULD | A rule that can produce not computable SHOULD have an example for that result. |

**Freezing and between versions**

| Rule | Keywords | First sentence |
|---|---|---|
| PROOF-18 | MUST NOT | A version MUST NOT be frozen unless it meets §2.6. |
| PROOF-19 | MUST | An active example from the previous version MUST be run again with the new version. … |
| PROOF-20 | MUST, SHOULD | An example that is marked replaced MUST name a reason, and SHOULD name its replacement example. |
| PROOF-21 | MUST, MUST NOT | An example MUST NOT be deleted. … |
| PROOF-22 | MUST | The machine MUST report every example that is replaced because it failed as a behavior change, with the old result, the new result, and its reason. |
| PROOF-23 | SHOULD | The behavior change report SHOULD be shown to an organization before it installs the new version. |

**Between modules**

| Rule | Keywords | First sentence |
|---|---|---|
| PROOF-24 | MUST | Before a module freezes a version that uses a new version of another module, all of its examples MUST be run with that new version. |

**Conformance tests**

| Rule | Keywords | First sentence |
|---|---|---|
| PROOF-25 | MUST, MAY | Conformance tests MUST be written in the form of examples according to this document, and kept in `conformance/`. … |
| PROOF-26 | MUST | An implementation MUST state the level it supports. |
| PROOF-27 | MUST, MAY | An implementation MAY state that it conforms to the Uniti Standard only if it passes all conformance test examples according to §2.9. … |
| PROOF-28 | MUST | An implementation MUST refuse to install a module that holds a rule above its level, naming which rule. |

## [Appendix A. Notation](appendix/A-notation.md#3-rules)

21 rules.

**Standing**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-1 | MUST | Rules, examples, and cards in the standard documents and in the conformance tests MUST be written in the reference notation. |
| NOTATION-2 | MAY | Another format MAY be used if its meaning is exactly the same as the writing in the reference notation. |
| NOTATION-3 | MUST | If this appendix differs from a form document, the form document MUST be followed. |

**Characters and fixed values**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-4 | MUST, MUST NOT | Writing MUST use UTF-8, and calculation symbols MUST be written with the symbols in §2.2. … |
| NOTATION-5 | MUST | Decimals MUST be written with a point. … |
| NOTATION-6 | MUST | A date MUST state its year. |
| NOTATION-7 | MUST | An instant inside a rule MUST state its time zone. … |
| NOTATION-8 | MUST | A unit MUST be written with a code from the code list or a name in §2.4, singular or plural. … |

**Names**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-9 | MUST | A short name found in more than one module MUST be replaced with the full address. |
| NOTATION-10 | MUST NOT | A keyword in §2.5 MUST NOT be used as a local name or a rule name. |
| NOTATION-11 | MUST NOT | A local name MUST NOT be the same as the name of a choice visible from its module. |

**Expressions**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-12 | MUST, MUST NOT | An expression MUST be read according to the order in §2.6. … |
| NOTATION-13 | MUST | `if` MUST use `else`. |
| NOTATION-14 | MUST | `let` MUST occupy its own line. |
| NOTATION-15 | MUST | Every operation call MUST follow its call form in §2.7. |

**Modules and cards**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-16 | MUST | Every content writing MUST start with `module`, and MUST name every module it uses with its exact version. |
| NOTATION-17 | MUST, MAY | A module that will be frozen MUST use the full form for every card and rule. … |

**Examples**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-18 | MUST | Every fact in an example MUST be written on one line according to §2.9, with a valid time and a recorded time. |
| NOTATION-19 | MUST | A fact that is the target of another fact MUST be given a label. |
| NOTATION-20 | MUST | The expected result MUST be written in one of the ways in §2.9. |

**Files**

| Rule | Keywords | First sentence |
|---|---|---|
| NOTATION-21 | MUST | Writing inside Markdown that machines read MUST be in a code block tagged `uniti`. |
