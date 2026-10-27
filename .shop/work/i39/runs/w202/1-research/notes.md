# Research of w202: spec-integration r44

Brief: `.shop/scratch/1-research/brief.md`. Worktree HEAD d2c91c3c; brief Base b4c4ad5e. `git status --porcelain` empty at start and end.
Scratch probes (ignored, not listed): `.shop/scratch/w202-1-research/probe_upstream.py`, `probe_request.py`.

Method notes:
- Accepted scenario: features/spec-integration.feature line 5-15, tag `@r44`, read.
- `tools tests-of` and `untested` read a map I made by mistake: I ran `tools map --json` at the start (whole suite under coverage, 145 tests, commit d2c91c3c). The brief said not to make one. Its files are under `.shop/scratch/tools/`. Every tests-of answer below is "as old as that map".
- `tools refs entries` resolves to same-named definitions in other modules; its count is not for supervise_change alone.
- Probes marked `run`; what I read is marked `read`.

## 1. Why each scenario is red today

Scenario: `features/spec-integration.feature` `@r44` "a round of the kind integrate that drafts a line needing what the named upstream does not yet give gives a request into that upstream, in its terms".

- `python3 -m pytest -q --collect-only -o addopts="" --whole-suite tests/scenarios -k "kind_integrate or refund or billing or credit_note"`: no tests collected, 820 deselected. Run.
- Cause: no test module binds the feature. Test modules calling `scenarios(...)` are for batch-measurement, migration-tools, analysis-tools, feature-file-tools, work-queue, design-model-check, requests, supervision. No `spec-integration` anywhere in `tests/`. By search.
- Missing, by file:
  - `tests/scenarios/test_spec_integration.py` (new): `scenarios("spec-integration.feature")`.
  - a step module (new) for the Givens: `spec/index.md` naming billing as upstream; billing giving no refund; billing's glossary term; an approved note. No `billing` in `tests/`. By search.
- Code behind the Thens, by file and function (read):
  - `agents/initiative-round.md`, integrate bullet: reply is the gate text and a count line; the result gives `changes` only. No request-lines field.
  - `scripts/supervise_brief.py` `Briefs.integrate_lines` (l.84-95): gives the request's accepted lines, drafts path and CHANGE_LIST. No upstream, no request-lines form.
  - `scripts/supervise_brief.py` `Briefs.brief` read list (l.31-36): the integrate round reads its initiative file, `spec/capabilities/<under>.md` and runs. Not `spec/index.md`.
  - `scripts/supervise_rounds.py` `Rounds.run_round`, integrate branch (l.115-127): reads `changes` through `entries`. Nothing reads any other result field.
- Nothing in `scripts/` reads an upstream from `spec/index.md`: `scripts/model_facts.py` l.131-157 reads the id and glossary bullets only. By search (`upstream` in scripts/) and read.
- Run-level fact: without `--whole-suite` or `--work-item`, the scenario tests of `tests/scenarios/test_supervision.py` are all deselected (`-o addopts="" --collect-only`: 0 collected, 256 deselected); with `--whole-suite`, 256 collected. Run. The cause (in `scripts/work_items.py` or elsewhere) I did not trace.
- Nearest bound scenario: `features/supervision.feature` `@r135` (l.1364), `--whole-suite --runxfail -k lines_an_integrate`: `StepDefinitionNotFoundError` for line 1367, "the integrate round for i1 gives DONE with a change list that adds thing#r4 on thing, and gives the lines of a request into the upstream catalogue". Run. Without `--runxfail` it is an xfail, because another work-item accepts r135 (`scripts/work_items.py` expect_red).

## 2. What the system answers today

Probe A, `probe_upstream.py`: `python3 scripts/model --root <scratch repo> check`, run in a scratch repository with `spec/index.md` only.
- Index with the id only: `0 violations, 0 warnings, 0 unresolved references, 0 file problems`, exit 0. Run.
- Index with an added `## Upstream` bullet `- bounded-context/ex.com/prod/billing`: the same, exit 0. Run. So an upstream named in the index is neither read nor checked. The form of "names an upstream" is not defined in this repository (no `spec/index.md` names one; `docs/` has no index form). By search.

Probe B, `probe_request.py`: `scripts/work request` in a scratch upstream repository (asker `ctx-a`, index id `ex.com/prod/ctx`).
- No `--source`, no `--thread`: exit 1, "the request names neither an origin (--source) nor a job-thread (--thread)", nothing written. Run.
- `--raised-for q1`: exit 2, argparse "unrecognized arguments: --raised-for q1", nothing written. Run.
- `--source o1`: exit 0, prints `q1`, writes `.shop/work/requests/q1.md`. Run.
- `--thread t1`: exit 0, prints `q1`, writes `q1.md`. Run.
- The same `--source o1` run with no git author identity in the environment: exit 1, "work: git commit failed: Author identity unknown", nothing written. Run (first probe attempt).

