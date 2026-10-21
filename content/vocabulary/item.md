# Item

Status: draft

An item that is stored, sold, rented out, or made. The vocabulary holds only
the concept Item and the reference to an item. Other properties, such as
stock, rental rate, or production cost, are written in the module that uses
them with "applies to"
([`04-concepts`](../../form/04-concepts.md) §2.3).

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
