# Branch review of i54

**Verdict: DONE_WITH_CONCERNS.** i54's own work, w231 (supervision#r187), is clean. It adds only step definitions and one import, and nothing in it is fix now. The range `Base..HEAD` is on `main`, so it also holds the work of fourteen other initiatives (i45, i47 to i53, i55 to i60). In that part there is one Critical finding, carried from i51 (w230 removed the r162 outline with no `## Retires` entry). There is also one Important finding no review has raised: r209 and r210, and w230's code, contradict design-decision 0073, which supervision rests on. Neither is triaged fix now, so `questions` is empty. Both go to the person through this file and the status.

## Range

- `a2a53b36c02b74d046b7a490d802403f3f1828a9..eb1a30ac52528d23385846ad51c1947066590847` (branch `main`), 331 commits.
- i54's work-items:
  - w231 (`green`, under supervision, accepts supervision#r187). Its commits: `6e55ddd3` (added), `82832c5e`, `56f6efb6`, `f5f6671b`, `156d2b2b` (transitions), `afc4aa72` (steps), `3cc54654`, `eb1a30ac` (done, then green).
- i54's capability-proposals:
  - `i54-supervision`: `formulated`.
  - `i54-work-queue`: **`awaiting-answer`**. Its second question, "Are the lines of work-queue approved as drafted?", has no answer. q20's lines 1 and 2 (work show of a request, work list without requests) are not delivered, so under work-queue r47 the initiative stays `started`. This review covers the delivered part only.
- i54's own round commits, with no work-item: `49d8369f`, `c1aa3af9`, `97c440d1` (integrate), `985c0204`, `afb68414`, `ec944d15` (spec r187), `bb2caaeb` (formulate r187), `11726fc2`, `346c2612`, `59256f4c`, `147ad589`, and the i54 `work note` commits.

## Suite

`Suite: 1067 passed, 0 failed at eb1a30ac in 32.74 s`. The full line is "1067 passed, 1 skipped, 11 xfailed, 3 xpassed, 696 warnings, 56 subtests passed".

- **Parallel:** yes, `-n auto`.
- **In-process:** no. `tests/scenarios/test_supervision.py:80` (`run_work`) starts `work` as a subprocess. `test_work_queue.py:194` drives one move in-process.
- The suite is under 60 s, so neither is a finding.
- The 11 xfails are all w212's `test_requests.py` scenarios ("accepted by w212, neither green nor withdrawn").
- The output does not name the 3 xpassed tests, because `-rfEx` leaves XPASS out of the summary (see Observations).

**Dry-run and real mode:** the system has no dry-run mode of one of its own operations. The only `dry-run` in `scripts/` is `git push --dry-run`, used as a probe at `supervise_review.py:55` and `supervise_faults.py:71`. No agreement test applies.

## Checks

All runs at `eb1a30ac`.

- **w231's scenarios** (`pytest -n auto -p work_items --work-item w231`): exit 0, "181 passed, 1 skipped, 56 subtests passed in 6.65s". The r187 scenario passes. Its warning lines name it, `test_an_integrate_round_started_for_a_capabilityproposal_whose_change_list_names_another_capability...`.
- **`tools check --base a2a53b36`**: exit 1.
  - **ruff:** 17 errors. On files the branch touched:
    - `tests/scenarios/test_supervision.py:14` I001. This file is touched by w231, but the import order was wrong already at w231's base (w231's review, finding 1).
    - `tests/scenarios/supervision_integrate_steps.py:87` RUF059.
    - `tests/scenarios/supervision_proposal_steps.py:102` and `:137` RUF100.
    - `tests/scripts/test_supervise_answers.py:9` and `:10` RUF100.
    - Tracked round scratch scripts: `.shop/work/i50/runs/supervision/{2-apply,3-formulate}/splice.py` (SIM115 ×6) and `.shop/work/i59/runs/i59/1-integrate/cmp.py` (I001, SIM115 ×2, C402, FURB167).
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". This is no contract checked, not a failure.
- **`tools size`**: exit 0. It printed nothing, so no file is over the limit, touched or not.
- **`features deprecated`**: exit 0, 15 deprecated scenarios. One line resolves to no scenario: the r163 outline, "for: r209 and r210 | no scenario has that title". Its replacements' work-item, w230 (i51), is `green`, so this deprecated scenario is due for removal (Finding 4).
- **`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for:
- `-def test_` lines, `-` lines holding `assert`;
- parametrize cases and Examples rows dropped;
- `skip` or `xfail` added;
- step definitions whose patterns or assertions changed.

What I found:

1. **Deleted:** `tests/scripts/test_supervise_answers.py:59`, `test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`, in w230 (i51). It proved that `supervise_glossary.names_one` matches a glossary term or a glossary-proposal name as a whole word in any case, and no partial word (r162). w230's plan §4 lists it under "Tests the decisions break" (`.shop/work/i51/runs/w230/2-plan/plan.md:35`), so it is not a finding.
2. **Removed:** the `@r162` Scenario Outline, `features/supervision.feature` (formerly ~1346), both examples, in w230 (i51). It proved that a question naming the term "ledger" or the glossary-proposal g1 goes to no session under a delegation. w230's plan §4 lists it (plan.md:34). The removal through `features` under no `## Retires` entry is Finding 1.
3. **Widened, not weakened** (`supervision_delegation_steps.py`):
   - `glossary_proposal_awaiting` (Given), now with an optional question;
   - `two_unanswered` (Given), now for `w\d+`;
   - `question_unanswered` (Then), now for `w1|g1`. It keeps the same assertion.

