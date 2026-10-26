# Review of w199 (10-review)

**Verdict: DONE.** No Critical finding, and nothing is triaged fix now. The two Important findings of the 7-review are fixed:
- a researcher's questions now reach the planner whatever its status word (r129, r133);
- an apply round's questions are asked, and an apply round with neither questions nor a change list gets r131's question and stays awaiting-answer.

The three suite failures are green through setup-only allowances. Three Minor observations remain. Two of them are 7-review findings that report 8 calls fixed but that were only partly fixed.

## Commits reviewed

The branch work/w199 is gone, so the commits are taken from HEAD. They run from the last `8442012b work: w199 ready -> claimed` to `44b5725e work: w199 claimed -> done`, leaving out work run's `work:` commits:

| on HEAD | in the implementer's result | subject |
|---|---|---|
| 9052628d | 78b3e837 (8-implement) | supervision: a researcher's questions reach the planner whatever its status; an apply round's questions are asked and a missing change list is a question (r129, r131) |
| 1eea53ac | bd7fc9b1 (9-implement) | Apply-round stand-ins give a change list (r130, r131) |

The hashes differ because work run rebased the commits. `git diff 78b3e837~1 bd7fc9b1 -- scripts tests` and `git diff 8442012b 44b5725e -- scripts tests` are identical. The result in 8-implement gives a shorter subject than the commit has. Neither is a finding. The earlier commits of w199 (be4e1c7c to a853a2ea) were reviewed in 7-review.

## Removed and weakened tests

**None.**

**Searched for:** the following, in `git diff 8442012b 44b5725e -- tests features`:
- deleted test or step functions;
- removed Examples rows;
- removed or loosened `assert`s;
- added skip or xfail.

**What the commits change:**
- `features/` is untouched.
- In tests, the only changes are:
  - one moved import line (test_supervision.py);
  - a helper `apply_did_its_work`;
  - three Given steps (`every_round_ends`, `sessions_reply`, `formulate_gives_questions`, `apply_ends_formulate_question`, four in all), each of which gains a `plan["round:apply"]` entry.
- No assert, expected value or parametrize case changed.

## Allowances

| report | test | kind | holds? |
|---|---|---|---|
| 8 | supervision_session_faults_steps.py `formulate_gives_questions` | setup | holds: one plan line added, no assert or expected value |
| 8 | supervision_formulate_steps.py `apply_ends_formulate_question` | setup | holds: same |
| 9 | supervision_rounds_steps.py `every_round_ends` | setup | holds: calls `apply_did_its_work`, no assert. The person's allowance (answer 5) named the stand-ins of r80, r71/r114 and the delegation scenario. `every_round_ends` is shared by about 20 scenarios, so the change reaches beyond them. None of those scenarios asserts p1's lists after an apply round, and r114 uses its own step ("every other round ends"). That reach is setup, as plan decision 3 already made the stand-in's default deliver each output. |
| 9 | supervision_delegation_steps.py `sessions_reply` | setup | holds: same |

## Cannot verify

- **The whole suite on the merged branch.** work run ran it, and it is not re-run here. The scenarios the allowances serve were re-run here and pass (below).
- **Report 8's and report 9's figures** (207 passed under `--work-item w199`; 63 passed for test_supervision.py).
- **No scenario pins the two fixes.** Nothing covers a non-DONE researcher whose questions reach the planner, or an apply round with no change list asking r131's question. Report 8 says so, as the person's answer allowed. The behaviour was verified only by reading `supervise_brief.py:126-136` and `supervise_rounds.py:131-158`.

## Findings

### 1. Minor, observation (w199): "gave DONE" is still in two messages the status word no longer reaches only on DONE (scripts/supervise_rounds.py:139, :173)

**What is wrong.**
- Report 8 says finding 3 of the 7-review is fixed ("messages no longer say 'gave DONE'"). Only line 121 changed.
- `refuse_integrate` (line 173) still prints "the integrate round of i1 (...) gave DONE, and i1 keeps its status ...: it gave no change list", whatever status the round gave.
- Line 139 says the same for an apply round whose change list names an unknown capability.

