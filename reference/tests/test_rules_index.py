"""The rules index (`rules.md`) matches the documents it is made from."""

import unittest

from tools.rules_index import DOCUMENTS, OUTPUT, ROOT, build, rules_of


class TestRulesIndex(unittest.TestCase):
    def test_index_is_up_to_date(self):
        self.assertEqual(
            OUTPUT.read_text(encoding="utf-8"), build(),
            "rules.md is out of date: run `python -m tools.rules_index` from reference/",
        )

    def test_every_rule_is_defined_once(self):
        seen = []
        for name in DOCUMENTS:
            for _, items in rules_of(ROOT / name)[2]:
                seen += [rid for rid, _, _ in items]
        self.assertEqual(len(seen), len(set(seen)))
        self.assertGreater(len(seen), 0)


if __name__ == "__main__":
    unittest.main()
