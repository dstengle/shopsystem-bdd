# Review of w200: DONE_WITH_CONCERNS

Verdict: the formulate output check (r131, r132) and the r133 wording are done as planned, and the allowances hold. But the check counts `term/<term>` ids from a proposal's `adds`/`changes` as requirements with no scenario. A formulate round on a proposal that adds or changes a term is then always asked and never formulated. That is a wrong answer, triaged fix now (finding 1).

## Commits reviewed

Branch `work/w200` is gone. These are the commits on HEAD between `e93d69c4 work: w200 ready -> claimed` and `df5b3513 work: w200 claimed -> done`:

- `1e0eabf6` supervise_rounds: refusals no longer say the round gave DONE (r133). The 3-implement result lists it as `cab55fa6`, with the same subject.
- `5e486d94` supervision r131, r132: formulate round output check; retire the work-item-only r131 outline. 5-implement lists it as `c42d0188`, and 6-implement names it `208bb0e9`. All three have the same subject.
- `5b198dc9` supervision r83, delegation: formulate stand-in commits a scenario. 6-implement lists it as `6b86baff`. `git diff --stat 6b86baff 5b198dc9 -- scripts tests features` is empty, so the code is identical.

The hashes differ only because the commits were rebased or merged onto main. The subjects match one to one, and there are no extra or missing commits. Not a finding.

## Removed and weakened tests

I searched the diff for deleted `def test_`/step functions, dropped Examples rows, removed or changed `assert`s, added skip/xfail marks, and step bodies that changed. None is weakened. Changed step definitions:

- `features/supervision.feature`: the deprecated r131 outline (work-item only, 4 rows) is removed. It is listed under the work-item's Retires, so the removal is allowed. Its rows (researcher, planner, implementer, reviewer) are still covered by the live r131 outline, which also gains a formulate row.
- `supervision_formulate_steps.py::formulate_no_question` (the r83 Given): its stand-in now also commits a scenario. Setup only. The plan lists it under "Tests the decisions break".
- `supervision_session_faults_steps.py::stage_gives`: a formulate row that gives "a scenario for ..." now commits one, and an apply row's following formulate round commits one. Setup only. The plan lists it for the formulate row. The apply-row part is the same setup and changes no assert.
- `supervision_rounds_steps.py::answered_proposal`: the regex now reads the clause ", and the apply round for p1 ends with a change list that adds X on thing" and sets the apply stand-in. Setup only. The plan does not list it, but the 5-implement report lists it as a `setup` allowance.
- `supervision_delegation_steps.py::sessions_reply`: also calls `formulate_did_its_work`. Setup only, under the person's allowance (answer 3).
- `formulated_after_formulate` (the r83 Then): unchanged.

## Allowances

| Report | Row | Holds? |
|---|---|---|
| 5-implement | `stage_gives` (setup) | Holds: no assert, expected value or parametrize case changed |
| 5-implement | `answered_proposal` (setup) | Holds: only the regex and the plan stand-in changed |
| 6-implement | `formulate_no_question` (setup) | Holds: it replaces the plan entry with one that also commits; the person's answer 3 grants it |
| 6-implement | `sessions_reply` (setup) | Holds: one added setup call; the person's answer 3 grants it |

## Cannot verify

- Both reports say the whole suite passed. I did not run it; `work run` ran it before the merge.
- The plan's open cases are answered in the 5-implement report, but no scenario pins them:
  - the path is `features/<capability>.feature` only;
  - a deprecated scenario does not count;
  - the feature file is read after the merge;
  - for a removed id in `changes`, the report gives no reading.

## Findings

### 1. Important, fix now: `term/<term>` ids in a proposal's lists are asked as missing scenarios (w200)

**Where.** `scripts/supervise_outputs.py:44-55` (`unformulated`), called from `scripts/supervise_rounds.py:150-152`.

**What is wrong.** The check takes every id in the proposal's `adds` + `changes`. For `term/fault`, `partition("#")` gives capability `term/fault` and number `""`. That is never a scenario tag, so the id is always "lacking". The change-list format the briefs give allows `term/<term>` ids. The proposal of this very initiative has them: `.shop/work/i38/supervision.md:9` `changes: [..., term/fault, term/outcome, term/stage]`. So does every earlier proposal that adds a term (i18, i21, i22).

Probe: `.shop/scratch/w200-7-review/test_probe.py` calls `unformulated(root, ["thing#r1", "thing#r1-r3", "term/fault", "thing#r2"])` against a feature tagged `@r1`, `@r2 @r3`. It returned `LACKING ['thing#r1-r3', 'term/fault']`.

**Why it matters.** Such a proposal's formulate round always gets "the formulate round's scenario for term/fault ... is missing" and goes to `awaiting-answer`, never `formulated`. That contradicts r132 (a scenario for each *requirement*; a term is not one) and r83/r130. Answering the question cannot satisfy it, so it is asked again on every round.

**Fix.** In `unformulated`, take only ids of the form `<capability>#r<n>` and skip `term/...`. Add a scenario row (through a formulator) or a script test for a proposal whose `changes` names a term.

### 2. Minor, observation: ranges such as `thing#r1-r3` are read as one tag (w200)

**Where.** `scripts/supervise_outputs.py:51`.

**What happens.** The same probe reports `thing#r1-r3` as lacking even though `@r1`, `@r2` and `@r3` all exist. `rewrite_lists` writes what the apply round gives, and today's brief format is `<capability>#r<n>`, so no current client writes ranges. Older hand-written proposals do have them (e.g. `.shop/work/i18-deferred-findings/deferred-supervision.md:8` `supervision#r47-r54`).

**Fix.** Expand `r<a>-r<b>` before the lookup, or refuse it as unreadable.

### 3. Minor, drop: import order (w200)

**Where.** `scripts/supervise_rounds.py:13`.

**What is wrong.** `import supervise_outputs` is placed after `workqueue_request`, and ruff I001 flags the block as un-sorted. `ruff --fix` sorts it.

### Already present, not w200's

- vulture: `tests/scenarios/supervision_session_faults_steps.py:55` unused `node`. It was at line 48 at the base, so w200 did not add it.

## Commands run

- `git log --format='%H %s' --grep="^work: w200 " HEAD`; `git log --stat e93d69c4..df5b3513`; `git diff e93d69c4 5b198dc9`
- `git show -s cab55fa6 c42d0188 208bb0e9 6b86baff`; `git diff --stat 6b86baff 5b198dc9 -- scripts tests features` (empty)
- `sed -n 80,175p scripts/supervise_rounds.py`: checked the risk that the check reads a checkout other than the merged initiative branch. It does not: the round branch is merged into `self.root` before the read.
- greps for `formulated_as`, `term/` in proposals' `adds:`/`changes:`, step texts of the retired outline
- `python3 -m pytest -q -p no:cacheprovider .shop/scratch/w200-7-review/test_probe.py`: failed, `LACKING ['thing#r1-r3', 'term/fault']`
- `python3 <Scripts>/tools check --base e93d69c4`:
  - ruff: 1 (I001 `scripts/supervise_rounds.py:7`, finding 3)
  - vulture: 1, already present
  - import-linter: no contracts
- `python3 <Scripts>/tools size --limit 300`: nothing printed
