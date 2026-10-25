# Branch review of i30

**Verdict: DONE_WITH_CONCERNS.** There is one Important finding, triaged fix now: `agents/code-scout.md:24` still tells the researcher it has 40 turns (`--max-turns 40`), while `work run` now gives it 80 (r19, w184). Every check a work-item names was run and passes. Nothing is Critical. No test was removed or weakened outside what the plans list.

## Range and work-items

- Range: `4fbc25cd..5892599d` on `i25-review-findings-to-implementation`. The branch is shared by i25 through i31. The range also holds the commits of i25, i26, i27, i28, i29 and i31: their rounds, work-items, branch reviews and records. This review judges i30's work-items and names the other initiatives' commits only where a check reaches them.
- i30's work-items and their commits (between `ready -> claimed` and `claimed -> done`, less `work:` commits):
  - **w180** (formulation#r23, green): two commits.
    - `75cd7fda`: claim `225d3ed2` to done `5d20b71e`.
    - `4f1d4641`: the fix of review 6's F1, claim `ce37512e` to done `5ee2e95a`.
  - **w182** (withdrawn): no commit reached the branch. Claim `a0be069f` was followed by `90c3ec28 awaiting-answer`, then `df76cd2f` withdrawn.
  - **w184** (supervision r19, r110, r117, green): claim `85065878` to done `6df21f90`. Its commits are `cd134f29` (r19), `d40c0d26` (r117) and `b1b8562c` (r110). `1f4a0731` falls in that window but is w186's (i25).
- i30 commits outside any work-item:
  - Spec and round commits: `31738369`, `d54f006a`, `2f3698be`, `88f2de4c` and the `work note` commits. These are the integrate, gate, apply and formulate rounds, not work-item code. The changes to `features/` in `2f3698be` are the formulate round's, the path decision held-scenarios gives. They are not graded as work-item edits to `features/`.
  - Hand commits: `f7135e20` sets i30-supervision's ids by hand. `0eb572a2` adds w184's Retires section by hand. Both are named in Observations.

## Suite

`Suite: 885 passed, 10 failed at 5892599d in 21.58 s`

- Command: `python3 -m pytest -q -rfEx`. The 21.58 s is pytest's own wall time; `/usr/bin/time` could not be run here.
- It runs in parallel (`-n auto` in pytest.ini).
- The step definitions do not drive the entry point in-process: `test_supervision.py:71` runs `scripts/work` with `subprocess.run`. The suite is under 60 s, so that is no finding.
- The 10 failures are i31's w185 scenarios (r70, r83, r111–r116); w185 is `drafted`. With `-p work_items --work-item w184 --whole-suite` the result is `883 passed, 1 skipped, 10 xfailed, 2 xpassed`.
  - Each xfail reads "expected: accepted by w185, neither green nor withdrawn".
  - The 2 xpasses are w185's: the deprecated r83 scenario and the r70 apply scenario.
- No failure is i30's.

## Checks

- **w180** (`python3 -m pytest -q -p work_items --work-item w180`): `143 passed, 1 skipped, 56 subtests passed`. formulation is `group: guarantees`, so r23 has no scenario.
  - I also ran the skill's selection: `python3 -m pytest -q -k test_a_researcher_is_given_the_workitems_file_set_and_accepted_scenarios_and_a_limit_of_80_turns` gave `1 passed`. The derivation in step 4 collects the one test.
- **w184** (`python3 -m pytest -q -p work_items --work-item w184`): `146 passed, 1 skipped, 56 subtests passed`.
- **w182**: withdrawn, no commits, no check.
- **`tools check --base 4fbc25cd`**:
  - `ruff`: 30 errors. None is on a line an i30 work-item commit added or changed.
    - `tests/scripts/stub_claude.py:189,190` FURB167: the existing `re.M` lines, moved down by w184's three-line insert at 186–188.
    - `tests/scenarios/test_supervision.py:14` I001: an import block w184 did not touch.
    - `tests/scenarios/supervision_proposal_steps.py:118` RUF100: not on w184's lines 48–70.
    - `.shop/work/i30/runs/supervision/3-formulate/splice.py:1,2,11,16`: a scratch script that i30's formulate round committed (`88f2de4c`). See Observations.
    - The rest are other initiatives' files.
  - `vulture`: clean.
  - `import-linter`: "the project states no import contracts". Nothing for me to read in its place: CLAUDE.md states no contracts either.
- **`tools size --limit 300`**: printed nothing. No file is over the limit, touched or not.
- **`features deprecated`**: 5 deprecated scenarios.
  - supervision @r83: its replacement is w185's (drafted). It stays.
  - supervision @r102 (i28): its replacements w170, w171 and w172 are `green`, so it is due for retiring. Not i30's.
  - work-queue @r9: w140 (i24), which accepts r9, is `green`, so it is due for retiring if w140 holds its replacement. Not i30's.
  - work-queue @r1 and migration-tools @r15: every work-item that accepts them is withdrawn. Not i30's.
- **`features bindings`**: "every binding names a scenario".
- **Dry-run and real mode**: the system has no dry-run mode of its own. The only `--dry-run` is `git push --dry-run`, used as a probe in `supervise_review.py:41` and `supervise_faults.py:67`. No randomized agreement test applies.

## Removed and weakened tests

What I searched for: in i30's work-item commits, deleted `def test_` or step functions, scenario removals in `features/`, parametrize or Examples changes, `assert` lines removed or changed, added `skip` or `xfail`, and changed step patterns.

- **Removed**: the scenario "a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns (deprecated)" (supervision @r19), in `cd134f29`.
  - It proved `--max-turns 40`.
  - w184's Retires lists it, and so does plan §4. w184 is green. Its binding is gone with it: `features bindings` is clean.
- **Changed, kept**:
  - `tests/scenarios/supervision_proposal_steps.py` `reviewer_lists` (the r74 Given) now gives the reviewer `[findings, nothing]`.
    - It proves one fix work-item, drafted under p1 for the two findings.
    - Plan §4 lists it. No assert changed.
  - `tests/scenarios/supervision_rounds_steps.py:57` `questions_hold`: the pattern is narrowed to text that begins with `"`.
    - Plan §4, decision 4, lists it.
    - Every use in the features begins with a quote (supervision.feature:1231, :1257); `w1's ...` at :690 is another step. The assert is unchanged.
  - `tests/scenarios/test_supervision.py:100` `is_green`: the pattern changed from `parse("{name} is green")` to `re(r"(?P<name>w\d+) is green$")`.
    - The plan does not list it; the report's allowance does.
    - Every `Then/And <x> is green` in the features names a `w<n>` (:367, :869, :1301), so no use was lost. The assert is unchanged.
- None other.

## Allowances

- w184, `reviewer_lists`, `setup`: **holds**. Only the plan dict changed. No `assert`, no expected value and no parametrize case changed.
- w184, `is_green`, `setup`: **holds**. Only the step's matcher changed, and the body and its assert are byte for byte the same.
- w180: "none" in all four reports. Its commits touch no test.

## Cannot verify

None. Each check above was run.

## Findings

1. **Important, w184, fix now: `agents/code-scout.md:24`.**
   - **What is wrong:** it says "`work run` gives you 40 turns (`--max-turns 40`)", while `scripts/supervise_worker.py:54` now gives the researcher 80 (`cd134f29`).
   - **Why it matters:** the researcher is told a limit that is false. It is told to write its notes "well before the last turn", so it budgets for 40. r19's raise, which q7 asked for because researchers ran out of turns, then does not reach the researcher. This contradicts r19's Behaviour line as the worker reads it.
   - **The fix:** state 80 (`--max-turns 80`) in `agents/code-scout.md:24`. The file was outside w184's file set; drafting a fix should add it there.
   - **Reproduction:** search the repository outside `.shop/` for `40 turns|max-turns 40`. Two lines come back: `agents/code-scout.md:24` and `README.md:174`. The README line is the 0.24.0 release note, which is history and is fine.
2. **Minor, w184, observation: `scripts/supervise.py:210-215`.**
   - **What is wrong:** the r110 loop has no bound. A branch review that lists fix-now findings after every green fix keeps the run drafting, delivering and re-reviewing.
   - **Why it is hardening:** no line names a bound, and r111 asks the run to take every node through. The plan (§5) and the report name this open case.
   - **Reproduction:** from the code, not run. `while kept is not None and self.fix_work_item(kept): ... kept = self.branch_review()` only ends on a review with no fix-now findings, a fix that is not green, or no unread commit.
3. **Minor, w180, drop: commit `4f1d4641`'s subject says "take no collection as a verdict".** The text says the opposite: "A selection that collects no test, or more than one, is no verdict". Review 8 named this already. Commit messages are not rewritten.
4. **Minor, w180, observation: `skills/formulating-features/SKILL.md:26`.**
   - **What is wrong:** it says "every character that is not a letter, a digit or a space dropped", but pytest-bdd keeps `_`. Titles such as `... v_t1` show it.
   - **Why it is harmless:** the next sentence says not to trust the derived name, and to find the node id with `--collect-only -q | grep`.
   - **The fix:** add the underscore to the kept characters.

## Shape

The rules of `CLAUDE.md`:

- **Size limit 300**: met. `tools size` prints nothing, and every file i30 touched is at or under 300.
- **Module-map rows touched**:
  - `scripts/supervise*.py`: met. The researcher's limit is in `supervise_worker.py:53-54`, the r117 question in `supervise_rounds.py:112-114`, and the r110 loop in `supervise.py:210-215`, all within `work run`.
  - `tests/scenarios/`: met. The steps are in `supervision_rounds_steps.py:52-67` and `supervision_proposal_steps.py:46-70`.
  - `tests/scripts/`: met. The stand-in change is at `tests/scripts/stub_claude.py:186-188`.
  - `skills/formulating-features/SKILL.md` is a skill and has no row.
- **Code no line asks for**: none. The break at `supervise.py:213-214` serves r110, which fires only on green. The wording of the approval question at `supervise_rounds.py:113-114` serves r117, in r68's form of a question with readings and a recommended one.
- **Code and step definitions no scenario reaches any more**: none found. vulture is clean.

## Coupling

- **pytest-bdd's test-function naming** (`skills/formulating-features/SKILL.md:26`): the skill derives a test name from a title the way pytest-bdd does internally. That rule is not a published contract.
  - It would break if pytest-bdd changed how it names tests. The skill already guards against this: it says to collect and grep for the node id, and it treats zero or several collected tests as no verdict.
  - What would make it stable: select by the node id that `--collect-only` prints, which the skill already says.
- **The claude CLI's `--max-turns`** (`supervise_worker.py:54`): a published flag. Nothing more is relied on.
- **pytest-bdd internals**: the warnings about `_register_fixture` and `FixtureDef` baseid come from pytest-bdd's own `compat.py`, not this repository's code. Nothing to do here.

## Observations

- `.shop/work/i30/runs/supervision/3-formulate/splice.py` holds ruff errors (I001 and SIM115) and is tracked. It was committed by `88f2de4c`, the formulate round's merge: a round's scratch script, not a work-item's. Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 4fbc25cd` lists its lines 1, 2, 11 and 16.
- `.shop/work/i30/w184.md:4`: `part_of: capability-proposal/i30-supervision` is the short id, where w180 has the full `capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i30-formulation`. It was written by `44704434 work add`. Reproduction: read the front matter of the two files.
- Hand commits:
  - `f7135e20` set i30-supervision's ids by hand, because q8 r114 is not yet delivered.
  - `0eb572a2` gave w184 its Retires section by hand, because `work add` has no `--retires`.
  - Both are named in their messages. Neither belongs to a work-item.
- Deprecated scenarios due for retiring, not i30's:
  - supervision @r102 (i28's w170, w171 and w172 are green).
  - work-queue @r9 (i24's w140 is green).
  - Reproduction: `features deprecated` together with the work-items' `status:`.
