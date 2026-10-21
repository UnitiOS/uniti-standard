# Pembayaran

Status: draf

Uang yang berpindah dari satu pihak ke pihak lain. Jumlahnya **tanpa
arah**, karena pembayaran yang sama adalah uang keluar bagi pembayarnya dan
uang masuk bagi penerimanya
([`03-nilai`](../../bentuk/03-nilai.md) §2.3). Modul pemakainya menentukan
arahnya dengan sifatnya sendiri, misalnya pinjaman atau sewa yang dibayar.

Hanya jumlah yang wajib. Tanggal dan cara bayar boleh dicatat, tetapi tidak
wajib, karena tidak semua kasus mencatatnya.

```uniti
module uniti/payment@v1

concept Payment
  label.en       Payment
  label.id       Pembayaran
  definition.en  Money that moves from one party to another, once, in a
                 specific amount.
  includes.en    Clinic: a patient pays for a visit with BPJS.
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
