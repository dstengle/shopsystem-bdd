# Branch review 2 of i54

**Verdict: DONE_WITH_CONCERNS.** i54's own work is clean: w231 (supervision#r187) and w232 (work-queue#r59, r60, r61) are both `green`, and neither has a finding that is Critical or fix now. w232's earlier fix-now finding (lines with no line outcome left out of `work show <request>`) is fixed at `scripts/workqueue_list.py:86`.

The status is DONE_WITH_CONCERNS because the range is on `main` and also holds other initiatives' work. Two findings there are carried from earlier reviews and are not i54's:
- one Critical: w230 (i51) removed the r162 outline from `features/` with no `## Retires`;
- one Important: w236 (i63) loosened `is_failed` under an allowance that does not hold.

Neither is triaged fix now, so `questions` is empty.

## Range

- `a2a53b36c02b74d046b7a490d802403f3f1828a9..c25a4c0d22c882d576e5b09f38c2b9f3335b74e1` (branch `main`): 644 commits, of which 22 belong to an i54 work-item.
- **w231** (`green`, under supervision, accepts supervision#r187), fileset `[tests/scenarios/supervision_merge_steps.py, tests/scenarios/test_supervision.py]`.
  - Commits: `6e55ddd3`, `82832c5e`, `56f6efb6`, `f5f6671b`, `156d2b2b`, `afc4aa72` (steps), `3cc54654`, `eb1a30ac`.
- **w232** (`green`, under work-queue, accepts work-queue#r59, r60, r61).
  - Commits: `911cac0f`, `63e22026`, `3fe3a538`, `a2c10dd2`, `7b1e1e12`, `a5d6b59b` (code), `14e01547`, `069d133d`, `74c02e0c`, `9d5b527a`, `e49440e2`, `cb269262` (fix), `20334492`, `c25a4c0d`.
- i54's own round and spec commits, with no work-item. These are workflow commits, not code:
  - `49d8369f`, `c1aa3af9`, `97c440d1`, `985c0204`, `afb68414`;
  - `ec944d15` (spec r187), `bb2caaeb` (features r187);
  - `ec30d007` (spec r59-r61, r34 r35 retired), `fe960a7a` (features r59-r61, r34 r35 deprecated), `d10d81ce`;
  - the i54 `work note` commits.
- Branch review 1 of i54 is `850ce9d3`, at `eb1a30ac`. This review covers the whole range again, with w232 and the commits after `eb1a30ac` new.

## Suite

`Suite: 1088 passed, 0 failed at c25a4c0d in 35.10 s`. The full line is "1088 passed, 1 skipped, 18 xfailed, 3 xpassed, 872 warnings, 56 subtests passed".

- **Parallel:** yes, `-n auto` ("bringing up nodes...").
- **In-process:** mostly no. `run_work` (`tests/scenarios/test_work_queue.py:179`, and `test_supervision.py`'s `run_work`) runs `work` as a subprocess. Only `test_work_queue.py:195` drives one move through the library, in-process.
- The suite runs under 60 s, so neither is a finding.
- **The 18 xfails:**
  - 11 are w212's `test_requests.py` scenarios;
  - 2 are w238's supervision r188/r189 scenarios;
  - 5 are the r62 outline rows ("accepted by work-queue, neither green nor withdrawn").
  - None of them is i54's.
- **Dry-run and real mode:** the system has no dry-run mode of an operation of its own. I grepped `scripts/` for `dry.run`. The only hits are `git push --dry-run`, used as a probe at `supervise_review.py:55` and `supervise_faults.py:71`. So no agreement test applies.

## Checks

All runs at `c25a4c0d`.

- **w231's scenarios** (`pytest -q -n auto -p work_items --work-item w231`): exit 0, "182 passed, 1 skipped, 258 warnings, 56 subtests passed in 6.91s". The r187 scenario is named in the warnings and passes.
- **w232's scenarios** (`--work-item w232`): exit 0, "184 passed, 1 skipped, 256 warnings, 56 subtests passed in 4.59s".
- **`tools check --base a2a53b36`**: exit 1.
  - **ruff:** 28 errors. On non-`.shop/` files the branch touched:
    - `tests/scenarios/supervision_integrate_steps.py:87` RUF059;
    - `tests/scenarios/supervision_proposal_steps.py:102` and `:137` RUF100;
    - `tests/scenarios/test_supervision.py:14` I001. w231 touched this file, but the order was wrong already at its base (w231 review, finding 1);
    - `tests/scenarios/work_queue_list_steps.py:134` RUF015. w232 touched this file, but w232's review traced the line by `git blame` to `a033c460`, before w232;
    - `tests/scripts/stub_claude.py:208`, `:209` FURB167;
    - `tests/scripts/test_supervise_answers.py:9`, `:10` RUF100.
    - The rest are tracked round scratch scripts under `.shop/work/` (i50, i59, i60, i63).
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". No contract is checked. The heading does not say `missing`.
- **`tools size`** (300 by default, `scripts/tools:57`): exit 0 and no output. No file is over the limit, touched or not.
- **`features deprecated`**: exit 0, 20 deprecated scenarios. One line resolves to no scenario: the r163 outline, "for: r209 and r210 | no scenario has that title" (Finding 6).
- **`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for:
- `-def test_` lines;
- `-` lines holding `assert`;
- dropped Examples rows and parametrize cases;
- `skip` or `xfail` added;
- step patterns that changed;
- scenarios removed from `features/`.

What I found:

1. **Deleted test, not a finding.** `tests/scripts/test_supervise_answers.py`, `test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`, in w230 (i51).
   - It proved that `names_one` matches a glossary term or a glossary-proposal name as a whole word in any case (r162).
   - w230's plan lists it under "Tests the decisions break".
2. **Removed scenario.** The `@r162` outline in `features/supervision.feature`, both examples, in w230 (i51), commit `998966626`.
   - It proved that a question naming "ledger" or g1 goes to no session.
   - w230's plan lists it. The removal under no `## Retires` is Finding 1.
3. **Loosened, plan-listed, not a finding.** `tests/scenarios/requests_flow_steps.py:99` `show_prints`, in w232 (`a5d6b59b`).
   - Before, it asserted that the whole stdout of `work show <request>`, split into words, was `<name> delivered asker`.
   - Now it checks the first line only.
   - w232's plan §4 lists it, with this rewrite.
4. **Pattern changed, narrower, not weakened.** `tests/scenarios/work_queue_list_steps.py:56` `prints_question`, in w232: a `parsers.parse` pattern became an anchored regex with `[^"]*`.
   - Its assert is unchanged.
   - The feature line it used to swallow ("... and the answer ...") now goes to `prints_question_answer`, which asserts more.
5. **Loosened, not plan-listed, allowance does not hold.** `tests/scenarios/supervision_faults_steps.py:148` `is_failed`, in w236 (i63, commit `94f0a748`).
   - Before, it asserted that `git status --porcelain -- .shop/work` was empty.
   - Now it excludes `.shop/work/i2`.
   - This is Finding 2.
6. **Widened, not weakened.** In `supervision_delegation_steps.py` (w230), `glossary_proposal_awaiting`, `two_unanswered` and `question_unanswered` were widened; their assertions are kept.
   - In `tests/scripts/stub_claude.py` (w237), the double's `git` calls now retry on `index.lock`. They are still checked (`check_returncode`), and no assertion changed.

## Allowances

- **w231, 3-implement**: "none". This holds: w231 changed no existing test.
- **w232, 3-implement**: "none (show_prints was listed in the plan; prints_question respelled)". This holds: `show_prints` is plan-listed, and `prints_question`'s assert is unchanged.
- **w232, 6-implement**: "none". This holds: the commit adds `tests/scripts/test_work_show_request.py` and changes no test.
- **w236, 4-implement (i63, not i54)**, row "`is_failed` — setup/interim": **does not hold.**
  - Setup fails because the diff changes an assert's pathspec.
  - Interim fails because `is_failed` was first committed before `Base`.
  - i63's branch review 1 (`ea0d0022`) raised this already. It is carried as Finding 2.

## Cannot verify

None. Every check this review takes is in the brief's runs at `c25a4c0d`.

## Findings

### 1. Critical, w230 (i51, not i54), observation: `features/supervision.feature`, the `@r162` outline removed by a work-item that lists no Retires

- **What is wrong.** Commit `998966626` removes the deprecated r162 outline. w230 has no `## Retires` section.
- **Why it matters.** The only change to `features/` a work-item may make is removing a deprecated scenario that it lists under Retires.
- **Why it is not fix now.** No answer is wrong and no data was lost. r162 is in supervision's `retired:`, and `features bindings` is clean. i51 is `done`, and its own review and review 1 of i54 raised this.
- **Fix.** The person rules on it. Either record the removal under a `## Retires` of w230, or restore the outline and retire it through r123.

### 2. Important, w236 (i63, not i54), observation: `tests/scenarios/supervision_faults_steps.py:148`, `is_failed` loosened under an allowance that does not hold

- **What is wrong.** The clean-status assert now excludes `.shop/work/i2`, for every scenario that uses `is_failed`, not only r218's. The plan does not list it, and the allowance row holds neither as setup nor as interim.
- **Why it matters.** A scenario where `work run` wrongly left i2's path dirty would now pass `is_failed`.
- **Fix.**
  - Restore the full check for the scenarios that have no i2.
  - Give the r218 scenario its own Then that excludes i2's path.
  - Carried from i63's branch review 1.

### 3. Important, w230 with spec `2c74c3a6` (i51, not i54), observation: r209/r210 and `scripts/supervise_answers.py:74` contradict design-decision 0073, which supervision `rests_on`

- **What is wrong.** `spec/decisions/0073-the-glossary-is-a-target-of-spec-work.md` says "a question that names a term or a glossary-proposal is the person's, never answered under a delegation". r210 and `supervise_answers.py:74` give such a question to a session, whatever words it uses.
- **Why it matters.** The decision a capability rests on is binding, and nothing amends it.
- **Fix.** The person rules on it. Either amend or supersede 0073, or retire r209/r210.
- Carried from review 1, Finding 2. It is unchanged at `c25a4c0d`.

### 4. Important, w232, observation: `scripts/workqueue_list.py:99-100`, `work show <request> --json` gives only name, status and turn, none of r59's parts

- **What is wrong.**
  - r38: "Where `--json` is given, `work show` shall print its result as one JSON object".
  - r59 makes that result the request's status, its turn, its lines with their outcomes, its questions, its answers and its resolution.
  - The JSON branch prints `{"request", "status", "turn"}` only. Plan D4 left it so, on the ground that w232 does not accept r38.
- **Why it matters.** A script reading `work show q1 --json` gets less than r59 says `show` gives.
- **Why it is not fix now.** No client reads the JSON of a request's show today: the plan's search found no test or caller. The fields it does give are right, so the answer is not wrong.
- **Fix.** Add `lines`, `outcomes`, `questions`, `answers` and `resolution` to the JSON object, from `workqueue_request.sections`.
- **Test, not run:** `work show q1 --json` on the r59 scenario's request, asserting each of r59's parts is in the object.

### 5. Important, none (the range's commits outside i54's work-items), observation: 622 of 644 commits belong to no i54 work-item

- **What is wrong.** i54's branch is `main`, so `Base..HEAD` interleaves every initiative delivered meanwhile. The commits outside i54's work-items are of these kinds:
  - **Bookkeeping:** transitions, `work note`, outcome, turn, request, delegate and round merges.
  - **Spec and features commits of formulate and apply rounds.**
  - **Other initiatives' work-item code:**
    - `a807b5b7` (w228, i50);
    - `998966626` (w230, i51);
    - `4e206ec4` (w233, i60);
    - `ed25c279`, `ab71c3fc` (w235, i60);
    - `d8f57cc8`, `94f0a748` (w236, i63);
    - `a9cb7536`, `fd8364d1` (w237, i63).
  - **Hand repairs:** `73758cad`, `556cba3b`, `c0d2f0e2`, `28ce4056`, `a411ea7a`, `ef8e1609`, `f7659913`, `74132b41`, `9b453fd2`.
  - **The step `started_fulfilling_bare`** (`tests/scenarios/supervision_integrate_steps.py:22`, r180). It reached `main` through no green work-item: w229, which accepts r180, is still not green.
- **Why it matters.** A branch review of one initiative cannot tell its change from another's.
  - The other work-items' code was reviewed by their own initiatives' branch reviews: `a746612b` (i50), `9e8c48dc` (i51), `ff632c3a` to `55aae903` (i60), `ea0d0022` (i63).
  - The r180 step was reviewed by none.
- **Fix.** Either `work run` gives a branch review only its initiative's commits and their change, or each initiative gets its own branch. The r180 step needs a work-item that owns it.

### 6. Minor, none (formulate `af49d7ff`, i51), observation: `features/supervision.feature`, the r163 outline is deprecated "for: r209 and r210", which names no scenario, though its replacements' work-item w230 is `green`

- **Fix.** Give the replacement's title in `Deprecated for:`, or retire the outline under the `## Retires` of the next work-item that touches supervision.

### 7. Minor, w232 and w236, observation: deprecated scenarios whose successors' work-items are `green`

- **What is wrong.**
  - `features/work-queue.feature`, the r34 and r35 scenarios (deprecated "for: removal"). Their successors r60 and r61 are w232's, which is `green`. w232 has no `## Retires`.
  - `features/supervision.feature`, the r28 scenario (deprecated "for: removal"). Its successor r218 is w236's (i63), which is `green`.
  - These still run.
- **Why it matters.** Nothing will retire them until a work-item lists them under Retires.
- **Fix.** Draft a work-item that retires them.

### 8. Minor, w232, drop: docstrings that name retired ids or leave out requests

- `scripts/workqueue_list.py:1-4`: the module docstring still says "r34-r39", and that `show` gives "one initiative ... or one work-item". The docstring of `show` (`:94`) says the same.
- `tests/scenarios/work_queue_list_steps.py:1`: "(r34-r39)". The plan §2 asked for r59.
- w232's review 4 raised these, as finding 2. They are cheap, but nothing behaves differently.

### 9. Minor, w231, drop: `tests/scenarios/test_supervision.py:14`, ruff I001

- The order was wrong already at w231's base.
- **Fix.** `ruff --fix` in the next work that touches the file.

### 10. Minor, none (other initiatives' step changes and round scratch), drop: ruff on touched files and on tracked round scripts

- RUF059, RUF100 and FURB167 at the lines listed under Checks.
- SIM115, I001, C402 and FURB167 on the tracked scratch scripts under `.shop/work/i50`, `i59`, `i60` and `i63`.
- **Fix.** Exclude `.shop/` from `tools check`, or keep round scratch out of the commit.

## Shape

CLAUDE.md's rules, and each module-map row the branch touched:

- **Size limit (300).** Met: `tools size` printed nothing.
- **"A new concern gets a new module and a row here".**
  - Met for w231: `tests/scenarios/supervision_merge_steps.py` is one concern (r187).
  - Met for w235: `scripts/migrate_prompt.py` has its row.
- **`scripts/workqueue_list.py` row** ("the queue listed, an initiative or a work-item shown, the record of raised requests"). **Not met** after w232: `show` now also gives a request's parts (r59, `workqueue_list.py:79-93`).
  - Minor, w232, observation: add "a request shown (r59)" to the row.
  - Shown complete by `grep -n "workqueue_list" CLAUDE.md` giving a row that names a request.
- **`scripts/workqueue_request.py` row.** Met.
  - `sections` (`workqueue_request.py:32-36`) is the requests' own reader, called by `show`, as plan D2 says.
  - `delegate` is in the row.
- **`scripts/supervise_glossary.py` row.** **Not met.** It still says "the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162)". w230 removed `names_one`, and the row does not name r173's `approval_question`.
  - Minor, none (i51 and i50), observation, carried.
  - Shown complete by `grep -n "r162" CLAUDE.md` printing nothing.
- **`scripts/supervise*.py` row.** Met. `supervise_faults.py:106-115` (r214, r218) and `supervise_rounds.py:160-162` (r173) belong to its "faults" and "gate" parts.
- **Function-local import.** `workqueue_list.request_parts` (`:82`) imports `workqueue_request` inside the function.
  - I checked whether this breaks an import cycle: no module in `scripts/` but `scripts/work` imports `workqueue_list`, so it does not.
  - Minor, drop: move it to the top.
- **Unreached code.** None found.
  - vulture is clean.
  - `names_one`, `terms_of` and `proposals_of` went with their test.
  - `ENDED` in `migrate_prompt.py:14` repeats the tuple in `workqueue_request.delegate`. This is a drop.
- **r187's production code.** w231 changed none. `merge_lists`/`write_proposals` in `scripts/supervise_change.py` predate `Base`, and r187 is now the line that asks for them. So it is not "code no line asks for".
- **Code no line asks for.** None in w231 or w232. Each new output of `request_parts` serves r59: the turn, the lines with their outcomes, `unsettled` for a line with none, the questions, the answers and the resolution.

## Coupling

- **pytest / pytest-bdd.** The suite gives `PytestRemovedIn10Warning` from `pytest_bdd/compat.py:28` (×308): pytest-bdd passes a nodeid to `_register_fixture`. pytest-bdd relies on more than pytest publishes.
  - A move to pytest 10 would break the scenario layer.
  - Pin pytest below 10, or pytest-bdd to a release that passes `node`.
- **Unregistered marks.** The tags `@deprecated`, `@r209`, `@r210`, `@r211`, `@r214`, `@r215`, `@r216` and `@r218` reach pytest as unknown marks (×32 each). Under `--strict-markers` the suite would fail at collection.
  - Register the tag marks in conftest.
- **Claude Code's hooks.** `hooks/hooks.json` adds `UserPromptSubmit` (w235, i60), running `migrate prompting`. It relies only on what Claude Code publishes: a hook's stdout on exit 0 is added to the session's context, and `${CLAUDE_PLUGIN_ROOT}` is set.
  - `tests/scenarios/requests_session_steps.py:20` reads the hook's command from `hooks.json` by its structure, which is the repository's own file.
  - This is stable.
- **ruff, vulture, import-linter, the `claude` CLI.** These are reached through `tools` and the `SHOPSYSTEM_WORK_CLAUDE` stand-in. The branch adds no new reliance on them.

## Observations

- **`scripts/workqueue_list.py:83`, a request with no `turn:`** (w232) prints "it is the None's turn". Reproduction, by reading: `workqueue.requests` yields `data.get("turn")`, which is None when the field is missing. No request in the repository lacks `turn:` (w232 review 4, by grep).
- **`scripts/workqueue_list.py:84-91`, an entry with no number** (w232). An entry under `## Lines` or `## Questions` that holds ". " but does not start with a number makes the sort's `int()` raise `ValueError`, so `work show` crashes rather than refuses. Example: `- Note. later`.
  - Reproduction, by reading: `workqueue_request.sections` (`:35`) keys each entry by the text before its first ". ".
  - Test, not run: `show` of a request with that entry under `## Lines`, asserting a refusal or a printed line.
- **`scripts/migrate_prompt.py:39-44`, "always exits 0"** (w235, i60). It catches only `workqueue.Refused`. Any other error reading a request exits 1 with a traceback on every prompt. Exit 1 does not block the prompt.
  - Reproduction, by reading.
  - Test, not run: `migrate prompting` in a repository whose request has broken frontmatter, asserting exit 0.
- **`tests/scripts/stub_claude.py:112-120`, git retry in the double** (w237, i63). The double now retries while `index.lock` is held. Whether `work run`'s own git calls race with sessions that commit beside them is not shown by any run.
  - Test, not run: two initiatives' sessions committing at once while `work run` commits a transition, asserting no `index.lock` failure.
- **The 3 XPASS.** The suite output does not name them, because `-rfEx` leaves XPASS out of the summary.
  - Reproduction: the summary line says "3 xpassed", and no XPASS line is printed.
  - Test, not run: the suite with `-rX`.
- **`supervise_glossary.approval_question` with empty lists** (i50) writes "Are the terms of g1 approved as drafted? It ." Reproduction, by reading: `", ".join([])`. Carried.
- **w231's open cases** (plan §5): an id repeated within or across lists, p2's status and Q&A after a merge, two proposals for one capability. No scenario covers them.
  - Test, not run: a change list that removes an id p2 holds in `changes`, asserting where it lands.
- **Resolved since review 1:** the duplicate supervision r186/r149, and the overlap of r184 with r32. `3611f76b` retires r149 and r32 (`spec/capabilities/supervision.md` `retired:`).
