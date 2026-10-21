"""Tests for the evaluator and the action checker, with small examples in the
reference notation.

Each test writes a module and an example, then checks the status of that
example: passed, failed, not defined, or notation error.
"""

import unittest

from calculator.reader import read
from calculator.examples import run_all
from calculator.module_set import ModuleSet


def status(text):
    """The status of each example, by example name."""
    return {report.example.rpartition("/")[2]: (report.status, report.detail)
            for report in run_all(ModuleSet(read(text)))}


INVENTORY = """
module uniti/inventory@v1

concept Item
property initial_stock : number (level)

computed Item.available : number (level), open:
  this.initial_stock + sum(contributions)

example without_rental_module
  kind         compute
  title        Without the rental module
  explanation  The rental module is not installed, so nothing contributes.
  facts        recorded 1 Oct 2026
    tent  type       Item  valid 1 Oct 2026
    tent  initial_stock  5       valid 1 Oct 2026
  ask          tent.available   T: 7 Oct 2026   R: 7 Oct 2026
  result       5

module rudi/rental@v1
  uses uniti/inventory@v1

concept Rental
property item : reference Item
property start_date : date
property end_date : date

contribution being_rented to Item.available:
  − count(all(Rental, s: s.item = this
                             and T in range(s.start_date, s.end_date)))

example one_rented
  kind         compute
  title        One tent is being rented
  explanation  Stock 5, one is being rented, 4 available.
  facts        recorded 1 Oct 2026
    tent  type       Item      valid 1 Oct 2026
    tent  initial_stock  5           valid 1 Oct 2026
    r1     type       Rental        valid 1 Oct 2026
    r1     item     tent       valid 1 Oct 2026
    r1     start_date      6 Oct 2026  valid 1 Oct 2026
    r1     end_date    9 Oct 2026  valid 1 Oct 2026
  ask          tent.available   T: 7 Oct 2026   R: 7 Oct 2026
  result       4

example already_returned
  kind         compute
  title        The tent is back
  explanation  On 9 October the rental has ended.
  facts        as in one_rented
  ask          tent.available   T: 9 Oct 2026   R: 9 Oct 2026
  result       5
"""


class Contributions(unittest.TestCase):
    """06 §2.11, CALC-35 and CALC-49."""

    def test_only_from_installed_modules(self):
        result = status(INVENTORY)
        self.assertEqual(result["one_rented"][0], "passed")
        self.assertEqual(result["already_returned"][0], "passed")

    def test_without_contributor(self):
        self.assertEqual(status(INVENTORY)["without_rental_module"][0], "passed")

    def test_facts_from_unused_module(self):
        """An example in the vocabulary cannot use the facts of an example owned by
        the rental module, because the vocabulary does not use that module
        (CALC-17)."""
        start = INVENTORY.index("  facts        recorded 1 Oct 2026")
        ending = INVENTORY.index("  ask          tent.available")
        text = (INVENTORY[:start] + "  facts        as in rudi/rental/one_rented\n"
                + INVENTORY[ending:])
        self.assertEqual(status(text)["without_rental_module"][0], "notation error")

    def test_contribution_in_closed_computed(self):
        text = INVENTORY.replace("number (level), open:", "number (level), closed:")
        self.assertEqual(status(text)["one_rented"][0], "notation error")

    def test_contribution_reason_independent_of_install_order(self):
        """06 §2.9 (decision 0054): contributions have no computation order, so
        the reason kind reported is the topmost one in the table."""
        for order in ("divide empty", "empty divide"):
            uses = "\n".join(f"  uses ref/{m}@v1" for m in order.split())
            self.assertEqual(status(TWO_CONTRIBUTIONS.format(uses=uses))["c"][0], "passed", order)


