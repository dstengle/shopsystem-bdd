# Branch review 2 of i24-requests-and-the-context-loop

**Verdict: DONE_WITH_CONCERNS.** The suite is green and every work-item's check passes at HEAD. Four of branch review 1's five fix-now findings are fixed: F1 by w157, F3 by w159, F4 by w161 and F5 by w160. F2's fix (w158) covers only an initiative with no `fulfils`. One finding is triaged fix now (Important, w158): a `proposed` initiative whose `fulfils` names a request the queue does not hold still leaves invalid data behind, and this was reproduced at HEAD. No finding is Critical.

## Range

`f890f2f..25f9d50`: 437 commits. Branch review 1 read `f890f2f..4dec501` (its findings are at `.shop/work/i24-requests-and-the-context-loop/runs/branch-review/1/findings.md`). This review re-runs every check over the whole branch and reads the diff `4dec501..25f9d50` line by line.

**Work-items.**
- w121 is withdrawn (its commits were merged; see review 1).
- w122–w135, w137–w155 and w157–w161 are green.
- w136 and w156 are withdrawn and have no implementation commits.

**Attribution of the new commits.** Each implementation commit falls inside its work-item's `ready -> claimed` .. `claimed -> done` window. Where windows overlap, the commit just before the item's `claimed -> done` is taken as that item's:

| Commit | Work-item | Subject |
|---|---|---|
| 6e6d314 | w157 | per-answer commit, r77 |
| 38bc1ca | w158 | r79 |
| 460e639 | w159 | r27 |
| d04cc02 | w160 | r23 |
| a4c0856 | w161 | r65–r67 |

w161's report says "Commit 16eaabf", which is its pre-merge hash. The content matches a4c0856.

**Commits that belong to no work-item** (Minor, observation, as in review 1). These are made under the person's delegation:
- `spec:` f9395a2.
- `features:` 3a47d3b and 45beb7f. Both only add scenarios.
- Hand-written `work:` commits: 4a50590, 331acaf (a delegate's ruling on w158), c2c7dbd (notes on w157–w160) and d20cd17 (w156's dangling gitlinks removed).

## Suite

`Suite: 848 passed, 0 failed at 25f9d50 in 18 s`. pytest's own line is `848 passed, 1 skipped, 360 warnings, 56 subtests passed in 17.86s`, and the wall time was 18.1 s.

