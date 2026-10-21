"""Tests for the operations in 06-calculation-rules §2.5 to §2.9.

The numbers are taken from the paper test when there is one, plus the
boundary points that were not tested yet according to the review of the
paper test §5.
"""

import datetime as dt
import unittest
from fractions import Fraction

from calculator import operations as op
from calculator.values import (
    EMPTY, Number, NotDefined, Entity, NotationError, Collection, Choice,
    Record, Range, NotComputable, parse_number, parse_unit, parse_time, parse_zone,
)

WIB = parse_zone("WIB")


def a(text):
    return parse_number(text)


def t(text):
    return parse_time(text, WIB)


def k(*members, ordered=True):
    return Collection(tuple(members), ordered)


class TestBase(unittest.TestCase):
    def assertNotComputable(self, kind, function, *args):
        with self.assertRaises(NotComputable) as cm:
            function(*args)
        self.assertEqual(cm.exception.kind, kind)


class Arithmetic(TestBase):
    """CALC-20 and CALC-24; 06 §2.8."""

    def test_exact_fraction(self):
        third = op.divide(a("1,000,000"), a("3"))
        self.assertEqual(third.value, Fraction(1000000, 3))
        self.assertEqual(op.multiply(third, a("3")), a("1,000,000"))

    def test_unit_is_computed_along(self):
        period = op.make_range(t("6 Oct 2026"), t("9 Oct 2026"), WIB)
        days = op.span(period, parse_unit("day"), WIB)
        self.assertEqual(op.multiply(a("50,000 IDR/day"), days), a("150,000 IDR"))
        self.assertEqual(op.divide(days, a("1 day")), a("3"))

    def test_volumetric_weight(self):
        """X1: 40 × 30 × 20 cm ÷ 5.000 cm³/kg = 4,8 kg."""
        volume = op.multiply(op.multiply(a("40 cm"), a("30 cm")), a("20 cm"))
        self.assertEqual(op.divide(volume, a("5,000 cm³/kg")), a("4.8 kg"))

    def test_add_requires_same_unit(self):
        self.assertNotComputable("unit mismatch", op.add,
                                 a("10 USD"), a("5,000 IDR"), WIB)
        self.assertNotComputable("unit mismatch", op.add,
                                 a("1 kg"), a("500 g"), WIB)

    def test_zero_without_unit_follows_its_partner(self):
        self.assertEqual(op.add(a("0"), a("5 IDR"), WIB), a("5 IDR"))
        self.assertTrue(op.compare("≤", a("0"), a("5 IDR"), WIB))
        self.assertNotComputable("unit mismatch", op.add,
                                 a("1"), a("5 IDR"), WIB)

    def test_division_by_zero(self):
        self.assertNotComputable("division by zero", op.divide, a("5"), a("0 IDR"))

    def test_empty_used_in_computation(self):
        self.assertNotComputable("empty value", op.add, EMPTY, a("1"), WIB)
        self.assertNotComputable("empty value", op.compare, "=", EMPTY, a("1"), WIB)


class Power(TestBase):
    """06 §2.5: power with a whole number."""

    def test_whole_number(self):
        self.assertEqual(op.power(a("1.01"), a("2")), a("1.0201"))
        self.assertEqual(op.power(a("3 cm"), a("3")), a("27 cm³"))
        self.assertEqual(op.power(a("2"), a("−2")), a("0.25"))
        self.assertNotComputable("division by zero", op.power, a("0"), a("−1"))

    def test_not_a_whole_number(self):
        """A fractional power is not part of the core (decision 0045)."""
        with self.assertRaises(NotationError):
            op.power(a("2"), a("0.5"))
        with self.assertRaises(NotationError):
            op.power(a("2"), a("2 kg"))


class FloorMultiple(TestBase):
    """CALC-56. The ways of rounding that use it are tested in test_library."""

    def test_largest_multiple_not_above(self):
        self.assertEqual(op.floor_multiple(a("4.8 kg"), a("0.5 kg")), a("4.5 kg"))
        self.assertEqual(op.floor_multiple(a("5 kg"), a("0.5 kg")), a("5 kg"))
        self.assertEqual(op.floor_multiple(a("0.125"), a("0.01")), a("0.12"))

    def test_negative(self):
        """06 §2.5: floor_multiple(−4.8 kg, of: 0.5 kg) = −5 kg."""
        self.assertEqual(op.floor_multiple(a("−4.8 kg"), a("0.5 kg")), a("−5 kg"))
        self.assertEqual(op.floor_multiple(a("−5 kg"), a("0.5 kg")), a("−5 kg"))

    def test_units_must_match(self):
        self.assertNotComputable("unit mismatch", op.floor_multiple,
                                 a("4.8 kg"), a("1 IDR"))
        self.assertEqual(op.floor_multiple(a("0"), a("1 IDR")), a("0 IDR"))

    def test_multiple_must_be_above_zero(self):
        for to in ("0", "−1"):
            with self.assertRaises(NotationError):
                op.floor_multiple(a("5"), a(to))


