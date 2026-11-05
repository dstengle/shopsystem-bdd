# Plan 7 of the workflow simplification: implementation report

This is the report of the one implementer agent that executed `plan-7-telemetry.md` on 2026-11-05. It used
superpowers:executing-plans, with one commit per task and no subagents per task. The one subagent was the real
reviewer of Task 6's smoke run.

All 6 tasks are done. The `telemetry` capability is built, and all 4 of its requirements are out of `unbuilt:`.
- `measure batch <batch>` measures a batch from git and its sessions' transcripts on disk. It gives the wall time,
  session time, tokens, cost and cost by role, the pull request's findings by grade, the defects traced to their
  items, and the knobs. It writes them as `.shop/records/measurements/<date>-batch-<n>.md`, with a `## Summary` of
  tables before the JSON block.
- `measure defect <item> --says …` records a fault found after the merge, against its delivered item and its merged
  batch.
- `measure show` prints a batch's summary and sessions. `measure compare` takes `batch-<n>` names.
- 0060 is superseded by `0078-measure-a-batch` (a `requirement` decision enforced by telemetry r1-r4). A knob is
  changed by a decision (`0079`, `judgement`).
- analyzing-a-batch, building-a-batch and shaping-items say how a batch is measured and how a defect is recorded.

A real reviewer subagent was dispatched on a scratch batch and measured: **$0.28** and **36 s** of session time for
**5 requests** (plan 5's open problem). The commits are on `workflow-simplification`, from `8212c6f4` to this
report's commit, and are not pushed. No baseline got worse.

## Final state

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | **1459 passed**, 1 skipped, **4 xfailed**, **135 subtests** passed (29.7 s). The start was 1402 passed and 8 xfailed. The 57 new passes are the 4 telemetry scenarios and 53 script tests: cost 6, batch read 7, batch 19 (8 of them the role cases), defect 8 (4 of them the refusal cases), batch show 6, decision checks 1, analyzing-a-batch 3, building-a-batch 2 and shaping-items 1. The ceiling report lists `test_e2e_codified` (13.3 s), as before. |
| Timing run (`python3 -m pytest -m timing -n 0 -q`) | `2 passed, 1464 deselected` (5.8 s) |
| Unbuilt ids | `False 5 []`: telemetry is absent, 5 ids remain (brainstorming r3, conversation r1-r4), no problems |
| `model check` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems (at baseline) |
| `model logic` | `11 findings: 6 L5, 5 L6` |
| `model lexicon --check` | `401 terms, 0 problems` |
| `model decisions --check` | `4 check decisions: 4 hold, 0 failing`, exit 0 |
| `features generate --check` | exit 0 |
| `features vocab --check` | `every step has one handler` |
| `features bindings --unbound` | `every binding names a scenario` |
| `tools size --limit 300` | Silent. These files have their own limits: `scripts/measure` 142 (≤ 150), `measure_show.py` 122 (≤ 135) and `measure_write.py` 42 (≤ 50). The new files are `measure_cost.py` 60, `measure_batch_read.py` 90, `measure_batch_sessions.py` 86, `measure_batch.py` 135, `measure_batch_show.py` 98, `measure_defect.py` 111, `telemetry_handlers.py` 188, `measure_batch_testing.py` 84 and `test_measure_batch.py` 220. `measure_read.py`, `measure_build.py`, every `batch_*.py` and the shared scenario worlds are unchanged. |
| `tools check $(git diff --name-only 9d765bb8...HEAD -- '*.py' scripts/measure)` | ruff and vulture clean; import-linter states no contracts |

## The smoke run with a real review (D18)

The run was in `/home/vscode/.claude/jobs/7e9ba079/tmp/smoke7/`, using `build.py` and `close.py` (the suite's helpers,
`review_testing.published`'s recipe). It had the fixture spec of `ex.com/prod/ctx`, a bare `origin` and the stand-in
gh. It built two ready items, b1 "Abandon" and b2 "Exit". Then it ran `work batch start`, `resume`, the hand commits,
`done`, `review` and `brief`.

1. **The reviewer.** This session does not list `shopsystem-bdd:pr-reviewer`, so I dispatched a `general-purpose`
   agent on `opus`. Its description was `batch-1 review 1`. Its prompt was the body of `agents/pr-reviewer.md` and
   the brief's path, and it was told to use only Read, Glob, Grep and Write.
   - It found that the scratch items build nothing real, with 2 `fix now` findings (Important, on b1 and on b2) and 2
     observations (Minor).
   - **The harness refused its Write** ("Subagents should return findings as text"), so it returned the findings file
     in its reply. I saved it byte for byte at the brief's `Findings file:` path. The only change was to fence its two
     quoted run lines, as it asked. `work batch reviewed` then printed `batch-1 review 1: 4 findings, 2 fix now ->
     building`.
2. **Closing the batch** (`close.py`). I made one hand fix commit for each finding, with `Item:` and `Finding:`, then
   ran `review` and `brief`. **Review 2's findings file was written by hand** (`None.`, then `f1: fixed`, `f2:
   fixed`). This kept the plan's spend on a model to one reviewer, and the record says it is a stand-in. After that
   came `-> awaiting-merge`, the `--no-ff` merge, gh's state `MERGED` and `work batch merged` (`batch-1 merged`).
3. **The measurement**:
   `measure batch batch-1 --sessions ~/.claude/projects/-home-vscode-shopsystem-bdd/6e62f351-f72c-4381-bd4b-b228ec741fcd`
   took 0.37 s and found 26 transcripts.

| Figure | Measured |
|---|---|
| The window | started 06:00:00Z, first review 06:00:01Z, built 06:01:51Z, closed 06:01:51Z; wall time **1 minute 51 seconds** |
| The reviewer's session | `general-purpose`, role **review** (from its description, D6 rule 3), first request 06:00:39.8Z, **5 requests**, session time **36 s**. Tokens: output **3,712**, new input **31,988**, cache read **209,642**. Cost **$0.276098**. The harness's own report for the agent was 54,170 tokens, 9 tool uses and **42.6 s** wall. |
| Cost by role | planning 0, implementing 0, review **0.276098** (1 session), fixing 0; the total is 0.276098; `unpriced` {} |
| Findings by grade | Critical 0, Important 2, Minor 2; `defects.review` {b1: 1, b2: 1} |
| Knobs | batch_size 4, items 2, changed_lines 2 (the last review's range: the two fix commits), size_limit 1000, reviews 2, readiness_bar mechanical |
| After `measure defect b1 --says …` | It wrote `.shop/batches/1/defect-1.md`, committed as `measure defect: batch-1 d1 of b1 "Abandon"`. `measure batch batch-1 --replace` gave `after_merge` {b1: 1}, `per_item` 1.5 and `goals.defects_per_item` 1.5. |
| `measure compare batch-1 batch-1` | Every row with a figure has ratio `1`. The rows whose figure is 0 (planning, implementing and fixing cost, Critical findings) show `-`, as `measure_show.ratio` gives for a 0 base. |
| `git status --porcelain` | only `?? .shop/records/`: the record, not committed |
| Text in the record | Not one of `batch-1 review 1`, `Findings file:`, `adversarial` or `work abandon` (the defect's text) is in the record |

The record is `/home/vscode/.claude/jobs/7e9ba079/tmp/smoke7/repo/.shop/records/measurements/2026-11-05-batch-1.md`.
It is not committed.

**Not met: "this session's requests inside the window are `planning`."** This implementer is itself a subagent of a
main session, so its rows carry an `agentId`. Its first request was before the batch started, so D4 leaves it out
entirely. That is why planning shows 0. For the same reason, this worktree's `project_dir` does not hold the
reviewer's transcript. Claude Code writes every subagent of a session under the main session's directory,
`-home-vscode-shopsystem-bdd/<session>/subagents/`. So `--sessions` named that directory. In the workflow the plan
designs for, `work batch` runs from a main session in the base checkout and the default directory holds it, but that
was not what this run had.

## Commits

| Task | Commit | Done | Verified |
|---|---|---|---|
| 1 | `8212c6f4` | `measure_cost.py` (D5: table, longest key, cache writes by TTL, overrides refused naming the key, zero usage free, unpriced None) and `measure_batch_read.py` (D2, D4, D6: requests counted once, writes by TTL, meta files, `project_dir`); the test helpers; 2 CLAUDE.md rows | RED: `No module named 'measure_cost'`. 13 tests pass; with measure tests and batch-measurement, 37 pass. Mutations: sum not max fails the request-in-several-rows test; 1 h at 1.25 fails the one-hour test; shortest key fails the dated-model test. Suite 1415 / 8 xfailed. |
| 2 | `4030162f` | `measure_batch_sessions.py`, `measure_batch.py`, `measure_batch_show.summary`, `measure_write` taking any name and a summary, `measure batch`; `telemetry_handlers.py` (r1, r2), `test_telemetry.py` on `bind_all`; telemetry `unbuilt: [r3, r4]` and its Implementation section; CLAUDE.md rows | RED: `No module named 'measure_batch'`. 19 tests pass. Telemetry `2 passed, 2 xfailed`; batches, supervision and batch-measurement unchanged (117 passed). Mutations: an observation counted as a defect; no window filter; no D6 rule 3 (3 role cases and the cost-by-role test); r2 left unbuilt → `XPASS(strict)`. Suite 1436 / 6 xfailed; generate exit 0; `model check` at baseline. |
| 3 | `b18dd3e3` | `measure_defect.py` (D11), `measure defect`, `after_merge` in the figures, the r3 handlers, telemetry `unbuilt: [r4]` and its D11 bullet, a CLAUDE.md row | RED: no `measure_defect`. 8 tests pass; telemetry `3 passed, 1 xfailed`. Mutations: accepting `abandoned` fails the abandoned case; numbering by count fails the next-defect test. Suite 1445 / 5 xfailed. |
| 4 | `981ca30f` | `measure_batch_show.resolve`, `show` and `compare`; `measure_show` handing a batch's figures over and refusing a mixed pair; `compare` taking batch names; `FIGURES` and `write_measurement` in the helpers; the r4 When; telemetry `unbuilt: []`, its D12 bullet and `## Not yet` | RED: 5 of 6 fail (`no measurement at batch-2`, no `resolve`); the r21 pin passes, as it pins old behaviour. 32 pass with telemetry `4 passed` and batch-measurement's 22. Mutations: the oldest record; a mixed pair let through. Suite 1452 / 4 xfailed. |
| 5 | `c59fe465` | 0078 and 0079; 0060's frontmatter (`superseded`, no tier, no `enforced_by`); the index regenerated; telemetry's `rests_on` and `## Not yet`; analyzing-a-batch, building-a-batch and shaping-items; the README bullet; the pinned totals (78; 28/48/2; 4/15/9; 9 judgement) | RED: 8 fail. The guard "an initiative is still measured" passed before. After: 45 pass; `decisions --check` 4 hold; `model check` 53/16/19/0. Mutations: 0060 keeping its tier fails the totals test (and two more); `telemetry#r9` gives 20 unresolved. Suite 1459 / 4 xfailed; logic 11; lexicon 401/0. |
| 6 | this commit | Step 1, every Step 2 figure, the smoke run, this report, the records index row, every box ticked | As in Final state |

## Deviations

Each is a ruling, decided by the implementer; revisit.

1. **Requests are counted once by `request_key` across files, not per file** (Task 1). This way a forked or resumed
   transcript that repeats a request does not double its cost. If two files ever share a request id for different
   requests, they would be merged.
2. **The scenario's review record gives its `fix now` finding a body** (Task 2). `batch_findings.parse` refuses a
   `fix now` finding with no text, so D13's body `""` could not be read back.
3. **`sessions_found` counts the `*.jsonl` files under the directory** (D2's "holds no transcript"), not the sessions
   counted. A directory whose transcripts all fall outside the window shows an empty sessions table, with no "no
   transcripts" line.
4. **`defects.per_item` and `goals` are computed from Task 2 on**, from the review's defects. Task 3 added
   `after_merge`. The figures also end with `date`, as `measure initiative`'s do.
5. **D6 rule 3 accepts any `batch-<n>`** in a description, not only the batch being measured.
6. **`findings_by_triage` gives every triage**, 0 included, like `findings_by_grade`.
7. **`scripts/measure`'s old `# noqa: E402` markers are removed** (RUF100), so `tools check` is clean on the changed
   file.
8. **`measure defect` refuses in this order** (Task 3): an empty `--says`, then an item in no batch, then one refusal
   that names both the item's status and its batch's (`b2 "Exit" is in-batch in batch-1, which is in-review`). This
   lets each of D11's cases name its word. The command holds `batch_git.locked` while it reads and commits.
9. **Two test cases go further than the plan says** (Task 3), so that the plan's mutations can turn them red:
   - In the abandoned case, b1 is written `delivered` by hand after the abandon, so only the batch's status refuses
     it. Otherwise the mutation could not turn it red, since abandon returns items to `ready`.
   - The next-defect test removes `defect-1.md` with `git rm` itself and expects `defect-3.md`.
   - batch-2 in the own-batch test is written by hand with `batch_plan.render`.
10. **`FIGURES` and `write_measurement` live in `tests/scripts/measure_batch_testing.py`** (Task 4). The r4 handler
    loads that helper by path, since a scenario handler cannot cleanly import a test module.
11. **A batch measurement is recognised by its keys `batch` and `cost_by_role`** (Task 4). In `compare`, the findings
    rows are named `<grade> findings`. In `show`, a subagent is named `<session>/<agent>`.
12. **`model decisions` prints `wrote spec/decisions/index.md` on every run** (Task 5). It has no "is current" message
    for Step 4 to match.
13. **analyzing-a-batch's report changes its sections** (Task 5). "Findings and defects" and "Items parked" replace
    the work-item tables, to match step 3's three judgements. The defect bullet of shaping-items is in its Overview.
14. **The smoke run** (Task 6) differs in three ways:
    - the reviewer's findings file was saved from its reply, since the harness refused a subagent's Write;
    - review 2 was a stand-in written by hand;
    - `--sessions` named the main session's directory, not this worktree's `project_dir`, and planning measured 0, as
      the smoke section explains.

## D1-D19

| | Kept or changed |
|---|---|
| D1 | Kept: committed on `workflow-simplification`, not pushed |
| D2 | Kept. The smoke run showed a gap: a session that is itself a subagent has its transcripts under the main session's directory, not under its own working directory's (open problem 3) |
| D3, D4 | Kept (Deviation 1: one request across files) |
| D5 | Kept: the table, `AS_OF = "2026-10-06"`, writes 1.25× and 2×, overrides refused naming the key |
| D6 | Kept (Deviation 5) |
| D7 | Kept (Deviation 6) |
| D8, D19 | Kept |
| D9 | Kept, with `date` at the end (Deviation 4) |
| D10 | Kept. `changed_lines` is over the last review's range only, so after a fix loop it is the fix's size (2 lines in the smoke run), not the batch's |
| D11 | Kept (Deviation 8) |
| D12 | Kept (Deviation 11) |
| D13 | Kept (Deviations 2, 10) |
| D14-D17 | Kept |
| D18 | Changed in its means (Deviation 14). A real reviewer was measured: $0.28, 36 s session time, 5 requests. |

## Open problems for plans 8-9

1. Plan 9 retires `measure initiative`, batch-measurement and `batch-analyst`, and rewrites the glossary's `measure`
   actor (D17).
2. The price table is dated (`prices_as_of` 2026-10-06) and kept by hand (D5).
3. **The default sessions directory misses a session that is a subagent.** Claude Code writes a subagent's
   transcript under its main session's directory. A batch driven from a subagent, as in this run, needs `--sessions`.
   Also, every other session in the same project directory inside the window counts as planning (D2, D4), and
   `--sessions` is the way round that too.
4. **`changed_lines` is the last review's range** (D10). After a fix loop it measures the fix, not the batch. It may
   be wanted over `forked_from..head`.
5. **A subagent's Write was refused by the harness** ("Subagents should return findings as text"). If `pr-reviewer`
   runs as a subagent of a subagent, building-a-batch may need to save the findings file from the reply.
6. Plan-5 D21 (recurring findings) and D23 (the third-review park) wait for real batches' figures.
7. The end-of-branch review of this plan (`plan-7-review.md`) is still to be run, by a separate reviewer, as the plan
   says.

## Files

- New:
  - scripts: `scripts/measure_cost.py`, `measure_batch_read.py`, `measure_batch_sessions.py`, `measure_batch.py`,
    `measure_batch_show.py`, `measure_defect.py`;
  - scenario handlers: `tests/scenarios/telemetry_handlers.py`;
  - script tests: `tests/scripts/measure_batch_testing.py`, `test_measure_cost.py`, `test_measure_batch_read.py`,
    `test_measure_batch.py`, `test_measure_defect.py`, `test_measure_batch_show.py`, `test_skill_analyzing_a_batch.py`;
  - decisions: `spec/decisions/0078-measure-a-batch.md`, `0079-a-knob-is-changed-by-a-decision.md`;
  - this report.
- Changed:
  - scripts: `scripts/measure`, `measure_show.py`, `measure_write.py`;
  - tests: `tests/scenarios/test_telemetry.py`, `tests/scripts/test_decision_checks.py`,
    `test_skill_building_a_batch.py`, `test_skill_shaping_items.py`;
  - spec: `spec/capabilities/telemetry.md`, `spec/decisions/0060-measure-an-initiative.md`, `spec/decisions/index.md`;
  - skills: `skills/analyzing-a-batch/SKILL.md`, `building-a-batch/SKILL.md`, `shaping-items/SKILL.md`;
  - docs and records: `README.md`, `CLAUDE.md`, `.shop/records/README.md`, `plan-7-telemetry.md` (boxes ticked).
