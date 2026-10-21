# 0001. Standard first, software follows

Date: 2026-10-17
Status: partly replaced by 0052. The result of the comparison with the system
is a new system built from the standard, not a list of changes for the
prototype.

**Context**
During the prototype, the basic vocabulary of Uniti (the roles in the "core")
was designed together with the software, and its form was largely determined
by what the code could do at the time. Some parts were never used and had to
be torn down. Uniti wants to be a standard that anyone can follow, and that is
not possible if the standard exists only inside one piece of software.

**Decision**
- The Uniti Standard is written as a document of its own, without referring to
  any existing software, database, or code.
- When software differs from the standard, the standard is right.
- Experience from the prototype is used as inspiration, not as a benchmark.
- The comparison with the existing system is done **after** v0.1 is frozen,
  and its result is a list of changes for the system.

**Alternatives**
- *Formulating the standard from what already exists in the code.* Rejected:
  the standard would inherit the limits of the current code, and what has not
  been built yet would never get in.
- *Writing the standard and the code together.* Rejected: experience from the
  prototype shows that the code tends to determine the form.

**Consequences**
- Software work that depends on the basic form, including the update of the
  "core", is postponed until v0.1 is done.
- Uniti's own implementation will later be only one implementer of the
  standard.