TWO_CONTRIBUTIONS = """
module ref/total@v1

concept Item
property price : number (level)

computed Item.total : number (level), open:
  sum(contributions)

module ref/divide@v1
  uses ref/total@v1

contribution divided_by_zero to Item.total:
  this.price ÷ 0

module ref/empty@v1
  uses ref/total@v1

property remaining : number (level)

contribution from_empty to Item.total:
  this.remaining + 1

module ref/shop@v1
  uses ref/total@v1
{uses}

example c
  kind         compute
  title        Two contributions fail
  explanation  One fails because of division by zero, one because of an empty value.
  facts        recorded 1 Oct 2026
    b  type   Item  valid 1 Oct 2026
    b  price  5       valid 1 Oct 2026
  ask          b.total   T: 1 Oct 2026   R: 1 Oct 2026
  result       not computable: empty value
"""


def one_example(module, facts, query, result, zone="WIB"):
    return f"""
module example/test@v1

{module}

example c
  kind         compute
  title        Test
  explanation  Test.
  zone         {zone}
  facts        recorded 1 Oct 2026
{facts}
  ask          {query}
  result       {result}
"""


COST = """
concept Part
property component : reference Part, many
property own_cost : number (money, level)

computed Part.cost : number (money, level), closed:
  this.own_cost + sum(this.component, k: k.cost)
"""

BICYCLE = """\
    bicycle  type           Part       valid 1 Oct 2026
    bicycle  own_cost  100,000 IDR  valid 1 Oct 2026
    bicycle  component       wheel         valid 1 Oct 2026
    wheel    type           Part       valid 1 Oct 2026
    wheel    own_cost  50,000 IDR   valid 1 Oct 2026"""


class Recursion(unittest.TestCase):
    """06 §2.5 level 3, CALC-13."""

    def test_recursion_for_other_entity(self):
        result = status(one_example(COST, BICYCLE, "bicycle.cost  T: 1 Oct 2026  R: 1 Oct 2026",
                                    "150,000 IDR"))
        self.assertEqual(result["c"][0], "passed", result)

    def test_cycle(self):
        facts = BICYCLE + "\n    wheel    component       bicycle       valid 1 Oct 2026"
        result = status(one_example(COST, facts, "bicycle.cost  T: 1 Oct 2026  R: 1 Oct 2026",
                                    "not computable: cycle"))
        self.assertEqual(result["c"][0], "passed", result)


PRICE = """
concept Item
property price : number (money, level)
property movement : number (money, no_direction)

computed Item.third : number (money, level), closed:
  this.price ÷ 3

computed Item.rounded_third : number (money, level), closed:
  floor_multiple(this.price ÷ 3, of: 1 IDR)

computed Item.price_difference : number (money, no_direction), closed:
  this.movement − this.price

computed Item.with_reserve : number (money, level), closed:
  let reserve = this.price ÷ 0
  this.price

computed Item.reserve_used : number (money, level), closed:
  let reserve = this.price ÷ 0
  reserve

computed Item.total_expensive : number (money, level), closed:
  sum(all(Item, x: x.price > 1,000 IDR), x: x.price)

helper first(a, b) : number:
  a

computed Item.argument_unused : number (money, level), closed:
  first(this.price, this.price ÷ 0)

computed Item.argument_used : number (money, level), closed:
  first(this.price ÷ 0, this.price)

helper itself(n) : number:
  itself(n)

computed Item.helper_uses_itself : number (money, level), closed:
  itself(this.price)

computed Item.helper_in_helper_argument : number (money, level), closed:
  first(first(this.price, 0 IDR), 0 IDR)

computed Item.rate_times_days : number (money, level), closed:
  this.price ÷ 1 day × 3 days

computed Item.rate_times_hours : number (money, level), closed:
  this.price ÷ 1 day × 72 hours
"""


def price(query, result, extra_facts=""):
    facts = ("    b  type    Item      valid 1 Oct 2026\n"
             "    f1: b  price   100 IDR     valid 1 Oct 2026\n"
             "    b  movement  40 IDR      valid 1 Oct 2026" + extra_facts)
    return status(one_example(PRICE, facts, query, result))["c"]


