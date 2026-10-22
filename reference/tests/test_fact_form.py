"""Rejection of facts with a wrong form inside an action (FACT-2, FACT-9,
FACT-10, FACT-11, FACT-13, FACT-14). The examples are in
conformance/22-fact-form.md; here is each row of the table and the edges.
"""

import unittest

from tests.test_compute import status

SHOP = """
module ref/shop@v1

concept Customer
concept Product

property phone : text
property tags : text, many
property price : number (money, position)

applies to Customer:
  phone
  tags

applies to Product:
  price

constraint Product.cheap
  label.en     Cheap
  definition.en  A price stays under one million.
  message.en   Too expensive.
  rule:
    this.price < 1,000,000 IDR

example t
  kind         KIND
  title        Fact form
  explanation  A test.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    c1       type   Customer       valid 1 Oct 2026
    c2       type   Customer       valid 1 Oct 2026
    p1       type   Product        valid 1 Oct 2026
    f1: c1   phone  "0812-111"     valid 1 Oct 2026
    f2: c2   phone  "0812-222"     valid 1 Oct 2026
    f3: p1   price  100,000 IDR    valid 1 Oct 2026
    f4: p1   price  120,000 IDR    valid 1 Nov 2026  replaces f3
    f5: c1   phone  valid 1 Dec 2026  ends f1
    f6: c2   phone  valid 1 Oct 2026  retracts f2
EXTRA
  action       recorded 20 Oct 2026 10:00
ACTION
  result       RESULT
"""


def run(action, result, kind="reject", extra=""):
    text = (SHOP.replace("KIND", kind).replace("EXTRA", extra)
            .replace("ACTION", action).replace("RESULT", result))
    return status(text)["t"]


def rejects(case, action, by, entity="c1"):
    case.assertEqual(run(action, f"rejected by {by}, entity {entity}")[0], "passed")


def accepts(case, action):
    case.assertEqual(run(action, "accepted", "accept")[0], "passed")


class Form(unittest.TestCase):
    def test_fact_2_ending_with_a_value(self):
        rejects(self, '    c1   phone  "0812-9"  valid 1 Nov 2026  ends f1', "FACT-2")

    def test_fact_2_retraction_with_a_value(self):
        rejects(self, '    c1   phone  "0812-9"  valid 1 Oct 2026  retracts f1', "FACT-2")

    def test_fact_2_redaction_with_a_value(self):
        rejects(self, '    c1   phone  "0812-9"  valid 1 Oct 2026  redacts f1', "FACT-2")

    def test_fact_2_statement_without_a_value(self):
        rejects(self, '    c3   type   Customer  valid 1 Oct 2026\n'
                      '    c3   phone  valid 1 Oct 2026', "FACT-2", "c3")

    def test_fact_2_replacement_without_a_value(self):
        rejects(self, '    c1   phone  valid 1 Nov 2026  replaces f1', "FACT-2")

    def test_fact_2_correction_without_a_value(self):
        rejects(self, '    c1   phone  valid 1 Oct 2026  corrects f1', "FACT-2")

    def test_fact_9_other_entity(self):
        rejects(self, '    c1   phone  "0812-9"  valid 1 Nov 2026  replaces f2', "FACT-9")

    def test_fact_9_other_property(self):
        rejects(self, '    c1   tags  "x"  valid 1 Nov 2026  replaces f1', "FACT-9")

    def test_fact_9_target_in_the_same_action(self):
        rejects(self, '    c3   type   Customer  valid 1 Oct 2026\n'
                      '    g1: c3   phone  "0812-8"  valid 1 Oct 2026\n'
                      '    c3   phone  "0812-9"  valid 1 Nov 2026  replaces g1', "FACT-9", "c3")

    def test_fact_10_replacement_not_later(self):
        rejects(self, '    p1   price  90,000 IDR  valid 1 Nov 2026  replaces f4', "FACT-10", "p1")

    def test_fact_10_ending_not_later(self):
        rejects(self, '    p1   price  valid 1 Oct 2026  ends f3', "FACT-10", "p1")

    def test_fact_10_a_later_replacement_is_fine(self):
        accepts(self, '    p1   price  90,000 IDR  valid 1 Dec 2026  replaces f4')

    def test_fact_11_correction_of_an_ending(self):
        rejects(self, '    c1   phone  "0812-9"  valid 1 Dec 2026  corrects f5', "FACT-11")

    def test_fact_11_correction_of_a_retraction(self):
        rejects(self, '    c2   phone  "0812-9"  valid 1 Oct 2026  corrects f6', "FACT-11", "c2")

    def test_fact_13_retraction_of_a_retraction(self):
        rejects(self, '    c2   phone  valid 1 Oct 2026  retracts f6', "FACT-13", "c2")

    def test_fact_14_a_statement_while_a_value_is_in_force(self):
        rejects(self, '    c1   phone  "0812-9"  valid 15 Oct 2026', "FACT-14")

    def test_fact_14_a_statement_after_an_ending_is_fine(self):
        accepts(self, '    c1   phone  "0812-9"  valid 2 Dec 2026')

    def test_fact_14_a_statement_of_a_property_with_many_values_is_fine(self):
        accepts(self, '    c1   tags  "a"  valid 1 Oct 2026\n    c1   tags  "b"  valid 1 Oct 2026')

    def test_fact_14_replacement_of_a_value_not_in_force(self):
        rejects(self, '    p1   price  90,000 IDR  valid 1 Dec 2026  replaces f3', "FACT-14", "p1")

    def test_fact_14_replacement_when_nothing_is_in_force(self):
        rejects(self, '    c2   phone  "0812-9"  valid 1 Nov 2026  replaces f2', "FACT-14", "c2")

    def test_fact_14_two_values_for_one_date(self):
        rejects(self, '    p1   price  90,000 IDR  valid 1 Dec 2026  replaces f4\n'
                      '    p1   price  95,000 IDR  valid 1 Dec 2026  replaces f4', "FACT-14", "p1")

    def test_fact_14_one_date_written_as_date_and_as_instant(self):
        rejects(self, '    c3   type   Customer  valid 1 Oct 2026\n'
                      '    c3   phone  "1"  valid 1 Nov 2026\n'
                      '    c3   phone  "2"  valid 1 Nov 2026 00:00', "FACT-14", "c3")


