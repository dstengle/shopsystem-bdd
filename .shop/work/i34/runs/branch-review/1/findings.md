# Branch review of i34

**Verdict: DONE.** There is no Critical finding, none is triaged fix now, and every check was run and verified. There are three Minor findings: two observations and one drop.

## Range and work-items

- **Range:** `c7f6d2f7..86a8c33f` on `i25-review-findings-to-implementation`: 46 commits.
- **i34's one work-item:** w195 (`supervision#r122`), green. Its commits lie between `23d63b30 work: w195 ready -> claimed` and `e1065200 work: w195 claimed -> done`. Leaving out `work run`'s `work:` commits, that is one commit:
  - `f682b013`: `scripts/work_items.py` +21/-2, `tests/scenarios/supervision_proposal_steps.py` +15, `tests/scenarios/supervision_tests_steps.py` +11/-1. All three are in the fileset.
- **i34's commits outside w195** are `work run`'s own rounds:
  - `c7f6d2f7`, `c3b67a4a`, `96aab65d`, the integrate merge `c3ece9ea`
  - the gate, answer and apply rounds: `7b86595b`, `d87214ea`, the spec commit `eb30678a`, `87b3ad82`
  - the formulate round: `e8f5572a`, merged by `58dc0e3f`, then `df1a5abd`
  - `work note` and `work add`: `fa0b2569`, `34485aeb`, `5e4bd378`, `282551ce`, `a1c76864`
- **Other initiatives' commits on the shared branch:**
  - i33's w192 and w194: `620ec316`, `64c62951`, `77954d18`, `bbbee221`, `7b81607b`, `272bd226`, `cc081259`, `32823806`, `919e4510`, `6ef3162b`, `78ecb78d`, `94827704`, and its branch review `608ad208`
  - i31's w193, review, measure and done: `8114d5f6`, `6b06211b`, `d787c410`, `5f36222c`, `2d5bb19a`, `7088d12b`, `c3ae56d8`
  - i32's w192 green and its branch reviews 7 and 8: `1a41ab8a`, `0b6aba9f`, `6a19ad00`

  Each of these belongs to a work-item or round of its own initiative, and each initiative's own branch review covers it (i33: `608ad208`). They are not graded here. No commit in the range belongs to no work-item and no round.

## Suite

Suite: 922 passed, 0 failed at 86a8c33f in 23.12 s. The run also had 1 skipped and 56 subtests passed.

- It runs in parallel: `pytest.ini` addopts `-n auto`.
- The step definitions drive the entry points by subprocess, not in-process. For example, `tests/scenarios/test_supervision.py:72` runs `scripts/work`. Some other steps run in-process, such as `batch_measurement_world.py:128` calling `script.main`.
- At 23 s the suite is under 60 s, so this is no finding.

## Checks

- **w195, `python3 -m pytest -q --work-item w195`** (the plugin through the conftest): 154 passed, 1 skipped, 56 subtests, in 10.85 s. The 10 rows of the r122 outline are among them.
- **w195, whole-suite check, `python3 -m pytest -q -rfEx --work-item w195 --whole-suite`:** 922 passed, 1 skipped, **0 xfailed**, in 26.09 s. So no open capability-proposal in this repository masks a scenario today.
- **`tools check --base c7f6d2f7`:**
  - ruff: 3 hits, all already present at Base on lines the branch did not change.
    - `scripts/supervise_analysis.py:4` I001: lines 1-12 are the same at Base and HEAD.
    - `scripts/workqueue.py:248` I001: the same function-local import is at Base.
    - `tests/scenarios/supervision_proposal_steps.py:118` RUF100: present at `23d63b30`, as w195's review verified.
  - vulture: clean.
  - import-linter: "the project states no import contracts". Nothing is `missing`.
- **`tools size --limit 300`:** no output, so no file is over the limit. w195's files are 150, 168 and 218 lines.
- **`features deprecated`:** 7 deprecated scenarios:
  - migration-tools r15
  - supervision r75, r102 and r105
  - work-queue r1, r23 and r9

  None is i34's. w195 has no Retires.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run and real mode:** none applies. The system's only `--dry-run` is `git push --dry-run`, which verifies a push (`supervise_review.py:41`, `supervise_faults.py:67`). It is not a dry-run mode of the system's own operation, so there is no agreement test to run.

## Removed and weakened tests

None in i34's commits. I searched `git show f682b013` for:
- deleted `def` lines of tests or steps
- removed `assert` lines
- dropped parametrize or Examples rows
- added skip or xfail marks
- changes to expected values

The one changed test is `counted_as` (`supervision_tests_steps.py:134`). Its body moved verbatim into `check_counted(repo, context, stage, counted)`, which it calls with `"merge"`. The filter, the `len(records) == 1` assertion and the comparison are all unchanged. w195's plan lists no "Tests the decisions break", and none is needed.

