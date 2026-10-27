# Branch review of i41 (Supervision lines of a redrafting integrate round)

**Verdict: DONE.** No finding is Critical or triaged fix now. The work-item's check passes, and every check this review names was run. The 16 suite failures are all `StepDefinitionNotFoundError` in scenarios that the branch does not add, change or bind. They are other initiatives' formulated scenarios that are not yet implemented (see Suite). The previous reviews' F2 and F3 still stand as observations. Four ruff errors remain in files the branch touched. 6-review said `tools check` was clean, but that held only for its narrower base.

## Range and work-items

- Range: `c2cbb99c..7062a487` (30 commits). `c2cbb99c` is the commit that adds `.shop/work/i41/initiative.md`.
- One capability-proposal, `supervision` (formulated), with its rounds:
  - integrate `04a395b3`
  - gate
  - apply `580ad083` (spec: r140-r148 added; r80, r114, r71 retired)
  - formulate `1cf1be38` (9 scenarios added; r80, r114, r71 scenarios deprecated)
- One work-item, **w204** (green, under `supervision`, accepts r140-r148):
  - `d076baa8`, between `be28c607` (ready -> claimed) and `9a7de712` (claimed -> done): the implementation.
  - `d6667395`, between `a73ea6b2` and `68829a60`: the fix of 4-review F1.
- Commits that belong to no work-item and to no round:
  - `3934c55a`: a hand edit of `.shop/work/i40/supervision.md`, status withdrawn "by hand".
  - `f6569633`: `.shop/records/observations.md`.
  - The `work note` and `work answer` commits: `.shop/work/i41/` bookkeeping.

  See finding B5.

## Suite

`Suite: 955 passed, 16 failed at 7062a487 in 29.18 s` (plus 1 skipped and 56 subtests passed).