class Hidden(unittest.TestCase):
    ACTION = ('    p1   phone  "0812-9"  valid 1 Nov 2026\n'
              '    p1   price  1,500,000 IDR  valid 1 Dec 2026  replaces f4\n'
              '    p1   price  valid 1 Nov 2026  ends f4')

    def test_a_fact_rejection_hides_the_other_checks(self):
        # The first fact breaks CONCEPT-6 and the second breaks `cheap`, but
        # the third breaks FACT-10; only the rule of the fact is reported.
        # The expected result names FACT-10 and every rejection must be by it.
        self.assertEqual(run(self.ACTION, "rejected by FACT-10, entity p1")[0], "passed")

    def test_without_the_fact_rejection_the_other_checks_are_reported(self):
        action = ('    p1   phone  "0812-9"  valid 1 Nov 2026')
        self.assertEqual(run(action, "rejected by CONCEPT-6, entity p1")[0], "passed")
        action = ('    p1   price  1,500,000 IDR  valid 1 Dec 2026  replaces f4')
        self.assertEqual(run(action, "rejected by cheap, entity p1")[0], "passed")


class StartingFacts(unittest.TestCase):
    NEW = '    c3   type   Customer  valid 1 Oct 2026'

    def test_fact_2_in_starting_facts_is_a_notation_error(self):
        for fact in ('    g1: c1   phone  valid 1 Nov 2026',
                     '    g1: c1   phone  "1"  valid 1 Nov 2026  ends f1'):
            self.assertEqual(run(self.NEW, "accepted", "accept", fact)[0], "notation error", fact)

    def test_fact_9_in_starting_facts_is_a_notation_error(self):
        fact = '    g1: c1   phone  "1"  valid 1 Nov 2026  replaces f2'
        self.assertEqual(run(self.NEW, "accepted", "accept", fact)[0], "notation error")

    def test_fact_10_in_starting_facts_is_a_notation_error(self):
        fact = '    g1: p1   price  90,000 IDR  valid 1 Oct 2026  replaces f3'
        self.assertEqual(run(self.NEW, "accepted", "accept", fact)[0], "notation error")

    def test_other_notation_errors_in_an_action_stay_notation_errors(self):
        for fact in ('    c1   phone  "0812-9  valid 1 Nov 2026',
                     '    c1   colour  "red"  valid 1 Nov 2026',
                     '    p1   price  tomorrow  valid 1 Nov 2026  replaces f4'):
            self.assertNotEqual(run(fact, "accepted", "accept")[0], "passed", fact)
        self.assertEqual(run('    c1   phone  "0812-9  valid 1 Nov 2026',
                             "accepted", "accept")[0], "notation error")


if __name__ == "__main__":
    unittest.main()
