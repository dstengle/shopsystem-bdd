---
id: decision/work-file-forms
summary: "Initiatives, parts and records are Markdown files whose frontmatter carries the grammar's fields, in the forms `model --help` states."
date: 2026-10-15
status: proposed
source: "docs/design-model/design-model.md v3 section 8"
---

# 0026. Work file forms

## Decision

`work/<initiative>/initiative.md`: id, title, summary, kind, owner-level, status, priority, source, date. `work/<initiative>/<part>.md`: id, kind, part_of, status, and for a capability-proposal argues, adds, changes, removes, date; for a work-item under, wkind, accepts, check, blocked_by, depends_on, fileset, for. `records/observations.md`: one `## <id>` heading an observation, with `about:`, `by:`, `date:` lines. Other records: frontmatter id, kind, about.

## Context

v3 names the files and fields but not their spelling.

## Alternatives

One YAML file per breakdown; a database.

## Consequences

Files first, as v3 says; the corpus when a trace can no longer be assembled from them.
