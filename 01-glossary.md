# Glossary

Status: draft

> [Uniti Standard](README.md) › Glossary
> · Previous: [Principles](00-principles.md) · Next: [Facts](form/01-facts.md)

Every term in this standard is used with the meaning below, and only with that
meaning. A new term is added here **before** it is used in another document.
Terms still marked *(provisional)* will be confirmed in the form document named
in the last column.

## General terms

| Term | Meaning | Defined in |
|---|---|---|
| **Uniti Standard** | A shared form for recording the facts, knowledge, and logic of an organization, together with its first shared content | `00-principles` |
| **Organization** | Anyone who records their activities: a business, clinic, school, institution, community | — |
| **Domain** | One field of activity with its own needs, for example rental, health, education | — |
| **Form** | The way to record anything, the same for all domains. The layer that is standardized strictly | `00-principles` |
| **Content** | Anything written in the form: concepts, properties, calculation rules, examples. Vocabularies and modules are content | `00-principles` |
| **Vocabulary** | Content used together by many organizations in many domains | `content/README` |
| **Module** | One container of content belonging to one owner, with versions. A vocabulary is also delivered as a module | v0.2 (`decisions/0048`) |
| **Owner** | The party that has the right to write content under an address | v0.2 (`decisions/0048`) |
| **Implementation** | Software that carries out the standard | `00-principles` |

## Facts

| Term | Meaning | Defined in |
|---|---|---|
| **Entity** | Anything that can be talked about: a person, an item, an event, a promise, a document. Every entity has its own identifier | `form/01-facts` |
| **Fact** | One statement about one entity: subject, property, and value, together with its time and provenance | `form/01-facts` |
| **Subject** | The entity a fact talks about | `form/01-facts` |
| **Property** | What is said about the subject, for example its name, price, or customer | `form/01-facts` |
| **Value** | The content of a property for one subject: text, a number, a date, or another entity that is referred to | `form/03-values` |
| **Valid time** | Since when a fact is true in the world | `form/01-facts` |
| **Recorded time** | Since when a fact is known and recorded | `form/01-facts` |
| **Provenance** | Who stated a fact, through which action, and from which source | `form/01-facts` |
| **Identifier** | A random code, unique across the world, and permanent, for an entity or for a fact | `form/01-facts` |
| **Type** | A basic property belonging to the form that states the concept an entity belongs to | `form/01-facts` |
| **Fact kind** | What a fact does to another fact. The list is closed: statement, replacement, ending, correction, retraction, redaction | `form/01-facts` |
| **Target** | The old fact that is touched by a fact whose kind is not a statement | `form/01-facts` |
| **Statement** | A fact kind that does not touch another fact | `form/01-facts` |
| **Replacement** | A fact kind: the target was true before, and from the valid time of this fact its value is replaced | `form/01-facts` |
| **Ending** | A fact kind: the target was true before, and from the valid time of this fact it no longer holds | `form/01-facts` |
| **Correction** | A fact kind: the target was never true, and this fact replaces it completely | `form/01-facts` |
| **Retraction** | A fact kind: the target was never true, and there is no replacement | `form/01-facts` |
| **Redaction** *[provisional]* | A fact kind: the target stays valid, but its value must not be read any more | `form/01-facts` |
| **Personal data** *[provisional]* | A mark on a property that its value concerns a person's private matters and may be redacted | `form/04-concepts` |
| **Reason** | Why a fact is corrected, retracted, or redacted. The list is open, in the vocabulary | `form/01-facts` |
| **Action** | One act of recording that records one or several facts at once, together with their provenance | `form/01-facts` |
| **Actor** | The entity that states the facts in an action: a person, an AI, or a machine | `form/01-facts` |
| **Approver** | The entity that approves and is responsible for an action, when different from the actor | `form/01-facts` |
| **Source** | Where the facts of an action come from. The list is open, in the vocabulary | `form/01-facts` |
| **Version used** | The version of the module that was used when a fact was stated | `form/01-facts` |
| **As of (R)** | The recorded time limit used when reading facts | `form/01-facts` |
| **Value type** | The kind of a value. The list is closed: text, number, yes/no, date, instant, choice, reference | `form/03-values` |
| **Quantity** | The kind of measure of a number, for example money, mass, duration. Set by the property | `form/03-values` |
| **Unit** | The way to measure a quantity, for example IDR, kg, day. Carried by every value | `form/03-values` |
| **Direction** | What a positive number means on a number property: increase, decrease, no direction, or position | `form/03-values` |
| **Date** | One calendar day, without a time of day | `form/03-values` |
| **Instant** | One exact point in time, always with its time zone | `form/03-values` |
| **Default time zone** | The time zone of an organization, used to read a date as the start of the day | `form/03-values` |
| **Language code** | The language code of a text according to BCP 47, for example `id` or `en` | `form/03-values` |
| **Choice list** | A set of permitted choices, with its own address. Open or closed | `form/03-values` |
| **Open choice list** | A choice list that anyone can add to, in their own module | `form/03-values` |
| **Closed choice list** | A choice list that only its owner can add to | `form/03-values` |
| **Reference** | A value type that is the identifier of another entity | `form/03-values` |
| **Derived** | A kind of number that is calculated with certainty from facts by a calculation rule | `form/06-calculation-rules` |
| **Decided** | A kind of number or value that someone chooses, for example which invoice this payment settles. Recorded as a fact | `form/06-calculation-rules` |
| **Estimated** | A kind of number that comes from a model, a guess, or a search for a solution. Recorded as a fact with a machine or AI actor | `form/06-calculation-rules` |
| **Conformance level** | The level of calculation operations that an implementation supports: 1 basic, 2 ordering and folding, 3 recursion | `form/06-calculation-rules` |
| **Computed value** | A number derived from facts by a calculation rule. Not a fact | `form/06-calculation-rules` |

