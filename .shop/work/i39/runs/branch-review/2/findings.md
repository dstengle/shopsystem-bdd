# Branch review 2 of i39 (Requests go through one shared tool)

**Verdict: DONE_WITH_CONCERNS.** Two findings are triaged fix now:

1. The defect of branch review 1's finding 1 is still in the code. In w204 (i41), `scripts/supervise_change.py:91-99` `write_proposals` still overwrites the lists of any other proposal that a change list names (data lost). The coordinator restored the data by hand in `2ae8e313` and recorded it as observation 2026-10-27-redraft-overwrites-other-proposal, but the code is unchanged.
2. w205's `work list --json` gives each request's `turn`, which no line asks `work list` for (code no line asks for).

One check could not be verified, carried from review 1: whether a real `claude -p` integrate round can read the upstream's spec outside its worktree (w202).

Otherwise w205 does what r34-r39 and the reading-A ruling ask. Its fix of review F1 holds. No change under `features/` comes from i39's work-items, and no test was removed or weakened. The restoration in `2ae8e313` works: with `--work-item w205 --whole-suite`, the 14 requests scenarios are xfailed again.

## Range and work-items

- **Range:** `b4c4ad5e..e4c0b40f` on `main`.
  - Branch review 1 covered the range up to `d3079697` (`.shop/work/i39/runs/branch-review/1/findings.md`). I re-ran every check on the whole range.
  - I read in full only the code that changed after `d3079697`: w205 and `2ae8e313`. I confirmed that no commit after `d3079697` touches w202's files.
