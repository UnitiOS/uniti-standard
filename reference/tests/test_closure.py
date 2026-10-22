"""Tests for decision 0057 (closure before the lock): T2 to T7, T9, T11c.

T1 and the examples are in conformance/21-closure.md.
"""

import datetime as dt
import unittest

from calculator import operations as op
from calculator.compute import Evaluator, FactStore
from calculator.module_set import ModuleSet
from calculator.reader import read
from calculator.values import (
    EMPTY, Entity, NotComputable, NotationError, parse_number, parse_unit, UTC,
)
from tests.test_compute import status


def a(text):
    return parse_number(text)


class UnitPower(unittest.TestCase):
    """0057 T2 (A22): a unit code reaches the power 3 or -3 at most."""

    def test_four_lengths_multiplied(self):
        cube = op.multiply(op.multiply(a("2 cm"), a("3 cm")), a("4 cm"))
        self.assertEqual(str(cube), "24 cm³")
        with self.assertRaises(NotComputable) as e:
            op.multiply(cube, a("5 cm"))
        self.assertEqual(e.exception.kind, "unit mismatch")

    def test_divided_below_minus_three(self):
        rate = op.divide(a("1"), op.multiply(op.multiply(a("1 cm"), a("1 cm")), a("1 cm")))
        self.assertEqual(str(rate.unit), "1/cm³")
        with self.assertRaises(NotComputable) as e:
            op.divide(rate, a("1 cm"))
        self.assertEqual(e.exception.kind, "unit mismatch")

    def test_power(self):
        self.assertEqual(str(op.power(a("2 cm"), a("3")).unit), "cm³")
        with self.assertRaises(NotComputable) as e:
            op.power(a("2 cm"), a("4"))
        self.assertEqual(e.exception.kind, "unit mismatch")

    def test_power_three_is_reached_but_not_passed(self):
        cube = op.power(a("2 cm"), a("3"))
        self.assertEqual(str(op.divide(cube, a("1 cm²")).unit), "cm")


class UnitOf(unittest.TestCase):
    """0057 T3 (A23) and T4 (A24)."""

    def test_compound_unit_is_unit_mismatch(self):
        with self.assertRaises(NotComputable) as e:
            op.unit_of(a("50,000 IDR/day"))
        self.assertEqual(e.exception.kind, "unit mismatch")

    def test_power_of_a_code_is_unit_mismatch(self):
        with self.assertRaises(NotComputable) as e:
            op.unit_of(a("5 m²"))
        self.assertEqual(e.exception.kind, "unit mismatch")

    def test_number_without_unit_is_empty(self):
        self.assertIs(op.unit_of(a("5")), EMPTY)

    def test_single_code_still_a_choice(self):
        self.assertEqual(op.unit_of(a("5 kg")), op.unit_as_choice(parse_unit("kg")))


class TieBreaker(unittest.TestCase):
    """0057 T5 (A25)."""

    def test_entity_without_type_has_no_place(self):
        evaluator = Evaluator(ModuleSet([]), [], FactStore([]),
                              dt.datetime(2026, 10, 1, tzinfo=UTC))
        with self.assertRaises(NotComputable) as e:
            evaluator.tie_key(Entity("x"), dt.date(2026, 10, 1))
        self.assertEqual(e.exception.kind, "undefined order")


PHONES = """
module ref/phones@v1

concept Person
concept Report
property phone : text, many
property rate : number (money, position)
property boss : reference Person

applies to Person:
  phone
  rate

applies to Report:
  boss

computed Report.count_phones : number (position), closed:
  count(history(this.boss.phone, in: range(1 Jan 2026, 1 Jan 2027)))

computed Report.count_rates : number (position), closed:
  count(history(this.boss.rate, in: range(1 Jan 2026, 1 Jan 2027)))

computed Report.folded : number (position), closed:
  fold(history(this.boss.phone, in: range(1 Jan 2026, 1 Jan 2027)),
       initial: 0, step: (s, p): s + 1)

computed Report.has_history : yes_no, closed:
  exists(history(this.boss.rate, in: range(1 Jan 2026, 1 Jan 2027)))

example NAME
  kind         compute
  title        History
  explanation  History of a person.
  zone         WIB
  facts        recorded 1 Jan 2026
    p     type    Person   valid 1 Jan 2026
    f1: p phone   "0811"   valid 1 Jan 2026
    p     phone   "0855"   valid 1 Mar 2026
    p     rate    5 IDR    valid 1 Jan 2026
    r     type    Report   valid 1 Jan 2026
BOSS
  ask          r.PROP   T: 1 Feb 2026   R: 1 Feb 2026
  result       RESULT
"""


