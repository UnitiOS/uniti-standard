# 0003. Its own standard, with three ways of relating to outside standards

Date: 2026-10-17
Status: accepted

**Context**
Many outside standards are well established, but each one covers only one
narrow field: currencies, units, data provenance, descriptions on the web, or
economic models. Uniti needs something that is detailed and at the same time
very broad, plus things that no standard has yet. The question: does Uniti
"follow" an outside standard, or make its own standard?

**Decision**
Uniti makes **its own standard**, inspired by outside standards, and relates to
outside standards in three ways:

| Kind | Stance |
|---|---|
| Established code lists (currencies, units, countries, languages) | Used directly, not recreated |
| Concepts that have an equivalent in an outside standard | Owned by Uniti, with a bridge to the equivalent |
| Things that have no standard yet | Entirely owned by Uniti |

In this way, outsiders recognize the code lists directly, understand the
concepts through their bridges, and only need to learn from scratch the things
that are truly specific to Uniti.

**Alternatives**
- *Following one outside standard completely.* Rejected: no single standard
  covers all the needs, and their content is not designed to record the
  activities of an organization over time.
- *Making everything itself without bridges.* Rejected: Uniti would become
  "yet another standard" that is hard to understand and hard to connect to
  other systems.

**Consequences**
- The concept form provides a place for bridges, and the relation form
  contains the kind of relation "same or similar in meaning to".
- Part B contains the list of outside code lists that are used.
- This pattern is similar to the health standard FHIR, which makes its own
  concepts but uses code lists that already exist and names their equivalents
  in other standards.
