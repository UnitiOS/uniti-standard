# Facts with a wrong form inside an action

Examples for the rules of the form of a fact when it arrives inside an action:
FACT-2, FACT-9, FACT-10, FACT-11, FACT-13, and FACT-14. They fill the known gap
of [`decisions/0056`](../decisions/0056-conformance-test-owners-and-known-gap.md)
([`decisions/0058`](../decisions/0058-rejection-of-facts-with-a-wrong-form.md)):
until now no example rejected an action because of a rule of a fact. The module
has no constraint and no required property, so the only thing that can reject
an action here is the rule named in the result (PROOF-32). The last three
examples are the other way round: the action is right, and it is accepted.
All the blocks below belong to one module, `reference/fact-form@v1`.

```uniti
module reference/fact-form@v1

concept Customer
concept Product

property phone : text
property price : number (money, position)

applies to Customer:
  phone

applies to Product:
  price
```

## A value that the kind does not take, or does not have (FACT-2)

An ending says that something stops. It states no value. A correction replaces
a wrong value, so it must state one.

```uniti
example ending_with_a_value
  kind         reject
  title        An ending that states a value
  explanation  Alex, a customer, stops using a phone number on 1 November. The
               cashier ends the number but also types a new one in the same
               fact. An ending states no value, so the action is rejected.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    c1   phone  "0812-333-444"  valid 1 Nov 2026  ends f1
  result       rejected by FACT-2, entity c1, at 1 Nov 2026

example correction_without_a_value
  kind         reject
  title        A correction without a value
  explanation  Sam notices that the phone number of a customer was typed wrong.
               The correction is recorded but the right number is forgotten. A
               correction must state the right value.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    c1   phone  valid 1 Oct 2026  corrects f1
  result       rejected by FACT-2, entity c1, at 1 Oct 2026
```

## A target that does not fit (FACT-9)

The target must be a fact recorded before, about the same entity and the same
property.

```uniti
example target_of_another_customer
  kind         reject
  title        A replacement aimed at the phone of another customer
  explanation  Maria has a new phone number. The cashier replaces the number of
               Nina by mistake, because the two lines look alike. The target is
               about another customer, so the action is rejected.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    c2       type   Customer       valid 1 Oct 2026
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
    f2: c2   phone  "0812-555-666"  valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    c1   phone  "0812-333-444"  valid 1 Nov 2026  replaces f2
  result       rejected by FACT-9, entity c1, at 1 Nov 2026

example target_in_the_same_action
  kind         reject
  title        A replacement aimed at a fact of the same action
  explanation  Alex gives a phone number on 1 October, and then a new one from
               1 November, both typed in one action. The second fact replaces
               the first, but the first is not recorded yet. A target must be a
               fact from before the action.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
    c1       phone  "0812-333-444"  valid 1 Nov 2026  replaces f1
  result       rejected by FACT-9, entity c1, at 1 Nov 2026
```

## A replacement that is not later than its target (FACT-10)

```uniti
example replacement_on_the_same_date
  kind         reject
  title        A price replaced on the date of the price it replaces
  explanation  The shop owner entered the price of a lamp as 150,000 IDR from
               1 October, and finds that it should have been 125,000 IDR from
               the same day. A replacement must be valid later than its
               target. A wrong price is repaired with a correction.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    p1       type   Product        valid 1 Oct 2026
    f1: p1   price  150,000 IDR    valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    p1   price  125,000 IDR  valid 1 Oct 2026  replaces f1
  result       rejected by FACT-10, entity p1, at 1 Oct 2026
```

## A correction of a fact that has no value (FACT-11)

```uniti
example correction_of_an_ending
  kind         reject
  title        A correction aimed at an ending
  explanation  Maria sees that the price of a lamp was ended on the wrong date.
               Maria records a correction of the ending with a price. An ending
               has no value to correct. A wrong ending is retracted, and the
               right one is recorded.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    p1       type   Product        valid 1 Oct 2026
    f1: p1   price  150,000 IDR    valid 1 Oct 2026
    f2: p1   price  valid 1 Nov 2026  ends f1
  action       recorded 20 Oct 2026 10:00
    p1   price  150,000 IDR  valid 1 Dec 2026  corrects f2
  result       rejected by FACT-11, entity p1, at 1 Dec 2026
```

## A retraction of a retraction (FACT-13)

