# 0041. Numbers in calculation: exact fractions, written rounding, units count

Date: 2026-10-19
Status: partly replaced by 0045. `allocate` and the rounding modes become
content of the calculation library, and fractional power leaves the operation
list.

**Context**
The paper test (Indonesian archive, `uji/01-hitung.md`,
findings T7 to T10) showed that decimal numbers alone are not enough:
1,000,000 ÷ 3 cannot be written as a terminating decimal, and divisions that
are rounded separately lose or add one rupiah.

**Decision**
- Inside rules, numbers are calculated as **exact fractions**.
- The value of a computed property must be writable as a terminating
  decimal. If it is not, the rule must round; without that, the result is
  not computable.
- Rounding always names the multiple and the mode. Where the rounding takes
  place, per line or at the end, is content and must be written.
- `allocate` divides with nothing lost, with a stated way of giving out the
  remainder.
- `power` with an exponent that is not a whole number must state its
  precision.
- Units count in the calculation: add, subtract, and compare only for the
  same unit; multiply and divide combine units.

**Alternatives**
- *Decimals with a fixed number of digits after the point.* Rejected: two
  implementations with different precision give different numbers, and the
  order of summing can change the result.
- *Automatic rounding by currency.* Postponed as an open question, together
  with the precision of numbers in `form/03-values.md`.

**Consequences**
- The machine reports rules that use division without rounding at the end.
- A daily rate has the unit money per day, so rate × span has the unit money.