class Summaries(TestBase):
    """06 §2.5, the Summaries group; paper test C2."""

    WAIT = ["10 minutes", "25 minutes", "15 minutes", "40 minutes", "20 minutes"]

    def test_empty_collection(self):
        self.assertEqual(op.sum_values([]), a("0"))
        self.assertEqual(op.count(k()), a("0"))
        self.assertTrue(op.all_match([]))
        self.assertFalse(op.any_match([]))
        for f in (op.smallest, op.largest):
            self.assertNotComputable("empty collection", f, [], WIB)

    def test_sum_c2(self):
        self.assertEqual(op.sum_values([a(x) for x in self.WAIT]), a("110 minutes"))

    def test_min_two_values_and_time(self):
        self.assertEqual(op.smallest([a("4,800,000 IDR"), a("1,200,000 IDR")], WIB),
                         a("1,200,000 IDR"))
        self.assertEqual(op.largest([t("1 Oct 2026"), t("5 Oct 2026")], WIB),
                         t("5 Oct 2026"))

    def test_chosen_zero_follows_unit(self):
        """06 §2.8; paper test G2: max(0, h.hours − 8 hours)."""
        for result in (op.largest([a("0"), a("−2 hours")], WIB),
                       op.largest([a("0"), a("0 hours")], WIB),
                       op.smallest([a("0 hours"), a("0")], WIB)):
            self.assertTrue(op.identical(result, a("0 hours")), result)
        self.assertTrue(op.identical(op.largest([a("0"), a("3 hours")], WIB), a("3 hours")))

    def test_sum_mixed_units(self):
        self.assertNotComputable("unit mismatch", op.sum_values,
                                 [a("1 IDR"), a("1 USD")])

    def test_all_match_with_empty(self):
        self.assertNotComputable("empty value", op.all_match, [False, EMPTY])

    def test_single(self):
        self.assertEqual(op.single(k(a("16,200"))), a("16,200"))
        self.assertNotComputable("not single", op.single, k())
        self.assertNotComputable("not single", op.single, k(a("1"), a("2")))


class Select(TestBase):
    """06 §2.5, the Compare group; decision 0043 item 3."""

    def test_less_than_or_equal_boundary_o2(self):
        """A boundary not yet tested in O2: a purchase of exactly 10,000,000."""
        self.assertTrue(op.compare("≤", a("10,000,000 IDR"), a("10,000,000 IDR"), WIB))
        self.assertFalse(op.compare("≤", a("10,000,001 IDR"), a("10,000,000 IDR"), WIB))

    def test_records_equal(self):
        draft, submitted = Choice("example/doc/draft"), Choice("example/doc/submitted")
        r1 = Record({"from": draft, "to": submitted})
        r2 = Record({"to": submitted, "from": draft})
        self.assertTrue(op.equals(r1, r2, WIB))
        self.assertFalse(op.equals(r1, Record({"from": draft}), WIB))

    def test_status_transition_o3(self):
        draft, submitted, posted = (Choice(f"example/doc/{n}")
                                     for n in ("draft", "submitted", "posted"))
        allowed = k(Record({"from": draft, "to": submitted}))
        self.assertTrue(op.within(Record({"from": draft, "to": submitted}), allowed, WIB))
        self.assertFalse(op.within(Record({"from": draft, "to": posted}), allowed, WIB))

    def test_ordered_collections_equal(self):
        self.assertTrue(op.equals(k(a("1"), a("2")), k(a("1"), a("2")), WIB))
        self.assertFalse(op.equals(k(a("1"), a("2")), k(a("2"), a("1")), WIB))

    def test_unordered_collections_equal(self):
        """06 §2.5: equal regardless of order,
        with the same number of occurrences."""
        self.assertTrue(op.equals(k(a("1"), a("2"), ordered=False),
                                  k(a("2"), a("1"), ordered=False), WIB))
        self.assertTrue(op.equals(k(a("1"), a("2")), k(a("2"), a("1"), ordered=False), WIB))
        self.assertFalse(op.equals(k(a("1"), a("1"), a("2"), ordered=False),
                                   k(a("1"), a("2"), a("2"), ordered=False), WIB))
        self.assertFalse(op.equals(k(a("1"), ordered=False), k(ordered=False), WIB))

    def test_different_types(self):
        with self.assertRaises(NotationError):
            op.equals(a("1"), True, WIB)

    def test_entities_compared_by_identifier(self):
        self.assertTrue(op.equals(Entity("h1", "tent"), Entity("h1", "other name"), WIB))
        self.assertFalse(op.equals(Entity("h1"), Entity("h2"), WIB))