## Addresses and change

| Term | Meaning | Defined in |
|---|---|---|
| **Address** | A unique and permanent name for an owner, module, concept, property, or choice, which contains its owner | `form/02-addresses` |
| **Root** *[provisional]* | The start of the address that is the same for the whole ecosystem. For now `https://uniti.example` | `form/02-addresses` |
| **Choice** | One value from a choice list, with its own address | `form/03-values` |
| **Version reference** | The address of a module plus one exact version number, for example `alex/rental@v3` | `form/02-addresses` |
| **Draft** | Content that is being written and has not been frozen. Not yet part of the ecosystem | `form/07-change` |
| **Version** | One state of a module that has been frozen and never changes again | `form/07-change` |
| **Freeze** | To make a version fixed, after all its checks pass | `form/07-change` |
| **Deprecated** | A mark that an address is no longer recommended, naming its replacement when there is one | `form/07-change` |
| **Withdrawn** | A mark that a version must not be used or installed any more because of a serious error; it stays readable | `form/07-change` |
| **Install** | To use one version of a module in an organization to record and read facts. The content and relations of a module apply only to the organization that installs it | v0.2 (`decisions/0048`) |

## Content

| Term | Meaning | Defined in |
|---|---|---|
| **Concept** | One class of entities, for example "transaction" or "person" | `form/04-concepts` |
| **Concept card** | The standard description of a concept: address, label, definition, includes, excludes, parent, properties, bridges | `form/04-concepts` |
| **Property card** | The standard description of a property: address, label, definition, value type, number of values, personal data mark, and others | `form/04-concepts` |
| **Includes** / **excludes** | Real things that belong, or that look similar but do not belong, to a concept. Not an *example* in the sense of proof | `form/04-concepts` |
| **Parent** | A concept that is more general than a child concept. At most one | `form/04-concepts` |
| **Child concept** | A concept that states a parent, and inherits all its properties | `form/04-concepts` |
| **Role** | The position of an entity toward another entity, for example customer or employee. Recorded as a reference, not as a type | `form/04-concepts` |
| **Number of values** | Whether a property holds one or many values at one time | `form/04-concepts` |
| **Required** (property) | A property that must have a value for an entity of a concept. Checked per action | `form/04-concepts` |
| **Main label** / **other label** | One main name per language, and the other names that can be used | `form/04-concepts` |
| **Label** | The name of a concept or property in a particular human language | `form/04-concepts` |
| **Relation** | The way one piece of content points to other content. The list is closed, in two groups: structural and meaning | `form/05-relations` |
| **Structural relation** | Subtype of, applies to, refers to, uses list, in list | `form/05-relations` |
| **Meaning relation** | Replaced by, and the four bridges | `form/05-relations` |
| **Applies to** | The relation that states a property can be used for entities of a concept, and whether it is required | `form/05-relations` |
| **Bridge** | A note that a piece of content has the same, a broader, a narrower, or a similar meaning as content in an outside standard or in another module | `form/05-relations` |
| **Code list** | A list of standard values from an outside standard that is used directly, for example currency codes. Always closed, and its choices are the original codes | `03-values` §2.6, `content/code-lists` |
| **Calculation rule** | The way a value is derived from facts. It is a computed property, a helper, a constraint, or a contribution | `form/06-calculation-rules` |
| **Computed property** | A property whose value is always calculated from its rule, read like any other property, and never recorded | `form/06-calculation-rules` |
| **Helper** | A rule for an intermediate result, used only by other rules | `form/06-calculation-rules` |
| **Constraint** | A yes/no rule for a concept, checked per action. An action that makes it unmet is rejected | `form/06-calculation-rules` |
| **Open / closed computed property** | A computed property that can, or cannot, receive contributions from other modules | `form/06-calculation-rules` |
| **Contribution** | A part of an open computed property owned by someone else, written in the contributor's module | `form/06-calculation-rules` |
| **Expression** | The content of a rule, built only from core operations and other calculation rules | `form/06-calculation-rules` |
| **Reference notation** | The way to write rules, examples, and cards that is used in the standard documents and in the conformance tests | `appendix/A-notation` |
| **Binding** | The name given to each member of a collection inside an operation, for example `s` in `s: s.amount` | `appendix/A-notation` |
| **Local name** | A name that applies only inside one rule: a binding, a `let`, or a parameter | `appendix/A-notation` |
| **Keyword** | A word whose meaning is fixed in the reference notation, such as `if`, `this`, and the names of operations, so it cannot be used as a local name | `appendix/A-notation` |
| **Full / short form** | The way to write cards and rules: complete with all parts of the card for a frozen module, or only the head and its expression for a quotation | `appendix/A-notation` |
| **Operation list** | The closed list of operations that calculation rules may use, divided into three levels. Also called the core operations | `form/06-calculation-rules` |
| **Core operations** | The operations that are part of the form: they cannot be written from other operations, and contain no choice of method | `form/06-calculation-rules` |
| **Calculation library** | Ways of calculating written as helpers without concepts in a vocabulary module, using only the core operations. Content, not form | `form/06-calculation-rules` |
| **Intermediate value** | A collection, record, or range used inside a rule. Never becomes the value of a property | `form/06-calculation-rules` |
| **Range** | From one time up to before another time (half open) | `form/06-calculation-rules` |
| **Tie-breaker** | The standard order for equal members: valid time, recorded time, then identifier | `form/06-calculation-rules` |
| **Exact fraction** | The way numbers are calculated inside rules, without rounding, for example exactly one third | `form/06-calculation-rules` |
| **Empty** | The result of an expression when there is no value, for example a property without facts | `form/06-calculation-rules` |
| **Not computable** | A result that cannot be determined, together with its kind of reason, its explanation, and its location. Never becomes 0 | `form/06-calculation-rules` |
| **Module set** | The exact versions of the modules that determine a computed value | `form/06-calculation-rules` |
| **Projection** | A computed value that is stored to speed up reading. It can be thrown away and rebuilt | `form/06-calculation-rules` |
| **Rejection** | A note that an action was rejected, by which constraint, from which module, and why | `form/06-calculation-rules` |
| **Rejection record** | A record about a rejected action. It can be read back, but it is not a fact | `form/06-calculation-rules` |
| **Example** | Some facts, plus one question or one action, and the result that must come out of them, as proof that the logic of a piece of content is correct | `form/08-proof` |
| **Compute / accept / reject example** | Three kinds of example: the result of a computed property; an action that is accepted; an action that is rejected by a particular constraint | `form/08-proof` |
| **Local id** | The name of an entity that applies only inside one example, in place of an identifier | `form/08-proof` |
| **Behavior change** | A machine report that an example from an old version no longer passes in a new version, and is marked replaced | `form/08-proof` |
| **Conformance tests** | A set of examples owned by the standard, to test whether an implementation conforms to the standard | `form/08-proof` |

## Rules

| Term | Meaning | Defined in |
|---|---|---|
| **Requirement keyword** | MUST, MUST NOT, SHOULD, SHOULD NOT, MAY | `00-principles` §6 |
| **Conform** | The state of content or software that meets all the MUST and MUST NOT rules | `00-principles` §7 |
