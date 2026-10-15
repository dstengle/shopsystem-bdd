# Records

Dated, never edited (design model v3, section 3a). Not design and not work.

| path | record | kind |
|---|---|---|
| `observations.md` | what was noticed, one `## <id>` each | origin: may be an initiative's `source` |
| `measurements/kb-baseline-2026-10-11/` | facts of shopsystem-kb batches 32-35 (`measurement/kb-batches-32-35`) | origin |
| `measurements/fixture-runs/` | test logs of each release's fixture runs | origin (not yet given ids) |
| `review-findings/` | reviews of the plugin, such as the 13 October assessment | origin |
| `archive/design-notes/`, `archive/plans/`, `archive/requests/` | the design notes, plans and requests of releases 0.6.0-0.18.0, moved from `docs/superpowers/` | history: read to trace why, never a source |

A record file is a node for `scripts/model` only when its frontmatter has an `id`, a `kind` and `about`.
