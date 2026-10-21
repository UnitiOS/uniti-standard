# 0040. Conformance tests for implementations

Date: 2026-10-19
Status: accepted

**Context**
Any software may implement the standard (principle P11). There must be one
way, the same for everyone, to prove that an implementation really follows
it.

**Decision**
- The standard contains **conformance tests**: a set of examples owned by the
  standard, in the same form as the examples in a module, with addresses
  under the owner `standard`.
- The conformance tests are grouped by part of the form and by level of the
  calculation operations.
- An implementation states the level it supports, and may claim to conform
  to the standard only if it passes the tests for that level and all the
  groups outside calculation. The claim always names the version of the
  standard and the level.
- An implementation refuses to install a module that contains a rule above
  its level.

**Alternatives**
- *Conformance declared by oneself without tests.* Rejected: it cannot be
  checked.
- *One test for all levels.* Rejected, in line with decision 0026.

**Consequences**
- The reference calculator becomes the first implementation that must pass
  these tests.
- Who may use the Uniti name in a conformance claim is discussed in study B7.
