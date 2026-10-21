# Outside the calculation rules

Cases B1 to B4 of the paper test (`uji/01-hitung.md`)<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.M. These cases are deliberately not calculated: the result is a decision or
an estimate, and it is recorded as a fact through an action
([`decisions/0025`](../decisions/0025-three-kinds-of-numbers.md)). What is tested is that the fact can be
recorded, with the actor and the approver, and then read back like any other
property.

The confidence level and the source of the action cannot be written in the
`action` line (appendix A §2.9). No rule reads either of them, so they do not
affect the result of the example.

```uniti
module paper/b@v1

concept Product
concept Forecast
concept Invoice
concept Payment
concept Nurse
concept Shift

property product : reference Product
property month : date
property quantity : number (position)
property number : text
property invoice : reference Invoice
property nurse : reference Nurse
property start : instant

applies to Forecast:
  product      required
  month        required
  quantity     required

applies to Invoice:
  number       required

applies to Payment:
  invoice      required

applies to Shift:
  nurse        required
  start        required

example b1_sales_forecast
  kind         accept
  title        B1. Sales forecast for next month
  explanation  Estimate. Recorded with the forecast model as actor, not
               calculated.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    tent   type   Product   valid 1 Jan 2026
  action       recorded 25 Oct 2026 02:00, actor forecast_model_v2
    r1     type      Forecast     valid 25 Oct 2026
    r1     product   tent         valid 25 Oct 2026
    r1     month     1 Nov 2026   valid 25 Oct 2026
    r1     quantity  120          valid 25 Oct 2026
  result       accepted
  ask          r1.quantity   T: 25 Oct 2026   R: 25 Oct 2026 03:00
  result       120

example b2_invoice_number
  kind         accept
  title        B2. Sequential invoice number
  explanation  Decision. The number is decided when the invoice is recorded,
               not calculated from the previous invoice.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    tent   type   Product   valid 1 Jan 2026
  action       recorded 12 Oct 2026 10:00, actor cashier
    f12    type     Invoice   valid 12 Oct 2026
    f12    number   "F-12"    valid 12 Oct 2026
  result       accepted
  ask          f12.number   T: 12 Oct 2026   R: 12 Oct 2026 11:00
  result       "F-12"

example b3_customer_chooses_invoice
  kind         accept
  title        B3. The customer chooses to pay invoice F-12
  explanation  Decision. The customer's choice is recorded as a fact.
  zone         WIB
  facts        recorded 12 Oct 2026 10:00
    f11    type     Invoice   valid 10 Oct 2026
    f11    number   "F-11"    valid 10 Oct 2026
    f12    type     Invoice   valid 12 Oct 2026
    f12    number   "F-12"    valid 12 Oct 2026
  action       recorded 20 Oct 2026 14:00, actor cashier
    pb1    type     Payment   valid 20 Oct 2026
    pb1    invoice  f12       valid 20 Oct 2026
  result       accepted
  ask          pb1.invoice   T: 20 Oct 2026   R: 20 Oct 2026 15:00
  result       f12

example b4_shift_schedule
  kind         accept
  title        B4. Best nurse shift schedule
  explanation  Estimate. Made by an automatic scheduler, approved by the head
               nurse, then recorded as a schedule fact.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    sari   type   Nurse   valid 1 Jan 2026
  action       recorded 25 Oct 2026 16:00, actor auto_scheduler, approver head_nurse
    j1     type     Shift                  valid 25 Oct 2026
    j1     nurse    sari                   valid 25 Oct 2026
    j1     start    1 Nov 2026 07:00       valid 25 Oct 2026
  result       accepted
  ask          j1.nurse   T: 25 Oct 2026   R: 25 Oct 2026 17:00
  result       sari
```
