# 0011. Addresses without versions; the identifier of an entity is random

Date: 2026-10-17
Status: accepted

**Context**
Facts are stored for years, while content keeps changing versions and codes
made by humans can change.

**Decision**
- **A content address does not contain a version.** A concept and a property
  with an address are the same in all versions of their module. The version
  used is recorded in every fact (version used). When the meaning changes
  fundamentally, a new address is made.
- **The identifier of an entity is random**, unique across the world,
  permanent, and without meaning. Codes that are meaningful to humans (customer
  number, item code, registration number) are recorded as properties.
- The same entity in two organizations has two identifiers, which can be
  connected with a "same as" fact. Its form is not yet determined.

**Alternatives**
- *The version inside the address.* Rejected: every new version would cut the
  old facts off from their content.
- *A meaningful code as the identifier.* Rejected: codes change, get
  mistyped, or get reused, while an identifier must not.

**Consequences**
- Changing a name for humans is done through a label, not through the address.
