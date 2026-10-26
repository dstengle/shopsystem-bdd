# Branch review of i38

**Verdict: DONE_WITH_CONCERNS.** There is no Critical finding. One Important finding is triaged fix now: a formulate round's output is never checked. A formulate round that gives no question and commits no scenario still moves its proposal to `formulated`, against r131 and r132. The r132 scenario that should pin this passes without the scenario its Given names. Every check was run and verified.

## Range and work-items

- **Range:** `50a40103..34e514e0` (66 commits). Base is the commit that added i38's `initiative.md`. HEAD is `34e514e0 work: w199 done -> green`.
- **Work-items:** one, **w199** (supervision, `green`). It accepts r4, r31, r32, r36, r37, r45, r61, r86-r90, r115 and r128-r134. Its commits are those inside its claims, less `work run`'s own `work:` commits:
  - `be4e1c7c`, `36c7061f`, `e17b2b0f`, `a853a2ea` (claim `3451c15b` to `239fa2a5`);
  - `9052628d`, `1eea53ac` (claim `8442012b` to `44b5725e`).
- **Commits of the capability-proposal i38-supervision:** its rounds' commits `4be48031` (apply), `70195d02` and `04ab2ba1` (formulate), plus `work answer`/`work note` commits.
- **Commits that belong to no work-item and no round:** see Finding 5.
  - `46b35719`: a feature-formulator hand-back that rewrote the r32, r36 and r37 scenarios and deprecated the old ones.
  - `33ba1e88`, `5d6c49ad`, `8c1d9d51`: hand edits of w199's `accepts` and `## Retires`.

## Suite

`Suite: 945 passed, 0 failed at 34e514e in 26.9 s` (1 skipped, 56 subtests passed; pytest says 26.56 s and the shell timed 26.855 s).

- **Parallel:** yes. `pytest.ini` gives `addopts = -n auto`.
- **In-process:** no. The step definitions start `scripts/work run` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite is under 60 s, so this is not a finding.

## Checks

| check | result |
|---|---|
| w199's check: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w199 --whole-suite` | 945 passed, 1 skipped, 0 failed (30.0 s) |
| w199's scenarios: `python3 -m pytest -q -n auto -p work_items --work-item w199` | 207 passed, 1 skipped, 0 failed |
| `tools check --base 50a40103`: **ruff** | 11 errors, exit 1. None is on a line w199 changed. 8 are in Python scripts that the proposal's rounds left in their stage directories, which are committed (`.shop/work/i38/runs/supervision/2-apply/merge.py`, `3-formulate/deprecate.py`, `4-formulate/splice.py`: I001, SIM115); see Finding 6. The other 3 were already there at Base: `tests/scenarios/test_supervision.py:14` I001, where `supervision_review_steps` comes before `supervision_request_steps` as it does at Base (`git show 50a40103:tests/scenarios/test_supervision.py`, lines 37-38); and `tests/scripts/stub_claude.py:195-196` FURB167, on lines this branch did not touch. |
| `tools check`: **vulture** | clean |
| `tools check`: **import-linter** | "the project states no import contracts". No contracts to read, and nothing to read in their place. |
| `tools size --limit 300` (the limit CLAUDE.md gives) | prints nothing: no tracked Python file is over 300 lines |
| `features deprecated` | 5 scenarios, each "Deprecated for: removal": r3, the r5 implementer outline, r16, r112 and r113 (Finding 7) |
| `features bindings` | "every binding names a scenario" |
| Dry run against real run, randomized | Not applicable. No operation this branch touches has a dry-run mode next to a real one. The only `--dry-run` in `scripts/` is `git push --dry-run` (`supervise_faults.py:71`, `supervise_review.py:41`), a check before a push that git provides, not a mode of this system. |

Also run: `model check` gives 12 violations. One of them, v3 on q8 for `supervision#r113`, comes from this branch (Finding 8). The rest are about other initiatives and requests.

## Removed and weakened tests

