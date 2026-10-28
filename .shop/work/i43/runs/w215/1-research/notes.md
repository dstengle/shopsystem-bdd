# Notes: research of w215 (review r32, r33, r34)

Map: none (`tools: no map`). `tests-of` and `untested` unavailable; tests found by search (text) and `tools refs` where it applies. Accepted scenarios found by search of `features/`.

## 1. Why each scenario is red today

No accepted scenario (by search). `features/` has no `review.feature`; the `@r32`-`@r34` tags in other files (supervision, work-queue, requests, migration-tools, design-model-check) carry those capabilities' ids and are not counted. Review is a `guarantees` capability: a work-item of guarantees capabilities left with no test succeeds (read, scripts/work_items.py:156-164).

Run: `python3 -m pytest -q --work-item w215` (run): 176 passed, 1 skipped, 56 subtests, 4.22 s. Nothing red. Under `--work-item` the plugin keeps every non-scenario test (read, scripts/work_items.py:128-145), so these 176 are not review scenarios.

## 2. Old assumptions

Old: the branch reviewer runs the suite, its checks and its dry-run test itself (r9 retired; agent body and tools).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| agents/bdd-branch-reviewer.md:4 `tools:` | gives Bash to the branch reviewer | r32: it runs nothing (see conflict C1) | none (test_agents.py test_r2 reads this line, asserts only no Edit) | search |
| agents/bdd-branch-reviewer.md:31-39 "What you run" | reviewer runs suite once, each work-item's pytest, `tools check`, `tools size`, `features deprecated`/`bindings`, the dry-run test | r32: work run gives these; r34: verify from work run's suite run | none (no test reads the body) | search |
| agents/bdd-branch-reviewer.md:3 description | "runs the suite, the work-items' checks and the plugin's commands itself" | r32 contradicts | none | search |
| agents/bdd-branch-reviewer.md:29, 59 probes and observation reproductions | reviewer writes probes in scratch, reproduces by commands | r33: run-only behaviour is a finding with its test, marked not run, no reproduction | none | search |
| agents/bdd-branch-reviewer.md:35-37 "a check you did not run is not a check that passed" | reviewer runs each check itself | r32 + r6: a check work run did not give cannot be verified, so the review fails | none | search |
| agents/bdd-branch-reviewer.md:66 findings file `Suite`, `Checks` | sourced from reviewer's own runs | r7, r34: sourced from work run's records | none | search |
| scripts/supervise_worker.py:39 `TOOLS["review"] = READER` | one list for both reviewers: includes `Bash(python3 -m pytest*)`, `features`, `model`, `tools` scripts and git status/diff/log/show | r32: the branch reviewer gets none of the runs; the work-item reviewer (r13 of review) is not covered, so the list must split | none by test; supervision scenarios run it through the stand-in and assert no list for the review stage | read + search |
| scripts/supervise_worker.py:31-33 `PYTHON`, `STAGE_SCRIPTS`, `READER` | the pytest and plugin scripts a review session may run | as above | as above | read |
| scripts/supervise_review.py:64-71 brief text | names Initiative, Base, Head, Scripts; no run record, no run list | r32, r34: must carry work run's runs (supervision r154, r155; formulated in spec, not in code) | none in tests/scripts; scenario steps reach it through work run | read + search |
| scripts/supervise_review.py:47-94 `Reviews.branch_review` | starts the session with no run at the head | r34 depends on work run's branch-head runs (supervision r154); not implemented | none in tests/scripts; by search, scenario steps only | read |
| scripts/work_items.py:119-125 `pytest_configure` | exempts worker "the branch review" from the `--whole-suite` refusal | r32: no reviewer runs pytest, so the exemption serves no session | tests/scripts/test_work_items_worker.py:32-33 `test_the_branch_review_runs_the_whole_suite` (by search: only test of it) | read + search |
| spec/decisions/0053-the-v3-agents.md:28 table row | `bdd-branch-reviewer` has Read, Glob, Grep, Bash, Write | the decision lists Bash for the reviewer (see C1) | none (no test reads decisions; by search) | search |

