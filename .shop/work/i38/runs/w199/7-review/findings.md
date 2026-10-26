# Review of w199

**Verdict: DONE_WITH_CONCERNS.** Two Important findings are triaged fix now. Both come from removing the status gate (r133) without carrying out the rest of r129 and r131:

1. A researcher's questions given with a status other than DONE are lost.
2. An apply round's questions are lost, and an apply round with no change list moves its proposal on.

No Critical finding.

## Commits reviewed

The branch work/w199 is gone, so the commits are taken from HEAD. They run from `3451c15b work: w199 ready -> claimed` to `239fa2a5 work: w199 claimed -> done`, leaving out work run's own `work:` commits:

| on HEAD | in the implementer's results | subject |
|---|---|---|
| be4e1c7c | 947bdc50 (4-implement) | a work-item worker's stage output and questions decide its transition (r4, r31, r45, r61, r130-r133) |
| 36c7061f | 8c99590f (5-implement) | the steps of r87, r88, r89, r90, r128, r132 and r134 |
| e17b2b0f | 2ea88344 (5-implement) | a round's or an answering session's fault is recorded on its node and printed ... |
| a853a2ea | ae5da7ff (6-implement) | a researcher's questions go to the planner's brief, a planner's question asks ... |

The hashes differ because work run rebased the commits; the subjects are the same. `git diff ae5da7ff a853a2ea` touches only `.shop/work/` files and is empty for `scripts tests CLAUDE.md`, so the code is the same. Not a finding.

## Removed and weakened tests

**Searched for:** deleted `@given`/`@then`/test functions, removed Examples rows, deleted asserts, and added skip or xfail, in `git diff 3451c15b a853a2ea -- tests features`.

**Removed scenarios:** 16, all deprecated, each listed in the work-item's `## Retires`:
- r4: 4
- r5: the researcher outline
- one each of r32, r36, r37, r61, r31, r45, r89, r90, r87, r88 and r115

The plan's part 4 lists the r5 outline and the Retires scenarios. Nothing else under `features/` changed: the diff has no added lines.

**Removed step definitions.** Each one bound only retired scenarios. A grep of `features/` finds no remaining use of their texts:
- `supervision_given.py`:
  - `researcher_asks` ("the researcher gives <status>[, asking ...]"), used by the deprecated r5, r32, r36 and r37 versions
  - `implementer_leaves_uncommitted`, used by the deprecated r4 scenario
- `supervision_faults_steps.py`: `researcher_cut_short` and `ENDINGS`, used by the deprecated r45 outline
- `supervision_delegation_steps.py`: `session_in_error`, used by the deprecated r90 scenario
- `supervision_rounds_steps.py`:
  - `apply_blocked`
  - `formulate_without_result`
  - `apply_was_started` (the text without ", given the answers"; the line at features 1047 uses a different step)
  - `no_transition_after_apply`
  - `names_formulate_without_result`

  These were used by the deprecated r87 and r88 scenarios.
- `supervision_formulate_steps.py`: the "gives BLOCKED" branch of `gate_ends_badly`, the BLOCKED row of the deprecated r115 outline

**Weakened:** none. `supervision_then_workers.py` `none_after` gains a "planner" key; it asserts the same thing.

`tests/scripts/stub_claude.py`: by default it now delivers each stage's output (`DELIVERS`). This is plan decision 3, and no assert changed.

## Allowances

One row, in 4-implement's report: `supervision_given.py researcher_asks`, setup. In be4e1c7c it gains a `fields: {fileset: None}` when no question is given, and adds or changes no assert, expected value or parametrize case. **It holds.** a853a2ea later removes the step together with the scenarios it bound, which were retired.

Reports 5 and 6 list no row.

## Cannot verify

- The whole suite on the merged branch. work run ran it, and it is not re-run here.
- Report 5's and report 6's figures (201 passed under `--work-item w199`; 253 passed for test_supervision.py).
- That r90's stage directory and log lines are committed when an answering session faults. `note()` commits through `self.commit(name, status, status)`; the scenario is said to be green, and I did not run it.

## Findings

### 1. Important, fix now: a researcher's questions given with a status other than DONE never reach the planner (scripts/supervise_brief.py:132)

**What is wrong.**
- `outcome()` (scripts/supervise_worker.py:251-252) now returns None for any researcher result that gives questions, whatever its status word. `stage()` (supervise.py:171-173) then moves w1 drafted -> researched.
- But `research_questions` still begins with `if data.get("status") != "DONE" or not data.get("questions"): return []`.
- So a researcher that gives QUESTION, BLOCKED or PARTIAL with questions moves w1 to researched, and its questions appear nowhere: not in the planner's brief, and not under `## Questions`.

**Why it matters.**
- This loses data and contradicts r129 ("a researcher's [questions go] into the planner's brief") and r133 (no transition from the outcome).
- The person's third answer asked for exactly this: "a researcher's questions, whatever its status word, go into the planner's brief".
- Plan part 2 names this edit to `supervise_brief.py` ("passes on the researcher's questions whatever status the researcher gave"). It was never made, and `supervise_brief.py` is in the work-item's file set.
- The r129 researcher row passes only because the stand-in's researcher gives DONE.