w231 removed or weakened nothing: its diff only adds lines (`supervision_merge_steps.py`, new, 39 lines, and one import).

## Allowances

- w231 report, `## Tests changed under an allowance`: "none". This holds, because w231 changed no existing test.
- w230 (i51) report: "none". The removals are plan-listed, so none is needed.

## Cannot verify

None. Every check this review takes is in the brief's runs at `eb1a30ac`.

## Findings

### 1. Critical, w230 (i51, not i54), observation: `features/supervision.feature` (r162 outline, ~1346 at its merge), a deprecated scenario removed that its work-item does not list under Retires

- **What is wrong.** Commit `998966626` removes the `@r162 @deprecated` outline. `.shop/work/i51/w230.md` has no `## Retires` section, and w230's plan says so (plan.md:7).
- **Why it matters.** The only change to `features/` a work-item may make is removing a deprecated scenario its work-item lists under Retires.
- **Why it is not fix now.** No answer is wrong and no data was lost. r162 is in supervision's `retired:`, and `features bindings` is clean. i51's branch review 1 raised this already (its Finding 1), and i51 is `done`.
- **Fix.** The person rules on it. Either record the removal under a `## Retires` of w230, or restore the outline and retire it through r123. The root is Finding 4: a `Deprecated for:` that gives ids, not a title.

### 2. Important, w230 (i51, not i54) with the spec commit `2c74c3a6`, observation: r209/r210 and `scripts/supervise_answers.py:74` contradict design-decision 0073, which supervision `rests_on`

- **What is wrong.** `spec/decisions/0073-the-glossary-is-a-target-of-spec-work.md:15` and its summary (l.3) say: "a question that names a term or a glossary-proposal is the person's, never answered under a delegation".
  - r210 now gives such a question to a session "whatever words it uses".
  - `supervise_answers.py:74` asks every open question of an awaiting-answer work-item or capability-proposal (`asking`, l.51-58).
  - 0073 is still `status: proposed` and unamended. Nothing supersedes it.
