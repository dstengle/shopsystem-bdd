# Notes: w169 (spec-integration#r43, round-ids-avoided)

Method: `tools refs` works (run). `tools tests-of` and `tools untested` refuse: "no map: make one with tools map" (run); I did not make a map. Tests are listed by search, marked `by search`. Scripts run from `/home/vscode/shopsystem-bdd/scripts`; probes import this worktree's `scripts/`, which is the same base.

## 1. Why each scenario is red today

No accepted scenario. `features/spec-integration*.feature` does not exist (Glob, run). The `@r43` tags in `features/` belong to other capabilities: `design-model-check`, `supervision`, `batch-measurement` (grep, by search).

Not red, by design: `spec/capabilities/spec-integration.md` has `group: guarantees`. `scripts/work_items.py:108` and `:114-131` exempt a work-item whose requirements are all guarantees when it collects no test. So `work run` passes w169 with no check (read). The previous session's run (`1-research`, turn limit) gave `collected 178 items / 178 deselected / 0 selected` for `tests/scenarios/test_supervision.py` with `--work-item w169` (its notes; not re-run here).

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n 0 .shop/scratch/w169-2-research/probe_integrate_ids.py` (run, 3 passed). Fixture in the scratch: request `q1` with lines 1 (accepted) and 2 (refused); `.shop/work/i25/supervision.md` and `.shop/work/i26/supervision.md`, each `adds: [supervision#r98]`. Called `Briefs.integrate_lines` (supervise_brief.py:66) with `{"fulfils": "request/x/q1"}`:

- `Request: q1`
- `Accepted lines of the request:` then `- 1. first line` (line 2 left out, as it should be)
- `Drafts path: .../fx/round/drafts`
- the change-list form: `{"capability", "adds", "changes", "removes"}`, ids `<capability>#r<n>` or `term/<term>`
- `mentions supervision#r98: False`: the other initiatives' drafted `supervision#r98` is not in the brief.

Nearest cases (same fixture, run):
- request `q9` missing: raises `Refused: there is no request q9 under .shop/work/requests` (workqueue_request.py:22).
- `fulfils` absent: raises `Refused: there is no request  under .shop/work/requests` (same refusal, empty id).

## 3. Old assumptions

The old rule: an added line takes one above the ids the capability has used or retired, counted in `spec/` and in this initiative's own drafted rounds. r43 adds ids that other initiatives' drafts add, which are not in `spec/` yet.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_brief.py:integrate_lines (66-76) | gives the request, its accepted lines, the drafts path and the change-list form; no other proposal's ids | must give the ids other initiatives' drafts add, per capability (or the round must read them) | by search: no test names it; the `work run` scenarios of features/supervision.feature (`given q1's lines 1 and 3`, :868, :1082) reach it; not run | refs (1 production caller, supervise_brief.py:38, 0 tests); read |
| agents/initiative-round.md:28 (kind integrate, Drafts path and change list) | gives the change-list form; says nothing of other drafts' ids | the round must be given them, or read them, and check its added ids against them | none (agent text) | read |
| skills/integrating-a-proposal/SKILL.md:23 (step 2) | the added rows take the next ids above the capability's lines, `retired` and this initiative's earlier drafted lines | also above the other initiatives' drafted adds | none (skill text) | grep, read |
| agents/capability-writer.md:18-21 | a new line takes one above every id the capability has used or retired | same, for the writer's numbering | none (agent text) | read |
| docs/capability-format.md:159-163 | the same rule, in the format doc | same | none (doc) | read |
| scripts/supervise_change.py:write_proposals (38-52) | writes one drafted proposal per capability with its `adds`; no check of ids against other proposals | a check, or the ids carried to the round, lands here or upstream | by search: features/supervision.feature:1133 and :1142-1150 (`@r92`: two proposals for one capability get different proposal ids, not line ids); not run | refs; read |
| scripts/model.lp:173-176 (v15b) with scripts/model_work.py:166-175 | v15b counts `req_id` facts, which an `adds` gives only when the id is retired (model_work.py:172-173); two proposals adding one live id raise no row | not changed by r43, but it is the only check of the collision, and it sees `spec/` only | none: tests/scripts/test_model_reading.py:96-103 has two proposals adding different ids (`thing#r1`, `other#r1`), not one id twice | grep `v15b`; read |

Not reached: whether the other initiatives' drafts are visible from a round's worktree. `supervise_rounds.py:75` makes the round's worktree on its branch; proposals are committed on their initiative's branch (`supervise_rounds.py:108-109`). Read, not verified.

## 4. Tests the requirements make impossible to keep

None. r43 adds lines to the integrate brief and changes no output that a test asserts. Searched `tests/` for the brief's text (`Drafts path`, `Accepted lines`, `Request:`, `integrate_lines`, `brief.md`): no assertion of the integrate brief's contents. The `brief.md` hits are for other rounds (`supervision_review_steps.py`, `supervision_analysis_steps.py`, `supervision_delegation_steps.py`, `supervision_then_workers.py`), which check the file's path only. The features `given q1's lines 1 and 3, and not line 2` (:873, :1087) stay true with an added line. Mark: by search, not run; `tests-of` unavailable.

## 5. A step the work-item skips

The existing way reads the request through `workqueue_request.accepted_lines` (workqueue_request.py:31-36), which refuses a missing request (probe above). r43's step is a read of other initiatives' drafted `adds`, which the existing brief never makes. Effects only that step would have: none found (read). Whether that read sees drafts on other branches or only in this checkout decides the answer (see section 3, last paragraph); not verified.

## 6. Defects

### r43 not met by today's integrate brief
Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w169-2-research/probe_integrate_ids.py` (run). The brief names no id that another initiative's draft adds (`supervision#r98` in `.shop/work/i25/` and `.shop/work/i26/`), so a round numbers its added line `r98` too. The collision is caught only at apply, through `model check` on `spec/` (read: model.lp:175-176 and the skill's step 4), which then sends the drafts back to the gate. This is a spec gap, not a crash.

