# Branch review 2 of i30

**Verdict: DONE.** Review 1 had one fix-now finding: `agents/code-scout.md:24` said 40 turns. w188 fixed it in `2e913069`, and the line now says 80 turns (`--max-turns 80`). That matches `scripts/supervise_worker.py:54` and supervision#r19. Nothing is Critical and nothing is fix now. Every check a work-item names was run here and passes.

This is the re-review of a fix work-item (r110). Under that rule, everything below is an observation or a drop.

## Range and work-items

- **Range:** `4fbc25cd..0e9620ac` on `i25-review-findings-to-implementation`.
  - The branch is shared by i25 to i31. Most of the range is other initiatives' commits: their rounds, work-items, branch reviews, `done` commits and records. They are judged by their own reviews and named here only where a check reaches them.
  - Since review 1 (at `5892599d`), the only code change in the range is `agents/code-scout.md`: `git diff --stat 5892599d HEAD -- . ':!.shop'`.
- **i30's work-items.** Each one's commits fall between `ready -> claimed` and `claimed -> done`, less the `work:` commits:
  - **w180** (formulation#r23, green): `75cd7fda` (window `225d3ed2..5d20b71e`) and `4f1d4641` (window `ce37512e..5ee2e95a`).
    - The first window also holds w181's commits (i29): `4d3113e1`, `5048b72e`, `c482f4f8`, `07d5c24c` and `d87a295b`. They are attributed by their messages.
  - **w182** (withdrawn): no commit reached the branch.
  - **w184** (supervision r19, r110, r117, green): `cd134f29`, `d40c0d26` and `b1b8562c` (window `85065878..6df21f90`).
    - `1f4a0731` in that window is w186's (i25).
  - **w188** (the fix of review 1, green): `2e913069` (window `44667d3a..71732a3c`).
- **i30 commits outside any work-item.** These are `work run`'s and the rounds' own commits, not unowned code:
  - spec and round commits: `31738369`, `d54f006a`, `2f3698be`, `88f2de4c`
  - `work note` commits
  - `2e3c65b5 branch review 1 of i30`
  - `0279766f work add: i30/w188`
  - the hand commits `f7135e20` and `0eb572a2`, both named in review 1

## Suite

`Suite: 885 passed, 10 failed at 0e9620ac in 22.2 s`

- **Command:** `time python3 -m pytest -q -rfEx -p no:warnings`. The 22.2 s is the shell's wall time; pytest itself reported 21.91 s.
- **Parallel:** yes. `pytest.ini` has `addopts = -n auto`.
- **In-process:** no. The step definitions run `scripts/work` as a subprocess (`tests/scenarios/test_supervision.py:71`). The suite is under 60 s, so this is no finding.
- **The 10 failures:** all are i31's w185 scenarios (r70, r83, r111–r116). w185 is `drafted`. These are the same 10 as in review 1, and none is i30's.
- **The gate as `work run` runs it:** `-p work_items --work-item w188 --whole-suite` gives `883 passed, 1 skipped, 10 xfailed, 2 xpassed`.
  - Every xfail reads "expected: accepted by w185, neither green nor withdrawn".
  - Both xpasses are w185's: the deprecated r83 scenario and the r70 apply scenario.

## Checks

- **w180** (`python3 -m pytest -q -p work_items --work-item w180`): `143 passed, 1 skipped, 56 subtests passed`. formulation is `group: guarantees`, so r23 has no scenario of its own.
- **w184** (`... --work-item w184`): `146 passed, 1 skipped, 56 subtests passed`.
- **w188** (`... --work-item w188`): `146 passed, 1 skipped, 56 subtests passed`.
  - This is the check the plan names. Its change is to agent text that no test reads (plan §4).
  - The text itself I verified by search: `40 turns|max-turns 40|max-turns` outside `.shop/`. It now appears only in `agents/code-scout.md:24` (80) and `README.md:174`, which is the 0.24.0 release note and is history.
- **w182**: withdrawn, no commits, so there is no check.
- **`tools check --base 4fbc25cd`** (exit 1):
  - `ruff`: 30 errors, the same 30 as review 1. None is on a line an i30 work-item commit added or changed.
    - `tests/scripts/stub_claude.py:189,190` FURB167 are the old `re.M` lines, moved down by w184's three-line insert at 186–188.
    - `.shop/work/i30/runs/supervision/3-formulate/splice.py:1,2,11,16` is the formulate round's scratch script. See Observations.
    - The rest are other initiatives' files.
  - `vulture`: clean.
  - `import-linter`: "the project states no import contracts". `CLAUDE.md` states none either, so there was nothing to read in its place.
- **`tools size --limit 300`**: printed nothing. No file is over the limit, touched or not.
- **`features deprecated`**: 5 deprecated scenarios.
  - **supervision @r83 (i31):** its replacement is w185's, which is drafted. It stays.
  - **supervision @r102 (i28):** its replacement's work-items are green. It is due for retiring, and it is not i30's.
  - **work-queue @r9 (i24):** due for retiring if w140 holds the replacement. Not i30's.
  - **work-queue @r1 and migration-tools @r15:** their work-items are withdrawn. Not i30's.
  - i30's only deprecated scenario was the old 40-turn r19 one, and w184 retired it.
- **`features bindings`**: "every binding names a scenario".
- **Dry-run and real mode**: the system has no dry-run mode of an operation. The only `--dry-run` is `git push --dry-run`, used as a probe at `scripts/supervise_review.py:41` and `scripts/supervise_faults.py:67`. No randomized agreement test applies.

## Removed and weakened tests

What I searched for, in the i30 work-item commits listed above:
- deleted `def test_` or step functions
- scenarios removed from `features/`
- parametrize or Examples changes
- `assert` lines removed or loosened
- `skip` or `xfail` added
- changed step patterns

What I found:
- **Removed:** the scenario "a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns (deprecated)" (supervision @r19), in `cd134f29`.
  - It proved `--max-turns 40`.
  - w184's Retires and plan §4 list it. w184 is green, and its binding went with it.
- **Changed:**
  - `supervision_proposal_steps.py` `reviewer_lists`: the plan dict now gives two reviewer results. No assert changed, and plan §4 lists it.
  - `supervision_rounds_steps.py:57` `questions_hold`: the pattern is narrowed to text that starts with `"`. Every use starts with a quote, and the plan lists it (decision 4).
  - `test_supervision.py:100` `is_green`: the pattern changed from `parse` to `re(w\d+)`. Every use names a `w<n>`, so no use is lost. It is not in the plan; the report's `setup` allowance covers it.
- **w188** (`2e913069`) and **w180** touch no test.

## Allowances

- **w184, `reviewer_lists`, `setup`: holds.** No `assert`, no expected value and no parametrize case changed.
- **w184, `is_green`, `setup`: holds.** Only the matcher changed. The body and its assert are byte for byte the same.
- **w180:** "none". Its commits touch no test.
- **w188:** "none" (report, `## Tests changed under an allowance`). Holds: the commit touches only `agents/code-scout.md`.

## Cannot verify

None. Every check above was run here, at `0e9620ac`.

## Findings

No finding is Critical and none is fix now.

1. **Minor, w184, observation: `scripts/supervise_rounds.py:111-112`.**
   - **What is wrong:** a gate result whose `questions` is `""` or `[""]` writes one empty question (`- `) under p1's `## Questions`, not r117's approval question. The cause is that `asked` is `[""]`, which is truthy.
   - **Why it is an observation:** no client sends this today, and r117 does not say whether an empty question is "no question". The plan (§5, D1) and the report leave it open.
   - **The fix:** drop blank questions before the `not asked` test, or write a line that settles the reading.
   - **Reproduction:** the w188 researcher's probe, `.shop/work/i30/runs/w188/1-research/notes.md` §2, cases c and d. It ran `python3 -m pytest -q -s -n 0 -W ignore .shop/scratch/w188-1-research/probe_r117.py`. It exited 0, and `p1.md ## Questions` held `- ` with no text. I confirmed the cause by reading line 111.
2. **Minor, w184, observation (carried from review 1): `scripts/supervise.py:210-215`.**
   - **What is wrong:** the r110 review-and-fix loop has no bound. It ends only on a review with nothing to fix now, a fix that is not green, or no review.
   - **Why it is an observation:** no line names a bound. Plan §5 and the report name it.
   - **Reproduction:** from the code: `while kept is not None and self.fix_work_item(kept): ... kept = self.branch_review()`.
3. **Minor, w180, observation (carried from review 1): `skills/formulating-features/SKILL.md:26`.**
   - **What is wrong:** it says pytest-bdd drops every character that is not a letter, a digit or a space. pytest-bdd keeps `_`.
   - **Why it is harmless:** the next sentence says to find the node id with `--collect-only -q | grep` and not to trust the derived name.
   - **The fix:** add the underscore to the kept characters.
4. **Minor, w180, drop (carried from review 1):** the subject of commit `4f1d4641`, "take no collection as a verdict", reads the opposite of its text. Commit messages are not rewritten.

## Shape

- **Size limit 300:** met. `tools size` prints nothing.
- **Module-map rows touched:**
  - `scripts/supervise*.py`: met. They hold `supervise_worker.py:53-54` (r19), `supervise_rounds.py:111-114` (r117) and `supervise.py:210-215` (r110).
  - `tests/scenarios/`: met. They hold `supervision_rounds_steps.py:52-67` and `supervision_proposal_steps.py:46-70`.
  - `tests/scripts/`: met (`stub_claude.py:186-188`).
  - `agents/code-scout.md` and `skills/formulating-features/SKILL.md` have no row and need none.
- **Code no line asks for:** none.
  - w188 changes text only, and that text serves r19.
  - The `break` at `supervise.py:213-214` serves r110, which fires on green only.
  - The approval question's wording at `supervise_rounds.py:113-114` serves r117.
- **Unreached code or steps:** none found, and vulture is clean.

## Coupling

- **pytest-bdd's test-function naming** (`SKILL.md:26`) is not a published contract.
  - The skill guards against a change: it selects by the node id from `--collect-only`, and it takes zero or several collected tests as no verdict.
  - Selecting by that node id is the stable form, and the skill already gives it.
- **The claude CLI's `--max-turns`** (`supervise_worker.py:222`) is a published flag. `agents/code-scout.md:24` now states the same value the code passes. The two numbers are kept in step by hand: nothing checks that the agent text matches `MAX_TURNS`. A test reading `agents/code-scout.md` for `MAX_TURNS["research"]` would tie them.

## Observations

- **The r117 empty-question case (finding 1).** Reproduction: `notes.md` §2, cases c and d, as above.
- **The r110 unbounded loop (finding 2).** Reproduction: from the code, as above.
- **The agent's turn text and `MAX_TURNS` are kept in step by hand.** Review 1's finding 1 was this drift. Reproduction: `git grep -n max-turns -- agents scripts`.
- **Formulate-round scratch scripts are tracked and fail ruff.**
  - The files are `.shop/work/i30/runs/supervision/3-formulate/splice.py`, plus i29's and i31's like it.
  - Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 4fbc25cd` lists `splice.py:1,2,11,16` for i30.
- **`.shop/work/i30/w184.md:4` and `w188.md:4` give `part_of: capability-proposal/i30-supervision`**, the short id. w180 and w182 give the full id. Reproduction: read the front matter.
- **Deprecated scenarios due for retiring, not i30's:** supervision @r102 (i28) and work-queue @r9 (i24). Reproduction: `features deprecated`, read with the work-items' `status:`.
