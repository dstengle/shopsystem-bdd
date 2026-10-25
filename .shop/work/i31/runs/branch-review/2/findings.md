# Branch review 2 of i31: DONE

Verdict: this is the re-review after w193, the fix work-item for branch review 1. Review 1's one fix-now finding was
that r114 was met only against the stand-in. That is fixed at the point `work run` controls. The apply brief
(`scripts/supervise_brief.py:51-52`) asks for the applied change list in the result's `changes`. So does the `apply`
kind of `agents/initiative-round.md:33`. The r114 Then now asserts that the brief asks for it.

- No finding is Critical, and none is triaged fix now.
- i31's checks (w185, w193) pass.
- The suite has 8 failures at HEAD. All 8 are i33's scenarios (r75, r105, r120, r121), which w194 accepts, and w194 is
  awaiting-answer. None is a scenario of i31's.

## Range and work-items

- **Range**: `9839b05a..5f36222c`. 9839b05a is "work: start i31, fulfilling q8", the commit that added
  `.shop/work/i31/initiative.md`.
- **Shared branch**: the branch `i25-review-findings-to-implementation` also holds i25 to i30, i32, i33 and i34. Those
  initiatives have their own work-items, rounds and branch reviews, and their content is not i31's.
- **i31's work-items**:
  - **w183**: withdrawn (researcher hit its turn limit), no commits.
  - **w185**: green, reviewed in branch review 1. Commits `aef1793b`, `a0f2b5ba`, `ce5c1bfb`, `968344f4`.
  - **w193**: green, the fix of branch review 1.
    - Its claims were `32ce42d3`, `05777a48` and `8114d5f6`. It was merged again twice, on i33's failures.
    - Its done is `d787c410`.
    - Its one commit that is not a `work:` commit is `6b06211b` "work run asks the apply round for the change list it
      applied (r114)". It changes `agents/initiative-round.md` (+1), `scripts/supervise_brief.py` (+7 −3) and
      `tests/scenarios/supervision_formulate_steps.py` (+3 −1), all three in its fileset.
    - The other code commit in that window, `64c62951`, is w192's (i33).
- **Commits since review 1 (`d91509e8..HEAD`)**: each one that is not a `work:` commit is one of these:
  - a work-item's: w192's `64c62951`, w193's `6b06211b`
  - a round's: `50addf01`, `f1a9ecd3`, `af6357e1`
  - a branch review of i32
  - a records commit: `6e562ea5`
  - a by-hand repair of i33 under the person's delegation: `59ca81e1`, `6e17f0de`, `13e91f83`

  None of them is an i31 commit outside a work-item.

## Suite

`Suite: 905 passed, 8 failed at 5f36222c in 22.0 s` (1 skipped, 56 subtests passed; pytest reports 21.74 s).

- It runs in parallel: `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- It is not in-process: the steps run `work run` through `subprocess` (`tests/scenarios/conftest.py:34`).
- It is under 60 s, so neither is a finding.
- **The 8 failures**:
  - r121 Outline ×4 (`features/supervision.feature:1024`): its Given has no step yet.
  - r105 Outline ×2 (`:1455`).
  - r75 ×1: "… kept branch review lists nothing to fix now, measured".
  - r120 ×1 (`:1516`).

  All four ids are accepted by i33's w194 (`accepts: [supervision#r120, supervision#r121, supervision#r75,
  supervision#r105]`), which is awaiting-answer. They are not i31's and not a finding of this review.

## Checks

- **w193's check, its acceptance scenarios** (`python3 -m pytest -q --work-item w193`): 155 passed, 1 skipped, 56
  subtests passed, in 5.9 s.
- **w185's check** (`--work-item w185`): 155 passed, 1 skipped, in 4.1 s.
- **The r114 scenario by name** (`-n 0 tests/scenarios/test_supervision.py -k "change_list or adds_changes"`): 6
  passed.
- **`tools check --base 9839b05a`**:
  - **ruff**: 44 errors. None is in a file w193 touched (`supervise_brief.py`, `supervision_formulate_steps.py`; the
    agent file is not Python).
    - i31's own hits are the round sessions' committed scratch scripts `.shop/work/i31/runs/supervision/{1-gate/gq.py,
      2-apply/apply.py,3-formulate/splice.py}`, as in review 1.
    - `tests/scenarios/test_supervision.py:14 I001` and `tests/scripts/stub_claude.py:189-190 FURB167` are as review 1
      found them: not on lines i31 wrote.
    - The rest are other initiatives' (`scripts/workqueue.py:248` from w192, `scripts/supervise_analysis.py:4`, i29 to
      i33 run scripts).
  - **vulture**: clean.
  - **import-linter**: "the project states no import contracts".
- **`tools size --limit 300`**: printed nothing. `supervise_brief.py` 171 lines, `supervision_formulate_steps.py` 84,
  `supervise_rounds.py` 192, `supervise_change.py` 88.
- **`features deprecated`**: 8 deprecated scenarios. None is i31's: its old r83 was retired by w185 (`ce5c1bfb`).
  - migration-tools @r15
  - supervision @r75, @r121, @r102, @r105
  - work-queue @r1, @r23, @r9
- **`features bindings`**: "every binding names a scenario".
- **A dry-run mode and a real mode**: none in the system (as review 1 found), and w193 adds none. No agreement test
  applies.

## Removed and weakened tests

None in w193. I searched `6b06211b` for:

