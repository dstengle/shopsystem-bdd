# Branch review of i48 (supervision r188, r189)

**Verdict: DONE_WITH_CONCERNS.** w238's own change is sound. It does what r188 and r189 and the plan's decisions 1 to 4 ask, it touches nothing under `features/`, and the one test it changes is the one the plan lists. No w238 finding is triaged fix now.

The concern is the range itself. The initiative branch is `main`, so `Base..HEAD` carries 961 commits that belong to no i48 work-item. These are other initiatives' intake rounds, spec applies, formulate rounds, hand edits and implementations (i49 to i64, q17 to q45). Among them are changes under `features/` and removed or loosened tests. By this review's rules those are a Critical finding and Important findings. I triage them as observations: they are not wrong answers, crashes or lost data, and they are other initiatives' work. They still go to the person through the status.

Every check was given by a run in the brief, so nothing is listed under Cannot verify.

## Range reviewed

- `6cf63096..85638a50`, on the initiative branch `main`. All runs were made at `85638a50`.
- The range has 991 commits.
  - **30 belong to w238.** 27 are transitions or answers (`fa887c01` work add through `85638a50` done -> green).
  - **Three are w238's implementer commits:**
    - `4b6996da`: r188 plus the r189 steps (red). Touches `scripts/supervise_change.py`, `tests/scenarios/supervision_reintegrate_steps.py` and `tests/scripts/test_supervise_change.py`.
    - `3e242ec9`: r189. Touches `scripts/supervise_change.py` and `tests/scripts/test_supervise_change.py`.
    - `7c39e421`: r189's step, so that g1's apply round gives the unheld answer. Touches `tests/scenarios/supervision_reintegrate_steps.py`.
  - **961 belong to no work-item.** See finding C1.
