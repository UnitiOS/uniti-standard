"""Tests for the reader of the reference notation: appendix A §2.6, §2.7, §4, and §5."""

import unittest

from calculator.reader import (
    Line, NotationError, Let, Call, HelperCall, UnitLiteral, Fixed, read,
    render, parse_expression, parse_text,
)
from calculator.values import parse_number, parse_unit, parse_zone


def parenthesize(text):
    return render(parse_text(text))


def make_lines(*content):
    return [Line(i + 1, 2, x) for i, x in enumerate(content)]


class ReadingOrder(unittest.TestCase):
    """The reading-order table in appendix A §4, NOTATION-12."""

    def test_appendix_table(self):
        self.assertEqual(parenthesize("a + b × c"), "(a + (b × c))")
        self.assertEqual(parenthesize("− sum(k) + 5"), "((− sum(k)) + 5)")
        self.assertEqual(parenthesize("not exists(x) or x = 0"), "((not exists(x)) or (x = 0))")
        self.assertEqual(parenthesize("x with sum = x.sum × n"),
                         "(x with sum = (x.sum × n))")
        self.assertEqual(parenthesize("s.item = this and T in s.period"),
                         "((s.item = this) and (T in s.period))")

    def test_not_binds_looser_than_comparison(self):
        self.assertEqual(parenthesize("not a = b"), "(not (a = b))")

    def test_with_twice(self):
        self.assertEqual(parenthesize("r with a = 1 with b = 2"),
                         "((r with a = 1) with b = 2)")

    def test_if_extends_as_far_as_possible(self):
        self.assertEqual(parenthesize("if a then 1 else 2 + 3"),
                         "(if a then 1 else (2 + 3))")
        self.assertEqual(parenthesize("max(0, (if exists(b) then b else a) − c)"),
                         "max(0, ((if exists(b) then b else a) − c))")

    def test_keyword_after_dot_and_in_record(self):
        self.assertEqual(parenthesize("{claim: k, sum: b}.sum"), "{claim: k, sum: b}.sum")


class FixedValues(unittest.TestCase):
    """Appendix A §2.3, NOTATION-5 to NOTATION-7."""

    def test_number_with_unit_and_comma(self):
        n = parse_text("min(1, 5)")
        self.assertEqual(len(n.positional), 2)
        n = parse_text("min(1,500)")
        self.assertEqual(len(n.positional), 1)
        self.assertEqual(n.positional[0].value, parse_number("1,500"))
        n = parse_text("min(1.5)")
        self.assertEqual(n.positional[0].value, parse_number("1.5"))
        self.assertEqual(parse_text("50,000 IDR/day").value, parse_number("50,000 IDR/day"))

    def test_name_after_number_is_not_unit_if_keyword(self):
        self.assertEqual(parenthesize("if a then 5 else 0"), "(if a then 5 else 0)")

    def test_instant_in_rule_requires_zone(self):
        parse_text("6 Oct 2026 09:00 WIB")
        with self.assertRaises(NotationError):
            parse_text("6 Oct 2026 09:00")
        self.assertEqual(parse_text("6 Oct 2026 09:00", parse_zone("WIB")).value.utcoffset().seconds,
                         7 * 3600)

    def test_text_with_quotes(self):
        self.assertEqual(parse_text('"Tent ""dome"""@en').value.content, 'Tent "dome"')


