# 0017. Standalone properties, which may be added to concepts owned by others

Date: 2026-10-17
Status: accepted

**Context**
Content from different authors must be able to be combined. If every property
belongs to one concept, "name" in ten concepts becomes ten different
properties. If concepts owned by others cannot be extended, every small need
forces people to copy or make a new concept.

**Decision**
- A property has **its own address** and may be used by many concepts.
- A property **applies to** a concept through a statement, which anyone may
  write in their own module, and which applies only to organizations that
  install that module.
- That statement says whether the property is **required**. Only the owner of
  a concept may make a property required for its concept.

**Alternatives**
- *A property belongs to a concept, like a table column.* Rejected: the same
  meaning is scattered over many addresses, and content is hard to combine.
- *No adding to concepts owned by others.* Rejected: every small addition
  would have to wait for the owner or make a child concept.
- *Additions by other parties may be required.* Rejected: other modules that
  record that concept do not know the additional property, so their actions
  would be rejected for a reason they do not recognize.

**Consequences**
- Required attaches to the pair of property and concept, not to the property
  alone.
- Other parties who need a required property make a child concept of their
  own.