def phones(name, prop, result, boss="    r     boss    p        valid 1 Jan 2026"):
    text = (PHONES.replace("NAME", name).replace("PROP", prop)
            .replace("RESULT", result).replace("BOSS", boss))
    return status(text)[name]


class History(unittest.TestCase):
    """0057 T6 (A26) and T7 (A27)."""

    def test_empty_reference_gives_empty(self):
        self.assertEqual(phones("e", "has_history", "no", boss="")[0], "passed")
        self.assertEqual(phones("e", "has_history", "yes", boss="")[0], "failed")

    def test_many_values_are_records_in_a_collection_with_no_order(self):
        self.assertEqual(phones("m", "count_phones", "2")[0], "passed")

    def test_one_value_stays_one_record(self):
        self.assertEqual(phones("o", "count_rates", "1")[0], "passed")

    def test_fold_over_many_values_needs_order_by(self):
        self.assertEqual(phones("f", "folded", "2")[0], "notation error")


LATER = """
module ref/later@v1

concept Person
concept Customer
property name : text
property phone : text

applies to Person:
  name

applies to Customer:
  name         required
  phone        required

example NAME
  kind         KIND
  title        Required later
  explanation  Old records.
  zone         WIB
  facts        recorded 1 Mar 2026 09:00
    p1       type   Person     valid 1 Mar 2026
    f1: p1   name   "Mari"     valid 1 Mar 2026
    c1       type   Customer   valid 1 Mar 2026
    f2: c1   name   "Alex"     valid 1 Mar 2026
  action       recorded 20 Oct 2026 10:00
ACTION
  result       RESULT
"""


def later(name, action, result, kind="reject"):
    text = (LATER.replace("NAME", name).replace("KIND", kind)
            .replace("ACTION", action).replace("RESULT", result))
    return status(text)[name]


class OldGap(unittest.TestCase):
    """0057 T11c: CONCEPT-18 and an old gap."""

    def test_old_gap_does_not_block(self):
        action = '    c1   name   "Alexa"   valid 1 Mar 2026   corrects f2'
        self.assertEqual(later("g", action, "accepted", "accept")[0], "passed")

    def test_new_entity_must_be_complete(self):
        action = ('    c2   type   Customer   valid 20 Oct 2026\n'
                  '    c2   name   "Sam"      valid 20 Oct 2026')
        self.assertEqual(later("n", action, "rejected by CONCEPT-18, entity c2")[0], "passed")

    def test_entity_that_gets_the_type_through_the_action_must_be_complete(self):
        action = '    p1   type   Customer   valid 20 Oct 2026'
        self.assertEqual(later("t", action, "rejected by CONCEPT-18, entity p1")[0], "passed")

    def test_gap_made_by_the_action_blocks(self):
        action = '    c1   name   valid 1 Mar 2026   retracts f2'
        self.assertEqual(later("r", action, "rejected by CONCEPT-18, entity c1")[0], "passed")


MODULES = """
module ref/item@v1
concept Item

module ref/item@v2
concept Item

module ref/cashier@v1
  uses ref/item@v1

module ref/warehouse@v1
  uses ref/item@v2

module ref/shop@v1
  uses ref/cashier@v1
  uses ref/warehouse@v1
"""


class OneVersion(unittest.TestCase):
    """0057 T9: an organization has at most one version of each module."""

    def test_two_versions_are_refused_naming_both(self):
        module_set = ModuleSet(read(MODULES))
        shop = next(m for m in module_set.all_modules() if m.address == "ref/shop")
        with self.assertRaises(NotationError) as e:
            module_set.installed_modules(shop)
        for text in ("ref/item", "v1", "v2"):
            self.assertIn(text, str(e.exception))


if __name__ == "__main__":
    unittest.main()