## 7. The file set

Production and test files the change needs (found by refs, grep and read; none is run by a test that names them):
- scripts/supervise_brief.py: `integrate_lines` gives the other drafted `adds` per capability (or the round gets a list). 135 lines, room 165.
- agents/initiative-round.md: integrate kind says what the round is given and checks its added ids against it. 61 lines (agent text).
- agents/capability-writer.md: numbering above the given ids as well. 87 lines (agent text).
- skills/integrating-a-proposal/SKILL.md: step 2's numbering rule. 78 lines (skill text).
- docs/capability-format.md: the id rule, one sentence. 395 lines (doc; `tools size` covers Python only).
- tests/scenarios/supervision_integrate_steps.py: a step for the brief's new lines, if the planner adds a scenario. 91 lines, room 209.
- features/supervision.feature: a scenario for the brief (a feature file; no line count, not Python).

Modules on the change's path, edited or not, with `wc -l` and room under 300:
- scripts/supervise_rounds.py 134 (room 166): calls `integrate_lines` path; `write_proposals`.
- scripts/supervise_change.py 52 (room 248): `write_proposals`; a check of ids would go here or upstream.
- scripts/supervise.py 248 (room 52): `Run`, its `root` and `dir`; read only.
- scripts/workqueue_request.py 144 (room 156): `accepted_lines`; read only.
- scripts/model_work.py 219 (room 81): proposals' `adds` facts; read only.
- scripts/model.lp: v15b, read only.

`tools size --limit 300` printed nothing (run): no tracked Python file is over the limit.

## Not done

- No scenario was run (none accepted). No `tools map`, so no `tests-of` answer.
- Where other initiatives' drafts are visible from a round's root: read, not verified.
- The planner has two readings of r43, not decided here: (a) `work run` gives the round the other drafted ids in its brief (the spec's "given"); (b) the round or writer reads other initiatives' drafts itself.
