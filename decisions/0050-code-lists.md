# 0050. Code lists

Date: 2026-10-20
Status: accepted

**Context**
According to `03` §2.3, a unit is a choice from a code list, so a unit can
also be a value, for example the original currency of an exchange rate. That
list did not yet have an address, so property cards and examples could not
name it (finding A29, case K2).

When the list was written in `content/code-lists` in stage 6, a gap in the
form appeared (I1). Codes from an outside standard are used exactly (P8), for
example `IDR` and `USD`. But choice names must be lowercase (ADDRESS-2). The
codes also cannot be made lowercase, because UCUM tells uppercase from
lowercase: `mm` is millimeter and `Mm` is megameter.

Experiment: the list `uniti/unit/Unit` was written as a code list, and K2
was written again as in the paper test, with an exchange rate that has an
original and a target currency as choices. All examples passed, and no new
way of writing was needed except one word in the header line of the list.

**Decision**
1. A **code list** is a third kind of list, besides open and closed. A code
   list is written `choice_list Unit, code`. A code list is always closed,
   and the names of its choices are the codes of its outside standard,
   written exactly, including uppercase and lowercase.
2. **The address of a code list choice** has the same structure as other
   choices: the module address, then its code, for example `uniti/unit/IDR`.
   For a code list, a choice name may contain uppercase letters. Its code may
   contain only basic Latin letters and digits.
3. **The unit list** is `uniti/unit/Unit` in `content/code-lists`. It holds
   ISO 4217 currency codes, UCUM unit codes, and two codes owned by Uniti:
   calendar `month` and `year`. `unit_of(n)` gives a choice from this list.
   Codes are chosen because they are needed, and new codes are added through
   a new version of the list. That is a change of content, not of form.
4. **How to write units in the reference notation.** The five old time units
   are written with Indonesian names: `detik`, `menit`, `jam`, `hari`, and
   `minggu`, for the UCUM codes `s`, `min`, `h`, `d`, and `wk`. Other units are
   written with their codes. The time zone names `WIB`, `WITA`, and `WIT` are
   also ways of writing. Other time zones are written as an offset from UTC.
   Appendix A §2.4 is no longer marked [provisional].
5. **Calendar months and years are not `mo` and `a`.** In UCUM both are
   average lengths, 30.4375 days and 365.25 days. The equivalent written in
   appendix A §2.4 is wrong, and is removed (I2).
6. Postponed under 0046, because no case needs them yet:
   - the version of the code list that applies to a module that writes units
     without using `uniti/unit`. Until decided, examples use only codes that
     exist in the first version;
   - codes that contain marks other than letters and digits, for example
     UCUM `[in_i]`;
   - the address of the list of languages and countries.

**Alternatives**
- *Codes written in lowercase, `idr`.* Rejected: UCUM tells uppercase from
  lowercase, and the code would no longer be the same as its outside
  standard.
- *Indonesian names as codes, `uniti/unit/hari`, with a bridge to UCUM.*
  Rejected: the code list would be made again (P8), and a permanent address
  would be tied to one language. Indonesian names are still used as a way of
  writing.
- *ADDRESS-2 relaxed for all choices.* Rejected: only code lists need it.
- *A value from a code list without an address, as a pair of standard and
  code.* Rejected: the value of a choice must be an address (VALUE-14), so a
  new value form would be needed.

**Consequences**
- `form/02-addresses.md` §2.4: letters for code list choices.
- `form/03-values.md` §2.3 and §2.6: the code list as a third kind of list,
  and the address of the unit list. VALUE-12 is adjusted.
- `form/06-calculation-rules.md` §2.5: `unit_of(n)` gives a choice from
  `uniti/unit/Unit`.
- `appendix/A-notation.md` §2.4, §2.8, NOTATION-8, and §8 question 4.
- `content/code-lists.md`: the list of units and quantities.
- The reference calculator reads code lists, checks VALUE-13, and runs K2
  with an exchange rate whose currencies are choices. A29 is finished.
