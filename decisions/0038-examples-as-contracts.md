# 0038. Examples as a contract between versions and between modules

Date: 2026-10-19
Status: accepted

**Context**
The kinds of change between versions (decision 0012) show what changed, but
not the effect on the numbers. A user of a module needs to know, before
installing a new version, whether the numbers will change.

**Decision**
- The examples of the old version are run again with the new version. Those
  that fail must be fixed, or marked **replaced** with a reason.
- An example is never deleted. A replaced example can still be read and is no
  longer run.
- Every example that is replaced because it failed is reported by the
  machine as a **behavior change**, with the old result, the new result, and
  the reason.
- Before a module uses a new version of another module, all its examples are
  run with that new version.
- An organization may write examples in its own module to bind the module set
  it has installed.

**Alternatives**
- *The maker states for themselves whether behavior changed.* Rejected, for
  the same reason as in decision 0012.
- *An old example that fails blocks the new version forever.* Rejected: a
  legitimate policy may change, as long as the change is visible.

**Consequences**
- Marking an example as replaced in the vocabulary may need the approval of
  more than one party. This is discussed together with governance (study
  A2).
