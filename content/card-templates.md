# Card templates

Status: locked (v0.1.0)

Templates for writing cards in the full form, which is the form for a module
that will be frozen (appendix A §2.8, NOTATION-17). The parts that the
standard requires are marked *required*. The other parts may be written or
left out.

Text between `‹ ›` is replaced with its content. Filled-in examples are in
[`vocabulary/`](vocabulary/).

The reference calculator checks the required parts with
`python -m calculator.completeness ‹file›`, from the `reference` folder.

## Concept card

```
concept ‹ConceptName›
  label.en       ‹name for humans›                       # required, CONCEPT-1
  definition.en  ‹what this concept is, one or two sentences›   # required, CONCEPT-1
  parent         ‹ParentConcept›                         # at most one
  includes.en    ‹Domain›: ‹things that belong›          # required, at least one
  excludes.en    ‹Domain›: ‹things that look similar but do not belong, and
                 why›                                    # required, at least one
  similar        ‹full address or IRI›                   # bridge, optional
  note.en        ‹extra remarks›
```

In the vocabulary, the includes and the excludes are each taken from at least
two domains (CONCEPT-2). The domain is written at the start of the sentence,
for example "Clinic: ...", so that it is easy to check when reading.

## Property card

```
property ‹property_name› : ‹value type›                  # required, CONCEPT-3
  label.en       ‹name for humans›                       # required
  definition.en  ‹what this property states›             # required
  personal       ‹yes or no›                             # required [provisional]
  same_as        ‹full address or IRI›                   # bridge, optional
  note.en        ‹extra remarks›
```

The value type is written in the head line: `text`, `number (‹quantity›,
‹direction›)`, `yes_no`, `date`, `instant`, `choice ‹List›`, or `reference
‹Concept›`, plus `, many` for a property with many values (appendix A §2.8).

## Choice list card

```
choice_list ‹ListName›, ‹open, closed, or code›
  label.en       ‹name for humans›                       # required, VALUE-19
  definition.en  ‹which choices this list holds›         # required, VALUE-19
  choices:
    ‹first_choice›
    ‹second_choice›
```

## Computed property

```
computed ‹Concept›.‹name›(‹parameters›) : ‹value type›, ‹open or closed›
  label.en       ‹name for humans›                       # required, CALC-4
  definition.en  ‹what is computed›                      # required
  personal       ‹yes or no›                             # required [provisional]
  rule:
    ‹expression›
```

## Constraint

```
constraint ‹Concept›.‹name›
  label.en       ‹name for humans›                       # required, CALC-37
  definition.en  ‹what is guarded›                       # required
  message.en     ‹sentence for humans when rejected›     # required
  rule:
    ‹yes/no expression›
```

## Helper

```
helper ‹name›(‹parameters›) : ‹result type›
  definition.en  ‹what is produced›
  rule:
    ‹expression›
```

A helper has no required card parts, but it is still written in the full form
in a module that will be frozen.
