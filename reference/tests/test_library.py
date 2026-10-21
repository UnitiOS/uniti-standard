"""Tests for the first calculation library (06 §2.5, decision 0045).

The ways of computing that used to be operations are now helpers in
`content/calc.md`. The tests here are the old operation tests, with the same
numbers, run through those helpers. Only the reason kind changed, for
failures that the library checks itself: *declared by rule*.
"""

import datetime as dt
import unittest
from pathlib import Path

from calculator import operations as op
from calculator.examples import read_files
from calculator.compute import TYPE_PROPERTY, Action, Fact, FactStore, Evaluator
from calculator.values import (
    EMPTY, UTC, Entity, NotationError, Collection, Choice, Record, NotComputable,
    parse_number, parse_unit, parse_time, parse_zone,
)

LIBRARY = Path(__file__).parents[2] / "content" / "calc.md"
WIB = parse_zone("WIB")
T = dt.date(2026, 10, 1)


def a(text):
    return parse_number(text)


def k(*members, ordered=True):
    return Collection(tuple(members), ordered)


def numbers(*text, ordered=False):
    return k(*(a(x) for x in text), ordered=ordered)


def choice_of(name):
    return Choice(f"uniti/calc/{name}")


def weighted_list(weight, members=None, ordered=True):
    """A collection of records {member, weight} for `allocate`."""
    members = members or [Entity(f"h{i}") for i in range(len(weight))]
    return k(*(Record({"member": h, "weight": a(w)}) for h, w in zip(members, weight)),
             ordered=ordered)


class LibraryBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        module_set = read_files(LIBRARY)
        cls.module = next(m for m in module_set.all_modules() if m.address == "uniti/calc")
        R = dt.datetime(2026, 10, 1, tzinfo=UTC)
        action = Action(R, Entity("actor"))
        # Tie-breaker: r2 is valid earlier than r1, r1 earlier than r3.
        cls.rooms = [Entity("r1"), Entity("r2"), Entity("r3")]
        valid = [dt.date(2026, 9, 2), dt.date(2026, 9, 1), dt.date(2026, 9, 3)]
        facts = [Fact(h, TYPE_PROPERTY, "x", b, R, action, order=i)
                 for i, (h, b) in enumerate(zip(cls.rooms, valid))]
        cls.evaluator = Evaluator(module_set, [cls.module], FactStore(facts), R)

    def helper(self, name, *args):
        return self.evaluator.compute(self.module.content[name], None, list(args), T)

    def shares(self, *args):
        return [r.get("share") for r in self.helper("allocate", *args).members]

    def assertDeclaredByRule(self, name, *args):
        """A failure that the library checks itself (decision 0045 item 7)."""
        with self.assertRaises(NotComputable) as cm:
            self.helper(name, *args)
        self.assertEqual(cm.exception.kind, "declared by rule")


class Rounding(LibraryBase):
    """Paper tests E3, G3, X1; formerly CALC-22."""

    def round_to(self, n, to, mode):
        return self.helper("round", n, to, choice_of(mode))

    def test_nearest_half_away_from_zero(self):
        self.assertEqual(self.round_to(a("0.125"), a("0.01"), "nearest"), a("0.13"))
        self.assertEqual(self.round_to(a("−0.125"), a("0.01"), "nearest"), a("−0.13"))
        self.assertEqual(self.round_to(a("0.124"), a("0.01"), "nearest"), a("0.12"))

    def test_attendance_e3(self):
        percent = op.multiply(op.divide(a("90"), a("96")), a("100"))
        self.assertEqual(self.round_to(percent, a("0.1"), "nearest"), a("93.8"))

    def test_prorated_salary_g3(self):
        month_length = a("31")
        part = op.add(
            op.divide(op.multiply(a("9,000,000 IDR"), a("15")), month_length),
            op.divide(op.multiply(a("9,300,000 IDR"), a("16")), month_length), WIB)
        self.assertEqual(self.round_to(part, a("1 IDR"), "nearest"), a("9,154,839 IDR"))

    def test_up_x1(self):
        self.assertEqual(self.round_to(a("4.8 kg"), a("0.5 kg"), "up"), a("5 kg"))
        self.assertEqual(self.round_to(a("4.8 kg"), a("0.5 kg"), "down"), a("4.5 kg"))

    def test_negative(self):
        """up goes to the larger, down goes to the smaller."""
        self.assertEqual(self.round_to(a("−4.8 kg"), a("0.5 kg"), "up"), a("−4.5 kg"))
        self.assertEqual(self.round_to(a("−4.8 kg"), a("0.5 kg"), "down"), a("−5 kg"))

    def test_multiple_unit_must_match(self):
        with self.assertRaises(NotComputable) as cm:
            self.round_to(a("4.8 kg"), a("1 IDR"), "nearest")
        self.assertEqual(cm.exception.kind, "unit mismatch")


