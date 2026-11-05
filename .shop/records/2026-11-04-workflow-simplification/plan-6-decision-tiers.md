---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-6
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Plan 6: Decisions in tiers — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `decision-tiers` capability, so that all 6 of its requirements leave `unbuilt:`. Every decision
in force carries a `tier` (`check`, `requirement` or `judgement`). A `check` decision names the tests that enforce it,
and a `requirement` decision names the requirement lines that state it. `model check` keeps each decision to its tier
and keeps a superseded decision marked so. `model decisions --check` runs the tests of the `check` decisions. The 73
decisions are sorted into tiers once, the old process's decisions are marked superseded, and the tier-1 checks join
the readiness bar and the pull request's checks. This closes plan 1's ruling P5 (the tier-1 checks left out of
`passing`) and plan 5's open end (the pull request brief's `## Judgement decisions` is empty).

**Architecture:**
- **The decision file carries its tier (D2).** Two frontmatter fields are added: `tier:` and `enforced_by:`, a list
  of pytest node ids (for `check`) or requirement ids (for `requirement`). `model_work.read_decisions` reads them into
  facts (`tier/2`, `enforced_test/2`, `enforced_req/2`). `model.lp` gains `w_untiered`, `v_d6`, `v_d7` and `v_d8`.
  An entry of the wrong form is a file problem; a requirement id that names nothing is an unresolved reference.
- **`model decisions --check` checks the index, then runs the tests (D5).** The index check is unchanged
  (design-model-check r51, r52). After it, every `check` decision's tests are run by a new module, `model_decisions.py`:
  one pytest run per decision, in the repository, with the repository's `addopts` cleared and nothing written. Each
  decision is printed as `holds` or `failing`, and the run exits 1 when the index is stale or any decision fails.
- **The sort is in this plan (D7).** The planner sorted every decision from its summary and its `## Decision` section;
  the table is under "The sort". The implementer applies it with evidence: each test named passes, and each
  requirement named states the decision. Where the evidence fails, the decision drops to `judgement`, and the report
  says why. The decisions of the old process are superseded by `0074-the-workflow-simplified` (D8).
- **Tier 1 at the bar and at the pull request (D13, D14).** `readiness_bar.check` adds a reason for each `check`
  decision that a capability of the item's lines rests on (`rests_on:`) whose tests fail. `batch_brief.CHECKS` gains
  `model decisions --check`. The `judgement` decisions reach the batch's task subagents (building-a-batch step 4,
  D15) and, unchanged since plan 5, the pull request's reviewer.
- **How each line is met:**

  | id | line (short) | met by | checked by |
  |---|---|---|---|
  | r1 | `model check` on an untiered decision → `w_untiered` | `model.lp` `w_untiered`; `model_work` reads `tier` | scenario @r1; `test_model_tiers.py` (Task 1) |
  | r2 | `check` + untested → `v_d6` | `model.lp` `v_d6` over `enforced_test` | scenario @r2; Task 1 tests |
  | r3 | `requirement` + unrequired → `v_d7` | `model.lp` `v_d7` over `enforced_req` | scenario @r3; Task 1 tests |
  | r4 | `model decisions --check` uses the test | `model_decisions.check_tests` | scenario @r4; `test_model_decisions.py` (Task 2) |
  | r5 | a failing test → error naming the decision | `model_decisions.report` | scenario @r5; Task 2 tests |
  | r6 | accepted supersedes accepted → `v_d8` | `model.lp` `v_d8` | scenario @r6; Task 1 tests |

  `decision-tiers` is a `service` capability with a generated feature. Its ids leave `unbuilt:` in the commit that
  makes their scenarios pass, and the strict xfail holds that rule (plan-1 ruling P6).
- **New modules** (each ≤ 300 lines): `scripts/model_decisions.py`; `tests/scenarios/decision_tiers_handlers.py`;
  `tests/scripts/test_model_tiers.py`, `tests/scripts/test_model_decisions.py`, `tests/scripts/test_decision_checks.py`,
  `tests/scripts/test_readiness_decisions.py`.

**Tech Stack:** Python 3.11 (standard library: `subprocess`, `concurrent.futures`, `dataclasses`), clingo (through
`model check`), pytest with xdist and pytest-bdd.

**Spec:**
- Read first: `spec/capabilities/decision-tiers.md` (6 lines; conditions `untiered`, `untested`, `unrequired`; the
  relation `design-decision enforced by requirement`; its `## Not yet`).
