# Branch review 3 of i24-requests-and-the-context-loop

**Verdict: DONE_WITH_CONCERNS.** The suite is green, and every work-item's check passes at HEAD (37a9445).

- **Branch review 2's one fix-now finding, R2-F1, is fixed by w162.** A `proposed` initiative whose `fulfils` names a request the queue does not hold now gets no integrate round, and nothing moves.
- **One finding is triaged fix now: R3-F1 (Important, w151).** Every integrate round that ends DONE leaves its stage directory `runs/<initiative>/<k>-integrate/` uncommitted, so the next `work run` is refused under r46. I reproduced this at HEAD. w162's researcher had found it (D3 in its notes) and its plan listed it as an open case, but no review or work-item took it up.
- No finding is Critical.

## Range

`f890f2f..37a9445`: 450 commits.

- Branch review 1 read `f890f2f..4dec501` and branch review 2 read `4dec501..25f9d50`. Their findings are under `.shop/work/i24-requests-and-the-context-loop/runs/branch-review/{1,2}/findings.md`.
- This review re-runs every check over the whole branch, and reads the diff `25f9d50..37a9445` line by line: 13 commits.

**Work-items.**
- w122–w135, w137–w155 and w157–w162 are green.
- w121, w136 and w156 are withdrawn. w121's commits were merged (see review 1). w136 and w156 have no implementation commits.

**The new commits' attribution.**

| Commit | Work-item | What |
|---|---|---|
| 3a307c0 | w162 | `supervise_rounds.py` +6/-1 and one Given in `supervision_rounds_steps.py`, between `01ba96d work: w162 ready -> claimed` and `4ff04ce work: w162 claimed -> done` |
| e3fbf0b | none (formulation) | `features:`, adds one @r79 scenario only. The coordinator made it under the person's delegation, between w162's `claimed -> awaiting-answer` and its answer. It belongs to no implementer. |
| 623cbee | none | branch review 2's record |
| `work:` / `work add` / `work answer` commits | `work run` and the queue | |

Under the rule "a change under `features/` other than removing a deprecated scenario" this would be Critical. I do not grade it that way, as reviews 1 and 2 did not for the other `features:` commits: e3fbf0b is a formulation round's commit, not a work-item's, and it only adds a scenario. It is a Minor observation, a commit of no work-item (O7).

## Suite

`Suite: 849 passed, 0 failed at 37a9445 in 19.8 s`

- pytest's own line: `849 passed, 1 skipped, 362 warnings, 56 subtests passed in 19.53s`. The wall time, by `date` before and after, was 19.8 s.
- The skip is `tests/scripts/test_tools.py:78`, "nothing is missing here", which was already there before this branch.
- It runs in parallel: `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- The step definitions do not drive the entry points in-process. They run them as programs with `subprocess.run` (`tests/scenarios/conftest.py:34`, `test_supervision.py` `run_work`).
- It runs under 60 s, so this is no finding.

## Checks

**Work-item checks.** I ran `python3 -m pytest -q --work-item <w>` (with `-n auto` from pytest.ini) at 37a9445 for every green work-item. All pass. Each run also has 1 skipped and 56 subtests passed.

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
| w151 | 146 passed (one more than in review 2: the new @r79 scenario) |
| w152 | 143 passed |
| w153 | 146 passed |
| w154 | 145 passed |
| w155 | 144 passed |
| w157 | 145 passed |
| w158 | 145 passed (one more than in review 2: the new @r79 scenario) |
| w159 | 156 passed |
| w160 | 147 passed |
| w161 | 145 passed |
| w162 | 145 passed |

**`tools check --base f890f2f`** exits 1, with the same 13 ruff errors as review 2. w162 adds none. See O4.

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

**`tools size --limit 300`**: prints nothing.

**`features deprecated`**: three deprecated scenarios.
- migration-tools @r15 and work-queue @r1 were already there at Base.
- work-queue @r9 "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)": its replacement's work-item, w140, is green, and no work-item retires it. This is review 1's M1 and review 2's O5, still open (O5).

**`features bindings`**: "every binding names a scenario".

**Dry-run and real modes**: none on this branch, and w162 adds none. No randomized agreement test is needed.

## Removed and weakened tests

None.

- **In `25f9d50..HEAD`.** I searched `git diff 25f9d50 HEAD -- tests conftest.py features` for removed lines (`^-[^-]`), and found none. The only changes are one new Given, `proposed_fulfilling_missing` (`supervision_rounds_steps.py:115-118`), and one new scenario.
- **In `f890f2f..HEAD`.** Added `pytest.skip`, `mark.skip`, `skipif` or `xfail` under `tests/` or `conftest.py`: 0. Reviews 1 and 2 found no removed or weakened test in their ranges.

## Allowances

- **w162**: its implementer's report gives "none", and the commit agrees: it only adds a step.
- **Earlier rows** (review 1: w121 `run_work` setup, w130 `with_state` setup; review 2: w159, w161): unchanged since then.

## Cannot verify

Nothing a work-item names.

- Review 1's F-obs-1 and F-obs-3 stay checked by reading only. Their code is unchanged.
- w162's red run (made with the scenario copied in uncommitted) is not in the commits. What I verified instead: with the new scenario, the code before 3a307c0 moved the initiative in `round()` before it read the request. Review 2 reproduced R2-F1 on that code.

## Findings

### R3-F1. Important, w151 (c79de72), fix now: a DONE integrate round leaves its stage directory uncommitted, and the next `work run` is refused

**Where:** `scripts/supervise_rounds.py:83-84` (`if kind != "integrate": self.move(...)`), with `start_initiative` at `:86-91`.

**What is wrong:**
- `start_initiative` commits the initiative's move to `started` before the round's session runs.
- The integrate round makes no `move` after it ends, so nothing commits its stage directory. For a gate, apply or formulate round, `move` commits it under r7.
- A round that faults or ends other than DONE is committed by `keep_round`. Only the DONE integrate round is not.

So the round's `brief.md`, `result.json` and `session.json` under `.shop/work/<initiative>/runs/<initiative>/<k>-integrate/` stay untracked.

**Why it matters:**
- This is data left invalid: `.shop/work/` differs from its commit after a run that exited 0.
- Every later `work run` is refused under r46 until the person commits the directory by hand.
- This happens on every successful integrate round, which is the normal path of a request's initiative (r79, r84). The r79 and r84 scenarios do not catch it because none of them checks the tree after a DONE integrate round.

**Reproduced** at HEAD. The probe is the suite's own steps on a scratch feature file, with the supervision Background, then `i1 is proposed and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused`, then `every round ends`, then `work run i1`. What came back:
- `nothing under .shop/work/ is left uncommitted` failed: `?? .shop/work/i1/runs/i1/`
- The second `work run i1` exited 1: `work: .shop/work/i1/runs/i1/1-integrate/brief.md, .shop/work/i1/runs/i1/1-integrate/result.json, .shop/work/i1/runs/i1/1-integrate/session.json under .shop/work are not committed; commit them before work run starts`

w162's research had found the same (notes D3, probe P-d), and w162's plan listed it under Open cases.

**Fix:**
1. When an integrate round ends DONE, commit its stage directory and `log.jsonl` as r7 has a transition do. For example, call `keep_round`'s commit (with its own message) after the merge, or move `start_initiative`'s commit to after the round, keeping r84's order of the log line.
2. Add the r84 (or r79) case below.

**Keep as a test:**

```
@r84
Scenario: an integrate round that ends leaves nothing uncommitted and blocks no later `work run`
  Given i1 is proposed and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
  And every round ends
  When the person runs `work run i1`
  Then i1 is started
  And nothing under .shop/work/ is left uncommitted
  When the person runs `work run i1` a second time
  Then the second `work run` was not refused
