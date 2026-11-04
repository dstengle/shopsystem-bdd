---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-recon
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Recon for the workflow simplification: cost, review yield, gates, decisions, quotes

Three read-only surveys made during the 2026-11-04 brainstorming session that led to `design.md` in this folder. They
read the measurements, review files and analyses of i42-i64, the GF-conversion records, `spec/decisions/`,
`.shop/work/`, the hooks and the superpowers 7.0.0 plugin. Counts of findings come from headings
(`### N. <grade>, <triage>`). Findings carried from one review round to the next are counted again.

## Cost and time (11 measured initiatives, i42-i64)

- **Totals:** $87.08 and about 6.2 h of session time.
- **The window:** 15-104 min of session time per initiative, but 0.7-119 h from first stage to last.
- **By stage (cost):**
  - task review $20.12 (23%), more than implement at $16.94 (19%);
  - integrate $15.23, plan $13.34, formulate $11.91;
  - research $1.19.
- **Branch reviews:** cost not recorded in the measurements.
- **Sources:** `.shop/records/measurements/<date>-<i>.md`, `.shop/records/2026-11-02-work-run-efficiency.md`.

## Review yield

- **Task reviews:** 38 of them.
  - About 75 findings, 2 Critical and 19 Important.
  - About 7-8 distinct fix-now defects.
  - 28 of the 38 found nothing to fix now.
- **Branch reviews:** 25 of them.
  - 167 findings.
  - About 4 fix-now defects that only a branch review caught.
  - Much of the rest is noise. The review range was all of `main` (in i54, 323 of 331 commits belonged to no
    work-item of the initiative), and findings were carried across rounds (i60 ran 6 rounds with the same fix-now).
- **Sources:** `.shop/work/<i>/runs/*/*review*/findings.md` and `.shop/records/<date>-<i>-analysis.md`.

## Question gates

- **Stops:** 64 awaiting-answer stops, 35 of proposals and 29 of work-items.
  - Median wait 1-6 min, about 300 h in total.
  - The longest single waits: 98.7 h (i62) and 77.7 h (i48).
- **Causes**, from the efficiency record's 26 stops: 8 were a decision missing from the spec, and 12 came from outside
  the work-item (dropped ids, flaky scenarios, start failures, an unrebased branch).

## The superpowers-built GF conversion

- **Measured:** $150.09 over 6 h 21 min, unattended, with no questions to the person.
- **Gates:** 6, costing $8.52, all passed first time.
- **The same work through `work run`** was estimated at $292-$1,682 with 100-1,180 rulings
  (`2026-11-03-gf-conversion/cost-analysis.md`).
- **Defects found afterwards:**
  - 7 in the live run;
  - revisions 2-3 after the person's review: generation crashes on removed Given blocks, 115 of 128 condition
    definitions not parsing, 174 L1 clashes before fixes.
  - These were spec and design problems, not ones a code review would catch.

## Decisions (`spec/decisions/`)

- **Count:** 72, from 0001 to 0073 with no 0070.
  - Newest 2026-10-28 (0073); nothing added since.
  - 18 declare `supersedes:`, yet the decisions they replace still say `accepted`.
- **Rough sort:**
  - about 18-20 checkable mechanically (e.g. 0017, 0042, 0045, 0055 not yet enforced);
  - about 28 behaviour or contract that could be spec requirements;
  - about 10 judgement only (0005, 0007, 0009);
  - about 15-18 obsolete or superseded.

## The queue (`.shop/work/`)

- **Counts:**
  - 64 initiatives: 46 done, 12 started, 6 abandoned;
  - 224 capability-proposals and 7 glossary-proposals;
  - 246 work-items: 172 green, 72 withdrawn;
  - 47 requests.
- **Files per initiative:** i39 alone holds 348 files of about 20 kinds.
- **`model check`:** reports 53 violations, 16 warnings and 29 unresolved references. Nearly all are about requests and
  initiatives.

## Quotes, transcripts, ids

- **Quotes:**
  - The person's words are kept only as dated one-line quotes (`delegation:` in `q<n>.md`, `work note`, `work answer`).
  - `scripts/migrate_prompt.py` ignores the hook's stdin, so the session id and `transcript_path` are dropped. No
    conversation context around a quote is stored.
  - Only worker rounds carry session ids, in `log.jsonl`.
- **Transcripts:** `scripts/measure_read.py` reads usage, timestamps, session and agent ids, tool-use names and
  compaction boundaries from transcripts, never message text.
- **Ids:** `i<n>`, `w<n>`, `q<n>`, `r<n>`, `g<n>`, `NNNN` decisions, and full `request/<context>/q<n>`. Nothing expands
  them to names for the person.

## Superpowers 7.0.0

- **What it lacks:** no telemetry (`diagnosing-superpowers` analyses transcripts after the fact), no backlog, and no
  cross-session state beyond plans under `docs/superpowers/plans/` and the gitignored `.superpowers/sdd/<plan>/`
  progress ledger.
- **What it offers:** parallel agents, worktrees, subagent-driven development (implementer plus reviewer per task),
  requesting and receiving code review, and finishing a branch.