class ComputedPropertyResult(unittest.TestCase):
    """CALC-21, 06 §2.10."""

    def test_needs_rounding(self):
        self.assertEqual(price("b.third  T: 1 Oct 2026  R: 1 Oct 2026",
                               "not computable: needs rounding")[0], "passed")
        self.assertEqual(price("b.rounded_third  T: 1 Oct 2026  R: 1 Oct 2026",
                               "33 IDR")[0], "passed")

    def test_direction_violated(self):
        self.assertEqual(price("b.price_difference  T: 1 Oct 2026  R: 1 Oct 2026",
                               "not computable: direction violated")[0], "passed")

    def test_let_computed_only_when_used(self):
        """CALC-51."""
        self.assertEqual(price("b.with_reserve  T: 1 Oct 2026  R: 1 Oct 2026",
                               "100 IDR")[0], "passed")
        self.assertEqual(price("b.reserve_used  T: 1 Oct 2026  R: 1 Oct 2026",
                               "not computable: division by zero")[0], "passed")

    def test_helper_argument_computed_only_when_used(self):
        """CALC-51, decision 0045."""
        self.assertEqual(price("b.argument_unused  T: 1 Oct 2026  R: 1 Oct 2026",
                               "100 IDR")[0], "passed")
        self.assertEqual(price("b.argument_used  T: 1 Oct 2026  R: 1 Oct 2026",
                               "not computable: division by zero")[0], "passed")

    def test_conceptless_helper_uses_itself(self):
        """CALC-12."""
        self.assertEqual(price("b.helper_uses_itself  T: 1 Oct 2026  R: 1 Oct 2026",
                               "100 IDR")[0], "notation error")

    def test_helper_in_helper_argument_is_not_self_use(self):
        """CALC-12: the argument `first(…)` belongs to the calling rule, even
        though it is only computed inside `first` (CALC-51). Paper test M1."""
        self.assertEqual(price("b.helper_in_helper_argument  T: 1 Oct 2026  R: 1 Oct 2026",
                               "100 IDR")[0], "passed")

    def test_entity_not_yet_classified(self):
        """CALC-54: b is not yet an Item on 30 Sep."""
        self.assertEqual(price("b.rounded_third  T: 30 Sep 2026  R: 1 Oct 2026",
                               "empty")[0], "passed")

    def test_zero_without_unit(self):
        """CALC-55: the sum over an empty collection is 0 without a unit,
        although the total is in money."""
        self.assertEqual(price("b.total_expensive  T: 1 Oct 2026  R: 1 Oct 2026",
                               "not computable: unit mismatch")[0], "passed")

    def test_different_codes_do_not_cancel(self):
        """06 §2.8 (decision 0054): day and day cancel each other, day and hour
        do not, because that is a conversion. IDR·hour/day is not a money unit."""
        self.assertEqual(price("b.rate_times_days  T: 1 Oct 2026  R: 1 Oct 2026",
                               "300 IDR")[0], "passed")
        self.assertEqual(price("b.rate_times_hours  T: 1 Oct 2026  R: 1 Oct 2026",
                               "300 IDR")[0], "notation error")

    def test_wrong_result_makes_example_fail(self):
        self.assertEqual(price("b.rounded_third  T: 1 Oct 2026  R: 1 Oct 2026",
                               "33.33 IDR")[0], "failed")
        self.assertEqual(price("b.rounded_third  T: 1 Oct 2026  R: 1 Oct 2026",
                               "33 USD")[0], "failed")


