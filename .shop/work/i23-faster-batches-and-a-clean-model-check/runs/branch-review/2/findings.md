# Branch review 2 of i23-faster-batches-and-a-clean-model-check

**Verdict: DONE_WITH_CONCERNS.** Review 1's two fix-now findings are resolved: F1 by w119 and F2 by w120. One new finding is fix now: Important, w119 (G1). w119's research stage committed 440 probe files onto the branch. Among them are 7 gitlinks to commits that exist in no repository, with no `.gitmodules`, and two probe scripts that make `tools check` exit 1 again. Nothing is Critical, and every check was run and verified.

## Range

`1ad6281..3280486` (branch `next`). The base is the commit that added `initiative.md`.

Review 1 covered `1ad6281..1620d96` (runs/branch-review/1/findings.md). I re-ran every check over the whole range and read the new commits in full. For the commits up to 1620d96, I re-checked review 1's diff findings against the current tree (`git diff 1ad6281 HEAD -- tests`).

| work-item | status | commits (between `ready -> claimed` and `claimed -> done`) | accepts |
|---|---|---|---|
| w107 | green | 753c5a6 | analysis-tools#r7 |
| w108 | green | e00780e | migration-tools#r4 r9 r30 r31 |
| w109 | green | 4232bc6 | supervision#r1 r20 r59-r63 |
| w113 | green | a3cb90e | work-queue#r15 |
| w114 | green | 8f76e50 | analysis-tools#r58 |
| w115 | green | 4ebe93b | batch-measurement#r47 r57-r59 |
| w116 | green | 495a420 | design-model-check#r27 |
| w117 | green | aaeea80 | design-model-check#r106 |
| w118 | green | 8a32a57 | design-model-check#r111 |
| w119 (fix of review 1 F1) | green | fd035f0; and work run's 27b455b (`drafted -> researched`), which carries G1 | supervision#r63 |
| w120 (fix of review 1 F2) | green | edad3b6 | work-queue#r15 |
| w110 | withdrawn | 5d88909, aecf1e7, 2e956ab (w115 accepts the same ids) | batch-measurement |
| w111 | withdrawn | none inside work run; c8eb828 and 6559731 were delivered outside it (review 1 F4, still open) | delivery#r17 r18 |
| w101-w106, w112 | withdrawn | none | |

New commits since review 1 that belong to no work-item:

- a1d3686: work run's commit of review 1.
- 12de9c8: the coordinator's new r63 scenario, a formulation commit.
- 3b16ac2 and dd86fd8: `work add`.
- e6dca58: a work-item note.

None of them holds code.

## Suite

`Suite: 724 passed, 0 failed at 3280486 in 16.09 s` (1 skipped: tests/scripts/test_tools.py "nothing is missing here", which comes from the environment; 56 subtests passed).

- It runs in parallel: `-n auto` is in pytest.ini's addopts, on 32 CPUs.
- It is not in-process: the step definitions drive `work`, `model`, `measure`, `migrate` and `tools` as subprocesses.
- At under 60 s, this is no finding.

## Checks

No work-item names a `check:`. Each green work-item's acceptance is its scenarios. I ran `python3 -m pytest -q --work-item <w>` for each at HEAD:

| work-item | result |
|---|---|
| w107 | 139 passed, 1 skipped |
| w108 | 152 passed, 1 skipped |
| w109 | 151 passed, 1 skipped |
| w113 | 146 passed, 1 skipped |
| w114 | 139 passed, 1 skipped |
| w115 | 146 passed, 1 skipped |
| w116 | 150 passed, 1 skipped |
| w117 | 143 passed, 1 skipped |
| w118 | 139 passed, 1 skipped |
| w119 | 140 passed, 1 skipped |
| w120 | 146 passed, 1 skipped |

For w119, the run includes the new scenario "a worker is started for a work-item whose blocked_by names a green work-item of another initiative". With `-rA` it is PASSED.

w120's own check is that `tools check` passes on `work_queue_answer_steps.py`. That file is now clean under ruff. The project-wide check still fails, for G1's files: w120's implementer ran the check on the one file only (its report says so).

`tools check --base 1ad6281` exits 1:

- **ruff**: 3 errors, all in files G1 committed:
  - `.shop/work/i23-…/runs/w119/1-research/probe_blocked.py:3:1 I001`
  - `…/probe_other.py:3:1 I001`
  - `…/probe_other.py:8:27 F401` (`probe_blocked.BASE` unused)
- **vulture**: clean.
- **import-linter**: "the project states no import contracts". No heading says `missing`.

The other checks:

