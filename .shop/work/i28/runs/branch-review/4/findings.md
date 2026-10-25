# Branch review of i28 (review 4, at 125b2ad1)

**Verdict: DONE.**

- Every check of i28's six work-items passes, and I ran each one myself.
- No finding is Critical and none is triaged fix now.
- No code, test or step definition has changed since review 3 passed at `4640ef08`. The 47 commits since then are of two kinds:
  - queue commits and records under `.shop/`;
  - i25's and i26's spec and feature rounds: `112fe1b6`, `5c441e9e`, `3d3da4df`, `1c0c4fb6`, `d07a8b38` and `159bdfdf`.
- **The suite is red at head: 8 failures.** Every one is a `StepDefinitionNotFoundError` in a scenario that those i25 and i26 formulate rounds added after review 3: requests r4, r5, r12, r20 and r21 for i26, and work-queue r26, r27 and r28 for i25. None of these scenarios is i28's, and none of i28's work-items reaches them (finding 6).
- What remains of i28 is the Minor carried over from review 3: the ruff errors, the module-map row and the deprecated @r102 scenario.

## Range and work-items

- **Range:** `4b7dca6c..125b2ad1` on `i25-review-findings-to-implementation`. Head is `125b2ad1` ("work: w174 ready -> claimed", an i25 work-item).
- **w167** (supervision#r92): `12f0b295`
- **w168** (work-queue#r30): `fa6929fb`
- **w169** (spec-integration#r43, a guarantee): `50788670`
- **w170** (supervision#r102, r103, r104): `bcc41527`, `55eea183`, `2e0f2555`
- **w171** (supervision#r102, the fix of w170's task-review finding): `a414d2bd`
- **w172** (the fix of branch review 1): `a1ff989a`
- **Commits that belong to no work-item of i28:**
  - those that review 3 listed;
  - since `4640ef08`, the commits of i25, i26 and i29 and of q7's intake:
    - spec applies `112fe1b6`, `5c441e9e`, `1c0c4fb6` and `d07a8b38`;
    - formulate commits `3d3da4df` and `159bdfdf`, with merges `f13e5b08`, `05a71892` and `bcdaac6a`;
    - `90ff4a17` and `0adf90f8`, the records of branch review 3 of i28 and of i27;
    - `409627b7`, an observation record;
    - the queue's `work answer`, `work note`, `work add`, `work retry` and `work:` transitions, and `work request`, `outcome` and `turn` for q7.
  - See finding 5.

## Suite

`Suite: 870 passed, 8 failed at 125b2ad1 in 35.5 s` (1 skipped, 56 subtests passed; pytest's own figure is 35.07 s).

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- The suite takes under 60 s, so the wall time is no finding.
- **The 8 failures**, each a `StepDefinitionNotFoundError`:
  - **`features/requests.feature`**, five scenarios:
    - @r4 "…leaves the request's lines and answers as the asker wrote them";
    - @r5 "the asker answering a question leaves…";
    - @r12 "a change to a request commits…";
    - @r20;
    - @r21.
  - **`features/work-queue.feature`**, three scenarios: @r26, @r27 and @r28.

## Checks

**Each work-item's check, `pytest --work-item <w>`, which I ran myself at `125b2ad1`:**

| Work-item | Result |
|---|---|
| w167 | 144 passed, 1 skipped |
| w168 | 144 passed, 1 skipped |
| w169 | 142 passed, 1 skipped |
| w170 | 146 passed, 1 skipped |
| w171 | 144 passed, 1 skipped |
| w172 | 146 passed, 1 skipped |

w169's spec-integration#r43 is a guarantee, so no scenario covers it. The four instruction files that carry it are unchanged since review 3, which read them against the line. They still match the brief's label at `scripts/supervise_brief.py:79`.

**`tools check --base 4b7dca6c`:**

- **ruff:** fails with 5 errors, the same 5 as reviews 2 and 3 (finding 4):
  - `scripts/supervise_brief.py:82` ISC004
  - `tests/scenarios/supervision_intake_steps.py:65` FURB167
  - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
  - `tests/scripts/stub_claude.py:186` FURB167
  - `tests/scripts/stub_claude.py:187` FURB167
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing, so no file is over the limit.
- **`features deprecated`:** eight deprecated scenarios.
  - supervision @r102 is i28's (finding 3).
  - requests @r4, @r5 and @r12 come from i26's formulate round, `3d3da4df`.
  - work-queue @r14 comes from i25's formulate round, `159bdfdf`.
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
  - The replacements of the i25 and i26 scenarios are not green, which is right while they wait for their work-items.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing i28 touches has a dry-run mode and a real mode of one operation. There is no randomized test to run and no finding.

## Removed and weakened tests

None in i28's commits.

What I searched for:

- **Since review 3:** `git diff --stat 4640ef08 HEAD` touches nothing under `tests/`. Under `features/`, the removed lines (`git diff 4640ef08 HEAD -- features/ | grep '^-'`) are only the old tag and title lines of requests @r4, @r5 and @r12 and of work-queue @r14. Each was re-added with `@deprecated` and "(deprecated)" by i26's or i25's formulate round, not by a work-item.
- **Over the whole range:** the findings of review 3 hold unchanged. The removed test lines are only:
  - imports;
  - one docstring line;
  - the stub's heading regex, widened;
  - `re.M` becoming `re.MULTILINE`.

  No `skip`, `xfail` or mark was added. w172's `integrate_given_ids` is stricter than before.

## Allowances

Unchanged since review 3, and the commits behind them are unchanged:

- **w171, `other_initiative`, setup: holds.** `a414d2bd` changes only the draft's path, adding `round-1/`.
- **w172, `integrate_given_ids`, interim: holds.** The step was first committed in `55eea183`, after Base, and now asserts plan decision D2.
- **w167, w168, w169 and w170:** each report gives "none".

## Cannot verify

No check is unverified.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:79`.
- **What I verified:** the line is unchanged and still writes the label the round's instructions name.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` starts the initiative of an accepted request that no initiative fulfils, and the row does not say so.
- **Fix:** add "and the start, with `work start`, of the initiative of an accepted request no initiative fulfils (r103)" to the row.
- **Triage:** observation. It is unchanged from reviews 1 to 3.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-item is green
- **Where:** `features/supervision.feature`, the deprecated @r102 scenario, with its step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:157-167`).
- **What is wrong:** w171 and w172, which deliver the replacement, are green. Neither has a `## Retires`.
- **Fix:** a work-item accepting supervision#r102 that retires the deprecated scenario, its binding and `other_initiative`.
- **Triage:** observation.

### 4. Minor, w167, w170 and w172, drop: the 5 ruff errors under Checks
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** parenthesize the string at `supervise_brief.py:81-83`, then run `ruff check --fix` on the other three files.
- **Triage:** drop.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item of i28
- **What:** the commits listed under Range.
- **Why it is not more:**
  - The code-free kinds land on whatever branch is checked out (work-queue r9): queue commands, records, and the spec and feature rounds of i25, i26 and i29.
  - This branch is shared by i25, i26, i27, i28 and i29, as the ledger records.
  - None of them changes code or tests.
- **Triage:** drop.

### 6. Minor, none of i28 (i25 and i26), observation: the suite at head is red on scenarios formulated for other initiatives
- **Where:**
  - `features/requests.feature` @r4, @r5, @r12, @r20 and @r21, from `3d3da4df` (i26);
  - `features/work-queue.feature` @r26, @r27 and @r28, from `159bdfdf` (i25).
- **What is wrong:** their steps are not written yet.
  - i25's w174 (claimed) accepts work-queue r26, r27 and r14. **It does not accept r28**, so the r28 scenario has no work-item that would turn it green. That is for i25's own review to take up.
  - i26 has no work-item yet for requests r4, r5, r12, r20 or r21.
- **Why it matters:** this is the red-first state of in-flight work, not a regression of i28. But anyone who runs the whole suite on this branch, or merges it to main, gets 8 failures until i25 and i26 deliver.
- **Fix:** none in i28. Do not release or merge this branch until those work-items are green, and give r28 a work-item in i25.
- **Triage:** observation.
- **Reproduction:** `python3 -m pytest -q` at `125b2ad1` gives "8 failed, 870 passed". Each failure's `E` line is `StepDefinitionNotFoundError`. `grep accepts .shop/work/i25/w174.md` gives `[work-queue#r26, work-queue#r27, work-queue#r14]`.

## Shape

Unchanged since review 3, because no code changed:

- **Size limit:** met.
- **`supervise_drafts.py`:** has its row (`CLAUDE.md:32`).
- **Module-map rows:**
  - met for `supervise_brief.py`, `workqueue_answer.py`, `supervise_change.py`, `supervise_draft.py` and `tests/scenarios/`;
  - not met for `supervise_all.py` (finding 2).
- **Code no scenario reaches:** none today. Once finding 3's scenario is retired, `other_initiative` is reached by nothing. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none.
- **Behaviour against the lines and the Purpose:** no contradiction found. The real queue still agrees:
  - **r102:** three kept drafts are now on the queue, i25's, i26's and i29's, all under `runs/<i>/<n>-integrate/drafts/round-1/spec/capabilities/`. That is the layout `kept_drafts` globs.
  - **r103:** q7 is `accepted`, and no `initiative.md` fulfils it. The next `work run` starts its initiative, as r103 says (`supervise_all.py:18-35`).

## Coupling

The branch adds no dependence on another project. Two couplings were there before it:

- **pytest-bdd and pytest 10:** pytest-bdd relies on internals that pytest 10 removes (`PytestRemovedIn10Warning`, `pytest_bdd/compat.py:28`). Pin `pytest<10` beside pytest-bdd.
- **The `@deprecated` tag:** pytest-bdd treats it as an unregistered mark (`PytestUnknownMarkWarning`). Register `deprecated` under `markers` in `pytest.ini`.

## Observations

- **w168: a capability-proposal's commit subject drops the initiative.**
  - `workqueue_answer.py:30` rebinds `name` before `:56` and `:58` use it.
  - Reproduction: `git show --stat 056ba39a 134a84a8` gives the same subject "work answer: supervision" for `.shop/work/i25/supervision.md` and `.shop/work/i26/supervision.md`. `804a237d` ("work answer: requests") shows it again.
- **w170: a start of several requests is not atomic.** If `work start` refuses a later request after an earlier one has committed, the earlier initiative stays started.
  - Reproduction: by reading `supervise_all.py:31-35` against `workqueue_start.py:25-33`.
- **w171: r102 also gives ids that a later round of the same initiative renumbered.** i26's kept draft still holds supervision r98 and r99, although its spec apply `d07a8b38` used r100 and r101. The cost is only skipped ids.
  - Reproduction: `.shop/work/i26/runs/i26/2-integrate/drafts/round-1/spec/capabilities/supervision.md` against `git show d07a8b38 --stat`.
- **w169: `integrating-a-proposal`'s dispatch templates have no slot for the given ids.** The round passes them freehand.
  - Reproduction: by reading the skill's Template.
- **w168: the refusal for a missing `<initiative>/<name>` file says "work-item" even for a capability-proposal.**
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py:37`.