- **Why it matters.** The design-decisions a capability rests on are binding. The spec, the code and the decision now disagree, and the next reader of 0073 will expect the opposite of what `work run` does. i51's branch review did not raise this.
- **Fix.** The person rules on which holds. Either amend 0073 (or supersede it with a decision that a glossary-proposal's own questions are the person's, as r209 says), or retire r209/r210.
- **What I verified** (the risk: a glossary-proposal's question reaching a session): `asking()` takes only `work-item` and `capability-proposal` kinds (`supervise_answers.py:56`). So r209 holds in code, and the r209 scenario passes in the suite.

### 3. Important, none (round and bookkeeping commits of i45, i47 to i53, i55 to i60), observation: the range holds 323 commits that belong to no i54 work-item

- **What is wrong.** i54's branch is `main`, so `Base..HEAD` interleaves every initiative delivered meanwhile. Of 331 commits, 8 are w231's. The rest are of these kinds:
  - workflow bookkeeping: `work note`, transitions, `work outcome`/`turn`/`request`, round merges;
  - spec and formulate commits: `78f23fec`, `86104ff4`, `d27c27d3`, `2c74c3a6`, `deda9fa6`, `ec944d15`, `e4e58445`, `6ce69452`, `a3da368c`, `af49d7ff`, `bb2caaeb`;
  - code commits of other initiatives' work-items: `a807b5b7` (w228, i50, r173) and `998966626` (w230, i51);
  - two hand changes: `73758cad` "i51 hand repair" and the step `started_fulfilling_bare` (`supervision_integrate_steps.py:22`, r180). w229 (i49), which accepts r180, is `awaiting-answer` with fileset `[scripts/supervise_rounds.py]`, so this step reached `main` through no green work-item.
- **Why it matters.** A branch review of one initiative cannot tell its change from another's. Code from the other work-items was reviewed by their own initiatives' branch reviews (`a746612b` i50, `9e8c48dc` i51). The r180 step was reviewed by none.
- **Fix.** Either `work run` gives a branch review only its initiative's commits and their change, or each initiative gets its own branch. Separately, the r180 step needs a work-item that owns it (w229's open question asks this).

### 4. Minor, none (formulate `af49d7ff`, i51), observation: `features/supervision.feature:1336-1338`, the r163 outline is deprecated "for: r209 and r210", which names no scenario, and its replacements' work-item w230 is `green`

- **What is wrong.** `features deprecated` prints "no scenario has that title".
- **Why it matters.** r73/r123 draft and retire from a `Deprecated for:` that names a scenario title. This one cannot be resolved, so nothing will retire the outline, and it keeps running as a scenario of a retired line.
- **Fix.** Give the replacement's title in `Deprecated for:`, or have the next work-item that touches supervision retire the outline under `## Retires`.

### 5. Minor, none (formulate `6ce69452`, i49), observation: `features/supervision.feature:1427-1429`, r93 is deprecated "for: removal", though r180 replaces it

- **What is wrong.** The tag says removal, but r180's scenario is its replacement.
- **Why it matters.** It is only a record. No scenario is lost.
- **Fix.** Name r180's scenario in `Deprecated for:`.

### 6. Minor, w231, drop: `tests/scenarios/test_supervision.py:14`, ruff I001 on a file w231 touched

- **What is wrong.** The import block is out of order. The order was wrong already at w231's base, and w231's line sits in its correct place.
- **Fix.** `ruff --fix` in the next work that touches the file.

### 7. Minor, none (other initiatives' step changes), drop: ruff on touched files

- `supervision_integrate_steps.py:87` RUF059.
- `supervision_proposal_steps.py:102` and `:137` RUF100.
- `test_supervise_answers.py:9` and `:10` RUF100.

These are lint findings only. The fix is `ruff --fix` where safe.

### 8. Minor, none (rounds of i50 and i59), observation: round scratch scripts are tracked Python files

- **What is wrong.** `.shop/work/i50/runs/supervision/2-apply/splice.py`, `.../3-formulate/splice.py` and `.shop/work/i59/runs/i59/1-integrate/cmp.py` are committed with the round's directory.
- **Why it matters.** `tools check` lints them, and they fail it. `tools size` and vulture count them too.
- **Fix.** Exclude `.shop/` from `tools check`, or keep round scratch out of the commit.

## Shape

CLAUDE.md rules and the rows the branch touched:

