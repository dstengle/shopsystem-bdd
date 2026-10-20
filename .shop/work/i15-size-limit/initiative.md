---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i15
title: Files within the size limit
summary: A mechanical size check over every tracked Python file, tests included, with a 300-line limit, and this repository's files split to it.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 1
source: [observation/2026-10-20-files-too-large]
date: 2026-10-20
---

Pulled into this release (the person, 2026-10-20: "Every edit to those large files is expensive"). Large code files slow agents down.

Covers:
- analysis-tools gains `tools size` (lines to formulate, as proposed to the person):
  - **When** `tools size` is run, `tools` shall print each tracked Python file over the size limit, with its line count.
  - **If** any tracked Python file is over the size limit, then `tools size` shall exit 1.
  - **Where** the repository's `CLAUDE.md` gives no size limit, `tools size` shall use 300 lines.
  A Python file is one with a `.py` extension or a `python` shebang, a test or step module included.
- the reviewers and the implementer's done check run `tools size` in place of judging by eye;
- this repository gets a `CLAUDE.md` with its module map and the limit: 300 lines for code and tests alike;
- this repository's files split to it (scripts/model, the step modules, scripts/features, scripts/supervise.py,
  scripts/tools; scripts/plan goes with slicing, scripts/measure is i12's).
