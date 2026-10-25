# Branch review 4 of i24-requests-and-the-context-loop

**Verdict: DONE.** No finding is Critical and none is triaged fix now. I ran every check myself at HEAD (a89acb5), and every one passed or is accounted for below.

- **Branch review 3's one fix-now finding, R3-F1, is fixed by w163 (aa84202).** An integrate round that ends DONE now commits its stage directory, so nothing is left under `.shop/work/` and the next `work run` is not refused. The new @r84 scenario pins this, and it passes.
- What is left is Minor observations and the Important observations carried over from earlier reviews. None of them changed in this range.

## Range

`f890f2f..a89acb5`: 473 commits, linear, with no merge commits.

- Branch reviews 1–3 read `f890f2f..37a9445` line by line. Their findings are under `.shop/work/i24-requests-and-the-context-loop/runs/branch-review/{1,2,3}/findings.md`.
- This review re-runs every check over the whole branch. It reads the diff `37a9445..a89acb5` (23 commits) line by line, and re-checks the whole branch for test removals, `features/` changes and attribution.

**Work-items.**
- w122–w135, w137–w155 and w157–w163 are green.
- w121, w136 and w156 are withdrawn. w121's commits 3593951 and 82ad81f are on the branch (review 1). w136 and w156 have no implementation commits.

**Attribution.** Every commit that touches `scripts/`, `tests/`, `agents/`, `skills/`, `hooks/`, `CLAUDE.md` or `README.md` falls inside its work-item's `ready -> claimed` .. `claimed -> done` window. I listed the 45 commits with `git log -- scripts tests agents skills hooks CLAUDE.md README.md …` and matched each one to its window. The new ones in this range:

| Commit | Work-item | What |
|---|---|---|
| aa84202 | w163 | `supervise_rounds.py` +3, `supervision_rounds_steps.py` +16, between `103aee0 work: w163 ready -> claimed` and `e8a6d4e work: w163 claimed -> done` |
| c552fa6 | none (formulation) | `features:`, adds one @r84 scenario only. The coordinator wrote it under the person's delegation (w163's first answer). |
| b1ae888 | none | branch review 3's record |
| 6c3c3e3 | none | hand removal of w163's probe gitlinks (see O1) |
| `work:` / `work add` / `work answer` / `work retry` | `work run` and the queue | |

## Suite

`Suite: 850 passed, 0 failed at a89acb5 in 21.0 s`

