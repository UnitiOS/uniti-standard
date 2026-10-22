"""Operations on values, according to form/06-calculation-rules.md §2.5 to §2.9.

Only the part of the operations that does not read facts is here. The
operations that read facts or use a binder (`all`, `at`, `history`,
`before_action`, `each`, `fold`, …) are run by the evaluator, which uses the
functions here for their computing part.

A function that compares a date with an instant takes `default_zone`, because
a date is read as the start of the day in that zone (VALUE-10).
"""

from __future__ import annotations

import calendar
import datetime as dt
import functools
import math
from fractions import Fraction
from typing import Callable, Sequence

from .values import (
    EMPTY, Number, NotDefined, Entity, NotationError, Collection,
    Choice, Record, Range, Unit, Text, NotComputable,
    is_time, unit_group, to_instant, list_code,
)

TimeZone = dt.timezone


# --- Shared checks ----------------------------------------------------------

def _type_name(x: object) -> str:
    if isinstance(x, bool):
        return "yes_no"
    if isinstance(x, dt.datetime):
        return "instant"
    if isinstance(x, dt.date):
        return "date"
    return {Number: "number", Text: "text", Choice: "choice", Entity: "entity",
            Record: "record", Collection: "collection",
            Range: "range"}.get(type(x), type(x).__name__)


def require_value(x: object, what: str) -> object:
    """An empty value that is used in a computation becomes not computable
    (06 §2.9)."""
    if x is EMPTY:
        raise NotComputable("empty value", f"empty value used for {what}")
    return x


def _as_number(x: object, what: str) -> Number:
    x = require_value(x, what)
    if not isinstance(x, Number):
        raise NotationError(f"{what} requires a number, not {_type_name(x)}")
    return x


def as_yes_no(x: object, what: str) -> bool:
    x = require_value(x, what)
    if not isinstance(x, bool):
        raise NotationError(f"{what} requires yes/no, not {_type_name(x)}")
    return x


def _as_collection(x: object, what: str) -> Collection:
    x = require_value(x, what)
    if not isinstance(x, Collection):
        raise NotationError(f"{what} requires a collection, not {_type_name(x)}")
    return x


def _unify(a: Number, b: Number, what: str) -> tuple[Number, Number]:
    """Both sides MUST have the same unit (CALC-24). A zero without a unit
    takes the unit of the other side (06 §2.8)."""
    if a.unit == b.unit:
        return a, b
    if a.unit.dimensionless and a.value == 0:
        return Number(0, b.unit), b
    if b.unit.dimensionless and b.value == 0:
        return a, Number(0, a.unit)
    raise NotComputable("unit mismatch", f"{what}: {a} and {b}")


def _uniform(a, b, default_zone: TimeZone):
    """A date and an instant that are compared: the date is read as an instant."""
    if isinstance(a, dt.datetime) != isinstance(b, dt.datetime):
        return to_instant(a, default_zone), to_instant(b, default_zone)
    return a, b


def _order(a: object, b: object, default_zone: TimeZone) -> int:
    a = require_value(a, "comparison")
    b = require_value(b, "comparison")
    if isinstance(a, Number) and isinstance(b, Number):
        a, b = _unify(a, b, "comparison")
        a, b = a.value, b.value
    elif is_time(a) and is_time(b):
        a, b = _uniform(a, b, default_zone)
    else:
        raise NotationError(
            f"{_type_name(a)} and {_type_name(b)} cannot be ordered")
    return (a > b) - (a < b)


# --- Compute ----------------------------------------------------------------

def add(a: object, b: object, default_zone: TimeZone) -> object:
    a = require_value(a, "+")
    if is_time(a):
        return shift(a, _as_number(b, "+"), 1)
    a, b = _unify(_as_number(a, "+"), _as_number(b, "+"), "+")
    return Number(a.value + b.value, a.unit)


def subtract(a: object, b: object, default_zone: TimeZone) -> object:
    a = require_value(a, "−")
    if is_time(a):
        if is_time(require_value(b, "−")):
            raise NotationError(
                "the distance between two times is written difference(a, b, unit)")
        return shift(a, _as_number(b, "−"), -1)
    a, b = _unify(_as_number(a, "−"), _as_number(b, "−"), "−")
    return Number(a.value - b.value, a.unit)


def negate(a: object) -> Number:
    a = _as_number(a, "−")
    return Number(-a.value, a.unit)