The one `features/` change attributable to i34 is the r122 outline, added by the formulate round (`e8f5572a`), not by a work-item.

## Allowances

w195's report gives `## Tests changed under an allowance`: none. The commit agrees: no existing test's asserts, expected values or cases changed.

## Cannot verify

Nothing. Every check was run here.

## Findings

### F1 Minor, w195: observation
**Where:** `scripts/work_items.py:109`, with the docstring at `:97-98`.

**What is wrong:** when a capability-proposal causes the xfail, its reason still reads "expected: accepted by p1, neither green nor withdrawn". A proposal neither accepts nor turns green. The `expect_red` docstring also still names work-items only, though plan §2 asked for it to name proposals.

**Why it matters:** the text shows in `-rx` output and in the suite record a person reads. No count is wrong.

**Fix:** give proposals their own reason, for example "added or changed by p1, neither formulated nor withdrawn", and extend the docstring.

**Reproduction:** the r122 rows pass. Reading `work_items.py:105-110`, `open_` mixes work-item and proposal names under one reason string.

### F2 Minor, w195: observation
**Where:** `scripts/work_items.py:79-80`.

**What is wrong:** a proposal that is `merged`, or has no `status:` line, counts as open for good. This follows r122's text and its accepted row (`merged` gives expected).

**Why it matters:** this repository holds 44 capability-proposals still `merged` (decision 0065 says they become `formulated`). A risk I named: one of them might mask a failing scenario of a capability that has a feature file. What I verified:
- A grep of `^(adds|changes): \[.*(<each features/ stem>)#r` over `.shop/work/*/*.md` gives 95 files, none of them among the 44 `merged` files.
- `--whole-suite --work-item w195` showed 0 xfailed.

So nothing is masked today. A consumer repository with a leftover `merged` proposal on a capability that has scenarios would have that capability's failures xfailed for good.

**Fix, if wanted:** a request to narrow r122 to the statuses `work run` writes, or an upgrade step that moves the leftover `merged` proposals to `formulated` as 0065 says.

### F3 Minor, w195: drop
**Where:** `tests/scenarios/supervision_proposal_steps.py:126-139`.

**What is wrong:** the `approved` rows of the r122 outline do not observe `approved` at the suite runs. The step makes the formulate round ask a question, so p1 stands `awaiting-answer` when the suites run. The step's docstring and the report both say so.

**Why it matters:** the rule is a blacklist, so the outcome is the same. But a later allowlist that dropped `approved` would not turn these rows red.

**Fix:** there is no cheap one within `work run`'s lifecycle.

## Shape

CLAUDE.md rows the branch touched for i34:
- **`scripts/work_items.py`, "the pytest plugin of `--work-item`": met.** `proposals()` at `:71` sits beside `acceptors()` at `:59` and serves the same marker.
- **`tests/scenarios/`, "one `<capability>_*_steps.py` module a concern": met.**
  - The proposal Given is in `supervision_proposal_steps.py:126`.
  - The suite-record Then is in `supervision_tests_steps.py:139`, beside `counted_as`.
- **Size limit 300: met.** The files are 150, 168 and 218 lines.

Code no line asks for: none.
- `proposals()` and the added xfail source serve r122.
- The new Given and Then serve the accepted outline at `features/supervision.feature:812`.
- The xfail reason's words are mechanism (F1).

Code and step definitions no scenario reaches any more: none from w195. `counted_as` and `check_counted` are both reached, by the r43 outline and the r122 outline.

## Coupling

- **pytest-bdd:** `scenario_of` (`work_items.py`, already at Base) reads the private attribute `__scenario__` of pytest-bdd's test functions. The suite also warns that pytest-bdd's `compat.py:28` uses fixture APIs pytest marks "RemovedIn10". A pytest-bdd or pytest 10 release could break the `--work-item` selection and the r43/r122 xfails behind their public contract.
  - **Stable:** pin pytest-bdd's major version, or derive the scenario from the item's markers and the feature tags pytest-bdd adds as public marks.
- **w195 adds no new reliance on another project.**

## Observations

- **F1 reproduction:** read `scripts/work_items.py:105-110`. The reason string is shared by work-items and proposals.
- **F2 reproduction:**
  - Grep `^status: merged` over `.shop/work/*/*.md`: 44 files.
  - Grep for adds or changes that name a capability with a feature file: 95 files, disjoint from the 44.
  - `python3 -m pytest -q -rfEx --work-item w195 --whole-suite`: 922 passed, 0 xfailed.
- **Pre-existing lint (not the branch's):**
  - `ruff` I001 at `scripts/supervise_analysis.py:4` and at `scripts/workqueue.py:248`
  - RUF100 at `tests/scenarios/supervision_proposal_steps.py:118`

  All three come from `tools check --base c7f6d2f7`, compared with `git show c7f6d2f7:<path>`.