**Searched for:**
- `git diff 50a40103 HEAD -- features tests`, for deleted `Scenario` lines, deleted step and test functions, dropped Examples rows, removed or loosened asserts, and added skip or xfail;
- the allowance commits read one at a time (`git show 9052628d 1eea53ac be4e1c7c -- tests`).

**Removed scenarios:** 16, all in w199's commits, each deprecated and each listed under w199's `## Retires`:
- 4 of r4;
- the r5 researcher outline;
- one each of r32, r36, r37, r61, r31, r45, r89, r90, r87, r88 and r115.

The plan (3-plan part 4) lists the r5 outline and the Retires scenarios. No scenario was removed that was not deprecated.

**Removed step definitions.** Each bound only retired scenarios:
- `researcher_asks` and `implementer_leaves_uncommitted` (`supervision_given.py`);
- `researcher_cut_short` and `ENDINGS` (`supervision_faults_steps.py`);
- `session_in_error` (`supervision_delegation_steps.py`);
- `apply_blocked`, `formulate_without_result`, `apply_was_started`, `no_transition_after_apply` and `names_formulate_without_result` (`supervision_rounds_steps.py`);
- the BLOCKED branch of `gate_ends_badly` (`supervision_formulate_steps.py`).

**Weakened:** no assert removed or loosened, and no skip or xfail added. One case is weakened in effect: the r132 formulate row's Given claims a scenario its step never sets up (part of Finding 1).

## Allowances

| report | test | kind | holds? |
|---|---|---|---|
| 4-implement | `supervision_given.py` `researcher_asks` | setup | **Holds.** `be4e1c7c` adds `fields: {fileset: None}` when no question is given, and changes no assert, expected value or case. The step was later removed with the scenarios it bound. |
| 8-implement | `supervision_session_faults_steps.py` `formulate_gives_questions` | setup | **Holds.** `9052628d` adds one `plan["round:apply"]` line and nothing else. |
| 8-implement | `supervision_formulate_steps.py` `apply_ends_formulate_question` | setup | **Holds.** Same change. |
| 9-implement | `supervision_rounds_steps.py` `every_round_ends` (via `apply_did_its_work`) | setup | **Holds.** `1eea53ac` adds the helper call and no assert. It reaches every scenario that uses this step, which matches plan decision 3. |
| 9-implement | `supervision_delegation_steps.py` `sessions_reply` | setup | **Holds.** Same change. |

## Cannot verify

Nothing. Every check above was run here at HEAD `34e514e`.

## Findings

### 1. Important, w199, fix now: a formulate round's output is never checked, so a formulate round that gives no question and no scenario moves its proposal to `formulated` (scripts/supervise_rounds.py:147-158)

**What is wrong.**
- r132 makes a formulate round's output "a scenario for each requirement its proposal adds or changes".
- r131 says a session whose result gives neither a question nor its output gets a question naming the missing output, and its node goes to `awaiting-answer`.
- The gate answer 3 recorded in the proposal kept r83 "as written, r130 and r131 deciding whether the next transition happens".
- `run_round` reads only a formulate round's `questions` (line 148). With none, it moves the proposal to `formulated` (line 158). No scenario is looked for.
- Plan decision 2 named this check: "a non-deprecated scenario tagged `@r<n>` for each id the proposal adds or changes". Plan part 2 put it in `run_round`: "checks the apply and formulate outputs". Report 5 left it "unchosen". The 7-review raised only the apply half, which 9052628d fixed.

**The scenario does not pin it.** The r132 row "a formulate round's result giving a scenario for thing#r4 is taken as its stage's output" passes, but its Given sets up no scenario. `stage_gives` (`tests/scenarios/supervision_session_faults_steps.py:80`) skips the formulate round on purpose ("a formulate round's scenario is its output, no question is asked"). The stand-in round gives a bare DONE and commits nothing, and `stub_claude.DELIVERS` has no entry for `initiative-round`. The row's text claims an output that the test never produces.