Callers: `Reviews.branch_review` is called from scripts/supervise.py:231 and :237 (text search; `tools refs` reports 0 because the call is a method on self).

## 3. Tests the requirements make impossible to keep

By search (no map). Read: each file/test listed.
- tests/scripts/test_agents.py test_r2 (45-48): still passes without Bash on the reviewer. Sound.
- tests/scripts/test_agents.py test_r5 (62-68): reviewer model stays `opus`. Sound.
- tests/scripts/test_agents.py ResultFirst (78-88): branch reviewer not in its list. Sound.
- tests/scripts/test_work_items_worker.py test_the_branch_review_runs_the_whole_suite (32-33): still passes (plugin unchanged), but asserts an exemption r32 leaves unused. Not impossible; keep or remove is the plan's choice.
- tests/scenarios/supervision_then_workers.py given_tools (127-130): checks the researcher's list only. Sound.
- supervision step definitions with `plan["bdd-branch-reviewer"]` (supervision_review_steps.py:24, supervision_analysis_steps.py:20,41, supervision_proposal_steps.py:41,45, supervision_done_steps.py:22, supervision_faults_steps.py:156-159): stand-in plans give questions, notes or touch, no `run` list. Sound by search; not read in full.
- tests/scenarios/supervision_retire_steps.py:101-112 reads the branch review brief for ordering; not read. Likely sound.

Nothing that cannot pass. No currently-passing test asserts that the branch reviewer runs a command.

## 4. The file set

Must change:
- agents/bdd-branch-reviewer.md (77 lines; markdown, no line limit): tools line, "What you run", findings file per r32-r34.
- scripts/supervise_worker.py (256 lines, room 44): split `TOOLS["review"]` so the branch review gets no runs; work-item reviewer keeps READER.
- scripts/supervise_review.py (94 lines, room 206): brief carries work run's runs and the stage's list.
- tests/scripts/test_agents.py (88 lines, room 212): a test that the branch reviewer has no Bash (reading A).

Change if reading A of C1 or C2 is taken:
- scripts/work_items.py (164 lines, room 136): drop the "the branch review" exemption.
- tests/scripts/test_work_items_worker.py (33 lines, room 267): its last test goes with the exemption.
- spec/decisions/0053-the-v3-agents.md (36 lines, markdown): the reviewer's tools row.

On the change's path, not edited:
- scripts/supervise.py (293 lines, room 7; tight): calls branch_review at 231 and 237.
- scripts/supervise_merge.py (138 lines, room 162): `suite_record` (35-39), work run's whole-suite runner, per work-item at merge; reusable for r154's branch-head run (supervision's work).
- tests/scenarios/supervision_review_steps.py (102 lines, room 198): branch-review steps; not changed by w215.
- tests/scripts/stub_claude.py (281 lines, room 19): the stand-in; not changed by w215.
- spec/capabilities/review.md (52 lines): read; the text is the requirements.

Limit: CLAUDE.md, 300 lines for Python code and tests; markdown has none.

## Conflicts (both readings, for the plan)

C1. r32 ("runs nothing") against decision 0053's row (Bash in the reviewer's tools) and against the coordinator's ledger (q24, i44: the Bash tool removed; not yet applied).
- Reading A: r32 removes Bash. The agent's tools line, the decision row and test_agents change. The branch review's brief and stage list give it the reads only.
- Reading B: r32 governs conduct. Bash stays for read-only git (`git show`, `log`, `diff`), and the stage list still loses pytest and the scripts. Decision 0053 then needs no change, but r32 and the table disagree on what Bash is for.

C2. r34 ("from the suite run `work run` gave it") against the code. The only run work run makes now is the per-work-item suite at merge (supervise_merge.py:35-39). The branch-head run is supervision r154/r155 (spec, formulated, not in supervise_review.py).
- Reading A: w215 changes the agent's wording only; r34 is verified once supervision r154/r155 land.
- Reading B: w215 also requires the run's record to carry the randomized test's case count. The current `Suite: N passed, M failed at <hash> in <s> s` line does not carry it. The test must print its count into the output (question for the plan).
