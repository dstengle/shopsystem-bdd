# Notes: w169 (spec-integration#r43, round-ids-avoided)

Method: `tools map` has never run here (`tests-of` and `untested` say "no map"), so no test lists; searched by text.
`tools refs` works. Scripts run from `/home/vscode/shopsystem-bdd/scripts`. Accepted scenarios: none found (see 1).

## 1. Why each scenario is red today

No accepted scenario. `features/` has no `spec-integration.feature`; the `@r43` tags in `features/` belong to
`design-model-check`, `batch-measurement` and `supervision` (other capabilities). Nothing is red.

Why this is not a failure: `spec-integration` is `group: guarantees`. `scripts/work_items.py:108` and `:124-131`
exempt a work-item whose requirements are all guarantees: with no test left it exits OK.
Run: `python3 -m pytest -n 0 --work-item w169 tests/scenarios/test_supervision.py` gave
`collected 178 items / 178 deselected / 0 selected` (run). So `work run` would pass w169 with no check at all.

## 2. What the system answers today

Probe `.shop/scratch/w169-1-research/probe_integrate_ids.py` (run with `-n 0`; `pytest.ini` otherwise hides prints).
Fixture: request q1 with lines 1 (accepted), 2 (refused); i25 and i26 each drafted a `supervision.md` proposal adding
`supervision#r98`; `spec/capabilities/supervision.md` holds r1-r97.
`Briefs.integrate_lines({"fulfils": "request/x/q1"}, here)` returned (run):
- `Request: q1`
- `Accepted lines of the request:` `- 1. first line` (line 2 left out, as it should be)
- `Drafts path: .../round/drafts`
- the change-list form (`{"capability", "adds", "changes", "removes"}`)
- nothing about the other drafts: `supervision#r98` in i25 and i26 is not in the brief.

Nearest cases not given by the scenarios (run, same fixture): `-n 0` needed for output. Plain run of
`tests/scenarios/test_supervision.py` collects 178 and deselects all 178 with no `--work-item` (run); I did not find
the cause (`pytest.ini` addopts `-m "not fixture"`; no `fixture` marks in the file). Not chased further.

## 3. Old assumptions

The old rule: a new line's id is one above the capability's own lines and `retired` list, counted in `spec/` and in the
initiative's own earlier rounds. r43 adds ids other initiatives' drafts add (not yet in `spec/`).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_brief.py:integrate_lines (66-76) | gives the request, its accepted lines, the drafts path and the change-list form; no other proposals' ids | must give (or let the round read) ids other initiatives' drafts add, per capability | by search: features/supervision.feature:868 and :1082 (`given q1's lines 1 and 3`); not run | refs (1 caller, supervise_brief.py:38); read |
| agents/initiative-round.md:27-28 (kind integrate) | round gives the change list; no instruction on other drafts | the round must be given them, or it must read them | none (agent text) | read |
| skills/integrating-a-proposal/SKILL.md:23 (step 2) | added rows numbered above the capability's lines, `retired`, and this initiative's earlier drafted lines | also above other initiatives' drafted adds | none (skill text) | read |
| agents/capability-writer.md:19-21 | new line one above every id the capability has used or retired | same, for the writer's numbering | none (agent text) | read |
| docs/capability-format.md:159-163 | the same rule, in the format doc | same | none (doc) | read |
| scripts/supervise_change.py:write_proposals (38-52) | writes a drafted proposal with its `adds`; no check against other proposals | a check or a carried list lands here or upstream | by search: features/supervision.feature:1133 (change list gives one proposal per capability) | read |
| scripts/model.lp:173-175 (v15b) with scripts/model_work.py:160-175 (adds facts) | duplicate ids are checked within `spec/` only | two drafted proposals adding one id pass `model check`; the collision shows at apply | by search: tests/scripts/test_model_reading.py:99-110 (two proposals adding); not run | grep `adds`; read |

## 4. Tests the requirements make impossible to keep

None. r43 adds lines to the brief and sets no existing output. Searched tests for the brief's text
(`Accepted lines`, `Drafts path`, `Request:`, `change list`): no assertion of the integrate brief beyond
`given q1's lines 1 and 3, and not line 2` (features/supervision.feature:873, :1087). An added line keeps those true.
Mark: by search, not run. `tests-of` unavailable (no map).

## 5. A step the work-item skips

The existing way reads the request through `workqueue_request.accepted_lines` (workqueue_request.py:31-36), which
refuses a missing request (`there is no request <id>`, :22). A read of other initiatives' drafts would be a second
read of files under `.shop/work/<other>/`. Effects only that step makes: none found. Where those drafts sit (on their
initiative branches, or in this checkout) decides whether the read sees them: `supervise.py:49` takes `self.dir` from
`self.root`; `supervise_rounds.py:75` makes the round's worktree on its own branch. Not verified: `read` only.

## 6. Defects

### r43 not met by today's integrate brief
Reproduction: probe_integrate_ids.py (above). The brief names no id that another initiative's draft adds
(`supervision#r98`, drafted by i25 and i26 in the fixture), so a round numbers its added line `r98` as well.
Read: the collision is caught only at apply, when `model check` reports v15b in `spec/` (model_work.py, apply step 4 in
the skill), which sends the drafts back to the gate. This is a spec gap, not a crash.

### Observation: test_supervision.py collects 0 without --work-item
`python3 -m pytest -n 0 --collect-only tests/scenarios/test_supervision.py` gives `178 deselected` (run). Cause not found.

## 7. The file set

Files a plan would change for r43 (found by refs, grep and read; none is run by a test today):
- scripts/supervise_brief.py: `integrate_lines` gives the other drafts' ids per capability (or the round gets a list). 135 lines, room 165.
- agents/initiative-round.md: integrate kind says what the round is given and checks it. 61 lines (text, not Python).
- agents/capability-writer.md: numbering above the other drafts' ids too. 87 lines (text).
- skills/integrating-a-proposal/SKILL.md: step 2's numbering rule. 78 lines (text).
- docs/capability-format.md: the id rule, one sentence. 395 lines (a doc; `tools size` covers Python only).
- tests/scenarios/supervision_integrate_steps.py: a step for the brief's new lines. 91 lines, room 209.
- features/supervision.feature: a scenario for the brief (not measured; this is a feature file).

Modules on the change's path, edited or not, with line count (`wc -l`) and room under 300:
- scripts/supervise_rounds.py 134 (room 166) — calls integrate_lines and write_proposals.
- scripts/supervise_change.py 52 (room 248).
- scripts/supervise.py 248 (room 52).
- scripts/workqueue_request.py 144 (room 156) — accepted_lines.
- scripts/model_work.py, scripts/model.lp: read only, not changed by r43.
`tools size --limit 300` printed nothing: no tracked Python file is over the limit.

## Not done

- No scenario was run (none accepted). No `tools map`, so no `tests-of` answer.
- Where other initiatives' drafts are visible from the round's root: read, not verified.
- r43's two readings for the planner: (a) `work run` gives the round the ids in its brief (the spec's "given");
  (b) the round or writer reads other initiatives' drafts itself. Not decided here.
