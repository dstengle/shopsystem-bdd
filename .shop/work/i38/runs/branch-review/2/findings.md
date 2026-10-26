# Branch review 2 of i38 (re-review after the fix work-item w200)

**Verdict: DONE_WITH_CONCERNS.** There is no Critical finding, and every check was run and verified here. One Important finding is triaged fix now. It is in w200's own fix: the new formulate-output check (`supervise_outputs.unformulated`) asks for a scenario for every `<capability>#r<n>` the proposal adds or changes, and that includes requirements of **guarantees** capabilities. By design-decision 0065, those capabilities have no feature file and no scenarios. So a capability-proposal on planning, review, formulation or any other guarantees capability can never become `formulated`: each formulate round that correctly writes no scenario is asked "the formulate round's scenario for planning#rN is missing", and asked again after every answer. Review 1's finding 1 (no formulate check at all) is fixed, and its finding 3 ("gave DONE") is fixed.

## Range and work-items

- **Range:** `50a40103..922f5f6c` (97 commits). Base is the commit that added i38's `initiative.md`. HEAD is `922f5f6c work: w200 done -> green`. Review 1 covered `50a40103..34e514e0`, and its findings are at `.shop/work/i38/runs/branch-review/1/findings.md`. This review reads the whole range again and looks most closely at `34e514e0..HEAD`.
- **w199** (supervision, green): its commits are those review 1 listed (`be4e1c7c`, `36c7061f`, `e17b2b0f`, `a853a2ea`, `9052628d`, `1eea53ac`). Nothing of w199 changed after `34e514e0`.
- **w200** (supervision, green, the fix work-item from review 1's findings). It had five claims. The first three (`b118483a..c6e54f42`, `84aa57c5..3bc47c3f`, `89a10a10..c5642ae9`) each ended in a question and hold no content commit. The other two hold all of its content:
  - `e93d69c4..df5b3513`: `1e0eabf6` (refusal wording, r133), `5e486d94` (formulate check, new r131 row bound, old r131 outline retired), `5b198dc9` (formulate stand-ins commit a scenario);
  - `56c39faa..80bd7cf6`: `684f1409` (term ids skipped).
- **Commits in the range that belong to no work-item:**
  - `a886e59c`: review 1's own commit;
  - `177ec65c`: `work add`;
  - `e9cfc7ff`: a feature-formulator hand-back that adds the r131 outline with a formulate row and deprecates the work-item-only outline;
  - `bf58a9b3`: a hand edit of w200's Retires;
  - review 1's four (`46b35719`, `33ba1e88`, `5d6c49ad`, `8c1d9d51`).
  
  See Finding 6.

## Suite

`Suite: 946 passed, 0 failed at 922f5f6 in 27.1 s` (1 skipped, 56 subtests passed; pytest reports 26.77 s, and the shell measured 27.07 s from start to end).

- **Parallel:** yes. `pytest.ini` gives `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions start `scripts/work run` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite is under 60 s, so this is not a finding.

## Checks

| check | result |
|---|---|
| w200's check: `python3 -m pytest -q -rfEx -p work_items --work-item w200 --whole-suite` | 946 passed, 1 skipped, 0 failed (27.41 s) |
| w200's scenarios: `python3 -m pytest -q -p work_items --work-item w200` | 208 passed, 1 skipped, 0 failed |
| w199's scenarios: `python3 -m pytest -q -p work_items --work-item w199` | 208 passed, 1 skipped, 0 failed. w199's `--whole-suite` check is the same suite as above. |
| `tools check --base 50a40103`: **ruff** | 12 errors, exit 1. **One is new from w200:** `scripts/supervise_rounds.py:7` I001, from `import supervise_outputs` being placed after `workqueue_request` in `5e486d94` (Finding 3). Review 9 of w200 called ruff clean because it ran with `--base 56c39faa`, which leaves out that commit. The other 11 are review 1's: 8 in the committed round scripts under `.shop/work/i38/runs/supervision/` (Finding 7), `tests/scenarios/test_supervision.py:14` I001 (already present at Base), and `tests/scripts/stub_claude.py:195-196` FURB167 (on lines this branch did not touch). |
| `tools check`: **vulture** | clean |
| `tools check`: **import-linter** | "the project states no import contracts". There are no contracts to read and nothing to read in their place. |
| `tools size --limit 300` (the limit CLAUDE.md gives) | prints nothing |
| `features deprecated` | 5 scenarios, each "for: removal": r3 ("a worker's outcome DONE ..."), the r5 implementer outline, r16, r112 and r113. These are review 1's Finding 7, unchanged (Finding 8 below). None has a replacement whose work-item is green. |
| `features bindings` | "every binding names a scenario" |
| Dry run against real run, randomized | Not applicable. The only `--dry-run` in `scripts/` is `git push --dry-run` (`supervise_faults.py:71`, `supervise_review.py:41`), a check git provides before a push, not a mode of this system. |
| `model check` (also run) | 12 violations, 13 warnings, as at review 1. Review 1's v3 on q8 / `supervision#r113` is still there (Finding 8). |

## Removed and weakened tests

**Searched for:**
- `git diff 34e514e0 HEAD -- tests features`: deleted lines with `assert`, `def test`, `skip`, `xfail`, `Scenario` or an Examples row;
- each of w200's commits read in full (`git show 1e0eabf6 5e486d94 5b198dc9 684f1409 e9cfc7ff`).

**Removed scenarios since review 1:** one. `5e486d94` removes the r131 outline "a <who> whose result gives neither a question nor <missing> puts a question naming it under the work-item's ## Questions and makes the work-item awaiting-answer (deprecated)". It was deprecated in `e9cfc7ff`. It is listed under w200's `## Retires`, and its replacement's work-item, w200, is green. All four of its rows (researcher, planner, implementer, reviewer) are kept in the replacement outline with the same Givens, gives and Thens (`w1` as `<node>`). The Then wording is unchanged.

**Removed or weakened tests:** none since review 1. No assert was removed or loosened, no parametrize case was dropped, and no skip or xfail was added. Review 1's list for w199 stands: 16 retired scenarios, each deprecated and under w199's Retires, and their step definitions.

**Strengthened:** review 1's weakness is gone. The r132 formulate row's Given now commits the scenario its text names (`stage_gives`, `scenario_commit`).

## Allowances

| report | test | kind | holds? |
|---|---|---|---|
| w200 5-implement | `supervision_session_faults_steps.py` `stage_gives` | setup | **Holds.** `5e486d94` makes the formulate row commit a scenario and makes an apply row's following formulate round commit one. No assert, expected value or case changed. |
| w200 5-implement | `supervision_rounds_steps.py` `answered_proposal` | setup | **Holds.** The step regex takes an optional apply-round clause and sets the apply stand-in. No assert. |
| w200 6-implement | `supervision_formulate_steps.py` `formulate_no_question` (r83 Given) | setup | **Holds.** `5b198dc9` replaces `{"status": "DONE", "questions": []}` with `formulate_did_its_work`, the same result plus a committed scenario. The Then `formulated_after_formulate` is unchanged. Plan part 4 lists it. |
| w200 6-implement | `supervision_delegation_steps.py` `sessions_reply` | setup | **Holds.** One added setup call. |
| w200 8-implement | none | - | Agrees with `684f1409`, which touches no test. |
| w199's five rows | - | setup | Verified by review 1. Nothing of them changed after it. |

## Cannot verify

Nothing. Every check above was run here at HEAD `922f5f6`.

## Findings

### 1. Important, w200, fix now: the formulate check asks for scenarios of guarantees capabilities, so a proposal on one is never `formulated` (scripts/supervise_outputs.py:44-58, called from scripts/supervise_rounds.py:150-154)

**What is wrong.**
- `unformulated` looks for `features/<capability>.feature` and, if the file is missing, counts every id of that capability as lacking.
- Design-decision 0065, which supervision `rests_on`, makes ten capabilities guarantees (spec-integration, spec-migration, spec-consistency, review, delivery, formulation, red-green, code-research, planning, trials). These are checked by `measure` and have no scenarios. None of them has a feature file under `features/`.
- The rest of the system leaves them out already:
  - `model.lp:187-188`: v15f, "a formulated proposal has a scenario for each id", excepts `group(C, "guarantees")`;
  - `work_items.py:133-149` and supervision r56, r64, r65 excuse a guarantees work-item from having scenarios.
- `unformulated` does not leave them out.

**Reproduction.** I wrote a probe at `.shop/scratch/i38-branch-review/test_probe.py`, since deleted, that calls `supervise_outputs.unformulated(<repo root>, ["planning#r1", "supervision#r132", "supervision#r3", "supervision#r999", "term/x"])` at HEAD.
- Run with `python3 -m pytest -q -n 0 -s -p no:cacheprovider <probe>`, it printed `unformulated: ['planning#r1', 'supervision#r3', 'supervision#r999']`.
- `supervision#r3` is lacking because its only scenario is deprecated, which is correct.
- `planning#r1` is lacking only because planning is guarantees.
- Proposals on guarantees capabilities do occur, for example `.shop/work/i9-ubiquitous-language/ubiquitous-language-formulation.md`, `...-spec-consistency.md`, `...-spec-integration.md` and `.shop/work/i8-model-in-consumers/*-spec-migration.md`.

**Why it matters.** This is a wrong transition, a fault of the system itself on valid input.
- A formulate round on such a proposal that correctly writes no scenario gives no question. `work run` then writes "the formulate round's scenario for planning#r1 is missing ..." under the proposal's `## Questions` and moves it to `awaiting-answer` instead of `formulated`. That contradicts r83, read with 0065.
- No answer can satisfy the question. Each answer starts a new formulate round (`supervise_rounds.py:60-61`), and that round is asked again.
- Under a delegation (r77), the answering session answers it, so the loop has no bound inside one `work run`.
- It is the same kind of defect as w200 review 7's term-id finding, for a different class of id.

**Fix.**
- In `unformulated`, skip ids whose capability has `group: guarantees` in `spec/capabilities/<cap>.md`. Use the reading `work_items.guarantees` already makes.
- Add a scenario that pins it, through a formulator hand-back: an r83/r132 row for a proposal whose `adds` names a requirement of a guarantees capability, with the stand-in committing no scenario, which then ends `formulated`.
- If r132's words "for each requirement its proposal adds or changes" are to carry the exception, write it into r132 through integrating-a-proposal ("... that is not of a guarantees capability", as r56 and r64 say).

### 2. Minor, w200, observation: requirement ranges and Gherkin keyword synonyms are not read (scripts/supervise_outputs.py:28-41, :51)

- **Ranges.** `thing#r1-r3` is looked up as the single tag `r1-r3`, so it is always lacking. This is w200 review 7 finding 2, unchanged. No client writes ranges today: `rewrite_lists` writes the apply round's `<capability>#r<n>` ids. Hand-written proposals have them, for example `.shop/work/i18-deferred-findings/deferred-supervision.md:8` `supervision#r47-r54`.
- **Keyword synonyms.** `scenario_ids` knows only `Scenario:` and `Scenario Outline:`. The repository's own reader, `features_gherkin.py:7`, also takes `Scenario Template:` and `Example:`. A scenario written with either is not counted. Feature-level tags are dropped too. The formulator writes `Scenario:`/`Scenario Outline:` today.
- **Reproduction:** w200 review 7's probe gave `LACKING ['thing#r1-r3', ...]`. For the synonyms, see `grep -n "Scenario Template" scripts/features_gherkin.py scripts/supervise_outputs.py` (it is only in the first).
- **Fix:** read the tags through `features_gherkin`, and expand or refuse ranges.

### 3. Minor, w200, observation: ruff I001 on the import block w200 changed (scripts/supervise_rounds.py:7-16)

`5e486d94` put `import supervise_outputs` after `import workqueue_request`, so `tools check` reports a new ruff error on a file the branch touched. w200 review 7 found it (finding 3, "drop"), and review 9 missed it because it ran with `--base 56c39faa`.

- **Reproduction:** `python3 <Scripts>/tools check --base 50a40103` gives `scripts/supervise_rounds.py:7:1: I001`.
- **Fix:** `ruff check --fix scripts/supervise_rounds.py`, or move the import above `workqueue`.

### 4. Minor, w200, observation: a changed requirement's old scenario satisfies the formulate check (scripts/supervise_outputs.py:44-58)

For an id in `changes`, a non-deprecated scenario that was there before the round counts. A formulate round that leaves a changed requirement's old scenario untouched is therefore taken as having formulated it.
- r132 says "a scenario for each requirement its proposal adds or changes" and does not say a new one, so this follows the line as written.
- Plan part 5's open case "a requirement in `changes` the list removes" got no reading in the reports.
- **Reproduction (by reading):** `unformulated` reads only the feature file at HEAD, not the round's diff.

### 5. Important, i38 (the proposal's apply round `4be48031`), observation, carried from review 1 finding 2: design-decision 0039 still guards on `DONE`

`grep -c DONE spec/decisions/0039-work-item-lifecycle-as-run.md` gives 6. r133 says "make no transition from the outcome". No decision supersedes 0039. Fix as in review 1.

### 6. Minor, none (i38's run), observation, carried from review 1 finding 5 and extended: commits outside any work-item or round

- `e9cfc7ff` is a feature-formulator hand-back made between w200's `claimed -> awaiting-answer` (`c6e54f42`) and its answer. It is a correct deprecate-and-add: the old four rows are kept, and the formulate row is added.
- `bf58a9b3` edits w200's Retires by hand, and its subject says "(by hand)".
- **Reproduction:** `git show --stat e9cfc7ff bf58a9b3`.
- **Fix:** as in review 1: `work` commands for accepts and Retires, and hand-backs through a formulate round.

### 7. Minor, none (the proposal's rounds), observation, carried from review 1 finding 6: committed round scripts fail ruff

8 of the 12 ruff errors are in `.shop/work/i38/runs/supervision/{2-apply/merge.py,3-formulate/deprecate.py,4-formulate/splice.py}`. Fix as in review 1.

### 8. Minor, w199 / the proposal, observation, carried from review 1 findings 7 and 8

- **Deprecated for removal, nothing to retire them.** `features deprecated` lists 5 "for: removal" scenarios, of r3, r5, r16, r112 and r113. Those requirements are retired, and nothing retires the scenarios.
- **q8's resolution.** `model check` gives v3 on q8 for the removed `supervision#r113`.

### 9. Minor, w199, observation, carried from review 1 finding 4: no intake output check and no implementer-commit check

There is still no output check for an intake round or for an implementer that commits nothing. `supervise_outputs.missing` has no intake or implementer branch. The plan left this to its owners (w200 plan part 5).

## Shape

CLAUDE.md is checked rule by rule and module-map row by row, for what the branch touched.

**Rules:**
- **Size limit, 300 lines:** met. `tools size --limit 300` prints nothing.
- **"A new concern gets a new module and a row here":** met. w200 added no new concern. The formulate output is a stage's output, which is `supervise_outputs.py`'s row ("`work run`'s reading of what a stage's result must give").

**Module-map rows:**
- `scripts/supervise_outputs.py`: met. `scenario_ids` and `unformulated` are at `supervise_outputs.py:28-58`, and the question is built by `supervise_outputs.question` (`:61`), as plan decision 3 asked.
- `scripts/supervise*.py` (rounds): met. The call is at `supervise_rounds.py:150-154`. The proposal's frontmatter is read in `run_round`, which is where the other round kinds read theirs.
- `tests/scenarios/`: met. The new helpers are `scenario_commit` (`supervision_session_faults_steps.py:30`) and `formulate_did_its_work` (`supervision_rounds_steps.py:114`), each in an existing module of its concern.

**Code no scenario reaches:** vulture is clean, and `features bindings` says every binding names a scenario. The retired r131 outline's Given "every other worker gives DONE" is no longer in any feature line. Its step definition still binds the live outline's "every other session gives DONE", and the bindings check passes.

**Refactor, as an observation:** `scenario_ids` is a third Gherkin tag reader, beside `features_gherkin.py` and `model_parse.scenarios`. It is complete when `supervise_outputs` reads tags through `features_gherkin` and `grep -n "startswith((\"Scenario:\"" scripts/supervise_outputs.py` finds nothing.

## Code no line asks for

None. w200's new observable behaviour is each asked for by a line:
- the formulate round's missing-scenario question and the move to `awaiting-answer`: r131 and r132;
- term ids not counted as requirements: r132 ("requirement");
- the refusal wording without "gave DONE": r133 and r96.

## Coupling

- **Claude Code CLI's JSON result:** unchanged since review 1. `how_ended` reads the documented `subtype`, `num_turns` and exit code. An unknown subtype reads as "ended in an error", which is safe.
- **Gherkin, as pytest-bdd reads it:** new. `scenario_ids` relies on a subset of Gherkin's keywords (`Scenario:` and `Scenario Outline:`). It would miss `Scenario Template:`, `Example:` and feature-level tags, all of which pytest-bdd and Gherkin publish (Finding 2). Reading the feature file through `features_gherkin` would make it stable.
- **pytest-bdd on pytest internals:** unchanged since review 1. 540 warnings per run, `PytestRemovedIn10Warning` among them. Pinning `pytest<10` and registering the `deprecated` mark would make it stable.
- **The agents' result fields:** unchanged since review 1. These are within the repository.

## Observations

1. Guarantees capabilities are asked for scenarios (Finding 1, fix now). `unformulated(root, ["planning#r1", ...])` gave `['planning#r1', 'supervision#r3', 'supervision#r999']`.
2. Ranges and keyword synonyms (Finding 2). w200 review 7's probe gave `thing#r1-r3` as lacking. `grep -n "Scenario Template" scripts/features_gherkin.py scripts/supervise_outputs.py` finds it only in `features_gherkin.py`.
3. Import order (Finding 3). `tools check --base 50a40103` gives `scripts/supervise_rounds.py:7:1: I001`.
4. A changed requirement's old scenario counts (Finding 4). See by reading `supervise_outputs.py:44-58`, which does not look at the round's diff.
5. 0039 still guards on DONE (Finding 5). `grep -c DONE spec/decisions/0039-work-item-lifecycle-as-run.md` gives 6.
6. Commits outside work-items (Finding 6). `git show --stat e9cfc7ff bf58a9b3 46b35719 33ba1e88 5d6c49ad 8c1d9d51`.
7. Committed round scripts fail ruff (Finding 7). `tools check --base 50a40103` gives 8 errors under `.shop/work/i38/runs/`.
8. Deprecated-for-removal scenarios and q8 (Finding 8). `features deprecated` lists 5, and `model check` gives v3 on q8 / `supervision#r113`.
9. No intake or implementer-commit output check (Finding 9). See by reading `supervise_outputs.py:12-25`.