**Reproduction.**
- `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -k "taken_as_its_stages_output and formulate"` gives `1 passed`. Its Then: "p1's transition to formulated was made once the formulate round had ended". In that run no scenario for thing#r4 exists anywhere.
- `grep -n "scenario for each\|formulate.*missing" scripts/` finds nothing.

**Why it matters.** This is a wrong transition. Once a proposal is `formulated`, r72 drafts work-items accepting requirements that have no scenario. Their `--work-item` selection is then empty, so r4's checks pass on an implementer that did nothing, and the work-item can go to `green` with nothing implemented.

**Fix.**
- In `run_round`, for kind `formulate` with no question, look on the merged initiative branch for a non-deprecated scenario tagged `@r<n>` in `features/<capability>.feature` for each id in the proposal's `adds` and `changes`.
- If any is missing, write r131's question naming the requirements without a scenario, and leave the proposal `awaiting-answer`.
- Make the r132 formulate row's stand-in commit that scenario.
- Add an r131 formulate row through a formulate hand-back.

### 2. Important, i38 (capability-proposal i38-supervision, apply round 4be48031), observation: design-decision 0039, on which supervision rests, still guards every work-item transition on the outcome `DONE`, which r133 now forbids (spec/decisions/0039-work-item-lifecycle-as-run.md:19-29)

**What is wrong.**
- supervision `rests_on: work-item-lifecycle-as-run`. 0039's guard column says, for example: "drafted → researched: DONE, a non-empty file set ...", "drafted → awaiting-ruling: any result but DONE", "done → awaiting-ruling: any result but DONE".
- r133, which w199 implements, says "make no transition from the outcome".
- No decision supersedes or amends 0039.

**Why it matters.** A binding decision now says the opposite of the code and the capability. The next planner or reviewer who reads 0039 will "fix" the code back.

**Fix.** Record a design-decision, or an amendment of 0039 like its 0.21.0 one, under which a transition is decided by how the session ended and what its result gives (r128-r133), and supersede the guard column.

**Reproduction.** `grep -n DONE spec/decisions/0039-work-item-lifecycle-as-run.md` gives lines 19, 20, 21, 25, 29 and 41.

### 3. Minor, w199, observation: two error messages still say "gave DONE" whatever status the round gave (scripts/supervise_rounds.py:139, :173; docstring :170)

Both messages are reached for any status since the DONE gate went (r133):
- `refuse_integrate` prints "the integrate round of i1 (...) gave DONE, and i1 keeps its status ...: it gave no change list" even for a round that gave BLOCKED.
- The apply round's unknown-capability error says the same.

This was 10-review finding 1. Report 8 called it fixed, but only line 121 changed.

**Reproduction.** `grep -n "gave DONE" scripts/supervise_rounds.py` gives 139 and 173, and the docstring at 170 says "ended DONE". No branch on `data["status"]` comes before them.

**Fix.** Drop "gave DONE, and", and "DONE" from the docstring.

### 4. Minor, w199, observation: plan part 5's open cases are left unchosen against r131 and r132

- **Intake round.** A result that gives neither a line outcome nor a question (for example `{"status": "BLOCKED"}`) is merged and logged "ended" (`scripts/supervise_intake.py:88-107`). The request then stays `open`, and the next `work run` starts the round again. No line says where r131's question goes for a request, which has no `## Questions`. This was 7-review finding 5, and no ruling followed.
- **Implementer.** An implementer that commits nothing, gives no question and whose tests pass on the unchanged branch is merged and moved to `done` (`supervise_outputs.missing` gives None for the implementer; `supervise_merge.py:128-139` checks only the tests). Plan decision 2 named "at least one commit the initiative branch lacks". In practice the work-item's red scenarios catch this case.

**Reproduction (by reading).** `scripts/supervise_outputs.py:12-25` (`missing`) has no implementer branch and no intake branch, and `supervise_intake.py:88` takes any result.

### 5. Minor, none (i38's run), observation: four commits belong to no work-item and no round

