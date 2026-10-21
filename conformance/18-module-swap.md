# Swapping a module

Stage 7, quick test 7.1 (`uji/03-uji-singkat.md`)<!-- ARCHIVE-LINK: ../../03-uji-singkat.md -->.
The story comes from the prototype. Toko Kemah Ceria records rentals with a
module owned by Rudi, then moves to the SewaPro cashier. Two things have to
stay true:

- **the number of tents currently out** stays one number, from old rentals and
  new rentals, without a double column;
- **an old rental is returned through the new cashier.**

In the prototype, the second thing failed: a return in the new cashier could
only point to orders owned by that cashier itself.

With the standard form, both things are true if both modules derive their
concept from a **shared concept**. That shared concept may belong to anyone.
In this case its owner is the rental community (`komunitas-sewa`), because
Rental is needed by one domain only, so it is not in the vocabulary yet
(`content/README.md` §3). Rudi's rental and SewaPro's order both count as
Rental (CONCEPT-12). So one rule calculates both, and the shared return
accepts both (VALUE-16).

The third cashier, SewaKilat, does not use the shared concept. Its return
points to its own order, so Rudi's rental is rejected there, exactly as in the
prototype. The form cannot force two makers who do not know each other to use
the same concept. The form only provides a place for the shared concept.

```uniti
module komunitas-sewa/base@v1
  uses uniti/item@v1

concept Rental
concept Return

property quantity : number (level)
property rental : reference Rental

applies to Rental:
  item         required
  quantity     required

applies to Return:
  rental       required

computed Item.currently_rented : number (level), closed:
  sum(all(Rental, s: s.item = this
                    and count(all(Return, k: k.rental = s)) = 0),
      s: s.quantity)

module rudi/rental@v1
  uses komunitas-sewa/base@v1

concept EquipmentRental
  label.en     Equipment rental
  parent       Rental

module sewapro/cashier@v1
  uses komunitas-sewa/base@v1

concept Order
  label.en     Rental order
  parent       Rental

module sewakilat/cashier@v1
  uses uniti/item@v1

concept Booking
concept GiveBack

property booking : reference Booking

applies to GiveBack:
  booking      required

module kemah-ceria/shop@v1
  uses uniti/item@v1
  uses komunitas-sewa/base@v1
  uses rudi/rental@v1
  uses sewapro/cashier@v1
  uses sewakilat/cashier@v1

example tents_out_two_modules
  kind         compute
  title        Tents currently out, from the old module and the new cashier
  explanation  Two tents were rented through Rudi's module on 1 October,
               before the shop moved cashier. One tent was rented through
               SewaPro on 6 October. On 7 October there are 3 tents
               currently out.
  zone         WIB
  facts        recorded 7 Oct 2026 09:00
    tent   type      Item              valid 1 Jan 2026
    r1     type      EquipmentRental   valid 1 Oct 2026
    r1     item      tent              valid 1 Oct 2026
    r1     quantity  2                 valid 1 Oct 2026
    p1     type      Order             valid 6 Oct 2026
    p1     item      tent              valid 6 Oct 2026
    p1     quantity  1                 valid 6 Oct 2026
  ask          tent.currently_rented   T: 7 Oct 2026   R: 7 Oct 2026 18:00
  result       3

example return_through_new_cashier
  kind         accept
  title        Old rental returned through the new cashier
  explanation  Rudi's rental r1 is returned through SewaPro. A return points
               to Rental, and r1 counts as Rental because EquipmentRental is
               its child.
  zone         WIB
  facts        as in tents_out_two_modules
  action       recorded 8 Oct 2026 10:00, actor sari
    k1     type      Return   valid 8 Oct 2026
    k1     rental    r1       valid 8 Oct 2026
  result       accepted

example tents_out_after_return
  kind         compute
  title        Tents currently out after the old rental is returned
  explanation  After the two tents of rental r1 are returned on 8 October,
               only one tent is still out, from the SewaPro order.
  zone         WIB
  facts        recorded 8 Oct 2026 10:00
    tent   type      Item              valid 1 Jan 2026
    r1     type      EquipmentRental   valid 1 Oct 2026
    r1     item      tent              valid 1 Oct 2026
    r1     quantity  2                 valid 1 Oct 2026
    p1     type      Order             valid 6 Oct 2026
    p1     item      tent              valid 6 Oct 2026
    p1     quantity  1                 valid 6 Oct 2026
    k1     type      Return            valid 8 Oct 2026
    k1     rental    r1                valid 8 Oct 2026
  ask          tent.currently_rented   T: 9 Oct 2026   R: 9 Oct 2026 18:00
  result       1

example return_through_other_cashier
  kind         reject
  title        A cashier without the shared concept cannot accept an old rental
  explanation  SewaKilat does not use the shared concept Rental. Its return
               only points to its own Booking, so Rudi's rental r1 is
               rejected.
  zone         WIB
  facts        as in tents_out_two_modules
  action       recorded 8 Oct 2026 10:00, actor sari
    x1     type     GiveBack  valid 8 Oct 2026
    x1     booking  r1        valid 8 Oct 2026
  result       rejected by VALUE-16, entity x1
```

Rentals that are already recorded do not need to be moved or changed when the
shop moves cashier. The new cashier only adds. Rudi's module stays installed,
because the statement that EquipmentRental is a child of Rental only applies to
an organization that installs its module (RELATION-5). If Rudi's module is
removed, r1 is no longer read as a Rental.
