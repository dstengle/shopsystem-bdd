# Branch review 2 of i29 (work run closes what it delivers)

**Verdict: DONE.** No Critical finding and nothing triaged fix now. I ran every check the work-items name, and each one passes. There is one Important finding, triaged observation: the hand-written r15 scenario, carried over from review 1. There are four Minor observations. One of them is new: i29's measurement and analysis record reached the branch through a hand commit, not through `work run` (r106).

## Range and work-items

- Range: `4640ef08..ce37512e` on `i25-review-findings-to-implementation`, 304 commits.
  - The branch is shared with i25–i28, i30 and i31, so most commits are their work-items, rounds and reviews.
  - Review 1 covered `4640ef08..8ae0e927`. The 29 commits since then are i30's (w184, w186, w187, w180), i25's note, q9, review 1's own commit and `e37050ea`, i29's records.
- i29's work-items, all `green`. No i29 work-item commit came after review 1.
  - **w175** (requests#r22): `959cba20`, between `a39bb7a0` (ready → claimed) and `c2ea4a21` (claimed → done).
  - **w179** (supervision#r15): `0c654848`, between `eca9d404` and `7c3b0a9a`.
  - **w181** (supervision#r105–r109): `4d3113e1` (r107), `5048b72e` (r108), `c482f4f8` (r106), `07d5c24c` (r105, r109) and `d87a295b` (the r92 scenario's setup), between `307f8496` and `a7102a44`.
- i29 commits that belong to no work-item:
  - the round merges and their spec and features commits (`7c548d23`, `6cd77b2b`, `3bfdba68`, `d073c518`);
  - `work add`, `work answer` and `work note` commits;
  - `7fed86a0`, a hand commit to `features/` (Finding 2);
  - `e37050ea`, a hand commit of `.shop/records/` (Finding 6, new).

## Suite

`Suite: 885 passed, 10 failed at ce37512e in 57.2 s`

- Command: `python3 -m pytest -q -n auto -rfEx -p no:cacheprovider`.
- It runs in parallel (pytest-xdist `-n auto`, 745 % CPU).
- It is not in-process: the step definitions run `scripts/work` as a subprocess. The suite is under 60 s, so that is no finding.
- All 10 failures are scenarios accepted by **w185** (i31, not green): undefined steps of the r83, r92 gate-ending and apply/formulate-round scenarios.
- With the work_items plugin (`-p work_items --work-item w181 --whole-suite`): 883 passed, 0 failed, 10 xfailed (each "accepted by w185, neither green nor withdrawn"), 2 xpassed, in 33 s.

## Checks

| Check | Result |
|---|---|
| w175: `pytest -n auto -p work_items --work-item w175 --whole-suite` | 883 passed, 10 xfailed (w185), 2 xpassed, 0 failed |
| w175: `pytest -n auto -p work_items --work-item w175` | 144 passed, 1 skipped |
| w179: `--work-item w179 --whole-suite` | 883 passed, 10 xfailed (w185), 2 xpassed, 0 failed |
| w179: `--work-item w179` | 145 passed, 1 skipped |
| w181: `--work-item w181 --whole-suite` | 883 passed, 10 xfailed (w185), 2 xpassed, 0 failed |
| w181: `--work-item w181` | 149 passed, 1 skipped |
| `tools check --base 4640ef08`, ruff | 32 errors, attributed below |
| `tools check`, vulture | clean |
| `tools check`, import-linter | "the project states no import contracts": nothing to check |
| `tools size --limit 300` | prints nothing; exit 0 |
| `features deprecated` | 5 deprecated scenarios, none of them i29's (see Feature files) |
| `features bindings` | "every binding names a scenario" |
| dry-run against real mode | i29 adds no operation with a dry-run mode. A grep for `dry.run` in the files i29 touched finds nothing, so no randomized test is due. |

Where the 32 ruff errors come from:

- **23** are in tracked round probe scripts under `.shop/work/i29/runs/supervision/` (10) and under i30's and i31's run directories (13). See Finding 3.
- **1** is on a line w181 wrote: `scripts/supervise_analysis.py:4` I001, from line 10 (`c482f4f8`). See Finding 1.
- **8** are on lines no i29 work-item wrote:
  - `supervise_brief.py:89` ISC004 (`a4e922a6`);
  - `supervision_intake_steps.py:84` FURB167 (`bcc41527`);
  - `supervision_proposal_steps.py:118` RUF100 (`2e0f2555`);
  - `test_supervision.py:14` I001 (the import block; w181 added one line in sorted position);
  - `supervision_all_steps.py:127` RUF007 and `tests/scripts/test_supervise_change.py:7` RUF100, both from `bd765f03` (w187, i30);
  - `tests/scripts/stub_claude.py:189-190` FURB167. The lines predate Base (`12f0b295`, `6e6d3143`); the file is listed because `bd765f03` touched it.

## Removed and weakened tests

None for i29. I searched each i29 work-item commit's diff under `tests/` and `features/` for:

- removed lines (`^-`) and deleted `def`s;
- changed or removed `assert`s;
- `parametrize`, `skip` and `xfail`;
- renamed steps.

Two lines are removed, and neither weakens a test:

- `supervision_integrate_steps.py` `integrate_with_changes` (`d87a295b`): the signature gains `repo`.
- `supervision_analysis_steps.py:5` (`c482f4f8`): the import gains `git`.

Since review 1, i30's commits changed tests w181 also touched:

- `supervision_proposal_steps.py`: a second branch-reviewer result and two new steps for r110.
- `test_supervision.py`: `is_green` moved from `parse` to `re` with `w\d+`.

Neither drops an assertion of an i29 scenario. The i29 scenarios pass at HEAD.

## Allowances

- w175, both implement reports: none.
- w179, implement report: none.
- w181, 3-implement report: none.
- w181, 4-implement report, `integrate_with_changes`, **setup**: **holds**.
  - `d87a295b` adds a write and commit of `spec/capabilities/other.md` and the `repo` parameter.
  - It changes no `assert`, no expected value and no parametrize case.

## Cannot verify

- w181's 3-implement report says r105 and r109 were not run red after their steps were written. The commits cannot show it. Both are green now, and their steps were undefined before w181.
- Every check is verified.

## Findings

1. **Minor, w181, observation**: `scripts/supervise_analysis.py:10`. The import line is 123 characters, so ruff reports the block as unformatted (I001 at :4).
   - Why it matters: lint is no longer clean on a file w181 touched.
   - Fix: wrap the import, or shorten its comment.
   - Reproduction: `python3 <Scripts>/tools check --base 4640ef08` → `scripts/supervise_analysis.py:4:1: I001`.
2. **Important, no work-item (hand commit `7fed86a0`), observation**: `features/supervision.feature`, the r15 scenario "a field of a worker's result giving a sentence longer than a file name may be is taken as no file".
   - What is wrong: it was committed straight to `features/`, with no formulate round and in no capability-proposal (`i29-supervision` names r105–r109, not r15).
   - What it says is within r15's text.
   - Why it matters: it bypassed formulating-features and its gate.
   - Fix: none to code. Later scenarios of an existing line go through a capability-proposal that names the line under `changes`.
   - Reproduction: `git show --stat 7fed86a0` → `features/supervision.feature | 10 +`, on the first parent, no round merged.
3. **Minor, no work-item (i29's round stage directories), observation**: three tracked probe scripts make 10 of the 32 ruff errors and bury the real ones.
   - The files: `.shop/work/i29/runs/supervision/1-gate/mk.py`, `5-apply/splice.py` and `6-formulate/splice.py`.
   - Fix: exclude `.shop/` from ruff, or keep only the files a round's result names.
   - Reproduction: `git ls-files -- '.shop/work/i29/*.py'` → 3 files.
4. **Minor, w181, observation**: `scripts/supervise_rounds.py:103-111`, r107's mixed case. When the change list names one known and one unknown capability, the known one's proposal is committed and then `work run` exits with an error. No scenario reaches this path.
   - Review 1 probed `Changes.unknown`: for `thing, newcap, nowhere, ../thing, thing.md` it returned `['nowhere', '../thing', 'thing.md']`.
   - Keep as a test: an r107 scenario whose change list names `thing` (held) and `nowhere`. It would check that `thing.md` is written and committed, that no `nowhere.md` exists, and that the exit is an error naming `nowhere`.
5. **Minor, w181, observation**: `scripts/supervise_analysis.py:62-78`. When the analysis session is cut short or writes no record, the measurement is left uncommitted. A rerun the same day is then refused by `measure_write.py:22` ("exists; --replace writes over it"), so there is no analysis and no done that day.
   - No line names the case.
   - Reproduction by reading: the commit is only inside the `analysis.md` branch (:68-76), and `records_committed` (`supervise_done.py:17-25`) needs both files tracked.
6. **Minor, no work-item (hand commit `e37050ea`), observation, new**: `.shop/records/2026-10-25-i29-analysis.md` and `.shop/records/measurements/2026-10-25-i29.md` were committed by hand ("records: i29's measurement and analysis, as work run wrote them"), not by r106's `work: i29 measurement and analysis record`. i29 is still `started`.
   - Risk: whether r106 fails in a real run.
   - What I verified: the run that did i29's analysis started before w181 merged. Its process had imported the base's `supervise_analysis.py` and `supervise.py`:
     - `git show 4640ef08:scripts/supervise_analysis.py | grep commit` finds only "commit nothing" in the brief;
     - the base's `supervise.py` has no `set_done`;
     - i29's `log.jsonl` has no analysis stage line after the branch review's end, 18:28:10.
   - So this is not a defect of w181's code. It is a run of stale code, and the hand commit stands in for r106. i26 had the same (`cebadf9d`, "left uncommitted; q5").
   - What follows at HEAD: a rerun is refused by `measure initiative` (same date), and `set_done` then finds both records tracked. Whether it sets done turns on `workqueue_done.holds`, which needs the requests naming i29 delivered.
   - What would make it stable: `work run` re-executes itself, or checks that its scripts are unchanged, after it merges a change to `scripts/`. That needs a line if wanted.

## Feature files

- i29 adds these scenarios:
  - through rounds: supervision r105–r109 (`d073c518`) and requests r22 (`6cd77b2b`);
  - by hand: r15 (`7fed86a0`, Finding 2).
- i29 removes no scenario, and no i29 work-item commit touches `features/`.
- Deprecated scenarios, none of them i29's:
  - supervision r102 (i28): its replacements' work-items w170–w172 are `green`, and it is still there. That is for i28.
  - work-queue r9: replacement accepted by w140 (i24), `green`. Still there.
  - work-queue r1, migration-tools r15 and supervision r83 (w185 `drafted`): their replacements are not green.
  - The r19 40-turn scenario of review 1 was retired by `cd134f29` (i30).
- Every binding names a scenario.

## Shape

Size limit: **met**. `tools size --limit 300` prints nothing.

Module map, each row i29 touched:

| Row | Result |
|---|---|
| `scripts/supervise_done.py` | met. A new module and a new row (CLAUDE.md:34, `07d5c24c`). |
| `scripts/supervise_analysis.py` | met. The commit of the records (:71-76) is the measure-and-analysis concern. |
| `scripts/supervise_change.py` | met. `unknown` and `kept_path` belong to the change list. i30's merge of the entries naming one capability (`bd765f03`, :58-62) runs after r107's filter at `supervise_rounds.py:111`; checked by reading. |
| `scripts/supervise*.py` | met. Covers `supervise_brief.py` (Drafts path), `supervise_rounds.py:103-111` and `supervise_worker.py:233-238`. In `supervise.py:208-218`, i30's r110 loop leaves r105's `set_done` behind `lists_nothing(kept)`. A fix that does not turn green breaks out with `kept` still the review with findings, so no done follows. Checked by reading. |
| `scripts/workqueue_done.py` | met. `holds` (:41) is the same condition, made public. |
| `scripts/workqueue_request.py` | met (:93). It strips whitespace, per Reading B in w175's Answers. |
| `tests/scenarios/` | met. `supervision_done_steps.py` is its own `<capability>_*_steps.py` module. |

- Unreached code: vulture is clean. No scenario reaches the r107 mixed case (Finding 4) or the no-drafts fallback of `kept_path`.
- Refactor, as an observation: the drafts path goes from `supervise_change` to `supervise_brief` as a prose sentence that a regex reads back.
  - Fix: a shared constant or function.
  - Check that it is complete: `git grep "The drafts of this proposal are in"` finds the literal in one module only.

## Coupling

- i29's code relies only on what its dependencies publish:
  - git porcelain and plumbing (`ls-files`, `status --porcelain`, `add`, `commit -- <paths>`);
  - pathlib raising `OSError`/`ValueError` on names the file system refuses;
  - the `measure initiative` contract (its last stdout line is the path; it refuses an existing measurement), which is this repository's own script.
- Nothing would break behind those contracts.
- Internal couplings:
  - the prose sentence of Shape;
  - a long-running `work run` holding imported code while it merges changes to that code (Finding 6).

## Observations

- `supervise_analysis.py:4` I001: `tools check --base 4640ef08` → `scripts/supervise_analysis.py:4:1: I001`.
- Hand-written r15 scenario: `git show --stat 7fed86a0` → `features/supervision.feature | 10 +`, no round.
- Tracked round probe scripts: `git ls-files -- '.shop/work/i29/*.py'` → 3 files; 10 ruff errors.
- r107 mixed case not pinned: the probe of `Changes.unknown` → `['nowhere', '../thing', 'thing.md']`; no scenario covers it.
- Lone measurement left uncommitted: read in `supervise_analysis.py:62-78` and `measure_write.py:22`.
- Records committed by hand: `git show --stat e37050ea` → 2 records files. `git show 4640ef08:scripts/supervise_analysis.py` has no commit, and there is no analysis log line in `.shop/work/i29/log.jsonl`.
- Deprecated supervision r102 (i28) and work-queue r9 (i24) with green replacements: `features deprecated` lists them.
