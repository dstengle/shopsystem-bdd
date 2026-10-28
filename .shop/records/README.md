# Records

Dated, never edited (design model v3, section 3a). Not design and not work. Paths are under `.shop/records/`.

| path | record | kind |
|---|---|---|
| `observations.md` | what was noticed, one `## <id>` each | origin: may be an initiative's `source` |
| `measurements/kb-baseline-2026-10-11/` | facts of shopsystem-kb batches 32-35 (`measurement/kb-batches-32-35`) | origin |
| `measurements/fixture-runs/` | test logs of each release's fixture runs | origin (not yet given ids) |
| `review-findings/` | reviews of the plugin, such as the 13 October assessment | origin |
| `2026-10-28-gate-question-wording.md` | the causes of 42 gate questions (i39-i43) against the wording of requests, spec lines, glossary and round instructions, with five recommendations | analysis |
| `2026-10-28-tools-skills-subagents.md`, `2026-10-28-tools-skills-subagents/` | tool friction, refused commands and the case for more tools, skills or subagents over 87 sessions of i37-i42, with its scripts | analysis |
| `2026-10-28-requirement-checking.md`, `2026-10-28-requirement-checking/` | whether clingo, English-structure NLP and a fast model judge can test a requirement line, with the parser, the clingo proof of concept, its outputs and a draft requirement-writing skill | analysis |
| `archive/design-notes/`, `archive/plans/`, `archive/requests/` | the design notes, plans and requests of releases 0.6.0-0.20.0, moved from `docs/superpowers/` | history: read to trace why, never a source |

A record file is a node for `scripts/model` only when its frontmatter has an `id`, a `kind` and `about`.