class Time(TestBase):
    """CALC-26; 06 §2.7."""

    def test_half_open_range(self):
        r = op.make_range(t("10 Oct 2026"), t("13 Oct 2026"), WIB)
        self.assertTrue(op.within(t("10 Oct 2026"), r, WIB))
        self.assertTrue(op.within(t("12 Oct 2026"), r, WIB))
        self.assertFalse(op.within(t("13 Oct 2026"), r, WIB))

    def test_boundary_day_p1(self):
        """A boundary not yet tested in P1: a rental from 5 to 8 Oct no longer
        counts on 8 Oct."""
        period = op.make_range(t("5 Oct 2026"), t("8 Oct 2026"), WIB)
        self.assertTrue(op.within(t("7 Oct 2026"), period, WIB))
        self.assertFalse(op.within(t("8 Oct 2026"), period, WIB))

    def test_boundary_day_r1(self):
        """A boundary not yet tested in R1: points that expire on 15 Jan 2027 are
        no longer valid on that day."""
        valid = op.make_range(t("15 Jan 2026"), t("15 Jan 2027"), WIB)
        self.assertTrue(op.within(t("14 Jan 2027"), valid, WIB))
        self.assertFalse(op.within(t("15 Jan 2027"), valid, WIB))

    def test_overlap(self):
        r1 = op.make_range(t("10 Oct 2026"), t("13 Oct 2026"), WIB)
        r2 = op.make_range(t("13 Oct 2026"), t("15 Oct 2026"), WIB)
        r3 = op.make_range(t("12 Oct 2026"), t("14 Oct 2026"), WIB)
        self.assertIs(op.overlap(r1, r2, WIB), EMPTY)
        self.assertEqual(op.overlap(r1, r3, WIB), Range(t("12 Oct 2026"), t("13 Oct 2026")))

    def test_range_parts(self):
        r = op.make_range(t("1 Jan 2026"), t("1 Feb 2026"), WIB)
        self.assertEqual(op.get_part(r, "start"), t("1 Jan 2026"))
        self.assertEqual(op.get_part(r, "end"), t("1 Feb 2026"))

    def test_reversed_range(self):
        """06 §2.5."""
        self.assertNotComputable("reversed time", op.make_range,
                                 t("13 Oct 2026"), t("10 Oct 2026"), WIB)

    def test_add_month_at_month_end(self):
        self.assertEqual(op.add(t("31 Jan 2026"), a("1 month"), WIB), t("28 Feb 2026"))
        self.assertEqual(op.add(t("31 Jan 2028"), a("1 month"), WIB), t("29 Feb 2028"))
        self.assertEqual(op.add(t("1 Jan 2026"), a("36 months"), WIB), t("1 Jan 2029"))
        self.assertEqual(op.subtract(t("1 Mar 2026"), a("1 day"), WIB), t("28 Feb 2026"))

    def test_month_and_year_only_for_dates(self):
        """CALC-53."""
        self.assertNotComputable("unit mismatch", op.add,
                                 t("1 Oct 2026"), a("12 hours"), WIB)
        self.assertNotComputable("unit mismatch", op.add,
                                 t("1 Oct 2026 09:00"), a("1 month"), WIB)
        self.assertNotComputable("unit mismatch", op.add,
                                 t("1 Oct 2026"), a("1.5 months"), WIB)
        self.assertNotComputable("unit mismatch", op.difference,
                                 t("1 Oct 2026 09:00"), t("1 Dec 2026 09:00"),
                                 parse_unit("month"), WIB)
        self.assertEqual(op.add(t("1 Oct 2026"), a("2 weeks"), WIB), t("15 Oct 2026"))
        self.assertEqual(op.add(t("1 Oct 2026"), a("48 hours"), WIB), t("3 Oct 2026"))

    def test_span_whole_months(self):
        month = parse_unit("month")
        self.assertEqual(op.span(op.make_range(t("1 Jan 2026"), t("1 Jan 2029"), WIB), month, WIB),
                         a("36 months"))
        self.assertEqual(op.span(op.make_range(t("15 Jan 2026"), t("14 Feb 2026"), WIB), month, WIB),
                         a("0 months"))
        self.assertEqual(op.span(op.make_range(t("31 Jan 2026"), t("28 Feb 2026"), WIB), month, WIB),
                         a("1 month"))
        self.assertEqual(op.span(op.make_range(t("1 Jan 2026"), t("31 Dec 2027"), WIB),
                                 parse_unit("year"), WIB), a("1 year"))

    def test_difference_can_be_negative(self):
        """S4: returned earlier than promised."""
        self.assertEqual(op.difference(t("10 Oct 2026"), t("8 Oct 2026"), parse_unit("day"), WIB),
                         a("−2 days"))

    def test_instant_difference_in_minutes(self):
        self.assertEqual(op.difference(t("6 Oct 2026 08:00"), t("6 Oct 2026 08:25"),
                                       parse_unit("minute"), WIB), a("25 minutes"))

    def test_date_compared_with_instant(self):
        """03 §4: a new price from 1 November, a payment at 00:30 WITA."""
        payment = parse_time("1 Nov 2026 00:30 WITA")
        self.assertTrue(op.compare("≤", t("1 Nov 2026"), payment, parse_zone("WITA")))
        self.assertFalse(op.compare("≤", t("1 Nov 2026"), payment, parse_zone("WIB")))

    def test_monthly_split_k4(self):
        r = op.make_range(t("1 Jan 2026"), op.add(t("1 Jan 2026"), a("36 months"), WIB), WIB)
        slices = op.split(r, a("1 month"), WIB)
        self.assertTrue(slices.ordered)
        self.assertEqual(len(slices), 36)
        self.assertEqual(slices.members[0], Range(t("1 Jan 2026"), t("1 Feb 2026")))
        self.assertEqual(slices.members[-1], Range(t("1 Dec 2028"), t("1 Jan 2029")))

    def test_split_without_month_end_drift(self):
        r = op.make_range(t("31 Jan 2026"), t("31 Mar 2026"), WIB)
        slices = op.split(r, a("1 month"), WIB).members
        self.assertEqual(slices, (Range(t("31 Jan 2026"), t("28 Feb 2026")),
                                  Range(t("28 Feb 2026"), t("31 Mar 2026"))))

    def test_split_last_slice_stops_at_end(self):
        r = op.make_range(t("1 Oct 2026"), t("11 Oct 2026"), WIB)
        slices = op.split(r, a("1 week"), WIB).members
        self.assertEqual(slices[-1], Range(t("8 Oct 2026"), t("11 Oct 2026")))