```

Every step exists already, in `supervision_rounds_steps.py` and `test_supervision.py`. The probe was `.shop/scratch/i24-requests-and-the-context-loop-branch-review/{probe.feature,test_probe.py}`, which is now deleted.

### R3-F2. Important, w158 and w162, observation: two scenarios hold `proposed` initiatives back from the integrate round, which r79's line does not say, and the person is told nothing

**Where:** `spec/capabilities/supervision.md:26` (r79) against `scripts/supervise_rounds.py:33-38`.

**What is wrong:**
- r79 reads "When an initiative is `proposed`, `work run` shall start a round of the kind `integrate`…", with no condition.
- The code, and the two @r79 scenarios behind it, give no round:
  - when `fulfils` is empty (w158);
  - when `fulfils` names a request the queue does not hold (w162).
- In the second case `work run` exits 0 and says nothing. r10 ("cannot start the delivery … exit with an error, say why") is the line w162's plan meant to apply. Its implementer dropped it because the formulated scenario's `the second \`work run\` was not refused` asserts exit 0. The report says so.
- The `except Refused: pass` also swallows `workqueue.read`'s "is not UTF-8 text" for a request that is held (w162's task review, O1).

**Why it matters:**
- The behaviour stands on scenarios and a delegate's ruling (331acaf), not on the line.
- A mistyped `fulfils` leaves the initiative `proposed` with no word to anyone, until model's `w_stale_intake` warns after 90 days.

This is not a wrong answer by the scenarios, so it is triaged as an observation. It is review 2's O3, now with two cases.

**Fix:**
- Rewrite r79 through integrating-a-proposal as "When an initiative is `proposed` and fulfils a request the queue holds, …".
- Decide whether a missing request is said (for example, a warning on stderr that does not start with `work:`).
- Narrow the `except` to `path_of`'s refusal.

**Reproduction:**
- Read `supervision.md:26` against `features/supervision.feature:857-881`.
- `python3 -m pytest -q --work-item w162` → 145 passed, with exit 0 asserted at `supervision_rounds_steps.py:147`.

### Branch review 2's findings, re-checked

- **R2-F1 (w158 → w162): fixed.**
  - `due()` (`supervise_rounds.py:33-38`) reads the request's accepted lines before anything moves. A request the queue does not hold gives no round, so the initiative stays `proposed`, no branch is made and nothing is left uncommitted.
  - The new @r79 scenario pins all of that, and a second run that is not refused.
  - `due()` and `integrate_lines` (`supervise_brief.py:68`) take the request's id by the same expression. I read both.
