---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-job-gate-pages
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-21
---

# Gate pages of the migration release (0.21.0)

The gate pages the person judged during the migration release (0.21.0), copied out of a job workspace on 2026-10-22, kept raw. Each page is `head.html` plus a body template with its data (a JSON object) put in place of `__DATA__`; the person's verdicts, saved through the page's review store, are the measurement records 2026-10-19-job-gate-export-spec-gate-review, 2026-10-20-job-gate-export-skeleton-gate and 2026-10-21-job-gate-export-release-gate. No token or personal email address is in these files (checked).

- `spec-gate-review.html`: the Spec Gate Review page as it stood at commit 26e0dd2 (2026-10-19 23:10 UTC): i13's EARS rewrite of every capability (17 capability-proposals, each line with the line it came from and Claude's reading) and decisions 0051 and 0052. Its earlier content, which the exported spec-gate-review verdicts judge, is not kept here.
- `data.json`: that page's data, the same JSON as is embedded in `spec-gate-review.html`.
- `skeleton-gate.html`: the Skeleton Gate page at commit 3fb11a9 (2026-10-20): five question cards on i10's walking skeleton (the result of 3 real deliveries, new lines, workers' Python, Haiku for research, migration-tools' open readings).
- `release-gate.html`: the Release Gate page at commit bec63e9 (2026-10-21): nine question cards (release, glossary, pytest-python, delivery-toml, skill-tool, r20-fileset, lines, decisions, readings).
- `head.html`: the shared head (title and stylesheet) of the pages.
- `body.html`: the body template of the Spec Gate Review page (the rendering script, its group order and notes, and the review store calls).
- `body-gate.html`: the same template with the group order, names and notes of the earlier spec gate (no `ears` group).

Files kept as they were, beside this record:

- `spec-gate-review.html`: from `.shop/scratch/from-job/gate-pages/spec-gate-review.html`
- `data.json`: from `.shop/scratch/from-job/gate-pages/data.json`
- `skeleton-gate.html`: from `.shop/scratch/from-job/gate-pages/skeleton-gate.html`
- `release-gate.html`: from `.shop/scratch/from-job/gate-pages/release-gate.html`
- `head.html`: from `.shop/scratch/from-job/gate-pages/head.html`
- `body.html`: from `.shop/scratch/from-job/gate-pages/body.html`
- `body-gate.html`: from `.shop/scratch/from-job/gate-pages/body-gate.html`