class Convert(TestBase):
    """CALC-25; VALUE-7; 06 §2.5, the Unit group."""

    def test_fixed_units(self):
        self.assertEqual(op.convert(a("1 kg"), parse_unit("g")), a("1,000 g"))
        self.assertEqual(op.convert(a("36 hours"), parse_unit("day")), a("1.5 days"))
        self.assertEqual(op.convert(a("2 years"), parse_unit("month")), a("24 months"))
        self.assertEqual(op.convert(a("50,000 IDR/day"), parse_unit("IDR/hour")),
                         Number(Fraction(50000, 24), parse_unit("IDR/hour")))

    def test_month_and_day_cannot_be_converted(self):
        self.assertNotComputable("unit mismatch", op.convert,
                                 a("1 month"), parse_unit("day"))

    def test_currency_not_converted_in_core(self):
        """Decision 0045: the rate is a fact, so a currency is converted
        with `convert_money` in the calculation library."""
        self.assertEqual(op.convert(a("1,000,000 IDR"), parse_unit("IDR")), a("1,000,000 IDR"))
        self.assertNotComputable("unit mismatch", op.convert, a("100 USD"), parse_unit("IDR"))
        self.assertNotComputable("unit mismatch", op.convert,
                                 a("100 USD/day"), parse_unit("IDR/hour"))

    def test_unit_as_choice(self):
        """K2: k.from = unit_of(p.price)."""
        self.assertEqual(op.unit_of(a("100 USD")), op.unit_as_choice(parse_unit("USD")))
        self.assertNotEqual(op.unit_of(a("100 USD")), op.unit_of(a("100 IDR")))