- **`46b35719`** rewrote the r32, r36 and r37 scenarios to ask through the planner and deprecated the old ones. This was the feature-formulator hand-back the ledger records under q16's delegation. It was a correct deprecate-and-replace: the old three were deprecated, retired later by w199, and no Then was loosened. But it was made outside any formulate round, between w199's `claimed -> awaiting-answer` and its answer.
- **`33ba1e88`, `5d6c49ad` and `8c1d9d51`** edit w199's `accepts` and `## Retires` by hand. Their own subjects say "no command adds to a work-item's accepts/Retires".

**Why it matters.** No command or round records these changes, so they reach the branch outside `work`'s log.

**Fix.** Add `work` commands for a work-item's accepts and Retires, and route a hand-back's reformulation through a formulate round.

### 6. Minor, none (the proposal's rounds 2-apply, 3-formulate, 4-formulate), observation: the rounds' Python helper scripts are committed in their stage directories and fail `tools check`

`.shop/work/i38/runs/supervision/2-apply/merge.py`, `3-formulate/deprecate.py` and `4-formulate/splice.py` are now tracked Python files. ruff reports 8 errors in them, so `tools check` exits 1 on this branch for files that are no code of the project.

**Reproduction.** `python3 <Scripts>/tools check --base 50a40103` gives the `== ruff ==` lines listed under Checks.

**Fix.** Either exclude `.shop/` in the ruff configuration, or have rounds keep their probes in scratch so they are not copied into stage directories.

### 7. Minor, w199 / the proposal, observation: five scenarios deprecated for removal, of requirements i38 removed, are left with nothing to retire them (features/supervision.feature:63, 89, 332, 1387, 1396)

- r3, r5, r16, r112 and r113 are now `retired:` in `spec/capabilities/supervision.md`.
- Their scenarios remain, tagged `@r3`, `@r5`, `@r16`, `@r112` and `@r113` and "Deprecated for: removal". All 5 pass today (`-k deprecated`: 10 passed).
- r123 retires only deprecated scenarios whose replacement's work-item is green, and these have no replacement. w199 retired the r5 researcher outline only because it went red.
- They are none of the deprecated scenarios whose replacement's work-item is `green`.

**Fix.** Add a line, or a `work run` step, that retires "Deprecated for: removal" scenarios once their requirement is retired, or list them under a work-item's Retires.

### 8. Minor, the proposal (apply round 4be48031), observation: request q8's resolution now names a removed requirement

`model check` reports `v3 a delivered request's resolution names a requirement the spec does not have: q8, supervision#r113`. r113 was removed by this branch's apply round. At Base it was in the capability.

**Reproduction.** `python3 <Scripts>/model check` prints this v3 line.

**Fix.** Re-point q8's resolution to the line that replaced r113's behaviour, r129.

## Shape

CLAUDE.md is checked rule by rule and module-map row by row, for what the branch touched.

**Rules:**
- **Size limit, 300 lines:** met. `tools size` prints nothing.
- **"A new concern gets a new module and a row here":** met for `scripts/supervise_outputs.py`. Its row was added at `CLAUDE.md:29`, and the file is 30 lines.

**Module-map rows:**
- `scripts/supervise*.py`: met. The changes are to faults (`supervise_faults.py:96`, `note`; `:174` and `:183`, `how_ended` and `ended_of`), rounds (`supervise_rounds.py:106-158`), answers (`supervise_answers.py:110-122`), intake (`supervise_intake.py:88-107`), merge (`supervise_merge.py:131-136`) and worker (`supervise_worker.py:247-256`, `outcome`). Each change lands in the module whose concern it is.
- `scripts/supervise_answers.py` (answers under a delegation): met.
- `scripts/supervise_intake.py` (intake rounds): met.
- `tests/scenarios/` ("one `<capability>_*_steps.py` module a concern"): met. The new modules are `supervision_outputs_steps.py`, `supervision_session_faults_steps.py` and `supervision_then_faults_steps.py`. `supervision_given.py` and `supervision_then_workers.py` already did not follow the `_steps` pattern at Base.
- `tests/scripts/`: met. `stub_claude.py` gains `DELIVERS`, at lines 66-70.

