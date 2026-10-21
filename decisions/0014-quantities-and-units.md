# 0014. Quantity on the property, unit on the value

Date: 2026-10-17
Status: accepted

**Context**
A price can be in rupiah or dollars, a weight in kilograms or grams. It must be
decided where the unit is written: once on the property, or on every value.

**Decision**
- A number property **may set one quantity** (money, mass, duration, ...).
- When a quantity is set, **every value must carry a unit** of that quantity,
  for example `150,000 IDR` or `10 USD`.
- Quantities and units are taken from established code lists: ISO 4217 for
  currencies, UCUM for other units.
- **There is no automatic conversion.** Conversion is a calculation rule; an
  exchange rate is recorded as a fact.

**Alternatives**
- *A fixed unit per property* ("price is always in rupiah"). Rejected: an
  organization with two currencies would have to make two properties for the
  same meaning, and the vocabulary could not be used across countries.
- *A free unit on every value without a quantity on the property.* Rejected:
  the machine could not reject nonsensical values, such as "price = 5 kg".

**Consequences**
- Reports across currencies always state the exchange rate they use, because
  an exchange rate is a fact with provenance.
