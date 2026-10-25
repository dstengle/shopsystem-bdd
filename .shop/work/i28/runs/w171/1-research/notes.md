# Research notes: w171 (supervision#r102)

Tools: `scripts/tools` by path. No map exists (`tools tests-of` says "no map"), so every test list below is `by search`. `tools refs` ran (see part 3).

## 1. Why each scenario is red today

- `python3 -m pytest -q -p no:cacheprovider "tests/scenarios/test_supervision.py::test_an_integrate_round_is_given_every_requirement_id_..._whatever_that_initiatives_capabilityproposals_status"` (run): FAILED with `StepDefinitionNotFoundError: Given "an initiative i2 under .shop/work/, started, whose capability-proposal p2 is formulated"` (feature line 1257).
  - Missing step: no pattern matches `an initiative iN under .shop/work/, started, whose capability-proposal pN is <status>`. Existing patterns: `supervision_all_steps.py:68` (no "started," and only `drafted`), `supervision_all_steps.py:90` (`awaiting-answer`), `work_queue_status_steps.py:13`, `work_queue_answer_steps.py:19`.
  - Also undefined by read, after the first: `i2 keeps a draft of thing adding thing#r4 and thing#r5 at <path>` (line 1258), `an initiative i3 ... whose capability-proposal p3 is drafted` (line 1259, a `started,` form), `i3 keeps a draft of other adding other#r1 at <path>` (line 1260). Pytest-bdd stops at the first undefined step, so these are `read`.
  - Once steps exist, the Then would fail too: `supervise_drafts.added_by_others` reads only `drafts/spec/capabilities/*.md` under the last `<k>-integrate` (see part 6), so the brief would say `none` and the Then "given thing#r4 and other#r1" fails. `read`, and confirmed by the probe below.
- The `@r102` scenario with `(deprecated)` in its title (`test_..._deprecated`): run, PASSED (1 passed). It uses the old step `whose kept drafts add ...` (`supervision_integrate_steps.py:144-154`), which writes drafts at `runs/<name>/1-integrate/drafts/spec/capabilities/<cap>.md`.

## 2. What the system answers today

Probe: `.shop/scratch/w171-1-research/probe_drafts.py`, command `python3 -m pytest -q -s -p no:cacheprovider .shop/scratch/w171-1-research/probe_drafts.py` (run, 6 passed). It calls `scripts/supervise_drafts.added_by_others(root, "i1")` (the function `supervise_brief.py:76` calls) on a temp checkout: spec/capabilities/thing.md holds thing r1, r2, r5; i2 (started) and i3 (started) keep drafts.

| case (run) | layout | returned |
|---|---|---|
| CURRENT LAYOUT: i2 `2-integrate/drafts/round-1/spec/capabilities/thing.md` adds r4, r5; i3 `2-integrate/drafts/round-2/.../other.md` adds other#r1 | `drafts/round-<m>/spec/capabilities/` (the real layout, see part 6) | `[]` (expected `thing#r4`, `other#r1`) |
| OLD LAYOUT: same ids at `1-integrate/drafts/spec/capabilities/` | old layout | `['thing#r4', 'other#r1']` (r5 and r1/r2 excluded by spec) |
| OWN DRAFT: i1's own draft adds thing#r4 | — | `[]` (own initiative excluded, by code) |
| EARLIER STAGE ONLY: i2 draft in `1-integrate`, `2-integrate` has no drafts | — | `[]` (only the last integrate stage is read, by design: `last_integrate`) |
| CAPABILITY NOT IN spec/: i2 draft for `new` adds new#r1, spec has no new.md | round-N layout | `[]` (the glob misses it; the held-check rule by read: an absent file holds nothing, so every id counts) |
| NO RUNS: i2 with no runs dir | — | `[]` |