class Calls(unittest.TestCase):
    """Appendix A §2.7, NOTATION-15."""

    def test_unit_position(self):
        n = parse_text("span(month, day)")
        self.assertEqual(render(n.positional[0]), "month")
        self.assertEqual(n.positional[1], UnitLiteral(parse_unit("day")))
        self.assertEqual(parse_text("convert(n, to: IDR)").arg("to"), UnitLiteral(parse_unit("IDR")))

    def test_named_argument(self):
        n = parse_text("floor_multiple(n, of: 0.5 kg)")
        self.assertEqual(n.arg("of"), Fixed(parse_number("0.5 kg")))

    def test_binder_and_named_argument(self):
        n = parse_text("sum(k, x: x.length)")
        self.assertEqual([type(a).__name__ for a in n.positional], ["Name", "Binder"])
        n = parse_text("fold(k, initial: 0, step: (s, x): s + x)")
        self.assertEqual(n.arg("step").names, ("s", "x"))

    def test_wrong_forms(self):
        for text in ("floor_multiple(n)",                     # `of` is required
                     "power(2, 0.5, of: 0.01)",               # there is no `of`
                     "convert(n, to: IDR, rate: k)",          # there is no `rate`
                     "single(a, b)",
                     "all_match(k)",
                     "history(r, in: m)",                     # not x.s
                     "sum(to: 1, k)"):
            with self.assertRaises(NotationError, msg=text):
                parse_text(text)

    def test_library_helper(self):
        """Appendix A §2.7: a library helper is called like any other helper,
        without named arguments and without a binder (decision 0045)."""
        n = parse_text("round(n, 1 IDR, nearest)")
        self.assertIsInstance(n, HelperCall)
        self.assertEqual(render(n.arguments[2]), "nearest")
        for text in ("median(k, x: x.length)", "round(n, to: 1 IDR, mode: nearest)"):
            with self.assertRaises(NotationError, msg=text):
                parse_text(text)


class LetExpressions(unittest.TestCase):
    """Appendix A §2.6, NOTATION-14."""

    def test_lines(self):
        n = parse_expression(make_lines("let taxable = this.taxable_income",
                                        "let limit = 60,000,000 IDR",
                                        "min(taxable, limit) × 5%"))
        self.assertIsInstance(n, Let)
        self.assertEqual(render(n.body.body), "(min(taxable, limit) × 0.05)")

    def test_open_paren_continues_line(self):
        n = parse_expression(make_lines("let a = min(1,", "  2)", "a"))
        self.assertEqual(render(n), "(let a = min(1, 2); a)")

    def test_let_inside_binder(self):
        n = parse_expression(make_lines("fold(k, initial: 0,", "  step: (s, x):",
                                        "    let b = s + x", "    b × 2", ")"))
        self.assertIsInstance(n.arg("step").body, Let)

    def test_newline_outside_let_equals_space(self):
        self.assertEqual(render(parse_expression(make_lines("a +", "b"))), "(a + b)")


class NonExamples(unittest.TestCase):
    """Appendix A §5."""

    def test_all_rejected(self):
        for content in (["1,5"], ["price - discount"], ["price * 2"], ["if a then b"],
                        ["0 < x < 10"], ["let x = 1, x + 1"],
                        ["median(k, x: x.length)"],
                        ["let sum = 1", "sum"], ["at(6 Oct, x)"],
                        ["x + let y = 1", "y"]):
            with self.assertRaises(NotationError, msg=content):
                parse_expression(make_lines(*content))


class CardParts(unittest.TestCase):
    """Appendix A §2.8 and §2.10."""

    def test_markdown_only_uniti_blocks(self):
        text = "# Title\n\n```\nconcept No\n```\n\n```uniti\nmodule a/b@v1\n\nconcept Yes\n```\n"
        (m,) = read(text, markdown=True)
        self.assertEqual(list(m.content), ["Yes"])

    def test_writing_starts_with_module(self):
        with self.assertRaises(NotationError):
            read("concept Rental\n")

    def test_short_and_full_form_are_equal(self):
        short_form, = read("module a/b@v1\n\nhelper Rental.period : range:\n  range(this.start_date, this.end_date)\n")
        completeness, = read("module a/b@v1\n\nhelper Rental.period : range\n  label.en  Period\n"
                             "  rule:\n    range(this.start_date, this.end_date)\n")
        self.assertEqual(short_form.content["period"].expression, completeness.content["period"].expression)

    def test_computed_must_be_open_or_closed(self):
        with self.assertRaises(NotationError):
            read("module a/b@v1\n\ncomputed Rental.total : number (money, increase):\n  1\n")


if __name__ == "__main__":
    unittest.main()
