"""Tests for the version comparer (07 §2.2, 08 §2.7) and bridges (05 §2.5).

Their cases are in conformance/15-change.md and conformance/16-relations.md.
Here the result of the comparison is checked, and the situations that MUST be
rejected.
"""

import re
import unittest
from pathlib import Path

from calculator.reader import read
from calculator.examples import run_all
from calculator.values import NotationError
from calculator.module_set import ModuleSet
from calculator.versions import compare_versions

REFERENCE = Path(__file__).parent.parent
# Content (calculation library, code lists, vocabulary) is always read.
CONTENT = [p.read_text(encoding="utf-8") for p in sorted((REFERENCE.parent / "content").rglob("*.md"))]
CHANGE = (REFERENCE.parent / "conformance" / "15-change.md").read_text(encoding="utf-8")
RELATIONS = (REFERENCE.parent / "conformance" / "16-relations.md").read_text(encoding="utf-8")


def build_set(*text):
    return ModuleSet([m for t in CONTENT + list(text) for m in read(t, markdown=True)])


def compare(text, old, new):
    s = build_set(text)
    module = {m.full_name: m for m in s.all_modules()}
    return compare_versions(s, module[old], module[new])


def status(text):
    return {(report.example, report.version): report.status for report in run_all(build_set(text))}


def module_only(text, address):
    """One module of the writing, up to the next module."""
    start = text.index(f"module {address}\n")
    end = text.find("\nmodule ", start + 1)
    closer = text.find("\n```", start)
    end = min(x for x in (end, closer) if x != -1)
    return text[start:end]


class KindsOfChange(unittest.TestCase):
    def test_new_property_is_one_addition(self):  # U1, 07 §4
        h = compare(CHANGE, "rudi/rental@v1", "rudi/rental@v2")
        self.assertEqual(h.added, ["rudi/rental/promised_return_date"])
        self.assertEqual((h.modified, h.removed, h.meaning_changed, h.became_required, h.uses),
                         ([], [], [], [], []))

    def test_user_moves_version(self):  # U2
        h = compare(CHANGE, "kemah-ceria/shop@v1", "kemah-ceria/shop@v2")
        self.assertEqual(h.added, ["kemah-ceria/shop/promised_return_old_rental"])
        self.assertEqual(h.uses, ["rudi/rental: v1 → v2"])

    def test_user_bound_to_exact_version(self):  # CHANGE-14, 15
        s = build_set(CHANGE)
        module = {m.full_name: m for m in s.all_modules()}
        self.assertIn(module["rudi/rental@v1"], s.installed_modules(module["kemah-ceria/shop@v1"]))
        self.assertNotIn(module["rudi/rental@v2"], s.installed_modules(module["kemah-ceria/shop@v1"]))

    def test_behavior_change(self):  # U3, PROOF-22
        h = compare(CHANGE, "uniti/depreciation@v3", "uniti/depreciation@v4")
        self.assertEqual(h.added, ["uniti/depreciation/march_accumulated_remainder_first"])
        self.assertEqual(h.modified, ["uniti/depreciation/depreciation", "uniti/depreciation/march_accumulated"])
        self.assertEqual(len(h.behavior_changes), 1)
        p = h.behavior_changes[0]
        self.assertEqual((p.example, p.old, p.new),
                         ("uniti/depreciation/march_accumulated", "999,999 IDR", "1,000,011 IDR"))
        self.assertIn("new policy", p.reason)

    def test_removed_example(self):  # CHANGE-6, PROOF-21
        start = CHANGE.index("example february_depreciation", CHANGE.index("module uniti/depreciation@v4"))
        end = CHANGE.index("example march_accumulated_remainder_first")
        text = CHANGE[:start] + CHANGE[end:]
        h = compare(text, "uniti/depreciation@v3", "uniti/depreciation@v4")
        self.assertEqual(h.removed, ["uniti/depreciation/february_depreciation"])

    def test_unmarked_failure_blocks_freezing(self):  # 08 §2.6
        v4 = CHANGE.index("module uniti/depreciation@v4")
        section = CHANGE[v4:]
        for line in ("  status       replaced\n",
                     "  reason       Following the new policy: the remainder goes to the first month.\n",
                     "  replaced_by  march_accumulated_remainder_first\n"):
            section = section.replace(line, "", 1)
        result = status(CHANGE[:v4] + section)
        self.assertEqual(result[("uniti/depreciation/march_accumulated", "v4")], "failed")

    def test_version_jump(self):  # CHANGE-2
        text = CHANGE.replace("module rudi/rental@v2", "module rudi/rental@v3")
        with self.assertRaisesRegex(NotationError, "CHANGE-2"):
            compare(text.replace("uses rudi/rental@v2", "uses rudi/rental@v3"),
                    "rudi/rental@v1", "rudi/rental@v3")

    def test_meaning_changed(self):  # CHANGE-7, 04 §2.9
        old = module_only(CHANGE, "rudi/rental@v1")
        new = (old.replace("@v1", "@v2")
               .replace("property start_date : date", "property start_date : instant"))
        text = "```uniti\n" + old + "\n" + new + "\n```\n"
        h = compare(text, "rudi/rental@v1", "rudi/rental@v2")
        self.assertEqual(h.meaning_changed, ["rudi/rental/start_date"])

    def test_became_required(self):  # 04 §2.9
        old = module_only(CHANGE, "rudi/rental@v1")
        old = re.sub(r"\nexample .*", "", old, flags=re.DOTALL)
        new = (old.replace("@v1", "@v2")
               .replace("  end_date     required\n", "  end_date     required\n  daily_rate   required\n"))
        text = "```uniti\n" + old + "\n" + new + "\n```\n"
        h = compare(text, "rudi/rental@v1", "rudi/rental@v2")
        self.assertEqual(h.became_required, ["daily_rate for Rental"])
        self.assertEqual(h.modified, ["rudi/rental/applies to Rental: daily_rate"])


