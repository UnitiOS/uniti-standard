# 0015. Dates and instants

Date: 2026-10-17
Status: accepted

**Context**
"Valid since 1 November" and "paid at 09:00 WIB" are two different kinds of
time. If the two are mixed, a fact can be read as valid on a different day by
readers in different time zones.

**Decision**
- A **date** (a calendar day, without a clock time) and an **instant** (an
  exact point in time, always with a time zone) are two different value types.
- The **valid time** may be a date or an instant. A property may set one of
  the two.
- A date that is compared with an instant is read as the **start of the day
  according to the default time zone of the organization** that recorded it.
- The **recorded time** is always an instant.

**Alternatives**
- *All times are instants.* Rejected: "date of birth 12 March" has no clock
  time, and giving it 00:00 in a particular zone makes it shift in another
  zone.
- *All valid times are dates.* Rejected: some events need clock precision, for
  example a payment or an arrival.

**Consequences**
- Every organization must set a default time zone. How to record and change
  it, and organizations with several time zones, are still open.
