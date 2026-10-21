# Relations across modules

Stage 5, test U4 (`uji/02-lintas-domain.md`)<!-- ARCHIVE-LINK: ../../02-lintas-domain.md -->,
from the clinic and cashier example in 05 §4.

The payment vocabulary
([`content/vocabulary/payment.md`](../content/vocabulary/payment.md)) has the
open choice list `PaymentMethod`. Klinik Sehat and Apotek Ria each add the
choice `bpjs` to that list, in their own module. Klinik Sehat declares its
choice to be the **same as** the pharmacy's choice. That bridge is only a
remark (RELATION-9). The combined report of the two is computed with a
calculation rule that names both choices.

The clinic also has a child concept, `VisitPayment`, which is also read as
`Payment` (CONCEPT-12), complete with the properties of its parent.

```uniti
module klinik-sehat/cashier@v1
  uses uniti/payment@v1

concept VisitPayment
  label.en     Visit payment
  parent       Payment

choice bpjs to uniti/payment/PaymentMethod
  label.en     BPJS Kesehatan
  same_as      apotek-ria/cashier/bpjs

module apotek-ria/cashier@v1
  uses uniti/payment@v1

choice bpjs to uniti/payment/PaymentMethod
  label.en     BPJS Kesehatan

module klinik-sehat/report@v1
  uses uniti/payment@v1
  uses klinik-sehat/cashier@v1
  uses apotek-ria/cashier@v1

concept Report

computed Report.bpjs_total(period) : number (money, increase), closed:
  sum(all(Payment, p: (p.method = klinik-sehat/cashier/bpjs
                       or p.method = apotek-ria/cashier/bpjs)
                      and p.date in period),
      p: p.amount)

example combined_bpjs_october
  kind         compute
  title        BPJS payments of the clinic and the pharmacy
  explanation  A clinic visit of 150,000 and pharmacy medicine of 80,000 were
               paid with BPJS: 230,000. The cash payment of 50,000 is not
               included, and neither is the BPJS payment from September.
  zone         WIB
  facts        recorded 31 Oct 2026 17:00
    rep  type    Report                     valid 1 Jan 2026
    k1   type    VisitPayment               valid 5 Oct 2026
    k1   method  klinik-sehat/cashier/bpjs  valid 5 Oct 2026
    k1   amount  150,000 IDR                valid 5 Oct 2026
    k1   date    5 Oct 2026                 valid 5 Oct 2026
    a1   type    Payment                    valid 5 Oct 2026
    a1   method  apotek-ria/cashier/bpjs    valid 5 Oct 2026
    a1   amount  80,000 IDR                 valid 5 Oct 2026
    a1   date    5 Oct 2026                 valid 5 Oct 2026
    t1   type    Payment                    valid 7 Oct 2026
    t1   method  cash                       valid 7 Oct 2026
    t1   amount  50,000 IDR                 valid 7 Oct 2026
    t1   date    7 Oct 2026                 valid 7 Oct 2026
    s1   type    VisitPayment               valid 28 Sep 2026
    s1   method  klinik-sehat/cashier/bpjs  valid 28 Sep 2026
    s1   amount  120,000 IDR                valid 28 Sep 2026
    s1   date    28 Sep 2026                valid 28 Sep 2026
  ask          rep.bpjs_total(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 31 Oct 2026 18:00
  result       230,000 IDR
```

A clinic that installs only its own cashier module cannot name the pharmacy's
choice, even though the bridge points there (RELATION-5). This is tested in
`operasi/uji_versi.py`, because an example that names it is a notation error.
