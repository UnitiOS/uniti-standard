"""Tests for values: number notation, units, time, and reason kinds."""

import datetime as dt
import unittest
from fractions import Fraction

from calculator.values import (
    Number, NotationError, Unit, NotComputable, parse_number, terminates,
    parse_numeral, parse_unit, format_numeral, parse_time, parse_zone,
)


class Numerals(unittest.TestCase):
    """Appendix A §2.3, NOTATION-5."""

    def test_thousands_separator_and_decimal_point(self):
        self.assertEqual(parse_numeral("1,234.5"), Fraction(2469, 2))
        self.assertEqual(parse_numeral("150000"), 150000)
        self.assertEqual(parse_numeral("0.8"), Fraction(4, 5))

    def test_percent_divided_by_hundred(self):
        self.assertEqual(parse_numeral("5%"), Fraction(1, 20))
        self.assertEqual(parse_numeral("93.75%"), Fraction(15, 16))

    def test_negative_with_minus_sign(self):
        self.assertEqual(parse_numeral("−5,000"), -5000)

    def test_non_examples(self):
        for text in ("1,5", "1,50,000", "-5", "1."):
            with self.assertRaises(NotationError, msg=text):
                parse_numeral(text)

    def test_write_back(self):
        self.assertEqual(format_numeral(Fraction(-24691, 20)), "−1,234.55")
        self.assertEqual(format_numeral(Fraction(1, 3)), "1/3")


class UnitsAndNumbers(unittest.TestCase):
    """Appendix A §2.4; 06 §2.8."""

    def test_compound_unit(self):
        self.assertEqual(parse_unit("IDR/day"), Unit((("IDR", 1), ("day", -1))))
        self.assertEqual(parse_unit("cm³/kg"), Unit((("cm", 3), ("kg", -1))))
        self.assertEqual(str(parse_unit("IDR/day")), "IDR/day")

    def test_read_from_left(self):
        self.assertEqual(parse_unit("kg/m·hour"), Unit.from_map({"kg": 1, "m": -1, "hour": 1}))

    def test_unknown_unit(self):
        with self.assertRaises(NotationError):
            parse_unit("ounce")

    def test_number_with_unit(self):
        self.assertEqual(parse_number("50,000 IDR/day"),
                         Number(50000, parse_unit("IDR/day")))
        self.assertEqual(str(parse_number("2.5 kg")), "2.5 kg")


class Terminating(unittest.TestCase):
    """CALC-21."""

    def test_terminating(self):
        self.assertTrue(terminates(Fraction(1, 8)))
        self.assertTrue(terminates(Fraction(12000000, 36) * 36))
        self.assertFalse(terminates(Fraction(135000000, 31)))
        self.assertFalse(terminates(Fraction(1, 3)))


class Time(unittest.TestCase):
    """Appendix A §2.3 and §2.4, NOTATION-6 and NOTATION-7."""

    def test_date(self):
        self.assertEqual(parse_time("6 Oct 2026"), dt.date(2026, 10, 6))
        self.assertEqual(parse_time("6 October 2026"), dt.date(2026, 10, 6))

    def test_date_without_year_rejected(self):
        with self.assertRaises(NotationError):
            parse_time("6 Oct")

    def test_instant_with_zone(self):
        t = parse_time("6 Oct 2026 09:00 WIB")
        self.assertEqual(t.astimezone(dt.timezone.utc).hour, 2)
        self.assertEqual(parse_time("6 Oct 2026 09:00 UTC+5:30").utcoffset(),
                         dt.timedelta(hours=5, minutes=30))

    def test_instant_without_zone_uses_example_default_zone(self):
        self.assertEqual(parse_time("6 Oct 2026 12:00", parse_zone("WITA")).utcoffset(),
                         dt.timedelta(hours=8))
        with self.assertRaises(NotationError):
            parse_time("6 Oct 2026 12:00")


class ReasonKinds(unittest.TestCase):
    """CALC-28: reason kinds from a closed list."""

    def test_closed_list(self):
        NotComputable("not single", "two rates")
        with self.assertRaises(ValueError):
            NotComputable("missing data", "not a valid kind")


if __name__ == "__main__":
    unittest.main()
