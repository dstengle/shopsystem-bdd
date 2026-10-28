# Branch review 3 of i46

**Verdict: DONE_WITH_CONCERNS.**

- One finding is triaged fix now: F1, Important, w225. Branch review 2 found it, and it is still in the code at HEAD.
  - When a glossary-proposal's gate round gives no question, `work run` writes r117's approval question on it. No Behaviour line asks for that.
  - w227 was drafted to fix it, and was then withdrawn under reading A, changing no file.
  - The line that would ask for the behaviour is q36 line 1, which is still `status: open`. The line has not been written first, and the code has not been removed.
- No finding is Critical.
- Every check has a run in the brief.

## Range and work-items

- Range: `134745663cfa0a109b8564370c2464ef9ee9a7d5..c52906d9fc254217e2d3785aa1f9b33f123bd122` (i46, "The glossary as a target of spec work in its own right", fulfils q30).
- Work-items:
  - w219 (spec-integration r54 r55): green.
  - w220 (fix of branch review 1): withdrawn, with no code commit.
  - w221 (design-model-check r122 r123 r124): green.
  - w222 (supervision r171 r172): green.
  - w223 (supervision r162 r163): green.
  - w224 (supervision r159 r168): green.
  - w225 (supervision r161 r164-r167 r169 r170): green.
  - w226 (retires the deprecated r77, r92 and r104 scenarios): green.
  - w227 (fix of branch review 2): withdrawn, changing no file.
- What is new since branch review 2 (at 3779411):
  - 3a597af0, the branch review 2 commit;
  - w227's add, researched, awaiting-answer, answer and withdraw (fe6795e1..d64c855e);
  - c52906d9, a work note.
- None of these changes `scripts/`, `tests/`, `features/`, `agents/`, `spec/` or `CLAUDE.md`. The change the brief gives, minus `.shop/`, is the same as branch review 2's. I checked this by reading the whole change against branch review 2's findings and w227's plan §2 (reading A: no file).
- Limit: the brief gives the change for the whole range, not for each commit. I read which commit wrote what from the commit subjects and the reports.

## Suite

`Suite: 1066 passed, 0 failed at c52906d in 33.80 s`

