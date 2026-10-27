# Branch review of i39 (Requests go through one shared tool)

**Verdict: DONE_WITH_CONCERNS.** w202, i39's only work-item, is sound. Its check passes, it changes nothing under `features/`, and it removes or weakens no test.

There is one finding triaged fix now: data lost. The integrate round that re-drafted i39's work-queue proposal (`2862e7bf`) overwrote the `adds` and `removes` of i39's **requests** proposal. Those lists named lines that were already applied to `spec/` and formulated:
- adds: r25, r28-r34, r39-r45
- removes: r1, r3

The code that did this is i41's w204 (`d076baa8`, `scripts/supervise_change.py:91-99`). Because of it:
- 14 requests scenarios now fail under `--whole-suite` instead of being expected red;
- those lines would never get a work-item.

One check could not be verified (a real round reading the upstream's spec outside its worktree).

## Range and work-items

- Range: `b4c4ad5e..d3079697` on `main`, 135 commits.
- i39 has one work-item, **w202** (spec-integration#r44, `green`). Its commits, between `work: w202 ready -> claimed` and `work: w202 claimed -> done` (twice, after an answer), less `work run`'s `work:` commits:
  - `6e3c4f04` spec-integration r44: the integrate round is told its upstreams and gives the lines of a request into them
  - `fe844bb3` the writer's question template no longer asks for request lines in the upstream's terms; lint in the new tests
- i39's spec rounds' own commits (attributed by the ledger, not by any work-item):
  - applies: `af0977ce`, `e3d62661`, `da5772d6`, `6cd0d09c`
  - formulates: `e27313e1`, `bc58e42e`, `8c95a5fd`, `b80813ca`
- The range also holds i40 and i41, both started and finished on `main` after i39's base. Each has its own branch review (`c25d6dd6`, `a742afe9`):
  - i40: w203, `1c351ddc`; rounds `0c09944f`, `3df7df2e`
  - i41: w204, `d076baa8` and `d6667395`; rounds `580ad083`, `1cf1be38`

  I read their changes only where they touch i39's files, or where they touch i39's data or suite (finding 1).

## Suite

`Suite: 955 passed, 16 failed at d3079697 in 28.66 s` (plain `python3 -m pytest -q -p no:cacheprovider`, wall time 28.98 s).

- **Parallel:** yes, `-n auto` (pytest-xdist) from `pytest.ini`.
- **In-process:** no. The step definitions drive `scripts/work` as a subprocess. The suite runs under 60 s, so this is not a finding.
- **All 16 failures are `StepDefinitionNotFoundError`** on scenarios that are formulated but have no work-item yet:
  - design-model-check @r120
  - supervision @r135
  - 14 requests scenarios: @r28 ×3, @r44 ×3, @r29, @r30, @r31, @r32 ×2, @r40, @r42, @r45
- **With `--work-item w202 --whole-suite`** (the run that marks expected red): `14 failed, 955 passed, 1 skipped, 2 xfailed in 29.24 s`.
  - r120 and r135 are xfailed: their proposals are open and list them.
  - The 14 requests scenarios still fail. Their proposal no longer lists them (finding 1).

## Checks

- **w202's check:** `python3 -m pytest -q -p no:cacheprovider --work-item w202` gave `145 passed, 1 skipped, 56 subtests passed in 6.83s`. The r44 scenario passes.
- **`tools check --base b4c4ad5e`** (exit 1):
  - **ruff:** 16 errors, none in w202's files.
    - i39's committed round scripts:
      - `.shop/work/i39/runs/requests/3-formulate/splice.py`: I001, SIM115 ×3
      - `.shop/work/i39/runs/work-queue/6-gate/gen.py`: I001, SIM115
    - i41's committed round scripts: `.shop/work/i41/runs/supervision/{2-apply,3-formulate}/splice.py`, SIM115 ×6
    - w204 (i41) code:
      - `scripts/supervise_change.py:96` B023
      - `tests/scenarios/supervision_reintegrate_steps.py:13` F401
      - `tests/scenarios/supervision_reintegrate_steps.py:137` FURB167
      - `tests/scenarios/test_supervision.py:14` I001
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". It is not `missing`, so there is nothing I had to read for myself.
- **`tools size --limit 300`:** no output, so no tracked Python file is over 300 lines.
- **`features deprecated`:** 9 deprecated scenarios:
  - design-model-check r115 (for r120) and r117 (for removal)
  - requests r1 (for r44) and r3 (for r45)
  - 5 supervision scenarios for removal

  No replacement has a `green` work-item, so none is due for retirement.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The system has no dry-run mode of an operation. The only `--dry-run` uses (`supervise_faults.py:71`, `supervise_review.py:41`) are `git push --dry-run` reachability probes, and the branch did not touch them.

## Removed and weakened tests

None in w202. I searched `git diff b4c4ad5e HEAD -- tests/` for:
- removed lines;
- `skip`, `xfail` and `parametrize` changes;
- deleted test functions and changed `assert`s.

Across the whole range, the only removed lines are two step patterns in w204 (i41):
- `supervision_formulate_steps.py:36`
- `supervision_rounds_steps.py:21`

Both were widened with an optional group, so the old step texts still match and no assertion changed.

w204 also removed three scenarios from `features/supervision.feature`: r80, r114 and r71. All three were deprecated, and w204 lists them under `## Retires`.

The later commits of i40 and i41 to w202's `spec_integration_steps.py` only add steps (r45). The r44 steps are unchanged.

## Allowances

- w202 `3-implement/report.md`: "none". The commit agrees: there were no edits to existing tests.
- w202 `5-implement/report.md`: "none". The commit agrees: it only removed imports from the tests w202 itself wrote in `6e3c4f04`.

## Cannot verify

- **Whether a real integrate round may read the upstream's published spec.** w202 hands the round an absolute path outside its worktree.
  - `supervise_worker.py:224` starts `claude -p --permission-mode acceptEdits --allowedTools ...`, with `Read` granted and no `--add-dir`.
  - Whether Claude Code lets that session read outside its working directory can only be seen in a real session. I do not start one.
  - The scenario's stand-in session reads nothing.
- **Edge cases of `Briefs.upstreams`, judged by reading only.** Running my probe of `supervise_brief.py:94-101` was refused approval in this session. The probe is kept below under Observations.

## Findings

### 1. Important, fix now (data lost): an integrate round for one proposal overwrote another proposal's applied lists (w204, i41; i39's data)

**Where:** `scripts/supervise_change.py:91-99` (`write_proposals` with `proposal_for`), added by `d076baa8`.

**What is wrong:**
- `write_proposals` replaces the lists and the drafts path of every proposal the initiative holds for any capability the change list names, through `rewrite_lists(held.stem, [one])`.
- Supervision r142 and r148 ask for that only for the proposal that is being drafted anew from its answers.
- In i39, work-queue's integrate round 5 (`2862e7bf`) gave a change list naming both work-queue and requests. So `.shop/work/i39/requests.md` went:
  - adds: from `[requests#r25, requests#r28 … r34, r39 … r45]` to `[requests#r46, requests#r47]`
  - removes: from `[requests#r1, requests#r3]` to `[requests#r13, requests#r14]`
  - its drafts pointer moved to work-queue's round. Its old `## Questions` were left in place.
- The old lists were the lines the apply round `e3d62661` had already committed to `spec/`, and the formulate round `bc58e42e` had already formulated.

**Why it matters:**
- `supervise_draft.py:87` drafts a formulated proposal's work-items from its `adds` and `changes`. So r25, r28-r34 and r39-r45, which are live in `spec/capabilities/requests.md` and have scenarios, would never get a work-item.
- `work_items.py:72-86` takes a proposal's `adds` as expected red. So the 14 requests scenarios now fail every work-item's `--whole-suite` run, in i39 and in any initiative after it.
- The record of what was applied is lost. It survives only in git (`64890ad5:.shop/work/i39/requests.md`).

**Fix:**
1. In `write_proposals`, merge (union) the round's ids into a held proposal that is not the one being drafted anew, keeping its earlier drafts path beside the new one. Rewrite in place only the proposal the round was started for, as r142 and r148 say.
2. Restore `.shop/work/i39/requests.md` to:
   - adds: `[requests#r25, requests#r28 … r34, requests#r39 … r45, requests#r46, requests#r47]`
   - removes: `[requests#r1, requests#r3, requests#r13, requests#r14]`
3. Add a scenario: a re-integrate round for p1 whose change list also names a capability with an applied proposal p2 leaves p2's applied ids in its lists.

**Reproduction:**
- `git show 2862e7bf -- .shop/work/i39/requests.md`
- `cat .shop/work/i39/runs/work-queue/5-integrate/result.json`: its `changes` has a `requests` entry.
- `python3 -m pytest -q --work-item w202 --whole-suite`: 14 requests scenarios fail rather than xfail.

### 2. Minor, observation: lint errors in w204's code (w204, i41)

**Where:**
- `scripts/supervise_change.py:96`: B023, the lambda reads the loop's `said`. It is harmless here, because `re.sub` calls it at once.
- `tests/scenarios/supervision_reintegrate_steps.py:13`: F401, `git` is imported and unused.
- `tests/scenarios/supervision_reintegrate_steps.py:137`: FURB167, `re.M` alias.
- `tests/scenarios/test_supervision.py:14`: I001, the new import is out of order.

**Why it matters:** `tools check` exits 1 on the branch.

**Fix:**
- Bind `said` with `lambda _, said=said: said`, or pass a plain string escaped for `re.sub`.
- Drop the unused import, use `re.MULTILINE`, and sort the import block.

**Reproduction:** `python3 <Scripts>/tools check --base b4c4ad5e` lists them under `== ruff ==`.

### 3. Minor, observation: committed round scripts under `.shop/work/` fail lint (i39's and i41's rounds; no work-item)

**Where:**
- `.shop/work/i39/runs/requests/3-formulate/splice.py`
- `.shop/work/i39/runs/work-queue/6-gate/gen.py`
- `.shop/work/i41/runs/supervision/{2-apply,3-formulate}/splice.py`

**What is wrong:** the rounds' helper scripts were kept with their stage directories and committed by `work run`. They are tracked Python, so `tools check` and `tools size` judge them.

**Fix:** either exclude `.shop/work/**/runs/` in `ruff.toml`, or have rounds write their helpers under `.shop/scratch/`. Either way, a check that shows it complete: `tools check` prints no `.shop/` row.

### 4. Minor, observation: commits that belong to no work-item and no round

**What:** these commits were made by hand:
- `eb7316ae`: records, observation 2026-10-27-published-contracts (i39)
- `ce86effc`: records, observation 2026-10-27-silent-exit-on-questions (i40)
- `f6569633`: records, observation 2026-10-27-done-with-proposal-open (i41)
- `3934c55a`: i40-supervision withdrawn by hand, "no work command withdraws a proposal"

**Why it matters:** the records commits are the person's notes and touch no code. The by-hand withdrawal is a status change with no `work` command behind it, which the person already raised as q19.

**Fix:** none needed now.

## Shape

- **Module map, `scripts/supervise*.py` ("work run: briefs, …"):** met. `scripts/supervise_brief.py:14-18` (`REQUEST_LINES`, `UPSTREAM`), `:62-66` and `:94-101` (`upstreams`) are the brief's concern and sit in the briefs module.
- **Module map, `tests/scenarios/` ("one `<capability>_*_steps.py` module a concern"):**
  - Partly met. `tests/scenarios/spec_integration_steps.py` has no concern segment.
  - Since `1c351ddc` (w203, i40) it holds two concerns: upstreams (r44, l.27-57) and answers beyond the request (r45, l.60-95).
  - Observation: split it into `spec_integration_upstream_steps.py` and `spec_integration_answers_steps.py`.
  - A check that shows it complete: `ls tests/scenarios/spec_integration*_steps.py` lists two modules, and `--work-item w202` still passes.
- **Size limit, 300:** met. `tools size` prints nothing, and `supervise_brief.py` and `spec_integration_steps.py` are under it.
- **Duplicated launcher:**
  - `spec_integration_steps.py:98-111` (`run_integrate`) copies `run_work`'s environment set-up from `test_supervision.py:63-76`. The first w202 review dropped this finding, because the fix was out of the fileset.
  - Observation: move one launcher into `supervision_world.py`.
  - A check that shows it complete: `grep -n STUB_CLAUDE_PLAN tests/scenarios/*.py` finds it set in one place.
- **Reachability:** every step of w202 is reached by the r44 scenario. Vulture is clean. w204's widened step patterns still serve their remaining scenarios.
- **Code no line asks for (w202):** none.
  - The `Upstream:` lines, the Read-list entries and `REQUEST_LINES` serve r44.
  - The `## Upstreams` section in `docs/capability-format.md` is the format the Implementation section points to (`docs/capability-format.md`).
  - With no `## Upstreams` section, the brief is unchanged.
- **Behaviour against the lines:**
  - Nothing contradicts spec-integration's Purpose, r44 or requests#r28. w202 only reads a configured path and checks nothing out.
  - The person's answer to w202 (lines in the downstream's own terms, corrected by the upstream) contradicts r44's "in the upstream's terms". It is raised as q17 to replace r44. Until then, r44 stands, and the brief asks for it.

## Coupling

- **Claude Code's CLI (`claude -p`, `--allowedTools`, `--permission-mode acceptEdits`):**
  - w202 relies on a round session being able to read a path outside the worktree it is started in. Nothing Claude Code publishes promises that for `-p` with a bare `Read` and no `--add-dir`.
  - If the default changes, the round silently fails to read the glossary and words the lines in this context's terms.
  - To make it stable: pass the upstream spec's directory with `--add-dir` when the brief names upstreams, or copy the published spec into the round's stage directory.
- **The upstream's on-disk layout:**
  - `Briefs.upstreams` reads the upstream's `spec/` at a path relative to this repository's root. That is someone's working tree, not a published, pinned spec (design-model §3 says "at a pinned version").
  - It breaks if the checkout moves, and it reads uncommitted state.
  - To make it stable: name a revision or published artefact in the `## Upstreams` bullet, and read it with `git show <rev>:spec/...`.
- **pytest-bdd:**
  - `work_items.py:89-94` reads pytest-bdd's private `item.function.__scenario__`. The branch did not change this.
  - The suite prints 528 `PytestRemovedIn10Warning`s from pytest-bdd's own use of pytest fixture internals.
  - Both break on a pytest-bdd or pytest 10 upgrade. To make it stable: pin pytest-bdd, and have a probe test that fails when `__scenario__` disappears.

## Observations

- `Briefs.upstreams`, a bullet whose path does not exist (`- bounded-context/a/b/billing: ../nowhere/spec`): the brief lists that path to read, and nothing says it is missing.
  - Reproduction (from `supervise_brief.py:101`, which resolves the path unconditionally): run the kept probe with the repository's path.
- `Briefs.upstreams`, a bullet with an id and no path, or `id:path` with no space after the colon: silently ignored, because `UPSTREAM` needs `:\s+\S`.
  - Reproduction: the same probe.
- `Briefs.upstreams`, `spec/index.md` naming this context itself under `## Upstreams`: listed like any upstream.
  - Reproduction: the same probe.
- The requests proposal's `## Questions` still hold integrate round 1's questions, while its drafts pointer now names work-queue's round 5.
  - Reproduction: `sed -n 1,20p .shop/work/i39/requests.md`. This is part of finding 1.

Keep as a test (`tests/scripts/test_supervise_brief_upstreams.py`): a refusal or a named "missing" line for a path that is not a directory, and a bullet without a path not ignored silently, once a line asks for either. Probe used:

```python
import pathlib, sys, tempfile, types
sys.path.insert(0, str(pathlib.Path(sys.argv[1]).resolve() / "scripts"))
from supervise_brief import Briefs
CASES = {
    "named, path missing": "## Upstreams\n\n- bounded-context/a/b/billing: ../nowhere/spec\n",
    "id, no path": "## Upstreams\n\n- bounded-context/a/b/billing\n",
    "id with colon, no space": "## Upstreams\n\n- bounded-context/a/b/billing:../x/spec\n",
    "two upstreams": "## Upstreams\n\n- bounded-context/a/b/billing: ../b/spec\n- bounded-context/a/b/stock: ../s/spec\n",
    "this context itself": "---\nid: bounded-context/a/b/self\n---\n## Upstreams\n\n- bounded-context/a/b/self: spec\n",
}
for name, body in CASES.items():
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp) / "repo"; (root / "spec").mkdir(parents=True)
        (root / "spec" / "index.md").write_text(body)
        print(name, [(i, str(p), p.is_dir()) for i, p in Briefs.upstreams(types.SimpleNamespace(root=root))])
```