def multiply(a: object, b: object) -> Number:
    a, b = _as_number(a, "×"), _as_number(b, "×")
    return Number(a.value * b.value, a.unit.multiply(b.unit))


def divide(a: object, b: object) -> Number:
    a, b = _as_number(a, "÷"), _as_number(b, "÷")
    if b.value == 0:
        raise NotComputable("division by zero", f"{a} ÷ {b}")
    return Number(a.value / b.value, a.unit.divide(b.unit))


def power(a: object, n: object) -> Number:
    """`n` is a whole number without a unit (06 §2.5). A fractional power is
    not part of the core (decision 0045)."""
    a, n = _as_number(a, "power"), _as_number(n, "power")
    if not n.unit.dimensionless or n.value.denominator != 1:
        raise NotationError(f"power is only for whole numbers without a unit, not {n}")
    e = int(n.value)
    if a.value == 0 and e < 0:
        raise NotComputable("division by zero", f"power({a}, {n})")
    return Number(a.value ** e, a.unit.power(e))


def floor_multiple(n: object, to: object) -> Number:
    """The largest multiple of `to` that is not more than `n` (CALC-56). Every
    way of rounding in the calculation library is written from this
    operation."""
    n, to = _unify(_as_number(n, "floor_multiple"), _as_number(to, "floor_multiple"),
                   "floor_multiple")
    if to.value <= 0:
        raise NotationError(f"the multiple must be more than zero: {to}")
    return Number(math.floor(n.value / to.value) * to.value, to.unit)


# --- Compare ----------------------------------------------------------------

def equals(a: object, b: object, default_zone: TimeZone) -> bool:
    """`=` for every value type, including records and collections (06 §2.5).

    If one of the collections is unordered, the two are equal when their
    members are equal, ignoring order, with the same number of occurrences
    (06 §2.5).
    """
    a = require_value(a, "comparison")
    b = require_value(b, "comparison")
    if isinstance(a, Number) and isinstance(b, Number):
        a, b = _unify(a, b, "=")
        return a.value == b.value
    if is_time(a) and is_time(b):
        a, b = _uniform(a, b, default_zone)
        return a == b
    if isinstance(a, Record) and isinstance(b, Record):
        return (a.part_names() == b.part_names()
                and all(equals(a.get(n), b.get(n), default_zone)
                        for n in sorted(a.part_names())))
    if isinstance(a, Collection) and isinstance(b, Collection):
        if len(a) != len(b):
            return False
        if a.ordered and b.ordered:
            return all(equals(x, y, default_zone) for x, y in zip(a.members, b.members))
        remaining = list(b.members)
        for x in a.members:
            i = next((i for i, y in enumerate(remaining) if equals(x, y, default_zone)), None)
            if i is None:
                return False
            del remaining[i]
        return True
    if isinstance(a, Range) and isinstance(b, Range):
        return (equals(a.start, b.start, default_zone)
                and equals(a.end, b.end, default_zone))
    if type(a) is type(b) and isinstance(a, (bool, Text, Choice, Entity)):
        return a == b
    raise NotationError(f"comparing {_type_name(a)} with {_type_name(b)}")


def compare(op: str, a: object, b: object, default_zone: TimeZone) -> bool:
    if op == "=":
        return equals(a, b, default_zone)
    if op == "≠":
        return not equals(a, b, default_zone)
    c = _order(a, b, default_zone)
    return {"<": c < 0, "≤": c <= 0, ">": c > 0, "≥": c >= 0}[op]


def within(x: object, y: object, default_zone: TimeZone) -> bool:
    """`t in r` for a range, `x in k` for a collection."""
    y = require_value(y, "in")
    if isinstance(y, Range):
        t = require_value(x, "in")
        if not is_time(t):
            raise NotationError(f"{_type_name(t)} in a range")
        start, t2 = _uniform(y.start, t, default_zone)
        end, t3 = _uniform(y.end, t, default_zone)
        return start <= t2 and t3 < end
    if isinstance(y, Collection):
        return any(equals(x, m, default_zone) for m in y.members)
    raise NotationError(f"in requires a range or a collection, not {_type_name(y)}")


def negate_bool(x: object) -> bool:
    return not as_yes_no(x, "not")


def exists(x: object) -> bool:
    return x is not EMPTY


# --- Collect and summarize --------------------------------------------------

def single(k: object) -> object:
    k = _as_collection(k, "single")
    if len(k) != 1:
        raise NotComputable("not single", f"the collection holds {len(k)} members")
    return k.members[0]