class Allocate(LibraryBase):
    """Paper tests K4, K5, K6; formerly CALC-23."""

    def test_area_k5(self):
        self.assertEqual(
            self.shares(a("10,000,000 IDR"), weighted_list(["120 m²", "80 m²", "100 m²"]),
                        a("1 IDR"), choice_of("largest_fraction")),
            [a("4,000,000 IDR"), a("2,666,667 IDR"), a("3,333,333 IDR")])

    def test_tie_broken_by_order(self):
        """A boundary not yet tested in K5: two equal fractions."""
        self.assertEqual(self.shares(a("100 IDR"), weighted_list(["1", "1", "1"]), a("1 IDR"),
                                     choice_of("largest_fraction")),
                         [a("34 IDR"), a("33 IDR"), a("33 IDR")])

    def test_depreciation_k4(self):
        part = self.shares(a("12,000,000 IDR"), weighted_list(["1"] * 36), a("1 IDR"),
                           choice_of("last"))
        self.assertEqual(part[:35], [a("333,333 IDR")] * 35)
        self.assertEqual(part[35], a("333,345 IDR"))
        self.assertEqual(op.sum_values(part[:3]), a("999,999 IDR"))

    def test_revenue_k6(self):
        part = self.shares(a("10,000,000 IDR"), weighted_list(["1"] * 12), a("1 IDR"),
                           choice_of("last"))
        self.assertEqual(part[0], a("833,333 IDR"))
        self.assertEqual(part[-1], a("833,337 IDR"))
        self.assertEqual(op.sum_values(part[:5]), a("4,166,665 IDR"))

    def test_first_and_negative_total(self):
        self.assertEqual(self.shares(a("−10 IDR"), weighted_list(["1", "1", "1"]), a("1 IDR"),
                                     choice_of("first")),
                         [a("−4 IDR"), a("−3 IDR"), a("−3 IDR")])

    def test_sum_is_always_exact(self):
        for remaining in ("largest_fraction", "first", "last"):
            part = self.shares(a("1,000,000 IDR"), weighted_list(["3", "7", "11", "13"]),
                               a("1 IDR"), choice_of(remaining))
            self.assertEqual(op.sum_values(part), a("1,000,000 IDR"), remaining)

    def test_invalid_weights(self):
        """Formerly the reason kind "invalid weight", which was removed in 0045."""
        for weight in (["1", "−1"], ["0", "0"], []):
            self.assertDeclaredByRule("allocate", a("10 IDR"), weighted_list(weight), a("1 IDR"),
                                      choice_of("largest_fraction"))

    def test_total_not_a_multiple(self):
        self.assertDeclaredByRule("allocate", a("10.5 IDR"), weighted_list(["1", "1"]), a("1 IDR"),
                                  choice_of("largest_fraction"))

    def test_order_written_by_user(self):
        """An unordered collection is first ordered with `by_member`, by the
        tie-breaker of its members: r2, r1, r3."""
        r1, r2, r3 = self.rooms
        shuffled = weighted_list(["1", "1", "1"], [r1, r2, r3], ordered=False)
        with self.assertRaises(NotationError):  # CALC-18
            self.helper("allocate", a("100 IDR"), shuffled, a("1 IDR"), choice_of("largest_fraction"))
        order_by = self.helper("by_member", shuffled)
        result = self.helper("allocate", a("100 IDR"), order_by, a("1 IDR"),
                             choice_of("largest_fraction"))
        self.assertEqual([(r.get("member"), r.get("share")) for r in result.members],
                         [(r2, a("34 IDR")), (r1, a("33 IDR")), (r3, a("33 IDR"))])


class Summaries(LibraryBase):
    """Paper test C2."""

    WAIT = ["10 minutes", "25 minutes", "15 minutes", "40 minutes", "20 minutes"]

    def test_average_and_median_c2(self):
        wait = numbers(*self.WAIT)
        self.assertEqual(self.helper("average", wait), a("22 minutes"))
        self.assertEqual(self.helper("median", wait), a("20 minutes"))

    def test_median_even(self):
        """A boundary not yet tested in C2: an even number of data points."""
        self.assertEqual(self.helper("median", numbers(*self.WAIT, "30 minutes")),
                         a("22.5 minutes"))

    def test_duplicate_values(self):
        """Two numbers 7 from an unordered collection (decision 0045)."""
        self.assertEqual(self.helper("median", numbers("7", "3", "7", "5")), a("6"))

    def test_percentile_nearest_rank(self):
        value = numbers("5", "1", "4", "2", "3", "10", "9", "8", "7", "6")
        self.assertEqual(self.helper("percentile", value, a("0.9")), a("9"))
        self.assertEqual(self.helper("percentile", value, a("0.91")), a("10"))
        self.assertEqual(self.helper("percentile", value, a("1")), a("10"))
        for p in ("0", "1.1", "−0.5"):
            self.assertDeclaredByRule("percentile", value, a(p))

    def test_empty_collection(self):
        for name in ("average", "median"):
            self.assertDeclaredByRule(name, k(ordered=False))
        self.assertDeclaredByRule("percentile", k(ordered=False), a("0.5"))

    def test_median_numbers_only(self):
        date = [parse_time("1 Oct 2026", WIB), parse_time("3 Oct 2026", WIB)]
        for n in (1, 2):
            with self.assertRaises(NotationError):
                self.helper("median", k(*date[:n], ordered=False))


class ConvertMoney(LibraryBase):
    """Paper test K2. The rate is read only if the currencies differ."""

    IDR = op.unit_as_choice(parse_unit("IDR"))

    def test_same_currency_without_rate(self):
        self.assertEqual(self.helper("convert_money", a("1,000,000 IDR"), self.IDR, EMPTY),
                         a("1,000,000 IDR"))

    def test_rate(self):
        self.assertEqual(self.helper("convert_money", a("100 USD"), self.IDR, a("16,200 IDR/USD")),
                         a("1,620,000 IDR"))
        with self.assertRaises(NotComputable) as cm:
            self.helper("convert_money", a("100 USD"), self.IDR, EMPTY)
        self.assertEqual(cm.exception.kind, "empty value")

    def test_rate_without_unit(self):
        """100 USD × 16,200 is 1,620,000 USD, not rupiah."""
        self.assertDeclaredByRule("convert_money", a("100 USD"), self.IDR, a("16,200"))


if __name__ == "__main__":
    unittest.main()