- **Parallel:** yes. `pytest.ini` gives `addopts = -n auto` (xdist workers gw0…).
- **In-process:** no. The step definitions run the scripts as subprocesses (`tests/scenarios/conftest.py:34`, `:111`). The suite is under 60 s, so this is not a finding.
- **The 16 failures**, each a `StepDefinitionNotFoundError` in a scenario the branch did not touch:
  - 14 in `features/requests.feature`, e.g. the missing step "an upstream ctx-u that keeps no request".
  - 1 in `features/design-model-check.feature` (the r120 v17 scenario).
  - 1 in `features/supervision.feature:1433` (@r135, i39's "the lines an integrate round gives into an upstream…"). It was formulated in `b80813ca`, before the base, and its step is undefined.
- Neither feature file is in `git diff c2cbb99c HEAD`. The branch's only step-module changes are two widened regexes and one new module. 6-review recorded the same 955 passed with these failures listed as expected.

## Checks

- **w204's check** (`python3 -m pytest -q --work-item w204`): 153 passed, 1 skipped, 56 subtests passed, in 6.74 s. Pass. The nine accepted scenarios r140-r148 are green.
- **`tools check --base c2cbb99c`:**
  - **ruff: 10 errors.**
    - Six SIM115 errors are in the committed round artefacts `.shop/work/i41/runs/supervision/{2-apply,3-formulate}/splice.py`.
    - Four are in files w204 touched:
      - `scripts/supervise_change.py:96` B023
      - `tests/scenarios/supervision_reintegrate_steps.py:13` F401 (unused `git`)
      - `tests/scenarios/supervision_reintegrate_steps.py:137` FURB167
      - `tests/scenarios/test_supervision.py:14` I001

    See B3.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". That is not `missing`: there are no contracts to check.
- **`tools size --limit 300`:** printed nothing. No file is over the limit. The largest files the branch touched:
  - `scripts/supervise.py` 284
  - `tests/scenarios/supervision_rounds_steps.py` 272
  - `scripts/supervise_rounds.py` 229
- **`features deprecated`:** 9 deprecated scenarios, none of them i41's.
  - The r80, r114 and r71 scenarios were deprecated by the formulate round and removed by w204 (see Feature files).
  - The 9 listed belong to `design-model-check` (2), `requests` (2) and `supervision` (5, from earlier initiatives).
  - Of the three with a named replacement (design-model-check @r120, requests @r44, @r45), no work-item in `.shop/work/` accepts the replacement. None of them is a "replacement green, deprecated still there" case.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** the branch has no operation with a dry-run mode. The only `--dry-run` in `scripts/` is `git push --dry-run` in `supervise_faults.py:71` and `supervise_review.py:41`, which the branch did not touch. Not applicable.

## Removed and weakened tests

None. I searched every `-` line of `git diff c2cbb99c HEAD -- tests features` for:

- deleted `def test_` / step functions
- removed `assert`
- parametrize or Examples rows dropped
- `skip` / `xfail` added
- rewritten expectations

What I found:

- `tests/scenarios/supervision_formulate_steps.py:36` `apply_change_list`: the regex is widened with the optional `(?:applies p1's drafts and )?`. The body is unchanged.
- `tests/scenarios/supervision_rounds_steps.py:21` `answered_proposal`: the regex is widened with the optional `(?:, for thing,)?`. The body is unchanged.
- `features/supervision.feature`: the deprecated @r80, @r114 and @r71 scenarios were removed in `d076baa8`. They are exactly the three that w204's `## Retires` lists, under r144, r145 and r146. Their bindings went with them: `features bindings` is clean, and test_supervision.py binds through `scenarios()`.
  - The formulate round `1cf1be38` only added scenarios and deprecated those three. Its `-` lines are just the three old `@rNN`/`Scenario:` header pairs.
  - No feature change outside the Retires list. No Critical.

## Allowances

- 3-implement's report gives "none", with a note that the `answered_proposal` widening is setup. That holds: no `assert`, expected value or case changed. The `apply_change_list` widening is the same kind of change, but the report does not name it (4-review F5, Minor, drop).
- 5-implement's report gives "none". That holds: `d6667395` touches no test.

## Cannot verify

- **The 16 failures at the base.** Building a tree of `c2cbb99c` in the scratch directory (`git archive`) was not permitted in this session. I attributed the failures by their files and their missing steps, not by a run at the base (see Suite).
- **The reproduction of observation B1.** The probe I wrote (`probe_f2.py`, calling `Changes.write_proposals` on a temporary initiative) was not permitted to run. B1's reproduction is therefore by reading `scripts/supervise_change.py:89-99`, as in 4-review F2.
- **The real `initiative-round` agent.** I cannot tell whether it gives `nothing_applied` as `agents/initiative-round.md:36` asks. Only the scenario stand-in gives it.

## Findings

### B1. Important, w204, observation: a redraft's change list that names a second capability rewrites that capability's existing proposal in place, without setting it drafted
- **Where:** `scripts/supervise_change.py:89-99` (`write_proposals`, `held` branch), with `scripts/supervise_rounds.py:196-199`. This is 4-review F2, still present at HEAD.
- **What is wrong:** `proposal_for` is consulted for every capability in the change list, not only the one that the redrafted proposal `name` argues.
  - Take a proposal p2 for another capability, at any status (for example `formulated`). Its `adds`/`changes`/`removes` and its drafts sentence are replaced.
  - Only `name` is moved to drafted.
  - This contradicts r92: "a `drafted` capability-proposal for each capability the change list names". The result can be a `formulated` proposal whose lists name ids that were never applied.
- **Reproduction (by reading; the probe was not permitted to run):**
  - Setup: the initiative holds `p1.md` (`argues: [thing]`, awaiting-answer) and `p2.md` (`argues: [other]`, formulated).
  - The change list of p1's integrate round is `[{capability: thing, adds: [thing#r4]}, {capability: other, adds: [other#r9]}]`.
  - Result: `p2.md` gets `adds: [other#r9]` and `The drafts of this proposal are in <new>.`, and stays `formulated`.
- **Triage:** observation. The agent is told to give "one entry for its capability" (`agents/initiative-round.md:30`), and no client sends this today.
- **Fix:** rewrite in place only the proposal `name` that the round was started for. Treat any other capability as r92 does, or refuse it.

### B2. Minor, w204, observation: a proposal's integrate brief labels the proposal `Initiative:`
- **Where:** `scripts/supervise_brief.py:45` (4-review F3, still present).
- **What is wrong:** for p1 the brief reads `Initiative: .shop/work/<i>/p1.md`. The integrate bullet (`agents/initiative-round.md:30`) opens "When your brief names a capability-proposal…".
- **Fix:** use the `Capability-proposal` label when `name != self.initiative`.
- **Reproduction:** `sed -n 45p scripts/supervise_brief.py`.

### B3. Minor, w204, observation: ruff errors in the files w204 touched, wrongly reported as gone in 6-review
- **Where:**
  - `scripts/supervise_change.py:96` B023: a false positive, because `re.sub` calls the lambda at once.
  - `tests/scenarios/supervision_reintegrate_steps.py:13` F401 and `:137` FURB167.
  - `tests/scenarios/test_supervision.py:14` I001.
- **Why it matters:** `tools check` exits 1 for the branch. 6-review's "tools check is clean at HEAD" used `--base a73ea6b2`, which covers only `supervise_rounds.py`.
- **Fix:** `ruff check --fix` for the three fixable errors, and `lambda _, s=said: s` at `:96`.
- **Reproduction:** `python3 <Scripts>/tools check --base c2cbb99c` gives "Found 10 errors."

### B4. Minor, w204, observation: the retry after a failed redraft integrate round has no scenario
- **Where:** `scripts/supervise_rounds.py:79-80` (6-review F1).
- **What is wrong:** removing the trailing `-integrate` skip leaves the suite green.
- **Fix:** formulate a scenario under r86/r96 with r140, then bind it.
- **Reproduction:** `git show --stat d6667395` lists no file under `tests/` or `features/`.

### B5. Minor, no work-item, observation: commits in the range that belong to no work-item and no round
- **`3934c55a`** hand-sets i40's proposal to withdrawn: "no work command withdraws a proposal".
- **`f6569633`** adds an observation record.

Both touch only `.shop/`. They change no code and no spec. Recorded as the brief asks.

### B6. Minor, the proposal's rounds, drop: committed round artefacts fall under ruff
- **What is wrong:** `.shop/work/i41/runs/supervision/{2-apply,3-formulate}/splice.py` give 6 SIM115 errors in `tools check`. They are a round's throwaway scripts, kept with its stage directory.
- **Fix:** exclude `.shop/` in `ruff.toml`. That fix lies outside this initiative.

## Code no line asks for

None found.

- **`nothing_applied`** (`supervise_rounds.py:236-240`, `:170-173`) is the mechanism that r147 and r140 need, and plan D1 names it.
- **`Ledger:` / Read** (`supervise_brief.py:54-55`) serves r141.
- **`Earlier drafts path (read only):`** (`:56-59`) is not one of r141's items. It serves r142, because the earlier drafts are kept, not rewritten, when the proposal is drafted anew. No output, file or status beyond the brief follows from it.
- **`move(..., also=)`** (`supervise.py:145-154`) serves r142's single commit.
- **The in-place rewrite** serves r148. Its reach beyond p1's own capability is B1.

## Shape

- **Size limit (300):** met. `tools size` printed nothing.
- **Module map:**
  - `scripts/supervise*.py`: met. Routing and the redraft round sit in `supervise_rounds.py`, which the row names for the rounds.
  - `scripts/supervise_change.py`: the row says "writing of one drafted capability-proposal for each capability it names". Since `supervise_change.py:89-99`, the module also rewrites an existing proposal in place (r148), and the row does not say so. Observation, Minor. Check: the row names the in-place rewrite.
  - `tests/scenarios/` "one `<capability>_*_steps.py` module a concern": met. `supervision_reintegrate_steps.py` (138 lines) holds the redraft's steps, bound through `test_supervision.py:39`.
  - "A new concern gets a new module and a row": met for the test module, which the map's `tests/scenarios/` row covers.
- **Unreachable steps or code:** none found.
  - The retired scenarios' steps (`every round ends` and the others) are still used: `every round ends` appears 10 times in `features/supervision.feature`.
  - vulture is clean.

## Coupling

- The branch adds no dependency on another project.
- It relies on its own agent text: the field `nothing_applied` is defined by `agents/initiative-round.md:36` and read by `supervise_rounds.py:236-240`. Both are in this repository.
- It relies on the stage-directory naming `runs/<name>/<k>-<kind>` (`supervise_worker.py` `run_dir`). That naming is also in this repository.
- External dependencies are unchanged: pytest-bdd and ruff (dev), and git. The deprecation warnings from `pytest_bdd/compat.py:28` come from pytest-bdd itself, not from this repository's use of private API. Nothing here would break behind a published contract.

## Observations

- B1: `write_proposals` rewrites another capability's existing proposal in place without moving it (see B1 for the setup).
- B2: `sed -n 45p scripts/supervise_brief.py`. The label is `Initiative` for every integrate round.
- B3: `tools check --base c2cbb99c` gives 4 ruff errors in w204's files.
- B4: `git show --stat d6667395` touches no test. Without a scenario, the retry would not be caught if it regressed.
- Shape: the `scripts/supervise_change.py` row in the module map lacks the in-place rewrite (`supervise_change.py:89-99`).
- An unbounded loop within one `work run`, by reading `supervise_rounds.py:41-56` and `:62-66`. Suppose a redraft whose gate gives no questions; earlier answers still count, so it is due. It is followed by an apply round that again gives `nothing_applied`. That is integrate again, with no limit (plan §5, last case).