- pytest's own line: `850 passed, 1 skipped, 364 warnings, 56 subtests passed in 20.97s`. The wall time, by `date` around the background run, was under 25 s.
- The skip is `tests/scripts/test_tools.py:78`, "nothing is missing here". It was already there before this branch.
- It runs in parallel: `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- The step definitions do not drive the entry points in-process. They run them as programs with `subprocess.run` (`tests/scenarios/test_supervision.py:68`, `tests/scenarios/conftest.py`).
- It runs under 60 s, so this is no finding.

## Checks

**Work-item checks.** I ran `python3 -m pytest -q -p no:cacheprovider --work-item <w>` at a89acb5 for every green work-item, with `-n auto` from pytest.ini. Every one passes. Each run also has 1 skipped and 56 subtests passed.

| Work-items | Result |
|---|---|
| w122 | 146 passed |
| w123 | 154 passed |
| w124 | 146 passed |
| w125 | 145 passed |
| w126 | 152 passed |
| w127 | 149 passed |
| w128 | 148 passed |
| w129 | 144 passed |
| w130 | 148 passed |
| w131 | 160 passed |
| w132 | 157 passed |
| w133 | 145 passed |
| w134 | 147 passed |
| w135 | 144 passed |
| w137, w138, w139 | 146 passed each |
| w140 | 152 passed |
| w141–w145 (guarantees) | 142 passed each |
| w146 | 144 passed |
| w147 | 146 passed |
| w148 | 155 passed |
| w149 | 145 passed |
| w150 | 144 passed |
| w151 | 147 passed (one more than in review 3: the new @r84 scenario) |
| w152 | 143 passed |
| w153 | 146 passed |
| w154 | 145 passed |
| w155 | 144 passed |
| w157 | 145 passed |
| w158 | 145 passed |
| w159 | 156 passed |
| w160 | 147 passed |
| w161 | 145 passed |
| w162 | 145 passed |
| w163 | 147 passed |

**w163's red.** The implementer's report gives the red as `AssertionError: ([], …)` from the new Then, because the stage directory was untracked. I could not rerun the code before the fix: making a copy of the checkout needed a permission this session does not have. I verified it by reading instead:
- `start_initiative` (`supervise_rounds.py:89-94`) commits before `run_dir` (`:58`) creates `runs/i1/<k>-integrate/`.
- So no commit before aa84202 can hold an `-integrate/` path.
- So `integrate_stage_committed` (`supervision_rounds_steps.py:97-105`) cannot pass on the old code.

**`tools check --base f890f2f`** exits 1, with the same 13 ruff errors as reviews 2 and 3. w163 adds none. See O4.
- `== ruff ==`: 13 errors.
  - I001 at:
    - `runs/w156/1-research/probe_delegation.py:3`
    - `runs/w156/1-research/probe_more.py:3`
    - `scripts/measure_build.py:3`
    - `scripts/supervise_analysis.py:4`
    - `scripts/workqueue.py:244`
    - `tests/scenarios/test_design_model_check.py:7`
    - `tests/scenarios/test_work_queue.py:7`
  - FURB167 at:
    - `scripts/measure_read.py:58`
    - `tests/scenarios/design_model_check_requests.py:132`
    - `tests/scenarios/supervision_delegation_steps.py:144`
    - `tests/scripts/stub_claude.py:183`
    - `tests/scripts/stub_claude.py:184`
  - F401 at `tests/scenarios/design_model_check_problems.py:6`.
- `== vulture ==`: `tests/scenarios/work_queue_status_steps.py:77` has an unused variable `notes` (w123). This is unchanged.
- `== import-linter ==`: "the project states no import contracts". This is not `missing`.

**`tools size --limit 300`** prints nothing. The touched files are `supervise_rounds.py` at 105 lines and `supervision_rounds_steps.py` at 258.

**`features deprecated`**: three deprecated scenarios.
- migration-tools @r15 and work-queue @r1 were already there at Base.
- work-queue @r9 "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)": its replacement's work-item, w140, is green, and no work-item retires it. This is O5, still open.

**`features bindings`**: "every binding names a scenario".

**Dry-run and real modes**: none on this branch, and w163 adds none. No randomized agreement test is needed.

## Removed and weakened tests

None.

What I searched:
- every removed line (`^-[^-]`) in `git diff f890f2f HEAD -- tests conftest.py`;
- added `skip`, `xfail` or `skipif` in that diff: none.

The removed lines account for themselves:
- **`design_model_check_problems.py::malformed_record`** was moved unchanged to `design_model_check_records.py:10-44`, with two cases added (w159).
- **`batch_measurement_then_steps.py::gives_sessions`** now asserts every column of the table, which is stronger. The NUMBERS change is whitespace only.
- **`supervision_tests_steps.py`**: the Given "accepting other#r1" was used only by the deprecated r56 scenario, which w121 retires.
- **`stub_claude.py`**: plan lookup extended to `round:` and `question:` keys. The default is unchanged.
- **Givens and imports** in `batch_measurement_given_steps.py`, `_transcripts.py`, `_world.py` and `work_queue_answer_steps.py`.

Scenarios removed from `features/` inside work-item commits:
- w122 batch-measurement @r43 (9e99ba6)
- w124 migration-tools @r24 (63bdb23)
- w121 supervision @r56 (3593951)
- w131 design-model-check @r19 (d23a6a4)

Each was `@deprecated` and listed under its work-item's `## Retires`. Their bindings are whole-file `scenarios()` calls.

## Allowances

- **w163**: its report gives "none", and aa84202 agrees: it adds two step definitions and changes no existing test.
- **Earlier rows** (review 1: w121 `run_work` setup and w130 `with_state` setup; reviews 2 and 3: none): unchanged since then.

## Cannot verify

Nothing a work-item names.
- **w163's red**: verified by reading, as above, not by running.
- **Review 1's F-obs-1 and F-obs-3**: still checked by reading only. Their code is unchanged.

## Findings

No finding in this range is Critical, and none is triaged fix now.

### R3-F1 (w151, fixed by w163)

**What w163 does:** `Rounds.round` (`scripts/supervise_rounds.py:85-87`) commits the integrate round's stage directory, `initiative.md` and `log.jsonl` after the round's merge, and pushes (r38).