```uniti
example retraction_of_a_retraction
  kind         reject
  title        A retraction aimed at a retraction
  explanation  Sam retracted the phone number of a customer by mistake, and now
               retracts the retraction to bring the number back. A retraction
               cannot be retracted. The number is stated again as a new fact.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
    f2: c1   phone  valid 1 Oct 2026  retracts f1
  action       recorded 20 Oct 2026 10:00
    c1   phone  valid 1 Oct 2026  retracts f2
  result       rejected by FACT-13, entity c1, at 1 Oct 2026
```

## A property with one value (FACT-14)

A phone has one value at one time, and so does a price. A new value is a
replacement of the value in force, or a correction, and never a second
statement.

```uniti
example second_statement_of_the_phone
  kind         reject
  title        A second statement of a phone while one is in force
  explanation  Nina already has a phone number. The cashier types another one
               from 1 November as a new statement. It should be a replacement
               of the number in force.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    c1   phone  "0812-333-444"  valid 1 Nov 2026
  result       rejected by FACT-14, entity c1, at 1 Nov 2026

example replacement_of_an_old_price
  kind         reject
  title        A replacement of a price that is no longer in force
  explanation  A lamp cost 150,000 IDR from 1 October and 160,000 IDR from
               1 November. The shop owner wants a price from 1 December and
               aims at the old price of October. The price in force on
               1 December is the one from November, so the action is rejected.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    p1       type   Product        valid 1 Oct 2026
    f1: p1   price  150,000 IDR    valid 1 Oct 2026
    f2: p1   price  160,000 IDR    valid 1 Nov 2026  replaces f1
  action       recorded 20 Oct 2026 10:00
    p1   price  170,000 IDR  valid 1 Dec 2026  replaces f1
  result       rejected by FACT-14, entity p1, at 1 Dec 2026

example two_prices_for_one_date
  kind         reject
  title        Two prices of one product for the same date
  explanation  Alex types the price of a new lamp twice in one action, with two
               different amounts, both from 1 November. Only one price can hold
               at one time.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    p1       type   Product        valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    p1   price  150,000 IDR  valid 1 Nov 2026
    p1   price  155,000 IDR  valid 1 Nov 2026
  result       rejected by FACT-14, entity p1, at 1 Nov 2026
```

## The right way (accepted)

The same situations written in the way the rules ask for.

```uniti
example replace_the_price_in_force
  kind         accept
  title        A replacement of the price in force
  explanation  The price of a lamp goes up from 150,000 IDR to 175,000 IDR on
               1 November. The shop owner replaces the price in force. Before
               1 November the old price is read, and from then the new one.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    p1       type   Product        valid 1 Oct 2026
    f1: p1   price  150,000 IDR    valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    p1   price  175,000 IDR  valid 1 Nov 2026  replaces f1
  result       accepted
  ask          p1.price   T: 15 Oct 2026   R: 21 Oct 2026
  result       150,000 IDR
  ask          p1.price   T: 15 Nov 2026   R: 21 Oct 2026
  result       175,000 IDR

example price_before_the_first_price
  kind         accept
  title        A price stated for a time before the first price
  explanation  Sam finds the price list of September, when no price was
               recorded yet for the lamp. Nothing is in force then, so a
               statement is right. The September price is read in September,
               and the first price is still read from October.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    p1       type   Product        valid 1 Aug 2026
    f1: p1   price  150,000 IDR    valid 1 Oct 2026
  action       recorded 20 Oct 2026 10:00
    p1   price  140,000 IDR  valid 1 Sep 2026
  result       accepted
  ask          p1.price   T: 15 Sep 2026   R: 21 Oct 2026
  result       140,000 IDR
  ask          p1.price   T: 15 Oct 2026   R: 21 Oct 2026
  result       150,000 IDR

example state_the_phone_again
  kind         accept
  title        A phone retracted by mistake is stated again
  explanation  The phone number of Nina was retracted by mistake. The cashier
               does not retract the retraction. The number is stated again as a
               new fact, and it is read as before.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    f1: c1   phone  "0812-111-222"  valid 1 Oct 2026
    f2: c1   phone  valid 1 Oct 2026  retracts f1
  action       recorded 20 Oct 2026 10:00
    c1   phone  "0812-111-222"  valid 1 Oct 2026
  result       accepted
  ask          c1.phone   T: 25 Oct 2026   R: 21 Oct 2026
  result       "0812-111-222"
```
