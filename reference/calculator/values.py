"""Values in the reference calculator.

Follows form/03-values.md, form/06-calculation-rules.md §2.6 to §2.9, and
appendix/A-notation.md §2.3 and §2.4.

Three kinds of failure are told apart strictly:

- NotComputable: a legitimate computation result under 06 §2.9.
- NotDefined: a situation whose meaning the standard has not defined. The
  calculator stops, and the situation becomes a finding, not a guess.
- NotationError: a rule or example that is written wrongly, for instance
  comparing text with a number.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from fractions import Fraction


# --- Failures ---------------------------------------------------------------

class NotDefined(Exception):
    """A situation whose meaning the standard has not defined."""


class NotationError(Exception):
    """A rule or example that does not follow the form or the notation."""


# 06 §2.9: the list of reason kinds, closed.
REASON_KINDS = frozenset({
    "empty value", "division by zero", "not single", "empty collection",
    "unit mismatch", "needs rounding",
    "direction violated", "cycle", "redacted", "declared by rule",
    "reversed time", "undefined order",
})

# Order of the table in 06 §2.9. When the members that fail have no
# computation order, the kind reported is the topmost one (decision 0054).
REASON_ORDER = (
    "empty value", "division by zero", "not single", "empty collection",
    "unit mismatch", "needs rounding", "direction violated", "cycle",
    "reversed time", "undefined order", "redacted", "declared by rule",
)


class NotComputable(Exception):
    """A result that cannot be computed, with its reason kind.

    Used as an exception so that it spreads by itself (CALC-30). A part of
    an expression that is not computed never raises it.
    """

    def __init__(self, kind: str, detail: str):
        if kind not in REASON_KINDS:  # CALC-28
            raise ValueError(f"unknown reason kind: {kind}")
        super().__init__(f"{kind}: {detail}")
        self.kind = kind
        self.detail = detail
        self.where: list[str] = []  # filled by the evaluator: rule, entity, and T


class _Empty:
    """No value (06 §2.9)."""

    def __repr__(self) -> str:
        return "empty"


EMPTY = _Empty()


# --- Units ------------------------------------------------------------------

# content/code-lists §3: the unit code as written in the reference notation,
# the group whose members can be converted to one another, its size in the
# base unit of that group, and its code in the list `uniti/unit/Unit`.
_FIXED_UNITS: dict[str, tuple[str, Fraction, str]] = {
    "second": ("time", Fraction(1), "s"),
    "minute": ("time", Fraction(60), "min"),
    "hour": ("time", Fraction(3600), "h"),
    "day": ("time", Fraction(86400), "d"),
    "week": ("time", Fraction(604800), "wk"),
    "month": ("calendar", Fraction(1), "month"),
    "year": ("calendar", Fraction(12), "year"),
    "g": ("mass", Fraction(1), "g"),
    "kg": ("mass", Fraction(1000), "kg"),
    "mm": ("length", Fraction(1, 1000), "mm"),
    "cm": ("length", Fraction(1, 100), "cm"),
    "m": ("length", Fraction(1), "m"),
    "km": ("length", Fraction(1000), "km"),
}

_QUANTITY_OF_GROUP = {"time": "duration", "calendar": "duration",
                      "mass": "mass", "length": "length"}

# The plural form of a unit word points to the same code (N3).
_PLURALS = {"seconds": "second", "minutes": "minute", "hours": "hour",
            "days": "day", "weeks": "week", "months": "month", "years": "year"}

CURRENCIES = frozenset({"IDR", "USD"})  # ISO 4217 codes in content/code-lists


def unit_group(code: str) -> tuple[str, Fraction | None]:
    """The group of a unit code, and its size in the base unit.

    Each currency forms a group of its own with no fixed size, because the
    exchange rate is recorded as a fact (CALC-25).
    """
    if code in _FIXED_UNITS:
        return _FIXED_UNITS[code][:2]
    if code in CURRENCIES:
        return ("money:" + code, None)
    raise NotationError(f"unknown unit: {code}")


def list_code(code: str) -> str:
    """The code of a unit in the code list: `day` is written for UCUM `d`."""
    unit_group(code)
    return _FIXED_UNITS[code][2] if code in _FIXED_UNITS else code


def unit_table() -> dict[str, tuple[str, str]]:
    """List code → (how it is written, quantity), to compare with
    content/code-lists."""
    table = {k: (k, "money") for k in CURRENCIES}
    for spelling, (group, _, code) in _FIXED_UNITS.items():
        table[code] = (spelling, _QUANTITY_OF_GROUP[group])
    return table


_SUPERSCRIPT_WRITE = {2: "²", 3: "³"}
_SUPERSCRIPT_READ = {"²": 2, "³": 3}


@dataclass(frozen=True)
class Unit:
    """The unit of a number: codes with their powers, ordered by code."""

    parts: tuple[tuple[str, int], ...] = ()

    @staticmethod
    def from_map(powers: dict[str, int]) -> Unit:
        return Unit(tuple(sorted((k, p) for k, p in powers.items() if p)))

    @property
    def dimensionless(self) -> bool:
        return not self.parts

    def multiply(self, other: Unit, sign: int = 1) -> Unit:
        powers = dict(self.parts)
        for code, p in other.parts:
            powers[code] = powers.get(code, 0) + sign * p
        return Unit.from_map(powers)

    def divide(self, other: Unit) -> Unit:
        return self.multiply(other, -1)

    def power(self, n: int) -> Unit:
        return Unit.from_map({k: p * n for k, p in self.parts})

    def __str__(self) -> str:
        def render(code: str, p: int) -> str:
            if p == 1:
                return code
            if p in _SUPERSCRIPT_WRITE:
                return code + _SUPERSCRIPT_WRITE[p]
            raise NotDefined(f"unit power {p} has no way of being written yet")
        top = [render(k, p) for k, p in self.parts if p > 0]
        bottom = [render(k, -p) for k, p in self.parts if p < 0]
        text = "·".join(top) if top else "1"
        for b in bottom:
            text += "/" + b
        return text if self.parts else ""


DIMENSIONLESS = Unit()

QUANTITIES = frozenset({"money", "duration", "mass", "length"})


def quantity_of(s: Unit) -> dict[str, int] | None:
    """The quantity of a unit: {money: 1, duration: −1} for IDR/day.

    Different codes do not cancel each other, even when their quantity is
    the same: IDR·hour/day has no quantity, because hour and day can only
    cancel through a conversion (06 §2.8, decision 0054). The result is
    None."""
    powers: dict[str, int] = {}
    sign: dict[str, set[int]] = {}
    for code, p in s.parts:
        group = unit_group(code)[0]
        name = "money" if group.startswith("money:") else _QUANTITY_OF_GROUP[group]
        powers[name] = powers.get(name, 0) + p
        sign.setdefault(name, set()).add(1 if p > 0 else -1)
    if any(len(t) > 1 for t in sign.values()):
        return None
    return {k: p for k, p in powers.items() if p}


def parse_unit(text: str) -> Unit:
    """Reads a unit according to appendix A §2.4: `IDR/day`, `cm³/kg`.

    Read from the left: `a/b·c` is (a/b)·c.
    """
    powers: dict[str, int] = {}
    sign = 1
    for i, part in enumerate(re.split(r"(/|·)", text.strip())):
        if i % 2 == 1:
            sign = -1 if part == "/" else 1
            continue
        p = 1
        if part and part[-1] in _SUPERSCRIPT_READ:
            p = _SUPERSCRIPT_READ[part[-1]]
            part = part[:-1]
        part = _PLURALS.get(part, part)
        unit_group(part)
        powers[part] = powers.get(part, 0) + sign * p
    return Unit.from_map(powers)


# --- Numbers ----------------------------------------------------------------

@dataclass(frozen=True)
class Number:
    """An exact number, which may carry a unit (03 §2.2, 06 §2.8)."""

    value: Fraction
    unit: Unit = DIMENSIONLESS

    def __post_init__(self) -> None:
        if not isinstance(self.value, Fraction):
            object.__setattr__(self, "value", Fraction(self.value))

    def __str__(self) -> str:
        text = format_numeral(self.value)
        return f"{text} {self.unit}" if not self.unit.dimensionless else text


def terminates(x: Fraction) -> bool:
    """Whether x can be written as a terminating decimal (CALC-21)."""
    d = x.denominator
    for f in (2, 5):
        while d % f == 0:
            d //= f
    return d == 1


def format_numeral(x: Fraction) -> str:
    """A numeral with a thousands comma and a decimal point. A fraction
    that does not terminate is written a/b."""
    if not terminates(x):
        return f"{x.numerator}/{x.denominator}"
    sign = "−" if x < 0 else ""
    x = abs(x)
    whole, remaining = divmod(x.numerator, x.denominator)
    thousands = f"{whole:,}"
    decimals = ""
    while remaining:
        remaining *= 10
        d, remaining = divmod(remaining, x.denominator)
        decimals += str(d)
    return sign + thousands + ("." + decimals if decimals else "")


_NUMBER_RE = re.compile(r"^(−)?(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(%)?$")


def parse_numeral(text: str) -> Fraction:
    """Reads a numeral according to appendix A §2.3: `1,234.5`, `5%`, `−3`."""
    m = _NUMBER_RE.match(text.strip())
    if not m:
        raise NotationError(f"not a number according to the notation: {text!r}")
    negative, whole, decimals, percent = m.groups()
    x = Fraction(int(whole.replace(",", "")))
    if decimals:
        x += Fraction(int(decimals), 10 ** len(decimals))
    if percent:
        x /= 100
    return -x if negative else x


def parse_number(text: str) -> Number:
    """Reads a number with a unit: `150,000 IDR`, `50,000 IDR/day`, `0.8`."""
    part = text.strip().split(maxsplit=1)
    value = parse_numeral(part[0])
    if len(part) == 1:
        return Number(value)
    if part[0].endswith("%"):
        raise NotationError(f"a percent has no unit: {text!r}")
    return Number(value, parse_unit(part[1]))


# --- Time -------------------------------------------------------------------

Date = dt.date
Instant = dt.datetime

_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "october": 10,
    "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}

MONTH_NAMES = frozenset(_MONTHS)

# Appendix A §2.4 [provisional]
_NAMED_ZONES = {"WIB": 7 * 60, "WITA": 8 * 60, "WIT": 9 * 60, "UTC": 0}
_ZONE_OFFSET_RE = re.compile(r"^UTC([+−])(\d{1,2})(?::(\d{2}))?$")


def parse_zone(text: str) -> dt.timezone:
    """Reads a time zone: `WIB`, `UTC`, `UTC+7`, `UTC+5:30`, `UTC−3`."""
    if text in _NAMED_ZONES:
        minutes = _NAMED_ZONES[text]
    else:
        m = _ZONE_OFFSET_RE.match(text)
        if not m:
            raise NotationError(f"unknown time zone: {text}")
        minutes = int(m.group(2)) * 60 + int(m.group(3) or 0)
        if m.group(1) == "−":
            minutes = -minutes
    return dt.timezone(dt.timedelta(minutes=minutes), text)


UTC = parse_zone("UTC")

_TIME_RE = re.compile(
    r"^(\d{1,2}) ([A-Za-z]+) (\d{4})"
    r"(?: (\d{2}):(\d{2})(?::(\d{2}))?(?: (\S+))?)?$")


def parse_time(text: str, default_zone: dt.timezone | None = None) -> Date | Instant:
    """Reads a date or an instant: `6 Oct 2026`, `6 Oct 2026 09:00 WIB`.

    An instant without a zone is allowed only inside an example, and is read
    in the default time zone of that example (NOTATION-7).
    """
    m = _TIME_RE.match(text.strip())
    if not m or m.group(2).lower() not in _MONTHS:
        raise NotationError(f"not a date or an instant: {text!r}")
    day, month, year, hour, minutes, seconds, zone_name = m.groups()
    date = dt.date(int(year), _MONTHS[month.lower()], int(day))
    if hour is None:
        return date
    if zone_name:
        tz = parse_zone(zone_name)
    elif default_zone is not None:
        tz = default_zone
    else:
        raise NotationError(f"instant without a time zone: {text!r}")
    return dt.datetime.combine(
        date, dt.time(int(hour), int(minutes), int(seconds or 0)), tz)


def is_time(x: object) -> bool:
    return isinstance(x, dt.date)


def to_instant(t: Date | Instant, default_zone: dt.timezone) -> Instant:
    """A date is read as the start of the day in the default time zone (VALUE-10)."""
    if isinstance(t, dt.datetime):
        return t
    return dt.datetime.combine(t, dt.time(0), default_zone)


@dataclass(frozen=True)
class Range:
    """From `start` up to but not including `end` (CALC-26)."""

    start: Date | Instant
    end: Date | Instant


# --- Other values -----------------------------------------------------------

@dataclass(frozen=True)
class Text:
    content: str
    language: str | None = None


@dataclass(frozen=True)
class Choice:
    """One choice of a choice list, pointed to by its address."""

    address: str


@dataclass(frozen=True)
class Entity:
    """An entity. It is referred to by its identifier; the local id is only
    for humans to read in an example."""

    identifier: str
    name: str | None = None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entity) and other.identifier == self.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __repr__(self) -> str:
        return self.name or self.identifier


class Record:
    """An intermediate value holding named parts (06 §2.6)."""

    __slots__ = ("_parts",)

    def __init__(self, parts: dict[str, object]):
        self._parts = dict(parts)

    def get(self, name: str) -> object:
        if name not in self._parts:
            raise NotationError(f"the record has no part {name!r}")
        return self._parts[name]

    def part_names(self) -> frozenset[str]:
        return frozenset(self._parts)

    def with_part(self, name: str, value: object) -> Record:
        self.get(name)
        new = dict(self._parts)
        new[name] = value
        return Record(new)

    def __repr__(self) -> str:
        content = ", ".join(f"{k}: {v}" for k, v in self._parts.items())
        return "{" + content + "}"


@dataclass(frozen=True)
class Collection:
    """An intermediate value holding members (06 §2.6). A collection from
    `all` and `group` is unordered."""

    members: tuple
    ordered: bool

    def __len__(self) -> int:
        return len(self.members)