- Work-items of i48: w238 (`under: supervision`, accepts supervision#r188@0.29 and #r189), status green. Its capability-proposal `i48-supervision` is formulated.

## Suite

- **Suite: 1091 passed, 0 failed at 85638a50 in 35.35 s.** The full line: 1 skipped, 23 xfailed, 14 xpassed, 56 subtests passed.
  - Command: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w238 --whole-suite`, exit 0.
- **Parallel:** yes (`-n auto`, xdist).
- **In-process:** no. Step definitions drive the scripts through `subprocess.run` (`tests/scenarios/conftest.py:34`, `:111`).
  - The suite is under 60 s, so this is no finding.
- **The 23 xfailed** are requests scenarios (accepted by w212 or requests-deda9fa6) and four supervision scenarios accepted by w243. None is r188 or r189.
- **The 14 xpassed** are not named, because the run's `-rfEx` does not report XPASS. See observation O6.
- **Dry-run and real mode:** the system has no dry-run mode of one of its own operations. The only `--dry-run` is git's push probe (`scripts/supervise_faults.py:71`, `scripts/supervise_review.py:55`). So no agreement test is owed.

## Checks

All at `85638a50`.

- **w238's check (its scenarios):** `python3 -m pytest -q -n auto -p work_items --work-item w238`, exit 0: 186 passed, 1 skipped, 56 subtests passed in 6.62 s. r188 and r189 pass.
- **`tools check --base 6cf63096`:** exit 1.
  - **ruff:** 48 errors.
    - Three are in lines w238 added (finding M2):
      - `scripts/supervise_change.py:83` B023;
      - `tests/scenarios/supervision_reintegrate_steps.py:92` RUF100;
      - `tests/scenarios/supervision_reintegrate_steps.py:101` RUF100.
    - Others are in files w238 touched but not on its lines:
      - `supervise_change.py:103` and `:130` (B023, `merge_lists` and the drafts-path rewrite as they were before);
      - `supervision_reintegrate_steps.py:13` F401 and `:225` FURB167.
    - The rest are in other initiatives' files: `supervise_merge.py`, `supervision_integrate_steps.py`, `supervision_proposal_steps.py`, `test_supervision.py`, `work_queue_list_steps.py`, `stub_claude.py`, `test_supervise_answers.py`, `test_supervise_merge_rerun.py`.
    - Some are in throwaway scripts kept under `.shop/work/i50`, `i55`, `i59`, `i60` and `i63` (`splice.py`, `cmp.py`, `mk.py`). See observation O5.
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:100` unused variable `notes`. Not a w238 file.
  - **import-linter:** "the project states no import contracts".
- **`tools size`:** exit 0, printed nothing. No tracked Python file is over 300 lines, so none that the branch touched is over.
- **`features deprecated`:** exit 0, 23 deprecated scenarios.
  - None was deprecated by w238.
  - One names a replacement title that exists nowhere: r163's, "for: r209 and r210 | no scenario has that title" (finding I3).
- **`features bindings`:** exit 0, "every binding names a scenario".

## Removed and weakened tests

I searched the change for:
- removed `def test_` lines;
- removed `@given`, `@when` and `@then` steps;
- removed or changed `assert` lines;
- removed `Scenario` lines and parametrize lists;
- added `xfail` and `skip`.

No `xfail` or `skip` was added.

**w238 changed one test, and its plan lists it.**

- **`tests/scripts/test_supervise_change.py::test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal`, line 37.**
  - It proved that the round's own proposal p1 ends with `adds: [thing#r5]`, the old full replacement.
  - It now proves `adds: [thing#r1, thing#r5]`: r188, which keeps the held ids.
  - It is an exact assertion of the same strength, and its p2 assertions are kept.
  - Plan part 4 lists it under "Tests the decisions break". It holds.
- **The Given `questions_and_answers`** (`p1` generalised to `[pg]1`) and **the Then `integrate_after_apply`** (now `[pg]1`, with the same asserts) are the same tests, made more general. Neither is weakened.

**Tests removed or loosened by commits of no i48 work-item.** No i48 plan lists any of them, so each is Important. They are all triaged observation (finding I2).

1. `tests/scripts/test_supervise_answers.py::test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case` (diff line 4070) was deleted.
   - It proved `supervise_glossary.names_one`, the r162 whole-word match.
   - The function is removed with r162, which r209 and r210 replace.
2. `tests/scenarios/supervision_faults_steps.py` `is_failed` (diff 3511) is loosened. The clean-status assert now excludes `.shop/work/i2` (r218, commit 94f0a748).
3. `tests/scenarios/requests_flow_steps.py` `show_prints` (diff 3215) is loosened. It now asserts only the first line of `work show`'s output, because show now prints more (r59).
4. These step definitions were removed or replaced:
   - "the session runs `work status`", replaced by `work list` (r50);
   - "i1's glossary-proposal g1 is awaiting-answer$";
   - the two-question Given for w1;
   - "w1's question ... has no answer";
   - "it prints the question" (`work_queue_list_steps.py`);
   - "an initiative ... under .shop/work/ that is <state>, whose work-items" (`work_queue_status_steps.py`, r23 retired).
5. These scenarios were removed with no deprecated form at Base:
   - requests r39 (now r56), r43 (now r58), r14;
   - supervision r9 (now r212), r162 (now r209), r105 (now r213);
   - work-queue r23 (two scenarios).
   - Commits 0e9fa09f, a700415c and 19c0bc4d say these were deprecated first. 153518ea, aff8ddf1, fce410f4 and 99896662 then removed them.
   - The whole change does not show the steps in between. I name them as removed, and these commits as where to confirm.

## Allowances

- **3-implement**, `## Tests changed under an allowance`: "The plan lists `test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal`: its p1 assertion is now `adds: [thing#r1, thing#r5]`".
  - Commit 4b6996da changes exactly that one assertion, as plan part 4 says.
  - It is a plan-listed test, not a setup or interim row, and it claims nothing more. It holds.
- **6-implement:** "none (the p1 assertion ... rewritten at 440352d6 as plan part 4 says)". It holds.
- **9-implement:** "none beyond the earlier p1 assertion rewrite". It holds. The new unit test it adds removes no assert.
- **10-implement:** "none". It holds. 7c39e421 adds one `plan[...]` line to a Given and changes no assert.
- **11-implement:** "none". It holds, as no commit came from that stage.

## Cannot verify

None. Every check this review names is given by a run in the brief at `85638a50`.

## Findings

### C1. Critical, work-item none, observation: the range holds 961 commits of no i48 work-item, with changes under `features/`

- **Where:** `features/requests.feature`, `features/spec-consistency.feature`, `features/supervision.feature` and `features/work-queue.feature` (diff lines 1376-2358).
  - The r188 and r189 scenarios (`features/supervision.feature:1170-1193`) were added by c1927b85, "features: supervision r188 r189 formulated". That is a formulate round of i48's proposal, with no work-item.
  - All the others come from formulate rounds and hand edits of i49 to i64: e4e58445, 6ce69452, a3da368c, af49d7ff, bb2caaeb, fe960a7a, 19c0bc4d, 64726942, 566b7302, 61c39f01, 0e9fa09f, a700415c, 153518ea, aff8ddf1, fce410f4, ec876396, 2fb83d16, 627b4a71, d968719a, 383ee065, bddb538f.
- **What is wrong:** none of these commits is a work-item removing, with its binding, a deprecated scenario it lists under Retires.
  - Code and test commits of other initiatives are in the range too, also with no i48 work-item. Examples: 99896662, afc4aa72, ab71c3fc, d8f57cc8, 94f0a748, a9cb7536, fd8364d1, 4e206ec4, 4fa77b43.
  - Among them are the removed and loosened tests in finding I2.
- **Why it matters:** `main` is shared by every initiative. `Base..HEAD` is therefore not i48's change, and a review of it reviews other initiatives' delivery a second time, against i48's work-items, which do not ask for it.
- **What I verified:** w238's three implementer commits touch only its fileset. The `features/` change does not come from them: the brief's change is the whole range, and the 12-review's `git show --stat` of those three commits named no `features/` path.
- **Fix:**
  - Give a branch review the change of its initiative's own commits, or a branch per initiative, so that `Base..HEAD` is that initiative's.
  - Or let the brief mark each commit with the initiative it belongs to, so that one of another initiative is not "none".

### I1. Important, w238, observation: the module-map row of `scripts/supervise_change.py` no longer says what the module does

- **Where:** `CLAUDE.md`, row `scripts/supervise_change.py`.
- **What is wrong:** the row says the module writes "one drafted capability-proposal for each capability it names and ... one drafted glossary-proposal".
  - Since r187, and now r188 and r189 (`supervise_change.py:74-84`, `:127`, `:146-154`), it also redrafts the lists of the proposal the round was started for, whether capability or glossary.
  - That proposal keeps the ids and terms the change list does not name.
- **Fix:** add r188 and r189, the redraft of the round's own proposal, to the row.
- **Grade:** CLAUDE.md asks each concern to be in its row. This is Minor in effect, but graded at the rule.

### I2. Important, work-item none, observation: tests removed or loosened outside any i48 plan

These are the items 1 to 5 listed under "Removed and weakened tests" above. Each comes from another initiative's work under a line that replaced or retired the old one (r209/r210, r218, r59, r50, r212, r213, r62). Each was then reviewed by that initiative's own branch reviews (a746612b, 9e8c48dc, 850ce9d3, ff632c3a … 52de5b39).

- **What is wrong:** no i48 plan lists them.
- **Why it matters:** in this range they show as unexplained losses of coverage.
- **Fix:** none for i48. C1's fix keeps them out of this review.

### I3. Important, work-item none, observation: a deprecated scenario names a replacement title that does not exist

- **Where:** `features/supervision.feature` near diff line 1926, r163's scenario outline, "Deprecated for: r209 and r210".
- **What is wrong:** `features deprecated` prints "no scenario has that title". Its replacements, the r209 and r210 outlines, pass in the suite run: they are not among its xfails.
- **Why it matters:** the deprecated scenario can neither be retired nor be traced to its replacement by the tool.
- **Fix:** have the scenario name the replacement scenarios' titles, then retire it with its binding.
- **Work-item:** it came from af49d7ff, i51's formulate round.

### M1. Minor, w238, observation: `redraft_lists` loses the round's ids for a list the proposal's front matter lacks

- **Where:** `scripts/supervise_change.py:81-83`.
- **What is wrong:** each list is rewritten with `re.sub(r"(?m)^%s:.*$" % field, ..., count=1)`. If the held file has no `removes:` (or `adds:` or `changes:`) line, nothing matches, and the ids the change list gives there are silently dropped. `rewrite_lists` (`:70-72`), which this replaces for the own proposal, wrote all three lists.
- **Why it is only hardening:** every proposal `work run` writes has all three lines (`:135`, `:158`), and so do the r188 and r189 Givens.
- **Reproduction:** taken from what I read and the 12-review's probe (`.shop/scratch/w238-12-review/test_probe.py`). With p1 holding `adds: [thing#r1]` only, and a change list adding thing#r5 and removing thing#r2, p1 ends with `adds: [thing#r1, thing#r5]` and no `removes:`.
- **Test that would show it** (not run): a unit test of `write_proposals` on that p1, asserting `removes: [thing#r2]`.
- **Fix:** append a missing field line before the closing `---`.

### M2. Minor, w238, observation: three new lint findings in w238's lines

- `scripts/supervise_change.py:83` B023: the lambda reads loop variables `field` and `mine`. It is a false positive, because `re.sub` calls the lambda before the loop moves on.
- `tests/scenarios/supervision_reintegrate_steps.py:92` and `:101` RUF100: an unused `# noqa: E731`.
- Reproduction: the `tools check` run above.
- Fix: build the replacement string before calling `re.sub` (or pass it as a default), and drop the two `noqa` comments.

### M3. Minor, w238, drop: duplicated drafts-path rewrite and a stale docstring

- **Duplicated code:** `scripts/supervise_change.py:128-131` and `:149-152` repeat the "The drafts of this proposal are in …" rewrite.
- **Stale docstring:** `write_proposals`' docstring (`:107-110`) still says the own proposal's "lists and its drafts path [are] replaced". Since r188 its lists are redrafted, keeping the unnamed ids.
- **Module header:** it does not name r188 or r189, as plan part 2 said it would.
- **Triage:** polish with no observable change.

### M4. Minor, w238, observation: r189's Given arranges a round its text does not name

- **Where:** `tests/scenarios/supervision_reintegrate_steps.py`, the step `integrate_redrafts_g1`.
- **What is wrong:** "a round of the kind integrate is started for g1, redrafts the term "ledger" …" also arranges g1's apply round to give `unheld_answers` (7c39e421). That is what makes r221 start the integrate round. So r189's scenario depends on r221's route through a stub the feature file never names.
- **Why it is not more:** the person asked for this on 2026-11-02, with no feature change.
- **Check that would show it fixed:** a later formulate round writes the apply round as its own Given ("the apply round for g1 applies nothing, giving that g1's answers give what its drafts do not hold"), and the step only sets up the integrate round.

### M5. Minor, work-item none (behaviour as it was before, kept by w238's plan decision 4), observation: a held `glossary.md` is overwritten by an integrate round not started for it

- **Where:** `scripts/supervise_change.py:155-160`.
- **What is wrong:** an integrate round started for a capability-proposal or for the initiative, whose change list names the glossary while the initiative already holds `glossary.md`, writes a fresh `glossary.md`. The held one's terms, Questions and Answers are lost.
- **Why it is an observation:** no line names the case (plan part 5, open case 1), and r171's scenario is the fresh write.
- **Test that would show it** (not run): a unit test of `write_proposals(found_with_glossary, "new/", "p1")` with `glossary.md` held at awaiting-answer and holding a Questions section, asserting its Answers survive.
- **Fix:** a line first (an integrate round naming the glossary while a glossary-proposal is held merges into it, as r187 does for capabilities), through integrating-a-proposal.

## Shape

- **Size limit (CLAUDE.md):** met.
  - `tools size` prints nothing.
  - The w238 files have 161 (`supervise_change.py`), 226 (`supervision_reintegrate_steps.py`) and 80 (`test_supervise_change.py`) lines, as the 12-review measured.
- **Module map row `scripts/supervise*.py` / `supervise_change.py`:** the code sits in the right module, but the row's text is not updated (finding I1).
- **Module map row `tests/scenarios/`** (one `<capability>_*_steps.py` a concern): met. The r188 and r189 steps are in `supervision_reintegrate_steps.py`, the module of re-integration rounds.
- **Module map row `tests/scripts/`:** met. The new unit test is in `tests/scripts/test_supervise_change.py:100-114`.
- **Unreached code:** none from w238.
  - `rewrite_lists` (`:58-72`) is still reached by the apply round (r145).
  - `merge_lists` (`:94-104`) is still reached by the r187 path.
  - `supervise_glossary.names_one`, `terms_of` and `proposals_of` were removed with r162, by another initiative.
- **Refactor called for (M3):** one helper for the drafts-path sentence. It is complete when `grep -c "The drafts of this proposal are in %s" scripts/supervise_change.py` gives 1 and `test_supervise_change.py` still passes.

## Coupling

- **pytest-bdd on pytest internals.**
  - **Where it relies on more than pytest publishes:** pytest-bdd's `compat.py:28` calls `request._fixturemanager._register_fixture` with a nodeid. Every scenario module depends on it (318 `PytestRemovedIn10Warning` in the suite run).
  - **Would it break if pytest changed behind its contract:** yes. Pytest 10 removes the nodeid and baseid forms, and every scenario would stop collecting.
  - **What would make it stable:** pin `pytest<10` and a known pytest-bdd version with the project's interpreter (`tools install`), or move to a pytest-bdd release that passes the node.
- **pytest-bdd tags as marks.** Each `@rNNN` and `@deprecated` tag becomes an unregistered mark (`PytestUnknownMarkWarning`).
  - **Would it break:** yes, under `--strict-markers`, or if pytest-bdd stops turning tags into marks. The `--work-item` selection (`scripts/work_items.py`) relies on the tags.
  - **What would make it stable:** register the marks in `conftest.py` (`pytest_configure`) or rely on pytest-bdd's tag API alone.
- **w238 adds no new external dependency.** `supervise_change.py` uses only the standard library and `workqueue`.

## Observations

One line each, with its reproduction.

- **O1 (M1):** an own proposal lacking a list line loses that list's ids. Reproduction: `.shop/scratch/w238-12-review/test_probe.py` (12-review) gave p1 with no `removes:` line.
- **O2 (M2):** three new ruff findings in w238's lines. Reproduction: the `tools check` run, `supervise_change.py:83`, `supervision_reintegrate_steps.py:92` and `:101`.
- **O3 (M4):** r189 reaches its integrate round only through a stubbed apply result its Givens do not name. Reproduction: `supervision_reintegrate_steps.py`, `integrate_redrafts_g1`, sets `plan["round:apply:g1"]`.
- **O4 (M5):** `glossary.md` held, plus an integrate round for p1 naming the glossary, means a fresh overwrite. Reproduction: read at `supervise_change.py:155-160`. Test marked not run.
- **O5:** `tools check` lints throwaway scripts kept under `.shop/work/*/runs/` (`splice.py`, `cmp.py`, `mk.py`). Reproduction: the `tools check` run, 23 of the 48 ruff errors.
- **O6:** the suite has 14 XPASS that `-rfEx` does not name. An expected failure that passes may be a scenario whose work-item can turn green. Reproduction: the suite run's summary line, "14 xpassed"; the test that would show them is `-rX`.
- **O7 (I3):** r163's deprecated scenario names no existing replacement. Reproduction: the `features deprecated` run, "for: r209 and r210 | no scenario has that title".