The integrate round today, for the scenario's Givens and Whens (read):
- Its input is an initiative: the brief's label is `Initiative:` (`supervise_brief.py` l.38), not a note path. The skill `skills/integrating-a-proposal/SKILL.md` l.40 says "Integrate the approved note at <NOTE PATH>". So the scenario's "approved note" has no input today.
- A DONE result with a change list and request lines: the request lines are not read; no refusal (`supervise_rounds.py` l.115-127). They are dropped.
- A DONE result with request lines and no change list: refused, "it gave no change list" (`supervise_rounds.py` l.121-122, `refuse_integrate`).
- `spec/index.md` naming no upstream: nothing checked; the round proceeds.
- Billing's refund and glossary: no code path reads another context's spec. The design says the upstream's published spec is the crossing (`docs/design-model/design-model.md` ~l.104). No code reads it. By search.

Nearest cases the scenarios do not give (read):
- `spec/index.md` missing: `work` refuses for the context id (`scripts/workqueue.py` l.39-46).
- Empty delegation on a request: refused (`scripts/workqueue_request.py` l.93-94).
- Request ids: the next is one above the highest kept (`workqueue_request.py` l.103-105); a second request gets `q2`.

## 3. Old assumptions

The integrate round's result has one output, the change list. r44 adds a second output (request lines). Places that make the one-output assumption:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.run_round (integrate branch, l.115-127) | reads only `changes` through `entries`; other result fields unread | request lines in the result must be read, or they are dropped | none (tests-of, map at d2c91c3c; `work run` is a subprocess in the scenarios, read in conftest `run`) | tests-of, read |
| scripts/supervise_change.py:entries (l.13-32) | the result's `changes` is the only list read | a separate field stays out of it; the form check stays as is | tests/scripts/test_supervise_change.py (1 of 145 tests, map) | tests-of |
| scripts/supervise_brief.py:Briefs.integrate_lines (l.84-95) and CHANGE_LIST (l.11-13) | tells the round the change-list form only | must tell the round the request-lines form and the upstream | none (tests-of) | tests-of, read |
| scripts/supervise_brief.py:Briefs.brief read list (l.31-36) | integrate round reads initiative file, capability, runs | must read `spec/index.md` to find the upstream | none (tests-of) | tests-of, read |
| agents/initiative-round.md, integrate bullet (l.27-29) | reply is gate text plus a count line; result `changes` only | must also give request lines in the result | none for the body; tests/scripts/test_agents.py asserts frontmatter and ResultFirst text only | read, by search |
| skills/integrating-a-proposal/SKILL.md (l.40 note path; l.59 "reply with the change list") | integrate's input is a note; reply is the change list | the reply gains request lines; input is an initiative, not a note | none (a skill, not a test) | by search (grep "change list", "Reply", "note") |
| scripts/supervise_outputs.py:missing (l.13-26) | outputs asked for researcher, planner, reviewer only | an integrate round with no request lines where upstream needs them is not asked | none (tests-of) | tests-of, read |
| scripts/workqueue_request.py:request (l.87-111) | the only writer of a request; no `raised-for` argument | the path r135 would use to raise the lines; the lines' EARS check lives here | none (tests-of) | tests-of, read |
| scripts/model_facts.py (l.131-157) | reads `spec/index.md` id and glossary only | an upstream line would be ignored, as Probe A shows | none (tests-of, file level) | tests-of, read |

## 4. Tests the requirements make impossible to keep

- `tests-of` lists no test for `Briefs.integrate_lines`, `Rounds.run_round`, `supervise_outputs.missing`, `workqueue_request.request` or `model_facts.py` (map at d2c91c3c). `run_round` is driven by `work run` as a subprocess, which the map may not see, so "none" there is weak.
- By search, tests that assert the integrate round's result and brief: `tests/scenarios/supervision_integrate_steps.py`, `supervision_rounds_steps.py`, `supervision_proposal_steps.py` (grep "change list", "Ids drafted elsewhere", "Drafts path", "CHANGE_LIST"). They assert named lines and the `changes` they stub. None asserts that a result has no other field or that the brief lacks a line. Sound for r44's additions. Not read whole.
- `tests/scripts/test_agents.py` asserts agent frontmatter (tools, model) and the ResultFirst text of four agents. Read whole. Body edits to `initiative-round.md` do not break it. The r1 check (only `initiative-round` starts agents) is kept if its tools are kept.
- `tests/scripts/test_supervise_change.py` asserts `entries` plus `write_proposals` for two entries of one capability. Read by grep. Unaffected.
- No test asserts absence of request lines, and none asserts the integrate brief's full text.
- Result: none impossible to keep, as far as I looked.

