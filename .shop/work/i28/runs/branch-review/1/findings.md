# Branch review of i28

**Verdict: DONE_WITH_CONCERNS.** The suite is green and every check passes, apart from lint. There is no Critical finding. One Important finding is triaged fix now: the label the integrate brief uses for the other initiatives' ids is not the label that `initiative-round` and `integrating-a-proposal` are told to look for. Everything else is Minor and triaged observation or drop.

## Range and work-items

- Range: `4b7dca6c..1dfed57d` on `i25-review-findings-to-implementation`. Head is `1dfed57d` ("work: w171 done -> green").
- w167 (supervision#r92): `12f0b295`
- w168 (work-queue#r30): `fa6929fb`
- w169 (spec-integration#r43, guarantees): `50788670`
- w170 (supervision#r102, r103, r104): `bcc41527`, `55eea183`, `2e0f2555`
- w171 (supervision#r102, the fix of w170's task-review finding): `a414d2bd`
- Commits outside any work-item's claimed..done span:
  - the spec apply `f85f0d23`
  - the formulate commits `7e6266ca`, `79f4b429` and `7636eb12`
  - the hand-written capability-proposals `1649e9d2`
  - `work note`, `work add`, `work answer`, `work retry`, the start `f3143c56` and the integrate fault `d4a85c1e`

  See finding 5.

## Suite

`Suite: 867 passed, 0 failed at 1dfed57d in 22.5 s` (1 skipped, 56 subtests passed).

- It runs in parallel: `pytest.ini` has `addopts = -n auto`.
- It is not in-process: the steps start `work` and the other commands with `subprocess.run` (`tests/scenarios/conftest.py:34`, `:111`).
- It takes under 60 s, so this is no finding.

## Checks

- `pytest --work-item w167`: 144 passed, 1 skipped.
- `pytest --work-item w168`: 144 passed, 1 skipped.
- `pytest --work-item w169`: 142 passed, 1 skipped, no scenario collected. spec-integration is a guarantees capability.
  - I verified r43's text by reading `agents/initiative-round.md:27`, `agents/capability-writer.md:18-22`, `skills/integrating-a-proposal/SKILL.md:23` and `docs/capability-format.md:159-161`.
  - Finding 1 is the gap I found there.
- `pytest --work-item w170`: 146 passed, 1 skipped.
- `pytest --work-item w171`: 144 passed, 1 skipped.
- `tools check --base 4b7dca6c`:
  - **ruff**: 8 errors, so it fails (finding 4).
    - `scripts/supervise_brief.py:3` I001
    - `scripts/supervise_brief.py:82` ISC004
    - `tests/scenarios/supervision_intake_steps.py:65` FURB167
    - `tests/scenarios/supervision_integrate_steps.py:107` and `:112` FURB167
    - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
    - `tests/scripts/stub_claude.py:186` and `:187` FURB167
  - **vulture**: clean.
  - **import-linter**: "the project states no import contracts". No contract exists to read; `CLAUDE.md`'s module map states none.
- `tools size --limit 300`: printed nothing. No file is over the limit.
- `features deprecated`: four deprecated scenarios. Only the @r102 one in `features/supervision.feature` is this branch's (finding 3). The others, migration-tools @r15 and work-queue @r1 and @r9, were there before the branch.
- `features bindings`: "every binding names a scenario".
- Dry-run against real mode: nothing this branch touches has a dry-run mode of an operation. The only "dry-run" in `scripts/` is the `git push --dry-run` probe in `supervise_review.py:41` and `supervise_faults.py:67`. So there is no randomized test to run and no finding.

## Removed and weakened tests

None. What I searched for:

- removed lines under `tests/` and `features/` in `git diff 4b7dca6c HEAD`. These are only imports, a stub docstring line and the stub's heading regex, which was widened to also capture the name.
- added `skip`, `xfail` and `pytest.mark` lines: none.
- work-item commits that touch `features/`: none. Only the formulate commits do.

Inside the branch, w171 changed the setup of `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:146-155`), a step w170 added. It is under Allowances below.

## Allowances

- w171's row for `other_initiative`, the deprecated @r102 scenario: **holds as setup.**
  - The diff in `a414d2bd` changes only the path the draft is written to (`drafts/` becomes `drafts/round-1/`). No `assert`, expected value or parametrize case changes.
  - The test was first committed after Base (`55eea183`, w170), and w171's plan lists it under "Tests the decisions break".
  - The row's added word "Interim" claims nothing more than that.
- w167, w168, w169 and w170 report "none". Their diffs change no existing test.

## Cannot verify

Nothing a work-item names as a check. The behaviour of a live `initiative-round` under r43 has no test, because it is a guarantee. I judged it on its text (finding 1).

## Findings

### 1. Important, w170 (with w169), fix now: the integrate brief does not use the label the round's instructions name
- **Where:** `scripts/supervise_brief.py:79`, against `agents/initiative-round.md:27` and `skills/integrating-a-proposal/SKILL.md:23`.
- **What is wrong:**
  - The instructions tell the round to read the ids "when your brief lists requirement ids other initiatives' drafts add (its "Ids drafted elsewhere"…)". They also say "A brief that lists none leaves the numbering as it was."
  - The brief `work run` writes has no line by that name. It writes `Requirement ids other initiatives' kept drafts add, which spec/ does not hold yet; take none of them: …`.
  - Its wording also asks for less than r43: "take none of them" allows a lower free id, where r43 says "above every id it is given".
  - w169's implementer said so: "The label "Ids drafted elsewhere" must match what w170's integrate_lines writes; w170 should use it or reconcile". w170 did not, and no task review caught it.
- **Why it matters:** r102 and r43 exist together to stop two initiatives drafting the same id, which is the collision i28 was opened for (i25's and i26's supervision r98). A round that follows its text literally finds no "Ids drafted elsewhere" line and numbers as before. That is a wrong answer, the same collision again.
- **Fix:** make one label serve both sides. For example, write the brief line as `Ids drafted elsewhere (number added lines above each on the same capability): <ids or none>` in `supervise_brief.py:79`. Or change the two texts to quote the brief's words. Either way, assert the label in the r102 step (`integrate_given_ids`).

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md` module map, row `scripts/supervise_all.py`; the code is at `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` now starts, with `work start`, the initiatives of accepted requests that no initiative fulfils (r103). The row still reads only "every open initiative taken side by side, one `Run` each, and the exit on their statuses".
- **Fix:** add "and the start of the initiative of an accepted request no initiative fulfils (r103)" to the row.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-item is green
- **Where:** `features/supervision.feature:1239-1250`, with its step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:144-155`).
- **What is wrong:** the replacement scenario at line 1252 is delivered by w171, which is green. w171 was added by hand with no `## Retires`, so nothing retires the old scenario. Both scenarios now pass, because w171 moved the old step to the new layout.
- **Fix:** a work-item accepting supervision#r102 whose `## Retires` lists the deprecated scenario. That removes it, its binding, and the step `other_initiative`, which only it reaches.

### 4. Minor, w167 and w170, drop: ruff errors on the lines the branch added
- **Where:** as listed under Checks.
  - w170: `supervise_brief.py:3` (I001), `supervision_intake_steps.py:65`, `supervision_proposal_steps.py:96`.
  - w167: `supervision_integrate_steps.py:107`, `stub_claude.py:186`.
  - Already there before the branch, on lines it did not add: `supervise_brief.py:82` (ISC004), `supervision_integrate_steps.py:112` and `stub_claude.py:187` (FURB167).
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** `ruff check --fix` on the five files.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item
- **What:**
  - the spec apply `f85f0d23`
  - the formulate commits `7e6266ca`, `79f4b429` and `7636eb12`
  - the hand-written proposals `1649e9d2`
  - the queue's own `work note`, `work add`, `work answer` and `work retry` commits
- **Why it is not more:** each is a round or a queue command of the initiative, recorded in `.shop/work/i28/ledger.md`. The hand bootstrap is explained there (observation 2026-10-25-loop-collisions). None touches code or tests.

## Shape

- **Size limit (CLAUDE.md, Size limit):** met. `tools size --limit 300` prints nothing.
- **"A new concern gets a new module and a row here":** met for `scripts/supervise_drafts.py`, with a row added by w170 at `CLAUDE.md:32`.
- **Rows the branch touched:**
  - `scripts/workqueue_answer.py` (`work answer`): met, at `scripts/workqueue_answer.py:29-36`.
  - `scripts/supervise_change.py` (writing drafted proposals): met, at `:47-50`.
  - `scripts/supervise_draft.py` (drafting): met, at `:51`.
  - `scripts/supervise*.py` (briefs): met, at `supervise_brief.py:43-46`, `:76-80`.
  - `scripts/supervise_all.py`: not met. See finding 2.
  - `tests/scenarios/` "one `<capability>_*_steps.py` module a concern": met. r103's steps are in `supervision_intake_steps.py` (requests this context is the upstream of), r102's and r92's in `supervision_integrate_steps.py`, r104's in `supervision_proposal_steps.py`.
- **Code no scenario reaches any more:** none today. Once finding 3's scenario is retired, `other_initiative` (`supervision_integrate_steps.py:144`) is reached by nothing. Check: `features bindings`, and a grep for "whose kept drafts add", both after the retirement.
- **Code no line asks for:** none found.
  - The r104 lines in the gate brief serve r104.
  - `Intake.check` before `work start` in `run_all` serves r10 and r103.
  - `workqueue.entry` on both halves of `<initiative>/<name>` gives r30's form its refusals.
  - The stub's `round:<kind>:<name>` key is test harness.
- **Behaviour against the lines and the Purpose:** no contradiction found.
  - r102 says "not yet applied". The code reads it as "spec/ does not hold", and counts drafts of initiatives of any status. That gives every id r102 asks for. It gives more only for ids that are spec/'s already or drafts of abandoned initiatives, and those cost only skipped numbers.
  - The probe on this branch's real queue: `added_by_others(root, "i28")` gave `supervision#r98, work-queue#r26, work-queue#r27, requests#r20, requests#r21, supervision#r99`. For `i25` it gave `requests#r20, requests#r21, supervision#r98, supervision#r99`. These are i25's and i26's kept round-1 drafts, so r102 now works on the real layout.

## Coupling

The branch adds no dependence on another project's behaviour.

- It reads its own layout: the integrate round's `drafts/round-<m>/spec/capabilities/`, which supervision r91 and `initiative-round` give.
- It reads its own brief heading, `# <kind> of <name>`, in the stub.

Two couplings were there before the branch and the suite shows them:

- pytest-bdd uses pytest internals that pytest 10 removes: `PytestRemovedIn10Warning` from `pytest_bdd/compat.py:28` (`_register_fixture` with a nodeid) and `FixtureDef(baseid=…)`. The suite would break on pytest 10 until pytest-bdd follows. Pinning `pytest<10` beside pytest-bdd's version keeps it stable.
- pytest-bdd turns the `@deprecated` tag into an unregistered mark (`PytestUnknownMarkWarning`). Registering `deprecated` under `markers` in `pytest.ini` stops it.

## Observations

- **The next `work run` with no initiative will start an initiative for q5.** This is r103 working as written: q5 is `accepted` and no initiative fulfils it. Reproduction: a pytest probe in scratch calling `supervise_all.unfulfilled(root)` on this checkout returned `['q5']`. The person may want to know before the next run, if q5 was meant to be carried by i27.
- **A multi-request start is not atomic** (w170). `run_all` runs `Intake.check()` for every unfulfilled request and then `work start` for each. A refusal `work start` alone makes, after an earlier start has committed, leaves the earlier initiative started. Reproduction: by reading `supervise_all.py:31-35` against `workqueue_start.py:25-33`. The only refusals there are "no such request" and "not accepted", which `unfulfilled` already excludes, so no client reaches it today.
- **r102 also gives ids a later round dropped** (w171). A later round of one initiative may drop an id an earlier round drafted. Because every kept round is read, the dropped id is still given. Reproduction: by reading `supervise_drafts.py:16-19`. It costs only skipped ids. w171's task review found it too.
- **The writer's dispatch templates have no slot for the given ids** (w169). `skills/integrating-a-proposal/SKILL.md` The Template and The Question Template have none, so the round adds them freehand. Step 2's check sends back a wrong id. This is from w169's task review, confirmed by reading.
- **The prefixed form's refusal for a missing file says "work-item" even for a capability-proposal** (w168). Reproduction: `workqueue.agrees`'s message (`workqueue.py:190`) is reached from `workqueue_answer.py:37`. It is wording only.