def count(k: object) -> Number:
    return Number(len(_as_collection(k, "count")))


def sum_values(values: Sequence[object]) -> Number:
    """Empty collection: 0 (06 §2.5)."""
    total = Number(0)
    for x in values:
        total, x = _unify(total, _as_number(x, "sum"), "sum")
        total = Number(total.value + x.value, total.unit)
    return total


def _require_nonempty(values: Sequence[object], what: str) -> None:
    if not values:
        raise NotComputable("empty collection", f"{what} over an empty collection")


def _pick(values: Sequence[object], what: str, sign: int, default_zone: TimeZone) -> object:
    """A zero without a unit takes the unit of the other number used with it
    (06 §2.8), also when that zero is the one chosen: max(0, −2 hours) = 0
    hours."""
    _require_nonempty(values, what)
    result = require_value(values[0], what)
    for x in values[1:]:
        x = require_value(x, what)
        if isinstance(x, Number) and isinstance(result, Number):
            x, result = _unify(x, result, what)
        if _order(x, result, default_zone) * sign > 0:
            result = x
    return result


def smallest(values: Sequence[object], default_zone: TimeZone) -> object:
    return _pick(values, "min", -1, default_zone)


def largest(values: Sequence[object], default_zone: TimeZone) -> object:
    return _pick(values, "max", 1, default_zone)


def all_match(values: Sequence[object]) -> bool:
    """Empty collection: yes."""
    return all([as_yes_no(x, "all_match") for x in values])


def any_match(values: Sequence[object]) -> bool:
    """Empty collection: no."""
    return any([as_yes_no(x, "any_match") for x in values])


def group_by(pairs: Sequence[tuple[object, object]], ordered: bool,
             default_zone: TimeZone) -> Collection:
    """A collection of groups `{key, members}`, unordered (06 §2.5).

    The members of each group follow the order of the collection they came
    from.
    """
    group: list[tuple[object, list[object]]] = []
    for members, key in pairs:
        for k, group_members in group:
            if equals(k, key, default_zone):
                group_members.append(members)
                break
        else:
            require_value(key, "group")
            group.append((key, [members]))
    return Collection(tuple(
        Record({"key": k, "members": Collection(tuple(a), ordered)})
        for k, a in group), False)


def merge(parts: Sequence[object], ordered: bool) -> Collection:
    members: list[object] = []
    for k in parts:
        members.extend(_as_collection(k, "each_merged").members)
    return Collection(tuple(members), ordered)


def identical(a: object, b: object) -> bool:
    """Two values that no operation can tell apart: the same type, unit,
    zone, and collection order. Stricter than `=`, which equates 0 with 0 IDR
    and unordered collections regardless of order."""
    if type(a) is not type(b):
        return False
    if isinstance(a, Record):
        return (a.part_names() == b.part_names()
                and all(identical(a.get(n), b.get(n)) for n in a.part_names()))
    if isinstance(a, Collection):
        return (a.ordered == b.ordered and len(a) == len(b)
                and all(identical(x, y) for x, y in zip(a.members, b.members)))
    if isinstance(a, Range):
        return identical(a.start, b.start) and identical(a.end, b.end)
    if isinstance(a, dt.datetime):
        return a == b and a.utcoffset() == b.utcoffset()
    return a == b


def sort_by_key(pairs: Sequence[tuple[object, object]], ordered: bool,
                tie_key: Callable[[object], tuple | None],
                default_zone: TimeZone) -> list[object]:
    """The order for `fold`: by key, then by tie-breaker (06 §2.6, CALC-18).

    `tie_key` gives the tie-breaker key of an entity, or None for a member that
    is not an entity. A key that is an entity is ordered by its tie-breaker.
    A tied member that is not an entity can only be broken if the collection
    is ordered, that is by its original order, or if the two are identical;
    otherwise the order is undefined (06 §2.6, CALC-18).
    """
    indexed = list(enumerate(pairs))

    def key_cmp(a, b) -> int:
        if isinstance(a, Entity) and isinstance(b, Entity):
            sa, sb = tie_key(a), tie_key(b)
            return (sa > sb) - (sa < sb)
        return _order(a, b, default_zone)

    def compare_entries(p, q) -> int:
        c = key_cmp(p[1][1], q[1][1])
        if c:
            return c
        sp, sq = tie_key(p[1][0]), tie_key(q[1][0])
        if sp is not None and sq is not None:
            return (sp > sq) - (sp < sq)
        if ordered:
            return p[0] - q[0]
        if identical(p[1][0], q[1][0]):
            return 0
        raise NotComputable(
            "undefined order",
            f"{p[1][0]} and {q[1][0]} tie, are not entities, in an unordered collection")

    return [p[1][0] for p in sorted(indexed, key=functools.cmp_to_key(compare_entries))]


