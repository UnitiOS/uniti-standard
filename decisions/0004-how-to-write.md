# 0004. Location, language, and how the standard is reviewed

Date: 2026-10-17
Status: partly replaced by 0048 and 0052. Ownership moves from stage 4 to v0.2
(0048). Stage 7 becomes a quick test, and stage 8 is added (0052).

**Context**
The standard needs a place, a language, and a way of working before its content
is written.

**Decision**
- **Location:** the directory `uniti-standard/` in the root of the repository.
  Its name is deliberately different from the existing code so that they are
  not confused. Later this directory may be moved to a repository of its own,
  because the standard stands apart from its implementation.
- **Language:** Indonesian while the standard is being shaped, then translated
  into English when it is stable. The English equivalent of every term is
  recorded from the start.
- **Way of working:** written in stages. Each stage is written as a draft,
  reviewed by the owner, its decisions recorded here, and then committed with
  the owner's approval.

| Stage | Content |
|---|---|
| 1 | Skeleton, principles, glossary, document layout |
| 2 | Facts, addresses, change |
| 3 | Values, concepts, relations |
| 4 | Calculation rules, proof, ownership |
| 5 | Cross-domain test of the form |
| 6 | First content: concept cards, code lists, first vocabulary |
| 7 | Quick test: makes sense, and better than the prototype (0052) |
| 8 | Locking v0.1, translating it into English, and packaging it (0052) |

**Alternatives**
- *English right away.* Rejected for now: harder to review while the content is
  still being shaped.
- *The directory name `standard/`.* Rejected: easily confused with the part of
  the code that has the same name.

**Consequences**
- File names and titles use Indonesian until the translation is made.
