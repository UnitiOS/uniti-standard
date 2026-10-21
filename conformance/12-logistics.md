# Logistics

Case X1 of the paper test (`uji/01-hitung.md`)<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.L, written in the reference notation with the core and the calculation
library.

## X1. Shipping cost with volumetric weight

The unit is part of the calculation: cm × cm × cm ÷ (cm³/kg) = kg.

```uniti
module paper/x1@v1
  uses uniti/calc@v1

concept Service
concept Package

property rate_per_kg : number (money/mass, level)
property service : reference Service
property weight : number (mass, level)
property length : number (length, level)
property width : number (length, level)
property height : number (length, level)

applies to Service:
  rate_per_kg required

applies to Package:
  service      required
  weight       required
  length       required
  width        required
  height       required

computed Package.shipping_cost : number (money, increase), closed:
  let volumetric = this.length × this.width × this.height ÷ 5,000 cm³/kg
  round(max(this.weight, volumetric), 0.5 kg, up) × this.service.rate_per_kg

example volumetric_weight
  kind         compute
  title        Volumetric weight is larger
  explanation  Weight 2.3 kg, size 40 × 30 × 20 cm. Volumetric 24,000 cm³ ÷
               5,000 = 4.8 kg, rounded up to 5 kg.
               5 × 9,000 = 45,000.
  zone         WIB
  facts        recorded 6 Oct 2026 09:00
    regular  type          Service         valid 1 Jan 2026
    regular  rate_per_kg   9,000 IDR/kg    valid 1 Jan 2026
    k1       type          Package         valid 6 Oct 2026
    k1       service       regular         valid 6 Oct 2026
    k1       weight        2.3 kg          valid 6 Oct 2026
    k1       length        40 cm           valid 6 Oct 2026
    k1       width         30 cm           valid 6 Oct 2026
    k1       height        20 cm           valid 6 Oct 2026
  ask          k1.shipping_cost   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       45,000 IDR
```
