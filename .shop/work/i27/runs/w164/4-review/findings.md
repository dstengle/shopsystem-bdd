# review of w164 (integrate-rounds-carried: supervision r91-r97, r66)

**Verdict: DONE.** No Critical finding and nothing to fix now. There are two Minor findings and two observations.

## Commits reviewed

The branch `work/w164` is gone. These are the commits between `4910049f work: w164 ready -> claimed` and
`44e59393 work: w164 claimed -> done` on HEAD:

- 0ca611cf work run: an initiative with no work-item gets no branch review and no measure (r94, r97)
- a4e922a6 work run: integrate rounds carried ... (r91-r93, r96)
- 12d95e83 work run: integrate, apply and formulate rounds of different initiatives run one at a time (r95); ...

They match the commits the implementer's `result.json` lists. Nothing under `features/` changed (`git diff --stat 4910049f 12d95e83`
shows 15 files, none under features/).

## Removed and weakened tests

What I searched for: in `git diff 4910049f 12d95e83 -- tests`, every removed `def`, `assert`, parametrize case, skip and xfail.

- `tests/scenarios/supervision_rounds_steps.py::second_not_refused` (lines 160-168). **Before:** it asserted that the second
  `work run` exited 0 and had no `work:` in its stderr. **Now:** for the r84 scenario (the one that has an integrate round), it asserts
  that stderr has no "not committed" refusal and that a second integrate round was started. The other scenarios that use this step keep the old
  assertion. The assertion is looser for the r84 scenario. **The plan lists it** under "Tests the decisions break" (part 4)
  and gives the reason: r93 and r96 make the second run end in r96's error. This is not a finding.
- `proposed_fulfilling` gained a `status="proposed"` parameter. No assertion and no expected value changed (a setup change).
  It is not weakened.

No other test was removed or weakened.

## Allowances

- `second_not_refused`: the report puts it in "Tests changed under an allowance" as listed in the plan, and the plan does list it (part 4).
  The row holds.

## Cannot verify

- The report's whole-suite figures (151 passed with `--work-item w164`; 315 passed for `test_supervision.py` + `tests/scripts`).
  I did not run the whole suite, as the brief says. The 8 scenarios of this work-item pass (see the commands below).
- The drafts path in a real `initiative-round` session. The agent text was changed (`agents/initiative-round.md`), but only
  the stand-in exercises it.

## Findings

1. **Minor, observation.** `tests/scripts/stub_claude.py` is changed (`linger`, `wait_until(seconds=)`) but is
   outside the work-item's `fileset`. The report declares it ("Outside the file set"), and it serves r95's scenario only.
   **Why it matters:** the file set is the claim (design-decision/the-file-set-is-the-claim), so a parallel work-item that
   claims the stand-in could collide. **Fix:** none now. Future plans that need the stand-in should name it.
2. **Minor, observation.** Ruff findings in lines these commits added:
   - `scripts/supervise_brief.py:74` ISC004 (implicit string concatenation in a list);
   - `tests/scenarios/supervision_all_steps.py:111` FURB167 (`re.M`), and `:127` RUF007 (`zip` over pairs);
   - `tests/scenarios/supervision_integrate_steps.py:72` FURB167.

   The findings at `tests/scripts/stub_claude.py:185-186` are on lines the commits did not touch, so they already existed. The I001 at
   `tests/scenarios/test_supervision.py:14` is in an import block where the commit inserted one line in its sorted place.
   It probably already existed.
   **Reproduction:** `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 4910049f` exits 1 with 7 ruff errors; vulture is
   clean; import-linter reports that there are no contracts. **Fix:** parenthesize the concatenated string, use `re.MULTILINE`,
   and use `itertools.pairwise`.
3. **Important (hardening), observation.** `scripts/supervise_change.py:44`, in `write_proposals`: the proposal is written to
   `self.dir / (capability + ".md")`, and nothing checks the capability name.
   - A change list naming `initiative` would overwrite `initiative.md`, and the next commit would commit that.
   - A change list naming a work-item (`w1`) or `ledger` would overwrite that file.
   - A name holding `../` would write outside the initiative's directory.
   - An existing proposal file of the same name is overwritten.

   No client sends such a list today: the agent names capabilities from `spec/capabilities/`. The plan leaves this as an
   open case (part 5).
   **Reproduction:** reading the code: `entries()` accepts any non-blank string as `capability`. `write_proposals` joins it to the
   path as given. **Fix:** refuse, as BadChanges, a capability that is not a file in `spec/capabilities/`.
4. **Minor, observation.** The gate round's brief does not name where the drafts are now kept (`runs/<initiative>/<k>-integrate/drafts/`).
   The agent's gate kind says "read each round's `gate.md` where it was written", and that path was under the removed
   worktree. This is not a regression: the drafts under `.shop/scratch/drafts` in the worktree were lost before this change too. It is an open case of the
   plan (part 5).

Risks I checked and found sound:
- **r91 on the turn limit.** `supervise_worker.worker` copies `here` (which holds `drafts/`) into the stage directory at
  line 186, before the `cut_short` fault at line 196. `keep_round` then commits it. Its scenario passes.
- **r95 lock order.** `round_lock` is taken in `Rounds.round` before `run_round`. `worker()` then takes `self.lock` and `self.slots`
  inside it, and nothing that holds `lock` or `slots` waits on `round_lock`. Gate rounds don't take it, as r66 requires.
- **r96.** `refuse_integrate` keeps the stage directory and drafts, and raises an error naming "the integrate round of
  <name> (<stage dir>)". A malformed `changes` is refused in the same way.
- **r94/r97.** `pull_through` tests `self.items()` before the branch review and `analyse`.
- **Code that no line asks for.** I found none. `commit(also=)` serves r92, the `Drafts path:` brief line serves r91, and
  the `changes` form serves r92/r96.
- **Size.** `tools size --limit 300` printed nothing.

## Commands run

- `git log --format='%h %s' -15 HEAD`; `git diff --stat 4910049f 12d95e83`; `git diff 4910049f 12d95e83 -- scripts CLAUDE.md agents`;
  `git diff 4910049f 12d95e83 -- tests`; `git show 12d95e83:scripts/supervise_rounds.py`
- `grep -nE 'r(9[1-7]|66)' spec/capabilities/supervision.md`; `grep -n copytree ... scripts/supervise*.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 4910049f`: ruff 7 errors (above), vulture clean,
  import-linter: no contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output (exit 0)
- `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -k "no_workitem or no_work_item or integrate or one_at_a_time or drafts or change_list"`:
  8 passed (r91 ×2, r92, r93, r94, r95, r96, r97)