Also `run` by reading the real repo: `Glob .shop/work/*/runs/*/*-integrate/drafts/**/*.md` finds `i25/runs/i25/2-integrate/drafts/round-1/spec/capabilities/{supervision,work-queue}.md` and `i26/.../round-1/spec/capabilities/{requests,supervision}.md`. So the real kept drafts are all under `round-1`, and today's function returns none for them.

## 3. Old assumptions

Callers, `tools refs`: `refs added_by_others` reports 0 references (`refs` does not follow the module-attribute call `supervise_drafts.added_by_others`); the caller was found by search: `scripts/supervise_brief.py:76` (`integrate_lines`). `refs last_integrate` 1 production ref (`supervise_drafts.py:30`, its own module), `refs ids_in` 2 refs (1 production, `supervise_drafts.py:31`, `:30`).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_drafts.py:added_by_others, the glob `"drafts/spec/capabilities/*.md"` (line 29) | reads kept drafts only at `<k>-integrate/drafts/spec/capabilities/` (no round level) | must read `drafts/round-<m>/spec/capabilities/` (every round's drafts, or the last round's, see part 7 decision) | the deprecated scenario `test_..._deprecated` (passes today through the old layout); the new scenario is red and executes it only once its steps exist (`none` by run) | read, probe |
| scripts/supervise_drafts.py:last_integrate (line 16) | highest-numbered `<k>-integrate` stage only | the r102 text reads drafts of "another initiative", not only its last round; a re-run round with no writer (see gate notes in ledger) leaves no drafts in the last stage | the deprecated scenario (1-integrate only, one stage) | read, probe EARLIER STAGE ONLY |
| scripts/supervise_drafts.py:added_by_others, the held check `root/spec/capabilities/<name>` (line 30) | reads spec/ of the checkout `root` (working tree), not of the branch the integrate round starts from | r102 says "on the branch it starts from"; the checkout may differ from that branch | the deprecated scenario | read |
| scripts/supervise_drafts.py:ID regex and dedupe (lines 8, 31-32) | `[r<n>]` lines | unchanged by r102 | the deprecated scenario | read |
| features/supervision.feature:1240 (deprecated scenario) and its step `supervision_integrate_steps.py:144-154` | writes the old layout | the only user of the old step (`by search`: "whose kept drafts add" in features is only lines 1245-1246) | `test_..._deprecated` (passes today) | search |
| spec/capabilities/supervision.md:32 r102 text | "not yet applied" | code and the new scenario use "spec/ does not hold"; the two differ for an id the spec holds but whose proposal is not applied (not in the scenario) | none | read |

No place is `none`: the table lists each place a search finds.

## 4. Tests the requirements make impossible to keep

`tools tests-of` cannot answer (no map). By search:

- `tests/scenarios/test_supervision.py::test_..._deprecated` (feature line 1240): passes today. The new requirement reads only the round-level layout, so its Given (old layout, `supervision_integrate_steps.py:149`) gives `added_by_others` nothing: the Then `a round of the kind integrate was started for i1, given thing#r4 and other#r1` would fail. Cannot pass as it is, unless the reader keeps the old path too, its fixture moves to round-1, or the scenario is retired (r73: a deprecated scenario whose @r102 the work-item accepts goes under `## Retires`; w171 has no Retires section). Both readings below in part 7.
- `supervision_integrate_steps.py:79-85` (`drafts_committed`, r91): writes the round's own drafts at `.shop/scratch/1-integrate/drafts/spec/capabilities/thing.md` and checks the kept path ends in `drafts/spec/capabilities/thing.md`. Not changed by r102 (the reading changes, not the keeping). Kept: sound for r91 by read. It encodes the old layout (real runs keep `drafts/round-1/`), so it is out of step with the real layout but still passes; `by search` only.
- `supervision_integrate_steps.py:96-102`, `:105-108`, `:116-130`: r92 and r91 assertions, not touched by r102. Kept by read.
- `supervision_integrate_steps.py:165-169` (the new scenario's "was not given" Then): passes once the steps exist, since it reads the brief. Kept by read.
- No other test asserts the brief's "Requirement ids other initiatives' kept drafts add" sentence (`by search`: grep of tests/ for the sentence and for `supervise_drafts` finds none).

## 5. A step the work-item skips

- The reader takes the held ids from `root/spec/capabilities/` (working tree of the checkout) and the other initiatives' drafts from `root/.shop/work/<other>/runs/...` (working tree). r91 keeps drafts on each initiative's own branch, and r102 says "on the branch it starts from". So a draft that is on another initiative's branch and not in the checkout is never read. `read` (not run; a probe with two branches was not built).
- Effect only this step produces: the brief's "take none of them" list depends on the checkout's working tree, not on git. `read`.

## 6. Defects

### D1. kept drafts in the round-level layout are never read

- Reproduction (run): `python3 -m pytest -q -s -p no:cacheprovider .shop/scratch/w171-1-research/probe_drafts.py`, test `test_current_round_layout`: `CURRENT LAYOUT for i1 -> []` with i2 holding `.shop/work/i2/runs/i2/2-integrate/drafts/round-1/spec/capabilities/thing.md` (adds thing r4, r5) and i3 holding `.../2-integrate/drafts/round-2/spec/capabilities/other.md` (adds other r1). Expected `['thing#r4', 'other#r1']`.
- Real data (run, Glob): `.shop/work/i25/runs/i25/2-integrate/drafts/round-1/spec/capabilities/supervision.md` and i26's `drafts/round-1/spec/capabilities/requests.md` and `supervision.md`. The brief of an integrate round (`supervise_brief.py:76-80`) therefore never names another initiative's drafted ids. This is the defect that makes the i28 hand bootstrap's collisions possible (ledger: supervision r98 in both i25 and i26).

### D2 (note, not a defect by reading)

- `tools refs` misses the module-attribute call in `supervise_brief.py:76`, so `refs` reports 0 callers. Found by search.

## 7. The file set

Production:
- `scripts/supervise_drafts.py` (33 lines; room 267): the glob at line 29 changes to the round level (`drafts/round-*/spec/capabilities/*.md`, or each round's drafts; the choice is the plan's). Found by read and probe D1.
- `scripts/supervise_brief.py` (143 lines; room 157): calls `added_by_others` at line 76 unchanged. Listed because it is on the path; edit only if the signature changes. Found by search.
- `scripts/workqueue.py` (290 lines; room 10): on the path (supplies `WORK`, read by supervise_drafts line 26). Not edited unless WORK changes. Found by read.

Tests:
- `tests/scenarios/supervision_integrate_steps.py` (170 lines; room 130): new steps: `an initiative iN under .shop/work/, started, whose capability-proposal pN is <status>` and `iN keeps a draft of <cap> adding <ids> at <path>`; the old `whose kept drafts add` step (lines 144-154) stays only if the deprecated scenario stays. Found by the pytest-bdd undefined-step message.
- `tests/scenarios/supervision_integrate_steps.py` or the deprecated scenario's step: decision between (a) keep the old layout read as well, (b) move the deprecated scenario's fixture to `drafts/round-1/`, (c) retire the deprecated scenario under `## Retires`. Each is a reading: (a) keeps a path no real run writes; (b) keeps the scenario, its text unchanged; (c) removes it, as r73 says. Plan to choose.
- `tests/scenarios/test_supervision.py` (258 lines; room 42): pytest-bdd scenario bindings; both r102 scenarios are already collected. No edit needed by read.
- `features/supervision.feature`: the deprecated scenario (line 1240) changes only under option (c). Not Python, no size limit.

Spec (not needed by the scenarios): `spec/capabilities/supervision.md:32` (r102 text "not yet applied" vs "spec does not hold"). Listed for the plan, not for the tests.

Size: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` (run) printed nothing: no tracked Python file is over 300 lines. Room figures are `wc -l` (run).

Scratch: `.shop/scratch/w171-1-research/` (probe_drafts.py). `git status --porcelain` shows nothing (run) at the end of research, so the scratch directory is ignored.