# --- Time -------------------------------------------------------------------

def add_months(t: dt.date, n: int) -> dt.date:
    """The same date n months later; if it does not exist, the last day of
    that month (06 §2.7)."""
    year, month = divmod(t.month - 1 + n, 12)
    year += t.year
    month += 1
    return dt.date(year, month, min(t.day, calendar.monthrange(year, month)[1]))


def _time_code(s: Unit, what: str) -> tuple[str, Fraction]:
    if len(s.parts) != 1 or s.parts[0][1] != 1:
        raise NotComputable("unit mismatch", f"{what} with unit {s}")
    group, factor = unit_group(s.parts[0][0])
    if group not in ("time", "calendar"):
        raise NotComputable("unit mismatch", f"{what} with unit {s}")
    return group, factor


def shift(t: dt.date, length: Number, sign: int) -> dt.date:
    """A date or an instant shifted by `length` (06 §2.5 and §2.7).

    Month and year are only for dates, and a date is only shifted by whole
    days, weeks, months, or years (CALC-53).
    """
    group, factor = _time_code(length.unit, "shifting a time")
    amount = length.value * factor * sign
    if group == "calendar":
        if isinstance(t, dt.datetime):
            raise NotComputable("unit mismatch", f"instant {t} shifted by {length}")
        if amount.denominator != 1:
            raise NotComputable("unit mismatch", f"date shifted by {length}, not a whole month")
        return add_months(t, int(amount))
    if isinstance(t, dt.datetime):
        micros = amount * 10 ** 6
        if micros.denominator != 1:
            raise NotImplementedError("calculator limit: finer than a microsecond")
        return t + dt.timedelta(microseconds=int(micros))
    days = amount / 86400
    if days.denominator != 1:
        raise NotComputable("unit mismatch", f"date shifted by {length}, not a whole day")
    return t + dt.timedelta(days=int(days))


def _whole_months(a: dt.date, b: dt.date) -> int:
    if b < a:
        return -_whole_months(b, a)
    n = (b.year - a.year) * 12 + b.month - a.month
    while add_months(a, n) > b:
        n -= 1
    return n


def difference(a: object, b: object, s: Unit, default_zone: TimeZone) -> Number:
    """The length from a to b. Days, hours, minutes, and seconds are computed
    exactly; months and years are computed from whole calendar months
    (06 §2.7), only between two dates (CALC-53)."""
    a, b = require_value(a, "difference"), require_value(b, "difference")
    if not (is_time(a) and is_time(b)):
        raise NotationError(f"difference between {_type_name(a)} and {_type_name(b)}")
    group, factor = _time_code(s, "difference")
    a, b = _uniform(a, b, default_zone)
    if group == "calendar":
        if isinstance(a, dt.datetime):
            raise NotComputable("unit mismatch", f"difference of two instants in {s}")
        return Number(int(Fraction(_whole_months(a, b)) / factor), s)
    delta = b - a
    seconds = (Fraction(delta.days * 86400 + delta.seconds)
               + Fraction(delta.microseconds, 10 ** 6))
    return Number(seconds / factor, s)


def make_range(a: object, b: object, default_zone: TimeZone) -> Range:
    a, b = require_value(a, "range"), require_value(b, "range")
    if not (is_time(a) and is_time(b)):
        raise NotationError(f"range from {_type_name(a)} to {_type_name(b)}")
    a, b = _uniform(a, b, default_zone)
    if b < a:  # 06 §2.5
        raise NotComputable("reversed time", f"range from {a} up to but not including {b}")
    return Range(a, b)


def _as_range(r: object, what: str) -> Range:
    r = require_value(r, what)
    if not isinstance(r, Range):
        raise NotationError(f"{what} requires a range, not {_type_name(r)}")
    return r


def span(r: object, s: Unit, default_zone: TimeZone) -> Number:
    r = _as_range(r, "span")
    return difference(r.start, r.end, s, default_zone)