**Fix.**
- Drop the status test at line 132, and the "with its DONE" wording at lines 127 and 135.
- Add a scenario row (or an r133 row) of a researcher giving QUESTION or BLOCKED with questions, whose Then is "the planner's brief has the researcher's questions".

### 2. Important, fix now: an apply round's questions are dropped, and an apply round with no change list moves its proposal to approved (scripts/supervise_rounds.py:127, 131-154)

**What is wrong.**
- e17b2b0f removes the refusal of a round whose status is not DONE (old lines 113-117).
- An apply round still has `asked = None` (line 127 sets it only for a gate). Line 154 then calls `self.move(name, "awaiting-answer", "approved", None)`.
- So an apply round that gives BLOCKED or QUESTION with questions and no change list:
  - moves p1 awaiting-answer -> approved;
  - drops its questions;
  - leaves p1's lists as they were (r114).
- Before these commits, the run refused that round and p1 kept awaiting-answer.

**Why it matters.**
- It is a wrong transition, and the questions are lost.
- r129 says every stage's questions other than a researcher's go under the node's `## Questions` with the node awaiting-answer. r131 says a round with neither questions nor its output (an apply round's change list, r132) writes a question naming the missing output.
- Plan part 2 and decision 2 name both changes for `run_round` ("writes a gate, apply or formulate round's questions under the proposal ...; checks the apply and formulate outputs"). Report 5 leaves them "unchosen" because no scenario asserts them. But the plan chose them, and the regression comes from these commits.

**Fix.**
- In `run_round`, take an apply round's questions as the formulate round's are taken: under p1's `## Questions`, with p1 awaiting-answer.
- When an apply round gives neither questions nor a change list that `entries()` reads, write r131's question naming "the apply round's change list" and keep p1 awaiting-answer.
- Add the r129 or r131 apply row that pins it.

### 3. Minor, observation: messages still say "gave DONE" when the status may be anything (scripts/supervise_rounds.py:121, 139)

**What is wrong.** "it gave DONE without a change list" (integrate) and "the apply round of %s ... gave DONE" are now reached with any status word, because the DONE gate is gone (r133).

**Reproduction (by reading).** An integrate round result `{"status": "BLOCKED"}` with no change list reaches line 121 and prints "gave DONE".

**Fix.** Say "gave no change list" or "its change list names ...", without the status.

### 4. Minor, observation: the import block of tests/scenarios/test_supervision.py is no longer sorted (line 14, ruff I001)

**What is wrong.** 36c7061f inserts `from .supervision_then_faults_steps import *` before `from .supervision_tests_steps import *`. In sorted order "tests" comes before "then_faults". At the base the block was sorted.

**Reproduction.** `tools check --base 3451c15b` reports `tests/scenarios/test_supervision.py:14:1: I001`.

**Fix.** Move the line after `supervision_tests_steps`, or run `ruff --fix`.

The two FURB167 notices in tests/scripts/stub_claude.py (lines 195-196, `re.M`) are in lines these commits did not touch; they are at lines 189-190 of the base. They are already there and are not a finding.

### 5. Minor, observation: an intake round that gives neither a line outcome nor a question now just ends (scripts/supervise_intake.py:88-104)

**What is wrong.** With the DONE gate gone, an intake result such as `{"status": "BLOCKED"}`, with no question and no line outcome, is merged and logged "ended". r131 does not say where the question naming a missing output would go for a request, which has no `## Questions` of its own. Plan part 5 lists this as an open case.

**Reproduction (by reading).** Lines 88-99 run for any status. With `questions` empty, only the merge happens.

**Fix.** Ask the person where r131's question for an intake round goes, or what the request's status should be in that case.

## Risks checked outside the diff

- **Risk:** the planner never receives a researcher's non-DONE questions. I read `supervise_brief.py:126-136` and `supervise.py:157-174`; this confirmed finding 1.
- **Risk:** an apply round with a non-DONE status moves the proposal on. I read `supervise_rounds.py:86-160` and `AFTER` at line 19; this confirmed finding 2.

## Commands run

- `git log --format='%H %s' --grep="^work: w199 " HEAD`
- `git log --oneline -40 HEAD`
- `git log --stat 3451c15b..239fa2a5`
- `git show --stat 947bdc50 8c99590f 2ea88344 ae5da7ff`
- `git diff 947bdc50 be4e1c7c --stat`
- `git diff ae5da7ff a853a2ea --stat` and `-- scripts tests CLAUDE.md` (empty)
- `git diff 3451c15b a853a2ea -- scripts CLAUDE.md`
- `git diff 3451c15b a853a2ea -- tests/...`
- `git diff 3451c15b a853a2ea -- features/ | grep ...`
- `git show be4e1c7c -- tests/scenarios/supervision_given.py`
- `git show 3451c15b:tests/scenarios/test_supervision.py | grep ...`
- `grep -rnE '<removed step texts>' features/` (only unrelated matches at features 86 and 1047)
- `grep` of `spec/capabilities/supervision.md` for the accepted lines
- `python3 <Scripts>/tools check --base 3451c15b`:
  - ruff: 3 errors (I001 test_supervision.py:14, introduced; FURB167 stub_claude.py:195-196, already there)
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: nothing printed (no file over the limit)
