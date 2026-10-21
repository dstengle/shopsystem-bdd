---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/light-decisions
summary: "A decision file is light: frontmatter (id, summary, date, status, supersedes, revisit_when, source, by) and a Decision section; Context and Alternatives are written only where options were weighed."
date: 2026-10-19
status: accepted
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0046. Light decisions

## Decision

A decision file is `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in the directory.
Its frontmatter is `id`, `summary` (one sentence), `date`, `status`, and where they apply `supersedes`,
`revisit_when`, `revisit_signal`, `source` and `by`. Its body is a `# <nnnn>. <title>` heading and a
`## Decision` section: a paragraph, a layout or a convention. `## Context` and `## Alternatives` are added
only where there was a real trade-off, two options weighed; `## Consequences` is not written. A decision that
needs neither is a summary and a Decision section, nothing else.

Existing decision files keep their sections: they are not rewritten to the light form, since the Context,
Alternatives and Consequences of an accepted decision are record.