- deleted `def test_` and step functions
- dropped parametrize or Examples rows
- removed or changed `assert` lines
- an added `skip` or `xfail`
- a step rewritten to assert something else

Its only test change adds one assertion to `lists_written` (`supervision_formulate_steps.py:77-78`): every apply brief
of p1 contains "result's `changes`", and there is at least one. That strengthens the step, as the plan's Decision 2
says. The plan lists no test under "Tests the decisions break" ("None"), which agrees. w185's removals and rewrites are
as review 1 gave them: only the retired @r83, listed under its Retires.

## Allowances

The 3-, 4- and 5-implement reports of w193 all give "none". No allowance is needed, because no test was weakened.
w185's `setup` row (`answered_proposal`) was verified in review 1 and nothing has changed it since.

## Cannot verify

- **Whether a real `initiative-round` apply session now gives `changes`.** No apply round has run since `6b06211b`:
  i34's proposal has had only its gate. What I verified instead:
  - The brief asks for it (the r114 Then).
  - The installed plugin at `/home/vscode/shopsystem-bdd` has both the new apply text (`agents/initiative-round.md:33`)
    and `CHANGE_LIST` in the apply brief (`scripts/supervise_brief.py:52`).

  This is not a check a work-item names. It is open because no apply round has run, not because a check failed.

## Findings

No Critical, no Important, nothing fix now.

### 1. Minor, w193, drop: the implementers' results name commits that did not land

`.shop/work/i31/runs/w193/3-implement/result.json` names `f92c4536`, and `5-implement/result.json` names `69bad2e0`.
The commit on the branch is `6b06211b`. The w193 review checked that the three commits have the same content on the
three files. Someone tracing by hash finds unreachable commits. Fix: none needed.

### 2. Minor, w185 (made reachable by w193), observation: an apply list with no entry for the proposal's capability empties its lists

This is review 1's F2, at `scripts/supervise_change.py:52-65`. It is now reachable, because the apply text asks for
"one entry for each capability you applied". i33's 7-apply applied supervision and work-queue in one round, and its
work-queue round then reported "nothing to write". If an apply round lists only another capability, `rewrite_lists`
sets all three of p1's lists to `[]`. An empty list (`if applied:`) leaves them as drafted.

- Reproduction: by reading. `lists = {f: [] for f in FIELDS}` is filled only by entries with `each["capability"] ==
  argues`.
- No line names the case, and this is a re-review, so it is an observation. Fix: leave the lists when no entry names
  `argues`, after a line says so.

### 3. Minor, w185, observation: a DONE apply round with no `changes` keeps the drafted lists silently

`scripts/supervise_rounds.py:135-147`. This is review 1 F1's last point and w193's open case. Integrate treats a DONE
with no list as an error (r96, `agents/initiative-round.md:28`), and apply does not. No line names it.

- Reproduction: by reading. `applied = entries(data)`; `if applied: self.rewrite_lists(...)`.

Review 1's F3, F4, F6 and F7 (observations) and F8 to F10 (drops) stand unchanged. w193 did not touch those files.

## Feature files

- **A deprecated scenario whose replacement's work-item is green**: work-queue @r23 "a command whose change leaves
  every work-item … sets the initiative to done (deprecated)". Its replacement's work-item, i33's w192, is green, and
  w192 has no Retires section. This is i33's, not i31's; named for i33's branch review.
- **supervision @r75, @r121, @r105**: their replacements are w194's, which is awaiting-answer, so they are not this
  case.
- **A scenario removed that was not deprecated**: none in w193. w185 removed only the deprecated @r83.
- **A binding naming no scenario**: none.

## Shape

- **Size, 300 lines**: met, figures above.
- **Module map, `scripts/supervise*.py` row** ("briefs, …"): met. The apply brief's wording sits in
  `supervise_brief.py:11-13` and `:51-52`, and is shared with the integrate brief as `CHANGE_LIST`, so the two cannot
  drift.
- **Module map, `scripts/supervise_change.py` row**: still names only "an integrate round's change list" while the
  module also reads the apply round's (review 1, drop). Unchanged by w193. Check: the row names the apply round's list.
- **`tests/scenarios/` row**: met. The new assertion uses `starts` from `supervision_world`, the shared helper.
- **Code and steps no scenario reaches**: vulture is clean. `CHANGE_LIST` is reached by both the integrate briefs and the
  apply briefs (the r114 scenario).
- **Code no line asks for**: none. The brief wording serves r114 ("from the change list the round applied") under
  design-decision 0038 (worker-results-are-files).

## Coupling

Nothing new in w193. Review 1's point on `claude -p` result JSON `usage` stands. That point is mechanism `measure`
relies on, and it is not i31's.

## Observations

- **F2 (above)**: an apply list naming only another capability empties p1's lists. Reproduction: read
  `scripts/supervise_change.py:52-65` with `found=[{"capability": "other", ...}]` and `argues: [thing]`.
- **F3 (above)**: a DONE apply with no `changes` is a silent keep. Reproduction: read
  `scripts/supervise_rounds.py:135-147`.
- **No work-item**: round sessions' scratch scripts are committed as tracked Python under `.shop/work/*/runs/` and are
  linted by `tools check` (i31: `gq.py`, `apply.py`, `splice.py`). Reproduction: `python3 <Scripts>/tools check --base
  9839b05a`, the `.shop/work/i31/...` lines.