- The run also gave 1 skipped, 11 xfailed (w212's parked requests scenarios, "accepted by w212, neither green nor withdrawn") and 56 subtests passed.
- Command: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w219 --whole-suite`, exit 0.
- Parallel: yes (`-n auto`, xdist, "bringing up nodes").
- In-process: no. The step definitions start `scripts/work` as a subprocess (`tests/scenarios/test_supervision.py`, `spec_integration_steps.py`, as branch review 2 found). The suite is under 60 s, so this is no finding.
- Dry-run against real mode: the system has no dry-run mode of an operation. The only `--dry-run` in `scripts/` is `git push --dry-run`, a probe of the remote (`supervise_faults.py:71`, `supervise_review.py:55`). There is no agreement test to give.

## Checks

Every run was at c52906d.

**Each work-item's scenarios** (`pytest -q -n auto -p work_items --work-item <w>`). Each exited 0, with 1 skipped and 56 subtests passed:

| Work-item | Passed | Time |
|---|---|---|
| w219 | 183 | 6.59 s |
| w220 (withdrawn) | 183 | 4.51 s |
| w221 | 212 | 4.52 s |
| w222 | 183 | 4.40 s |
| w223 | 185 | 4.46 s |
| w224 | 183 | 4.41 s |
| w225 | 189 | 4.38 s |
| w226 | 183 | 4.33 s |
| w227 (withdrawn) | 189 | 4.33 s |

No work-item names a `check:`.

**`tools check --base 134745663`: exit 1.**

- **ruff**: 29 errors.
  - From this branch:
    - `tests/scenarios/design_model_check_problems.py:6` F401 `I1`, `CONTEXT` (w221);
    - `tests/scenarios/design_model_check_work.py:6` F401 `THING` (w221);
    - `tests/scenarios/supervision_integrate_steps.py:81` RUF059 `commit` (w222);
    - `tests/scenarios/supervision_proposal_steps.py:137` RUF100 (w222/w225);
    - `tests/scenarios/test_design_model_check.py:7` I001 (w221 added an import to the block);
    - fourteen SIM115/I001 errors in `.shop/work/i46/runs/{design-model-check,supervision}/*-formulate/splice.py` (formulate rounds, no work-item; F10).
  - Already there, on lines the branch did not change: `scripts/supervise_change.py:91,118` B023, `scripts/workqueue.py:248` I001, `supervision_proposal_steps.py:102` RUF100, `supervision_reintegrate_steps.py:13,174`, and `tests/scripts/test_supervise_answers.py:9,10` RUF100.
- **vulture**: clean.
- **import-linter**: "the project states no import contracts". It does not say `missing`.

**`tools size`**: exit 0, printed nothing. No file is over 300 lines.

**`features deprecated`**: exit 0, 13 scenarios.
- Two are this initiative's. Formulate commit edf03019 deprecated them, and they have no replacement (F7):
  - @r77 "under a delegation, a work-item with two questions …";
  - @r92 "the change lists of two initiatives …".
- The other 11 were there before the branch: v18; the supervision worker, implementer and researcher scenarios, and formulate ×2; work-queue show ×2 and status ×3.
- No deprecated scenario is left whose replacement's work-item is green.

**`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched for: deleted `def`s, dropped Examples rows or parametrize cases, removed or loosened `assert`s, added skip or xfail, Thens rewritten or widened, and renames.

1. **The five @r27 scenarios** (`features/design-model-check.feature`), removed by w221.
   - They proved the shape of work files, which requirements need a scenario before a work-item accepts them, and statuses in the lifecycle.
   - They are listed under w221's Retires and in w221's plan. Formulate a0295498 deprecated them, and @r124 replaces them, so this is a retirement.
   - Two cases are in no @r124 row (F8): a work-item status `loved` outside its lifecycle, and a withdrawn request being no file problem.
2. **Step definitions `work_item_accepting` and `work_item_with_status_accepting`** (`design_model_check_problems.py`), removed by w221. Only the retired @r27 scenarios used them. `malformed_work` moved to `design_model_check_work.py`, and lost its `loved` branch with the dropped row.
3. **The three deprecated scenarios @r77 "… that <reply>", @r92 "… with what it adds …" and @r104 "… lines and terms …"**, removed by w226 under its Retires, each with its replacement green (r163, r159, r168).
4. **`spec_integration_steps.py` `drafts_glossary_change`**: `assert not (repo / ".shop/work/i1/glossary.md").exists()` removed by w222.
   - It proved that the r54 integrate round wrote no glossary-proposal (w219's interim stance).
   - w222's plan §4 says "None", so the plan does not list it. The allowance row holds (Allowances).
5. **Widened, not weakened**:
   - `proposals_written` and `gate_names_its_ids` (w224) got an optional term clause.
   - These steps (w225) went from `p1` to `[pg]1`: `gate_started`, `apply_started`, `approved_after_apply`/`position`, `proposal_awaiting`, `round_given_drafts`, `written_from_round`, `no_formulate_for_p1`, `gate_gives_question`.
   - The p1 cases assert the same as before (`rounds(..., name="p1")` defaults to p1).

No skip or xfail was added. `tests/scripts/test_supervise_answers.py` only gains a test.

## Allowances

- **w222 3-implement and 4-implement, `drafts_glossary_change`, interim: holds.** It was first committed in 085527d8 (w219), after Base. It now gives way to w222's D1/D2, which have `work run` write `glossary.md`, and r171's scenario asserts that.
- **w225 7-implement, `started_glossary_only`, setup: holds.** The change adds one write of `ledger.md`, with no assert, expected value or case changed.
- **w225 7-implement, `glossary_drafted`, comment only: holds.** The `noqa` was removed from the `listed` lambda.
- **"none" rows hold**: w219 3, w221 3/5, w223 3, w224 3, w225 3 and w226 3-implement. w221 4 and w225 4-implement made no commit.

## Cannot verify

None. Every check has a run in the brief.

## Findings

### F1. Important, w225, fix now: an approval question is written on a glossary-proposal, which no line asks for

- **Where**: `scripts/supervise_rounds.py:159-161`. w225's routing (`scripts/supervise_glossary.py:13`, `route` at `:26`, called from `supervise_rounds.py:57-60`) brings glossary-proposals to this branch.
- **What is wrong**: when a glossary-proposal's gate round gives no question, `work run` writes "Are the lines of g… approved as drafted? …" under its `## Questions`. r117 asks for this only for a capability-proposal.
  - q36 line 1, which would ask for it, is still `status: open`.
  - w227, drafted to fix it, was withdrawn under reading A ("keep … until q36 line 1 is integrated"), changing no file.
- **Why it matters**: it is observable behaviour on the person's queue (a question they must answer) that reaches code with no line behind it.
- **Fix**: integrate and formulate q36 line 1 (through integrating-a-proposal), so the line is written first. Or take the r117 branch only for `kind: capability-proposal`, and route a zero-question glossary-proposal under r165.

### F2. Important, w222, observation: a started initiative with only a glossary-proposal gets no integrate round, against r93's text

- **Where**: `scripts/supervise_rounds.py:49`.
- **What is wrong**: r93 names "neither a capability-proposal nor a work-item". The code also requires no glossary-proposal.
- **Why it matters**: the code serves r164 and r161; without the change, `due()` would integrate again. It was accepted under the delegation, and q35 is `open`.
- **Fix**: integrate q35, retiring r93.

### F3. Important, w222, observation: a later integrate round overwrites `glossary.md` whole

- **Where**: `scripts/supervise_change.py:133-139`.
- **What is wrong**: `write_text` writes a `drafted` proposal holding only that round's terms. An `awaiting-answer` proposal loses the person's Questions and Answers, and an `approved` one goes back to its gate.
- **Fix**: merge into an existing glossary-proposal or rewrite it in place, as `proposal_for`/`merge_lists` do for capabilities.
- Test that would show it (not run): i1's `glossary.md` awaiting-answer with an answer, and an r150 re-integrate round of p1 giving `{"glossary": true, "adds": ["term/x"]}`. Then g1 keeps its Answers and status.

### F4. Important, w223, observation: "names a term of the glossary" matches any whole-word use

- **Where**: `scripts/supervise_glossary.py:90-94`.
- **What is wrong**: the Glossary holds common words: run, check, status, suite, scenario, request, round, answer, result, review. Every glossary-proposal is named `glossary`. So most questions are left for the person, and r163's delegation sessions are rarely reached.
- **Reproduction**: by reading. `.shop/work/i46/w221.md:22` ("… the whole suite pass …") matches on "suite".
- **Fix**: a question to the person on r162's reading: a question *about* a term, or one that *uses* it.

### F5. Important, w223, observation: after a question is left for the person, later questions still go to sessions whose answers are discarded

- **Where**: `scripts/supervise_answers.py:75-78`.
- **What is wrong**: `ask()` is called before the `left` check, so its answer is thrown away. r78 says the answer is written.
- **Fix**: skip `ask()` once `left` is set, or write answers by question.
- Test that would show it (not run): w1 with "Does it write the ledger?" then "Which module owns the log?", the Glossary holding "ledger", and the full delegation. Then no second delegation-answerer session is started, or its answer is written.

### F6. Important, w227 (commit d64c855e; pre-existing work-queue r23), observation: i46 is `done` at HEAD before this review, with F1 open

- **Where**: `.shop/work/i46/initiative.md:4` reads `status: done`. No `log.jsonl` line moves i46 to done; the only line for i46 is `proposed -> started`.
- **What is wrong**: `work withdraw w227` made every work-item green or withdrawn, so `workqueue_done.becomes` (`scripts/workqueue_done.py:52-59`, used by `work withdraw`) set the initiative done.
  - r105's condition, "whose kept branch review lists nothing to fix now", does not hold: branch review 2 lists F1 as fix now.
  - The move is not logged.
- **Why it matters**: the queue shows i46 finished while a fix-now finding is open. This code is outside the branch's change, so it is triaged an observation.
- **Fix**: a work-queue line making `work withdraw`'s done wait for the kept branch review (or leaving the done to `work run`'s r105), and logging the move.

### F7. Minor, none (formulate edf03019), observation: two deprecated-for-removal scenarios of retired ids have no replacement

@r77 "a work-item with two questions …" and @r92 "two initiatives that name the same capability …" still run. What they pin is in no live scenario. Retire them through a work-item, or write lines that keep what they pin.

### F8. Minor, none (formulate a0295498), observation: two cases of the retired @r27 scenarios are in no @r124 row

The two cases are a work-item status outside its lifecycle (`loved`) and a withdrawn request being no file problem. r124's line still names both. Fix: add both rows to the @r124 Examples. Check: `pytest --work-item w221` runs both.

### F9. Minor, none, drop: commits that belong to no work-item

53 commits, all the workflow's own:
- `work note`, `work:`, `work answer` and `work request` q32-q36;
- `spec:` 92e82b4e, f19a7713;
- formulate/features: a0295498, a7147684, edf03019, d6c99676, e4159920;
- the merge 441c5954;
- the restore 7d0e08ca;
- branch reviews 44d15c56 and 3a597af0.

By their subjects and the reports, none of them changes `scripts/` or `tests/`.

### F10. Minor, none (formulate rounds), observation: round helper scripts are committed as tracked Python

- **Where**: `.shop/work/i46/runs/{design-model-check,supervision}/*-formulate/splice.py`.
- **What is wrong**: ruff lints them (14 errors).
- **Fix**: keep them under `.shop/scratch/`, or exclude `.shop/` from ruff.

### F11. Minor, w221, w222, w225, drop: ruff errors the branch adds

See Checks. `ruff --fix` handles four of them; rename `commit` to `_` for the RUF059.

### F12. Minor, w225, observation: the module-map row for `scripts/supervise_glossary.py` is incomplete

The row does not name `ROUTES`, `route` and `statuses` (r164-r170) or `glossary_only_done` (r161). Fix: extend the row.

## Shape

- **Size**: met.
- **Module map**:
  - `supervise_glossary.py` has a row (incomplete, F12).
  - The `supervise_change.py` row is widened. Met.
  - `model_work.py`/`model.lp` fall under `model*`. Met.
  - `supervise.py`, `supervise_rounds.py`, `supervise_brief.py`, `supervise_answers.py`, `supervise_done.py` and `workqueue.py` are covered by their rows. Met.
  - `tests/scenarios/design_model_check_work.py` is a step module for one concern. Met.
  - `tests/scripts/test_supervise_answers.py` tests a script no scenario drives. Met.
- **Steps no scenario reaches**: the optional `and the term "ledger"` branch of `proposals_written` (`supervision_integrate_steps.py`) and of `gate_names_its_ids` (`supervision_proposal_steps.py`). Their only users were the retired @r92 and @r104 scenarios. Check that would show the refactor complete: the regex group is gone and `pytest --work-item w224` stays green.
- **Docstrings citing retired ids** (r27, r92, r104, r77): polish, dropped.

## Coupling

- `git show HEAD:spec/index.md` and `git status --porcelain -- spec/index.md` (`supervise_glossary.py:71-72`) are published git interfaces, so they are stable.
- The steps use `pytest_bdd.parsers.re`, `given` and `then`, pytest-bdd's published API.
- Already there: pytest-bdd's `compat.py:28` and `FixtureDef` trip `PytestRemovedIn10Warning`, so pytest 10 would break the suite through pytest-bdd. Pin pytest below 10, or upgrade pytest-bdd.
- `@deprecated` is an unregistered mark, which would fail under `--strict-markers`. Register it.
- This branch relies on no upstream project.

## Observations

- F1: `supervise_rounds.py:159-161` and `q36.md:6` `status: open`; `w227.md:5` `status: withdrawn`.
- F2: `supervise_rounds.py:49` against r93's text; q35 `open`.
- F3: `supervise_change.py:134-139`, `write_text` with no read. Test not run.
- F4: `names_one` regex over `terms_of(root)` flags `w221.md:22` on "suite". By reading.
- F5: `supervise_answers.py:75` calls `self.ask` before the `left` check at `:76`. Test not run.
- F6: `initiative.md:4` `status: done`; `log.jsonl` has only the `proposed -> started` line for i46.
- A glossary-only initiative with an undelivered raised request is set done (`supervise_done.py:28-37` checks only `glossary_only_done`; r161 is silent). Not run.
- An abandoned glossary-only initiative run by name is set done (`supervise_done.py` guards only `before == "done"`). Not run.
- `workqueue.move` (`workqueue.py:155`) accepts work-item statuses and `formulated` for a glossary-proposal, which r124 then reports as a file problem. Not run.
- A change-list entry with both `"glossary": true` and `"capability"` is read as a capability entry, its `term/` ids landing in a capability-proposal (`supervise_change.py:27`). No client sends it.
- A capability named `glossary` would collide with `glossary.md` (`supervise_change.py:122,134`).