- **w202** (spec-integration#r44, `green`): commits `6e3c4f04` and `fe844bb3`. Unchanged since review 1.
- **w205** (work-queue#r34-r39, `green`). Its commits are those between `work: w205 ready -> claimed` and `work: w205 claimed -> done`, less `work run`'s own commits:
  - `a033c460` "work list and work show <target> (work-queue r34-r39)". The implementer's `bc517d85`, rebased onto main; it touches 7 files.
  - `bf231ddc` "work show refuses a file that is not a work-item, naming its kind (review F1)".
- **i39's spec rounds since review 1:**
  - `9bc3be06`: apply, work-queue r34-r39 and decision 0072.
  - `fefe7407`: formulate work-queue.
- **A commit that belongs to no work-item and no round:** `2ae8e313`, made by hand. It restores the adds and removes of `.shop/work/i39/requests.md` and records an observation. See finding 4.
- The range also holds i40 (w203) and i41 (w204), as review 1 described. Each has its own branch review.

## Suite

`Suite: 962 passed, 16 failed at e4c0b40f in 25.55 s` (`python3 -m pytest -q -p no:cacheprovider`; wall time 25.9 s).

- **Parallel:** yes, `-n auto` from `pytest.ini`.
- **In-process:** no. The steps drive `scripts/work` as a subprocess. The suite runs under 60 s, so this is not a finding.
- **The 16 failures** are all `StepDefinitionNotFoundError` on scenarios that are formulated but have no work-item yet:
  - 14 requests scenarios (r28, r29, r30, r31, r32, r40, r42, r44, r45)
  - design-model-check @r120
  - supervision @r135
- **With `-p work_items --work-item w205 --whole-suite`:** `962 passed, 1 skipped, 16 xfailed in 27.92s`. Nothing fails. The restoration in `2ae8e313` brought back the xfail of the 14 requests scenarios.

## Checks

- **w205's check** (`python3 -m pytest -q -p no:cacheprovider --work-item w205`): 151 passed, 1 skipped, 56 subtests passed in 6.13 s.
- **w205's whole-suite check:** as above, 0 failed and 16 xfailed.
- **w202's check** (`--work-item w202`): 145 passed, 1 skipped, 56 subtests passed in 3.87 s.
- **`tools check --base b4c4ad5e`** exited 1:
  - **ruff:** 25 errors.
    - **New in w205:** `tests/scenarios/work_queue_list_steps.py:79` RUF015 (finding 5).
    - **In a file w205 touched, from before base:** `tests/scenarios/test_work_queue.py:7` I001. The out-of-order import is already at `b4c4ad5e`.
    - **w204 (i41), as in review 1:** `scripts/supervise_change.py:96` B023; `tests/scenarios/supervision_reintegrate_steps.py:13` F401 and `:137` FURB167; `tests/scenarios/test_supervision.py:14` I001.
    - **Round helper scripts committed under `.shop/work/*/runs/`** (review 1's finding 3, which has grown):
      - `i39/runs/requests/3-formulate/splice.py`
      - `i39/runs/work-queue/6-gate/gen.py`
      - `i39/runs/work-queue/8-apply/apply.py` (new, committed by `e72c9871`)
      - `i41/runs/supervision/{2-apply,3-formulate}/splice.py`
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:77`, unused `notes`. The line is already at `b4c4ad5e`; it is reported now because w205 touched the file.
  - **import-linter:** "the project states no import contracts". It is not `missing`.
- **`tools size --limit 300`:** printed nothing. No tracked Python file is over 300 lines.
- **`features deprecated`:** 14 deprecated scenarios.
  - Replacements of i39's lines that have no `green` work-item yet: design-model-check r115 (for r120), requests r1 (for r44), requests r3 (for r45).
  - Deprecated for removal: design-model-check r117, 5 supervision scenarios, and work-queue r3, r11, r16, r17 and r18.
  - The work-queue ones are deprecated for removal by decision 0072. w205 retires none of them (plan D1, D2), and all of them still pass.
  - None has a replacement with a `green` work-item, so none is due for retirement.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. No operation the branch touches has a dry-run mode. The only `--dry-run` uses are `git push --dry-run` probes, which the branch did not touch.

## Removed and weakened tests

None by i39's work-items.

**What I searched for:**
- In `git diff b4c4ad5e HEAD -- tests/`: every removed line, and every added `skip`, `xfail` or `parametrize`. No skip, xfail or parametrize was added.
- In `features/`: removed `@r` tags and `Scenario` lines.

**The removed lines are:**
- **w204 (i41):** two step patterns, widened. Covered in review 1.
- **w205, `tests/scenarios/work_queue_status_steps.py`:**
  - `open_with_proposal`: the fixed text "neither done nor abandoned" became `{state}`. The setup is the same for every scenario that uses the step, and the step has no assert. See observation O4.
  - `with_state`: the parse became a regex with a `findall`. It now also takes "work-items" and a question clause. It has no assert, and every feature line that used it writes the same files.
- **w205, `tests/scenarios/work_queue_withdraw_steps.py:58`:** the `gives` step's pattern was narrowed to `it gives \S+ in \S+ with .+` so that it is no longer ambiguous. Its body and assert are unchanged, and the r11 line it served still matches.
- **Scenario lines in `features/`:** each removed `@rN` tag line was re-tagged `@rN @deprecated` by a formulate round (`e27313e1`, `bc58e42e`, `fefe7407`).
  - The only scenarios removed are r80, r114 and r71 of supervision. w204 (i41) removed them; they were deprecated and listed under its Retires.

## Allowances

- **w205 `4-implement/report.md`:** "none", with the step changes named. This holds: neither step file's diff changes an `assert`, an expected value or a parametrize case.
- **w205 `5-implement/report.md`:** "none beyond what bc517d85 already holds (setup in work_queue_status_steps.py and work_queue_withdraw_steps.py)". Read as `setup` rows, both hold for the same reason.
- **w205 `7-implement/report.md`:** "none". This holds: `bf231ddc` touches only `scripts/workqueue_list.py`.
- **w202:** both reports say "none", and that holds (review 1).

## Cannot verify

- **(w202, carried from review 1)** Whether a real integrate round, `claude -p` with `Read` and no `--add-dir` (`supervise_worker.py`), can read the upstream's `spec/` at a path outside its worktree.
  - Only a real session would show it, and I do not start one. The scenario's stand-in session reads nothing.

## Findings

### 1. Important, fix now (data lost): `write_proposals` still rewrites another proposal's applied lists (w204, i41; carried from review 1)

- **Where:** `scripts/supervise_change.py:91-99`.
- **What is wrong:**
  - For each capability a change list names, the function rewrites the lists of whatever proposal the initiative holds for that capability, through `rewrite_lists(held.stem, [one])`.
  - Supervision r142 and r148 ask for that only for the proposal that is being drafted anew.
- **What has changed since review 1:** `2ae8e313` restored the data of `.shop/work/i39/requests.md` by hand, and observation 2026-10-27-redraft-overwrites-other-proposal records the defect. No commit has changed the code (`git log d3079697..HEAD -- scripts/supervise_change.py` is empty).
- **Why it matters:** the next re-integrate round whose change list names a second capability with an applied proposal loses that proposal's `adds` and `removes` again. That puts its formulated scenarios back to failing in every `--whole-suite` run, and their lines never get a work-item.
- **Fix:**
  1. Merge (union) the round's ids into a held proposal that is not the one the round was started for, and rewrite in place only that one.
  2. Add a scenario: a re-integrate round for p1 whose change list also names p2's capability leaves p2's applied ids in its lists.
- **Reproduction:** `git show 2862e7bf -- .shop/work/i39/requests.md` shows the overwrite. `sed -n 85,99p scripts/supervise_change.py` shows the unchanged code.

### 2. Important, fix now (code no line asks for): `work list --json` gives each request's `turn` (w205)

- **Where:** `scripts/workqueue_list.py:42`.
- **What is wrong:**
  - `"requests": [{"request": n, "status": s, "turn": t} ...]`. r34 and r35 ask for each request "with its status", and r35's scenario pins "and nothing besides".
  - The request's turn is asked for only by requests#r13, and only of `work show`.
  - The text form of `work list` does not print the turn (`:51`), so the two forms disagree.
- **Why it matters:** behaviour reaches code only through a line. A script reading `list --json` will come to rely on a key that no line keeps.
- **Fix:** drop `"turn"` from `list --json`. Alternatively, write a line for it first, through integrating-a-proposal. Decision 0072 moves the listing of requests to `work list`, and the gate's answer of 2026-10-27 (ledger) retires r34 for r40 (`work list` without requests), so a line is unlikely.
- **Reproduction:** with a request q1 `accepted` under `.shop/work/requests/`, `work list --json` gave `"requests": [{"request": "q1", "status": "accepted", "turn": null}]`.

### 3. Minor, observation: `work list` crashes on a malformed `raised.jsonl` line (w205)

- **Where:** `scripts/workqueue_list.py:31-32`.
- **What is wrong:** with a line that lacks `status`, `work list` printed two initiative lines and then `KeyError: 'status'` (exit 1, traceback). With a line `not json`, it raised `JSONDecodeError`. The right answer is a refusal under r7, naming the file and the line.
- **Why it is an observation:** no command writes `raised.jsonl` yet (plan §5), so no client sends this input today.
- **Fix:** catch `ValueError` and `KeyError` and raise `Refused("<path> line <n> is not a raised request")`.
- This was the w205 review's F2, and it is unchanged.

### 4. Minor, observation: a commit made by hand outside any work-item or round (no work-item)

- **What:** `2ae8e313` changed `.shop/work/i39/requests.md`'s `adds` and `removes` by hand and recorded an observation.
- **Why it matters:** it is the repair of finding 1's data. Its new lists are exactly the union review 1 asked for, and the whole-suite run now xfails the 14 requests scenarios. Nothing is wrong in it, but no `work` command made the change.
- **Fix:** none needed now.

### 5. Minor, drop: RUF015 in w205's steps

- **Where:** `tests/scenarios/work_queue_list_steps.py:79`, `[...][0]`, where ruff prefers `next(...)`.
- **Why drop:** it is polish. It is cheap, but it changes no behaviour.

## Shape

- **CLAUDE.md, size limit 300:** met. `scripts/workqueue_list.py` is 78 lines, `tests/scenarios/work_queue_list_steps.py` 80, and `tools size` printed nothing.
- **Module map, "A new concern gets a new module and a row":** met. `scripts/workqueue_list.py` is a new module, and CLAUDE.md has its row: "`work list` and `work show <target>` … the record of raised requests (`raised.jsonl`)".
- **`scripts/work` row:** met. `scripts/work:31-37` only dispatches to `workqueue_list`, and `:121-125` holds the argument parsing.
- **`scripts/workqueue_status.py` row ("`work status`"):** w205 reuses `workqueue_status.status`, `section` and `natural` for `show <initiative>` (`workqueue_list.py:21,64,77`).
  - Once decision 0072's retirement of `work status` is built, this module's concern becomes `work show <initiative>`, and its row should say so.
  - That is an observation for the work-item that retires `status`. A check that shows it complete: `grep -n "work status" CLAUDE.md` finds no row.
- **`tests/scenarios/` row ("one `<capability>_*_steps.py` module a concern"):** met for w205. `work_queue_list_steps.py` holds `list` and `show <target>`.
  - Carried from review 1: `spec_integration_steps.py` holds two concerns, r44 and r45 (i40). Observation: split it. A check that shows it complete: `ls tests/scenarios/spec_integration*_steps.py` lists two modules.
- **Reachability:**
  - Every step in `work_queue_list_steps.py` is reached by r34-r39.
  - The no-target `show` path (`scripts/work:38-45`) is still reached by requests#r13 and the deprecated r3 and r11 scenarios. It goes dead when those are retired.
  - Vulture's `notes` hit is older than base.
- **Behaviour against the lines:**
  - r34: holds, ended initiatives included.
  - r35: holds, apart from finding 2.
  - r36: holds; it reuses `status`.
  - r37: holds. In the probe, `show w1` printed `work-item i1/w1 awaiting-answer` and its open question.
  - r38: holds for an initiative and for a work-item.
  - r39: holds under reading A. The probe shows that the last line of a given (upstream, request) pair decides its status, and that a `delivered` entry drops its waiting line.
  - r7:
    - `show q1` is refused, naming its kind.
    - `show ../i1` is refused: "the target ../i1 is not a name".
    - `show i9` is refused: "there is no work-item i9".
    - A work-item id in two initiatives is refused: "more than one work-item w2".
    - Nothing contradicts work-queue's Purpose: `list` and `show` only read.
- **Code no line asks for (w205):** finding 2. The rest serves a line:
  - the waiting line's `(in ctx-up, accepted)`: r39
  - the `question:` lines: r37
  - the kind refusal: r7, ruled
  - the kept no-target `show`: requests#r13

## Coupling

- **`raised.jsonl`, between w205 and the work that will write it:**
  - `work list` relies on a record that nothing writes yet. The writers would be requests#r29 `--raised-for` and supervision#r135, both still xfail.
  - Its format is given only in `workqueue_list.py`'s docstring and in a test Given: one JSON object a line with `upstream`, `request`, `initiative` and `status`, the last line of a request winning. No capability's Implementation gives it.
  - If the writer's work-item writes another shape or place, r39 stays silently empty, or crashes (finding 3).
  - What would make it stable: state the record's form in work-queue's (or requests') Implementation section, and have the writer's scenario then run `work list`.
- **The gate's answers not applied** (ledger, apply round 8): r48 (`work show <request>`) and the retirement of r34 for r40 (`work list` without requests) are carried as an internal request after i39. When r40 lands, w205's request lines in `list` (`workqueue_list.py:41-42,50-51`) go, and finding 2 goes with them.
- **Carried from review 1, unchanged:**
  - the upstream's spec is read from a working-tree path, not a pinned revision (w202);
  - Claude Code's `-p` read scope (w202);
  - pytest-bdd's private `__scenario__` (`work_items.py`), and the 560 `PytestRemovedIn10Warning`s.

## Observations

- **O1 (w205): open questions are counted by position.** A work-item with questions "first?" and "second?" and one answer that answers the second gave `question: second?` as its open question. Questions and answers are counted by position, as `workqueue_status.py:47` already does.
  - Reproduction: write w1 with `## Questions` holding `- first?` and `- second?`, and `## Answers` holding one line, then run `work show w1`.
  - Same convention as `work status`; not new.
- **O2 (w205): a wrongly worded refusal.** A work-item file with no `kind` gives the refusal `w5 is a None, not a work-item …`.
  - Reproduction: write `.shop/work/i2/w5.md` with frontmatter `id` and `status` only, then run `work show w5`.
  - No such file exists in the repository.
- **O3 (w205): `list --json` does not carry r39's waiting.** The lines leave this open (w205 review F3).
  - Reproduction: write `raised.jsonl` with an `accepted` entry, then run `work list --json`. There is no waiting key.
- **O4 (w205): a step ignores its parameter.** `open_with_proposal` (`work_queue_status_steps.py:14-19`) takes `{state}` and ignores it; it always writes `started`.
  - It is harmless today: every use means started.
- **O5 (carried from review 1):**
  - Round helper scripts committed under `.shop/work/*/runs/` fail ruff. A third one has been added since review 1: `i39/runs/work-queue/8-apply/apply.py`.
  - Fix: exclude `.shop/work/**/runs/` in the ruff configuration, or have rounds write their helpers in `.shop/scratch/`. A check that shows it complete: `tools check` prints no `.shop/` row.

The probe I used for findings 2 and 3 and observations O1 and O2 was a pytest file in `.shop/scratch/i39-branch-review/`. It built a git-initialised `tmp_path` with i1 (started), i2 (done), w1-w3, request q1 and an `i1/raised.jsonl`, and ran `scripts/work list`, `list --json`, `show w1 [--json]`, `show q1`, `show ../i1`, `show i9` and `show w2` (with w2 in two initiatives), and then `list` with a `raised.jsonl` line lacking `status`, `list` with a line that is not JSON, and `show w5` (no `kind`). The scratch directory is deleted.

Keep as a test (`tests/scripts/test_workqueue_list.py`), once r7's refusal of a malformed record is asked for: write `.shop/work/i1/raised.jsonl` holding `{"upstream": "u", "request": "q2"}`, run `work list`, and assert that the exit is non-zero with a message naming `raised.jsonl` and line 1, and no traceback.