**Why it matters.** The text is wrong for a round that gave BLOCKED or PARTIAL. No scenario pins these words: a grep of the features finds only the step text "gives DONE with no change list".

**Reproduction (by reading).** An integrate round result `{"status": "BLOCKED"}` with no `changes` goes through lines 120-121 to line 173.

**Fix.** Drop "gave DONE, and" from lines 139 and 173, and from the docstring at line 170.

### 2. Minor, observation (w199): `tests/scenarios/test_supervision.py:14` still fails ruff I001

**What is wrong.**
- Report 8 says finding 4 of the 7-review is fixed. 9052628d moved `supervision_then_faults_steps`, but `tools check --base 8442012b` still reports I001 at line 14.
- What remains is `supervision_review_steps` imported before `supervision_request_steps` (lines 37-38). That order was already there at 3451c15b, before w199.

**Why it matters.** The lint is not clean on a file these commits touched.

**Fix.** Swap the two lines (`ruff --fix`).

### 3. Minor, drop (w199): an unreadable apply change list is asked about as a missing one (scripts/supervise_rounds.py:132-146)

**What is wrong.** When `entries(data)` raises `BadChanges`, `applied` becomes `[]`. With no questions, the question written is "gave no change list", although one was given and could not be read.

**Why it matters.** r131 is kept, since the node goes to awaiting-answer with a question. Only the wording misleads.

**Fix.** Name the unreadable list in the question.

## Not in this range

vulture reports `tests/scenarios/supervision_session_faults_steps.py:48: unused variable 'node'`. That line comes from 36c7061f, an earlier w199 commit the 7-review covered, not from this range. It is named here only.

## Risks checked outside the diff

- **Risk:** after an apply round asks a question, the proposal is routed back to the wrong round once it is answered.
  - **Checked:** `route()` and `AFTER` (supervise_rounds.py:19, 52-61). The apply round commits `awaiting-answer -> awaiting-answer`, so the last move into awaiting-answer is not from approved, and `AFTER["awaiting-answer"]` gives apply again.
  - **Result:** correct.
- **Risk:** the shared `every_round_ends` change alters the r114 scenario.
  - **Checked:** r114 uses "every other round ends and every worker gives DONE" (features 1061-1067).
  - **Result:** not affected.

## Tools

- `tools check --base 8442012b`:
  - ruff: `tests/scenarios/test_supervision.py:14:1: I001` (finding 2);
  - vulture: `supervision_session_faults_steps.py:48` unused `node` (not in this range);
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: nothing printed.

## Commands run

- `git log --format='%h %s' -1 --grep="^work: w199 ready -> claimed$"` (work/w199 is gone; taken on HEAD)
- `git log --oneline -40`
- `git show --stat 9052628d 1eea53ac 78b3e837 bd7fc9b1`
- `git diff 8442012b 44b5725e --stat`
- `git diff 8442012b 44b5725e -- scripts tests`
- `git diff 78b3e837~1 bd7fc9b1 -- scripts tests`
- grep for `gave DONE|without a change list|no change list` in features, scripts and step modules
- `grep -n 'every round ends|...' features/supervision.feature`
- `sed -n 995,1085p features/supervision.feature`
- `git show 3451c15b:tests/scenarios/test_supervision.py | grep ...`
- `git show 8442012b:tests/scenarios/supervision_session_faults_steps.py`
- `python3 <Scripts>/tools check --base 8442012b`
- `python3 <Scripts>/tools size --limit 300`
- `python3 -m pytest -q -n auto -p work_items --work-item w199 --whole-suite tests/scenarios/test_supervision.py -k "apply_round_work_run_started or under_a_delegation_each_question or questions_before_a_section or transition_to_awaitinganswer or one_is_awaitinganswer"`: 10 passed
