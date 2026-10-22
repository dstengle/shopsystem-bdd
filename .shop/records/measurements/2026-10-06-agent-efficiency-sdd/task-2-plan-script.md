---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-06-agent-efficiency-sdd-task-2
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-07
---

# Agent efficiency task 2: the plan script, implementer report

Implementer report for task 2 of the 2026-10-06 agent-efficiency plan (0.10.0): scripts/plan built test-first, run read-only on shopsystem-knowledge's living plan, and its fix round 1 (whole log entries, --current usage error). The brief is Task 2 of .shop/records/archive/plans/2026-10-06-agent-efficiency.md. Commits 8382992..db66c75. The slice-plan-tool capability that later specified this script has since been removed, so the record is about the bounded context.

Archived from `.superpowers/sdd/2026-10-06-agent-efficiency/task-2-report.md` (git-ignored scratch), text as it was.

---

# Task 2 report: scripts/plan

## Implemented
`scripts/plan` (executable, stdlib): check, log, backlog, status, add-slice, archive, show (--open, --backlog, --requests, --last-suite [--current]). Contract in `--help` epilog. Blocks are kept as raw lines; only the touched block is edited, so unknown sections survive byte for byte. Every read and write validates; a refused edit leaves the file untouched. `--current` uses `git rev-parse --verify` (unknown commit -> `stale: commit X is not in this repository`), `git diff --name-only <commit>` and `git status --porcelain`.

## TDD evidence
Tests written verbatim from the brief first.
RED: `python3 -m unittest tests/scripts/test_plan.py` -> `Ran 18 tests ... FAILED (failures=17)` (script missing: "can't open file .../scripts/plan"). One test, test_an_unknown_section_survives_every_edit, passed vacuously in RED (a missing script edits nothing).
Then built one slice of behaviour at a time, re-running after each: check (2 pass), log+backlog, status, show, add-slice, archive, --current; failures went 17 -> 15 -> 14... -> 3 -> 2 -> 0.
GREEN: `python3 -m unittest discover -s tests/scripts -v` -> `Ran 33 tests in 1.018s OK`.

## Step 5 (clone at $SCRATCH/sk, plan untouched; git status clean)
- `plan check` -> `ok` (exit 0)
- `plan show --open` ->
  53 shop-knol answers through a kb server ... : blocked: awaiting a kb release ...
  55.1 init never furnishes twice: in progress: its server row waits on slice 53
  55.2 init furnishes a served empty store: blocked: awaiting slice 53
- `plan show --last-suite --current` -> record line, then `stale: the record names no commit` (exit 1): the real record reads "(after ... e05a55b; ...)", not `at <hash>`. Safe outcome; the template format is `Suite: N passed, M failed at <hash> in <s> s`.
No shape needed fixing; tests added: 0 (count stays 33).

## Files
scripts/plan, tests/scripts/test_plan.py

## Self-review
- Untested but built because the contract/interface requires: show --backlog, slice-after-section and duplicate-number checks, title check.
- `--current` without `--last-suite` is silently ignored (unpinned, not built).
- archive with no Suite line omits the "; last ..." suffix (unpinned choice).
- archive's archive file keeps only bullet log lines.

## Concerns
- Real plan's suite record lacks `at <hash>`; `--current` will say stale until a record in the 9. global-constraints format is logged.

## Fix round 1
Changes: `bullets()` now returns whole entries (a bullet plus its non-blank continuation lines); archive writes every entry whole to the archive and keeps whole REQUEST entries in the living log; `show --requests/--backlog` print whole entries; `show --current` without `--last-suite` is a usage error (exit 2); `--help` CONTRACT now carries all five Step 3 bullets plus the exit-status line.
Tests added (RED first: both failed, 20 run, failures=2): test_archive_keeps_continuation_lines_with_their_entries, test_current_without_last_suite_is_a_usage_error.
Command: `python3 -m unittest discover -s tests/scripts -v` -> `Ran 35 tests ... OK`.
