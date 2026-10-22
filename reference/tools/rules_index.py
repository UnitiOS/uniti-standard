"""Builds `rules.md`, the index of every rule in the form documents and in
appendix A.

The index is made from the text, never written by hand. The rule in its
document is the rule; the index only shows where it is and how it starts.
A test fails when `rules.md` no longer matches the text.

To run, from `reference/`:

    python -m tools.rules_index          # writes ../rules.md
    python -m tools.rules_index --check  # only compares
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "rules.md"

# The documents that hold rules, in reading order.
DOCUMENTS = [
    "form/01-facts.md",
    "form/02-addresses.md",
    "form/03-values.md",
    "form/04-concepts.md",
    "form/05-relations.md",
    "form/06-calculation-rules.md",
    "form/07-change.md",
    "form/08-proof.md",
    "appendix/A-notation.md",
]

KEYWORDS = ["MUST NOT", "SHOULD NOT", "MUST", "SHOULD", "MAY"]
# The order in which the keywords of one rule are shown.
_SHOWN = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY"]

_RULE = re.compile(r"^- \*\*([A-Z]+-\d+)\.\*\*\s*(.*)$")
_GROUP = re.compile(r"^\*\*([^*]+)\*\*$")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def _anchor(heading: str) -> str:
    """The anchor that GitHub gives a heading."""
    text = heading.lstrip("#").strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def _first_sentence(text: str) -> str:
    """The first sentence, followed by "…" when the rule says more. A revoked
    rule, written in italics, is shown whole."""
    text = _LINK.sub(r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    if text.startswith("*") and text.endswith("*"):
        return text
    # A sentence ends at a full stop followed by a space and a capital letter,
    # outside code.
    inside = False
    for i, ch in enumerate(text):
        if ch == "`":
            inside = not inside
        elif ch == "." and not inside and text[i + 1:i + 3].strip()[:1].isupper() \
                and text[i + 1:i + 2] == " ":
            return text[:i + 1] + " …"
    return text


def _keywords(text: str) -> list[str]:
    found = []
    rest = re.sub(r"\s+", " ", text)
    for word in KEYWORDS:
        if re.search(r"\b" + word + r"\b", rest):
            found.append(word)
            rest = re.sub(r"\b" + word + r"\b", " ", rest)
    return [word for word in _SHOWN if word in found]


def rules_of(path: Path) -> tuple[str, str, list[tuple[str, list[tuple[str, str, list[str]]]]]]:
    """The title of a document, the anchor of its rules section, and its rules
    by group: (group, [(id, full text, keywords)])."""
    lines = path.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ").strip()
    anchor, groups = "", []
    in_rules, current = False, None
    for line in lines:
        if line.startswith("## "):
            in_rules = line.startswith("## 3. Rules")
            if in_rules:
                anchor = _anchor(line)
            current = None
            continue
        if not in_rules:
            continue
        group = _GROUP.match(line)
        if group:
            groups.append((group.group(1), []))
            continue
        rule = _RULE.match(line)
        if rule:
            if not groups:
                groups.append(("", []))
            current = [rule.group(1), rule.group(2)]
            groups[-1][1].append(current)
        elif current is not None and line.startswith("  ") and line.strip():
            current[1] += " " + line.strip()
        else:
            current = None
    return title, anchor, [
        (name, [(rid, text, _keywords(text)) for rid, text in items]) for name, items in groups
    ]


def build() -> str:
    out = [
        "# Rules index",
        "",
        "Status: generated; not normative",
        "",
        "Every rule of the form documents and of appendix A, in reading order.",
        "Each line shows the rule's ID, the requirement keywords it uses, and its",
        "first sentence, with \"…\" when the rule says more. The rule itself is",
        "the text in its document, which may hold more sentences, exceptions,",
        "and examples: read it there before relying on a rule.",
        "",
        "This file is made by `reference/tools/rules_index.py`. Do not edit it by",
        "hand; a test fails when it no longer matches the documents.",
        "",
    ]
    total = 0
    for name in DOCUMENTS:
        title, anchor, groups = rules_of(ROOT / name)
        count = sum(len(items) for _, items in groups)
        total += count
        out += [f"## [{title}]({name}#{anchor})", "", f"{count} rules.", ""]
        for group, items in groups:
            if group:
                out += [f"**{group}**", ""]
            out += ["| Rule | Keywords | First sentence |", "|---|---|---|"]
            for rid, text, words in items:
                sentence = _first_sentence(text).replace("|", "\\|")
                out.append(f"| {rid} | {', '.join(words) or '—'} | {sentence} |")
            out.append("")
    out[4:4] = [f"{total} rules in {len(DOCUMENTS)} documents.", ""]
    return "\n".join(out)


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        same = OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == text
        print("rules.md is up to date" if same else "rules.md is out of date")
        sys.exit(0 if same else 1)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"written {OUTPUT}")
