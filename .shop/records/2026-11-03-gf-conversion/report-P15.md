---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p15
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# P15 report: a new request through the new requirements system (the test)

Branch `gfc/P15`, from `gf-conversion` at 11158f12. Run with `SHOPSYSTEM_GF` unset (P1's installer). The package is
a test, so the test came first and no plugin code changed: every step passed on the plugin as merged at layer 5.
This record is written with Bash, because the harness's Write tool refuses subagent report files.

## What was added

- `tests/scripts/fixtures/e2e/repo/`: a small codified context.
  - `spec/index.md` holds a typed glossary. `spec/universal.md` holds U1.
  - There are two capabilities. `work-queue` is a service capability with g1 (`work start`), and `review` is a
    guarantees capability.
  - `features/work-queue.feature` is generated. `pytest.ini`, `.shop/delivery.toml` (2 workers) and
    `.shop/records/observations.md` hold the origin the request cites.
  - The Python files carry the suffix `.in` so that neither this repository's pytest nor its size and lint checks
    read them. They are the scenario `conftest.py.in` (with `@PLUGIN@`), `test_work_queue.py.in`,
    `work_queue_handlers.py.in` and a toy `queue_cmd.py.in`.
  - The fixture gives `model check` 0 rows, `model logic` no findings, and `features generate --check` exit 0.
- `tests/scripts/test_e2e_codified.py` (228 lines): one test. It clones the fixture into a git repository with a bare
  remote and puts the stand-in claude (`SHOPSYSTEM_WORK_CLAUDE`, `STUB_CLAUDE_PLAN`) first on PATH, with one plan and
  one record per phase. It then goes through these steps:
  1. `work request --from internal --source <observation>` with one good line and one line that does not parse is
     refused. The output says `line 2 does not parse … parsed up to: When asked`, and nothing is written.
  2. The codified line alone is accepted, and q1 is `open`.
  3. `work run` (no initiative) runs the intake round. Its stub runs `work outcome q1 1 accepted` and `work turn q1`,
     and q1 becomes `accepted`. Then `work start q1` gives i1, `proposed`.
  4. `work run i1` runs the integrate round. The first session drafts g2 with `proposed` → `abandoned`. That draft
     is refused, and the second session's brief carries
     `Refused drafts (send-back 1 of 2): L3 work-queue#r3 … which no transition allows`. The second session drafts
     the clean g2 (r3, r4 and a `given` block).
  5. The gate session's brief has `Generated scenarios (preview):`. The proposal is `awaiting-answer`, and
     `work answer work-queue …` approves it.
  6. `work run i1`: the apply round's stub commits the drafts into `spec/capabilities/work-queue.md`.
  7. The scripted formulate runs with no session. `features generate` writes `@g2 @r3 @r4` and commits
     `features: work-queue generated from work-queue`. The proposal becomes `formulated`.
  8. w1 is drafted with `accepts: [work-queue#r3, work-queue#r4]`.
  9. Research, plan, implement and review run. The implementer stub commits the `work abandon` handler and
     `queue_cmd.abandon`. Before the merge, the suite record names the new scenario as failing. After the merge with
     `--work-item`, the record is `Suite: 2 passed, 0 failed`. Then come the branch review, the analysis and i1
     `done`. The run exits 0.
  10. `work resolve q1 --line 1 work-queue#r3 <head>` sets q1 to `delivered`.
  The final checks: the generated feature, `features generate --check` exit 0, `model check` with 0 violations,
  `model logic` with no findings, i1 `done`, and a clean tree.

## Checks

- `python3 -m pytest -q tests/scripts/test_e2e_codified.py`: 1 passed in about 11 s.
- Full suite: 771 passed, 1 skipped, 0 failed. That is layer 5's 770 plus this test.
- `python3 scripts/tools size --limit 300`: exit 0. `ruff check` on the test: clean. `tools check`: nothing to check.

## Calls

- **The request's origin.** At first the request cited `the person` as its source. `model check` then gave v10a and
  v17 rows, because only an origin can be a source. The fixture therefore has an observation record, and the request
  cites it.
- **The review capability's line.** At first `review#r1` restated U1, which gave an L2 note. It now says
  `Every worker shall hold a worker slot.`, so `model logic` reports no findings at all.
- **The gate's question.** The gate stub gives no questions. `work run` then asks its own approval question
  (`Are the lines of work-queue approved as drafted? …`), and the test answers that question.
- **The resolve version.** The version given to `work resolve` is the short HEAD commit, because the fixture has no
  plugin version of its own.

## Asks

- None. No shared file was changed.

## Module-map rows

- None. The package adds a test and a fixture, and no script.