class IntermediateValues(TestBase):
    """06 §2.5 and §2.6."""

    def test_record_with(self):
        r = Record({"quantity": a("10"), "price": a("100,000 IDR")})
        r2 = op.with_part(r, "quantity", a("5"))
        self.assertEqual(op.get_part(r2, "quantity"), a("5"))
        self.assertEqual(op.get_part(r, "quantity"), a("10"))
        with self.assertRaises(NotationError):
            op.with_part(r, "discount", a("1"))

    def test_part_of_empty(self):
        self.assertIs(op.get_part(EMPTY, "quantity"), EMPTY)

    def test_append(self):
        self.assertEqual(op.append_item(k(a("1")), a("2")), k(a("1"), a("2")))
        with self.assertRaises(NotationError):
            op.append_item(k(ordered=False), a("1"))

    def test_group_m1(self):
        pipe, tire = Entity("pipe"), Entity("tire")
        lines = [Record({"item": pipe, "quantity": a("4")}),
                 Record({"item": tire, "quantity": a("1")}),
                 Record({"item": tire, "quantity": a("1")})]
        result = op.group_by([(b, b.get("item")) for b in lines], True, WIB)
        self.assertFalse(result.ordered)
        totals = {g.get("key").identifier: op.sum_values([x.get("quantity") for x in
                                                        g.get("members").members])
                  for g in result.members}
        self.assertEqual(totals, {"pipe": a("4"), "tire": a("2")})

    def test_each_merged(self):
        self.assertEqual(op.merge([k(a("1")), k(), k(a("2"), a("3"))], True),
                         k(a("1"), a("2"), a("3")))


class Ordering(TestBase):
    """CALC-18; 06 §2.6 tie-breaker, entity as key, and members that are
    identical."""

    @staticmethod
    def tie_key(x):
        return (x.identifier,) if isinstance(x, Entity) else None

    def test_tie_broken_by_tie_breaker(self):
        """P2: two movements on the same date."""
        m1, m2, m3 = Entity("m1"), Entity("m2"), Entity("m3")
        pairs = [(m3, t("7 Oct 2026")), (m2, t("5 Oct 2026")), (m1, t("5 Oct 2026"))]
        self.assertEqual(op.sort_by_key(pairs, False, self.tie_key, WIB), [m1, m2, m3])

    def test_tie_not_entity(self):
        pairs = [(a("2"), a("1")), (a("1"), a("1"))]
        self.assertEqual(op.sort_by_key(pairs, True, self.tie_key, WIB), [a("2"), a("1")])
        self.assertNotComputable("undefined order", op.sort_by_key,  # CALC-18
                                 pairs, False, self.tie_key, WIB)

    def test_entity_as_key(self):
        """A record is ordered by the entity it names."""
        a1, a2 = Entity("a1"), Entity("a2")
        r1, r2 = Record({"room": a2}), Record({"room": a1})
        pairs = [(r1, a2), (r2, a1)]
        self.assertEqual(op.sort_by_key(pairs, False, self.tie_key, WIB), [r2, r1])

    def test_identical_needs_no_tie_breaker(self):
        """Two numbers 7 from an unordered collection (decision 0045)."""
        pairs = [(a("7"), a("7")), (a("3"), a("3")), (a("7"), a("7"))]
        self.assertEqual(op.sort_by_key(pairs, False, self.tie_key, WIB), [a("3"), a("7"), a("7")])
        r = [(Record({"x": a("1")}), a("1")), (Record({"x": a("1")}), a("1"))]
        self.assertEqual(len(op.sort_by_key(r, False, self.tie_key, WIB)), 2)

    def test_equal_but_not_identical(self):
        """0 and 0 IDR are equal under `=`, but can be told apart."""
        pairs = [(a("0"), a("1")), (a("0 IDR"), a("1"))]
        self.assertNotComputable("undefined order", op.sort_by_key,
                                 pairs, False, self.tie_key, WIB)

    def test_identical(self):
        self.assertTrue(op.identical(a("7"), a("7.0")))
        self.assertFalse(op.identical(a("0"), a("0 IDR")))
        self.assertFalse(op.identical(t("1 Oct 2026"), parse_time("1 Oct 2026 00:00", WIB)))
        self.assertFalse(op.identical(k(a("1"), a("2"), ordered=False),
                                      k(a("2"), a("1"), ordered=False)))
        self.assertFalse(op.identical(k(a("1")), k(a("1"), ordered=False)))


if __name__ == "__main__":
    unittest.main()
