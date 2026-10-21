# 0023. A closed relation list

Date: 2026-10-17
Status: accepted

**Context**
Content points to other content: a child to its parent, a property to a
concept, a choice to a list, content to an outside standard. If the kinds of
relation can be made freely, a machine cannot understand content made by
others.

**Decision**
- The relation list is form, and closed. Two groups:
  - **structural**: subtype of, applies to, refers to, uses list, in list;
  - **meaning**: replaced by, and four bridges (same as, broader, narrower,
    similar).
- Every relation applies only to organizations that install the module in
  which it is written.
- No relation changes the content it points to.
- **Inverse of** and **part of** are deliberately not provided yet, and may be
  added later without breaking anything.

**Alternatives**
- *Free relations made by content.* Rejected: equivalent to adding to the form
  through content, so a machine could no longer check them.
- *Providing inverse and part of from the start.* Rejected for now: not yet
  proven necessary, and the form is made as small as possible.

**Consequences**
- "In list", "refers to", and "uses list" appear in this list as a result of
  decisions 0016 and 0017.