- **`tools size --limit 300`**: prints nothing.
- **`features deprecated`**: two scenarios, both from i21 and neither from this branch:
  - migration-tools @r15 "`migrate run` on a repository with <change> refuses…"
  - work-queue @r1 "add with --part-of…"

  Their replacements' work-items (i21 w86, w89, w90) are withdrawn, not green, so this is no finding.
- **`features bindings`**: "every binding names a scenario".
- **Dry-run against real mode**: `model decisions --check` against `model decisions` is the system's one pair. The `git push --dry-run` calls in supervise_review.py:41 and supervise_faults.py:66 are git's mode, not the system's. The suite still has no randomized test that the pair agrees (review 1 F7, unchanged). My probe, review 1's with seed 24, tried **60 cases**, and all agreed. It is kept below as O5.

## Removed and weakened tests

Searched: `git diff 1ad6281 HEAD -- tests` for removed `def`s, step decorators, `assert`s, parametrize and Examples rows, and added `skip`/`xfail`.

- Since review 1 (`git diff 1620d96 HEAD -- tests`): w119 adds three steps (supervision_parallel_steps.py:31-40 and :134-136). w120 removes one blank line (work_queue_answer_steps.py:6). Nothing was removed or weakened.
- Before that: the same nine items review 1 lists in its "Removed and weakened tests", each still in the tree and each listed in its work-item's plan or Retires. They are:
  - analysis_tools_probe_steps `failed_command` (w107)
  - the batch_measurement_then_steps `gives_totals` columns (w110)
  - the migration_safety n1 steps (w108)
  - the migration_version r30/r31 Thens (w108)
  - supervision_then_workers `one_at_a_time` (w109)
  - test_supervision `merged_in_line` (w109)
  - the work_queue_answer two-lines When (w113)
  - the retired @r20 "no more than two" scenario (w109)
  - the retired @r47 outline (w110 and w115)

  No skip or xfail was added.
- **`features/`**: the only change since review 1 is 12de9c8, which adds an r63 scenario. That is a formulation commit, not a work-item's. No work-item's commits change `features/` other than the retirements review 1 verified. Nothing is Critical.

## Allowances

- **w119**: "none". Verified: fd035f0 changes no existing test, only adding steps.
- **w120**: "none". Verified: edad3b6 removes one blank line.
- **w108, w113, w118**: review 1's rows still hold, and those files are unchanged since.

## Cannot verify

None.

## Findings

### G1. Important, w119, fix now: probe repositories and scripts committed into the branch, with dangling gitlinks

- **Where**: 27b455b (`work: w119 drafted -> researched`), `.shop/work/i23-faster-batches-and-a-clean-model-check/runs/w119/1-research/`. It holds `probe_blocked.py`, `probe_other.py` and `probe_blocked_runs/<7 cases>/`, 440 files and 6924 lines in all.
- **What is wrong**:
  - The researcher ran its probes in its run directory. Its brief's "Run directory" is `.shop/scratch/1-research`, and its notes call that "scratch directory only".
  - work run copies the whole run directory into `runs/w119/1-research` and commits it (supervise_worker.py:169-170, `shutil.copytree(here, kept_at)` and then `self.own`). The commit took everything with it:
    - bare `remote.git` repositories with their objects and hooks: 119 executable files, among them `hooks/pre-receive` and `post-receive`;
    - the stand-in `claude` and its transcripts;
    - **7 gitlinks** (mode 160000), one per case's `repo`.
  - Verified for the gitlinks:
    - `git ls-files -s … | grep ^160000` gives 7 entries.
    - There is no `.gitmodules`.
    - `git cat-file -t 9b4c6aa…` gives "could not get object info": the commits exist in no repository.
    - The `repo` directories are empty in the checkout.
- **Why it matters**:
  - The branch tree holds invalid data: gitlinks that cannot be resolved, without the mapping that git's submodule commands need.
  - `tools check --base` exits 1 on the two probe scripts. That undoes w120's purpose for the branch as a whole.
  - The noise lands in every later review and measure range.
- **Fix**:
  - `git rm -r --cached` the `probe_blocked_runs/` directory and the two probe scripts, remove them from the checkout, and commit.
  - Hardening, an observation for supervision (O1): keep only the regular files of a run directory. Or refuse a run directory that holds a `.git`, as the coordinator's scratch rule would want.

## Review 1's findings, re-checked

- **F1** (w109, fix now) is **resolved** by w119.
  - Where: supervise_pool.py:62-63 builds the statuses from `workqueue.items(self.root)` across every initiative, and this initiative's reading wins on a shared name (plan D1).
  - Risk named: that this makes `work run` read other initiatives' files for the first time, so an unreadable file there could stop it. Verified: `Run.items()` (supervise.py:60-61) already globs every initiative through the same `workqueue.items`, so no new read can fail. The new scenario passes.
