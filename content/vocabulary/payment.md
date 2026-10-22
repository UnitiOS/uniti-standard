# Payment

Status: locked (v0.1.0)

Money that moves from one party to another. Its amount has **no direction**,
because the same payment is money out for the payer and money in for the
recipient
([`03-values`](../../form/03-values.md) §2.3). The module that uses it sets
the direction with its own property, for example a loan or a rental that is
paid.

Only the amount is required. The date and the payment method may be recorded,
but are not required, because not every case records them.

```uniti
module uniti/payment@v1

concept Payment
  label.en       Payment
  label.id       Pembayaran
  definition.en  Money that moves from one party to another, once, in a
                 specific amount.
  includes.en    Clinic: a patient pays for a visit with national insurance.
  includes.en    Loans: a borrower pays this month's installment.
  excludes.en    Subscription: a monthly invoice. An invoice is a request
                 to pay, and the money has not moved yet.
  excludes.en    Finance: revenue recognized each month from a contract.
                 Recognizing revenue does not move money.
  similar        https://schema.org/PayAction

property amount : number (money, no_direction)
  label.en       Amount
  label.id       Jumlah
  definition.en  The amount of money paid. Never negative.
  personal       no

property date : date
  label.en       Payment date
  label.id       Tanggal bayar
  definition.en  The day the money is paid.
  personal       no

choice_list PaymentMethod, open
  label.en       Payment method
  label.id       Cara bayar
  definition.en  The way money is paid. Anyone may add a payment method in
                 their own module.
  choices:
    cash
    transfer

property method : choice PaymentMethod
  label.en       Payment method
  label.id       Cara bayar
  definition.en  The way the money of a payment is paid.
  personal       no

applies to Payment:
  amount       required
  date
  method
```
