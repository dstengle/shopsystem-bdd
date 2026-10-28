# Branch review of i46

**Verdict: DONE_WITH_CONCERNS.** One finding is triaged fix now (F1, Important, w225). Through w225's routing, `work run` writes r117's approval question on a glossary-proposal whose gate round gives none. No Behaviour line asks for that. The line that would ask for it is q36 line 1, which is still `open`. No finding is Critical. Every check was given a run and is reported below.

## Range and work-items

- Range: `134745663cfa0a109b8564370c2464ef9ee9a7d5..3779411dd590407e8e3f84075b2725716df68f69` (initiative i46, "The glossary as a target of spec work in its own right", fulfils q30).
- Work-items:
  - w219 (spec-integration r54 r55): green.
  - w220 (fix of branch review 1): withdrawn, with no commit of code.
  - w221 (design-model-check r122 r123 r124): green.
  - w222 (supervision r171 r172): green.
  - w223 (supervision r162 r163): green.
  - w224 (supervision r159 r168): green.
  - w225 (supervision r161 r164-r167 r169 r170): green.
  - w226 (retires the deprecated r77, r92 and r104 scenarios): green.
- Commits with no work-item: see F9.
- Limit of this review: the brief gives the change of the whole range, not each commit's files. Which commit wrote which part of `features/` is read from the commit subjects and the implementers' reports, and checked against the whole change. It was not checked commit by commit.

## Suite

`Suite: 1066 passed, 0 failed at 3779411 in 33.64 s`

