"""Tests for content: the unit code list, the full form, and the first vocabulary.

The list in the content document and the table in the program MUST be equal,
so that a code added in the content does not silently differ from what the
program computes.
"""

import re
import unittest
from pathlib import Path

from calculator import completeness
from calculator.reader import ChoiceList, Concept, read
from calculator.examples import run_all
from calculator.values import NotationError, parse_number, unit_table
from calculator.module_set import ModuleSet

CONTENT = Path(__file__).parents[2] / "content"
CODE_LISTS = (CONTENT / "code-lists.md").read_text(encoding="utf-8")
ALL_CONTENT = [p.read_text(encoding="utf-8") for p in sorted(CONTENT.rglob("*.md"))]
VOCABULARY_17 = (Path(__file__).parents[2] / "conformance" / "17-vocabulary.md").read_text(encoding="utf-8")


def build_set(*text):
    return ModuleSet([m for t in text for m in read(t, markdown=True)])


class CodeLists(unittest.TestCase):
    def test_document_table_equals_program(self):
        rows = re.findall(r"^\| `([A-Za-z0-9]+)` \| (\w+) \| `([a-z0-9A-Z]+)` \|",
                          CODE_LISTS, re.MULTILINE)
        document = {code: (spelling, quantity) for code, quantity, spelling in rows}
        self.assertEqual(document, unit_table())

    def test_module_choices_equal_program(self):
        choice_list = build_set(CODE_LISTS).all_modules()[0].content["Unit"]
        self.assertIsInstance(choice_list, ChoiceList)
        self.assertTrue(choice_list.code)
        self.assertFalse(choice_list.is_open)
        self.assertEqual(sorted(choice_list.choices), sorted(unit_table()))

    def test_code_outside_list_is_not_a_unit(self):
        with self.assertRaisesRegex(NotationError, "unknown unit"):
            parse_number("10 EUR")

    def test_codes_only_in_code_lists(self):  # ADDRESS-2
        with self.assertRaisesRegex(NotationError, "ADDRESS-2"):
            read("module a/b@v1\n\nchoice_list MataUang, closed\n  choices:\n    IDR\n")
        with self.assertRaisesRegex(NotationError, "ADDRESS-2"):
            read("module a/b@v1\n\nchoice_list Code, code\n  choices:\n    in_i\n")

    def test_code_list_cannot_be_extended_by_others(self):  # VALUE-13
        other = "```uniti\nmodule a/b@v1\n  uses uniti/unit@v1\n\nchoice eur to uniti/unit/Unit\n```\n"
        with self.assertRaisesRegex(NotationError, "VALUE-13"):
            build_set(CODE_LISTS, other)


_RATE = """```uniti
module a/rate@v1
  uses uniti/unit@v1

concept Rate

property per : choice Unit
property price : number (money/duration, level)

computed Rate.daily : yes_no, closed:
  this.per = unit_of(1 day) and unit_of(this.price × 1 day) = IDR

example daily_rate
  kind         compute
  title        Daily rate
  explanation  The unit is written day in the reference notation, and its code is d.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    t  type   Rate           valid 1 Oct 2026
    t  per    {per}           valid 1 Oct 2026
    t  price  50,000 IDR/day  valid 1 Oct 2026
  ask          t.daily   T: 1 Oct 2026   R: 1 Oct 2026 10:00
  result       yes
```
"""


class UnitAsValue(unittest.TestCase):
    def run_set(self, per):
        return run_all(build_set(CODE_LISTS, _RATE.replace("{per}", per)))

    def test_written_like_notation_or_its_code(self):
        for per in ("day", "d", "uniti/unit/d"):
            with self.subTest(per=per):
                (report,) = [x for x in self.run_set(per) if x.example == "a/rate/daily_rate"]
                self.assertEqual(report.status, "passed", report.detail)

    def test_nonexistent_code(self):  # VALUE-14
        (report,) = [x for x in self.run_set("EUR") if x.example == "a/rate/daily_rate"]
        self.assertEqual(report.status, "notation error")
        self.assertIn("EUR", report.detail)


def content_modules():
    return [m for t in ALL_CONTENT for m in read(t, markdown=True)
            if m.address.startswith("uniti/")]


class FullForm(unittest.TestCase):
    def test_all_content_modules_complete(self):  # NOTATION-17
        for m in content_modules():
            with self.subTest(module=m.full_name):
                self.assertEqual(completeness.check(m), [])

    def test_short_form_is_incomplete(self):
        (m,) = read("module a/b@v1\n\nconcept Rental\n\ncomputed Rental.n : number (level), closed:\n  1\n")
        self.assertEqual(completeness.check(m), [
            "a/b/Rental: concept without label (CONCEPT-1)",
            "a/b/Rental: concept without definition (CONCEPT-1)",
            "a/b/Rental: concept without includes (CONCEPT-1)",
            "a/b/Rental: concept without excludes (CONCEPT-1)",
            "a/b/n: written in short form (NOTATION-17)",
        ])


class FirstVocabulary(unittest.TestCase):
    def test_includes_from_two_domains(self):  # CONCEPT-2, with the vocabulary notation
        for m in content_modules():
            for content in m.content.values():
                if not isinstance(content, Concept):
                    continue
                for part in ("includes", "excludes"):
                    with self.subTest(concept=content.address, part=part):
                        domain = {text.partition(":")[0] for keyword, text in content.card
                                  if keyword.partition(".")[0] == part}
                        self.assertGreaterEqual(len(domain), 2)

    def test_two_domain_cases_pass(self):
        s = ModuleSet([m for t in ALL_CONTENT + [VOCABULARY_17] for m in read(t, markdown=True)])
        result = {report.example: report.status for report in run_all(s)
                  if report.example.startswith(("kemah-ceria/rental/", "tunas-bangsa/tuition/"))}
        self.assertEqual(len(result), 3)
        self.assertEqual(set(result.values()), {"passed"})

    def test_others_may_not_make_required(self):  # CONCEPT-8
        text = VOCABULARY_17.replace("applies to Payment:\n  rental\n",
                                     "applies to Payment:\n  rental       required\n")
        with self.assertRaisesRegex(NotationError, "CONCEPT-8"):
            ModuleSet([m for t in ALL_CONTENT + [text] for m in read(t, markdown=True)])


if __name__ == "__main__":
    unittest.main()
