# The first vocabulary used by two domains

Stage 6 ([`content/README.md`](../content/README.md) §7, criterion 3). A
rental shop and a school use the same vocabulary: party, item, and payment
([`content/vocabulary/`](../content/vocabulary/)).

What it shows:
- **roles as references.** Renter and student are not concepts. Both are
  references to Person from the vocabulary (CONCEPT-13);
- **extra properties from other parties.** The shop and the school each add a
  property to Payment, which belongs to the vocabulary, without changing the
  vocabulary, and without making it required (CONCEPT-7, CONCEPT-8);
- **computed properties for vocabulary concepts.** The school writes a
  computed property for Person;
- **required properties of the vocabulary apply to every user.** A payment
  without an amount is rejected, in whichever module it is recorded
  (CONCEPT-18).

The payment amount in the vocabulary has no direction. The shop and the school
are both recipients, so both count a payment as money coming in.

```uniti
module happy-camp/rental@v1
  uses uniti/party@v1
  uses uniti/item@v1
  uses uniti/payment@v1

concept Rental

property renter : reference Person
property start_date : date
property end_date : date
property rental : reference Rental

applies to Rental:
  item         required
  renter       required
  start_date   required
  end_date     required

applies to Payment:
  rental

computed Rental.paid : number (money, increase), closed:
  sum(all(Payment, p: p.rental = this), p: p.amount)

example rental_paid
  kind         compute
  title        A rental paid twice
  explanation  Sam pays 200,000 in cash and 100,000 by transfer for the tent
               rental: 300,000. The payment of 50,000 for another rental is
               not included.
  zone         WIB
  facts        recorded 10 Oct 2026 17:00
    sam  type        Person       valid 1 Jan 2026
    eva  type        Person       valid 1 Jan 2026
    tent  type        Item         valid 1 Jan 2026
    r1    type        Rental       valid 5 Oct 2026
    r1    item        tent         valid 5 Oct 2026
    r1    renter      sam         valid 5 Oct 2026
    r1    start_date  5 Oct 2026   valid 5 Oct 2026
    r1    end_date    8 Oct 2026   valid 5 Oct 2026
    r2    type        Rental       valid 6 Oct 2026
    r2    item        tent         valid 6 Oct 2026
    r2    renter      eva         valid 6 Oct 2026
    r2    start_date  9 Oct 2026   valid 6 Oct 2026
    r2    end_date    10 Oct 2026  valid 6 Oct 2026
    b1    type        Payment      valid 5 Oct 2026
    b1    rental      r1           valid 5 Oct 2026
    b1    amount      200,000 IDR  valid 5 Oct 2026
    b1    method      cash         valid 5 Oct 2026
    b2    type        Payment      valid 8 Oct 2026
    b2    rental      r1           valid 8 Oct 2026
    b2    amount      100,000 IDR  valid 8 Oct 2026
    b2    method      transfer     valid 8 Oct 2026
    b3    type        Payment      valid 6 Oct 2026
    b3    rental      r2           valid 6 Oct 2026
    b3    amount      50,000 IDR   valid 6 Oct 2026
  ask          r1.paid   T: 10 Oct 2026   R: 10 Oct 2026 18:00
  result       300,000 IDR

example payment_without_amount
  kind         reject
  title        Payment without amount
  explanation  The amount is required for every payment according to the
               vocabulary, even when the shop records it.
  zone         WIB
  facts        as in rental_paid
  action       recorded 11 Oct 2026 09:00, actor eva
    b4  type    Payment  valid 11 Oct 2026
    b4  rental  r2       valid 11 Oct 2026
    b4  method  cash     valid 11 Oct 2026
  result       rejected by CONCEPT-18, entity b4

module bright-future/tuition@v1
  uses uniti/party@v1
  uses uniti/payment@v1

property student : reference Person

applies to Payment:
  student

computed Person.tuition_paid(period) : number (money, increase), closed:
  sum(all(Payment, p: p.student = this and p.date in period), p: p.amount)

example tuition_october
  kind         compute
  title        Tuition paid by a student in October
  explanation  Maria pays the tuition for September and October, 500,000 each.
               What is paid in October is only 500,000. Ivan's payment is
               not included.
  zone         WIB
  facts        recorded 31 Oct 2026 17:00
    maria    type     Person       valid 1 Jan 2026
    ivan  type     Person       valid 1 Jan 2026
    s1     type     Payment      valid 7 Sep 2026
    s1     student  maria          valid 7 Sep 2026
    s1     amount   500,000 IDR  valid 7 Sep 2026
    s1     date     7 Sep 2026   valid 7 Sep 2026
    s2     type     Payment      valid 6 Oct 2026
    s2     student  maria          valid 6 Oct 2026
    s2     amount   500,000 IDR  valid 6 Oct 2026
    s2     date     6 Oct 2026   valid 6 Oct 2026
    s3     type     Payment      valid 8 Oct 2026
    s3     student  ivan        valid 8 Oct 2026
    s3     amount   500,000 IDR  valid 8 Oct 2026
    s3     date     8 Oct 2026   valid 8 Oct 2026
  ask          maria.tuition_paid(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 31 Oct 2026 18:00
  result       500,000 IDR
```

The school does not install the shop module, so the property `rental` does not
apply to payments at the school. The shop also does not see the property
`student` (CONCEPT-7).