- The run also gave 1 skipped, 11 xfailed (w212's parked requests scenarios, "accepted by w212, neither green nor withdrawn") and 56 subtests passed.
- Command: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w219 --whole-suite`, exit 0.
- It runs in parallel (`-n auto`, xdist).
- It does not drive the entry point in-process: `tests/scenarios/test_supervision.py:79` and `tests/scenarios/spec_integration_steps.py:177` start `scripts/work` as a subprocess.
- At 33.64 s it is under 60 s, so this is no finding.
- Dry-run against real mode: the system has no dry-run mode of an operation. The only `--dry-run` in `scripts/` is `git push --dry-run`, used as a probe of the remote (`supervise_faults.py:71`, `supervise_review.py:55`). There is no agreement test to give.

## Checks

Every run was at 3779411.

**Each work-item's scenarios** (`python3 -m pytest -q -n auto -p work_items --work-item <w>`). Each exited 0, with 1 skipped and 56 subtests passed:

| Work-item | Passed | Time |
|---|---|---|
| w219 | 183 | 6.54 s |
| w220 (withdrawn) | 183 | 4.45 s |
| w221 | 212 | 4.42 s |
| w222 | 183 | 4.52 s |
| w223 | 185 | 4.46 s |
| w224 | 183 | 4.43 s |
| w225 | 189 | 4.41 s |
| w226 | 183 | 4.31 s |

No work-item names a `check:`.

**`tools check --base 134745663`: exit 1.**

- **ruff**: 29 errors. Those that come from this branch:
  - `tests/scenarios/design_model_check_problems.py:6` F401, `I1` unused (w221). Its last use, `malformed_work`, moved to `design_model_check_work.py`. The F401 on `CONTEXT` on the same line is not explained by the removed code.
  - `tests/scenarios/design_model_check_work.py:6` F401, `THING` unused (w221, new file).
  - `tests/scenarios/supervision_integrate_steps.py:81` RUF059, `commit` unused in `glossary_proposal_written` (w222).
  - `tests/scenarios/supervision_proposal_steps.py:137` RUF100, unused `# noqa: E731` on the `bullets` lambda of `glossary_proposal_answered` (w222's Given, widened by w225).
  - Fourteen errors in `.shop/work/i46/runs/{design-model-check,supervision}/*-formulate/splice.py` (SIM115, I001). These are formulate rounds' helper scripts, committed with no work-item (F10).

  Already there before the branch, on lines it did not change:
  - `scripts/supervise_change.py:91,118` B023 (in unchanged code, now 3 lines lower);
  - `scripts/workqueue.py:248` I001;
  - `supervision_proposal_steps.py:102` RUF100;
  - `supervision_reintegrate_steps.py:13` F401 and `:174` FURB167;
  - `tests/scripts/test_supervise_answers.py:9,10` RUF100.

  I cannot tell from the change whether `tests/scenarios/test_design_model_check.py:7` I001 was there before. w221 added `from .design_model_check_work import *` at the end of an alphabetical block.
- **vulture**: clean.
- **import-linter**: "the project states no import contracts". It does not say `missing`.

**`tools size`**: exit 0, printed nothing. No file is over 300 lines, touched or not.

**`features deprecated`**: exit 0, 13 deprecated scenarios.
- Two are this initiative's (`Deprecated for: removal`), deprecated by formulate commit edf03019:
  - `features/supervision.feature`: "under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated)" (@r77, retired);
  - "the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated)" (@r92, retired).
  Both are left in place by w226's plan D2 (F7).
- The other 11 were already there before the branch:
  - design-model-check: v18;
  - supervision: the worker's DONE, the implementer's DONE with failing tests, the researcher's DONE with questions, and the formulate round's questions ×2;
  - work-queue: show ×2, status ×3.

**`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for: deleted `def`s, dropped Examples rows or parametrize cases, removed or loosened `assert`s, added skip or xfail, and Then steps rewritten or widened.

1. **The five @r27 scenarios of `features/design-model-check.feature`**, removed by w221 under its Retires.
   - They proved the shape of work files: a missing `initiative.md` charged to its directory, missing id, kind or status, an out-of-lifecycle status, priority and date, which accepted requirements need a scenario, and statuses in the lifecycle.
   - They were deprecated by formulate commit a0295498 and replaced by the @r124 outline. The plan lists them under Retires (§1), so this is a retirement, not a break.
   - Two of their cases are in no row of @r124 (F8):
     - "the part p1.md has a status not in its kind's lifecycle" (a work-item with status `loved`);
     - "a request in `.shop/work/requests/q1.md` has the status withdrawn" is no file problem.
2. **Step definitions** `work_item_accepting` and `work_item_with_status_accepting` (`design_model_check_problems.py`), removed by w221. Only the retired @r27 scenarios used them. `malformed_work` moved to `design_model_check_work.py`, and its branch for the dropped "status loved" row went with it.
3. **The three deprecated scenarios of `features/supervision.feature` retired by w226**, each listed under its Retires:
   - the @r77 outline "… that <reply>";
   - the @r92 split "… with what it adds, changes and removes on that capability";
   - the @r104 gate "… on the lines and terms …".
4. **`tests/scenarios/spec_integration_steps.py` `drafts_glossary_change` (w222)**: `assert not (repo / ".shop/work/i1/glossary.md").exists()` removed.
   - It proved that the r54 integrate round wrote no glossary-proposal (w219's plan decision 3: r158 was not w219's).
   - w222's plan §4 says "None" for tests the decisions break, so the plan does not list it. The implementer's allowance row covers it (see Allowances).
5. **Widened, not weakened**:
   - `proposals_written` and `gate_names_its_ids` (w224): an optional `and the term "ledger"` clause; the assertions with the clause are unchanged.
   - `gate_started`, `apply_started`, `approved_after_apply`/`position`, `proposal_awaiting`, `round_given_drafts`, `written_from_round`, `no_formulate_for_p1` (w225): `p1` became `[pg]1`. `gate_started` and `apply_started` now pass `name` to `rounds()`. Since `rounds(repo, kind, name="p1")` defaults to p1 (`supervision_rounds_steps.py:150`), the p1 case asserts the same as before.

No skip or xfail was added. No parametrize case was dropped in `tests/scripts/`. `test_supervise_answers.py` only gains a test.

## Allowances

- **w222, 4-implement, `drafts_glossary_change`, interim: holds.**
  - The assertion was first committed in 085527d8 (w219), after Base.
  - It encoded w219's interim stance (no glossary-proposal yet).
  - w222's plan D1/D2 has `work run` write `glossary.md`, and the r171 scenario now asserts that it is written.
  - The step's remaining assertions (the brief's "no capability's entry" wording and the kept glossary entry) assert nothing against D1/D2.
  - w222's 3-implement report lists the same row.
- **w225, 7-implement, `started_glossary_only`, setup: holds.** The change adds one write of `.shop/work/i1/ledger.md`, with no assert, expected value or case changed.
- **w225, 7-implement, `glossary_drafted`, comment only: holds.** The `listed` lambda carries no `noqa` at HEAD. The other unused `noqa`, at `:137`, is still there (Checks).
- **"none" rows**: w219 3-implement, w221 3/5-implement, w223 3-implement, w224 3-implement, w225 3-implement and w226 3-implement. Each holds by the search above.
  - w225 3-implement says "no assertion changed". That holds for the reason in item 5 above.
  - w221 4-implement and w225 4-implement made no commit and checked no row.

## Cannot verify

None. Every check this review asks for has a run in the brief.

## Findings

### F1. Important, w225, fix now: the approval question is written on a glossary-proposal, which no line asks for

- **Where**: `scripts/supervise_rounds.py:159-160` (the r117 branch). w225's routing (`scripts/supervise_glossary.py:13-31`, `ROUTES` and `route`, called from `supervise_rounds.py:58-61`) brings glossary-proposals to it.
- **What is wrong**: when a glossary-proposal's gate round gives no question, `work run` writes "Are the lines of g… approved as drafted? …" under its `## Questions`. r117 asks for this for a capability-proposal only. No Behaviour line asks for it for a glossary-proposal. q36 line 1, which would ask for it, is `status: open` and not integrated.
- **Why it matters**: this is observable behaviour on the person's queue (a question they must answer) that reaches code without a line. The w225 4-review raised it, and an answer under the delegation (2026-10-28) accepted it "as it is" and raised q36.
- **Fix**: integrate q36 line 1 through integrating-a-proposal and formulate it, so the line is written first. Or limit the r117 branch to `kind == capability-proposal`. If you do that, decide what a zero-question glossary-proposal does: `route()` (`supervise_glossary.py:29`) leaves an `awaiting-answer` one with no question unrouted.

### F2. Important, w222, observation: a started initiative with only a glossary-proposal is given no integrate round, against the text of r93

- **Where**: `scripts/supervise_rounds.py:48`.
- **What is wrong**: r93's text gives the integrate round to a started initiative with "neither a capability-proposal nor a work-item". The code also requires no glossary-proposal.
- **Why it matters**: without the change, r164 (gate of a drafted glossary-proposal) and r161 could never be reached, because `due()` would re-integrate first (w222's plan D3; its 3-implement report saw the loop as a 120 s timeout). So the code serves r164, r171 and r161, and the conflict is between lines. It was accepted under the delegation (w222 Answers, 2026-10-28). q35 carries the reworded line and is `open`.
- **Fix**: integrate q35, retiring r93.

### F3. Important, w222, observation: a later integrate round overwrites `glossary.md` whole

- **Where**: `scripts/supervise_change.py:133-139`.
- **What is wrong**: `write_proposals` writes `self.dir / "glossary.md"` with `write_text` whenever the change list has a glossary entry. A re-integrate round (r142 or r150, for a capability-proposal) whose change list names the glossary replaces an existing glossary-proposal with status `drafted` and that round's terms only. This happens even when the proposal is `awaiting-answer` with the person's `## Questions` and `## Answers`, or `approved`.
  - Capability-proposals are rewritten in place or merged (r148, `:109-121`); the glossary-proposal is not.
- **Why it matters**: the person's answers on the glossary-proposal leave the working file, and an approved proposal goes back to its gate. git history keeps the earlier text. No line names the case, and w222's plan §5 left it open.
- **Fix**: rewrite or merge an existing glossary-proposal as `proposal_for` does for a capability. Test that would show it (not run): a scenario with i1's `glossary.md` awaiting-answer with an answer, and an r150 re-integrate round of p1 giving `{"glossary": true, "adds": ["term/x"]}`. Then g1 keeps its Answers and status.

### F4. Important, w223, observation: "names a term of the glossary" is matched as any whole-word use, which leaves most questions in this repository for the person

- **Where**: `scripts/supervise_glossary.py:90-94` (`names_one`).
- **What is wrong**: the question is matched against every term of `spec/index.md`'s Glossary as a whole word, in any case. Those terms include `run`, `check`, `status`, `suite`, `scenario`, `request`, `requirement`, `result`, `review`, `round`, `answer`, `work-item` and `input`. Every glossary-proposal's stem is matched as well, and `work run` names them all `glossary`.
- **Why it matters**: almost every question `work run` or a reviewer writes uses one of these words. For example, the w221 question at `.shop/work/i46/w221.md:22` contains "suite", and every question that says "work run" contains "run". So r163's delegation sessions are rarely reached, and r162's reading decides whether a delegation does anything at all.
- **Reproduction**: by reading the regex `(?<![\w-])%s(?![\w-])` with `re.IGNORECASE` over `terms_of(root)`. Not run.
- **Fix**: a question to the person on r162's reading: a question that is *about* a term (its definition or its change), or one that *uses* a term.

### F5. Important, w223, observation: after a question left for the person, later questions are still given to sessions whose answers are thrown away

- **Where**: `scripts/supervise_answers.py:75-78`.
- **What is wrong**: a question `names_one` flags sets `left`. Each later unflagged question is still given to `ask()`, and its answer is discarded by the positional gap rule. This contradicts r78 ("when a session … answers a question, `work run` shall write the answer").
- **Why it matters**: the session is spent and the answer is lost for this run. Nothing invalid is written, and the question is asked again once the person answers the earlier one. The gap rule was already there. r162 makes the gap certain whenever an item's first question names a term (w223's plan decision 4 and open case 1).
- **Fix**: skip `ask()` once `left` is set, or write answers by question rather than by position. Test that would show it (not run): w1 with "Does it write the ledger?" then "Which module owns the log?", the Glossary holding "ledger", and the delegation "Please get everything delivered…". Then no delegation-answerer session is started for the second question, or its answer is written.

### F6. Minor, w225, observation: the module-map row for `scripts/supervise_glossary.py` does not name the routing or the glossary-only done

- **Where**: `CLAUDE.md`, the `scripts/supervise_glossary.py` row.
- **What is wrong**: the row names the withheld terms (r55) and the delegation questions (r162). The module also holds `ROUTES`, `route` and `statuses` (r164-r170, `:13-31`) and `glossary_only_done` (r161, `:62`), all added by w225.
- **Fix**: extend the row.

### F7. Minor, i46 (formulate edf03019; w226 plan D2), observation: two deprecated-for-removal scenarios of retired ids are left in place

- **Where**: `features/supervision.feature`:
  - @r77 "under a delegation, a work-item with two questions … both answers stay written when the run ends (deprecated)";
  - @r92 "the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated)".
- **What is wrong**: neither has a replacement, so neither r123 nor r73 puts it in a Retires section, and they still run in the suite. What they pin (two answers of one work-item kept; distinct proposal ids across initiatives) is in no live scenario.
- **Fix**: retire them through a work-item, or write lines that keep what they pin.

### F8. Minor, i46 (formulate a0295498; w221's retirement), observation: two cases of the retired @r27 scenarios are in no @r124 row

- **What is wrong**: no @r124 row covers a work-item with a status outside its lifecycle (`loved`), or a withdrawn request being no file problem. r124's line still names both ("a status … not in its kind's lifecycle").
- **Fix**: rows for both in the @r124 Examples (formulation). The check that shows it complete: `pytest --work-item w221` runs both rows.

### F9. Minor, none, drop: commits that belong to no work-item

49 commits, all the workflow's own:
- `work note`, `work:`, `work answer` and `work request` (q32-q36);
- `spec:`: 92e82b4e, f19a7713;
- `formulate`/`features:`: a0295498, a714768, edf03019, d6c99676, e4159920;
- the round merge 441c5954;
- the proposal-list restore 7d0e08ca;
- branch review 1 (44d15c56).

By the commit subjects and the reports, none of them changes `scripts/` or `tests/`. Not verified commit by commit (Range).

### F10. Minor, none (formulate rounds), observation: round helper scripts committed as tracked Python

- **Where**: `.shop/work/i46/runs/design-model-check/{1,2}-formulate/splice.py` and `.shop/work/i46/runs/supervision/{1,6}-formulate/splice.py`.
- **What is wrong**: they are tracked Python files, so `tools check` lints them (14 ruff errors). i39's ledger recorded the same.
- **Fix**: keep round helpers under `.shop/scratch/` (ignored), or exclude `.shop/` from ruff.

### F11. Minor, w221, w222 and w225, drop: ruff errors the branch adds

- **Where**: `design_model_check_problems.py:6` (I1), `design_model_check_work.py:6`, `supervision_integrate_steps.py:81` and `supervision_proposal_steps.py:137` (Checks).
- **Fix**: `ruff --fix` handles three; rename `commit` to `_` in the fourth.

## Shape

**Size**: met. `tools size` printed nothing.

**Module map**:
- New `scripts/supervise_glossary.py`: it has a row (w219, widened by w223). The row is incomplete (F6).
- `scripts/supervise_change.py`: the row is widened for glossary-proposals (w222). Met.
- `scripts/model*.py` (`model_work.py`, `model.lp`): the `model` row. Met.
- `scripts/supervise.py`, `supervise_rounds.py`, `supervise_brief.py`, `supervise_answers.py`, `supervise_done.py`: the `supervise*.py` and `supervise_done.py`/`supervise_answers.py` rows. Met.
- `scripts/workqueue.py:155`: the `work` row. Met.
- `tests/scenarios/design_model_check_work.py`: a new step module for one concern (r124's work files). Met, per the `tests/scenarios/` row.
- `tests/scripts/test_supervise_answers.py`: a test of a script no scenario drives (`names_one`'s word boundaries). Met.

**Code and steps no scenario reaches any more**:
- The optional `(?P<term> and the term "ledger")?` branch of `proposals_written` (`supervision_integrate_steps.py`) and of `gate_names_its_ids` (`supervision_proposal_steps.py`). Their only users with the clause were the @r92 and @r104 scenarios that w226 retired.
- Check that shows them gone: `grep -n 'and the term \\"ledger\\")?' tests/scenarios/` finds nothing, and `pytest --work-item w224` stays green.

**Docstrings and comments still citing retired ids**:
- `design_model_check_problems.py:1` cites r27.
- w226's plan names r92, r104 and r77 in `supervise_change.py`, `supervise_rounds.py`, `supervise_brief.py` and `supervise_answers.py`.
- Polish; dropped.

**`scripts/workqueue.py:155`**: `move` takes, for a glossary-proposal, every work-item status plus `approved` and `formulated` (`STATUSES + PROPOSAL_STATUSES`). Only `drafted`, `awaiting-answer`, `approved` and `withdrawn` are in its lifecycle (`model_work.py`, r124). See the Observations.

## Coupling

- The branch adds `git show HEAD:spec/index.md` and `git status --porcelain -- spec/index.md` (`supervise_glossary.py:71-72`). Both are git's published plumbing and porcelain-v1 output, so they are stable.
- The new step definitions use `pytest_bdd.parsers.re` and `given`/`then`, pytest-bdd's published API.
- Already there and outside the branch: the suite warns that pytest-bdd's own `compat.py:28` and `FixtureDef` use pytest internals removed in pytest 10 (`PytestRemovedIn10Warning`). A pytest 10 upgrade would break the suite through pytest-bdd, not through this repository's code. Pinning pytest below 10, or a pytest-bdd release that drops those calls, keeps it stable.
- The `@deprecated` tag becomes an unregistered mark (`PytestUnknownMarkWarning`). It would fail under `--strict-markers`. Registering the mark makes it stable.
- No upstream project is relied on by this branch.

## Observations

Each with its reproduction:

- **F2**: `supervise_rounds.py:48` reads `… and not self.glossary_proposals() and not self.items()`, while r93's text (`spec/capabilities/supervision.md`) says "neither a capability-proposal nor a work-item". q35 is `open`.
- **F3**: `supervise_change.py:134-139` calls `path.write_text(...)` with `status: drafted`, with no read of an existing `glossary.md`. Test not run.
- **F4**: `names_one` (`supervise_glossary.py:93`) with the repository's Glossary flags `.shop/work/i46/w221.md:22` ("… the whole suite pass are missing") on "suite". By reading; not run.
- **F5**: `supervise_answers.py:75` calls `self.ask` before the `left` check at `:76`. Test not run.
- **F7**: listed by `features deprecated` (the run above), with `for: removal`.
- **F8**: the @r124 Examples in the change have no `loved` or request row.
- **F10**: the 14 SIM115/I001 errors in the `tools check` output above.
- **A glossary-only initiative with an undelivered raised request is set done.** `supervise_done.py:28-37` calls only `glossary_only_done`. r161 is silent; r105 checks requests (the w225 6-review, finding 2).
- **An abandoned initiative can be set done.** `supervise_done.py:31` guards only `before == "done"`, so an `abandoned` glossary-only initiative run by name moves to `done` (the w225 6-review, finding 3).
- **`workqueue.move` takes `formulated`, `ready`, `green` and others for a glossary-proposal.** `workqueue.py:155` combined with `STATUSES` and `PROPOSAL_STATUSES = ("approved", "formulated")` at `:16-19`. `model check` would then print a file problem (r124's "glossary-proposal … formulated" row).
- **A change-list entry with both `"glossary": true` and `"capability"` is read as a capability entry, so its `term/` ids go into a capability-proposal.** `supervise_change.py:27`. No client sends it today: the brief's `CHANGE_LIST` asks for separate entries.
- **A capability named `glossary` would collide with the glossary-proposal's file.** `supervise_change.py:122` writes `<capability>.md` and `:134` writes `glossary.md`. w222's plan §5.
