# 0037. Required examples, and the freezing gate

Date: 2026-10-19
Status: accepted

**Context**
If examples are only recommended, P9 becomes a slogan. The most dangerous
rules are exactly those whose makers feel they need no proof.

**Decision**
- Every computed property must have at least one compute example.
- Every contribution must have at least one compute example that shows it.
- Every constraint must have at least one accept example and one reject
  example.
- In the vocabulary, the examples must come from at least two domains.
- A version cannot be frozen unless all its examples are proven.
- The expected result should be calculated without running that rule.

**Alternatives**
- *Examples only recommended.* Rejected, for the reason above.
- *Examples also required for every helper.* Rejected: a helper is already
  tested through the calculations that use it.

**Consequences**
- Examples prove that a rule produces what its maker states, not that the
  statement is correct under accounting or law.