- It runs in parallel: `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- The steps do not drive the entry points in-process: they use `subprocess.run` (`tests/scenarios/conftest.py:34`, `:111`).
- It runs under 60 s, so this is no finding.

## Checks

**Work-item checks.** I ran `python3 -m pytest -q --work-item <w>` (`-n auto` comes from pytest.ini) at 25f9d50 for every green work-item. All pass. Each run also has 1 skipped and 56 subtests passed.

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
| w151 | 145 passed |
| w152 | 143 passed |
| w153 | 146 passed |
| w154 | 145 passed |
| w155 | 144 passed |
| w157 | 145 passed |
| w158 | 144 passed |
| w159 | 156 passed |
| w160 | 147 passed |
| w161 | 145 passed |

**`tools check --base f890f2f`** exits 1 (Minor, observation; see O4).

- `== ruff ==`: 13 errors. Review 1 had 7, and all 7 are still there, two at moved lines. The fix commits add four and w156's run record adds two.
  - **Review 1's seven, still there:**
    - I001 at `scripts/measure_build.py:3`
    - I001 at `scripts/supervise_analysis.py:4`
    - I001 at `tests/scenarios/test_design_model_check.py:7`
    - I001 at `tests/scenarios/test_work_queue.py:7`
    - FURB167 at `tests/scenarios/design_model_check_requests.py:132`
    - I001 at `scripts/workqueue.py:244`: the import that was at `:239`, which w160's d04cc02 moved into `moved_to`.
    - FURB167 at `tests/scripts/stub_claude.py:183`: review 1's `:182`, one line down.
  - **New on the fix commits:**
    - FURB167 at `scripts/measure_read.py:58` (w161, a4c0856)
    - F401 at `tests/scenarios/design_model_check_problems.py:6`: `CONTEXT` is unused since `malformed_record` moved out (w159, 460e639)
    - FURB167 at `tests/scenarios/supervision_delegation_steps.py:144` (w157, 6e6d314)
    - FURB167 at `tests/scripts/stub_claude.py:184` (w157, 6e6d314)
  - **New, in a run record:** I001 at `.shop/work/i24-requests-and-the-context-loop/runs/w156/1-research/probe_delegation.py:3` and `probe_more.py:3`. These are w156's research probes, still tracked after d20cd17 removed its gitlinks.
- `== vulture ==`: `tests/scenarios/work_queue_status_steps.py:77` has an unused variable `notes` (w123). This is unchanged since review 1.
- `== import-linter ==`: "the project states no import contracts". This is not `missing`; there is nothing to read.

**`tools size --limit 300`**: prints nothing.

**`features deprecated`**: three deprecated scenarios are left.
- migration-tools @r15 and work-queue @r1 were already there at Base.
- work-queue @r9 "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)": its replacement's work-item, w140, is green, and nothing retires it yet. This is review 1's M1, still open; see O5.

**`features bindings`**: "every binding names a scenario".

**Dry-run and real modes**: none on this branch. No fix commit adds one, so no randomized test is needed.

## Removed and weakened tests

None in `4dec501..HEAD`. Review 1 found none in `f890f2f..4dec501`.

What I searched: every removed line under `tests/` and `conftest.py` in `git diff 4dec501 HEAD`, for a removed `assert`, `def test_` or parametrize case, and every added `skip` or `xfail`. I found:

- `design_model_check_problems.py::malformed_record` (w159) moved unchanged to `design_model_check_records.py`, gaining two branches for the new r27 rows. The only removed `assert` is that function's own line, which is now in the new file.
- `batch_measurement_request_steps.py::fulfils` and `fulfils_none`, and `batch_measurement_world.py` (w161): Givens only. `world.request` became `world.requests`, a list; no assert changed.
- An added `skip` or `xfail` anywhere in `f890f2f..HEAD`: 0.

## Allowances

- w157, w158, w160: the reports give "none". This is checked against their diffs: they only add steps.
- w159: "none (malformed_record moved unchanged for existing rows)". This holds.
- w161: "none (the two existing Givens moved to the list form; asserts unchanged)". This holds.
- Review 1's two rows (w121 `run_work` setup, w130 `with_state` setup) are unchanged since then.

## Cannot verify

Nothing a work-item names. Review 1's F-obs-1 and F-obs-3 remain checked by reading only, as review 1 said. Neither part of the code changed since then.

## Findings

### R2-F1. Important, w158 (38bc1ca), fix now: a `proposed` initiative whose `fulfils` names a request the queue does not hold is left invalid

**Where:** `scripts/supervise_rounds.py:32-33` (`due`) with `:47-49` (`round` → `start_initiative`), and `scripts/supervise_brief.py:68-70` (`integrate_lines`).

**What is wrong:** w158 gates the integrate round on `data.get("fulfils")` being non-empty. A `fulfils` that names a request not under `.shop/work/requests/` still goes through `round()`:

- The initiative is moved to `started` and that is committed (r84).
- `round/i1-1-integrate` is made.
- `integrate_lines` → `accepted_lines` then raises `Refused`, which `except (Fault, GitFailed)` does not catch, so `keep_round` never runs.

This is branch review 1's F2 exactly, by the one other way in. The w158 plan named it as open case B ("Today the run moves the initiative to `started` before it refuses… decision 4 leaves it as it is"), and the report lists it unchosen.

**Why it matters:**
- It contradicts r10 ("If `work run` cannot start the delivery … change nothing").
- r84 moves to `started` only when the round starts, and here it does not.
- The data is left invalid: `log.jsonl` is uncommitted, the branch is left behind, and every later `work run` is refused under r46.

**Reproduced** (probe: the supervision Background, `initiative.md` with `status: proposed` and `fulfils: q9`, no `q9.md`, every round ends, `work run i1` twice). What came back:

- `EXIT 1`, `ERR work: there is no request q9 under .shop/work/requests`
- `STATUS  M .shop/work/i1/log.jsonl`
- `BRANCHES * main  round/i1-1-integrate`
- `INIT … status: started … fulfils: q9`
- `LOG work: i1 proposed -> started`
- The second run gives `EXIT 1`, `ERR work: .shop/work/i1/log.jsonl under .shop/work is not committed; commit it before work run starts`.

**Fix:**
1. Before anything moves (in `due()`, or in `round()` before `start_initiative`), read the request through `workqueue_request.path_of` / `accepted_lines`.
2. Refuse as r10 requires, with nothing changed. Alternatively, catch `Refused` in `round()`, put the status back and run `keep_round`.
3. Add an r10 (or r79) examples row "fulfils a request the queue does not hold".

**Keep as a test:** the probe above, as a scenario under r10:

```
Given i1 is proposed and fulfils the request q9, which the queue does not hold
And every round ends
When the person runs `work run i1`
Then it exits with an error, saying the queue does not hold q9
And i1 is proposed
And no branch is made for a round
And nothing under .shop/work/ is left uncommitted
```

Its Given writes `---\nid: <i1>\nkind: initiative\nstatus: proposed\nfulfils: q9\n---\n` and commits it.

### Branch review 1's findings, re-checked

- **F1 (w147 → w157): fixed.**
  - `supervise_answers.py:76` commits each answer as it is written, so r28's checkout check no longer reverts it.
  - The closing commit runs only when something is uncommitted (`:80`, `uncommitted`).
  - The r77 scenario with two questions on one work-item passes.
  - Remaining case, an observation (O6): a commit or push that fails after the first answer was pushed. w157's report lists it.
- **F2 (w151 → w158): fixed for an initiative with no `fulfils` only.** See R2-F1 for the other way in, and O3.
- **F3 (w131/w146 → w159): fixed.** `model_work.py:11,14` now has `awaiting-answer` for a capability-proposal and `withdrawn` for a request. There is a r27 examples row for each.
- **F4 (w133 → w161): fixed.** The refusals now have their lines: batch-measurement r65, r66 and r67 (f9395a2), with one scenario each. See O1 and O2 for the new reader.
- **F5 (w130 → w160): fixed.** `retry` and `withdraw` share `moved_to` (`workqueue.py:242-252`), which runs `workqueue_done.becomes`/`mark` and puts `initiative.md` in the commit. There is an r23 scenario for retry.

## Shape

- **Size limit (CLAUDE.md): met.** `tools size --limit 300` prints nothing.
- **Module map: met.**
  - The fix commits add one module, `tests/scenarios/design_model_check_records.py` (w159). It is a step module under `tests/scenarios/`, named like its siblings `design_model_check_requests.py` and `_reading.py`, which are already off the `<capability>_*_steps.py` pattern (review 1 noted this).
  - `measure_read.py` (w161), `model_work.py` (w159), `supervise_answers.py` (w157), `supervise_rounds.py` (w158) and `workqueue.py` (w160) each keep their rows' concerns.
  - Review 1's two stale rows are unchanged (Minor, observation): `supervise_rounds.py` also runs gate and integrate rounds, and `workqueue_done.py` is also called by `work retry` now (w160) and by work run's integrate round. Check that would show this complete: each row names every caller of its module's public functions.
- **Code no scenario reaches:**
  - `scripts/measure_read.py:65`: the test `"/" in ident` can never be true, because `ident` comes from `rsplit("/", 1)[-1]` (O2).
  - `CONTEXT` is unused at `design_model_check_problems.py:6` (F401).
  - vulture's `notes` is unchanged since review 1.
- **The repository's own `model check`** (Minor, observation, unchanged): v16a for i24, which fulfils no request, and v_d1 for i1, i3, i8–i11, i13, i16 and i17. There are 17 `w_uncited_obs` warnings. Repro: `python3 <Scripts>/model check`, which prints `10 violations, 17 warnings, 0 unresolved references, 0 file problems`.

## Coupling

Unchanged since review 1 (`Claude Code transcripts`, `claude -p --output-format json`, pytest-bdd internals in `work_items.py`, Claude Code hooks). The fix commits add no dependency on another project.

`tests/scripts/stub_claude.py` now also keys on the brief's `Question:` line (w157). That line is written by this repository's own `answer_brief`, so it is an internal contract.

## Observations

- **O1. Minor, w161, `scripts/measure_read.py:57-59`.** The new `fulfils` reader is a regex over the frontmatter, not the model's reader (`model_parse.frontmatter`, which strips comments and reads `[a]` and `- a` lists). Repro: `request_of` on an i9 whose request q3 is held. What came back:
  - `fulfils: request/…/q3   # the cart request` → `REFUSED … the initiative fulfils more than one request: #, cart, q3, request, the`
  - `fulfils: [q3]` → `REFUSED: the queue does not hold the request [q3]`
  - `fulfils: [request/…/q3]` → `REFUSED … q3]`
  - `fulfils:` followed by `  - q3` → `None`, read as fulfilling no request.
  - The scalar and bare-id forms read right.
  - No client writes those forms today: `work start` writes a scalar. Fix: take the values from `model_parse.frontmatter`, collecting a repeated key.
