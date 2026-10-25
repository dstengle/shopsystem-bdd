# Branch review of i28 (review 3, at 4640ef08)

**Verdict: DONE.**

- The suite is green. I ran every work-item's check myself, and each passes.
- No finding is Critical and none is triaged fix now.
- No code, test, feature or spec file has changed since review 2 passed at `3e969c93`. The 30 commits since then touch only `.shop/`:
  - branch review 2's own record;
  - i28's measurement and analysis;
  - 25 `work answer` commits on i25's and i26's capability-proposals;
  - the start of i29.
- What remains is Minor, as in review 2: ruff, the module-map row and the deprecated @r102 scenario.
- New this time, as evidence on the real queue rather than a finding:
  - r30 routed the answers correctly between i25's and i26's proposals, which share the name `supervision`.
  - r103 started i29 for q5.

## Range and work-items

- **Range:** `4b7dca6c..4640ef08` on `i25-review-findings-to-implementation`. Head is `4640ef08` ("work: start i29, fulfilling q5").
- **w167** (supervision#r92): `12f0b295`
- **w168** (work-queue#r30): `fa6929fb`
- **w169** (spec-integration#r43, a guarantee): `50788670`
- **w170** (supervision#r102, r103, r104): `bcc41527`, `55eea183`, `2e0f2555`
- **w171** (supervision#r102, the fix of w170's task-review finding): `a414d2bd`
- **w172** (the fix of branch review 1, accepting r102, r103 and r104): `a1ff989a`
- **Commits that belong to no work-item:**
  - From before review 2: `f85f0d23`, `7e6266ca`, `79f4b429`, `7636eb12`, `1649e9d2`, `f3143c56`, `d4a85c1e` and `cb04d752`, with the queue's own `work note`, `work add` and `work retry` commits.
  - New since review 2:
    - `6a6271af`: branch review 2's record.
    - `ab63bd6c`: the i28 records, which work run wrote but did not commit (q5).
    - `056ba39a..134a84a8`: 25 `work answer` commits on `.shop/work/i25/` and `.shop/work/i26/`.
    - `4640ef08`: the start of i29.
  - See finding 5.

## Suite

`Suite: 867 passed, 0 failed at 4640ef08 in 33.9 s` (1 skipped, 56 subtests passed; pytest's own figure is 33.51 s).

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- The suite takes under 60 s, so this is no finding.

## Checks

**Each work-item's check, `pytest --work-item <w>`, which I ran myself:**

| Work-item | Result |
|---|---|
| w167 | 144 passed, 1 skipped |
| w168 | 144 passed, 1 skipped |
| w169 | 142 passed, 1 skipped |
| w170 | 146 passed, 1 skipped |
| w171 | 144 passed, 1 skipped |
| w172 | 146 passed, 1 skipped |

w169's spec-integration#r43 is a guarantee, so no scenario covers it. I read the line against the instructions that carry it:

- `agents/initiative-round.md:27`
- `skills/integrating-a-proposal/SKILL.md:23`
- `agents/capability-writer.md:20-22`
- `docs/capability-format.md:162-163`

All of them match the brief's label at `scripts/supervise_brief.py:79` ("Ids drafted elsewhere").

**`tools check --base 4b7dca6c`:**

- **ruff:** fails with 5 errors, the same 5 as review 2 (finding 4):
  - `scripts/supervise_brief.py:82` ISC004
  - `tests/scenarios/supervision_intake_steps.py:65` FURB167
  - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
  - `tests/scripts/stub_claude.py:186` FURB167
  - `tests/scripts/stub_claude.py:187` FURB167
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing, so no file is over the limit.
- **`features deprecated`:** four deprecated scenarios.
  - supervision @r102 is this branch's (finding 3).
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing the branch touches has a dry-run mode and a real mode of one operation. There is no randomized test to run and no finding.

## Removed and weakened tests

None.

What I searched for:

- `git diff --stat 3e969c93 HEAD` touches nothing under `tests/` or `features/`.
- Over the whole range, as in review 2, the removed lines under `tests/` and `features/` in `git diff 4b7dca6c HEAD` are only:
  - imports;
  - one line of the stub's docstring;
  - the stub's heading regex, widened to also capture the name;
  - `re.M` becoming `re.MULTILINE` in `listed`, with the same behaviour.
- No `skip`, `xfail` or `pytest.mark` was added.
- No work-item commit touches `features/`.
- w172's `integrate_given_ids` is stricter than before: it now asserts the label line, and each id on that line.

## Allowances

- **w171, `other_initiative`, setup: holds.** `git show a414d2bd` changes only the path the draft is written to, adding `round-1/`. No assert, expected value or parametrize case changes.
- **w172, `integrate_given_ids`, interim: holds.**
  - The step was first committed in `55eea183`, after Base.
  - It now asserts what plan decision D2 says: the label, with each given id on that line.
- **w167, w168, w169 and w170:** each report gives "none". The commits change no existing test.

## Cannot verify

No check is unverified.

- The sandbox refused to run a probe that imported `supervise_drafts` and `supervise_all` against this checkout's queue.
- I read the same facts by hand instead. These readings are not checks a work-item names:
  - **r102:** the kept drafts on the queue are `i25/runs/i25/2-integrate/drafts/round-1/spec/capabilities/{supervision,work-queue}.md` and `i26/runs/i26/2-integrate/drafts/round-1/spec/capabilities/{supervision,requests}.md`. Against `spec/`, they add supervision#r98 and r99, work-queue#r26 and r27, and requests#r20 and r21. Those are the ids i29's integrate round would be given, and the layout `kept_drafts` globs.
  - **r103:** all six requests (q1 to q6) are `accepted`, and each is now fulfilled by one initiative (i24, i25, i26, i27, i29 and i28). So `unfulfilled` gives none, and the next `work run` starts no further initiative.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:79`.
- **What I verified:** the line is unchanged since review 2 and still writes the label the round's instructions name.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` now starts, with `work start`, the initiative of an accepted request that no initiative fulfils. The row names only "every open initiative taken side by side…". `4640ef08` shows this start happening on the real queue.
- **Fix:** add "and the start, with `work start`, of the initiative of an accepted request no initiative fulfils (r103)" to the row.
- **Triage:** observation. It is unchanged from reviews 1 and 2.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-item is green
- **Where:** `features/supervision.feature:1239-1250`, with its step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:157-167`).
- **What is wrong:** the replacement at `:1252` is delivered by w171 and w172, both green. Neither has a `## Retires`.
- **Fix:** a work-item accepting supervision#r102 whose `## Retires` lists the deprecated scenario. It removes the scenario, its binding and `other_initiative`.
- **Triage:** observation.

### 4. Minor, w167, w170 and w172, drop: ruff errors on lines the branch added or touched
- **Where:** the 5 errors under Checks.
- **The w172 part:** `supervise_brief.py:82` ISC004. w172's report says it fixed this, but the implicit concatenation inside the list is still there.
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** parenthesize the string at `:81-83`, then run `ruff check --fix` on the other three files.
- **Triage:** drop.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item
- **What:** the commits listed under Range.
- **The new ones since review 2:**
  - the i28 records `ab63bd6c`;
  - 25 `work answer` commits on i25's and i26's proposals, the coordinator answering under the person's delegation of 2026-10-25;
  - `work start` of i29.
- **Why it is not more:**
  - None touches code, tests, features or spec.
  - Each is a queue command or a record. Both kinds land on whatever branch is checked out (work-queue r9).
  - That i28's branch now also carries i25's, i26's and i29's queue changes is the shared-branch layout the ledger records, not a defect of i28's code.
- **Triage:** drop.

## Shape

- **Size limit:** met. `tools size` prints nothing.
- **"A new concern gets a new module and a row":** met for `scripts/supervise_drafts.py` (`CLAUDE.md:32`).
- **Module-map rows the branch touched:**
  - `scripts/supervise*.py` "briefs": met (`supervise_brief.py:40-46` and `:73-81`).
  - `scripts/workqueue_answer.py`: met (`:29-36`).
  - `scripts/supervise_change.py`: met (`:47-50`).
  - `scripts/supervise_draft.py`: met (`:51`).
  - `scripts/supervise_all.py`: not met (finding 2).
  - `tests/scenarios/` "one module a concern": met.
- **Code no scenario reaches any more:** none today. Once finding 3's scenario is retired, `other_initiative` is reached by nothing. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none.
- **Behaviour against the lines and the Purpose:** no contradiction found. The real queue agrees:
  - The 25 answers landed one per initiative. i25/supervision got its 2, i26/supervision its 11, i25/work-queue its 4 and i26/requests its 11, each in its own initiative's file, as r30 says.
  - i29 was started for q5, as r103 and the changed Purpose say.

## Coupling

The branch adds no dependence on another project. Two couplings were there before it and remain:

- **pytest-bdd and pytest 10:** pytest-bdd relies on pytest internals that pytest 10 removes (`PytestRemovedIn10Warning` from `pytest_bdd/compat.py:28`).
  - The suite breaks on pytest 10.
  - Pinning `pytest<10` beside pytest-bdd keeps it stable.
- **The `@deprecated` tag:** pytest-bdd makes it an unregistered mark (`PytestUnknownMarkWarning`, 32 times). Registering `deprecated` under `markers` in `pytest.ini` stops the warning.

## Observations

- **w168: a capability-proposal's commit subject drops the initiative.** `work answer i25/supervision …` commits as "work answer: supervision", because `workqueue_answer.py:30` rebinds `name` to the bare name before `:56` and `:58` use it.
  - On a queue where two initiatives hold a proposal of one name, the log does not say which was answered.
  - Reproduction: `git show --stat 056ba39a 134a84a8` gives the same subject "work answer: supervision" for `.shop/work/i25/supervision.md` and `.shop/work/i26/supervision.md`.
- **w170: a start of several requests is not atomic.** If `work start` refuses a later request after an earlier one has committed, the earlier initiative stays started. No client reaches this today.
  - Reproduction: by reading `supervise_all.py:31-35` against `workqueue_start.py:25-33`.
- **w171: r102 also gives ids that a later round of the same initiative dropped or renumbered.** For example, i26's answer 6 moves its supervision lines to r100 and r101, but its kept draft still holds r98 and r99, so those are what r102 gives. The cost is only skipped ids.
  - Reproduction: `.shop/work/i26/supervision.md` `## Answers` 6, against `.shop/work/i26/runs/i26/2-integrate/drafts/round-1/spec/capabilities/supervision.md:6,48`.
- **w169: `integrating-a-proposal`'s dispatch templates have no slot for the given ids.** The round passes them freehand.
  - Reproduction: by reading the skill's Template and Question Template.
- **w168: the refusal for a missing `<initiative>/<name>` file names "work-item" even for a capability-proposal.** Wording only.
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py:37`.
