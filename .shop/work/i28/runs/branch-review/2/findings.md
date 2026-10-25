# Branch review of i28 (re-review after w172)

**Verdict: DONE.**

- The suite is green, and I ran every work-item's check myself; each passes.
- Branch review 1's one fix-now finding is fixed by w172. The integrate brief now writes the "Ids drafted elsewhere" label that `initiative-round` and `integrating-a-proposal` look for, and the r102 step asserts it.
- No finding is Critical and none is triaged fix now.
- What remains is Minor: lint, the module-map row and the deprecated @r102 scenario. These are observations and drops, as in review 1.

## Range and work-items

- **Range:** `4b7dca6c..3e969c93` on `i25-review-findings-to-implementation`. Head is `3e969c93` ("work: w172 done -> green").
- **w167** (supervision#r92): `12f0b295`
- **w168** (work-queue#r30): `fa6929fb`
- **w169** (spec-integration#r43, guarantees): `50788670`
- **w170** (supervision#r102, r103, r104): `bcc41527`, `55eea183`, `2e0f2555`
- **w171** (supervision#r102, the fix of w170's task-review finding): `a414d2bd`
- **w172** (the fix of branch review 1, which accepts r102, r103 and r104): `a1ff989a`
- **Commits outside any work-item's claimed..done span:**
  - the spec apply `f85f0d23`
  - the formulate commits `7e6266ca`, `79f4b429` and `7636eb12`
  - the hand-written proposals `1649e9d2`
  - the start `f3143c56` and the integrate fault `d4a85c1e`
  - the queue's own `work note`, `work add`, `work answer` and `work retry` commits
  - `cb04d752` "branch review 1 of i28"

  See finding 5.

## Suite

`Suite: 867 passed, 0 failed at 3e969c93 in 22.1 s` (1 skipped, 56 subtests passed; pytest's own figure is 21.78 s).

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions start `work` and the other commands as subprocesses (`tests/scenarios/conftest.py`).
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

w169's spec-integration is a guarantees capability, so no scenario is collected for it. I read r43's text against the instructions:

- `agents/initiative-round.md:27`
- `skills/integrating-a-proposal/SKILL.md:23`

Both now match the brief's label at `scripts/supervise_brief.py:79`.

**`tools check --base 4b7dca6c`:**

- **ruff:** 5 errors, so it fails. Review 1 found 8; w172 cleared I001 at `supervise_brief.py:3` and FURB167 at `supervision_integrate_steps.py:107` and `:112`. The 5 left (finding 4):
  - `scripts/supervise_brief.py:82` ISC004
  - `tests/scenarios/supervision_intake_steps.py:65` FURB167
  - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
  - `tests/scripts/stub_claude.py:186` FURB167
  - `tests/scripts/stub_claude.py:187` FURB167
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none, so there is nothing more to read.

**The other tools:**

- **`tools size --limit 300`:** printed nothing. No file is over the limit.
- **`features deprecated`:** four deprecated scenarios.
  - supervision @r102 is this branch's (finding 3).
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing this branch touches has a dry-run mode and a real mode of one operation. So there is no randomized test to run and no finding.

## Removed and weakened tests

None.

What I searched for:

- Removed lines under `tests/` and `features/` in `git diff 4b7dca6c HEAD`. There are only:
  - imports
  - one line of the stub's docstring
  - the stub's heading regex, widened to also capture the name
  - `re.M` becoming `re.MULTILINE` in `listed`, with the same behaviour
- Added `skip`, `xfail` and `pytest.mark` lines: none.
- Work-item commits that touch `features/`: none. Only the formulate commits do, and they only add (74 insertions, 0 deletions net).

w172's change to `integrate_given_ids` (`tests/scenarios/supervision_integrate_steps.py:176-182`) is stricter, not weaker:

- Before, it asserted that each id appears anywhere in the brief.
- Now it asserts a line starting "Ids drafted elsewhere" exists and that each id is on that line.

## Allowances

- **w171, `other_initiative`, setup: holds.** This was verified in review 1 and is unchanged since. `a414d2bd` changes only the path the draft is written to.
- **w172, `integrate_given_ids`, interim: holds.**
  - The step was first committed in `55eea183`, which is after Base (`git log -S"def integrate_given_ids"`).
  - It now asserts what w172's plan decision D2 says: the label, with the given ids on that line.
- **w167, w168, w169 and w170:** their reports give "none", and their diffs change no existing test.

## Cannot verify

No check is unverified.

- I wrote a probe to print the brief's "Ids drafted elsewhere" line for i25, i26 and i28 on this checkout's real queue. Running it was refused by the sandbox, and I deleted it.
- The behaviour it would show is covered by the green r102 scenario, which uses the real layout `drafts/round-<m>/`.
- Review 1's probe of `added_by_others` on this queue gave i25's and i26's kept ids.

## Findings

### 1. Branch review 1's finding 1: resolved by w172
- **Where:** `scripts/supervise_brief.py:79`.
- **What it now writes:** `Ids drafted elsewhere (number added lines above each on the same capability): <ids or none>`.
- **Why it is resolved:**
  - That is the label `agents/initiative-round.md:27` and `skills/integrating-a-proposal/SKILL.md:23` name.
  - Its wording is now r43's "above", not "take none".
  - With no ids it writes "none", which the instructions read as "leaves the numbering as it was".
- **Risk checked:** some other step or the stub might have read the old wording.
  - `grep -rn "drafted elsewhere"` over `agents`, `skills`, `docs`, `scripts` and `tests` finds only the two instruction files, the brief line and the step.
  - The old wording "take none of them" is gone everywhere.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` now starts, with `work start`, the initiative of an accepted request that no initiative fulfils. The row still names only "every open initiative taken side by side, one `Run` each, and the exit on their statuses".
- **Fix:** add "and the start of the initiative of an accepted request no initiative fulfils (r103)" to the row.
- **Triage:** observation, unchanged from review 1. On a re-review this is neither invalid data nor a wrong write.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-item is green
- **Where:** `features/supervision.feature:1239-1250`, with its step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:144-155`).
- **What is wrong:** w171 and w172, which deliver the replacement at `:1252`, are both green. Neither has a `## Retires`.
- **Fix:** a work-item accepting supervision#r102 whose `## Retires` lists the deprecated scenario. It removes the scenario, its binding and `other_initiative`.

### 4. Minor, w167, w170 and w172, drop: ruff errors on lines the branch added or touched
- **Where:** the 5 errors listed under Checks.
- **The w172 part:** `supervise_brief.py:82` ISC004.
  - w172 touched this line and its report says "fixed ... ISC004", but only the quoting changed.
  - The implicit concatenation inside the list is still there. w172's task review found the same.
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** parenthesize the concatenated string at `:81-83`, and run `ruff check --fix` on the other three files.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item
- **What:** the commits listed under Range.
- **Why it is not more:**
  - Each is a round of the initiative, a queue command, or branch review 1's own record. The hand bootstrap is in the ledger (observation 2026-10-25-loop-collisions).
  - None touches code or tests.

## Shape

- **Size limit:** met. `tools size` prints nothing. The largest file w172 touched, `supervision_integrate_steps.py`, is within 300.
- **"A new concern gets a new module and a row":** met for `scripts/supervise_drafts.py`, at `CLAUDE.md:32`.
- **Rows the branch touched:**
  - `scripts/supervise*.py` "briefs": met. `supervise_brief.py:71-84` writes the integrate brief's lines.
  - `scripts/workqueue_answer.py`: met (`:29-36`).
  - `scripts/supervise_change.py`: met (`:47-50`).
  - `scripts/supervise_draft.py`: met (`:51`).
  - `scripts/supervise_all.py`: not met (finding 2).
  - `tests/scenarios/` "one module a concern": met.
- **Code no scenario reaches any more:** none today. After finding 3's retirement, `other_initiative` is reached by nothing. The check is `features bindings` and a grep for "whose kept drafts add".
- **Code no line asks for:** none.
  - w172's brief wording serves r102 (give the ids) and r43 (number above them).
  - The rest is as review 1 found it.
- **Behaviour against the lines and the Purpose:** no contradiction found.

## Coupling

The branch adds no dependence on another project. It reads only its own layouts and brief headings.

Two couplings were there before the branch and remain:

- **pytest-bdd and pytest 10:** pytest-bdd relies on pytest internals that pytest 10 removes (`PytestRemovedIn10Warning`, from `pytest_bdd/compat.py`).
  - The suite would break on pytest 10.
  - Pinning `pytest<10` beside pytest-bdd keeps it stable.
- **The `@deprecated` tag:** pytest-bdd turns it into an unregistered mark (`PytestUnknownMarkWarning`). Registering `deprecated` under `markers` in `pytest.ini` stops the warning.

## Observations

- **The next `work run` with no initiative starts an initiative for q5** (w170, r103 as written), if q5 is still accepted and unfulfilled.
  - Reproduction (review 1): `supervise_all.unfulfilled(root)` returned `['q5']`.
- **A start of several requests is not atomic** (w170). If `work start` refuses one request after an earlier start has committed, the earlier initiative stays started. Today `unfulfilled` already excludes the requests `work start` refuses, so no client reaches this.
  - Reproduction: by reading `supervise_all.py:31-35` against `workqueue_start.py:25-33`.
- **r102 also gives ids a later round of the same initiative dropped** (w171). The cost is only skipped ids.
  - Reproduction: by reading `supervise_drafts.py:16-19`.
- **`integrating-a-proposal`'s dispatch templates have no slot for the given ids** (w169). The round passes them freehand, and step 2's check sends back a wrong id.
  - Reproduction: by reading the skill's Template and Question Template.
- **The refusal for a missing file names "work-item" even for a capability-proposal** (w168). This is wording only.
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py:37`.