**Code no scenario reaches:** vulture is clean. The removed step definitions bound only retired scenarios (listed above). I did not search the remaining step texts against `features/` one by one, and vulture cannot see step bindings.

**A refactor, as an observation:** `supervise_rounds.run_round` (lines 86-167) now decides each round kind's output in-line. Moving this into `supervise_outputs.missing` with a round kind would put all of r132 in one module. It is complete when `grep -n "kind == \"apply\"\|kind == \"formulate\"" scripts/supervise_rounds.py` finds no output check, and r131's question is built only in `supervise_outputs.question`.

## Code no line asks for

None. Each new observable behaviour is asked for by a line:
- the fault recorded and printed on a proposal, the initiative or an answered node (`supervise.py:218-219, 246-256`; `note`): r128 and the person's reading A;
- the r88 words "ended in an error", "ended at its turn limit" and "left no result `work run` can read" (`how_ended`, `NO_RESULT`): r88;
- the missing-output questions (`supervise_outputs.py`, `supervise_merge.py:135`, `supervise_rounds.py:145-146`): r131;
- the answering-session fault no longer stopping the run (`supervise_answers.py:110-113`): r89 and r128.

## Coupling

- **Claude Code CLI's JSON result.** `how_ended` (`supervise_faults.py:174`) and `cut_short` read `subtype == "error_max_turns"`, `num_turns` and the exit code. These are fields the headless CLI documents in `--output-format json`. If a new error subtype appeared, it would read as "ended in an error", which is safe. The behaviour is stable while the documented fields hold.
- **The agents' result fields.** The new output check depends on the plugin's own agents writing `fileset` (code-scout), `plan` and `fileset` (bdd-planner) and `findings` (bdd-task-reviewer). `agents/*.md` say so at code-scout.md:82, bdd-planner.md:47-48 and bdd-task-reviewer.md:62. This is within the repository, not an outside contract. A change to an agent's result form now sends every one of its stages to `awaiting-answer`. A test reading each agent's result list against `supervise_outputs` would hold them together.
- **pytest-bdd on pytest internals.** pytest-bdd 8's `_register_fixture` and `FixtureDef(baseid=...)` raise `PytestRemovedIn10Warning` (259 warnings per run). The suite will break on pytest 10 until pytest-bdd follows. Pinning `pytest<10` in the project's requirements would make this stable. The unregistered `@deprecated` mark (`PytestUnknownMarkWarning`) would fail under `--strict-markers`; registering it in `pytest.ini` would stop that.

## Observations

1. The formulate round goes to `formulated` without its scenarios (Finding 1): `pytest -k "taken_as_its_stages_output and formulate"` gives 1 passed with no scenario committed.
2. Decision 0039 still guards on DONE (Finding 2): `grep -n DONE spec/decisions/0039-work-item-lifecycle-as-run.md` gives 6 lines.
3. "gave DONE" in the round errors (Finding 3): `grep -n "gave DONE" scripts/supervise_rounds.py` gives 139 and 173.
4. An intake round with nothing ends "ended" (Finding 4): read `supervise_intake.py:88-107`; there is no output test.
5. An implementer with no commit and tests passing is merged (Finding 4): read `supervise_outputs.py:12-25`, which has no implementer case.
6. By-hand commits outside a work-item (Finding 5): `git show --stat 46b35719 33ba1e88 5d6c49ad 8c1d9d51`.
7. Committed round scripts fail ruff (Finding 6): `tools check --base 50a40103` exits 1 with 8 errors under `.shop/work/i38/runs/`.
8. Deprecated-for-removal scenarios have no retirer (Finding 7): `features deprecated` lists 5.
9. q8's resolution cites the removed r113 (Finding 8): `model check` gives v3 on q8.
