# Branch review of i29 (work run closes what it delivers)

**Verdict: DONE.** No Critical finding and nothing triaged fix now. Every check the work-items name was run here and passes. There is one Important finding, triaged observation: a hand commit wrote an r15 scenario outside any formulate round. There are four Minor observations.

## Range and work-items

- Range: `4640ef08..8ae0e927` on `i25-review-findings-to-implementation`, 275 commits. The branch is shared with i25, i26, i27, i28, i30 and i31, so most of the range is their work-items, rounds and reviews. I review i29's part and name anything of the others' that I came across.
- i29's work-items, all `green`. Each commit is listed as it is on HEAD; I read each commit's whole diff.
  - **w175** (requests#r22): `959cba20` *work request refuses an empty delegation*. It is the implementer's 72bd6f14, re-applied by the merge.
  - **w179** (supervision#r15): `0c654848` *keep_named: a result value the file system refuses as a name names no file*. It is the implementer's f0695846.
  - **w181** (supervision#r105–r109): `4d3113e1` (r107), `5048b72e` (r108), `c482f4f8` (r106), `07d5c24c` (r105, r109) and `d87a295b` (the r92 scenario's setup).
- i29 commits that belong to no work-item:
  - the rounds' merges (`round/i29-1-integrate`, `round/requests-3-apply`, `round/requests-4-formulate`, `round/supervision-*`), with their spec and features commits `7c548d23`, `6cd77b2b`, `3bfdba68` and `d073c518`;
  - `work add`, `work answer` and `work note` commits;
  - `7fed86a0`, a hand commit to `features/` (Finding 2).

## Suite

`Suite: 882 passed, 13 failed at 8ae0e927 in 40.6 s`

- Command: `python3 -m pytest -q -n auto -rfEx -p no:cacheprovider`. It runs in parallel (pytest-xdist, `-n auto`, about 10 CPUs busy).
- It does not run in-process. The step definitions run `scripts/work` as a subprocess (`tests/scenarios/test_supervision.py`, `run_work`). The suite is under 60 s, so that is no finding.
- All 13 failures are undefined steps or assertions in scenarios that w184 and w185 accept. Those are i30's and i31's work-items, `claimed` and `drafted`, not i29's.
- With the work_items plugin, `-p work_items --work-item w181 --whole-suite` gives 863 passed, 0 failed, 13 xfailed, 19 xpassed in 32 s. Each of the 13 is xfailed as "accepted by w184/w185, neither green nor withdrawn".

## Checks

| Check | Result |
|---|---|
| w175: `pytest -n auto -p work_items --work-item w175 --whole-suite` | 863 passed, 13 xfailed, 19 xpassed, 0 failed |
| w175: `pytest -p work_items --work-item w175` | 143 passed, 1 skipped |
| w179: `--work-item w179 --whole-suite` | 863 passed, 13 xfailed, 19 xpassed, 0 failed |
| w179: `--work-item w179` | 144 passed, 1 skipped |
| w181: `--work-item w181 --whole-suite` | 863 passed, 13 xfailed, 19 xpassed, 0 failed |
| w181: `--work-item w181` | 148 passed, 1 skipped |
| `tools check --base 4640ef08`, ruff | 28 errors. 23 are in tracked probe scripts under `.shop/work/i29/runs/supervision/` and under i30's and i31's run directories (Finding 3). One is on a line w181 changed, `scripts/supervise_analysis.py:4` I001 (Finding 1). Four are on lines i29 did not write: `supervise_brief.py:89` ISC004 (a4e922a6), `supervision_intake_steps.py:84` FURB167 (bcc41527), `supervision_proposal_steps.py:96` RUF100 (2e0f2555), `test_supervision.py:14` I001 (the import block; w181 added one line in sorted position). |
| `tools check`, vulture | clean |
| `tools check`, import-linter | "the project states no import contracts": nothing to check |
| `tools size --limit 300` | prints nothing; no tracked Python file is over 300 lines |
| `features deprecated` | 6 deprecated scenarios, none of them i29's (see Feature files) |
| `features bindings` | "every binding names a scenario" |
| dry-run against real mode | i29 adds no operation with a dry-run mode. `git push --dry-run` in `supervise_review.py` and `supervise_faults.py` is a probe, not a mode of the system. No randomized test is due. |

## Removed and weakened tests

None. I searched every i29 work-item commit's test diff for:

- removed lines (`^-`) and deleted `def`s;
- changed or removed `assert`s;
- parametrize edits and added `skip`/`xfail`;
- renamed steps.

Two test lines are removed. Neither weakens a test:

- `tests/scenarios/supervision_integrate_steps.py:43` (`d87a295b`): the signature of `integrate_with_changes` gains the `repo` fixture. The step's pattern and the assertions its scenario reaches are unchanged.
- `tests/scenarios/supervision_analysis_steps.py:5` (`c482f4f8`): the import line gains `git`.

## Allowances

- w175, both implement reports: none.
- w179, implement report: none.
- w181, 3-implement report: none.
- w181, 4-implement report, `supervision_integrate_steps.py` `integrate_with_changes`, **setup**: **holds**.
  - `d87a295b` adds only a write and commit of `spec/capabilities/other.md`, plus the `repo` parameter.
  - It changes no `assert`, no expected value and no parametrize case. `proposals_written` (:146) asserts the same two proposals.
  - The r92 scenario still proves r92. Since r107, the capability `other` has to exist for that scenario to mean what it did.

## Cannot verify

- The 3-implement report of w181 says r105 and r109 were not run red after their steps were written. The commits cannot show whether they were. They are green now and their steps were undefined before w181.
- Every check is verified.

## Findings

1. **Minor, w181, observation**: `scripts/supervise_analysis.py:10`. w181 added `git` to the import line, which made it 123 characters. Ruff now reports the import block as unformatted.
   - Why it matters: lint is no longer clean on a file w181 touched.
   - Fix: wrap the import, or shorten its trailing comment.
   - Reproduction: `python3 <Scripts>/tools check --base 4640ef08` printed `scripts/supervise_analysis.py:4:1: I001 [*] Import block is un-sorted or un-formatted`.
2. **Important, no work-item (hand commit `7fed86a0` on the initiative branch), observation**: `features/supervision.feature:368-376`. The r15 scenario "a field of a worker's result giving a sentence longer than a file name may be is taken as no file" was added straight to `features/`, by a hand commit on the initiative branch (first parent, directly after `work retry: w176`). It came from no formulate round and is in no capability-proposal: `i29-supervision` adds r105–r108 and does not name r15.
   - What it says is within r15's text: "each file the worker's result names". A sentence names no file.
   - Why it matters: the scenario bypassed formulating-features and its gate. Scenarios are meant to reach `features/` only through a round.
   - Fix: none to the code. Give later scenarios of an existing line their own formulate round, through a capability-proposal that names the line under `changes`. If the person wants it on record, this one can be ratified that way.
   - Reproduction: `git show --stat 7fed86a0` shows `features/supervision.feature | 10 ++++++++++`, author `probe`, with no round branch merged. `git log --first-parent -3 7fed86a0` shows it on the first parent.
3. **Minor, no work-item (i29's round stage directories), observation**: three tracked Python files are kept round scratch scripts: `.shop/work/i29/runs/supervision/1-gate/mk.py`, `.shop/work/i29/runs/supervision/5-apply/splice.py` and `.shop/work/i29/runs/supervision/6-formulate/splice.py`. i30 and i31 have the same kind of files.
   - Why it matters: they make 23 of the 28 ruff errors of `tools check`, which buries the real ones. They are also tracked Python files under the size rule.
   - Fix: exclude `.shop/` from ruff in the project's configuration, or keep only the files a round's result names.
   - Reproduction: `git ls-files -- '.shop/work/i29/*.py'` lists the three files. `tools check --base 4640ef08` gives their I001, SIM115 and F401.
4. **Minor, w181, observation**: `scripts/supervise_rounds.py:115-119`, r107's mixed case. Some capabilities in the change list are known and some unknown. `work run` commits the known ones' proposals and then exits with an error. No scenario reaches this path; the r107 scenario names only `nowhere`.
   - I probed `Changes.unknown` with spec holding `thing` and round-2 drafts holding `newcap`. It returned `['nowhere', '../thing', 'thing.md']` for the names `thing, newcap, nowhere, ../thing, thing.md`, so the drafts exemption and the path-shaped names come out right.
   - `kept_path` picks `drafts/round-10/` over `round-9`. With no drafts it falls back to the stage directory.
   - The brief's regex reads back both the round path and the old stage-directory sentence.
   - Keep as a test: an r107 scenario whose change list names `thing` (held) and `nowhere`. It would check that `thing.md` is written and committed, that no `nowhere.md` exists, and that the run exits with an error naming `nowhere`.
5. **Minor, w181, observation**: `scripts/supervise_analysis.py:65-78` and `scripts/supervise_done.py:17-25`. The analysis session can be cut short or write no record. The measurement `measure initiative` wrote is then left uncommitted under `.shop/records/measurements/`, and `set_done` does not hold.
   - On a rerun the same day, `measure initiative` refuses (`measure_write.py:24`, "exists; --replace writes over it"). There is then no analysis and still no done until another day's measurement.
   - No line names this case; plan §5 left it open.
   - Reproduction by reading: `analyse` commits only inside the `analysis.md` branch (:68-76), and `records_committed` needs both files tracked.
   - What would close it: a line saying whether a lone measurement is committed, or whether a rerun replaces it.

## Feature files

- i29 adds these scenarios:
  - through rounds: supervision r105–r109 (`d073c518`, round `supervision-6-formulate`) and requests r22 (`6cd77b2b`, round `requests-4-formulate`);
  - by hand: r15 (`7fed86a0`, Finding 2).
- i29 removes no scenario, and no i29 work-item commit touches `features/`.
- Deprecated scenarios, none of them i29's:
  - supervision r102 (i28): its replacement's work-items w170, w171 and w172 are `green`, yet the deprecated scenario is still there. That is for i28's review.
  - work-queue r9: replacement accepted by w140 (i24), `green`. Still there.
  - work-queue r1 (w89, w90 not green), migration-tools r15 (w86 not green), supervision r19 (w184 `claimed`), supervision r83 (w185 `drafted`): their replacements' work-items are not green.
- Every binding names a scenario.

## Shape

Size limit (CLAUDE.md "Size limit"): **met**. `tools size --limit 300` prints nothing.

Module map, each row the branch touched:

| Row | Result |
|---|---|
| `scripts/supervise_done.py` | met. New concern, new module, new row (CLAUDE.md:34, `07d5c24c`). |
| `scripts/supervise_analysis.py` | met. The commit of measurement and record (:71-76) is part of the measure-and-analysis concern. |
| `scripts/supervise_change.py` | met. `unknown` (:38) and `kept_path` (:45) belong to the change list and the proposals written from it. |
| `scripts/supervise*.py` | met. `supervise_brief.py:47-51` (Drafts path), `supervise_rounds.py:103-119`, `supervise.py:215`, `supervise_worker.py:233-238`. |
| `scripts/workqueue_done.py` | met. `holds` (:41) is the same condition, made public. |
| `scripts/workqueue_request.py` | met (:93). |
| `tests/scenarios/` | met. `supervision_done_steps.py` is a `<capability>_*_steps.py` module of its own concern. |

- Unreached code: vulture is clean. Two branches serve lines but no scenario reaches them: the r107 mixed case (Finding 4) and the fallback in `kept_path` for a round with no drafts.
- Refactor, as an observation: the drafts path goes from `supervise_change.write_proposals` to `supervise_brief.brief` as a prose sentence in the proposal's body, read back with a regex (`supervise_brief.py:48`).
  - A shared constant for the sentence, or a function in `supervise_change` that both modules call, would remove that coupling.
  - Check that it is complete: `git grep "The drafts of this proposal are in"` finds the literal in one module only.

## Coupling

- i29's code relies only on what its dependencies publish:
  - git plumbing and porcelain output: `ls-files`, `status --porcelain`, `add`, `commit -- <paths>`;
  - pathlib raising `OSError`/`ValueError` on names the file system refuses (w179);
  - the `measure initiative` contract: its last stdout line is the measurement's path, and it refuses when the measurement exists. `measure` is this repository's own script.
- Nothing would break on a change behind those contracts.
- The one internal coupling is the prose sentence of Shape.

## Observations

- `supervise_analysis.py:4` I001: `tools check --base 4640ef08` → `scripts/supervise_analysis.py:4:1: I001`.
- Hand-written r15 scenario: `git show --stat 7fed86a0` → `features/supervision.feature | 10 +`, on the first parent, no round.
- Tracked round probe scripts: `git ls-files -- '.shop/work/i29/*.py'` → 3 files; 23 ruff errors in `tools check`.
- r107 mixed case not pinned: a probe of `Changes.unknown` returned `['nowhere', '../thing', 'thing.md']`; no scenario covers the case.
- Measurement left uncommitted when the analysis writes no record: read in `supervise_analysis.py:65-78` and `measure_write.py:24`.
- Deprecated supervision r102 with green replacements (i28) and work-queue r9 (i24): `features deprecated` lists them; w170, w171, w172 and w140 are `status: green`.
