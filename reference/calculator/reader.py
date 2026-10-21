"""Reader of the reference notation, according to appendix/A-notation.md.

The reader turns writing into a module set: modules, cards, rules, and
examples, with the expression of a rule as a tree. The meaning of each name
(which property, which choice) is decided later by the evaluator, because
it depends on the modules in use (appendix A §2.5).

Writing that does not follow the notation raises NotationError, with its
line number.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .values import (
    QUANTITIES, MONTH_NAMES, Number, NotationError, Unit, Text, parse_numeral,
    parse_unit, parse_time,
)


# --- Keywords (appendix A §2.5) ---------------------------------------------

# The call form of each operation (appendix A §2.7, NOTATION-15). For each
# operation: the valid forms of the plain arguments, and the named arguments
# in order, each with its kind and whether it is required. Argument kinds:
#   u   expression
#   p   binder with one name
#   p2  binder with two names
#   k   concept name
#   s   unit
CALL_FORMS: dict[str, tuple[tuple[str, ...], dict[str, tuple[str, bool]]]] = {
    "all": (("k", "k p"), {}),
    "single": (("u",), {}),
    "count": (("u",), {}),
    "exists": (("u",), {}),
    "unit_of": (("u",), {}),
    "before_action": (("u",), {}),
    "each": (("u p",), {}),
    "each_merged": (("u p",), {}),
    "group": (("u",), {"by": ("p", True)}),
    "sum": (("u", "u p"), {}),
    "min": (("u", "u p", "u u"), {}),
    "max": (("u", "u p", "u u"), {}),
    "all_match": (("u p",), {}),
    "any_match": (("u p",), {}),
    "power": (("u u",), {}),
    "floor_multiple": (("u",), {"of": ("u", True)}),
    "range": (("u u",), {}),
    "overlap": (("u u",), {}),
    "at": (("u u",), {}),
    "append": (("u u",), {}),
    "difference": (("u u s",), {}),
    "span": (("u s",), {}),
    "split": (("u",), {"step": ("u", True)}),
    "history": (("u",), {"in": ("u", True)}),
    "convert": (("u",), {"to": ("s", True)}),
    "not_computable": (("u",), {}),
    "fold": (("u",), {"order_by": ("p", False), "initial": ("u", True),
                      "step": ("p2", True)}),
}

SPECIALS = frozenset({"this", "T", "this_action", "contributions"})

KEYWORDS = SPECIALS | frozenset({
    "yes", "no", "if", "then", "else", "and", "or", "not",
    "in", "let", "with",
}) | frozenset(CALL_FORMS)

COMPARISONS = frozenset({"=", "≠", "<", "≤", ">", "≥", "in"})


# --- Expression tree --------------------------------------------------------

@dataclass(frozen=True)
class Fixed:
    """A fixed value (appendix A §2.3)."""
    value: object


@dataclass(frozen=True)
class Name:
    """A name without a dot: a local name, a choice, or a unit (§2.5)."""
    name: str
    lineno: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Special:
    """`this`, `T`, `this_action`, or `contributions`."""
    keyword: str


@dataclass(frozen=True)
class Dot:
    """`x.s`, or `x.s(…)` for a computed property and a helper with parameters."""
    base: object
    name: str
    arguments: tuple | None = None


@dataclass(frozen=True)
class Binder:
    """`x: u`, or `(a, k): u` (§2.7)."""
    names: tuple[str, ...]
    body: object


@dataclass(frozen=True)
class UnitLiteral:
    """A unit in the place of a unit: the third argument of `difference`, and so on."""
    unit: Unit


@dataclass(frozen=True)
class Call:
    """An operation call, with plain arguments and named arguments."""
    name: str
    positional: tuple
    named: tuple[tuple[str, object], ...]
    lineno: int = field(default=0, compare=False)

    def arg(self, name: str, default: object = None) -> object:
        return dict(self.named).get(name, default)


@dataclass(frozen=True)
class HelperCall:
    """A call of a helper without a concept: `scale(entries, 2)`."""
    name: str
    arguments: tuple
    lineno: int = field(default=0, compare=False)


@dataclass(frozen=True)
class Unary:
    """A one-sided operation: a leading `−`, or `not`."""
    op: str
    x: object


@dataclass(frozen=True)
class Binary:
    """A two-sided operation: arithmetic, comparison, `in`, `and`, `or`."""
    op: str
    a: object
    b: object


@dataclass(frozen=True)
class Conditional:
    condition: object
    then: object
    otherwise: object


@dataclass(frozen=True)
class WithRecord:
    record: object
    name: str
    value: object


@dataclass(frozen=True)
class Let:
    name: str
    value: object
    body: object


@dataclass(frozen=True)
class RecordLiteral:
    parts: tuple[tuple[str, object], ...]


@dataclass(frozen=True)
class CollectionLiteral:
    members: tuple


def render(n: object) -> str:
    """The tree written back with full parentheses, for tests and messages."""
    if isinstance(n, Fixed):
        x = n.value
        if isinstance(x, bool):
            return "yes" if x else "no"
        if isinstance(x, Text):
            return '"' + x.content.replace('"', '""') + '"' + (f"@{x.language}" if x.language else "")
        return str(x)
    if isinstance(n, Name):
        return n.name
    if isinstance(n, Special):
        return n.keyword
    if isinstance(n, Dot):
        args = "" if n.arguments is None else "(" + ", ".join(map(render, n.arguments)) + ")"
        return f"{render(n.base)}.{n.name}{args}"
    if isinstance(n, Binder):
        name = n.names[0] if len(n.names) == 1 else "(" + ", ".join(n.names) + ")"
        return f"{name}: {render(n.body)}"
    if isinstance(n, UnitLiteral):
        return str(n.unit)
    if isinstance(n, Call):
        all_args = [render(a) for a in n.positional] + [f"{k}: {render(v)}" for k, v in n.named]
        return f"{n.name}({', '.join(all_args)})"
    if isinstance(n, HelperCall):
        return f"{n.name}({', '.join(map(render, n.arguments))})"
    if isinstance(n, Unary):
        return f"({n.op} {render(n.x)})"
    if isinstance(n, Binary):
        return f"({render(n.a)} {n.op} {render(n.b)})"
    if isinstance(n, Conditional):
        return f"(if {render(n.condition)} then {render(n.then)} else {render(n.otherwise)})"
    if isinstance(n, WithRecord):
        return f"({render(n.record)} with {n.name} = {render(n.value)})"
    if isinstance(n, Let):
        return f"(let {n.name} = {render(n.value)}; {render(n.body)})"
    if isinstance(n, RecordLiteral):
        return "{" + ", ".join(f"{k}: {render(v)}" for k, v in n.parts) + "}"
    if isinstance(n, CollectionLiteral):
        return "[" + ", ".join(map(render, n.members)) + "]"
    raise TypeError(n)


# --- Lines (appendix A §2.2) ------------------------------------------------

@dataclass(frozen=True)
class Line:
    lineno: int
    indent: int
    content: str


def _strip_comment(text: str) -> str:
    """`#` starts a comment up to the end of the line, except inside text."""
    in_quotes = False
    for i, c in enumerate(text):
        if c == '"':
            in_quotes = not in_quotes
        elif c == "#" and not in_quotes:
            return text[:i]
    return text


def split_lines(text: str) -> list[Line]:
    """The lines that have content, without comments. Empty lines are skipped."""
    result = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw:
            raise NotationError(f"line {lineno}: tabs are not used (§2.2)")
        content = _strip_comment(raw).rstrip()
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        result.append(Line(lineno, indent, content.strip()))
    return result


_FENCE = re.compile(r"^(`{3,}|~{3,})\s*(\S*)\s*$")


def from_markdown(text: str) -> str:
    """Only code blocks tagged `uniti` are read (§2.10, NOTATION-21).

    Other lines are blanked, so that line numbers stay the same as in the
    file.
    """
    out = []
    fence = None
    in_uniti_block = False
    for source_line in text.splitlines():
        m = _FENCE.match(source_line.strip())
        if fence is None and m:
            fence, in_uniti_block = m.group(1), m.group(2) == "uniti"
            out.append("")
        elif fence is not None and m and m.group(1).startswith(fence[0]) \
                and len(m.group(1)) >= len(fence) and not m.group(2):
            fence, in_uniti_block = None, False
            out.append("")
        else:
            out.append(source_line if in_uniti_block else "")
    return "\n".join(out)


# --- Tokens -----------------------------------------------------------------

@dataclass(frozen=True)
class Token:
    kind: str          # value, name, symbol, newline, end
    text: str
    value: object = None
    lineno: int = 0


_NAME_PART = r"[A-Za-z_][A-Za-z0-9_]*(?:-[A-Za-z0-9]+)*[²³]?"
_NAME_RE = re.compile(rf"{_NAME_PART}(?:[/·]{_NAME_PART})*")
_NUMBER_RE = re.compile(r"(?:\d{1,3}(?:,\d{3})+(?!\d)|\d+)(?:\.\d+)?%?")
_AFTER_NUMBER = re.compile(rf" +({_NAME_PART}(?:[/·]{_NAME_PART})*)")
_ZONE = r"(?:WITA|WIB|WIT|UTC(?:[+−]\d{1,2}(?::\d{2})?)?)"
_TIME_RE = re.compile(
    rf"(\d{{1,2}}) ([A-Za-z]+) (\d{{4}})(?!\d)"
    rf"(?: \d{{2}}:\d{{2}}(?::\d{{2}})?(?!\d)(?: {_ZONE})?)?")
_TEXT_RE = re.compile(r'"((?:[^"]|"")*)"(?:@([A-Za-z]+(?:-[A-Za-z0-9]+)*))?')
_SYMBOLS = frozenset("()[]{},:.+−×÷=≠<≤>≥")


def _tokenize_line(content: str, lineno: int, default_zone) -> list[Token]:
    result: list[Token] = []
    i = 0
    while i < len(content):
        c = content[i]
        if c == " ":
            i += 1
            continue
        if c == '"':
            m = _TEXT_RE.match(content, i)
            if not m:
                raise NotationError(f"line {lineno}: quotation mark is not closed")
            value = Text(m.group(1).replace('""', '"'), m.group(2))
            result.append(Token("value", m.group(), value, lineno))
            i = m.end()
        elif c.isdigit():
            m = _TIME_RE.match(content, i)
            if m and m.group(2).lower() in MONTH_NAMES:
                result.append(Token("value", m.group(), parse_time(m.group(), default_zone), lineno))
                i = m.end()
                continue
            m = _NUMBER_RE.match(content, i)
            text = m.group()
            value: object = Number(parse_numeral(text))
            i = m.end()
            m2 = _AFTER_NUMBER.match(content, i)
            if m2 and not text.endswith("%"):
                keyword = m2.group(1)
                head = re.match(r"[A-Za-z_][A-Za-z0-9_]*", keyword).group()
                if head.lower() in MONTH_NAMES:
                    raise NotationError(
                        f"line {lineno}: date without a year: {text} {keyword} (NOTATION-6)")
                if head not in KEYWORDS:
                    value = Number(value.value, parse_unit(keyword))
                    text = f"{text} {keyword}"
                    i = m2.end()
            result.append(Token("value", text, value, lineno))
        elif c.isalpha() or c == "_":
            m = _NAME_RE.match(content, i)
            result.append(Token("name", m.group(), None, lineno))
            i = m.end()
        elif c in _SYMBOLS:
            result.append(Token("symbol", c, None, lineno))
            i += 1
        elif c == "-":
            raise NotationError(
                f"line {lineno}: a hyphen is not a minus sign; write − (NOTATION-4)")
        else:
            raise NotationError(f"line {lineno}: character {c!r} is not recognized (NOTATION-4)")
    return result


def tokens_of(lines: list[Line], default_zone=None) -> list[Token]:
    """Tokens of several lines, with a `newline` token between lines."""
    result: list[Token] = []
    for k, b in enumerate(lines):
        if k:
            result.append(Token("newline", "↵", None, b.lineno))
        result.extend(_tokenize_line(b.content, b.lineno, default_zone))
    result.append(Token("end", "end of text", None, lines[-1].lineno if lines else 0))
    return result


# --- Expression parser (appendix A §2.6, §2.7, §2.11) -----------------------

_LOCAL_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class _Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.depth = 0
        # The parenthesis depth of each `let` being read: at that depth, a
        # line break ends its expression (§2.6).
        self.let_depths: list[int] = []

    # Reading tokens

    def _newline_visible(self) -> bool:
        return bool(self.let_depths) and self.let_depths[-1] == self.depth

    def _peek_index(self, ahead: int = 0) -> tuple[Token, int]:
        i, n = self.pos, 0
        while True:
            t = self.tokens[i]
            if t.kind == "newline" and not self._newline_visible():
                i += 1
                continue
            if n == ahead or t.kind == "end":
                return t, i
            n += 1
            i += 1

    def _peek(self, ahead: int = 0) -> Token:
        return self._peek_index(ahead)[0]

    def _take(self) -> Token:
        t, i = self._peek_index()
        if t.kind != "end":
            self.pos = i + 1
        if t.kind == "symbol":
            if t.text in "([{":
                self.depth += 1
            elif t.text in ")]}":
                self.depth -= 1
        return t

    def _is_token(self, text: str, ahead: int = 0) -> bool:
        t = self._peek(ahead)
        return t.kind in ("symbol", "name") and t.text == text

    def _error(self, t: Token, message: str) -> NotationError:
        return NotationError(f"line {t.lineno}, near {t.text!r}: {message}")

    def _expect(self, text: str) -> Token:
        t = self._take()
        if not (t.kind in ("symbol", "name") and t.text == text):
            raise self._error(t, f"expected {text!r}")
        return t

    def _word(self) -> str:
        """Any name, including a keyword: a name after a dot, the name of a
        record part (§2.5)."""
        t = self._take()
        if t.kind != "name":
            raise self._error(t, "expected a name")
        return t.text

    def _local_name(self) -> str:
        t = self._take()
        if t.kind != "name" or not _LOCAL_NAME_RE.match(t.text):
            raise self._error(t, "expected a local name: lowercase letters, digits, underscore")
        if t.text in KEYWORDS:
            raise self._error(t, "a keyword MUST NOT be a local name (NOTATION-10)")
        return t.text

    # Short notation (§2.11)

    def parse_expr(self) -> object:
        t, i = self._peek_index()
        if t.kind == "name" and t.text == "let":
            if i > 0 and self.tokens[i - 1].kind != "newline":
                raise self._error(t, "let MUST occupy its own line (NOTATION-14)")
            self._take()
            name = self._local_name()
            self._expect("=")
            self.let_depths.append(self.depth)
            value = self.parse_if()
            end = self._take()
            self.let_depths.pop()
            if end.kind != "newline":
                raise self._error(end, "let MUST occupy its own line, "
                                         "and be followed by its result (NOTATION-14)")
            return Let(name, value, self.parse_expr())
        return self.parse_if()

    def parse_if(self) -> object:
        if self._is_token("if"):
            self._take()
            condition = self.parse_expr()
            self._expect("then")
            then = self.parse_expr()
            if not self._is_token("else"):
                raise self._error(self._peek(), "if MUST use else (NOTATION-13)")
            self._take()
            return Conditional(condition, then, self.parse_expr())
        return self.parse_with()

    def parse_with(self) -> object:
        x = self.parse_or()
        while self._is_token("with"):
            self._take()
            name = self._word()
            self._expect("=")
            x = WithRecord(x, name, self.parse_or())
        return x

    def parse_or(self) -> object:
        x = self.parse_and()
        while self._is_token("or"):
            self._take()
            x = Binary("or", x, self.parse_and())
        return x

    def parse_and(self) -> object:
        x = self.parse_not()
        while self._is_token("and"):
            self._take()
            x = Binary("and", x, self.parse_not())
        return x

    def parse_not(self) -> object:
        if self._is_token("not"):
            self._take()
            return Unary("not", self.parse_not())
        return self.parse_comparison()

    def _comparison_next(self) -> bool:
        t = self._peek()
        return t.kind in ("symbol", "name") and t.text in COMPARISONS

    def parse_comparison(self) -> object:
        a = self.parse_add()
        if self._comparison_next():
            op = self._take().text
            b = self.parse_add()
            if self._comparison_next():
                raise self._error(self._peek(), "a comparison MUST NOT be chained (NOTATION-12)")
            return Binary(op, a, b)
        return a

    def parse_add(self) -> object:
        x = self.parse_multiply()
        while self._is_token("+") or self._is_token("−"):
            op = self._take().text
            x = Binary(op, x, self.parse_multiply())
        return x

    def parse_multiply(self) -> object:
        x = self.parse_negation()
        while self._is_token("×") or self._is_token("÷"):
            op = self._take().text
            x = Binary(op, x, self.parse_negation())
        return x

    def parse_negation(self) -> object:
        if self._is_token("−"):
            self._take()
            return Unary("−", self.parse_negation())
        return self.parse_postfix()

    def parse_postfix(self) -> object:
        x = self.parse_primary()
        while self._is_token("."):
            self._take()
            name = self._word()
            arguments = None
            if self._is_token("("):
                self._take()
                arguments = tuple(self._list_until(")"))
            x = Dot(x, name, arguments)
        return x

    def _list_until(self, closer: str) -> list[object]:
        result = []
        if not self._is_token(closer):
            result.append(self.parse_expr())
            while self._is_token(","):
                self._take()
                result.append(self.parse_expr())
        self._expect(closer)
        return result

    def parse_primary(self) -> object:
        t = self._take()
        if t.kind == "value":
            return Fixed(t.value)
        if t.kind == "name":
            if t.text in ("yes", "no"):
                return Fixed(t.text == "yes")
            if t.text in SPECIALS:
                return Special(t.text)
            if t.text in CALL_FORMS:
                return self._call(t)
            if t.text in KEYWORDS:
                raise self._error(t, "keyword out of place")
            if self._is_token("("):
                self._take()
                return HelperCall(t.text, tuple(self._list_until(")")), t.lineno)
            return Name(t.text, t.lineno)
        if t.text == "(":
            x = self.parse_expr()
            self._expect(")")
            return x
        if t.text == "{":
            parts: list[tuple[str, object]] = []
            if not self._is_token("}"):
                while True:
                    name = self._word()
                    if name in dict(parts):
                        raise self._error(t, f"part {name!r} is written twice")
                    self._expect(":")
                    parts.append((name, self.parse_expr()))
                    if not self._is_token(","):
                        break
                    self._take()
            self._expect("}")
            return RecordLiteral(tuple(parts))
        if t.text == "[":
            return CollectionLiteral(tuple(self._list_until("]")))
        raise self._error(t, "expected a value, a name, or a parenthesis")

    # Operation calls (§2.7)

    def _binder_start(self) -> bool:
        if self._peek().kind == "name" and self._is_token(":", 1):
            return True
        return (self._is_token("(") and self._peek(1).kind == "name"
                and self._is_token(",", 2) and self._peek(3).kind == "name"
                and self._is_token(")", 4) and self._is_token(":", 5))

    def _binder(self, two: bool) -> Binder:
        if two:
            self._expect("(")
            name = (self._local_name(),)
            self._expect(",")
            name += (self._local_name(),)
            self._expect(")")
        else:
            name = (self._local_name(),)
        self._expect(":")
        return Binder(name, self.parse_expr())

    def _call(self, t: Token) -> Call:
        positional_forms, named_forms = CALL_FORMS[t.text]
        self._expect("(")
        positional: list[object] = []
        named: list[tuple[str, object]] = []
        if not self._is_token(")"):
            while True:
                keyword = self._peek()
                if keyword.kind == "name" and self._is_token(":", 1) and keyword.text in named_forms:
                    self._take()
                    self._take()
                    kind = named_forms[keyword.text][0]
                    if kind in ("p", "p2"):
                        value = self._binder(kind == "p2")
                    elif kind == "s":
                        name = self._take()
                        if name.kind != "name":
                            raise self._error(name, f"{keyword.text}: expected a name")
                        value = UnitLiteral(parse_unit(name.text))
                    else:
                        value = self.parse_expr()
                    named.append((keyword.text, value))
                elif named:
                    raise self._error(keyword, "plain argument written before a named argument (§2.7)")
                elif self._binder_start():
                    positional.append(self._binder(self._is_token("(")))
                else:
                    positional.append(self.parse_expr())
                if not self._is_token(","):
                    break
                self._take()
        self._expect(")")
        return _check_form(t, positional, named)


def _matches(kind: str, arg: object) -> bool:
    if kind == "p":
        return isinstance(arg, Binder) and len(arg.names) == 1
    if kind in ("k", "s"):
        return isinstance(arg, Name)
    return not isinstance(arg, Binder)


def _check_form(t: Token, positional: list, named: list) -> Call:
    """NOTATION-15: every call follows its call form."""
    positional_forms, named_forms = CALL_FORMS[t.text]
    error = NotationError(
        f"line {t.lineno}: {t.text}(…) does not follow its call form (NOTATION-15)")
    for form in positional_forms:
        kind = form.split()
        if len(kind) == len(positional) and all(_matches(m, a) for m, a in zip(kind, positional)):
            break
    else:
        raise error
    positional = [UnitLiteral(parse_unit(a.name)) if m == "s" else a for m, a in zip(kind, positional)]
    name = [n for n, _ in named]
    order = [n for n in named_forms if n in name]
    required = [n for n, (_, w) in named_forms.items() if w]
    if name != order or any(n not in name for n in required):
        raise error
    if t.text == "history" and not isinstance(positional[0], Dot):
        raise NotationError(f"line {t.lineno}: history requires x.s (NOTATION-15)")
    return Call(t.text, tuple(positional), tuple(named), t.lineno)


def parse_expression(lines: list[Line], default_zone=None) -> object:
    """Parses one expression from its lines.

    `default_zone` is given only inside an example; inside a rule, an instant
    MUST name its zone (NOTATION-7).
    """
    p = _Parser(tokens_of(lines, default_zone))
    result = p.parse_expr()
    t = p._take()
    if t.kind != "end":
        raise p._error(t, "the expression should have ended")
    return result


def parse_text(text: str, default_zone=None, lineno: int = 0) -> object:
    """Parses a one-line expression, for instance the question of an example."""
    return parse_expression([Line(lineno, 0, text.strip())], default_zone)


# --- Modules, cards, and rules (appendix A §2.8) ----------------------------

VALUE_TYPES = frozenset({"text", "number", "yes_no", "date", "instant", "choice", "reference"})
INTERMEDIATE_TYPES = frozenset({"collection", "record", "range"})
DIRECTIONS = frozenset({"increase", "decrease", "no_direction", "level"})


@dataclass(frozen=True)
class ValueType:
    """The value type in the heading line of a property or a rule."""
    type_name: str
    to: str | None = None              # the concept referred to, or the choice list
    quantity: dict | None = None        # {money: 1, duration: −1}
    direction: str | None = None
    many: bool = False

    def __hash__(self) -> int:
        return hash((self.type_name, self.to, self.direction, self.many))


@dataclass
class Part:
    """One part of a card or an example: the part keyword, the content on its
    line, and its continuation lines, which are indented further."""
    keyword: str
    content: str
    continuation: list[Line]
    lineno: int

    def text(self) -> str:
        return " ".join([self.content] + [b.content for b in self.continuation]).strip()


@dataclass(eq=False)
class ContentItem:
    name: str
    module: "Module" = field(repr=False)
    lineno: int = 0
    # Bridges on the card (04 §2.1, 05 §2.5): (relation, target address).
    bridges: list[tuple[str, str]] = field(default_factory=list)
    # Card parts as written: (part keyword, content). Empty in the short
    # form (appendix A §2.8).
    card: list[tuple[str, str]] = field(default_factory=list)
    short_form: bool = False

    @property
    def address(self) -> str:
        return f"{self.module.address}/{self.name}"


@dataclass(eq=False)
class Concept(ContentItem):
    parent: str | None = None


@dataclass(eq=False)
class Property(ContentItem):
    value_type: ValueType = None
    personal: bool | None = None


@dataclass(eq=False)
class ChoiceList(ContentItem):
    is_open: bool = False
    code: bool = False      # code list: its choices are codes from an outside standard
    choices: list[str] = field(default_factory=list)


@dataclass(eq=False)
class ChoiceItem(ContentItem):
    """One choice; `choice_list` is written as in the text, and looked up later."""
    choice_list: str = ""


@dataclass(eq=False)
class Rule(ContentItem):
    kind: str = ""                    # computed, helper, constraint, contribution
    concept: str | None = None          # written as in the text
    parameters: tuple[str, ...] = ()
    result: ValueType | None = None
    is_open: bool | None = None
    to: tuple[str, str] | None = None  # contribution: (concept, computed property)
    expression: object = None
    messages: dict[str, str] = field(default_factory=dict)


@dataclass(eq=False)
class Example(ContentItem):
    parts: list[Part] = field(default_factory=list)


@dataclass(eq=False)
class AppliesTo:
    concept: str
    properties: list[tuple[str, bool]]
    module: "Module" = field(repr=False)


@dataclass(eq=False)
class Module:
    address: str
    version: str
    uses: list[tuple[str, str]] = field(default_factory=list)
    content: dict[str, ContentItem] = field(default_factory=dict)
    applies_to: list[AppliesTo] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        return f"{self.address}@{self.version}"

    def add(self, content: ContentItem) -> None:
        if content.name in self.content:  # ADDRESS-3
            raise NotationError(
                f"line {content.lineno}: name {content.name!r} is already used in {self.address}")
        self.content[content.name] = content

    def __repr__(self) -> str:
        return self.full_name


def _split_parts(body: list[Line]) -> list[Part]:
    """A line with the smallest indent starts a new part; a line that is
    indented further continues the previous part (§2.8)."""
    if not body:
        return []
    base = body[0].indent
    result: list[Part] = []
    for b in body:
        if b.indent < base:
            raise NotationError(f"line {b.lineno}: indentation is not aligned")
        if b.indent == base:
            keyword, _, content = b.content.partition(" ")
            result.append(Part(keyword, content.strip(), [], b.lineno))
        else:
            result[-1].continuation.append(b)
    return result


def _parse_quantity(text: str, lineno: int) -> dict[str, int]:
    powers: dict[str, int] = {}
    sign = 1
    for i, piece in enumerate(re.split(r"(/|·)", text.strip())):
        if i % 2:
            sign = -1 if piece == "/" else 1
            continue
        p = 1
        if piece and piece[-1] in "²³":
            p = 2 if piece[-1] == "²" else 3
            piece = piece[:-1]
        if piece not in QUANTITIES:
            raise NotationError(f"line {lineno}: unknown quantity: {piece}")
        powers[piece] = powers.get(piece, 0) + sign * p
    return {k: p for k, p in powers.items() if p}


_VALUE_TYPE_RE = re.compile(
    r"^([a-z_]+)(?: ([A-Za-z0-9_/-]+))?(?: \(([^)]*)\))?((?:, [a-z_]+)*)$")


def _parse_value_type(text: str, lineno: int, intermediate: bool) -> tuple[ValueType, list[str]]:
    """`number (money/duration, level)`, `reference Party, many`, … together
    with the marks after it: `many`, `open`, `closed`."""
    m = _VALUE_TYPE_RE.match(text.strip())
    if not m:
        raise NotationError(f"line {lineno}: value type cannot be read: {text!r}")
    type_name, to, parens, marks = m.groups()
    marks = [t.strip() for t in marks.split(",") if t.strip()]
    if type_name not in VALUE_TYPES and not (intermediate and type_name in INTERMEDIATE_TYPES):
        raise NotationError(f"line {lineno}: unknown value type: {type_name}")
    if (type_name in ("reference", "choice")) != (to is not None):
        raise NotationError(f"line {lineno}: {type_name} {'requires' if to is None else 'takes no'} a name")
    quantity = direction = None
    if parens is not None:
        if type_name != "number":
            raise NotationError(f"line {lineno}: quantity and direction are only for numbers (CONCEPT-5)")
        content = [x.strip() for x in parens.split(",")]
        direction = content[-1]
        if direction not in DIRECTIONS or len(content) > 2:
            raise NotationError(f"line {lineno}: unknown direction: {parens}")
        if len(content) == 2:
            quantity = _parse_quantity(content[0], lineno)
    elif type_name == "number" and not intermediate:
        raise NotationError(f"line {lineno}: a number MUST name a direction (CONCEPT-5)")
    many = "many" in marks
    for t in marks:
        if t not in ("many", "open", "closed"):
            raise NotationError(f"line {lineno}: unknown mark: {t}")
    return ValueType(type_name, to, quantity, direction, many), marks


_MODULE_RE = re.compile(r"^([a-z0-9-]+/[a-z0-9-]+)@(\S+)$")
BRIDGES = ("same_as", "broader", "narrower", "similar")
_CONTENT_ADDRESS = re.compile(r"^[a-z0-9-]+/[a-z0-9-]+/[A-Za-z][A-Za-z0-9_]*$")
_CHOICE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_CODE_RE = re.compile(r"^[A-Za-z0-9]+$")  # code from an outside standard, exactly
_IRI = re.compile(r"^[a-z][a-z0-9+.-]*://\S+$")
_HEADS = {
    "concept": re.compile(r"^concept ([A-Z][A-Za-z0-9]*)$"),
    "property": re.compile(r"^property ([a-z][a-z0-9_]*) : (.+)$"),
    "choice_list": re.compile(r"^choice_list ([A-Z][A-Za-z0-9]*), (open|closed|code)$"),
    "choice": re.compile(r"^choice ([a-z][a-z0-9_]*) to (\S+)$"),
    "applies to": re.compile(r"^applies to (\S+):$"),
    "rule": re.compile(
        r"^(computed|helper|constraint) (?:(\S+)\.)?([a-z][a-z0-9_]*)"
        r"(?:\(([^)]*)\))?(?: : (.+))?$"),
    "contribution": re.compile(r"^contribution (\S+) to (\S+)\.([a-z][a-z0-9_]*)$"),
    "example": re.compile(r"^example (\S+)$"),
}


def _card_parts(card: list[Part]) -> list[tuple[str, str]]:
    """Card parts other than the choice list and the rule expression."""
    return [(b.keyword, b.text()) for b in card if b.keyword not in ("choices:", "rule:")]


def _bridges(card: list[Part]) -> list[tuple[str, str]]:
    """Card parts `same_as ‹address›` and the like (appendix A §2.8). The
    target is the address of Uniti content, or a full IRI for an outside
    standard (RELATION-8)."""
    result = []
    for b in card:
        if b.keyword in BRIDGES:
            destination = b.text()
            if not (_CONTENT_ADDRESS.match(destination) or _IRI.match(destination)):
                raise NotationError(
                    f"line {b.lineno}: a bridge points to a full address or an IRI (RELATION-8)")
            result.append((b.keyword, destination))
    return result


def _name_in_module(writing: str, module: Module, lineno: int) -> str:
    """A name in the heading line may be written with its full address."""
    if "/" not in writing:
        return writing
    address, _, name = writing.rpartition("/")
    if address != module.address:
        raise NotationError(f"line {lineno}: {writing} does not belong to module {module.address}")
    return name


class _Reader:
    def __init__(self) -> None:
        self.modules: list[Module] = []

    def read(self, lines: list[Line]) -> list[Module]:
        k = 0
        while k < len(lines):
            head = lines[k]
            if head.indent != 0:
                raise NotationError(
                    f"line {head.lineno}: every part starts without spaces in front of it (§2.2)")
            k += 1
            body = []
            while k < len(lines) and lines[k].indent > 0:
                body.append(lines[k])
                k += 1
            self._section(head, body)
        return self.modules

    def _section(self, head: Line, body: list[Line]) -> None:
        keyword = head.content.split()[0]
        if head.content.startswith("applies to "):
            keyword = "applies to"
        if keyword == "module":
            m = _MODULE_RE.match(head.content[len("module "):])
            if not m:
                raise NotationError(f"line {head.lineno}: a module is written address@version (NOTATION-16)")
            module = Module(m.group(1), m.group(2))
            for b in body:
                m = _MODULE_RE.match(b.content[len("uses "):]) if b.content.startswith("uses ") else None
                if not m:
                    raise NotationError(
                        f"line {b.lineno}: a module in use is written uses address@version (NOTATION-16)")
                module.uses.append((m.group(1), m.group(2)))
            self.modules.append(module)
            return
        if not self.modules:
            raise NotationError(f"line {head.lineno}: content writing starts with a module (NOTATION-16)")
        module = self.modules[-1]
        content = head.content
        short_form = content.endswith(":") and keyword in ("computed", "helper", "constraint", "contribution")
        if short_form:
            content = content[:-1].rstrip()
        card_kind = {"computed": "rule", "helper": "rule", "constraint": "rule"}.get(keyword, keyword)
        pattern = _HEADS.get(card_kind)
        m = pattern.match(content) if pattern else None
        if not m:
            raise NotationError(f"line {head.lineno}: unknown heading line: {head.content!r}")
        n = head.lineno
        if card_kind == "concept":
            card = _split_parts(body)
            parent = next((b.content for b in card if b.keyword == "parent"), None)
            module.add(Concept(m.group(1), module, n, _bridges(card), parent=parent,
                                card=_card_parts(card)))
        elif card_kind == "property":
            value_type, marks = _parse_value_type(m.group(2), n, intermediate=False)
            if set(marks) - {"many"}:
                raise NotationError(f"line {n}: a property is not open or closed")
            parts = _split_parts(body)
            card = {b.keyword: b.text() for b in parts}
            personal = {"yes": True, "no": False}.get(card.get("personal"))
            module.add(Property(m.group(1), module, n, _bridges(parts), value_type=value_type,
                               personal=personal, card=_card_parts(parts)))
        elif card_kind == "choice_list":
            choice_list = ChoiceList(m.group(1), module, n, is_open=m.group(2) == "open",
                                     code=m.group(2) == "code")
            pattern = _CODE_RE if choice_list.code else _CHOICE_NAME_RE
            choice_list.card = _card_parts(_split_parts(body))
            for b in _split_parts(body):
                if b.keyword == "choices:":
                    for x in b.continuation:
                        if not pattern.match(x.content):
                            raise NotationError(
                                f"line {x.lineno}: {x.content} is not a choice name (ADDRESS-2)")
                        choice_list.choices.append(x.content)
            module.add(choice_list)
            for p in choice_list.choices:
                module.add(ChoiceItem(p, module, n, choice_list=choice_list.name))
        elif card_kind == "choice":
            parts = _split_parts(body)
            module.add(ChoiceItem(m.group(1), module, n, _bridges(parts),
                                    choice_list=m.group(2), card=_card_parts(parts)))
        elif card_kind == "applies to":
            properties = []
            for b in _split_parts(body):
                if b.content not in ("", "required") or b.continuation:
                    raise NotationError(f"line {b.lineno}: write the property name, then required if it is required")
                properties.append((b.keyword, b.content == "required"))
            module.applies_to.append(AppliesTo(m.group(1), properties, module))
        elif card_kind == "rule":
            self._rule(module, m, short_form, body, n)
        elif card_kind == "contribution":
            rule = Rule(_name_in_module(m.group(1), module, n), module, n, kind="contribution",
                        to=(m.group(2), m.group(3)))
            rule.expression, rule.messages = self._expression(short_form, body, n)
            rule.short_form = short_form
            module.add(rule)
        elif card_kind == "example":
            module.add(Example(_name_in_module(m.group(1), module, n), module, n,
                                parts=_split_parts(body)))

    def _rule(self, module: Module, m: re.Match, short_form: bool, body: list[Line], n: int) -> None:
        kind, concept, name, parameters, result = m.groups()
        rule = Rule(name, module, n, kind=kind, concept=concept)
        if parameters is not None:
            rule.parameters = tuple(p.strip() for p in parameters.split(","))
            for p in rule.parameters:
                if not _LOCAL_NAME_RE.match(p) or p in KEYWORDS:  # NOTATION-10
                    raise NotationError(f"line {n}: parameter {p!r} is not valid")
        if kind == "constraint":
            if result is not None or parameters is not None or concept is None:
                raise NotationError(f"line {n}: a constraint is written constraint Concept.name")
        else:
            if result is None:
                raise NotationError(f"line {n}: {kind} MUST name its result type")
            rule.result, marks = _parse_value_type(result, n, intermediate=kind == "helper")
            if kind == "computed":
                if concept is None:
                    raise NotationError(f"line {n}: a computed property applies to one concept (CALC-4)")
                if len(set(marks) & {"open", "closed"}) != 1:
                    raise NotationError(f"line {n}: a computed property is open or closed (CALC-4)")
                rule.is_open = "open" in marks
            elif set(marks) - {"many"}:
                raise NotationError(f"line {n}: a helper is not open or closed")
        rule.expression, rule.messages = self._expression(short_form, body, n)
        rule.short_form = short_form
        if not short_form:
            rule.card = _card_parts(_split_parts(body))
        module.add(rule)

    def _expression(self, short_form: bool, body: list[Line], n: int) -> tuple[object, dict]:
        """Short form: its body is the expression. Full form: card parts, with
        the expression under `rule:` (§2.8)."""
        if short_form:
            if not body:
                raise NotationError(f"line {n}: rule without an expression")
            return parse_expression(body), {}
        expression = None
        messages = {}
        for b in _split_parts(body):
            if b.keyword == "rule:":
                if b.content or not b.continuation:
                    raise NotationError(f"line {b.lineno}: the expression is written under rule:")
                expression = parse_expression(b.continuation)
            elif b.keyword.startswith("message."):
                messages[b.keyword[len("message."):]] = b.text()
        if expression is None:
            raise NotationError(f"line {n}: rule without an expression; write rule: or end "
                                f"the heading line with :")
        return expression, messages


def read(text: str, *, markdown: bool = False) -> list[Module]:
    """Reads writing in the reference notation into modules."""
    if markdown:
        text = from_markdown(text)
    return _Reader().read(split_lines(text))