def overlap(r1: object, r2: object, default_zone: TimeZone) -> object:
    """The part two ranges share; empty if they do not overlap."""
    r1, r2 = _as_range(r1, "overlap"), _as_range(r2, "overlap")
    points = [r1.start, r1.end, r2.start, r2.end]
    if any(isinstance(t, dt.datetime) for t in points):
        points = [to_instant(t, default_zone) for t in points]
    start, end = max(points[0], points[2]), min(points[1], points[3])
    return Range(start, end) if start < end else EMPTY


def split(r: object, step: object, default_zone: TimeZone) -> Collection:
    """A range cut into consecutive ranges each as long as `step`. The last
    slice stops at the end of the range.

    Slice k is computed from the start of the range, not from the previous
    slice, so that month-end drift does not accumulate.
    """
    r = _as_range(r, "split")
    step = _as_number(step, "split")
    if step.value <= 0:
        raise NotationError(f"the split step must be more than zero: {step}")

    def point_at(k: int):
        return shift(r.start, Number(step.value * k, step.unit), 1)

    slices = []
    k = 0
    while (start := point_at(k)) < r.end:
        slices.append(Range(start, min(point_at(k + 1), r.end)))
        k += 1
    return Collection(tuple(slices), True)


# --- Units ------------------------------------------------------------------

def _split_money(s: Unit) -> tuple[dict[str, int], dict[str, int]]:
    money, other = {}, {}
    for code, p in s.parts:
        (money if unit_group(code)[0].startswith("money:") else other)[code] = p
    return money, other


def _dimensions_and_factor(parts: dict[str, int]) -> tuple[dict[str, int], Fraction]:
    dimension: dict[str, int] = {}
    factor = Fraction(1)
    for code, p in parts.items():
        group, f = unit_group(code)
        dimension[group] = dimension.get(group, 0) + p
        factor *= f ** p
    return {k: p for k, p in dimension.items() if p}, factor


def convert(n: object, to: Unit) -> Number:
    """Converts to a unit with a fixed factor (06 §2.5). Currencies are not
    converted in the core, because the rate is a fact (decision 0045): the
    calculation library provides `convert_money`."""
    n = _as_number(n, "convert")
    if n.unit == to:
        return n
    from_money, from_other = _split_money(n.unit)
    to_money, to_other = _split_money(to)
    from_dimension, from_factor = _dimensions_and_factor(from_other)
    to_dimension, to_factor = _dimensions_and_factor(to_other)
    if from_dimension != to_dimension or from_money != to_money:
        raise NotComputable("unit mismatch", f"{n} cannot be converted to {to}")
    return Number(n.value * from_factor / to_factor, to)


# A choice of the unit code list `uniti/unit/Unit` (06 §2.5;
# content/code-lists §3).
UNIT_MODULE = "uniti/unit"


def unit_as_choice(s: Unit) -> Choice:
    if len(s.parts) != 1 or s.parts[0][1] != 1:
        raise NotationError(f"{s} is not one unit code of the list (03 §2.3)")
    return Choice(f"{UNIT_MODULE}/{list_code(s.parts[0][0])}")


def unit_of(n: object) -> Choice:
    """`unit_of(n)`: the unit of a number, as a choice."""
    n = _as_number(n, "unit_of")
    if n.unit.dimensionless:  # 0057 T4 (A24), VALUE-5: no unit by definition
        return EMPTY
    if len(n.unit.parts) != 1 or n.unit.parts[0][1] != 1:  # 0057 T3 (A23), 06 §2.5
        raise NotComputable("unit mismatch", f"unit_of({n}): the unit is not one code")
    return unit_as_choice(n.unit)


# --- Intermediate values ----------------------------------------------------

def append_item(k: object, x: object) -> Collection:
    k = _as_collection(k, "append")
    if not k.ordered:
        raise NotationError("append requires an ordered collection")
    return Collection(k.members + (x,), True)


def with_part(r: object, name: str, value: object) -> Record:
    r = require_value(r, "with")
    if not isinstance(r, Record):
        raise NotationError(f"with requires a record, not {_type_name(r)}")
    return r.with_part(name, value)


def get_part(x: object, name: str) -> object:
    """`r.a` for a record and `r.start`, `r.end` for a range. Reading a part
    of an empty value gives empty, like an empty reference."""
    if x is EMPTY:
        return EMPTY
    if isinstance(x, Record):
        return x.get(name)
    if isinstance(x, Range) and name in ("start", "end"):
        return getattr(x, {"start": "start", "end": "end"}[name])
    raise NotationError(f"{_type_name(x)} has no part {name!r}")
