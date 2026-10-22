# Manufacturing

Cases M1 and M2 of the paper test (Indonesian archive, `uji/01-hitung.md`
§4.I), written in the reference notation. Both are level 3: the rule uses
itself for another entity, namely its components.

## M1. Material needs from a multi-level structure

```uniti
module paper/m1@v1

concept Item
concept BomLine
concept ProductionOrder

property assembly : reference Item
property component : reference Item
property amount : number (position)
property product : reference Item

applies to BomLine:
  assembly     required
  component    required
  amount       required

applies to ProductionOrder:
  product      required
  amount       required

helper Item.base_materials : collection:
  let lines = all(BomLine, b: b.assembly = this)
  if count(lines) = 0
  then [{item: this, amount: 1}]
  else each(group(each_merged(lines, b: scale(b.component.base_materials, b.amount)),
                  by: x: x.item),
            g: {item: g.key, amount: sum(g.members, x: x.amount)})

helper scale(entries, n) : collection:
  each(entries, x: x with amount = x.amount × n)

helper ProductionOrder.needs : collection:
  scale(this.product.base_materials, this.amount)

computed ProductionOrder.material_need(item) : number (position), closed:
  sum(this.needs, x: if x.item = item then x.amount else 0)

example pipes_for_ten_bicycles
  kind         compute
  title        Pipes for ten bicycles
  explanation  Bicycle = 1 frame + 2 wheels; frame = 4 pipes; wheel = 1 tire +
               32 spokes. One bicycle needs 4 pipes, so 10 bicycles need 40.
  facts        recorded 1 Oct 2026
    bicycle  type       Item              valid 1 Jan 2026
    frame    type       Item              valid 1 Jan 2026
    wheel    type       Item              valid 1 Jan 2026
    pipe     type       Item              valid 1 Jan 2026
    tire     type       Item              valid 1 Jan 2026
    spoke    type       Item              valid 1 Jan 2026
    b1       type       BomLine           valid 1 Jan 2026
    b1       assembly   bicycle           valid 1 Jan 2026
    b1       component  frame             valid 1 Jan 2026
    b1       amount     1                 valid 1 Jan 2026
    b2       type       BomLine           valid 1 Jan 2026
    b2       assembly   bicycle           valid 1 Jan 2026
    b2       component  wheel             valid 1 Jan 2026
    b2       amount     2                 valid 1 Jan 2026
    b3       type       BomLine           valid 1 Jan 2026
    b3       assembly   frame             valid 1 Jan 2026
    b3       component  pipe              valid 1 Jan 2026
    b3       amount     4                 valid 1 Jan 2026
    b4       type       BomLine           valid 1 Jan 2026
    b4       assembly   wheel             valid 1 Jan 2026
    b4       component  tire              valid 1 Jan 2026
    b4       amount     1                 valid 1 Jan 2026
    b5       type       BomLine           valid 1 Jan 2026
    b5       assembly   wheel             valid 1 Jan 2026
    b5       component  spoke             valid 1 Jan 2026
    b5       amount     32                valid 1 Jan 2026
    po       type       ProductionOrder   valid 1 Oct 2026
    po       product    bicycle           valid 1 Oct 2026
    po       amount     10                valid 1 Oct 2026
  ask          po.material_need(pipe)   T: 1 Oct 2026   R: 1 Oct 2026
  result       40

example tires_for_ten_bicycles
  kind         compute
  title        Tires for ten bicycles
  explanation  One bicycle needs 2 wheels, each with 1 tire: 2 × 10 = 20.
  facts        as in pipes_for_ten_bicycles
  ask          po.material_need(tire)   T: 1 Oct 2026   R: 1 Oct 2026
  result       20

example spokes_for_ten_bicycles
  kind         compute
  title        Spokes for ten bicycles
  explanation  One bicycle needs 2 × 32 = 64 spokes: 64 × 10 = 640.
  facts        as in pipes_for_ten_bicycles
  ask          po.material_need(spoke)   T: 1 Oct 2026   R: 1 Oct 2026
  result       640

example cyclic_structure
  kind         compute
  title        Wheel recorded as needing a bicycle
  explanation  Bicycle → wheel → bicycle. The result is not computable because
               of a cycle, not because the calculation gets stuck.
  facts        as in pipes_for_ten_bicycles
    b6       type       BomLine           valid 1 Jan 2026   recorded 1 Oct 2026
    b6       assembly   wheel             valid 1 Jan 2026   recorded 1 Oct 2026
    b6       component  bicycle           valid 1 Jan 2026   recorded 1 Oct 2026
    b6       amount     1                 valid 1 Jan 2026   recorded 1 Oct 2026
  ask          po.material_need(pipe)   T: 1 Oct 2026   R: 1 Oct 2026
  result       not computable: cycle
```

## M2. Multi-level standard cost

This module uses module M1, adds its own cost for each item, and uses the same
structure facts.

```uniti
module paper/m2@v1
  uses paper/m1@v1

property own_cost : number (money, position)

applies to Item:
  own_cost

computed Item.standard_cost : number (money, position), closed:
  this.own_cost
  + sum(all(BomLine, b: b.assembly = this), b: b.amount × b.component.standard_cost)

example wheel_cost
  kind         compute
  title        Standard cost of the wheel
  explanation  80,000 + 32 × 2,000 + 20,000 = 164,000.
  facts        as in pipes_for_ten_bicycles
    pipe     own_cost  50,000 IDR    valid 1 Jan 2026   recorded 1 Oct 2026
    tire     own_cost  80,000 IDR    valid 1 Jan 2026   recorded 1 Oct 2026
    spoke    own_cost  2,000 IDR     valid 1 Jan 2026   recorded 1 Oct 2026
    wheel    own_cost  20,000 IDR    valid 1 Jan 2026   recorded 1 Oct 2026
    frame    own_cost  100,000 IDR   valid 1 Jan 2026   recorded 1 Oct 2026
    bicycle  own_cost  150,000 IDR   valid 1 Jan 2026   recorded 1 Oct 2026
  ask          wheel.standard_cost   T: 1 Oct 2026   R: 1 Oct 2026
  result       164,000 IDR

example frame_cost
  kind         compute
  title        Standard cost of the frame
  explanation  4 × 50,000 + 100,000 = 300,000.
  facts        as in wheel_cost
  ask          frame.standard_cost   T: 1 Oct 2026   R: 1 Oct 2026
  result       300,000 IDR

example bicycle_cost
  kind         compute
  title        Standard cost of the bicycle
  explanation  300,000 + 2 × 164,000 + 150,000 = 778,000.
  facts        as in wheel_cost
  ask          bicycle.standard_cost   T: 1 Oct 2026   R: 1 Oct 2026
  result       778,000 IDR
```
