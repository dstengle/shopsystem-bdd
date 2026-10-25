# Branch review of i31: DONE_WITH_CONCERNS

Verdict: one Important finding is triaged fix now. w185 makes `work run` rewrite a proposal's `adds`, `changes` and
`removes` from a `changes` field in the apply round's result (r114). The real apply round never gives that field: its
role text does not ask for one, and neither does `work run`'s brief. So in a real run the lists are never rewritten,
and r114 is met only against the stand-in. Nothing else is Critical or fix now. The suite is green, and every check
named below was run.

## Range and work-items

- Range: `9839b05a..d91509e8`. 9839b05a is the commit that added `.shop/work/i31/initiative.md` ("work: start i31,
  fulfilling q8"). HEAD is d91509e8.
- The branch `i25-review-findings-to-implementation` is shared. The range also holds the commits of i25 to i30, i32
  and i33: their rounds, their work-items (w175 to w181, w184, w187 to w191) and their branch reviews. I mapped every
  code commit of the range to the claim window of a work-item, or to a round of a proposal, and none of them is
  outside both. Their content was reviewed by those initiatives' own reviews and is not i31's.
- i31's work-items:
  - **w183**: withdrawn. Its researcher hit the turn limit (failed, then withdrawn). It has no commits.
  - **w185**: green. Its commits, with `work:` moves left out:
    - `aef1793b` r111 steps; the stand-in gives `usage`
    - `a0f2b5ba` r116 steps
    - `ce5c1bfb` r83, r112 to r115: the production change; retires the old r83
    - `968344f4` the fix: the r107 check on an apply round's list; `rounds()` goes on past a refused round
- i31's spec and feature commits come from its proposal's rounds:
  - `fa05204d` apply: r111 to r116 added, r70 and r83 changed
  - `a30cfe25` formulate: 7 scenarios added, the old r83 deprecated
- `3e1cb8bb` "work: i31 back to started, by hand once" (author `probe`) belongs to no work-item and no round. It
  changes one line of `.shop/work/i31/initiative.md`. Minor, drop: it is a recorded manual repair of i31's status
  (observation 2026-10-25-withdrawn-initiative-done), not code.

## Suite

`Suite: 897 passed, 0 failed at d91509e8 in 22.8 s` (1 skipped, 56 subtests passed; pytest reports 22.54 s).

- It runs in parallel: `pytest.ini` has `addopts = -n auto`, at 1687 % CPU.
- It is not in-process: the steps run `work run` as a program through `subprocess` (`tests/scenarios/conftest.py:34`).
- It is under 60 s, so neither point is a finding.

## Checks

- **w185's check, its acceptance scenarios** (`python3 -m pytest -q --work-item w185`): 155 passed, 1 skipped, in
  6.1 s.
- **`tools check --base 9839b05a`**:
  - **ruff**: 40 errors.
    - None is on a line w185 wrote. `tests/scenarios/test_supervision.py:14 I001` was there at the base: the base
      file has the same `from .supervision_world import *` / `import (` pair at lines 39-40, and w185 only added one
      import, in alphabetical place. `tests/scripts/stub_claude.py:189-190 FURB167` are on lines `aef1793b` did not
      touch.
    - Hits in i31's own tracked files: `.shop/work/i31/runs/supervision/1-gate/gq.py`, `2-apply/apply.py` and
      `3-formulate/splice.py`. These are round sessions' scratch scripts that `work run` committed with the stage
      directories (see Observations).
    - The rest belong to other initiatives' files or are older.
  - **vulture**: clean.
  - **import-linter**: "the project states no import contracts".
- **`tools size --limit 300`** (the limit `CLAUDE.md` gives): it printed nothing. The largest files w185 touched are
  `tests/scenarios/supervision_rounds_steps.py` at 288 lines, `tests/scripts/stub_claude.py` at 274 and
  `scripts/supervise.py` at 271.
- **`features deprecated`**: 4 deprecated scenarios. All four were deprecated before the base, and none belongs to i31:
  - migration-tools @r15
  - supervision @r102
  - work-queue @r1
  - work-queue @r9

  The work-items that accept those ids are in i8, i18, i21, i24 and i28, not in i31. Within i31, the old r83 scenario
  was deprecated by `a30cfe25` and removed by `ce5c1bfb`, which is the Retires entry of w185.
- **`features bindings`**: "every binding names a scenario".
- **A dry-run mode and a real mode of one operation**: none on this branch. The only `--dry-run` is `git push
  --dry-run`, used as a probe in `supervise_faults.py:67` and `supervise_review.py:41`. That is not a mode of the
  system, so no agreement test applies.

## Removed and weakened tests

What I searched i31's commits (`aef1793b`, `a0f2b5ba`, `ce5c1bfb`, `968344f4`) for:

- deleted `def test_` and step functions
- parametrize and Examples rows dropped
- `assert` lines removed or changed
- `skip` and `xfail` added
- steps rewritten to assert something else

What I found:

- **features/supervision.feature, @r83 @deprecated "… ends, the proposal is formulated (deprecated)"**: removed in
  `ce5c1bfb`.
  - What it proved: a proposal given a formulate round ends formulated.
  - It is listed under w185's Retires, and the new @r83 covers the case of no question. Allowed.
  - Its binding is the whole-file `scenarios("supervision.feature")`, so there was no binding of its own to remove.
- **`supervision_rounds_steps.py` `questions_hold`**: rewritten. With four quoted strings it takes the old path
  unchanged; with any other count it checks each question is held, where before such a count could not unpack. Not
  weakened.
- **`apply_started`**: widened to `apply|formulate`. For apply it makes the same two assertions as before. Not weakened.
- **`answered_proposal`**: changed setup only (see Allowances).

The plan's "Tests the decisions break" lists none of these as broken, and none needs to be listed.

## Allowances

- **3-implement report, `answered_proposal` (setup)**: holds. I checked the diff of `a0f2b5ba`. It adds an optional
  `adds` group to the regex and, for "given by its … round", a log.jsonl move. It changes no `assert`, no expected
  value (the default adds stay `thing#r1`) and no parametrize case.
- **4-implement and 6-implement reports**: both give "none". No test of theirs needed an allowance.

## Cannot verify

- **Running probes in the scratch directory.** I wrote `.shop/scratch/i31-branch-review/probe_rewrite.py` to call
  `Changes.rewrite_lists` directly, and running it was refused (both `python3 -I <path>` and the relative form). The
  `rewrite_lists` observations below rest on reading `scripts/supervise_change.py:52-65` instead. The probe has been
  deleted.
- **Whether the `work run` process that ran i33's apply round at 19:56 had already loaded `ce5c1bfb`'s code.** The
  installed scripts at `/home/vscode/shopsystem-bdd/scripts/supervise_rounds.py` do have `rewrite_lists` (line 147)
  and `route` (line 52). Finding 1 does not depend on this, because that round's result has no `changes` field for
  any version of the code to read.

## Findings

### 1. Important, w185, fix now: r114 is met only against the stand-in; the real apply round gives no change list

`scripts/supervise_rounds.py:135-147` (from `ce5c1bfb`), with `agents/initiative-round.md:32-33`.

- **What is wrong**: after an apply round, `work run` rewrites the proposal's lists only when the round's result
  carries `changes` (`applied = entries(data)`; `if applied: self.rewrite_lists(...)`). With no list it leaves them as
  integrate wrote them (plan D3).
  - The apply round's role text gives no such field. Its reply is "the commit, the capability paths changed, the
    decision files added, the change list's path, and `model check`'s last line". Only the integrate kind is told to
    "Give the change list in your result's `changes`".
  - `work run`'s apply brief asks for `status`, `summary` and `questions` only.
  - The r114 scenario passes because its stand-in is given `"fields": {"changes": [...]}`
    (`tests/scenarios/supervision_formulate_steps.py:35-37`), a field no real apply round writes.
- **Reproduction**: the first apply round after the change, i33's `supervision` at 19:56:18.
  - Its result `.shop/work/i33/runs/supervision/7-apply/result.json` has only `status`, `summary` and `questions`.
  - Its summary says it changed "spec/capabilities/supervision.md (r120, r121 added; r75, r105 changed)".
  - `.shop/work/i33/supervision.md` after the approved move (log line 46) still reads `changes: []`.
- **Why it matters**: r114 says the proposal names "the change list the round applied". It is the line i31 was
  started for. Commit `f7135e20` fixed the proposals' ids by hand ("q8 r114 not yet delivered"). As things stand, the
  proposal still names what was drafted, not what was applied. `supervise_draft` drafts the work-items' `accepts` from
  those lists, so a work-item can accept a renumbered or dropped id, or miss a changed one. That is a wrong answer.
- **Fix**: the apply round has to give its change list in its result's `changes`, in the integrate form
  (design-decision/worker-results-are-files: `work run` reads stage fields and never prose).
  - Change the `apply` section of `agents/initiative-round.md`, and the brief if it names fields.
  - If no line of spec-integration asks for that, the line comes first, through integrating-a-proposal.
  - Then decide whether a DONE apply with no list is still a silent no-op (D3) or an error as for integrate (r96).
    Under D3, the gap stays invisible.

### 2. Minor, w185, observation: an apply list naming only other, known capabilities empties the proposal's lists

`scripts/supervise_rounds.py:146-147` with `scripts/supervise_change.py:52-65`.

- **What is wrong**: if `applied` is not empty but no entry is the proposal's `argues`, all three lists are written as
  `[]`.
- **Reproduction**: by reading (the probe was refused). `if applied: self.rewrite_lists(name, applied)`, and inside it
  `lists = {f: [] for f in FIELDS}` is filled only by entries with `each["capability"] == argues`.
- **Why it is not fix now**: no apply round gives a list today (finding 1). It becomes reachable once finding 1 is
  fixed and one apply round applies several capabilities, as i33's 7-apply did (supervision and work-queue).
- **Fix**: leave the lists as they are when no entry names the proposal's capability, or refuse. The fix for finding 1
  should settle this too.

### 3. Minor, w185, observation: `argues` with more than one capability matches nothing

`scripts/supervise_change.py:57`.

- **What is wrong**: `argues` is read as the raw text between the brackets, so `argues: [a, b]` gives `"a, b"`. No
  entry equals it, and the lists are emptied.
- **Reproduction**: by reading.
- **Why it is not fix now**: since `bd765f03` a proposal has one capability, so no client writes such a file.

### 4. Minor, w185, observation: an unreadable apply change list is ignored

`scripts/supervise_rounds.py:136-139` (`except BadChanges: applied = []`). The proposal moves to approved with
integrate's lists. No line names this case.

### 5. Minor, w185, observation: no scenario pins `route()`, the apply round's r107 check, or `rounds()` going on past a refused round

`scripts/supervise_rounds.py:52-61`, `:140-145` and `:63-76`.

- No scenario fails if `route()` always returns `AFTER[status]`. The r116 and new r83 scenarios also pass on the old
  apply-then-formulate chain, as the 3- and 4-implement reports say.
- No scenario has two due proposals with one refused, and none has an apply list naming an unknown capability.
- **Fix**: later Thens, "no round of the kind apply was started for p1", a second proposal in an r115 example, and an
  r107 example with an apply list.

### 6. Minor, w185, observation: a refused round also skips the branch review and the done

`scripts/supervise.py:212-213`: `raise refused` comes before the branch review and `set_done` at `:214-221`. r115
names "the initiative's other nodes". With every work-item green and one proposal refused, the initiative's branch
review waits for the next run. No scenario covers this (the r115 examples have w1 drafted). It is the 4-implement
report's open question.

### 7. Minor, w185, observation: with several refused rounds, only the first is named

`scripts/supervise_rounds.py:73` (`held = held or fault`). Each round's stage directory is still kept by its own
`keep_round`, so nothing is lost.

### 8. Minor, w185, drop: stale module docstring

`scripts/supervise_rounds.py:1-6` still says an awaiting-answer proposal "is given to an apply round" and an approved
one ends "formulated". It does not mention `route()` (r116), a formulate round's questions (r112, r113) or the apply
list (r114).

### 9. Minor, w185, drop: a change outside the file set

`tests/scripts/stub_claude.py:267-268` (from `aef1793b`): the stand-in's result now carries `usage`. The file is not in
w185's `fileset`. The 3-implement report lists it with its reason: `measure initiative` refused the session without
it.

### 10. Minor, w185, drop: a step defined twice

`tests/scenarios/supervision_formulate_steps.py:71-74` defines "p1 is awaiting-answer", and the pattern
`(?P<name>\w+) is awaiting-answer$` in `test_supervision.py` already matches it. It does no harm.

## Shape

- **Size, 300 lines**: met. `supervise_rounds.py` 192, `supervise_change.py` 88, `supervise.py` 271,
  `supervision_formulate_steps.py` 82, `supervision_rounds_steps.py` 288, `supervision_done_steps.py` 54,
  `test_supervision.py` 261, `stub_claude.py` 274.
- **Module map, `scripts/supervise*.py` row** (rounds): met. The routing, formulate questions and apply list sit in
  `supervise_rounds.py`.
- **Module map, `scripts/supervise_change.py` row**: not met (Minor, drop). The row reads "`work run`'s reading of an
  integrate round's change list and its writing of one drafted capability-proposal for each capability it names". The
  module now also rewrites an existing proposal's lists from an apply round's list (`rewrite_lists`,
  `supervise_change.py:52`), and checks that list with `unknown(..., runs=True)` (`:38-44`). The module docstring was
  updated in `968344f4` but the row was not. Check: the row names the apply round's list.
- **Module map, `tests/scenarios/` row** ("one `<capability>_*_steps.py` module a concern"): met by the new
  `supervision_formulate_steps.py`. Its concern is what a formulate round gives a proposal, the apply list it writes
  and the r115 gate endings. The r115 gate-ending Given (`:45-55`) is a different concern from formulation and would
  sit better with the faults steps. Observation only. Check: `grep -n "gate round for p1" tests/scenarios/*_steps.py`
  names a faults module.
- **Code and steps no scenario reaches**:
  - vulture is clean.
  - Every step in `supervision_formulate_steps.py` is used by one of r83, r112, r113, r114 and r115.
  - The retired r83 used only shared steps ("every round ends and every worker gives DONE", the formulated Then),
    which other scenarios still use.

## Coupling

- **`claude -p --output-format json`'s `usage`**: the stand-in now writes `usage.input_tokens` and `output_tokens`,
  because `measure initiative` refuses a session without them.
  - The measurement relies on the CLI's result JSON keeping those keys. That is the CLI's output format, not a
    contract this repository pins.
  - If the CLI renamed them, `measure` would refuse every session, and r105's done would not be reached.
  - Stable: read `usage` defensively and report a session without it as unmeasured, rather than refusing.
  - This is not new in i31; i31 only made the stand-in match.
- **pytest-bdd**: the new step module is registered by `import *` into `test_supervision.py`, as the other step
  modules are. It relies on pytest-bdd finding step fixtures in the test module's namespace, its published way. The
  warnings show pytest-bdd's `_register_fixture`/`FixtureDef` use is deprecated for pytest 10. That is not i31's and
  does not break today.

## Observations

- **F2**: an apply list naming only another capability empties p1's lists. Reproduction: read
  `supervise_change.py:52-65` with `found=[{"capability": "other", ...}]` and `argues: [thing]`. The probe that would
  print `adds: []` was refused.
- **F3**: `argues: [thing, more]` matches no entry. Reproduction: read `supervise_change.py:57`.
- **F4**: an unreadable apply list is ignored. Reproduction: read `supervise_rounds.py:136-139`.
- **F5**: `route()`, the apply r107 check and `rounds()` going on are unpinned. Reproduction: the 6-implement report,
  "No scenario pins either fix"; `pytest --work-item w185` gives 155 passed with no such Given.
- **F6**: a refused round skips the branch review. Reproduction: read `supervise.py:212-215`.
- **F7**: only the first refused round is named. Reproduction: read `supervise_rounds.py:73`.
- **No work-item**: round sessions' scratch scripts are committed as tracked Python. `.shop/work/i31/runs/supervision/
  {1-gate/gq.py,2-apply/apply.py,3-formulate/splice.py}` show up in `tools check` (ruff SIM115, I001, PLC0206) and
  count under `CLAUDE.md`'s "every tracked Python file". Reproduction: `python3 <Scripts>/tools check --base 9839b05a`,
  the `.shop/work/i31/...` lines.
