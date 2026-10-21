"""Runs every example in the case files and in the calculation library.

Every example MUST pass. So that passing is meaningful, every example is also
run with a deliberately changed result, and it MUST fail. The content library
modules (the calculation library and the code lists) are always available, so
cases can use them.
"""

import os
import re
import unittest
from pathlib import Path

from calculator.reader import read
from calculator.examples import run_all
from calculator.module_set import ModuleSet

FOLDER = Path(__file__).parent
CONTENT = FOLDER.parents[1] / "content"
LIBRARY = sorted(CONTENT.rglob("*.md"))
FILES = sorted((FOLDER.parents[1] / "conformance").glob("*.md")) + LIBRARY
# CASES="15-change.md,17-vocabulary.md" limits the case files that are run.
if os.environ.get("CASES"):
    _SELECTED = set(os.environ["CASES"].split(","))
    FILES = [b for b in FILES if b.name in _SELECTED or b in LIBRARY]

# A replacement result that is certainly wrong, by the shape of the original result.
_WRONG = [
    (re.compile(r"^accepted$"), "rejected by CONCEPT-6"),
    (re.compile(r"^rejected by "), "accepted"),
    (re.compile(r"^not computable: "), "empty"),
    (re.compile(r"^empty$"), "not computable: division by zero"),
    (re.compile(r".*"), "123,456,789 IDR"),
]

_RESULT_RE = re.compile(r"^(  result +)(.*)$", re.MULTILINE)


def reports_for(text, file):
    """The report of the examples in `text` only, with the other library
    modules also read."""
    own = read(text, markdown=True)
    other = [m for p in LIBRARY if p != file
             for m in read(p.read_text(encoding="utf-8"), markdown=True)]
    address = {m.address for m in own}
    return {(report.example, report.version): report for report in run_all(ModuleSet(own + other))
            if report.example.rpartition("/")[0] in address}


def _is_replaced(text, position, original):
    """A result in a replaced example is not run again (PROOF-21), so changing
    it does not make that example fail."""
    name = re.findall(r"^example (\S+)$", text[:position], re.MULTILINE)[-1]
    address, version = re.findall(r"^module (\S+)@(\S+)$", text[:position], re.MULTILINE)[-1]
    report = original.get((f"{address}/{name}", version))
    return report is not None and report.status == "replaced"


class Cases(unittest.TestCase):
    def test_files_exist(self):
        self.assertTrue(FILES)

    def test_all_examples_pass(self):
        for file in FILES:
            for address, report in reports_for(file.read_text(encoding="utf-8"), file).items():
                with self.subTest(example=address):
                    self.assertIn(report.status, ("passed", "replaced"), report.detail)

    def test_changed_result_makes_example_fail(self):
        for file in FILES:
            text = file.read_text(encoding="utf-8")
            original = reports_for(text, file)
            for m in _RESULT_RE.finditer(text):
                if _is_replaced(text, m.start(), original):
                    continue
                wrong = next(replacement for pattern, replacement in _WRONG if pattern.match(m.group(2)))
                changed = text[:m.start(2)] + wrong + text[m.end(2):]
                diff = [(address, report.status) for address, report in reports_for(changed, file).items()
                        if report.status != original[address].status]
                with self.subTest(file=file.name, line=text.count("\n", 0, m.start()) + 1):
                    self.assertEqual(len(diff), 1, diff)
                    self.assertEqual(diff[0][1], "failed", diff)


if __name__ == "__main__":
    unittest.main()