- **Size limit (300).** Met. `tools size` printed nothing.
- **"A new concern gets a new module and a row here".** Met for w231. `tests/scenarios/supervision_merge_steps.py` is a new `<capability>_*_steps.py` module for one concern (r187), covered by the `tests/scenarios/` row.
- **`scripts/supervise_glossary.py` row.** Not met. The row still says the module gives "the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162)". w230 deleted `names_one`, `terms_of` and `proposals_of`. The row does not name r173's `approval_question` (`supervise_glossary.py:45-54`, i50). This is Minor, none (i51 and i50) and an observation: rewrite the row. i51's review raised it too. It would be shown complete by `grep -n "r162" CLAUDE.md` printing nothing.
- **`scripts/supervise_answers.py` row.** Met. Its docstring cites r209 and r210.
- **`scripts/supervise*.py` row** (`supervise_rounds.py:155-157`, r173). Met. The gate's fallback question takes the glossary question when the proposal is a glossary-proposal, else r117's.
- **Unreached code.** None found. `names_one`, `terms_of` and `proposals_of` went with their test. `terms_in` (`supervise_glossary.py:57`) is still used by `withheld` and `glossary_only_done`, and vulture is clean.
- **r187 production code.** w231 changed none. `Changes.write_proposals` and `merge_lists` in `scripts/supervise_change.py` predate the base (w206, commit `e4e61321`, per w231's plan). r187 is now the line that asks for that code, and the r187 scenario passes. So it is not "code no line asks for".

## Coupling

- **pytest-bdd.** The steps rely on its `parsers.re` and `scenarios()` binding, which it publishes. The suite shows two `PytestRemovedIn10Warning`s from `pytest_bdd/compat.py:28` (300 each): pytest-bdd uses `_register_fixture` with a nodeid that pytest 10 removes. That is pytest-bdd relying on more than pytest publishes, not this repository. A pytest upgrade to 10 would break the scenario layer until pytest-bdd is upgraded. Pinning pytest below 10, or pytest-bdd to a release that passes `node`, keeps it stable.
- **Unregistered marks.** The tags `@deprecated`, `@r209` and `@r210` reach pytest as unregistered marks (`PytestUnknownMarkWarning`, 32 each). Under `--strict-markers` the suite would fail at collection. Registering the tag marks in conftest would make it stable.
- **ruff, vulture, import-linter, `claude` CLI.** They are reached through `tools` and the `SHOPSYSTEM_WORK_CLAUDE` stand-in. The branch adds no new dependency on any of them.

## Observations

- **`supervise_glossary.approval_question`, empty proposal** (`supervise_glossary.py:51-54`). A glossary-proposal whose `adds`, `changes` and `removes` are all empty writes "Are the terms of g1 approved as drafted? It ." No line names this edge. Reproduction: read from the code. `named` is `[]`, so `", ".join([])` gives "". Test, not run: a gate round giving no question for a glossary-proposal with empty lists, asserting a readable question.
- **The 3 XPASS.** The suite output does not name the three tests marked as expected failures that now pass (progress lines 52 and 55). Reproduction: the suite run's summary line says "3 xpassed", and `-rfEx` prints no XPASS line. Test, not run: the suite with `-rX`, to name them and see whether their xfail marks (likely w212's) are stale.
- **w231's open cases** (w231 plan §5). These are not covered by a scenario:
  - an id given twice within one list or across lists;
  - p2's status and its Q&A after a merge;
  - two proposals for one capability.

  Test, not run: a scenario whose change list removes an id that p2 holds in `changes`, asserting where it lands.
- **The r187 run's stderr.** It says the integrate round of p2 gave no change list (w231 report). The scenario does not assert on it. Reproduction: the w231 report, "Open questions".
- **The p2 Given** (`supervision_merge_steps.py:25-27`). It takes one `\S+` id for adds and for changes, and a fixed "nothing" for removes (w231's review, finding 2). This is hardening for later scenarios.
- **Duplicate line, from i55's apply** (`deda9fa6`, not i54). supervision r186 (`spec/capabilities/supervision.md:81`) is word for word r149 (l.80). r184 overlaps r32. Reproduction: the diff's added r186 and the context line r149. The fix is to retire r186, through integrating-a-proposal.
- **i54 is not finished.** `i54-work-queue` is awaiting-answer, and its approval question is unanswered. Reproduction: `.shop/work/i54/work-queue.md:19` has 2 questions and 1 answer.
