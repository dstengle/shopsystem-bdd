# Measuring a batch: test log (0.12.0)

Spec: `docs/superpowers/specs/2026-10-11-measuring-a-batch-design.md`.

## `scripts/measure`

`python3 -m unittest discover -s tests/scripts`: 70 OK, 14 of them `test_measure.py`. Each builds a repository
with dated commits (two archive commits, a batch plan that grows from two tasks to three) and a session directory
with generated transcripts. Pinned: a batch's bounds from the archive commits; a request's usage counted once
across rows; attribution by description, by the prompt's `task-<n>-brief.md`, and none; statuses and findings as
replied; commits and their files by the implementer running; `Lands:` against touched; tasks planned against run;
hand-backs with their continuation lines; the controller's requests inside the batch; the closing share with scouts
left out; a resumed agent as one dispatch with two prompts; a transcript with no usage refused by file and line; the
open batch; a facts file not written over; `show` and `compare`.

Two rules came from the runs below and not from the spec: a facts file that exists is not written over without
`--replace`, and a batch in which no dispatch is found writes nothing.

## The baseline: kb's batches 32 to 35

`measure batch` on shopsystem-kb, read only; the facts are under `docs/superpowers/testing/2026-10-11-kb-baseline/`
in this repository and nothing was written to kb. Batch 35 was open and is cut at 2026-10-11T01:41:36Z.

| | 32 | 33 | 34 | 35 (open) |
|---|---|---|---|---|
| plugin | 0.10.0, 0.11.0 | 0.11.0 | 0.11.0 | 0.11.0 |
| slices | 7 | 11 | 5 | 3 |
| dispatches | 26 | 31 | 11 | 8 |
| tasks planned, run | 7, 7 | 7, 11 | 5, 5 | plan not committed |
| hand-backs | 0 | 2 | 1 | 1 |
| span, minutes | 180 | 105 | 51 | 35 |
| share closing | 0.14 | 0.30 | 0.38 | 0 |
| task reviews, clean | 5, 2 | 8, 4 | 1, 1 | 3, 1 |
| implementers: new input | 1.13M | 1.60M | 0.67M | 0.52M |
| implementers: cache read | 72.5M | 28.9M | 9.8M | 10.7M |
| controller: requests | 107 | 96 | 38 | 28 |
| controller: cache read | 26.5M | 31.3M | 18.1M | 15.4M |
| controller: peak context | 412k | 433k | 519k | 585k |
| starting context, all dispatches | 512k | 714k | 276k | 192k |

Against the request's hand-summed figures:

- **Agrees.** Batch 33 planned as 7 tasks and ran 11; about 105 minutes; seven per-task reviews clean (2, 4 and 1
  in batches 32 to 34); the closing share (the request: about 37% of wall-clock closing; here 0.30 and 0.38 of
  agent time in the two batches run wholly on 0.11.0); batch 33's implementers at about 1.7M (1.60M new input and
  0.36M output).
- **Shares by role.** The request: implementers 49%, reviewers 28%, scouts 23%. Here, output and new input over all
  four batches: 52%, 28%, 20%.
- **Totals differ, and why.** The request's 3.0M, 1.8M and 1.4M are the agents' own usage totals for slices 157
  to 165.6. Here the same roles come to 4.8M, 2.6M and 1.9M of output and new input, because batch 32 as the
  archive bounds it also holds slices 154 to 156 (0.10.0, slice 156 alone 0.54M new input) and its planning
  scouts, and because an agent's own total is not the sum of what each request newly read.
- **Not in the request.** The controller: 26M to 31M cache-read tokens a batch, more than the implementers' in
  batch 33, in one session that ran all four batches and whose context grew from 412k to 585k. And `Lands:` against
  files touched: of the 23 slices that carried a `Lands:` line, 15 touched more than it in production or in test
  files (fix rounds included).
- **The floor per dispatch.** The request estimates 30k to 40k a dispatch, "CLAUDE.md, the brief, the reports
  before it". An implementer's first request already holds 29k and a reviewer's or a scout's 15k, before any file
  is read. Of the implementer's extra 14k, about 6k is the listing of every installed skill, which it is sent
  because it has the Skill tool, and 3k is `bdd-red-green`. kb's `CLAUDE.md` (about 6k to 8k) is in every agent's
  first request, loaded by the harness. In the session's transcripts no implementer opened `CLAUDE.md` with Read;
  before its first edit an implementer read the brief (about 900 tokens), sometimes the report (about 2k), and
  source and test files. A smaller brief would not lower this floor.

One dispatch of 76 was not attributed (a scout described as "Research export/import of versions"). No commit was
ambiguous.

## `analyzing-a-batch`

Fixture: a clone of kb at batch 33's archive commit, with the facts for batches 32 and 33 committed and batch 33's
ledger files beside it, under `/home/vscode/scratch/shopsystem-bdd/analyze/`. One prompt, headless
(`claude -p --plugin-dir`): the batch has closed, here are its archive, its ledger and the plugin's scripts; what
did it cost, why did it grow, what should we try changing; write it up, do not ask.

**Before (no skill, the script present), one run, Sonnet, 100 s:** a readable report, with these faults.

- It ran `measure batch` over the committed facts file, found no transcripts for the clone, wrote an empty file
  and restored the old one with `git checkout`. "I regenerated the facts with `measure batch` while working".
- The report went beside the measurements, in a shape of its own, with no `path:line`.
- Seven changes proposed, two worded as rules: "Add to the checkpoint step: an open question that names…", "In the
  brief template, ask the planner to…".
- Figures rounded and combined ("about 19%, 23%, 13% and 24% of the batch").
- No row per finding: which stage found each defect and which could have was not asked of every one.

**After, three runs (two Sonnet, 67 s and 82 s; one Opus, 215 s):** each loaded the skill, read the facts with
`show` and `compare` and did not write them again, and committed a report at
`docs/superpowers/reports/2026-10-11-batch33-analysis.md` with the eight sections in order (the Opus run added
"In short" above them). Each had 2 hand-back rows with the cause "listing omission" cited to the ledger and the
plan, 6 finding rows with the stage that found each and the earliest that could have, 4 task rows (all four
added tasks traced to a task review's spec question or finding), and exactly 3 candidates, each with what it rests
on and the number that would move.

One loophole closed after these runs: two of three listed the unattributed scout among the replies not done. The
skill now says which statuses count and that an unattributed dispatch goes under Not counted. Not re-run.

## Not tested

- The two lines added to the plan's execution rules (descriptions that say what a dispatch is; measure at the
  close): no controller ran by them. kb's controller wrote descriptions close to the convention unprompted, and 75
  of 76 were attributed without it.
- `measure` on a batch run in lanes, where two implementers' commits overlap in time.
- A harness version other than 2.1.293 and 2.1.296.