**The decision on "with i1's change to started":** the scenario's Then reads "a commit of the integrate round's stage directory with i1's change to started". The work lands as two commits, `started` and then the stage directory, and the step accepts that shape. The coordinator accepted it under the person's delegation (w163's third answer). See O2 for the wording this leaves.

**Risk checked:** if the round's commits had already tracked the stage directory, the new `git commit` would fail with nothing to commit, outside the `try`.
- What I verified: `session.json` is written by `work run` in the main checkout after the session ends (`supervise_worker`), so there is always something to commit.

**Code no line asks for:** checked, and not this finding.
- The new commit is the commit of r84's transition to `started`, made under r7's shape (stage directory, item file, `log.jsonl`) and pushed under r38.
- It is what r46 needs for the next run.
- The @r84 scenario pins it.

**Review 3's other items, re-checked:**
- R3-F2 (r79's line does not give the two held-back cases): still an observation, unchanged.
- O1–O9: unchanged, since aa84202 touches only the DONE path of `round()`.

## Shape

- **Size limit (CLAUDE.md): met.** `tools size --limit 300` prints nothing.
- **Module map:** `scripts/supervise*.py` names `supervise_rounds.py` "a capability-proposal's apply and formulate rounds". It also runs the gate and integrate rounds, and w163 adds an integrate-only branch at `:85-87`.
  - Minor, observation, carried from reviews 1–3.
  - Check that would show it complete: the row names every round kind in `AFTER` and `due()`.
- **Shape of w163's change:**
  - The commit message `work: i1 started -> started` (`supervise_rounds.py:87` → `supervise.py:103`) reads as a transition that did not happen.
  - `keep_round` gives its no-transition commit a message of its own (`supervise_rounds.py:102`).
  - `measure_build.py:81` matches `work: <name> .*-> .*`, but only for work-item names, and it looks only for `-> done`. So no figure changes today.
  - Minor, observation (w163's task review F1).
  - Check that would show it complete: `git log --format=%s` of a run with an integrate round shows no `X -> X` subject.
- **Code no scenario reaches:** unchanged.
  - `scripts/measure_read.py:65`: `"/" in ident`.
  - `CONTEXT` at `design_model_check_problems.py:6` (F401).
  - vulture's `notes`.
- **The repository's own `model check`** (Minor, observation, unchanged): `10 violations, 17 warnings, 0 unresolved references, 0 file problems`.
  - v16a holds for i24 itself.
  - v_d1 holds for nine done initiatives.
  - Repro: `python3 /home/vscode/shopsystem-bdd/scripts/model check`.

## Coupling

Unchanged since review 3:
- Claude Code transcripts
- `claude -p --output-format json`
- pytest-bdd internals in `work_items.py`
- Claude Code hooks
- the stand-in's `Question:` line

w163 adds no dependency on another project.

## Observations

- **O1. Minor, w163 (its research stage record, d69b48d): 224 probe files are tracked under `runs/w163/2-research/probe_repos/`.**
  - What they are: four bare `remote.git` repositories with their objects, plus stub transcripts and `calls.jsonl`.
  - 6c3c3e3 removed only the four `repo` gitlinks. The gitlinks had already faulted w163's 3-plan stage (w163.md `## Faults`).
  - This is the third time (w119 c9e1de6, w156 d20cd17, w163). A researcher's probes inside its stage directory are taken in whole by the stage's commit.
  - Repro: `git ls-files .shop/work/i24-requests-and-the-context-loop/runs/w163/2-research/probe_repos | wc -l` → 224.
  - Fix: remove the directory. For hardening, a supervision line on what a stage's commit takes, or a researcher rule that probes go under `.shop/scratch/` (the work-item already asked for this).
- **O2. Minor, w163, `features/supervision.feature:1070` with `supervision_rounds_steps.py:97-105`: the scenario reads more than the step checks.**
  - The scenario reads "a commit of the integrate round's stage directory with i1's change to started", and its Pins line says "committed with the initiative's change to started".
  - The step accepts any commit with an `-integrate/` path at which `initiative.md` reads `started`, which is the two-commit shape the coordinator accepted.
  - Fix: reword the Then and the Pins line through formulation, for example "a commit of the integrate round's stage directory, after i1's change to started".
  - Repro: read the two places.
- **O3. Minor, w163, `scripts/supervise_rounds.py:87`:** the commit message `work: <initiative> started -> started`. See Shape.
- **O4. Minor, w157, w159, w161 and w156's run record: lint.** These are the 13 ruff hits under Checks.
  - Repro: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base f890f2f`.
  - Fix: `ruff check --fix`, and remove `runs/w156/1-research/*.py`.
- **O5. Minor, w140:** the deprecated work-queue @r9 scenario is still there although its replacement's work-item is green. Repro: `python3 /home/vscode/shopsystem-bdd/scripts/features deprecated`.
- **O6. Minor, no work-item:** commits that belong to no work-item. These are c552fa6 (`features:`, adds one scenario only, under the person's delegation), b1ae888 (review 3's record) and 6c3c3e3 (hand clean-up). Repro: `git log --format='%h %s' 37a9445..HEAD`.
- **Carried over from review 3, unchanged:**
  - R3-F2 (r79's held-back cases)
  - O1 and O2 (w161 `measure_read.py`)
  - O3 (w162 `except Refused`)
  - O6 (w157 second-answer push)
  - O8 (`work add` on a `done` initiative)
  - O9 (a held request with no accepted line)
- **Carried over from review 1, unchanged:**
  - F-obs-1 (Important, w134: a thread crash exits 0)
  - F-obs-2 (Important, w147: the answer pass runs once a run)
  - F-obs-3 (Important, w124: hooks in worker sessions)
  - F-obs-4 (w153)
  - F-obs-5 (w148)
  - F-obs-6 (supervision r74)

  Their reproductions are in reviews 1 and 3.
