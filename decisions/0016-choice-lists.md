# 0016. Open or closed choice lists

Date: 2026-10-17
Status: accepted

**Context**
A choice list such as "payment method" is made by one owner, but other
organizations often need choices that do not exist yet, for example QR payment or
national insurance.

**Decision**
- A choice list has **its own address**, so that one list can be used by many
  properties.
- The owner declares the list **open** or **closed**.
- To an open list, anyone may add choices **in their own module**. The address
  of such a choice contains the one who added it, so they do not collide.
  Added choices apply only to organizations that install their module.
- A closed list may be opened later; an open list must not be closed.
- Established code lists (currencies, countries, languages) are always closed.

**Alternatives**
- *All lists closed.* Rejected: every new need would have to wait for the
  owner of the list, or force people to make copy lists.
- *All lists open.* Rejected: lists such as currencies must not be added to
  carelessly.

**Consequences**
- `02-addresses.md` adds choice lists as content that is given an address.
- The "in list" relation is added to the relation list (decision 0023).