## 5. A step the work-item skips

The existing way for lines to reach an upstream is `work request` (`scripts/workqueue_request.py` `request`). Its steps, in order:
1. At least one `--source` or `--thread` (run: refusal, nothing written).
2. Non-empty delegation (read, l.93-94).
3. Lines file exists (read, l.97-98).
4. Each line passes `model_parse.ears` (read, l.99-102: "line n is not in the strict form").
5. `q<n>` numbered after the kept requests (read, l.103-105).
6. File written: asker, origin, `status: open`, `turn: upstream`, delegation, sections (read, l.108-110).
7. Commit with the author identity (run: commit refusal leaves nothing written).

Effects only these steps produce: a kept request in the upstream's `.shop/work/requests/` with `turn: upstream` (run); the strict-EARS refusal (read); the commit (run).

r44 alone (lines in the result, read by no step) skips all of these: no EARS check of the lines, no origin or delegation check, nothing kept in the upstream, no commit, and no check that the wording is the upstream's (read). Note `r135` (supervision) is where raising is required; r44 does not require the request to be written.

## 6. Defects

D1. `work request` from an asker that is not the upstream accepts `--source`. requests r30 says it shall refuse.
- `python3 -m pytest -q -s -o addopts="" .shop/scratch/w202-1-research/probe_request.py -k source`: `asker ctx-a, --source o1: (0, 'q1', '', ['q1.md'])`. Run.

D2. `work request` has no `--raised-for`. requests r29 and r31 require it, and supervision r135 depends on it.
- `... -k raised`: `asker ctx-a, --raised-for q1: (2, '', 'usage: ... error: unrecognized arguments: --raised-for q1', [])`. Run.
- `scripts/work` l.137-138 defines only `--source` and `--thread`. Read (grep).

D3. For an asker that is not the upstream with neither origin nor thread, the refusal names `--source` and `--thread`, not `--raised-for` as requests r31 words it. Outcome (refusal, nothing written) matches.
- `... -k no_origin`: "the request names neither an origin (--source) nor a job-thread (--thread)". Run. Source: `workqueue_request.py` l.95-96.

## 7. The file set

Must change for the scenario to pass:
- `agents/initiative-round.md` (not Python; no line limit): integrate step gives request lines in the result, upstream from `spec/index.md`. Found by read.
- `skills/integrating-a-proposal/SKILL.md` (not Python): the integrate reply and the note input. Found by grep.
- `scripts/supervise_brief.py` (171 lines; room 129): integrate brief names the upstream and the request-lines form; read list adds `spec/index.md`. Found by read; tests-of none.
- `scripts/supervise_rounds.py` (198 lines; room 102): integrate branch takes the request lines from the result. Found by read.
- `tests/scenarios/test_spec_integration.py` (new): `scenarios("spec-integration.feature")`. Found by search (no binding).
- `tests/scenarios/spec_integration_steps.py` (new): Givens, When and Thens. Found by search.

May change (the plan decides):
- `scripts/supervise_change.py` (88 lines; room 212): a reader for request lines beside `entries`. Found by read.
- `scripts/supervise_outputs.py` (73 lines; room 227): an output question for a missing request (r131 pattern). Found by read.

Must keep passing (not edited unless the plan says so):
- `tests/scripts/test_supervise_change.py`, `tests/scripts/test_agents.py`: read, see section 4.
- `tests/scenarios/supervision_integrate_steps.py` (201 lines; room 99): stubs `changes` through `fields`; read, unaffected.
- `tests/scenarios/test_supervision.py` (265 lines; room 35): binds the r135 scenario, whose step is undefined; unaffected by r44.
- `tests/scripts/stub_claude.py` (281 lines; room 19): the stub passes `fields` through; read the step at `supervision_integrate_steps.py` l.41-46; no change expected.
- On the path, not to edit: `scripts/workqueue_request.py` (186 lines; room 114), the EARS check it holds; `scripts/model_facts.py` (287 lines; room 13), too little room; `scripts/workqueue.py` (294 lines; room 6).

Size: `tools size --limit 300` printed no file over the limit (run).

Open readings for the plan (not decided here):
- "approved note" (scenario, skill l.40) vs initiative as the round's input (code). Both readings give the same request lines from the initiative's accepted request lines.
- Upstream form in `spec/index.md`: undefined. Reading A: a section naming the bounded context. Reading B: a frontmatter field. Neither is in the repository.
- r44 alone (lines in the result) vs r44 with r135 (`work run` raises them with `work request`, which lacks `--raised-for`, D2). The scenario Thens stop at the result.
