# Code lists

Status: locked (v0.1.0)

## 1. Purpose

Code lists that are already standard are used directly, not made again
([`00-principles`](../00-principles.md) P8). This document names the external
code lists that the standard uses, which codes are used, and their address, so
that these codes can be choice values like any other choice
([`03-values`](../form/03-values.md) §2.3 and §2.6).

## 2. External code lists in use

| List | External standard | Used for | Address |
|---|---|---|---|
| Currencies | ISO 4217 | Units of money | `uniti/unit/Unit` |
| Other units | UCUM (*Unified Code for Units of Measure*) | Units of mass, length, and duration | `uniti/unit/Unit` |
| Languages | BCP 47 | Language codes in labels and text | no address yet |

Currencies and other units are in one list, because `unit_of(n)` gives the
unit of a number as a choice from one list
([`06-calculation-rules`](../form/06-calculation-rules.md) §2.5).

Language codes are used only in the way labels and text are written. No case
records a language as a value yet, so the list has no address yet.

## 3. The unit list

```uniti
module uniti/unit@v1

choice_list Unit, code
  label.en       Unit
  label.id       Satuan
  definition.en  Unit of measure, including currencies. Every number with a
                 unit uses a unit from this list.
  note.en        Currency codes come from ISO 4217 and other unit codes from
                 UCUM, except calendar months and years.
  choices:
    IDR
    USD
    s
    min
    h
    d
    wk
    month
    year
    g
    kg
    mm
    cm
    m
    km
```

The meaning of each code, and how it is written in the reference notation:

| Code | Quantity | Written in the reference notation | Fixed relation | Source of the code |
|---|---|---|---|---|
| `IDR` | money | `IDR` | — | ISO 4217 |
| `USD` | money | `USD` | — | ISO 4217 |
| `s` | duration | `second` | base unit | UCUM |
| `min` | duration | `minute` | 1 min = 60 s | UCUM |
| `h` | duration | `hour` | 1 h = 60 min | UCUM |
| `d` | duration | `day` | 1 d = 24 h | UCUM |
| `wk` | duration | `week` | 1 wk = 7 d | UCUM |
| `month` | duration | `month` | calendar base unit | Uniti |
| `year` | duration | `year` | 1 year = 12 months | Uniti |
| `g` | mass | `g` | base unit | UCUM |
| `kg` | mass | `kg` | 1 kg = 1,000 g | UCUM |
| `mm` | length | `mm` | 1,000 mm = 1 m | UCUM |
| `cm` | length | `cm` | 100 cm = 1 m | UCUM |
| `m` | length | `m` | base unit | UCUM |
| `km` | length | `km` | 1 km = 1,000 m | UCUM |

A unit can be converted only to another unit with which it has a fixed relation
(06 §2.5, `convert`). Money has no fixed relation, because the exchange rate is
recorded as a fact. Months and years also have no fixed relation with days,
because months differ in length.

**Calendar months and years** are codes owned by Uniti. The UCUM codes `mo` and
`a` mean average lengths, 30.4375 days and 365.25 days, and are not the same as
one calendar month or one calendar year. UCUM has no code for the calendar
month.

## 4. Quantities

| Quantity | Units |
|---|---|
| `money` | Currency codes |
| `duration` | `s`, `min`, `h`, `d`, `wk`, `month`, `year` |
| `mass` | `g`, `kg` |
| `length` | `mm`, `cm`, `m`, `km` |

A derived quantity is written in the same way as its units, for example
`length²` for area and `money/duration` for a rate (appendix A §2.4).

## 5. Adding codes

This list is content. A new code is added through a new version of
`uniti/unit`, without changing the form:
- a code from an external standard is written exactly as in that external
  standard;
- a code owned by Uniti is made only when the external standard has no
  counterpart, such as calendar months and years;
- a code is chosen because it is needed, not because it exists in an external
  standard.