- **O2. Minor, w161, `scripts/measure_read.py:65`.** `"/" in ident` cannot be true; drop it. Repro: reading the line above it.
- **O3. Minor, w158, `spec/capabilities/supervision.md:26`.** r79 still reads "When an initiative is `proposed`, `work run` shall start a round of the kind `integrate`…". The new @r79 scenario pins that a `proposed` initiative with no request gets none. It stands on a delegate's ruling (331acaf) that r9, r32 and r52 give the exit. Writing r79 as "proposed and fulfils a request the queue holds" (through integrating-a-proposal, with R2-F1's refusal) would make the line say what its scenario pins. Repro: `features/supervision.feature` @r79 "a proposed initiative that fulfils no request…" against `supervision.md:26`.
- **O4. Minor, w157, w159, w161 (and w156's run record): lint.** These are the four new ruff hits on the fix commits and the two in w156's run record, listed under Checks. Review 1's seven are still there too. Fix: `ruff check --fix`, and remove `runs/w156/1-research/*.py` from the run record, as d20cd17 did for its gitlinks. Repro: `python3 <Scripts>/tools check --base f890f2f`.
- **O5. Minor, w140: the deprecated work-queue @r9 scenario is still there.** Its replacement's work-item is green and no work-item retires it (review 1's M1). Repro: `python3 <Scripts>/features deprecated`.
- **O6. Minor, w157:** a second answer's commit or push that fails after the first answer is pushed. This is not exercised; w157's report lists it. Repro: none; read from `supervise_answers.py:76` and `supervise.py:96-107`.
- **Carried over from review 1, unchanged by the fix commits:** F-obs-1 (w134, a thread crash exits 0), F-obs-2 (w147, the answer pass runs once a run), F-obs-3 (w124, hooks in worker sessions), F-obs-4 (w153), F-obs-5 (w148) and F-obs-6 (supervision r74, one drafted fix work-item for findings across capabilities: here w157–w161 were drafted one a finding, by hand). Their reproductions are in review 1's findings.
