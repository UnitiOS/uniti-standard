# Barang

Status: draf

Barang yang disimpan, dijual, disewakan, atau dibuat. Kamus hanya memuat
konsep Barang dan rujukan ke barang. Sifat lain, seperti stok, tarif sewa,
atau biaya produksi, ditulis di modul pemakainya dengan "berlaku untuk"
([`04-konsep`](../../bentuk/04-konsep.md) §2.3).

```uniti
module uniti/item@v1

concept Item
  label.en       Item
  label.id       Barang
  definition.en  One kind of object that can be stored, moved, sold, rented
                 out, or made, for example "4-person dome tent". The
                 quantity is recorded in the record that names that item,
                 not with one entity for each object.
  includes.en    Inventory: tents that enter and leave the shop's warehouse.
  includes.en    Manufacturing: components and finished products in a bill
                 of materials.
  excludes.en    Logistics: a delivery service. A service cannot be stored.
  excludes.en    Loyalty: member points. Points are numbers, not objects.
  similar        https://schema.org/Product

property item : reference Item
  label.en       Item
  label.id       Barang
  definition.en  The item that a record refers to, for example the item
                 received, sold, or rented.
  personal       no
```