- The glossary of `spec/index.md`: `design-decision`, `tier` (`check`, `requirement`, `judgement`), `test` ("one test
  of the repository's suite, a scenario's or a script's, by its pytest id"), `failing` (condition of test), the
  relations `design-decision supersedes design-decision` and `design-decision enforced by test`, the status of
  design-decision (`proposed`, `accepted`, `rejected`, `superseded`), `well-formed` and `passing` (conditions of item).
- `design.md` goal 7 (the three tiers, "The 72 existing decisions are sorted into the tiers once. Superseded ones are
  marked superseded, and obsolete ones are retired."), goal 3 (the bar's "tier-1 decision checks … hold for any
  constraint the item states") and the Kept list.
- Read beside them:
  - `recon.md` § Decisions;
  - `roadmap.md` (plan 6's row);
  - `plan-1-rulings.md`: P5, P6, P10 ("Retire, never edit, starts at the merge to `main`"), S6;
  - `plan-5-pr-review.md` D6 and `plan-5-implementation.md` "Open problems";
  - `spec/capabilities/design-model-check.md` r40, r50-r52 (the existing `model decisions` lines);
  - `spec/capabilities/readiness.md`, `## Implementation, may change`.

## Global Constraints

- **Branch:** `workflow-simplification`, from `95178ceb` or later. Every plan is built on this one branch. No new
  branch, no push.
- **Shell rule (the person's):** never combine `cp` and `rm` in one command; they need the person's approval
  together. Run them as separate commands, or leave scratch directories under
  `/home/vscode/.claude/jobs/7e9ba079/tmp`. Keep shell variables few.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  - `scripts/model_work.py` (266) may grow to at most 285. The classifying of `enforced_by` entries lives in
    `model_decisions.py`.
  - `scripts/model` (206) may grow to at most 230 (the contract's text).
  - `scripts/model_report.py` (190) may grow to at most 205.
  - `scripts/readiness_bar.py` (114) may grow to at most 160.
  - `scripts/batch_brief.py` (232): only `CHECKS` changes.
  - `tests/scenarios/world_nodes.py` ("frozen after layer 2"), `analysis_tools_handlers.py`,
    `batches_handlers_more.py`, `design_model_check_handlers.py` and `design_model_check_handlers_conditions.py` are
    not changed. Decision-tiers' steps that share a key with them are taken through `work_queue_world.local` (D16).
- **Module map:** `CLAUDE.md` gains a row for `scripts/model_decisions.py` in Task 2. Task 1 adds `decision-tiers` to
  the list in the `tests/scenarios/<capability>_handlers*.py` row. The `scripts/model*.py` row is unchanged.
- **Spec:** no requirement line, group or relation row is edited or added anywhere. A line found wrong is reported, not
  changed. The only spec edits are these:
  - `decision-tiers.md`: `unbuilt:`, the `untiered` definition (D3), `## Implementation, may change`, `## Not yet`;
  - `readiness.md`: `## Implementation, may change`;
  - `spec/index.md`: the `well-formed` definition only (D13);
  - `spec/decisions/`: frontmatter only (D11), the two new files 0075 and 0076, and `index.md` as `model decisions`
    writes it.

  These definitions were added by plan 1 and have never been merged to `main`, so they may be fixed in place
  (plan-1 ruling P10).
- **Decision files:** a `## Decision` section is never edited. In an existing file only `tier:`, `enforced_by:` and
  `status:` are written, and in `0074` also `supersedes:`. `spec/decisions/index.md` is regenerated by
  `python3 scripts/model decisions` in every commit that changes a decision file. `model decisions --check`'s index
  line then reads `spec/decisions/index.md is current`.
- **The strict xfail:** an id leaves `decision-tiers.md`'s `unbuilt:` in the same commit that makes its scenario pass,
  never before and never after.
- **`model decisions --check` writes nothing** in the repository. There is no `.pytest_cache` and no `__pycache__`,
  even when a test fails: the U3 check after a generated scenario enforces this.
- **No network, no claude.** No test reaches a network or starts a session.
- **Names next to ids:** a decision is printed as its path (`spec/decisions/0076-python-files-stay-at-300-lines.md`)
  with its id, never its number alone (design goal 10).
- **Old behaviour kept:** every test of plans 1-5 passes unchanged. That includes design-model-check's r50-r52
  scenarios (`model decisions`, `--check` on a stale index and on a current one) and plan 5's
  `test_the_brief_lists_the_judgement_decisions`.
- **Baselines** (measured at `95178ceb` on this machine). Each task's expected figures are given in the task, and
  any change from these is planned there:
  - `python3 -m pytest -q`: `1356 passed, 1 skipped, 14 xfailed, 135 subtests passed` (27 s wall).
  - `python3 -m pytest -m timing -n 0 -q`: `1 passed, 1371 deselected`. The deselected count grows with the suite.
  - Unbuilt ids (`spec_unbuilt.unbuilt`): 15, with no problems. They are brainstorming r3; conversation r1-r4;
    decision-tiers r1-r6; telemetry r1-r4. At the end there are 9, and `decision-tiers` is absent.
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
    The rows are v10a 19, v17 25, v_d1 9 and w_uncited_obs 16, all under `.shop/work/`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/model lexicon --check | tail -1`: `401 terms, 0 problems`.
  - `python3 scripts/model decisions --check`: `spec/decisions/index.md is current`, exit 0.
  - `python3 scripts/features generate --check`: exit 0.
  - `python3 scripts/features vocab --check | tail -1`: `every step has one handler`.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - `python3 scripts/tools size --limit 300`: silent, exit 0.
  - `python3 scripts/tools check <the branch's changed Python>`: ruff and vulture `clean`. import-linter states no
    contracts.
- **The planned path of `model check`** (each change is expected, and why):

  | after | violations | warnings | why |
  |---|---|---|---|
  | `95178ceb` | 53 | 16 | baseline |
  | Task 1 | 72 (+19 `v_d8`) | 87 (+71 `w_untiered`) | The rules land before the sort. 19 supersessions are accepted → accepted today (18 decisions, 0053 superseding two). All 71 decisions that are not `rejected` have no tier. |
  | Task 3 | 53 | 16 | The sort: each superseded decision's status becomes `superseded`, and every decision in force gets its tier and enforcement. No `v_d6` or `v_d7` row is left. |

  Unresolved references stay at 19 and file problems at 0 throughout: a requirement id named in `enforced_by` must
  resolve.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-05;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as the main session ruled for every plan. |
| D2 | **The fields.**<br>- `tier: check \| requirement \| judgement`.<br>- `enforced_by: [<entry>, ...]`. An entry with `#` is a requirement id in the forms `resolve_req` reads (`design-model-check#r42`, `capability/<path>/<name>#r<n>`). Any other entry is a pytest node id: `<path>.py` or `<path>.py::<name>[::<name>]`, relative to the root.<br>- A `check` decision takes only test entries and a `requirement` decision only requirement entries. A `judgement` decision takes no `enforced_by`.<br>- File problems, each naming the decision's path:<br>&nbsp;&nbsp;- a tier outside the three values;<br>&nbsp;&nbsp;- an entry of the wrong kind for its tier;<br>&nbsp;&nbsp;- `enforced_by` on a `judgement` decision;<br>&nbsp;&nbsp;- a test entry whose `<path>.py` is not a file under the root.<br>- A requirement entry is `want`ed as a `requirement`, so one that names nothing is an unresolved reference.<br>- The field name follows the relation word `enforced by` (glossary: `design-decision enforced by test`; decision-tiers: `enforced by requirement`). |
| D3 | **History needs no tier.** `w_untiered` fires for a decision whose status is not `superseded` or `rejected`, which includes one with no status. The `untiered` condition's prose definition is fixed in place (P10) to say so: "a design-decision that is not `superseded` or `rejected` and whose frontmatter gives no `tier`." A superseded or rejected decision is given no tier. If it is given one anyway, `v_d6` and `v_d7` apply to it as written: r2 and r3 have no status condition. |
| D4 | **The rules in `model.lp`**, after `v_d5`:<br>- `label("v_d6", "a check decision names no test")`, `v_d6(D) :- tier(D, "check"), not has_test(D).`<br>- `label("v_d7", "a requirement decision names no requirement")`, `v_d7(D)`, the same over `enforced_req`.<br>- `label("v_d8", "an accepted decision supersedes one still accepted")`, `v_d8(Old, New) :- supersedes(New, Old), status(New, "accepted"), status(Old, "accepted").` It has arity 2, so each row names both.<br>- `label("w_untiered", "a decision in force gives no tier")`, among the warnings.<br>`#defined tier/2. #defined enforced_test/2. #defined enforced_req/2.` and the four `#show`s. A proposed superseder fires nothing: 0073 → 0033 stays silent, as plan-1 S6 wanted. |
| D5 | **`model decisions --check`.**<br>1. It checks the index first and prints its line, as today.<br>2. For each `check` decision, in file order, it runs `[sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", *entries]` in the root, with `PYTHONDONTWRITEBYTECODE=1`.<br>&nbsp;&nbsp;- Up to 4 decisions run at once (`concurrent.futures.ThreadPoolExecutor`).<br>&nbsp;&nbsp;- Each run has a 600 s timeout (`TIMEOUT`).<br>&nbsp;&nbsp;- `-o addopts=` clears the repository's own `-n auto` and `-m "not … timing"`, so a named test always runs, alone.<br>3. It prints one line a decision:<br>&nbsp;&nbsp;- `holds    <rel> (<id>): <entries, comma-separated>`;<br>&nbsp;&nbsp;- `failing  <rel> (<id>): <entries>: exit <code>`, or `: timed out after 600 s`, then the last 20 lines of pytest's output, indented four spaces;<br>&nbsp;&nbsp;- `failing  <rel> (<id>): names no test`, for a check decision with none.<br>4. It prints the summary `<n> check decisions: <h> hold, <f> failing`.<br>It exits 1 when the index is stale or any decision fails. A pytest exit other than 0 is failing: 1 failed, 4 not found, 5 collected nothing. It writes nothing in the repository. |
| D6 | **design-model-check r52 and decision-tiers r5.** r52 says `--check` "shall exit successfully" on a current index. r5 says it shall exit with an error when a check decision's test fails. Both are kept unchanged: r5 is an unwanted-behaviour ("If … then") line, and in EARS it takes precedence over the plain line. r52's scenario has no `check` decision, so it still passes. decision-tiers' `## Implementation, may change` says so in one bullet. design-model-check is merged to `main`, so changing r52 would mean retiring and replacing it. That is left to the person. |
| D7 | **The sort: who decided, on what evidence.** The planner sorted every decision (the table below) by these rules:<br>- `check`: a test in the suite fails when the decision is broken.<br>- `requirement`: a line of a capability states the decision.<br>- `judgement`: in force, but neither of those.<br>- `superseded`: an accepted decision supersedes it, or it governs the old process that 0074 replaces (D8).<br>The implementer applies the table and checks each row's evidence:<br>- every test entry passes in `model decisions --check`;<br>- every requirement entry resolves, and its line, read, states the decision.<br>A row whose evidence fails drops to `judgement` with no `enforced_by`. A row may move up only with evidence named in the report. Every change from the table is a deviation in the report. The person revisits the sort; nothing waits on that. |
| D8 | **The old process's decisions are superseded by 0074.** The design says obsolete decisions are "retired", but a design-decision has no `retired` status. `0074-the-workflow-simplified` replaces the stages, gates, proposals, rounds and their agents, so its frontmatter gains `supersedes:` naming the 27 decisions marked "0074" below, and each of those becomes `superseded`. 0074 has not been merged, so its frontmatter may be fixed (P10). The machinery those decisions describe still runs until plan 9, and the capabilities' lines describe it until plan 9 retires them. A superseded decision stays as history and is never deleted. |
| D9 | **A new decision supersedes 0046 (light decisions):** `0075-decisions-carry-their-tier.md`. 0046 lists the frontmatter fields, and the tier fields change that list, so 0046 is not edited. Instead, 0075:<br>- restates the list with `tier` and `enforced_by`;<br>- is `accepted`, `supersedes: [design-decision/light-decisions]`;<br>- is `tier: requirement`, `enforced_by: [decision-tiers#r1, decision-tiers#r2, decision-tiers#r3]`;<br>- has `source: [record/2026-11-04-workflow-simplification-design]`. |
| D10 | **Two tier-1 checks get their tests**, in `tests/scripts/test_decision_checks.py`:<br>- the 300-line limit, design goal 7's own example, which `CLAUDE.md` states but no decision or test did: new decision `0076-python-files-stay-at-300-lines.md`, `tier: check`, `enforced_by: [tests/scripts/test_decision_checks.py::test_every_tracked_python_file_is_300_lines_or_fewer]`. The test runs `tools size --limit 300` on the root and expects exit 0 with nothing printed.<br>- 0006 (a feature file is never edited by hand), with `test_the_features_are_what_features_generate_writes` (`features generate --check` on the root, exit 0). The existing live test accepts exit 1, so it does not enforce the decision.<br>No other new test is written for an old decision (YAGNI). |
| D11 | **Frontmatter only.** No `## Decision` section is edited (`integrating-a-proposal`: "never edit an existing decision file"). The tier is the design's own field and the status is what `v_d8` asks for. Adding them is the sort that the design orders once. |
| D12 | **The index gains a `tier` column**, after `status`: `\| decision \| summary \| status \| tier \| supersedes \| revisit when \|`. The person sees each decision's tier where they read the decisions. |
| D13 | **Tier 1 in the bar.** The design asks for "the tier-1 decision checks hold for any constraint the item states". An item states its constraints through the capabilities its lines go into: each capability's `rests_on:` names the decisions it rests on, and that relation already exists. So the bar adds:<br>- for each `check` decision that a capability of the item's lines rests on, run on the root checkout, since tests run on code and the item's lines change none of it: `design-decision <slug> (check) fails: <entries>: exit <code>`, or `… names no test`;<br>- matching by the id's last segment, so that both `design-decision/<slug>` and the full id match;<br>- each decision run once a process (a dict keyed by root and path), so `work batch start` over several items runs it once.<br>The reasons come after the well-formed reasons. `well-formed`'s prose definition gains ", and whose capabilities' `check` design-decisions pass their tests" (P10). decision-tiers' `## Not yet` bullet is removed. readiness' `## Implementation, may change` gains one bullet. `passing` is unchanged. |
| D14 | **Tier 1 at the pull request.** `batch_brief.CHECKS` gains `"python3 {scripts}/model decisions --check"`, so every review brief gives its exit code at the head and at the base (plan-5 S5). "With the suite" is met by the tests themselves, which are in the suite, and by `test_the_live_decisions_keep_their_tiers` (D17). |
| D15 | **Judgement decisions reach the batch's work.** The design says "These go to the batch's plan as context". The batch's tasks are its plan, so building-a-batch step 4's brief gains one bullet: "the `tier: judgement` design-decisions (`grep -l '^tier: judgement' spec/decisions/*.md`), to follow in the code it writes". The reviewer already reads them (plan 5 D6). |
| D16 | **Scenario handlers** live in `tests/scenarios/decision_tiers_handlers.py`.<br>- New registry keys: `GivenK_A design-decision`, `GivenR enforced by`, `GivenR supersedes`, `WhenRuns` `` `model decisions --check` ``.<br>- Keys that another capability already holds are taken through `work_queue_world.local`, each returning `False` for a step that is not its own:<br>&nbsp;&nbsp;- `GivenK test` and `GivenK_C test` (analysis-tools, whose tests import `cart`);<br>&nbsp;&nbsp;- `GivenK_C design-decision` (design-model-check's `headless`);<br>&nbsp;&nbsp;- `ThenDoes use` (batches' `uses_plan`; this one acts only after a `model decisions --check` run).<br>- `test_decision_tiers.py` binds with `bind_all`. |
| D17 | **The live guard** is `tests/scripts/test_decision_checks.py::test_the_live_decisions_keep_their_tiers`. It runs `model check --json` on the root and asserts:<br>- no `w_untiered`, `v_d6`, `v_d7` or `v_d8` row;<br>- no problem naming `spec/decisions/`.<br>It does not run `model decisions --check` inside the suite, since the tests that would run are in the suite already. |
| D18 | **No `--json` for `model decisions --check`.** It is a check, not a query (0058). Add one when a caller needs it. |

### The sort

The status after the sort and the tier of every decision, with what enforces it. The legend:
- "0074" in the status column: superseded by 0074 (D8).
- "superseded (00nn)": an accepted decision supersedes it already, and only its status changes.
- A blank tier: history, so no tier is given (D3).
- An `enforced_by` entry in **bold** must be confirmed by the implementer (D7).

| # | decision (slug) | status after | tier | enforced_by |
|---|---|---|---|---|
| 0001 | one-spec-per-context | accepted | requirement | design-model-check#r36, design-model-check#r38 |
| 0002 | gate-on-behaviour-lines | 0074 | | |
| 0003 | formulation-needs-no-second-approval | 0074 | | |
| 0004 | spec-writers-blind-to-code | 0074 | | |
| 0005 | plans-carry-intent-not-code | 0074 | | |
| 0006 | feature-files-read-only-in-red-green | accepted | check | tests/scripts/test_decision_checks.py::test_the_features_are_what_features_generate_writes |
| 0007 | tests-the-decisions-break | superseded (0044) | | |
| 0008 | slice-budget-refused-by-plan | superseded (0041) | | |
| 0009 | review-by-risk | superseded (0040) | | |
| 0010 | suite-record-holds | superseded (0039) | | |
| 0011 | held-scenarios | 0074 | | |
| 0012 | fresh-agents-short-replies | superseded (0038) | | |
| 0013 | one-batch-one-session | superseded (0037) | | |
| 0014 | controller-per-spec-round | 0074 | | |
| 0015 | scout-on-haiku-at-low-effort | 0074 | | |
| 0016 | an-experiment-is-a-release | accepted | judgement | |
| 0017 | scripts-stdlib-only | superseded (0035) | | |
| 0018 | measure-refuses-unknown-shapes | accepted | requirement | **batch-measurement#r6, batch-measurement#r7** |
| 0019 | superpowers-dependency | superseded (0042) | | |
| 0020 | rules-held-by-agent-tools | superseded (0053) | | |
| 0021 | model-pinned-in-agent-definitions | superseded (0053) | | |
| 0022 | plugin-adopts-the-design-model | superseded (0045) | | |
| 0023 | scenario-names-requirement-by-tag | superseded (0052) | | |
| 0024 | retired-ids-in-capability-frontmatter | accepted | requirement | design-model-check#r4 |
| 0025 | model-check-solves-with-clingo | accepted | requirement | design-model-check#r47, design-model-check#r48 |
| 0026 | work-file-forms | 0074 | | |
| 0027 | capability-ids-are-context-scoped | accepted | requirement | design-model-check#r36, design-model-check#r37 |
| 0028 | plugin-scenarios-run-as-unittest | rejected | | |
| 0029 | one-capability-per-proposal | 0074 | | |
| 0030 | workflow-scenarios-run-as-fixture-sessions | superseded (0065) | | |
| 0031 | held-scenario-formulates-no-requirement | 0074 | | |
| 0032 | model-reads-a-ledger | rejected | | |
| 0033 | glossary-terms-are-standing | accepted | requirement | design-model-check#r22, design-model-check#r23, design-model-check#r24 |
| 0034 | consistency-check-on-demand | 0074 | | |
| 0035 | plugin-takes-the-dependencies-it-needs | accepted | judgement | |
| 0036 | one-requirement-form | accepted | judgement | (a `check` if a test refusing `#behaviour/r<n>` is found; D7) |
| 0037 | a-script-supervises-delivery | 0074 | | |
| 0038 | worker-results-are-files | 0074 | | |
| 0039 | work-item-lifecycle-as-run | 0074 | | |
| 0040 | review-of-work-items | 0074 | | |
| 0041 | the-file-set-is-the-claim | 0074 | | |
| 0042 | superpowers-not-a-dependency | accepted | judgement | |
| 0043 | fixture-scenarios-under-pytest-bdd | superseded (0065) | | |
| 0044 | plans-list-the-tests-they-break | 0074 | | |
| 0045 | final-layout | accepted | requirement | design-model-check#r42 |
| 0046 | light-decisions | superseded (0075) | | |
| 0047 | references-are-ids | accepted | requirement | **design-model-check#r30, design-model-check#r32** |
| 0048 | plugin-scenarios-run-as-pytest-bdd | accepted | check | tests/scripts/test_bound.py::BoundTest::test_every_scenario_has_exactly_one_test |
| 0049 | migration-in-one-pass | accepted | requirement | **migration-tools#r1** |
| 0050 | living-plan-to-work-items | 0074 | | |
| 0051 | behaviour-lines-are-ears | accepted | requirement | design-model-check#r25 |
| 0052 | a-scenario-may-name-several-requirements | superseded (0054) | | |
| 0053 | the-v3-agents | accepted | check | tests/scripts/test_agents.py |
| 0054 | a-scenario-names-one-requirement | accepted | requirement | design-model-check#r10, design-model-check#r11 |
| 0055 | exits-are-successful-or-errors | superseded (0058) | | |
| 0056 | a-failed-work-item | 0074 | | |
| 0057 | work-retry-reads-the-log | 0074 | | |
| 0058 | query-commands-answer-in-their-output | accepted | judgement | |
| 0059 | the-session-keeps-the-gate | superseded (0068) | | |
| 0060 | measure-an-initiative | accepted | requirement | batch-measurement#r1 |
| 0061 | work-items-named-by-ids | 0074 | | |
| 0062 | upgrades-between-plugin-releases | accepted | requirement | migration-tools#r13, migration-tools#r14 |
| 0063 | a-ruling-returns-to-the-asking-stage | superseded (0069) | | |
| 0064 | answers-not-rulings | 0074 | | |
| 0065 | workflow-capabilities-are-guarantees | accepted | judgement | |
| 0066 | the-ledger-is-tracked | 0074 | | |
| 0067 | requests-written-through-work | accepted | judgement | |
| 0068 | the-context-runs-without-a-coordinator | 0074 | | |
| 0069 | an-answer-to-a-reviewer-returns-to-ready-or-done | 0074 | | |
| 0071 | an-asker-is-told-by-its-registered-asker-id | accepted | requirement | **requests#r42, requests#r57** |
| 0072 | work-list-and-work-show-replace-work-status | 0074 (was proposed) | | |
| 0073 | the-glossary-is-a-target-of-spec-work | 0074 (was proposed) | | |
| 0074 | the-workflow-simplified | accepted | judgement | |
| 0075 | decisions-carry-their-tier (new, D9) | accepted | requirement | decision-tiers#r1, decision-tiers#r2, decision-tiers#r3 |
| 0076 | python-files-stay-at-300-lines (new, D10) | accepted | check | tests/scripts/test_decision_checks.py::test_every_tracked_python_file_is_300_lines_or_fewer |

The totals, which Task 3's tests pin:
- 75 decisions: 2 rejected, 19 superseded by an accepted decision, 27 superseded by 0074, and 27 in force.
- The 27 in force: 4 `check` (0006, 0048, 0053, 0076), 15 `requirement` and 8 `judgement`.
- 0053 is old-process in part (the agents of the stages). It stays in force as a `check` because role-boundaries,
  `pr-reviewer` included, holds until plan 9.

## Review Focus

These are the input classes the spec implies but no line's check exercises, most likely to bite first. Each has its
test in the task named.

1. **A check that writes in the repository.** `model decisions --check` runs pytest in the person's checkout, and a
   failing test must not leave `.pytest_cache/` or `__pycache__/` behind. A refused run must change nothing (U3).
   This holds in the scenario repository too, where a test is written fresh.
   Pinned in Task 2: `test_the_check_writes_nothing_in_the_repository`, plus the U3 check on scenario @r5.
2. **The repository's own pytest settings.** This repository's `addopts` are `-n auto` and
   `-m "not fixture and not timing"`. A `check` decision naming a `timing` test must still run that test, alone. A
   test id that pytest cannot find (exit 4), or a file that collects nothing (exit 5), must count as failing, never
   as holding.
   Pinned in Task 2: `test_the_repositorys_addopts_do_not_deselect_a_named_test` and `test_a_test_that_does_not_run_is_failing`
   (parametrised: not found, collects nothing, timed out with `timeout=1`).
3. **An `enforced_by` written wrong.** Examples: a tier `checked`; a test path that is not a file; a requirement id
   on a `check` decision; a test on a `requirement` decision; `enforced_by` on a `judgement` decision; a requirement
   id that names no line. Each should be one file problem or one unresolved reference naming the decision's path, and
   never a silent pass.
   Pinned in Task 1: `test_a_wrong_enforced_by_is_named` (parametrised).
4. **History and supersession.** A `superseded` or `rejected` decision with no tier gives no warning. A `proposed`
   decision superseding an `accepted` one gives no `v_d8`. A chain A → B → C fires only for the accepted → accepted
   pairs. A decision with no `status:` is in force.
   Pinned in Task 1: `test_history_needs_no_tier` and `test_v_d8_fires_only_for_accepted_pairs`.
5. **The bar's match against `rests_on`.** Capabilities write both `design-decision/<slug>` and the full id. A
   `check` decision must be found under either. A decision that no capability of the item rests on must not run.
   `work batch start` over several items must run each decision once.
   Pinned in Task 4: `test_a_failing_check_decision_the_capability_rests_on_is_a_reason` (both forms),
   `test_a_decision_the_capability_does_not_rest_on_is_not_run` and `test_each_decision_runs_once_a_process`.

---

### Task 1: `model check` keeps each decision to its tier (r1, r2, r3, r6)

**Files:**
- Create: `scripts/model_decisions.py` (minimal, below), `tests/scripts/test_model_tiers.py`,
  `tests/scenarios/decision_tiers_handlers.py`
- Modify:
  - `scripts/model_work.py`: `read_decisions` reads `tier` and `enforced_by`.
  - `scripts/model.lp`: D4.
  - `scripts/model_report.py`: the `tier` column (D12).
  - `scripts/model`: the contract's text names the fields, the four codes and D3.
  - `tests/scenarios/test_decision_tiers.py`: binds with `bind_all`.
  - `spec/capabilities/decision-tiers.md`: `unbuilt: [r4, r5]`; the `untiered` definition (D3); one Implementation
    bullet naming the fields (D2) and D3.
  - `spec/decisions/index.md`: regenerated.
  - `CLAUDE.md`: `decision-tiers` in the `<capability>_handlers*.py` row.
- A minimal `scripts/model_decisions.py` holds only what `model_work` needs: `TIERS`, `split(entries)` and
  `test_file(entry)`. Task 2 grows it, and its module-map row lands in Task 2.

**Interfaces:**
- Produces, in `model_decisions.py`:
  - `TIERS = ("check", "requirement", "judgement")`.
  - `split(entries) -> tuple[list[str], list[str]]`: `(tests, requirements)`. An entry holding `#` is a requirement.
  - `test_file(entry) -> str`: the part before the first `::`.
- Produces, as facts of `Model.read()`: `tier(D, T)`, `enforced_test(D, Entry)`, `enforced_req(D, Q)` (Q as
  `resolve_req` qualifies it), and the D2 problems in `model.problems`.
- Produces, in `decision_tiers_handlers.py`:
  - `decision(step, name, tier=None, status="accepted") -> Path`: writes `spec/decisions/<name>.md` with its id, a
    summary, the tier and a `## Decision` section, and sets `says[name] = "spec/decisions/<name>.md"`.
  - `field(step, name, key, value)`: sets or replaces one frontmatter line of that file.
  - The handlers of D16 that r1, r2, r3 and r6 use: `GivenK_A design-decision` (a value in `TIERS` is the tier,
    any other is the status), the local `GivenK_C design-decision` (`untiered`, `untested`, `unrequired` write
    nothing, and any other returns `False`), and `GivenR supersedes`.

- [x] **Step 1: Write the failing script tests** (`test_model_tiers.py`, a `ModelTest` subclass from `test_model`,
  `self.good()` first, solved with `self.check_json()`):
  - `test_w_untiered_names_a_decision_with_no_tier`: one accepted decision with no tier gives one `w_untiered` row
    naming its id. With `tier: judgement` it gives none.
  - `test_history_needs_no_tier` (Review Focus 4): `superseded` and `rejected` give no row; no `status:` gives one.
  - `test_v_d6_a_check_decision_with_no_test`: `tier: check` with no `enforced_by` gives `v_d6`. With
    `enforced_by: [tests/test_x.py::test_x]` and that file written, it gives none.
  - `test_v_d7_a_requirement_decision_with_no_requirement`: `tier: requirement` gives `v_d7`. With
    `enforced_by: [thing#r1]` (the fixture's capability) it gives none and no unresolved reference.
  - `test_v_d8_fires_only_for_accepted_pairs` (Review Focus 4): with A → B → C, where A and B are accepted and C is
    accepted, the rows are `[B, A]` and `[C, B]`. With C `superseded`, only `[B, A]`. With A `proposed`, only
    `[C, B]`.
  - `test_a_wrong_enforced_by_is_named` (Review Focus 3), parametrised. Each case is one problem or unresolved
    reference holding the decision's path and the words given:
    - `tier: checked` → `checked`;
    - a `check` with `enforced_by: [tests/missing.py]` → `tests/missing.py`;
    - a `check` with `[thing#r1]` → `thing#r1`;
    - a `requirement` with `[tests/test_x.py]` → `tests/test_x.py`;
    - a `judgement` with `[thing#r1]` → `enforced_by`;
    - a `requirement` with `[thing#r9]` → an unresolved reference naming `thing#r9`.
  - `test_the_index_gives_the_tier`: `render_decisions` has the D12 header and `judgement` in the row of a judgement
    decision.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_model_tiers.py -q | tail -3`
  Expected: FAIL. There is no `model_decisions`, no `w_untiered` row, and no `tier` column.

- [x] **Step 3: Implement D2-D4 and D12.** Write `model_decisions.py` (TIERS, `split`, `test_file`) and the
  `read_decisions` lines (at most 19 more). Add the rules and labels to `model.lp`, `w_untiered` among the warnings,
  and the column to `render_decisions`. Then write the contract lines in `scripts/model`.

- [x] **Step 4: Run them, and the model tests.**
  Run: `python3 -m pytest tests/scripts/test_model_tiers.py tests/scripts/test_model.py tests/scripts/test_model_output.py tests/scripts/test_model_withdrawn.py tests/scripts/test_model_reading.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: Write the scenario handlers, take r1, r2, r3, r6 out of `unbuilt:`, and edit the `untiered`
  definition.** Switch `test_decision_tiers.py` to `bind_all`.
  Run: `python3 -m pytest tests/scenarios/test_decision_tiers.py tests/scenarios/test_design_model_check.py -q | tail -1`
  Expected: decision-tiers shows `4 passed, 2 xfailed`. design-model-check passes as before, `headless` (r40)
  included.

- [x] **Step 6: Check the vocabulary and the generated feature.**
  Run: `python3 scripts/features vocab --check | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/model lexicon --check | tail -1; python3 scripts/model logic | tail -1`
  Expected: `every step has one handler`; exit 0 (the `untiered` edit changes no step); `401 terms, 0 problems`;
  `11 findings: 6 L5, 5 L6`.

- [x] **Step 7: Mutations, each reverted.** Each must turn its test red:
  - `v_d8` without the `status(New, "accepted")` clause fails `test_v_d8_fires_only_for_accepted_pairs`;
  - `w_untiered` without the history clauses fails `test_history_needs_no_tier`;
  - r6 left in `unbuilt:` fails the suite as `XPASS(strict)`.

- [x] **Step 8: Regenerate the index; the baselines.**
  Run: `python3 scripts/model decisions && python3 scripts/model decisions --check; python3 -m pytest -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/model_decisions.py scripts/model_work.py scripts/model_report.py tests/scripts/test_model_tiers.py tests/scenarios/decision_tiers_handlers.py tests/scenarios/test_decision_tiers.py`
  Expected:
  - `spec/decisions/index.md is current`;
  - the suite: `10 xfailed`, no failures, passed = 1356 + 4 scenarios + the new script tests;
  - `model check`: `72 violations, 87 warnings, 19 unresolved references, 0 file problems` (the planned path);
  - `size` silent, with `model_work.py` ≤ 285;
  - `check` clean.

- [x] **Step 9: Commit.**
  ```bash
  git add scripts/model_decisions.py scripts/model_work.py scripts/model.lp scripts/model_report.py scripts/model \
    tests/scripts/test_model_tiers.py tests/scenarios/decision_tiers_handlers.py tests/scenarios/test_decision_tiers.py \
    spec/capabilities/decision-tiers.md spec/decisions/index.md CLAUDE.md
  git commit -m "model: a decision's tier and what enforces it, w_untiered, v_d6, v_d7, v_d8 (decision-tiers r1, r2, r3, r6)"
  ```

### Task 2: `model decisions --check` runs the tests of the `check` decisions (r4, r5)

**Files:**
- Modify:
  - `scripts/model_decisions.py`: the runs and the report (D5).
  - `scripts/model_report.py`: `cmd_decisions` with `--check` adds the decisions' report after the index line.
  - `scripts/model`: the contract's `decisions` paragraph.
  - `tests/scenarios/decision_tiers_handlers.py`: the r4 and r5 handlers.
  - `spec/capabilities/decision-tiers.md`: `unbuilt: []`; Implementation bullets for D5 and D6.
  - `CLAUDE.md`: the row for `scripts/model_decisions.py`: "the tiers of `spec/decisions/`: the `enforced_by`
    entries told apart, and `model decisions --check`'s runs of each `check` decision's tests (decision-tiers)".
- Create: `tests/scripts/test_model_decisions.py`

**Interfaces:**
- Consumes: Task 1's `TIERS`, `split`, `test_file`.
- Produces, in `model_decisions.py`:
  - `@dataclass Decision: rel: str, ident: str, status: str | None, tier: str | None, tests: list[str],
    requirements: list[str], summary: str`.
  - `decisions(root) -> list[Decision]`, in file order, read with `model_parse.frontmatter` over `decision_files`.
  - `TIMEOUT = 600`, `WORKERS = 4`, `TAIL = 20`.
  - `@dataclass Ran: decision: Decision, code: int | None, tail: str`, where `code` is `None` on a timeout.
    `ran.holds` is `code == 0`.
  - `run(root, decision, timeout=TIMEOUT) -> Ran`: the D5 command for one decision.
  - `check_tests(root, timeout=TIMEOUT) -> list[Ran]`: every `check` decision, run `WORKERS` at a time, returned in
    file order. A check decision with no test gives `Ran(code=None, tail="names no test")` with no pytest run.
  - `report(ran) -> tuple[list[str], bool]`: the D5 lines and whether all hold.
- `model decisions --check` prints the index line, then `report`'s lines. It exits 1 when either fails.
- Produces, in `decision_tiers_handlers.py`:
  - the local `GivenK test`: writes `tests/test_<t>.py` holding `def test_<t>():`, which appends `<t>` to
    `<outside>/ran` (an absolute path from `tmp_path_factory`, outside the repository) and passes. It sets
    `says[t] = "tests/test_<t>.py::test_<t>"`.
  - the local `GivenK_C test`: `failing` rewrites that test's body to also `assert False`. Any other condition returns
    `False`.
  - `GivenR enforced by`: adds the object's `says` to the decision's `enforced_by:`.
  - `WhenRuns` `` `model decisions --check` ``: `model decisions` (writing the index), then `model decisions --check`
    through design-model-check's `run_model`. It sets `context["decisions_run"]`.
  - the local `ThenDoes use`: only when `decisions_run` is set (otherwise it returns `False`). It asserts that the
    test's id is printed on a `holds` or `failing` line and that `<outside>/ran` holds `<t>`.

- [ ] **Step 1: Write the failing tests** (`test_model_decisions.py`, on a `tmp_path` repository: `spec/decisions/`
  with decision files written by a helper and `tests/test_*.py` files; `model` run through `subprocess` as
  `test_model_output.py` does):
  - `test_a_passing_check_decision_holds`: exit 0; the index line, `holds    spec/decisions/a.md (design-decision/…/a): tests/test_a.py::test_a`,
    and `1 check decisions: 1 hold, 0 failing`.
  - `test_a_failing_test_names_its_decision`: exit 1; a `failing  spec/decisions/b.md` line with `exit 1` and the
    assertion's text in the indented tail; `a` still `holds`.
  - `test_a_check_decision_with_no_test_is_failing`: `failing  … names no test`, exit 1.
  - `test_only_check_decisions_run`: `requirement` and `judgement` decisions print nothing, and their entries'
    files (which would fail) are not run.
  - `test_a_stale_index_still_runs_the_tests`: a stale index prints its message and the decisions' lines, exit 1.
  - `test_a_test_that_does_not_run_is_failing` (Review Focus 2), parametrised, each `failing`:
    - `tests/test_a.py::test_nothing` → `exit 4`;
    - an empty `tests/test_e.py` → `exit 5`;
    - a test sleeping 5 s with `check_tests(root, timeout=1)` → `timed out after 1 s`.
  - `test_the_repositorys_addopts_do_not_deselect_a_named_test` (Review Focus 2): the repository's `pytest.ini` has
    `addopts = -m "not timing"`, and a `@pytest.mark.timing` test is named; it runs (`<outside>/ran` holds its name)
    and holds.
  - `test_the_check_writes_nothing_in_the_repository` (Review Focus 1): after a run with one passing and one failing
    test, the repository's files (every path but `.git`) are exactly those before it. That means no `.pytest_cache`
    and no `__pycache__`.
  - `test_the_decisions_run_side_by_side`: three decisions, each sleeping 1 s, finish in under 2.5 s.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_model_decisions.py -q | tail -3`
  Expected: FAIL. `--check` prints only the index line.

- [ ] **Step 3: Implement D5** in `model_decisions.py` and `cmd_decisions`.

- [ ] **Step 4: Run them, and design-model-check's `model decisions` scenarios.**
  Run: `python3 -m pytest tests/scripts/test_model_decisions.py tests/scenarios/test_design_model_check.py -q -k "decisions or Decision" | tail -1`
  Expected: all pass; r50, r51 and r52 are unchanged.

- [ ] **Step 5: The r4 and r5 handlers; take r4 and r5 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scenarios/test_decision_tiers.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: `6 passed`; `every step has one handler`.

- [ ] **Step 6: Mutations, each reverted.** Each must turn its test red:
  - dropping `-o addopts=` fails `test_the_repositorys_addopts_do_not_deselect_a_named_test`;
  - dropping `-B` (or `-p no:cacheprovider`) fails `test_the_check_writes_nothing_in_the_repository`, and scenario
    @r5 fails U3;
  - treating exit 5 as holding fails the `exit 5` case.

- [ ] **Step 7: The live run and the baselines.**
  Run: `time python3 scripts/model decisions --check; python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/model_decisions.py scripts/model_report.py tests/scripts/test_model_decisions.py tests/scenarios/decision_tiers_handlers.py`
  Expected:
  - live: the index line and `0 check decisions: 0 hold, 0 failing`, exit 0, since no decision is tiered yet;
  - the suite: `8 xfailed`, no failures;
  - `size` silent;
  - `check` clean.

- [ ] **Step 8: Commit.**
  ```bash
  git add scripts/model_decisions.py scripts/model_report.py scripts/model tests/scripts/test_model_decisions.py \
    tests/scenarios/decision_tiers_handlers.py spec/capabilities/decision-tiers.md CLAUDE.md
  git commit -m "model: model decisions --check runs each check decision's tests and names a failing one (decision-tiers r4, r5)"
  ```

### Task 3: The decisions sorted into tiers

**Files:**
- Create:
  - `spec/decisions/0075-decisions-carry-their-tier.md` (D9);
  - `spec/decisions/0076-python-files-stay-at-300-lines.md` (D10);
  - `tests/scripts/test_decision_checks.py`.
- Modify:
  - the frontmatter of every `spec/decisions/00*.md` that the sort's table changes;
  - `0074`'s `supersedes:` (D8);
  - `spec/decisions/index.md`, regenerated.

**Interfaces:**
- Consumes: Task 1's rules and Task 2's `model decisions --check`; `batch_brief.judgement(root)` (plan 5).
- The two new decisions are written in 0046's light form, with `id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/<slug>`,
  `summary`, `date: 2026-11-05`, `status: accepted`, `source: [record/2026-11-04-workflow-simplification-design]`,
  `by: "workflow simplification plan 6"`, `tier`, `enforced_by` and a `## Decision` section of one paragraph:
  - 0075: "A decision file's frontmatter is id, summary, date, status, supersedes, revisit_when, source, by, tier and,
    for a `check` or `requirement` decision, enforced_by naming the tests or the requirements that enforce it; a
    decision in force gives its tier, and a superseded or rejected one needs none. It replaces 0046's list of fields."
    It also has `supersedes: [design-decision/light-decisions]`.
  - 0076: "Every tracked Python file stays at 300 lines or fewer; `tools size --limit 300` prints each one over it and
    exits 1, and the suite fails on it."

- [ ] **Step 1: Write the failing tests** (`test_decision_checks.py`, on the repository root):
  - `test_every_tracked_python_file_is_300_lines_or_fewer` (D10): `tools size --limit 300` exits 0 and prints
    nothing.
  - `test_the_features_are_what_features_generate_writes` (D10): `toolchain.require()`, then
    `features generate --check` exits 0.
  - `test_the_live_decisions_keep_their_tiers` (D17): `toolchain.require()`, then `model check --json` has no rows of
    `w_untiered`, `v_d6`, `v_d7` or `v_d8`, and no problem naming `spec/decisions/`.
  - `test_the_sort_holds_its_totals`: by `model_decisions.decisions(ROOT)`:
    - 75 decisions;
    - status counts `{"accepted": 27, "superseded": 46, "rejected": 2}`;
    - tiers over the accepted ones `{"check": 4, "requirement": 15, "judgement": 8}`, or the table's totals as
      changed by the report's deviations (D7);
    - no superseded or rejected decision with a tier.
  - `test_the_judgement_decisions_reach_the_brief`: `batch_brief.judgement(ROOT)` lists
    `spec/decisions/0074-the-workflow-simplified.md` among 8 entries.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_decision_checks.py -q | tail -3`
  Expected:
  - The size and generate tests pass. Each is the new form of a rule that holds already. Note this in the report as
    "passed at RED, by design".
  - The tiers test fails with 71 `w_untiered` and 19 `v_d8` rows.
  - The totals and judgement tests fail.

- [ ] **Step 3: Apply the sort.**
  - For each row of the table, set `status:` (and `tier:`/`enforced_by:` where given) in its frontmatter, adding a
    field after `status:` and touching no other line.
  - Write 0074's `supersedes:` as the 27 "0074" slugs in the short form `design-decision/<slug>`, one list.
  - Write 0075 and 0076.
  - Then confirm each row's evidence (D7):
    - read each requirement entry's line in its capability, and check that it states the decision;
    - for each **bold** entry, run `python3 scripts/model why <entry>` to see the line.
  - A row whose evidence fails drops to `judgement`, and its row in the report says why.

- [ ] **Step 4: Regenerate the index; run the check decisions live.**
  Run: `python3 scripts/model decisions && time python3 scripts/model decisions --check`
  Expected: `spec/decisions/index.md is current`; four `holds` lines (0006, 0048, 0053, 0076);
  `4 check decisions: 4 hold, 0 failing`; exit 0. Record the wall time; it is expected to be under 30 s.

- [ ] **Step 5: Run the tests again, and `model check`.**
  Run: `python3 -m pytest tests/scripts/test_decision_checks.py tests/scripts/test_batch_brief.py -q | tail -1; python3 scripts/model check | tail -1`
  Expected: all pass; `53 violations, 16 warnings, 19 unresolved references, 0 file problems`, back to the baseline
  as planned, since the only rows left are the `.shop/work/` ones.

- [ ] **Step 6: Mutations, each reverted.** Each must turn its test red:
  - 0012's status set back to `accepted` gives one `v_d8` row and fails the tiers test;
  - 0076's `enforced_by` removed gives `v_d6`;
  - a temporary 301-line Python file, `git add`ed, fails both 0076's test and `model decisions --check`, which names
    0076. Take it out with `git rm -f` on its own (the person's rule).

- [ ] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/features generate --check; python3 scripts/tools size --limit 300; python3 scripts/tools check tests/scripts/test_decision_checks.py`
  Expected: `8 xfailed`, no failures; `11 findings: 6 L5, 5 L6`; `401 terms, 0 problems`; exit 0; silent; clean.

- [ ] **Step 8: Commit.**
  ```bash
  git add spec/decisions tests/scripts/test_decision_checks.py
  git commit -m "spec: the decisions sorted into tiers; the old process's decisions superseded by the-workflow-simplified; 0075 and 0076"
  ```

### Task 4: Tier 1 in the readiness bar and at the pull request; judgement in the batch's briefs

**Files:**
- Modify:
  - `scripts/readiness_bar.py`: `decision_reasons` (D13), called from `check`.
  - `scripts/batch_brief.py`: `CHECKS` (D14).
  - `skills/building-a-batch/SKILL.md`: step 4's bullet (D15).
  - `tests/scripts/test_skill_building_a_batch.py`: one pinned test.
  - `spec/index.md`: `well-formed` (D13).
  - `spec/capabilities/readiness.md`: one Implementation bullet.
  - `spec/capabilities/decision-tiers.md`: the `## Not yet` bullet removed, leaving `- None.`.
- Create: `tests/scripts/test_readiness_decisions.py`

**Interfaces:**
- Consumes: `model_decisions.decisions`, `model_decisions.run` (Task 2); `backlog_lines.read`, `capability_file`;
  `spec_read.capability(path).frontmatter["rests_on"]`.
- Produces, in `readiness_bar.py`:
  - `rested_on(root, blocks) -> list[model_decisions.Decision]`: the `check` decisions that a capability of the
    blocks rests on, matched by the id's last segment, in file order, each once.
  - `decision_reasons(root, blocks) -> list[str]`: D13's reasons. Each run is cached in `_RAN: dict[tuple[str, str],
    Ran]`, keyed by the resolved root and the decision's path.
  - `check(root, item, others=())` returns `unsettled + well-formed reasons + decision_reasons` as reasons. The
    warnings are unchanged.

- [ ] **Step 1: Write the failing tests** (`test_readiness_decisions.py`, on `ready_repo`). Each test writes
  `spec/decisions/c.md` (`tier: check`, `enforced_by: [tests/test_c.py::test_c]`) and `tests/test_c.py`, makes the
  fixture's `work-queue` capability rest on it, and commits:
  - `test_a_failing_check_decision_the_capability_rests_on_is_a_reason`, parametrised over the `rests_on` forms
    `design-decision/c` and the full id. A shaped item with a passing line into `work-queue` and a failing
    `test_c`: `work ready` exits 1 naming `design-decision c (check) fails` and `tests/test_c.py::test_c`. The item
    stays `shaped`.
  - `test_a_passing_check_decision_readies`: with `test_c` passing, `work ready` readies the item.
  - `test_a_decision_the_capability_does_not_rest_on_is_not_run`: with `rests_on: []`, a failing `test_c` does not
    refuse, and `test_c` did not run (its marker file outside the repository is absent).
  - `test_a_check_decision_with_no_test_is_a_reason`: `… names no test`.
  - `test_each_decision_runs_once_a_process`: with `model_decisions.run` monkeypatched to count, two items' `check`
    in one process run it once.
  - `test_the_decisions_come_after_the_lines`: an item with a line that does not parse and a failing check decision
    names both, the parse reason first.

  In `test_skill_building_a_batch.py`, add `test_the_subagent_reads_the_judgement_decisions`: step 4's text holds
  `tier: judgement`. In `test_batch_brief.py` nothing changes; add to `test_decision_checks.py`
  `test_the_review_runs_the_check_decisions`: `"python3 {scripts}/model decisions --check" in batch_brief.CHECKS`.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_readiness_decisions.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_decision_checks.py -q | tail -3`
  Expected: FAIL. No decision reason exists, step 4 says nothing of tiers, and `CHECKS` has four entries.

- [ ] **Step 3: Implement D13-D15**, and edit `well-formed`, readiness' Implementation bullet and decision-tiers'
  `## Not yet`.

- [ ] **Step 4: Run them, the bar's and the batch's tests, and the readiness and batches scenarios.**
  Run: `python3 -m pytest tests/scripts/test_readiness_decisions.py tests/scripts/test_readiness_bar.py tests/scripts/test_batch_pick.py tests/scripts/test_batch_brief.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_decision_checks.py tests/scenarios/test_readiness.py tests/scenarios/test_batches.py -q | tail -1`
  Expected: all pass. The fixture's capabilities rest on no `check` decision, so no earlier test changes.

- [ ] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - matching `rests_on` by the full id only fails the short-form case;
  - dropping the cache fails `test_each_decision_runs_once_a_process`.

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/features generate --check; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/readiness_bar.py scripts/batch_brief.py tests/scripts/test_readiness_decisions.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_decision_checks.py`
  Expected: `8 xfailed`, no failures; `401 terms, 0 problems`; `11 findings: 6 L5, 5 L6` (the `well-formed` edit is
  prose); exit 0; silent, with `readiness_bar.py` ≤ 160; clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add scripts/readiness_bar.py scripts/batch_brief.py skills/building-a-batch/SKILL.md \
    tests/scripts/test_readiness_decisions.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_decision_checks.py \
    spec/index.md spec/capabilities/readiness.md spec/capabilities/decision-tiers.md
  git commit -m "readiness: the check decisions an item's capabilities rest on join the bar; the review runs model decisions --check; the batch's subagents read the judgement decisions"
  ```

### Task 5: Whole-plan verification and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-6-implementation.md`
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every requirement of the plan is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print('decision-tiers' in d, sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `False 9 []`.

- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 -m pytest -m timing -n 0 -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; time python3 scripts/model decisions --check | tail -1; python3 scripts/features generate --check; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only 95178ceb...HEAD -- '*.py')`
  Expected:
  - the suite: `8 xfailed`, no failures. Passed = 1356 + 6 decision-tiers scenarios + the new script tests, and the
    subtests stay 135;
  - the timing run: `1 passed`;
  - `model check`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: `401 terms, 0 problems`;
  - `decisions --check`: `4 check decisions: 4 hold, 0 failing` (or the sort's count after deviations), exit 0, and
    its time;
  - `generate --check`: exit 0;
  - `vocab --check`: `every step has one handler`;
  - `bindings --unbound`: `every binding names a scenario`;
  - `size`: silent;
  - `check`: clean.

- [ ] **Step 3: A smoke run of the bar's tier-1 check**, in bash, in a scratch repository under the job's tmp
  directory. Each `cp` and each `rm` is its own command (the person's rule).
  ```bash
  d=$(mktemp -d -p /home/vscode/.claude/jobs/7e9ba079/tmp) && git -C "$d" init -q -b main && git -C "$d" config user.name t && git -C "$d" config user.email t@example.com
  cp -r tests/scripts/fixtures/generate/repo/spec "$d/"
  rm "$d/spec/capabilities/legacy.md"
  sed -i 's#^id: bounded-context/.*#id: bounded-context/ex.com/prod/ctx#' "$d/spec/index.md"
  mkdir -p "$d/tests" "$d/spec/decisions" && printf 'def test_c():\n    assert False\n' > "$d/tests/test_c.py"
  printf -- '---\nid: design-decision/ex.com/prod/ctx/c\nsummary: s\nstatus: accepted\ntier: check\nenforced_by: [tests/test_c.py::test_c]\n---\n# c\n\n## Decision\nSo.\n' > "$d/spec/decisions/c.md"
  sed -i 's#^rests_on: .*#rests_on: [design-decision/c]#' "$d/spec/capabilities/work-queue.md"
  git -C "$d" add -A && git -C "$d" commit -qm init
  r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }
  W idea "Abandon a started initiative" && W shape b1 && W line b1 --into work-queue 'When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`.'
  W ready b1; echo "exit $?"; python3 "$r/scripts/model" --root "$d" decisions; python3 "$r/scripts/model" --root "$d" decisions --check; echo "exit $?"; git -C "$d" status --porcelain
  ```
  Then make `test_c` pass (`printf 'def test_c():\n    pass\n' > "$d/tests/test_c.py"`), commit, and run
  `W ready b1` again.
  Expected:
  - the first `ready` exits 1 naming `design-decision c (check) fails` and `tests/test_c.py::test_c`;
  - `decisions --check` exits 1 with `failing  spec/decisions/c.md`;
  - `status --porcelain` shows only `spec/decisions/index.md`, which `model decisions` wrote, with no
    `.pytest_cache` or `__pycache__`;
  - the second `ready` readies b1.

  Record the time of each `ready`.

- [ ] **Step 4: Write the implementation report** at `plan-6-implementation.md`, in `plan-5-implementation.md`'s form
  (no frontmatter):
  - Final state: each Step 2 figure as measured, and the smoke run's times.
  - The commits: a table of each task's commit, what was done and its verification, the mutations included.
  - The sort as applied: every row that differs from the plan's table, with its evidence, and the final totals.
  - Deviations, each with its reason.
  - D1-D18, each kept or changed.
  - Open problems for plans 7-9. Among them:
    - design-model-check r52 against decision-tiers r5 (D6), left for the person;
    - plan 9's retirement decision for the old capabilities may supersede 0053 and narrow 0065;
    - plan 7's knob changes are to be recorded as decisions with their figures (design goal 8);
    - 0060 is superseded when plan 7 builds `measure batch`;
    - `model decisions --check` has no `--json` (D18).
  - Files.

- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-6-decision-tiers.md`:
  `| \`2026-11-04-workflow-simplification/plan-6-implementation.md\` | plan 6 executed: decisions in tiers (\`tier\`, \`enforced_by\`, \`w_untiered\`, \`v_d6\`-\`v_d8\`, \`model decisions --check\` running the check decisions' tests), the 73 decisions sorted and the old process's superseded by the-workflow-simplified, tier 1 in the readiness bar and the review's checks, 6 requirements out of \`unbuilt:\` | report |`.
  Tick every box of this plan.

- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-6-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-6-decision-tiers.md
  git commit -m "records: plan 6 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-6-review.md`. It reads `<this plan's
  commit>..HEAD` on `workflow-simplification` against this plan's Review Focus and the sort's table.