- **F2** (w113, Minor) is **resolved** by w120: ruff reports nothing in work_queue_answer_steps.py.
- **F3, F6 and F7** (observations) are unchanged: the files are untouched since 1620d96.
- **F4 and F5** (commits outside work run, and unrelated records) are unchanged.

## Shape

- **Size limit**: met. Every touched file is ≤ 300 lines, and supervision_parallel_steps.py has gone from 125 to 142 lines.
- **`scripts/supervise*.py`**, the row for supervise_pool.py: met. The cross-initiative reading is in `Pool.choose` (supervise_pool.py:62-63), the pool's concern. `Run.items` stays this initiative's, since `check` and `run` read it.
- **`tests/scenarios/<capability>_*_steps.py`**: met. The new r63 steps are in supervision_parallel_steps.py, beside the other r63 steps.
- **Unreached code and steps**: vulture is clean, and `features bindings` is clean.
- Review 1's shape observations (supervise.py:53 `self.limit = 4`; the model_work.py:191 rebuild) still stand.

## Coupling

Unchanged from review 1, since no new dependency was added:

- Claude Code's transcript layout (supervise_worker.py `with_transcript`, measure_read.py) is unpublished.
- `claude -p --output-format json` is documented.
- `SystemExit` in work_items.py under xdist is a crash where a refusal belongs (outside this diff).
- `ruff==0.17.0` on PyPI.

## Observations

- **O1** (supervision, predates the branch): work run commits a run directory as it is, nested repositories included (supervise_worker.py:169).
  - Reproduction: `git ls-files -s .shop/work/i23-faster-batches-and-a-clean-model-check/runs/w119 | cut -c1-6 | sort | uniq -c` → `324 100644`, `119 100755`, `7 160000`.
- **O2** (w119): a blocker named by its id form, absent everywhere, or whose file disagrees with log.jsonl.
  - What happens: it blocks, or counts by its file, with nothing printed (plan §5; research probes A4, A5, B1). r63 asks for no reason.
  - Reproduction: research notes §2, probes A4 and B1.
- **O3** (w120's report): an empty answer `""` to an awaiting-answer item is accepted as an empty bullet. U+001C-U+001E are accepted as one line, while `splitlines` sees two.
  - Reproduction: w120 notes 6a and 6b; review 1's test_probe_breaks → `not refused ['0x1c', '0x1d', '0x1e']`.
- **O4**: review 1's F3 (merge order under lock contention), F6 (test_measure_runs fixture, `{'session': 's-1', 'turns': 14, 'session_json': 'empty'}`), and its w108 and w115 observations are all unchanged.
- **O5**: no randomized test that `model decisions --check` agrees with `model decisions`. The probe tried 60 cases at 3280486, and all agreed.

  Keep as a test (tests/scripts/test_model_decisions_agree.py):

```python
import random

from test_model import ModelTest

WORDS = ["cart", "shelf", "price", "order", "a b", "x-y", "é", "q", "z"]


class DecisionsAgree(ModelTest):
    def decision(self, rng, n):
        name = "-".join(rng.sample(["cart", "shelf", "price", "order", "tax"], rng.randint(1, 3)))
        summary = " ".join(rng.choice(WORDS) for _ in range(rng.randint(1, 6)))
        self.write("spec/decisions/%04d-%s.md" % (n, name),
                   "---\nid: design-decision/missingmass.io/shop/%s-%d\nsummary: \"%s\"\ndate: 2026-%02d-%02d\n"
                   "status: %s\nby: someone\n---\n\n# %04d. %s\n" % (name, n, summary, rng.randint(1, 12),
                   rng.randint(1, 28), rng.choice(["accepted", "proposed", "superseded"]), n, name))

    def test_check_agrees_with_write(self):
        rng = random.Random(24)
        for case in range(60):
            with self.subTest(case=case):
                self.reset()
                for n in rng.sample(range(1, 60), rng.randint(0, 8)):
                    self.decision(rng, n)
                index = self.tmp / "spec/decisions/index.md"
                if rng.random() < 0.5:
                    index.parent.mkdir(parents=True, exist_ok=True)
                    index.write_text(rng.choice(["", "# hand written\n", "stale\n"]))
                before = index.read_text() if index.exists() else None
                checked = self.run_model("decisions", "--check")
                self.assertEqual(before, index.read_text() if index.exists() else None)   # --check writes nothing
                self.assertEqual(self.run_model("decisions").returncode, 0)
                self.assertEqual(checked.returncode, 0 if before == index.read_text() else 1)
                self.assertEqual(self.run_model("decisions", "--check").returncode, 0)
```

- **Deprecated scenarios from i21**: migration-tools @r15 and work-queue @r1 are still in `features/`, and their replacements' work-items are withdrawn. Reproduction: `features deprecated`.