- **Review 2's observations O1–O6 and the ones it carried over from review 1** are unchanged by 3a307c0, which touches only `due()`.

## Shape

- **Size limit (CLAUDE.md): met.** `tools size --limit 300` prints nothing. `supervise_rounds.py` is 102 lines and `supervision_rounds_steps.py` is 242.
- **Module map:**
  - `scripts/supervise*.py` (`supervise_rounds.py`, "a capability-proposal's apply and formulate rounds"): w162 keeps the module to its concern, but the row is still stale. The module also runs the gate and integrate rounds (reviews 1 and 2, Minor, observation). Check that would show this complete: the row names every round kind in `AFTER` and `due()`.
  - `scripts/workqueue_request.py` ("the requests of a context"): `supervise_rounds.py` now imports it (`:9`) for `accepted_lines`, as `supervise_brief.py` already did. This is within its row.
- **Shape of w162's change:**
  - `str(fulfils).rsplit("/", 1)[-1]` is now written twice, at `supervise_rounds.py:35` and `supervise_brief.py:68`. Each round reads the request twice.
  - This is Minor, an observation. A helper in `workqueue_request` (for example, `fulfilled(data)` returning the id) would keep the two in agreement. Check that would show it complete: one definition, found by `grep -n 'rsplit("/", 1)\[-1\]' scripts/supervise_*.py`.
- **Code no scenario reaches:** unchanged since review 2.
  - `scripts/measure_read.py:65`: `"/" in ident` (O2).
  - `CONTEXT` at `design_model_check_problems.py:6` (F401).
  - vulture's `notes`.
- **The repository's own `model check`** (Minor, observation, unchanged): `10 violations, 17 warnings, 0 unresolved references, 0 file problems`. Repro: `python3 <Scripts>/model check`.

## Coupling

Unchanged since review 2:
- Claude Code transcripts
- `claude -p --output-format json`
- pytest-bdd internals in `work_items.py`
- Claude Code hooks
- the stand-in's `Question:` line, an internal contract

w162 adds no dependency on another project.

## Observations

- **O1. Minor, w161, `scripts/measure_read.py:57-59`:** a regex `fulfils` reader that differs from the model's frontmatter reader. Repro in review 2, O1.
- **O2. Minor, w161, `scripts/measure_read.py:65`:** `"/" in ident` cannot be true. Repro: reading `:64-65`.
- **O3. Minor, w162, `scripts/supervise_rounds.py:37`:** `except Refused: pass` also skips, without a word, a held request that is not UTF-8. Repro: by reading, `accepted_lines` → `workqueue.read` raises `Refused("… is not UTF-8 text")`, which `due()` swallows (w162 task review O1). Fix: catch only `path_of`'s refusal.
- **O4. Minor, w157, w159, w161, and w156's run record: lint.** These are the 13 ruff hits under Checks. Repro: `python3 <Scripts>/tools check --base f890f2f`. Fix: `ruff check --fix`, and remove the probes `runs/w156/1-research/*.py`.
- **O5. Minor, w140:** the deprecated work-queue @r9 scenario is still there although its replacement's work-item is green. Repro: `python3 <Scripts>/features deprecated`.
- **O6. Minor, w157:** a second answer's commit or push that fails after the first answer was pushed is not exercised. Repro: none; read from `supervise_answers.py:76`.
- **O7. Minor, no work-item: commits that belong to no work-item.** These are e3fbf0b (`features:`, adds one scenario only, under the person's delegation) and 623cbee (branch review 2's record). Repro: `git log --format='%h %s' 25f9d50..HEAD`.
- **O8. Minor, w130/w160 (work-queue r23): the initiative was `done` while it held drafted work-items.**
  - `c887d19 work withdraw: w156 failed -> withdrawn` (02:03) set i24's `initiative.md` to `status: done`.
  - `work add` then drafted w157–w161 in the same minute, and w162 at 02:32, while the initiative stayed `done`.
  - No line says what `work add` does to a `done` initiative, so this is hardening. It holds again at HEAD, since every work-item is green or withdrawn and i24 fulfils no request.
  - Repro: `git log --format='%h %ad %s' --date=format:%H:%M f890f2f..HEAD -- .shop/work/i24-requests-and-the-context-loop/initiative.md`, and `git show 66cfb8d:.shop/work/i24-requests-and-the-context-loop/initiative.md`, which gives `status: done`.
- **O9. Minor, w162 plan Open case D2 (supervision r79):** a held request with no accepted line still gets an integrate round with no lines. No line or scenario chooses. Repro: w162 research P-b and P-c (`runs/w162/1-research/notes.md:21-26`).
- **Carried over from reviews 1 and 2, unchanged:**
  - F-obs-1 (w134, a thread crash exits 0)
  - F-obs-2 (w147, the answer pass runs once a run)
  - F-obs-3 (w124, hooks in worker sessions)
  - F-obs-4 (w153)
  - F-obs-5 (w148)
  - F-obs-6 (supervision r74)

  Their reproductions are in review 1's findings.
