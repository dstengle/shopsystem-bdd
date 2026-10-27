# w210 research: supervision r135 and r136

Method. `tools tests-of`/`untested`: no map (`tools: no map`); I made none, so test counts are `by search`. `tools refs` answers 0 for `workqueue_request.request` and `Changes.write_proposals`: `scripts/work` has no .py name and `self.` calls are not followed; counts are `by search`. `tools size --limit 300` printed nothing: no tracked Python file is over 300. Pytest here runs with `--work-item w210` in force (the plugin's error names it), so only w210's accepted scenarios collect; other scenarios cannot be run.

## 1. Why each scenario is red today

**r136**, features/supervision.feature:1163. Command `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_formulated_capabilityproposal_whose_integrate_round_raised_..._not_delivered"` (run). Fails with StepDefinitionNotFoundError on the Given at line 1165 ("i1 is started and fulfils the request q1, and i1's capability-proposal p1 is formulated ... and i1's capability-proposal p2 is formulated, its adds naming other#r4"). Missing: a step for two proposals; supervision_proposal_steps.py:21 `formulated` handles one and writes `DIR/p1.md` only.
Undefined after it (read; pytest stops at the first): line 1166 (p1 "written by an integrate round that gave the lines ... into the upstream catalogue", p2 "gave no lines"); line 1167 (q2 "in catalogue ... raised by i1 for q1 and is awaiting-upstream": no step names a `catalogue` upstream); line 1170 ("`work add` drafted no work-item part of p1": the existing `two_drafted`, proposal_steps.py:73, asserts other text).
Code missing (read): `scripts/supervise_draft.py` `Drafts.draft_proposals` (77-97) drafts one work-item per capability of every `formulated` proposal and reads no record. Nothing reads whether a raised request is delivered: `workqueue_list.py` `waiting` (25-37) reads `.shop/work/<i>/raised.jsonl`, which nothing writes.

**r135**, features/supervision.feature:1445. Same command form (run). Fails with StepDefinitionNotFoundError at line 1448 ("the integrate round for i1 gives DONE with a change list that adds thing#r4 on thing, and gives the lines of a request into the upstream catalogue"). Line 1447 matches supervision_rounds_steps.py:153 (read). Undefined after (read): line 1451 (`work request` run "for the upstream catalogue", one line) and 1452 (the request "raised for q1 and gives the delegation").
Code missing (read): `supervise_rounds.py` `Rounds.run_round` (101-204), integrate branch, never reads the result's `requests` key (no reader under scripts/supervise*; supervise_brief.py:14-17 only asks for it) and never calls `workqueue_request.request`. The `work` CLI has no `--raised-for` (scripts/work:143-149); `workqueue_request.request` (87) has no raised-for parameter. The delegation source exists: `supervise_answers.py` `Answers.delegation` (36-45), by search.

## 2. What the system answers today

Probes: `.shop/scratch/w210-1-research/probe_work_request.py` and `probe_work_request_lines.py`, run `python3 -m pytest -q -n 0 -s <path>` (run; 7 cases, all passed as probes, each printing what came back). Each runs `scripts/work --root <scratch upstream> request ...` from the scratch upstream repo, with spec/index.md id `bounded-context/ex.com/prod/catalogue`, asker `bounded-context/ex.com/prod/ctx-a`, and the line "When a book is listed, the catalogue shall give its edition." (EARS form) in `lines.md`.

| case (the r135/r136 Givens against today's `work request`) | came back | run |
|---|---|---|
| `--raised-for q7` | exit 2, "work: error: unrecognized arguments: --raised-for q7" | run |
| `--thread i1 --delegation "Please get everything delivered."` | exit 0, q1 written: `part_of: i1`, `delegation: "..."`, `status: open`, `turn: upstream`; no raised field | run |
| `--source <asker>` | exit 0, `source: [asker]` | run |
| neither `--source` nor `--thread` | exit 1, "names neither an origin (--source) nor a job-thread (--thread)"; no requests dir | run |
| `--delegation "   "` (blank) | exit 1, "the delegation is empty" | run |
| a line not in EARS form | exit 1, "line 1 is not in the strict form model check holds" | run |
| EARS line, `--thread i1` | exit 0, commit "work request: q1" touching only requests/q1.md | run |
| `--lines lines.md` run from a directory other than the upstream | exit 1, "the file lines.md does not exist" (the lines path is taken from the process cwd, not `--root`) | run |

Read, not probed: `draft_proposals` has no check, so a formulated p1 gets its work-items whatever any record says. `waiting()` reads only the local record's fields (upstream, request, initiative, status): no proposal name. The status of a raised request is never updated here: workqueue_list.py docstring (4-6) "the upstream is never reached"; `work resolve` sets `delivered` only in the upstream's request (workqueue_request.py:166-186).

## 3. Old assumptions

| place (file:function) | what it does today | what r135/r136 make of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_draft.py:Drafts.draft_proposals (77-97) | drafts one work-item per capability of each formulated proposal | r136: skip the proposal whose raised request is not delivered | by search: supervision_proposal_steps.py:73 `two_drafted`; feature line 1155 scenario (not collectable here) | by search |
| supervise.py:Run.commit (100-111) | commits the item file, `runs/<name>`, log.jsonl and `also` only (r7) | a raised record written by work run must go in `also` of a commit, or be left uncommitted, which the next `check` refuses (supervise.py:88-92) | by search: integrate and move tests (not run) | by search |
| supervise_rounds.py:Rounds.run_round, integrate branch (139-204) | reads the change list, writes proposals; ignores `requests` | r135: raise each `requests` entry after the merge (line 129) | by search: spec_integration_steps.py approved_note (49-57), Thens (132-144) | by search |
| workqueue_request.py:request (87-117) | `--thread` writes `part_of`, `--source` writes `source`; no raised-for | r135 needs raised-for (requests r29) or a thread/source to be written | by search: tests/scenarios/test_requests.py raised-for scenario (not collectable here) | by search; probe rows 1-4 |
| workqueue_list.py:waiting (25-37) | reads `raised.jsonl`, last status per (upstream, request) | r136 reads it; the record has no proposal field to match p1 | by search: tests/scripts/test_workqueue_list.py:17, 50-55 | by search |
| workqueue_done.py:_holds (22-38) | initiative done waits on requests kept in this context, asker this context | raised requests are kept in the upstream, so not seen; r105 says "kept in this context": consistent, no change | none by search (supervision_done_steps.py not read) | read |
| scripts/model.lp:259 (v17), model_requests.py | a request in neither a thread nor an origin is flagged; no `raised` field is read anywhere in scripts/model*.py | a request written with `--raised-for` and no thread or source is flagged | by search: features/design-model-check.feature:864 (not run) | read (grep "raised" over scripts/*.py) |
| workqueue.py:committed (268-282) | commits a request in the repository it is written in; no push | r135 writes into the upstream's repository (a sibling checkout, as spec-integration's ../billing-ctx) | by search: test_requests.py (not run) | read |

## 4. Tests the requirements make impossible to keep

Not via `tests-of` (no map). By search, then read:
- spec_integration_steps.py `approved_note` (49-57) gives the round `requests` to billing (`../billing-ctx`). Once r135 is built, the round's end raises that line into billing; the `work run` may then end in an error the scenario does not expect (no raised-for in the CLI; or a thread or source written). Not run here: the scenario is not collectable under `--work-item w210`. Possibly breaks; unverified.
- supervision_proposal_steps.py `two_drafted` (73-79) and the feature line 1155 scenario: keep passing under r136, as no raised record exists for p1 (read).
- supervision_integrate_steps.py `proposals_written` (140-154): asserts the integrate commit's added `.md` files under `.shop/work/i1/`; a `raised.jsonl` is not `.md` and so passes (read).
- tests/scripts/test_workqueue_list.py (17, 50-55): record format unchanged by the plan (read): keep.
- tests/scenarios/test_requests.py raised-for scenario: already red (probe row 1); r29 is not in w210's accepts.
Verified sound (read): `Drafts.draft_proposals`' `have` set and `Run.commit`'s path list need no change for the existing tests.

## 5. A step the work-item skips

- Writing this context's record (`.shop/work/<i>/raised.jsonl`): no existing way writes it (read). Its only readers are r136's gate and `work list` (work-queue r39).
- Its status update to `delivered`: the existing way, `work resolve` (workqueue_request.py:166-186), sets it only in the upstream. This context never learns. Effect: r136 never releases unless a step updates the record (read).
- The raise's commit lands in the upstream's repository through `workqueue.committed` (workqueue.py:268-282): no push, no push verification. The by-hand `work request` does the same (read); r35 covers only this context's branch.
- The round's merge (supervise_rounds.py:129) lands before the raise. The lines check of `request()` (probe row 6) then refuses a non-EARS line after the round's commit is in (read). The change list is written after the merge too (lines 139-204).
- A blank delegation (probe row 5) refuses the raise: a fulfilled request with a blank delegation fails the same way (read).

## 6. Defects

**D1. `--raised-for` refused as an unknown option.** requests r29 and r44 and features/requests.feature:61 take it.
Repro: `python3 -m pytest -q -n 0 -s .shop/scratch/w210-1-research/probe_work_request.py -k raised_for` (run) → `work: error: unrecognized arguments: --raised-for q7`, exit 2.

**D2 (from the ledger, not run by me).** w208's research reported: `work list` prints None for a missing status; `work show` of an initiative directory without initiative.md says no work-item; `work list` stops on a malformed raised.jsonl where `list --json` ignores it. Not verified here.

## 7. The file set

Production:
- scripts/supervise_rounds.py (229 lines) — integrate branch: raise each `requests` entry after the merge.
- scripts/supervise_draft.py (122) — r136 skip in `draft_proposals` (read: 77-97).
- scripts/supervise.py (284, room 16) — `Run.commit` `also` for the record; call site (read: 100-111).
- scripts/workqueue_request.py (186) — `request()` takes raised-for (requests r29) (read: 87; probe row 1).
- scripts/work (181) — `--raised-for` on the request subparser (143-149) and `cmd_request` (71) (read).
- scripts/workqueue_list.py (84) — `waiting` reads the record, if it gains a proposal field (read: 25-37).
- new scripts/supervise_raise.py — the raising and the record: a new concern (CLAUDE.md: new module and module-map row).
- CLAUDE.md — module-map row for the new module (read: module map).
- scripts/model.lp, scripts/model_requests.py — only if a raised-for request must pass v17 (read: model.lp:259).
Tests:
- tests/scenarios/supervision_proposal_steps.py (152) — two-proposal Given, the integrate-given Given, the "no work-item part of p1" Then.
- tests/scenarios/supervision_integrate_steps.py (201) — Given with the catalogue lines; Then that `work request` was run.
- tests/scenarios/supervision_request_steps.py (29) — q2 in catalogue raised by i1, awaiting-upstream.
- tests/scenarios/test_supervision.py (266, room 34) — import line for any new step module.
- tests/scenarios/supervision_raise_steps.py — new, if the steps go in their own module.
- tests/scenarios/spec_integration_steps.py (155) — if its `approved_note` raise changes the outcome (read: 49-57).

Modules on the path, edited or not (line count, room to 300):
- scripts/supervise_worker.py 256 (room 44) — `git`, worker helpers the round uses.
- scripts/supervise_answers.py 146 (room 154) — `Answers.delegation`, reused for the delegation.
- scripts/supervise_brief.py 203 (room 97) — the `requests` ask (unchanged).
- scripts/supervise_change.py 126 (room 174) — `write_proposals`, the proposal name the mapping may need.
- scripts/workqueue.py 294 (room 6) — `committed`, `entry`; no edit fits without a split.
- scripts/workqueue_done.py 73 (room 227) — `_holds` (unchanged).

## Readings the plan must choose

1. Record and r7. (a) The record is written and committed with the round's commit (needs `also`; r7's "nothing else" is widened). (b) Not committed: `check` refuses the next run (supervise.py:88-92). Only (a) works.
2. Mapping of a raised request to its proposal, for r136. (a) A `proposal` field on each raised.jsonl line (the record then carries more than work-queue r39 describes). (b) The round's stage directory (`runs/<p>/<k>-integrate/result.json` with `requests`) plus the request id from `work request`'s stdout. Both readings are open.
3. Release of r136. (a) Something re-reads the upstream's request status and updates the record (not in any spec). (b) The record is updated when `work list` or a `work run` next runs. Neither is specified.
4. The upstream's root. (a) The directory above the upstream's `spec/`, from spec/index.md's `## Upstreams` path (supervise_brief.py:107-115), so `work --root` can reach the upstream's `work request`. (b) Raise into this context's own queue, leaving the upstream's request unwritten. Only (a) reaches the upstream.
5. `--raised-for` (requests r29) is not in w210's accepts. Either another work-item delivers it first, or w210 depends on it. The coordinator should say which.