class Bridges(unittest.TestCase):
    def test_combined_examples_pass(self):  # U4
        self.assertEqual(set(status(RELATIONS).values()), {"passed"})

    def test_bridge_read_on_card(self):
        s = build_set(RELATIONS)
        cashier = next(m for m in s.all_modules() if m.address == "klinik-sehat/cashier")
        self.assertEqual(cashier.content["bpjs"].bridges, [("same_as", "apotek-ria/cashier/bpjs")])

    def test_bridge_to_external_standard(self):  # RELATION-8
        text = "module example/a@v1\n\nconcept Class\n  similar      https://schema.org/Course\n"
        self.assertEqual(read(text)[0].content["Class"].bridges, [("similar", "https://schema.org/Course")])

    def test_bridge_without_full_address(self):  # RELATION-8
        text = "module example/a@v1\n\nconcept Class\n  similar      Course\n"
        with self.assertRaisesRegex(NotationError, "RELATION-8"):
            read(text)

    def test_bridge_of_different_kind(self):  # RELATION-12
        text = RELATIONS.replace("same_as      apotek-ria/cashier/bpjs",
                                 "same_as      uniti/payment/Payment")
        with self.assertRaisesRegex(NotationError, "RELATION-12"):
            build_set(text)

    def test_choice_of_uninstalled_module(self):  # RELATION-5
        text = RELATIONS.replace("module klinik-sehat/report@v1\n  uses uniti/payment@v1\n"
                                 "  uses klinik-sehat/cashier@v1\n  uses apotek-ria/cashier@v1\n",
                                 "module klinik-sehat/report@v1\n  uses uniti/payment@v1\n"
                                 "  uses klinik-sehat/cashier@v1\n")
        result = status(text)
        self.assertEqual(result[("klinik-sehat/report/combined_bpjs_october", "v1")],
                         "notation error")


if __name__ == "__main__":
    unittest.main()