class ReadingFacts(unittest.TestCase):
    """01 §2.5: reading at two times and the six fact kinds."""

    def test_correction_read_only_after_recorded(self):
        correction = "\n    b  price  120 IDR  valid 1 Oct 2026  recorded 5 Oct 2026  corrects f1"
        self.assertEqual(price("b.price  T: 10 Oct 2026  R: 4 Oct 2026", "100 IDR", correction)[0],
                         "passed")
        self.assertEqual(price("b.price  T: 10 Oct 2026  R: 5 Oct 2026", "120 IDR", correction)[0],
                         "passed")

    def test_ending_and_retraction(self):
        ending = "\n    b  price  valid 3 Oct 2026  recorded 5 Oct 2026  ends f1"
        self.assertEqual(price("b.price  T: 2 Oct 2026  R: 6 Oct 2026", "100 IDR", ending)[0], "passed")
        self.assertEqual(price("b.price  T: 3 Oct 2026  R: 6 Oct 2026", "empty", ending)[0], "passed")
        retract = "\n    b  price  valid 1 Oct 2026  recorded 5 Oct 2026  retracts f1"
        self.assertEqual(price("b.price  T: 2 Oct 2026  R: 6 Oct 2026", "empty", retract)[0], "passed")

    def test_replacement_of_corrected_fact(self):
        """01 §2.5 step 3: the correction is replaced too."""
        other = ("\n    f2: b  price  150 IDR  valid 1 Nov 2026  recorded 2 Oct 2026  replaces f1"
                 "\n    b  price  120 IDR  valid 1 Oct 2026  recorded 5 Oct 2026  corrects f1")
        self.assertEqual(price("b.price  T: 10 Oct 2026  R: 6 Oct 2026", "120 IDR", other)[0],
                         "passed")
        self.assertEqual(price("b.price  T: 2 Nov 2026  R: 6 Oct 2026", "150 IDR", other)[0],
                         "passed")
        ending = ("\n    b  price  valid 1 Nov 2026  recorded 2 Oct 2026  ends f1"
                  "\n    b  price  120 IDR  valid 1 Oct 2026  recorded 5 Oct 2026  corrects f1")
        self.assertEqual(price("b.price  T: 2 Nov 2026  R: 6 Oct 2026", "empty", ending)[0],
                         "passed")

    def test_target_must_be_labeled(self):
        without = "\n    b  price  120 IDR  valid 1 Oct 2026  recorded 5 Oct 2026  corrects f9"
        self.assertEqual(price("b.price  T: 10 Oct 2026  R: 6 Oct 2026", "120 IDR", without)[0],
                         "notation error")


RENTAL = """
module example/test@v1

concept Item
concept Rental
property item : reference Item
property start_date : date

applies to Rental:
  item required
  start_date required

example c
  kind         reject
  title        Test
  explanation  Test.
  facts        recorded 1 Oct 2026
    tent  type  Item  valid 1 Oct 2026
    table   type  Rental    valid 1 Oct 2026
  action       recorded 2 Oct 2026
{action}
  result       {result}
"""


class FormRules(unittest.TestCase):
    """04 §2.7: CONCEPT-6, CONCEPT-18, VALUE-16; 08 §2.4."""

    def run_case(self, action, result):
        return status(RENTAL.format(action=action, result=result))["c"]

    def test_forgotten_required_property(self):
        action = ("    r1  type    Rental   valid 2 Oct 2026\n"
                  "    r1  item  tent  valid 2 Oct 2026")
        self.assertEqual(self.run_case(action, "rejected by CONCEPT-18, entity r1")[0], "passed")
        self.assertEqual(self.run_case(action, "accepted")[0], "failed")

    def test_reference_to_other_concept(self):
        action = ("    r1  type    Rental         valid 2 Oct 2026\n"
                  "    r1  item  table         valid 2 Oct 2026\n"
                  "    r1  start_date   2 Oct 2026   valid 2 Oct 2026")
        self.assertEqual(self.run_case(action, "rejected by VALUE-16, entity r1")[0], "passed")

    def test_property_does_not_apply_to_its_type(self):
        action = "    tent  start_date  2 Oct 2026  valid 2 Oct 2026"
        self.assertEqual(self.run_case(action, "rejected by CONCEPT-6")[0], "passed")

    def test_complete_is_accepted(self):
        action = ("    r1  type    Rental         valid 2 Oct 2026\n"
                  "    r1  item  tent        valid 2 Oct 2026\n"
                  "    r1  start_date   2 Oct 2026   valid 2 Oct 2026")
        self.assertEqual(self.run_case(action, "accepted")[0], "passed")


if __name__ == "__main__":
    unittest.main()
