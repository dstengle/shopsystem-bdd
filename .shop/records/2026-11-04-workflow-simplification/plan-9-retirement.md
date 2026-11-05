---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Plan 9: Retirement and the 2.0 step — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire the old workflow and release plugin 2.0.0:
- the old capabilities' requirement lines are retired, with their ids;
- `work run`, the old queue's commands, `measure initiative`, and the agents and skills built for the old stages are
  deleted;
- `.shop/work/` is frozen as history;
- `migrate upgrade` gains the 2.0.0 step that moves a 1.0.x repository to the new workflow without loss;
- this repository is upgraded by that step.

This is the last plan of the workflow simplification (roadmap row 9, depending on plans 2-8).

**Architecture:**
- **Shared plumbing first (Task 1).** The kept modules (backlog, batches, intake, readiness, conversation, telemetry)
  import `Refused`, the frontmatter reading, the context path and the commit helper from `workqueue.py`, and the
  transcript readers from `measure_read.py`. Task 1 moves those into `scripts/shop_files.py` and
  `scripts/transcripts.py`. It also renames the request modules (`request_moves.py`, `request_lines.py`) and moves
  `is_guarantees` into `spec_read`. After it, no kept module imports a module that a later task deletes, and a test
  holds that rule. Every later deletion is then a deletion only.
- **Retire, then delete, one concern a commit.** Each task retires the lines of one concern and deletes the code,
  tests, handlers, agents and skills that only those lines needed, in the same commit, so the suite is green at every
  commit:
  - Task 2: the guarantees capabilities of the stages;
  - Task 3: `work run` and supervision;
  - Task 4: the queue, delegations and the hooks' initiative text;
  - Task 5: `model check` on `.shop/work/`;
  - Task 7: `measure initiative`.

  A one-off helper, committed as a record, does the spec side the same way every time.
- **A retired capability keeps its file (D3).** Its Behaviour is emptied and every id goes into `retired:`. Each 0.29
  id that only its retired groups restated goes under a `## Dropped` with the reason. Its Terms stay, so the lexicon
  does not move. It is listed under a "Retired in 2.0.0" table in `spec/index.md`. A service capability with no group
  has no feature file (D4).
- **Frozen means read by nothing, written by nothing (D5, D6).** No command writes under `.shop/work/` after
  Task 4. `model check` reads no node, fact or reference from it after Task 5, except the `source` ids it still cites
  observations with. Live requests move to `.shop/requests/` (Task 6). The 2.0.0 step (Task 9) writes
  `.shop/work/FROZEN.md` and moves each live request from another context there. It regenerates the decisions index
  and lists every open thing that it leaves.
- **The release (Tasks 9, 10).** `plugin.json` goes to 2.0.0 with the step. Task 10 then runs `migrate upgrade` on
  this repository itself and enters the surviving open work as backlog items.

**Tech Stack:** Python 3.11 (standard library), git, clingo, GF/pgf, pytest with xdist and pytest-bdd.

**Spec:** read first:
- `design.md` in this folder: §§ "What is kept and what goes", "Migration", "Constraints" (retire, never edit; the
  300-line limit), "The session's calls" (no compatibility layer for peers on 1.x);
- `roadmap.md` row 9;
- the rulings of plans 1-8 (`plan-<n>-rulings.md`), above all plan-1 P10 (a line never merged to `main` may be fixed
  in place) and S10, plan-6 "For plan 9", plan-7 "For plan 9", and plan-8 Q2 and S2;
- `spec/decisions/0024-retired-ids-in-capability-frontmatter.md`;
- `spec/capabilities/formulation.md`, the existing example of a capability kept as the record of where its lines
  went;
- `scripts/migrate_upgrade.py` and `migrate_upgrade_codified.py`, the 1.0.0 step's pattern.

## Global Constraints

- **Branch:** `workflow-simplification`, from `19e9fee5` or later. All plans are built on this one branch. No new
  branch, no push.
- **Shell rule (the person's):** never combine `cp` and `rm` in one command, since together they need the person's
  approval. Run them as separate commands, or leave scratch directories under
  `/home/vscode/.claude/jobs/7e9ba079/tmp` (this plan's: `/home/vscode/.claude/jobs/7e9ba079/tmp/p9`). Keep shell
  variables few. Delete tracked files with `git rm` (`git rm -r` for a directory) and rename them with `git mv`,
  never `rm`/`mv`.
- **No skipping, no weakening.**
  - A test is deleted only in the commit that deletes the code, line or handler it tests. No test is skipped or
    xfailed to get green.
  - Every task brackets its commit with a collection diff. Before the task, run
    `python3 -m pytest --collect-only -q -n 0 -p no:cacheprovider | grep '::' | sort > /home/vscode/.claude/jobs/7e9ba079/tmp/p9/ids-before-<task>.txt`.
    After it, write the same to `ids-after-<task>.txt`, then
    `comm -23 ids-before-<task>.txt ids-after-<task>.txt`.
  - Each removed id must be in a file the task deletes, a scenario of a line the task retires, or a test the task
    names. The implementation report gives each task's count of removed ids.
- **The gate (G)**, run before every commit; every figure must be as the task states:
  ```bash
  python3 -m pytest -q -p no:cacheprovider | tail -1
  python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1
  python3 scripts/model lexicon --check | tail -1; python3 scripts/model decisions --check | tail -1
  python3 scripts/model restates | tail -1
  python3 scripts/features generate --check; echo "generate $?"
  python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound | tail -1
  python3 scripts/tools size --limit 300; echo "size $?"
  python3 scripts/tools check $(git diff --name-only --diff-filter=d HEAD -- '*.py' scripts/work scripts/model scripts/measure scripts/migrate scripts/features scripts/tools)
  python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print(d, sum(map(len,d.values())), u.problems(pathlib.Path('.')))"
  ```
  The last line must print `{} 0 []` throughout. If a check other than the suite (`model check` and the like) moves
  in a way the task does not predict, stop and explain why in the report before committing.
- **File size:** every tracked Python file stays at 300 lines or fewer. `scripts/work` (219 today) shrinks.
- **Module map:** each commit that deletes a module removes its `CLAUDE.md` row (or the module's name from a shared
  row). Each commit that creates a module adds its row. Task 8 sweeps the map once more.
- **Retire, never edit (the person's rule, memory `requirements-retire-not-edit`):**
  - The 0.29 lines are the ones merged to `main` (`main` is at plugin 0.29.0, `96818f71`). Each stays covered:
    restated by a kept group, or listed under `## Dropped` with a reason. `model restates` must end with 0 missing.
  - A codified line (`[r<n>]` of `language: codified-1`) whose behaviour goes is retired: its id goes into its
    capability's `retired:`, and it is never reworded or reused.
  - Under plan-1 P10 a codified line that was never merged may be fixed in place. This plan uses P10 only for the
    example data of migration-tools r14 and r19 (D17). No other line, group title or given block is edited.
  - New lines are added only where a task says so (migration-tools r24).
- **Frozen history:** no task changes, moves or deletes anything under `.shop/work/` except Task 10's run of
  `migrate upgrade`, which writes `.shop/work/FROZEN.md` and moves the live requests it names. Records under
  `.shop/records/` are never edited; new records are added and indexed.
- **Baselines** (measured at `19e9fee5` on this machine):
  - Suite: `1582 passed, 1 skipped, 135 subtests passed` (30.5 s). 1583 ids collected in 124 files. The ceiling
    report lists `test_e2e_codified` (12.9 s) and `test_supervision`'s flaky-scenario test (11.2 s).
  - `python3 -m pytest -m timing -n 0 -q`: `4 passed, 1583 deselected` (6.4 s).
  - Unbuilt: `{} 0 []`.
  - `model check`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
    - The 53 violations: 25 `v17` (requests q23-q47), 19 `v10a` (initiatives' sources) and 9 `v_d1` (initiatives).
    - The 16 warnings are `w_uncited_obs`.
    - All 19 unresolved references are in `.shop/work/`.
  - `model logic`: `11 findings: 6 L5, 5 L6`. The 5 L6 are all supervision's. The L5 come from review, spec-migration,
    U4 (twice), U7 and U8.
  - `model lexicon --check`: `401 terms, 0 problems`.
  - `model decisions --check`: `4 check decisions: 4 hold, 0 failing` (0006, 0048, 0053, 0076). Decisions:
    78 `{accepted: 28, superseded: 48, rejected: 2}`, in force `{check: 4, requirement: 15, judgement: 9}`.
  - `model restates`: `581 ids: 513 restated, 68 dropped, 0 pending, 0 missing`.
  - `features generate --check` exits 0. `vocab --check` gives `every step has one handler`, and `bindings --unbound`
    gives `every binding names a scenario`.
  - `tools size --limit 300` is silent; `tools check` is clean (ruff, vulture; no import contracts).
  - `.shop/backlog/` does not exist in this repository: the names table has 0 rows (plan-8 Q2).
- **Intended baselines at the end** (Task 11 verifies them; each task gives its own):
  - Suite: no failures; `1 skipped`; no xfail. The pass count falls by exactly the removed ids, and the two ceiling
    entries above are gone. The retired lines alone remove 154 scenarios (supervision 80, work-queue 26,
    design-model-check 23, batch-measurement 17, requests 6, migration-tools 2), and the script tests of the
    deleted modules go with them.
  - Timing: `4 passed`.
  - `model check`: `0 violations, 16 warnings, 0 unresolved references, 0 file problems`.
    - No `.shop/work/` node is read, so `v10a`, `v_d1` and the unresolved references go.
    - The frozen requests are not read, so the 25 `v17` go too. q14, the only live request moved, cites an origin.
    - `w_uncited_obs` stays at 16, because the frozen `source` ids still count as citations (D6).
  - `model logic`: only L5 findings of U4, U7 and U8 are expected (4). Every L6 and every finding that names a
    retired capability goes; the report states the measured figure.
  - `model lexicon --check`: `402 terms, 0 problems`. The one new term is migration-tools' `queued`; the release
    value `1.0.0` is not a term.
  - Decisions: 82 `{accepted: 29, superseded: 51, rejected: 2}`, in force `{check: 5, requirement: 13,
    judgement: 11}`; `model decisions --check`: `5 check decisions: 5 hold, 0 failing`.
  - `model restates`: `581 ids: 140 restated, 441 dropped, 0 pending, 0 missing`. The 373 newly dropped ids were
    restated only by the 271 groups this plan retires; the planner measured both figures.
  - Features: `generate --check` exits 0. `features/supervision.feature` and `features/work-queue.feature` are gone.
  - Unbuilt: `{} 0 []`. Plugin `2.0.0`. `.shop/plugin-version` holds `2.0.0`, and `migrate status` lists no pending
    step.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-05;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as every plan is. |
| D2 | **What is retired.** 271 codified lines in all.<br>- **Every line of 12 capabilities:** `supervision` (84), `work-queue` (26), `review` (21), `spec-consistency` (17), `spec-integration` (16), `red-green` (15), `spec-migration` (14), `delivery` (11), `planning` (7), `code-research` (6), `role-boundaries` (6), `formulation` (0; already a record).<br>- **Lines of kept capabilities:**<br>  - `batch-measurement` r1-r17 (`measure initiative`);<br>  - `requests` r3, r4, r10-r13 (delegations);<br>  - `design-model-check` r8, r9, r12-r18, r21, r26, r27, r29, r31-r35, r37, r39, r45, r46, r53 (work-items, initiatives, proposals and `model why`'s proposals);<br>  - `migration-tools` r22, r23 (the hooks' initiative text).<br>**Kept:** `analysis-tools`, `feature-file-tools`, `trials` (the `trial-runner` agent stays), every capability of plans 1-8, `batch-measurement` r18-r22 (`measure show`/`compare` of an initiative's measurement, so history stays readable), `requests` r25/r26 (`work list`, `work show` of a request), and `design-model-check` r19, r20, r28 and r43 (requests and observations). |
| D3 | **A retired capability keeps its file**, as `formulation.md` does:<br>- **Purpose:** its first paragraph becomes the notice of D10's helper, and the rest stays.<br>- **Kept as they are:** `## Terms`, `## Relations` and `rests_on`.<br>- **Emptied:** `## Behaviour`.<br>- **Replaced:** `## Implementation, may change` becomes `- None: retired in plugin 2.0.0.` and `## Not yet` becomes `- None.`<br>- **Ids:** every id goes into `retired:`, and the 0.29 ids are listed under `## Dropped`.<br>- **Index:** its row in `spec/index.md`'s Composition moves to a new table, `Retired in 2.0.0`, with its narrator and group.<br>The ids stay unreusable (v15c), and frozen references to them still name a file. The design's alternative, deleting the file, would leave the ids only in git history and the 0.29 coverage with nowhere to live. |
| D4 | **A service capability with no group has no feature file.** `features generate` removes `features/<cap>.feature` for a codified service capability with no group and prints `removed features/<cap>.feature`. `--check` prints `differs: features/<cap>.feature` while such a file exists. feature-file-tools r17/r18 still hold (the generator owns every feature file). |
| D5 | **Frozen `.shop/work/`.**<br>- Nothing writes it after Task 4.<br>- `model check` reads no node, part, proposal or reference from it after Task 5. This settles plan-1 S10: i57's `backlog#r1-r8` no longer resolve against the new capability, because frozen history is not resolved at all.<br>- The 2.0.0 step writes `.shop/work/FROZEN.md` (D13).<br>- `.shop/work/README.md` and every other file is left byte for byte. |
| D6 | **What is still read from the frozen queue:** only the `source:` ids of `.shop/work/*/initiative.md` and `.shop/work/requests/*.md`, as citations of observations.<br>- Helper: `shop_frozen.sources(root) -> set[str]` (Task 5).<br>- `model check` reads them as the facts `cited(O)`, so `w_uncited_obs(O) :- node(O, "observation"), not source(_, O), not cited(O).`<br>- `work list`'s uncited observations (requests r25) are computed the same way.<br>- An observation an old initiative cited is therefore not reported as uncited. |
| D7 | **Live requests live in `.shop/requests/q<n>.md` (Task 6).**<br>- One constant, `request_text.REQUESTS`, is read by every reader and writer.<br>- A new request's number is one above the highest `q<n>` in `.shop/requests/` and `.shop/work/requests/` together (`request_text.next_number(root)`), so a new id never collides with a frozen one.<br>- No fallback to `.shop/work/requests/` for reading. |
| D8 | **Which requests the 2.0.0 step moves:** each request that is not closed (`open`, `awaiting-asker`, `awaiting-upstream`, `accepted`) and whose `asker` is neither `internal` nor this context's own `bounded-context/<path>`.<br>- It moves with `git mv`, name and id unchanged. A peer's negotiation in flight goes on.<br>- An internal request that is not closed stays frozen and is listed in the notes, to be entered again as an item: an internal intention is an item now (design goal 1).<br>- Closed requests stay frozen. |
| D9 | **What of `work` stays.**<br>- **The backlog, batch, intake, readiness and conversation commands.**<br>- **`request`** without `--delegation`, and **`outcome`, `ask`, `reply`, `turn`, `resolve`**.<br>- **`list`:** requests with their status and turn, and the uncited observations (requests r25). It no longer lists initiatives or work-items.<br>- **`show`:** an item, a request or a quote, but not an initiative or a work-item.<br>- **`withdraw` and `answer`:** an item only.<br>**Goes:** `add`, `run`, `retry`, `note`, `status`, `start`, `delegate`, and the work-item and initiative branches of `list`, `show`, `withdraw` and `answer`. A frozen file is read as a file. |
| D10 | **The retirement helper** is a record: `.shop/records/2026-11-04-workflow-simplification/plan-9-retire.py.txt`, run as `python3 <it> <cap> [r<n> ...]` (no ids: every id). It is committed once in Task 2 and never edited after. For each id given it:<br>- removes the `- [r<n>]` bullet (with its continuation lines) from `## Behaviour`, and every group left with no requirement (heading, `Restates:`, prose and given block);<br>- writes the ids into `retired:`, merged with any there and sorted by number;<br>- covers each 0.29 id of a removed group's `Restates:` that no remaining group restates (by the rules below);<br>- when it retires every id: writes the Purpose notice "**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went." as Purpose's first paragraph, and D3's Implementation and Not yet.<br>**The 0.29 rules:**<br>- an id of this capability, or one whose own `## Dropped` says `moved to <this cap>`, is written as `- r<n>@0.29: retired with <cap>#r<m>[, #r<k>] in 2.0.0 (the-old-workflow-retired).`;<br>- the second kind and an id of another capability that this capability restates are written qualified, `- <cap0>#r<n>@0.29: …`, in this capability's `## Dropped`;<br>- `## Dropped` is created after `## Not yet` when missing.<br>It prints what it did, and refuses an id the capability does not have. |
| D11 | **`model restates` reads a qualified dropped entry** (Task 2). A 0.29 id is `dropped` when any codified capability's `## Dropped` lists it with a reason that is not `moved to …`. That includes the qualified form in another file, such as supervision's `formulation#r1@0.29: retired with …`. "Restated by a group" still wins. |
| D12 | **Agents and skills (Task 3).**<br>- **Deleted agents:** `code-scout`, `bdd-planner`, `bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`, `initiative-round`, `capability-writer`, `delegation-answerer`, `spec-checker`, `batch-analyst` (`work run` starts it).<br>- **Deleted skills:** `delivering-an-initiative`, `formulating-features`, `integrating-a-proposal`, `checking-spec-consistency`, `migrating-to-capabilities` (it drives `capability-writer`; `scripts/migrate run` stays as a tool under migration-tools), `bdd-red-green` (loaded only by `bdd-implementer`; building-a-batch's brief already gives its rules inline).<br>- **Kept:** `pr-reviewer`, `architecture-reviewer`, `trial-runner`; `analyzing-a-batch`, `building-a-batch`, `raising-a-request`, `shaping-items`, `taking-in-a-request`.<br>The design names `spec-checker` among what goes even though memory `requirements-are-the-linchpin` values a model judge. The design is the later word. |
| D13 | **The 2.0.0 step "the workflow simplified"** (`scripts/migrate_upgrade_simplified.py`, `plan(root) -> Changes`):<br>- **The marker:** when `.shop/work/` exists, writes `.shop/work/FROZEN.md`, exactly:<br>`# Frozen`<br><br>`The request, initiative and work-item queue of plugin 1.x, frozen by \`migrate upgrade\` 2.0.0. Nothing writes here and \`model check\` reads nothing here but the \`source\` of its initiatives and requests. Items are in \`.shop/backlog/\`, batches in \`.shop/batches/\` and live requests in \`.shop/requests/\`.`<br>- **Requests:** moves D8's requests.<br>- **Decisions:** when `spec/decisions/` exists, rewrites `spec/decisions/index.md` as `model_report.render_decisions(root)` gives it (plan-6 M5).<br>- **Notes:** one line for each of the following, by id and title:<br>  - each initiative neither `done` nor `abandoned`: `open initiative i<n> "<title>" is frozen: shape what is still wanted as an item (work idea)`;<br>  - each capability- or glossary-proposal neither `formulated`, `approved`, `merged` nor `withdrawn`: `the lines of proposal <rel> were never applied: shape an item with them if still wanted`;<br>  - each internal request not closed: `internal request q<n> "<title>" is frozen: enter it as an item if still wanted`;<br>  - each moved request: `moved request q<n> to .shop/requests/`.<br>- **Refusals** (`failures`): a destination under `.shop/requests/` that exists ("could not move …", via `move_failures`), and a request file whose frontmatter does not read.<br>- **Nothing is deleted.** |
| D14 | **`work_items.py` keeps its name** (Task 3). It becomes the plugin's pytest plugin of the strict `unbuilt:` xfail only; `--work-item` and `--whole-suite` go. The name stays because `batch_tasks`' default test command and consumers' `[batch] tests` load it as `-p work_items`. Its docstring and CLAUDE.md row say why. |
| D15 | **Hooks (Task 4).**<br>- `migrate prompting` (the delegation text) and `migrate compacting` (the initiative hand-off) are removed, with `scripts/migrate_prompt.py` and `migrate_session.py`.<br>- hooks.json loses `migrate prompting` from UserPromptSubmit and the whole PreCompact block.<br>- `migrate status --hook` prints only the upgrade text.<br>- conversation r2 and r4 and the aliases `work quote --hook` and `work names --hook` stay (plan-8 S2). r2 is still true of the alias, so nothing is gained by changing it. |
| D16 | **`model check` rules deleted with their lines (Task 5):** `v8`, `v9a`-`v9g`, `v_k3`-`v_k6`, `v_b1`, `v_b3`, `v_w1`-`v_w4`, `v_d1`, `v_d3`, `v_d5`, `v15e`, `v15f`, `v16a`, `v18a`-`v18c`, `w_stale_intake`, `w_stale_proposed`. `v18d` stays for requests (`raised_for`). The job, seam and request rules stay. `model why` is deleted with r53: without proposals it says nothing that `model restates --json` and the file do not. |
| D17 | **migration-tools at 2.0.0 (Task 9).**<br>- **Edited in place (P10):** r14's and r19's given `.shop/plugin-version` changes from `"1.0.0"` to `"2.0.0"`. Their behaviour stays; their example data named the plugin's own release. The 1.0.0 lines were never merged or released (`main` is at 0.29.0).<br>- **`tests/scenarios/migration_old.TARGET`** becomes `"2.0.0"`.<br>- **Terms:** the `release` attribute gains the value `1.0.0` ("before the workflow was simplified"), and a new condition reads `- **queued** (condition of repository): A repository is queued when the repository is \`1.0.0\`.`<br>- **New group:** `### [g24] the upgrade step "the workflow simplified" freezes \`.shop/work/\`, moves the live requests to \`.shop/requests/\` and writes the decisions index`, with `- [r24] While the repository is queued, when the person runs \`migrate upgrade\`, \`migrate\` shall write \`.shop/work/FROZEN.md\`, rename \`.shop/work/requests/q2.md\`, rewrite \`spec/decisions/index.md\` and print "the workflow simplified", "i1" and "q1".` The planner parsed this sentence with `outdated` in place of `queued`; it gives one tree. |
| D18 | **Decisions.**<br>- **New `0080-the-old-workflow-retired`** (Task 2): `accepted`, `tier: judgement`, `supersedes: [design-decision/workflow-capabilities-are-guarantees]` (0065 narrowed). The old workflow's lines are retired in bulk, with D2's list, and the guarantees left (`trials`, `pr-review`, `brainstorming`) are checked by script tests, never as fixture sessions.<br>- **New `0081-the-2-0-layout`** (Task 8): `judgement`. It restates what of 0026 survives (plan-6 Q4): `.shop/backlog/b<n>.md`, `.shop/batches/<n>/`, `.shop/requests/q<n>.md`, `.shop/quotes/<n>.md`, `.shop/records/` (records with `id`/`kind`/`about`; `observations.md`, one `## <id>` an observation with `about:`, `by:`, `date:`), `.shop/plugin-version`, `.shop/delivery.toml`, and `.shop/work/` frozen.<br>- **New `0082-feature-files-written-by-features-generate`** (Task 8): `check`, `enforced_by: [tests/scripts/test_decision_checks.py::test_the_features_are_what_features_generate_writes]`, `supersedes: [design-decision/feature-files-read-only-in-red-green]` (0006, plan-6 Q3).<br>- **New `0083-the-2-0-agents`** (Task 3): `check`, `enforced_by: [tests/scripts/test_agents.py::RoleBoundaries]`, `supersedes: [design-decision/the-v3-agents]` (0053, plan-6 S4). The agents are `pr-reviewer` (opus; no Edit, Write or Bash), `architecture-reviewer` (opus; no Edit) and `trial-runner` (sonnet), and no agent can start an agent.<br>**Re-pointed (frontmatter only, plan-6 S5):**<br>- 0027 `enforced_by: [design-model-check#r36]`;<br>- 0047 `enforced_by: [design-model-check#r38]`;<br>- 0036 to `tier: judgement` with no `enforced_by`, because no kept line checks the requirement form;<br>- 0018 to `tier: check`, `enforced_by: [tests/scripts/test_measure_batch_read.py::test_an_unknown_row_is_refused_naming_it, tests/scripts/test_conversation_read.py::test_a_row_with_no_type_is_refused]`, since batch-measurement r6 and r7 retire.<br>No `## Decision` section is edited. |
| D19 | **The glossary (Task 8).**<br>- `review` becomes "a reviewer's reading of commits against the spec and the repository's rules, written as graded findings: a pull request review or an architecture review. Not: audit."<br>- `` `measure` `` becomes "the tool that measures a merged batch, records a defect found after a merge, and shows and compares measurements."<br>- `tool` drops `work run` from its list.<br>- `` `work run` `` becomes "the supervisor of plugin 1.x that ran an initiative's work-items through their stages; removed in 2.0.0, its record frozen under `.shop/work/`."<br>- Old kinds (`work-item`, `initiative`, `capability-proposal`, …) and retired capabilities' Terms stay in the lexicon. Removing an unused term waits for a check that names one (open). |
| D20 | **This repository's open work (Task 10)**, entered after the upgrade with `work idea` (provenance `own`), each with `--note "from <source> of the frozen queue"`:<br>- `Requests between repositories over GitHub issues` (i39 w212, deferred: it needs a design session with the person);<br>- `Request lines into an upstream in the downstream's own terms` (q17);<br>- `Every command answers in JSON and exits 0 but on a crash` (q25);<br>- `Requirement quality: fewer question cycles from better lines` (q26).<br>**Left out**, with the reason in the report:<br>- q41, settled by plan-5 S6's quiet git;<br>- q45 and q46, whose board and item dependencies plans 2-8 built;<br>- q14, a product request that is still accepted: the step moves it, and its fulfilment is "requests go through one shared tool", which `work request` already is. The report says to resolve it with `work resolve`, and does not do it, because a resolution names a requirement and version for the person to confirm;<br>- every other open internal request, each about `work run`, its rounds, gates, proposals or delegations, so no subject is left. |
| D21 | **Renames.** `workqueue_request.py` becomes `request_moves.py`, and `workqueue_lines.py` becomes `request_lines.py`, beside `request_text.py`, so that no kept module is named for the deleted queue. `tests/scenarios/work_queue_world.py` keeps its name: it is the shared repository world of backlog, batches, intake, conversation and requests, and renaming it would touch every test module for no behaviour. |
| D22 | **Plugin metadata.** `version: 2.0.0`. The description becomes "BDD workflow for the shopsystem harness: keep one spec of capability files, write requirements in a controlled language (GF), logic-check them, generate one Gherkin feature per capability, keep a backlog of items, build ready items in batches closed by one reviewed pull request, measure each batch, and upgrade repositories between releases." The README gains `## 2.0.0: the workflow simplified` above `## 1.0.0`. Its history sections stay as history. Its intro, layout, workflow, scripts and agents sections describe 2.0, and `## \`work run\`` goes. |
| D23 | **1.0.0 was never released.** `main` is at 0.29.0, so a consumer reaches 2.0.0 from 0.29.x through the 1.0.0 step and the 2.0.0 step in one `migrate upgrade` commit. Task 9 tests that chain as well as a repository on 1.0.0. |

## Every item left for plan 9

Each item that earlier plans marked "for plan 9" (or "until plan 9"), with the task that settles it or the reason it
stays open.

| # | From | Item | Settled by / stays open because |
|---|---|---|---|
| 1 | plan-1 S10 (rulings, open problems) | Frozen `.shop/work/` references now resolve against new ids by collision (i57's `backlog#r1-r8`) | Task 5 (D5): `model check` resolves nothing in frozen history |
| 2 | plan-4 D25, M9 | `_LineParser`'s class swap in `backlog_cli`, "plan 9 rewrites scripts/work's parser" | **Open.** The swap works around argparse before 3.12 (`work line b1 --into CAP TEXT`), and it is not tied to the old commands. It goes when the project's floor is Python 3.12; this machine is 3.11.15 |
| 3 | plan-4 rulings S4 | `bdd-red-green` left for `work run`; the batch subagent has its own brief | Task 3 deletes the skill and `bdd-implementer`; building-a-batch's brief says "these rules" with no skill name |
| 4 | plan-4-batches; plan-5 D18 and implementation | Delete `supervise*.py`, `stub_claude.py`, `bdd-task-reviewer`, `bdd-branch-reviewer`, `supervise_review_read.py`, `supervise_branch_runs.py` and the rest of `work run` | Task 3 |
| 5 | plan-5 D16, implementation | The glossary's `review` names the old kinds | Task 8 (D19) |
| 6 | plan-6 D8 | The old process's decisions are superseded by 0074, but their machinery runs until plan 9 | Tasks 3-5, 7: the machinery is deleted |
| 7 | plan-6 Q3 | 0006 is a `check` on a test that enforces a newer rule | Task 8: 0082 supersedes it |
| 8 | plan-6 Q4 | 0026's surviving forms to be restated | Task 8: 0081 |
| 9 | plan-6 S4 | 0053's agent table is stale | Task 3: 0083 supersedes it |
| 10 | plan-6 S5 | Re-point 0027, 0036 and 0047 when r31, r33 and r37 retire | Task 5 (D18), in the commit that retires them |
| 11 | plan-6 M5 | The 2.0.0 step regenerates `spec/decisions/index.md` | Task 9 (D13) |
| 12 | plan-6 implementation | 0065 to be narrowed | Task 2: 0080 supersedes it |
| 13 | plan-6 Q1/D6 | design-model-check r52 against decision-tiers r5 | **Open, and not changed:** ruled by `spec/universal.md`'s "If" precedence (plan-6 Q1). Retiring r52 would buy nothing |
| 14 | plan-7 D17, implementation 1 | `measure initiative`, batch-measurement and `batch-analyst`; the glossary's `measure` | Task 7 (`measure initiative`, batch-measurement r1-r17), Task 3 (`batch-analyst`), Task 8 (`measure`) |
| 15 | plan-7 D17 | The README's 0.23.0 history | **Kept as history** (D22). History sections are not rewritten |
| 16 | plan-7 rulings "For plan 9" | The old reviewers hit the harness's refusal of a subagent's Write | Task 3 deletes them |
| 17 | plan-7 rulings "Not done here" | `CLAUDE.md` rows of `measure_batch_read.py` and `measure_batch_sessions.py` could name `parents` and the driver | Task 8's module-map sweep |
| 18 | plan-8 D9, open problem 1 | `migrate prompting` and `migrate status --hook`'s initiative and request text | Task 4 (D15) |
| 19 | plan-8 Q2 | Measure the names table on the real backlog, and narrow it past about 50 rows | Task 10 measures it (0 rows before, 4 after D20). **Open:** under 50, so no narrowing |
| 20 | plan-8 S2 | r2 may be retired for a line naming `conversation_hook` | **Kept** (D15): r2 is true of the alias `work quote --hook`, which stays |
| 21 | plan-8 open problem 2 | The names table does not expand `i<n>`, `w<n>`, `q<n>` or `r<n>` | **Open:** frozen ids are history, read as files. A live `q<n>` and an `r<n>` are ids the person meets in the backlog's lines. Expanding them needs a line in `conversation`, and none exists |
| 22 | design § Migration | `.shop/work/` frozen; its open work entered again as items | Tasks 9-10 (D13, D20) |
| 23 | design § Migration | The old capabilities' requirements retired in bulk under one decision | Task 2 (0080) and Tasks 2-5, 7 |
| 24 | roadmap row 9 | `migrate upgrade` 2.0.0 | Task 9 |
| 25 | found by the planner | 1.0.0 was never released (`main` at 0.29.0) | Task 9 tests the chained 0.29 → 2.0.0 upgrade (D23) |
| 26 | found by the planner | Retired capabilities' Terms and the old kinds stay in the lexicon | **Open** (D19): no check names a term that no line uses, and removing one could break a kept given block |
| 27 | found by the planner | `docs/design-model/` (design model v5) still describes initiatives and parts | **Open:** it is the model's own versioned document. A v6 is a design session's work, not a retirement's. `spec/index.md` says that 2.0 builds on v5 with items in place of initiatives |

## Review Focus

These are the conditions most likely to bite a person, which no line's check exercises. Each has its test in the task
named.

1. **A kept command breaks because something it imported is gone.** Examples: `work batch …`, `work intake`,
   `work quote`, `measure batch` or `measure show` of an old initiative record, run in a consumer repository after
   the deletions. Pinned in Task 1: `test_no_kept_module_imports_an_old_module` (an import scan of every kept
   module). Task 3: `test_every_work_command_answers_help` (each subcommand `--help` exits 0). Task 7:
   `test_an_initiative_measurement_is_still_shown_and_compared` (a 1.x record fixture).
2. **The upgrade loses something.** A file is deleted or changed under `.shop/work/`, a peer's open request is left
   where nothing reads it, an open initiative or proposal goes unmentioned, or the upgrade is half-applied on a
   collision. Pinned in Task 9:
   - `test_nothing_under_shop_work_changes_but_the_marker_and_the_moved_requests`;
   - `test_a_peers_open_request_moves_and_an_internal_one_stays`;
   - `test_every_open_thing_is_named_in_the_notes`;
   - `test_a_request_already_in_shop_requests_refuses_and_changes_nothing`;
   - `test_no_file_is_deleted` (`git diff --diff-filter=D` empty).
3. **A retired id or 0.29 id falls out of coverage.** A retired id reused, a 0.29 id no longer restated nor dropped,
   or a moved id whose target retired it. Pinned in Task 2: `test_a_moved_id_retired_in_its_target_is_dropped`
   (`test_model_restates.py`); `test_spec_retired.py` (each retired capability has no group, lists every id it had
   in `retired:`, and `model restates` reports none of its ids missing). The gate's `model restates` runs in every
   task.
4. **A new request takes a frozen request's id.** Pinned in Task 6:
   `test_a_new_request_is_numbered_above_the_frozen_ones`, and `test_model_reads_no_frozen_request`.
5. **The session is still told about the old queue.** The SessionStart hook prints an initiative, the
   UserPromptSubmit hook prints delegation text, or a skill names a deleted command, agent or skill. Pinned in
   Task 4: migration-tools r19 (as edited, Task 9) and `test_no_hook_names_the_old_queue`. Task 3:
   `test_no_kept_skill_or_agent_names_a_deleted_one` (it greps `skills/`, `agents/`, `README.md` and `CLAUDE.md`
   for each deleted agent, skill and command, and allows only README's history sections).

---

### Task 1: The shared plumbing out of the old modules

A refactor with no behaviour change. After it, no kept module imports a module that a later task deletes.

**Files:**
- Create:
  - `scripts/shop_files.py`: the plumbing of `.shop/` that every command shares;
  - `scripts/transcripts.py`: Claude Code's transcripts read;
  - `tests/scripts/test_kept_modules.py`.
- Rename (`git mv`): `scripts/workqueue_request.py` → `scripts/request_moves.py`; `scripts/workqueue_lines.py` →
  `scripts/request_lines.py`; `tests/scripts/test_workqueue_request_asker.py` → `test_request_asker.py`;
  `tests/scripts/test_workqueue_request_parse.py` → `test_request_parse.py`.
- Modify:
  - `scripts/workqueue.py` (imports and re-exports from `shop_files`);
  - `scripts/measure_read.py` (imports from `transcripts`);
  - `scripts/spec_read.py` (gains `is_guarantees`), `scripts/supervise_outputs.py`, `scripts/work_items.py`;
  - every importer of a moved or renamed name: `backlog_*.py`, `batch_*.py`, `conversation_*.py`,
    `intake_moves.py`, `readiness_bar.py`, `request_text.py`, `measure_cost.py`, `measure_defect.py`,
    `measure_batch*.py`, `measure_show.py`, `measure_write.py`, `scripts/measure`, `scripts/work`, `supervise*.py`,
    `workqueue_*.py` and the tests that import them;
  - `CLAUDE.md`: new rows for `shop_files.py` and `transcripts.py`, and the two renamed rows.

**Interfaces:**
- Produces:
  - `shop_files`: `Refused` (the one exception class; `workqueue.Refused is shop_files.Refused`), `context_path(root)
    -> str`, `read(path, root) -> str`, `git(root, *args)`, `committed(root, rels, message, write)`, `append(log,
    data)`, `LINE_BREAKS` (from `workqueue_answer`).
  - `transcripts`: `Refused` (the same object as `measure_read.Refused`), `moment`, `json_rows`, `number`,
    `assistant_rows`, `request_key`, `store_dir`. `measure_read` imports them from here.
  - `measure_cost.KINDS` and `measure_cost.duration`, moved from `measure_build` and re-exported there.
  - `request_text.requests(root)`, moved from `workqueue.requests` (same rows), and
    `spec_read.is_guarantees(root, capability) -> bool`.
- Later tasks rely on these names only.

- [x] **Step 1: Write the failing test** `tests/scripts/test_kept_modules.py::test_no_kept_module_imports_an_old_module`.
  - It parses (with `ast`) every file in a `KEPT` list and asserts that none imports a name in `OLD`.
  - `KEPT` is `backlog_*`, `batch_*`, `conversation_*`, `intake_moves`, `readiness_bar`, `request_*`, `measure_cost`,
    `measure_defect`, `measure_batch*`, `measure_show`, `measure_write`, `transcripts`, `shop_files`, `spec_*`,
    `features*`, `tools*`, `model*` and `migrate*` under `scripts/`, plus `scripts/work`, `scripts/measure`,
    `scripts/conversation_hook`, `scripts/work_items.py` and `tests/scenarios/*.py`, less the files of supervision
    and work-queue.
  - `OLD` is `supervise*`, `workqueue`, `workqueue_answer`, `workqueue_done`, `workqueue_list`, `workqueue_note`,
    `workqueue_start`, `workqueue_status`, `measure_build`, `measure_read`, `stub_claude`, `migrate_session` and
    `migrate_prompt`.
  - `scripts/work`, `scripts/measure`, `scripts/migrate` and `migrate_upgrade.py` still import some of `OLD` today,
    because their commands are deleted later. They are listed in an
    `ALLOWED = {file: {modules}}` that Tasks 3-7 empty, entry by entry.
- [x] **Step 2: Run it.** `python3 -m pytest tests/scripts/test_kept_modules.py -q`. Expected: FAIL, naming e.g.
  `scripts/batch_git.py imports workqueue`.
- [x] **Step 3: Move the names** as the Interfaces block says. Every caller uses the new module. `workqueue.py` and
  `measure_read.py` keep working for the old code, by importing from the new modules.
- [x] **Step 4: Run the test and the gate.** The test passes. The gate's figures are the baselines exactly: `1583 passed`
  (the baseline's 1582 and the new test), the same `model check`, `logic`, `restates`. The collection diff removes nothing: the
  renamed test files' ids reappear under their new names.
- [x] **Step 5: Commit.**
  ```bash
  git add -A scripts tests CLAUDE.md
  git commit -m "plumbing: shop_files, transcripts and the request modules, so no kept module imports the old queue (plan 9, Task 1)"
  ```

### Task 2: The guarantees of the old stages retired, under 0080

Spec only, plus the helper and `model restates`' qualified entries. Nothing that runs changes.

**Files:**
- Create:
  - `.shop/records/2026-11-04-workflow-simplification/plan-9-retire.py.txt` (D10);
  - `spec/decisions/0080-the-old-workflow-retired.md` (D18);
  - `tests/scripts/test_spec_retired.py`.
- Modify:
  - `scripts/model_restates.py` (D11), `tests/scripts/test_model_restates.py`;
  - `spec/capabilities/{code-research,delivery,formulation,planning,red-green,review,role-boundaries,spec-integration,spec-consistency,spec-migration}.md`, by the helper only;
  - `spec/decisions/0065-workflow-capabilities-are-guarantees.md`: frontmatter `status: superseded`, with `tier` removed;
  - `spec/decisions/index.md` (`python3 scripts/model decisions`);
  - `spec/index.md`: Composition's rows of those ten capabilities move to `### Retired in 2.0.0`;
  - `tests/scripts/test_spec_guarantees.py`: `GUARANTEES` becomes `("trials",)`. Its formulation and moved-id tests
    move to `test_spec_retired.py`;
  - `tests/scripts/test_decision_checks.py`: totals 79 `{accepted: 28, superseded: 49, rejected: 2}`, in force
    `{check: 4, requirement: 15, judgement: 9}`; `test_the_judgement_decisions_reach_the_brief` expects 0080 in
    place of 0065, still 9.

**Interfaces:**
- Produces:
  - the helper's command line (D10), used again in Tasks 3, 4, 5 and 7;
  - `model_restates.coverage(root, capability=None)`, with the same rows; a qualified dropped entry now counts.

- [x] **Step 1: Write the failing tests.**
  - `test_model_restates.py::test_a_moved_id_retired_in_its_target_is_dropped`. In a fixture, `a.md`'s `## Dropped`
    says `- r1@0.29: moved to b`. `b.md` has no group restating it, and its `## Dropped` says `- a#r1@0.29: retired
    with b#r3 in 2.0.0 (the-old-workflow-retired).` Then `a#r1`'s state is `dropped` and its reason is b's.
  - `test_a_moved_id_restated_by_its_target_is_still_restated` keeps the old case.
  - `test_spec_retired.py`, parametrised over the ten capabilities:
    - `test_a_retired_capability_has_no_group_and_lists_every_id` asserts no group, `retired:` equal to
      `[r1..r<max>]` of the capability's ids at `19e9fee5` (read with `git show 19e9fee5:<path>`), and the Purpose
      notice;
    - `test_no_id_of_a_retired_capability_is_missing` checks that `model_restates.coverage(REPO, cap)` has no
      `missing` or `pending`.
- [x] **Step 2: Run them.** `python3 -m pytest tests/scripts/test_model_restates.py tests/scripts/test_spec_retired.py -q`.
  Expected: the restates test fails with the state `pending`, and the retired tests fail on groups.
- [x] **Step 3: Implement D11** in `model_restates.coverage`.
- [x] **Step 4: Write the helper** (D10), then retire the ten capabilities, one command each:
  `python3 .shop/records/2026-11-04-workflow-simplification/plan-9-retire.py.txt review` (and so on).
- [x] **Step 5: Write 0080, supersede 0065, regenerate the index, and update `spec/index.md` and the two test
  modules.**
  - 0080's `## Decision` lists D2's retired lines, says that each retired capability keeps its file (D3), and says
    which guarantees remain.
  - The Composition text before the tables gains one sentence: "The capabilities of plugin 1.x's stages are retired
    (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired) and kept as records of
    their ids."
- [x] **Step 6: The gate.** Expected:
  - Suite: no failure.
  - `model restates`: 0 missing, and the dropped figure grows by the 0.29 ids of these ten.
  - `model logic`: the findings naming review, delivery, spec-consistency, spec-integration and spec-migration go.
    Record the figure; supervision's 5 L6 remain until Task 3.
  - `lexicon`: 401.
  - `decisions --check`: 4 hold.
  - `model check`: 53/16/19/0.
  - Collection diff: only `test_spec_guarantees` ids of the ten capabilities, each replaced in `test_spec_retired`.
- [x] **Step 7: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-9-retire.py.txt spec scripts/model_restates.py tests/scripts
  git commit -m "spec: the old stages' guarantees retired under the-old-workflow-retired (0080, superseding 0065) (plan 9, Task 2)"
  ```

### Task 3: `work run`, supervision, and the agents and skills of the stages

**Files:**
- Delete (`git rm`):
  - `scripts/supervise*.py` (25 files);
  - `tests/scripts/stub_claude.py`, `tests/scripts/test_supervise_*.py`, `test_e2e_codified.py`,
    `test_work_items_worker.py`, `tests/scripts/fixtures/e2e/`;
  - `tests/scenarios/supervision_*.py` and `tests/scenarios/test_supervision.py`;
  - the agents and skills of D12.
- Modify:
  - `spec/capabilities/supervision.md` (the helper, every id);
  - `scripts/work` (drop `run`);
  - `scripts/work_items.py` (D14), `tests/scripts/test_work_items.py` (keep its unbuilt tests, delete its
    `--work-item` and `--whole-suite` tests);
  - `scripts/features` (D4), `tests/scripts/test_features_generate.py`;
  - `tests/scripts/test_agents.py` (rewritten to 0083);
  - `spec/decisions/0053-the-v3-agents.md` (`status: superseded`, with `tier` and `enforced_by` removed);
  - `spec/decisions/0083-the-2-0-agents.md` (new), `spec/decisions/index.md`;
  - `skills/building-a-batch/SKILL.md` (step 4: "these rules", with no skill name);
  - `skills/analyzing-a-batch/SKILL.md` (Common Mistakes: the `bdd-implementer` and work-item rows reworded for a
    batch's subagent and its item);
  - `README.md` (the agents section and table: three agents);
  - `CLAUDE.md` (the rows of every deleted module; `work_items.py`'s row per D14);
  - `spec/index.md` (supervision's row to "Retired in 2.0.0");
  - `tests/scripts/test_kept_modules.py` (`ALLOWED` loses `scripts/work`'s supervise entries);
  - `tests/scripts/test_decision_checks.py` (totals 80 `{accepted: 28, superseded: 50, rejected: 2}`, in force
    `{check: 4, requirement: 15, judgement: 9}`; 0083 replaces 0053 among the check decisions).
- Test: `tests/scripts/test_retirement.py` (new; Review Focus 1 and 5).

**Interfaces:**
- Consumes: Task 1's `spec_read.is_guarantees`; Task 2's helper.
- Produces:
  - `features generate` per D4;
  - `test_agents.REVIEWERS == ("architecture-reviewer", "pr-reviewer")` and `AGENTS_2_0 = ("architecture-reviewer",
    "pr-reviewer", "trial-runner")`.

- [x] **Step 1: Write the failing tests.**
  - `test_features_generate.py::test_a_service_capability_with_no_group_has_no_feature`. In a fixture, a codified
    service capability with no group has a stale `features/x.feature`. `generate` removes it and prints `removed
    features/x.feature`. `--check` before the removal prints `differs: features/x.feature` and exits 1.
  - `test_agents.py`, rewritten:
    - `test_the_agents_are_the_2_0_set` (`sorted(agents()) == list(AGENTS_2_0)`);
    - `test_no_agent_starts_an_agent`;
    - `test_no_reviewer_has_edit`;
    - `test_pr_reviewer_has_no_write_or_shell`;
    - `test_each_agent_names_its_model` (opus, opus, sonnet);
    - the CodifiedFlow tests that name no deleted file (`raising_a_request…`, `no_doc_names_telingo…`).
  - `test_retirement.py`:
    - `test_every_work_command_answers_help` (every subcommand `work` lists answers `--help` with exit 0);
    - `test_no_kept_skill_or_agent_names_a_deleted_one`. It greps `skills/`, `agents/`, `README.md` (less its
      `## <version>:` history sections) and `CLAUDE.md` for each D12 name and for `work run`, `--work-item` and
      `supervise_`, and expects no hit. It grows in Task 4 by `work add`, `work status`, `work note`, `work start`,
      `work delegate`, `work retry`, `migrate prompting` and `migrate compacting`.
- [x] **Step 2: Run them.** Expected: the generate test fails (the empty Feature is written), `test_the_agents_are_the_2_0_set`
  fails listing 13 agents, and the grep test fails naming `work run` in README.
- [x] **Step 3: Retire supervision** with the helper, then delete the files listed and make the modifications.
  - `scripts/work`'s `run` and `supervise`/`supervise_all` imports go.
  - `work_items.py` keeps only the unbuilt mark.
  - Write 0083 and supersede 0053. Run `python3 scripts/model decisions`.
  - Run `python3 scripts/features generate`: it removes `features/supervision.feature`.
  - Delete only the scenario handlers that no remaining step uses. Drop a module, run `features vocab --check`, and
    keep in it only the handlers of the steps that check then names.
- [x] **Step 4: The gate.** Expected:
  - Suite: no failure. The ceiling list loses both entries.
  - `model logic`: no L6, and no finding that names supervision.
  - `decisions --check`: `4 check decisions: 4 hold` (0048, 0076, 0006, 0083).
  - `model check`: 53/16/19/0, since `.shop/work/` is still read until Task 5.
  - `restates`: 0 missing.
  - `vocab --check`: one handler each.
  - Collection diff: supervision's 80 scenarios, the deleted test files' ids, and `test_work_items`' `--work-item`
    tests, each named in the report.
  - `ls agents` lists 3 files, and `ls skills` lists 5 directories.
- [x] **Step 5: Commit.**
  ```bash
  git add -A scripts tests spec skills agents features README.md CLAUDE.md
  git commit -m "work run retired: supervision's lines, supervise*, the stages' agents and skills; the 2.0 agents (0083, superseding 0053) (plan 9, Task 3)"
  ```

### Task 4: The old queue, delegations and the hooks' initiative text

**Files:**
- Delete (`git rm`):
  - `scripts/workqueue.py`, `workqueue_answer.py`, `workqueue_done.py`, `workqueue_list.py`, `workqueue_note.py`,
    `workqueue_start.py`, `workqueue_status.py`, `migrate_session.py`, `migrate_prompt.py`;
  - `tests/scenarios/test_work_queue.py`, and `work_queue_handlers.py` where nothing still uses it (Task 3, Step 3's
    rule);
  - `tests/scripts/test_work_add_title.py`, `test_work_item_ids.py`, `test_work_withdraw.py`, `test_workqueue_done.py`,
    `test_workqueue_list.py`.
- Create:
  - `scripts/request_view.py`: `work list` and `work show <request>` (requests r25, r26), with D6's uncited
    observations read through `shop_frozen.sources`;
  - `scripts/shop_frozen.py`: D6's `sources(root) -> set[str]`, read here and in Task 5;
  - `tests/scripts/test_request_view.py` (it absorbs `test_work_show_request.py`, which is `git mv`ed into it).
- Modify:
  - `spec/capabilities/work-queue.md` (the helper, every id), `spec/capabilities/requests.md` (the helper: r3, r4,
    r10-r13; its Implementation bullets lose `--delegation`, `work delegate` and `delegation` in the file's form),
    `spec/capabilities/migration-tools.md` (the helper: r22, r23; its Implementation bullet on `.shop/plugin-version`
    and the hook);
  - `spec/index.md` (work-queue's row to "Retired in 2.0.0");
  - `scripts/work` (D9; its docstring and `cmd_show`, `cmd_list`, `cmd_withdraw` and `cmd_answer` routes),
    `scripts/request_moves.py` (no `delegate`, no `--delegation`, and `resolve` without `workqueue_done`),
    `scripts/backlog_moves.py` and `backlog_items.py` (no `workqueue` import);
  - `scripts/migrate` (no `prompting` or `compacting`), `scripts/migrate_upgrade.py` (`run(hook=True)` writes only
    `session_text`);
  - `hooks/hooks.json` (D15), `tests/scripts/test_hooks.py`, `tests/scripts/test_backlog_moves.py` (its work-item
    `withdraw`/`answer` tests go), `tests/scripts/test_migrate_upgrade.py`;
  - `tests/scripts/test_retirement.py`, `tests/scripts/test_kept_modules.py` (`ALLOWED` loses the workqueue and
    migrate_session entries);
  - `skills/raising-a-request/SKILL.md` (step 5: a missing term goes into an item as a term bullet, `work line <item>
    --into <cap> --term "<bullet>"`, not through integrating-a-proposal), `README.md`, `CLAUDE.md`.

**Interfaces:**
- Consumes: Task 1's `shop_files`, `request_text.requests`.
- Produces:
  - `request_view.listing(root, as_json) -> int` and `request_view.show(root, name, as_json) -> int`, with the output
    of `work list`/`work show q<n>` unchanged for requests and observations;
  - `shop_frozen.sources(root) -> set[str]`, the `observation/…` and other ids named in the `source:` of
    `.shop/work/*/initiative.md` and `.shop/work/requests/*.md`; an unreadable frontmatter is skipped, never
    refused, because frozen history is not checked.

- [ ] **Step 1: Write the failing tests.**
  - `test_request_view.py`:
    - `test_work_list_gives_requests_and_uncited_observations_only` (a fixture with an initiative, a work-item and a
      request: the output names the request and no `i1`/`w1`);
    - `test_an_observation_a_frozen_initiative_cites_is_not_uncited`.
  - `test_hooks.py::test_no_hook_names_the_old_queue`: no hooks.json command names `prompting` or `compacting`, and
    `migrate status --hook` in a repository with a started initiative prints no `i1`.
  - `test_retirement.py`'s grep grows by the commands listed in Task 3.
- [ ] **Step 2: Run them.** Expected: FAIL (`work list` prints `initiative i1`; hooks.json has `prompting`).
- [ ] **Step 3: Retire** work-queue, requests r3, r4, r10-r13 and migration-tools r22, r23 with the helper. Then
  delete, create and modify as listed, and run `python3 scripts/features generate`, which removes
  `features/work-queue.feature` and regenerates requests and migration-tools.
- [ ] **Step 4: The gate.** Expected:
  - Suite: no failure.
  - `model check`: unchanged, 53/16/19/0, because the model still reads `.shop/work/`.
  - `restates`: 0 missing.
  - `vocab --check`: one handler each.
  - Collection diff: work-queue's 26 scenarios, requests' 6, migration-tools' 2, and the deleted test files' ids.
  - `grep -rn "workqueue" scripts tests --include=*.py` finds nothing but `test_kept_modules.OLD`.
- [ ] **Step 5: Commit.**
  ```bash
  git add -A scripts tests spec skills hooks features README.md CLAUDE.md
  git commit -m "the old queue retired: work-queue's lines, delegations, work add/run/retry/note/status/start/delegate, the hooks' initiative text (plan 9, Task 4)"
  ```

### Task 5: `model check` reads no `.shop/work/`

**Files:**
- Modify:
  - `spec/capabilities/design-model-check.md` (the helper: r8, r9, r12-r18, r21, r26, r27, r29, r31-r35, r37, r39,
    r45, r46, r53);
  - `scripts/model.lp` (D16's rules out; `cited/1` and the new `w_uncited_obs`);
  - `scripts/model_work.py` (no initiative, part or proposal; `cited` facts from `shop_frozen.sources`),
    `scripts/model_facts.py` (`WORK_KINDS` and the part kinds go), `scripts/model_report.py` (`why` goes),
    `scripts/model` (the `why` subcommand and the CONTRACT's `.shop/work/<initiative>` lines go; `.shop/work/` is
    "frozen, read only for the observations its sources cite");
  - `scripts/model_spec.py` and `model_requests.py`, only where they read a part or proposal;
  - `spec/decisions/0027-…`, `0036-…`, `0047-…` (D18), `spec/decisions/index.md`;
  - `tests/scripts/test_model*.py`: tests of the deleted rules go;
  - `tests/scenarios/design_model_check_handlers*.py`, `tests/scenarios/conftest.py` and `world_nodes.py`: Givens of
    work-items, initiatives and proposals go where no remaining step uses them;
  - `tests/scripts/test_decision_checks.py` (in force `{check: 4, requirement: 14, judgement: 10}`; the brief's
    judgement decisions 10, 0036 among them).

**Interfaces:**
- Consumes: Task 4's `shop_frozen.sources`.
- Produces: `model check --json` with no row whose subject is a `.shop/work/` node; `model rules` without D16's
  codes.

- [ ] **Step 1: Write the failing tests** (`tests/scripts/test_model.py`).
  - `test_frozen_work_is_not_read`: a fixture with `.shop/work/i1/initiative.md` (started, citing an unknown source),
    `w1.md` (no `part_of`), `proposal.md` (`adds: [cart#r9]`), and `.shop/work/i57/` naming `backlog#r1`. It expects
    0 violations and 0 unresolved.
  - `test_an_observation_a_frozen_initiative_cites_is_cited`: no `w_uncited_obs` for it, and one for an observation
    nobody cites.
  - `test_the_rules_of_the_old_queue_are_gone`: no D16 code in `model rules`.
- [ ] **Step 2: Run them.** Expected: FAIL (`v9a`, `v10a`, unresolved `backlog#r1`).
- [ ] **Step 3: Retire the lines**, then make the modifications. Run `python3 scripts/model decisions` and
  `python3 scripts/features generate`.
- [ ] **Step 4: The gate.** Expected:
  - `model check`: `25 violations, 16 warnings, 0 unresolved references, 0 file problems`. The 25 are the `v17` of
    the requests still read from `.shop/work/requests/` until Task 6.
  - Suite: no failure.
  - `decisions --check`: 4 hold. `test_the_live_decisions_keep_their_tiers` holds.
  - Collection diff: design-model-check's 23 scenarios, and each deleted model test named.
- [ ] **Step 5: Commit.**
  ```bash
  git add -A scripts tests spec features CLAUDE.md
  git commit -m "model check reads no .shop/work/: the old kinds' lines and rules retired, model why gone, 0027/0036/0047 re-pointed (plan 9, Task 5)"
  ```

### Task 6: Live requests in `.shop/requests/`

**Files:**
- Modify:
  - `scripts/request_text.py` (`REQUESTS`, `FROZEN`, `next_number`), `request_moves.py`, `request_view.py`,
    `intake_moves.py`, `readiness_bar.py`, `model_requests.py`, `scripts/model` (CONTRACT), `scripts/work`
    (docstring);
  - `spec/capabilities/requests.md` (Implementation: "kept in its upstream's repository as `.shop/requests/q<n>.md`;
    its number one above the highest of `.shop/requests/` and the frozen `.shop/work/requests/`"),
    `spec/capabilities/intake.md` (Implementation, where it names the path);
  - `skills/raising-a-request/SKILL.md`, `skills/taking-in-a-request/SKILL.md`, `README.md`;
  - the tests and fixtures that write `.shop/work/requests/`: `tests/scenarios/world_nodes.py`,
    `work_queue_world.py`, `design_model_check_handlers_conditions.py`, `tests/scripts/test_intake_outcome.py`,
    `test_request_view.py`, `test_model_withdrawn.py`, `test_request_asker.py`, `test_request_parse.py`,
    `test_request_counter.py`.
- Test: `tests/scripts/test_request_counter.py`, `tests/scripts/test_model.py`.

This repository's own requests are not moved here: Task 10's `migrate upgrade` moves them.

**Interfaces:**
- Produces:
  - `request_text.REQUESTS = Path(".shop") / "requests"`, `request_text.FROZEN = Path(".shop") / "work" /
    "requests"`;
  - `request_text.next_number(root) -> int`;
  - `request_text.requests(root)`, which reads `REQUESTS` only.
  - Task 9 relies on `REQUESTS`, `FROZEN` and the requests' frontmatter fields `status` and `asker`.

- [ ] **Step 1: Write the failing tests.**
  - `test_request_counter.py::test_a_new_request_is_numbered_above_the_frozen_ones`: with `.shop/work/requests/q7.md`
    and `.shop/requests/q2.md`, `work request` writes `.shop/requests/q8.md`.
  - `test_model.py::test_model_reads_no_frozen_request`: a request with no origin under `.shop/work/requests/` gives
    no `v17`, and the same request under `.shop/requests/` gives one.
- [ ] **Step 2: Run them.** Expected: FAIL (`q8` written under `.shop/work/requests/`; `v17` on the frozen file).
- [ ] **Step 3: Implement D7**, and move every fixture to `.shop/requests/`.
- [ ] **Step 4: The gate.** Expected:
  - `model check`: `0 violations, 16 warnings, 0 unresolved references, 0 file problems`. This repository's requests
    are all frozen until Task 10, and their sources still cite (D6).
  - `python3 scripts/work list` prints the 16 uncited observations and no request.
  - Suite: no failure, with nothing removed by the collection diff.
- [ ] **Step 5: Commit.**
  ```bash
  git add -A scripts tests spec skills README.md
  git commit -m "requests: live in .shop/requests/, numbered above the frozen queue's (plan 9, Task 6)"
  ```

### Task 7: `measure initiative` retired

**Files:**
- Delete (`git rm`): `scripts/measure_build.py`, `scripts/measure_read.py`, `tests/scripts/test_measure_runs.py`, and
  the `measure initiative` fixtures of `tests/scenarios/batch_measurement_*.py` that no remaining step uses.
- Modify:
  - `spec/capabilities/batch-measurement.md` (the helper: r1-r17; Purpose and narrator kept, since r18-r22 stay);
  - `scripts/measure` (the `initiative` subcommand and its CONTRACT lines go; `show`/`compare` keep the initiative's
    record), `scripts/measure_show.py`, `measure_batch_show.py`, `measure_batch_sessions.py`, `measure_write.py`
    (imports from `transcripts` and `measure_cost` only);
  - `spec/decisions/0018-measure-refuses-unknown-shapes.md` (D18), `spec/decisions/index.md`;
  - `tests/scripts/test_decision_checks.py` (in force `{check: 5, requirement: 13, judgement: 10}`), `CLAUDE.md`,
    `README.md`;
  - `tests/scripts/test_kept_modules.py` (`ALLOWED` is now empty, and is removed).
- Test: `tests/scripts/test_measure_show_old.py` (new).

**Interfaces:**
- Consumes: Task 1's `transcripts`, `measure_cost.KINDS` and `measure_cost.duration`.
- Produces: `measure show <record>` and `measure compare <a> <b>`, unchanged for both kinds of record.

- [ ] **Step 1: Write the failing test**
  `test_measure_show_old.py::test_an_initiative_measurement_is_still_shown_and_compared`. It copies one real 1.x
  record from `.shop/records/measurements/` (the newest `*-i<n>-*.md`) into a temporary repository. Then
  `measure show` prints `stages` and `totals`, and `measure compare <it> <it>` prints `ratio`, both exiting 0.
  `measure initiative i1` exits 2, naming the subcommand as unknown (argparse).
- [ ] **Step 2: Run it.** Expected: FAIL on the last assertion (`initiative` still parses).
- [ ] **Step 3: Retire r1-r17**, delete and modify as listed, then run `features generate` and `model decisions`.
- [ ] **Step 4: The gate.** Expected:
  - `decisions --check`: `5 check decisions: 5 hold` (0018's two tests among them).
  - `model check`: 0/16/0/0.
  - Collection diff: batch-measurement's 17 scenarios and `test_measure_runs`' 2.
  - `ls scripts/measure*` lists `measure`, `measure_batch.py`, `measure_batch_read.py`, `measure_batch_sessions.py`,
    `measure_batch_show.py`, `measure_cost.py`, `measure_defect.py`, `measure_show.py` and `measure_write.py`.
- [ ] **Step 5: Commit.**
  ```bash
  git add -A scripts tests spec features README.md CLAUDE.md
  git commit -m "measure initiative retired: batch-measurement r1-r17, measure_build and measure_read; show and compare keep 1.x records; 0018 a check (plan 9, Task 7)"
  ```

### Task 8: The glossary, the index, the docs and the last decisions

**Files:**
- Create: `spec/decisions/0081-the-2-0-layout.md`, `spec/decisions/0082-feature-files-written-by-features-generate.md`.
- Modify:
  - `spec/decisions/0006-feature-files-read-only-in-red-green.md` (`status: superseded`, with `tier` and
    `enforced_by` removed), `spec/decisions/index.md`;
  - `spec/index.md`:
    - the glossary per D19;
    - "Where it stands", rewritten for 2.0 in one paragraph: items, a backlog, batches and one review at the pull
      request, the old workflow retired under 0080, `.shop/work/` frozen;
    - Purpose: "items built in batches closed by one reviewed pull request" in place of "work-items taken through
      their stages by `work run`", and no "one human gate" sentence;
    - Constraints: one sentence saying that 2.0 builds on design model v5 with items in place of initiatives;
    - Composition: the retired table complete;
  - `docs/capability-format.md`: every passage on proposals, gates, rounds, work-items and `work run` reworded for
    items and batches, or cut where it describes only the old flow;
  - `README.md` (D22: the intro, layout, workflow, scripts and agents sections; `## \`work run\`` removed;
    `## 2.0.0: the workflow simplified` added);
  - `CLAUDE.md` (the sweep: every row names a file that exists, and every tracked module under `scripts/` has a row;
    the `measure_batch_*` rows per item 17);
  - `tests/scripts/test_decision_checks.py` (the totals of the Intended baselines: 82, in force
    `{check: 5, requirement: 13, judgement: 11}`, the brief's judgement decisions 11).
- Test: `tests/scripts/test_retirement.py::test_the_module_map_is_whole`.

- [ ] **Step 1: Write the failing test** `test_the_module_map_is_whole`. Each backticked `scripts/…` or `tests/…`
  path or glob in `CLAUDE.md`'s table matches a tracked file. Each tracked `scripts/*.py` and each extensionless
  script in `scripts/` is named by some row, by name or glob.
- [ ] **Step 2: Run it.** Expected: FAIL only if an earlier task missed a row. Otherwise it passes, and the report
  says it held from the start.
- [ ] **Step 3: Write 0081 and 0082, supersede 0006, regenerate the index, and edit the glossary, index, docs,
  README and CLAUDE.md.**
- [ ] **Step 4: The gate.** Expected:
  - `lexicon --check`: `401 terms, 0 problems`, since definitions change but no term is added.
  - `decisions --check`: `5 check decisions: 5 hold` (0048, 0076, 0083, 0018, 0082).
  - `test_the_sort_holds_its_totals`: 82 decisions.
  - `features generate --check`: exits 0. No glossary change alters a generated step; if one does, the regenerated
    features are part of this commit and the report names them.
  - `model logic`: as after Task 7.
- [ ] **Step 5: Commit.**
  ```bash
  git add -A spec docs README.md CLAUDE.md tests/scripts features
  git commit -m "spec and docs for 2.0: the glossary's review and measure, the 2.0 layout (0081), feature files only by features generate (0082, superseding 0006) (plan 9, Task 8)"
  ```

### Task 9: `migrate upgrade` 2.0.0 and the version

**Files:**
- Create: `scripts/migrate_upgrade_simplified.py` (D13), `tests/scripts/test_migrate_upgrade_simplified.py`.
- Modify:
  - `scripts/migrate_upgrade.py` (`STEPS` gains `("2.0.0", "the workflow simplified", "freeze .shop/work/, move the
    live requests to .shop/requests/ and write the decisions index", migrate_upgrade_simplified)`);
  - `.claude-plugin/plugin.json` (D22);
  - `spec/capabilities/migration-tools.md` (D17: r14's and r19's givens, the `release` value, `queued`, g24 and r24,
    and an Implementation bullet for the 2.0.0 step in the 1.0.0 bullet's form);
  - `tests/scenarios/migration_old.py` (`TARGET = "2.0.0"`), `tests/scenarios/migration_tools_handlers*.py` (only if
    r24's Givens need a handler that `vocab --check` names);
  - `features/migration-tools.feature` (generated);
  - `tests/scripts/test_migrate_upgrade_codified.py` (its in-process plugin version stays `1.0.0`, so it still tests
    the 1.0.0 step alone);
  - `README.md` (the 2.0.0 section names the step), `CLAUDE.md` (a row: "the 2.0.0 upgrade step "the workflow
    simplified": `.shop/work/FROZEN.md`, the live requests moved to `.shop/requests/`, the decisions index rewritten,
    and what is left reported").

**Interfaces:**
- Consumes:
  - `migrate_upgrade_ids.Changes` (`moves`, `texts`, `failures`, `notes`);
  - Task 6's `request_text.REQUESTS` and `FROZEN`;
  - `model_report.render_decisions(root)`;
  - `shop_files.context_path(root)`.
- Produces: `migrate_upgrade_simplified.plan(root) -> Changes`, and `FROZEN_TEXT` (D13's text, the one constant the
  tests compare).

- [ ] **Step 1: Write the failing tests** in `test_migrate_upgrade_simplified.py`. Build the fixture with the
  `repository(files)` helper of `test_migrate_upgrade_codified.py` (import it), and run `migrate upgrade`
  in-process with `migrate_upgrade.plugin_version = lambda: "2.0.0"`.
  - **The 1.0 repository:**
    - `.shop/plugin-version` holds `1.0.0`;
    - a codified `spec/index.md`, `spec/capabilities/cart.md` with one group, and `features/cart.feature`;
    - `spec/decisions/0001-one.md` (`tier: judgement`) and an `index.md` written without the tier column;
    - `.shop/records/observations.md` with `observation/…/o1` and `o2`;
    - `.shop/work/README.md`;
    - `.shop/work/i1/initiative.md` (started, `source: [observation/…/o1]`), `.shop/work/i1/w1.md` (drafted),
      `.shop/work/i1/cart-proposal.md` (capability-proposal, drafted);
    - `.shop/work/i2/initiative.md` (done);
    - `.shop/work/requests/q1.md` (`asker: internal`, open), `q2.md` (asker
      `bounded-context/example.org/acme/web`, open, turn upstream), `q3.md` (the same asker, delivered), `q4.md`
      (asker `product/example.org/acme`, accepted);
    - a `conftest.py` with `pytest_plugins = ["work_items"]`.
  - **Tests:**
    - `test_one_commit_freezes_the_queue`: exit 0. One new commit, `migrate upgrade: 1.0.0 to 2.0.0`, which names
      the step. `.shop/plugin-version` holds `2.0.0`. `.shop/work/FROZEN.md` holds `FROZEN_TEXT`.
    - `test_nothing_under_shop_work_changes_but_the_marker_and_the_moved_requests`:
      `git diff --name-status HEAD~1 -- .shop/work` lists only `A .shop/work/FROZEN.md` and the renames of q2 and
      q4.
    - `test_a_peers_open_request_moves_and_an_internal_one_stays`: `.shop/requests/q2.md` and `q4.md` are
      byte-identical to the old files (`git diff -M100% --name-status` gives `R100`). q1 and q3 stay where they
      were.
    - `test_the_decisions_index_is_rewritten`: it equals `model_report.render_decisions(root)`, and
      `model decisions --check` prints `is current`.
    - `test_every_open_thing_is_named_in_the_notes`: the output and the commit message hold `open initiative i1`,
      `cart-proposal.md`, `internal request q1`, `moved request q2` and `moved request q4`, and no `i2` and no
      `q3`.
    - `test_no_file_is_deleted`: `git diff --diff-filter=D HEAD~1` is empty.
    - `test_the_upgraded_repository_is_on_the_new_workflow`:
      - `model check --json` has no violation, warning subject or unresolved reference under `.shop/work/`, and no
        `w_uncited_obs` for o1;
      - `work list` names q2 and q4 and not q1;
      - `work request "x" --from <q2's asker> --lines <file>` writes `.shop/requests/q5.md`;
      - `migrate upgrade` again prints `no upgrade step is pending`.
    - `test_a_request_already_in_shop_requests_refuses_and_changes_nothing`: with a tracked `.shop/requests/q2.md`,
      the upgrade exits 1 with `could not move`, HEAD is unchanged, and `git status --porcelain` is empty.
    - `test_a_repository_with_no_work_gets_only_the_index`: with no `.shop/work/`, there is no `FROZEN.md` and the
      index is rewritten.
    - `test_a_0_29_repository_reaches_2_0_in_one_commit` (D23): r16's fixture, upgraded, has `spec/restated.json`,
      the scaffold, `FROZEN.md` and version `2.0.0` in one commit.
  - **The spec:** add D17's terms, group and line to `migration-tools.md`, edit r14's and r19's givens, and set
    `TARGET = "2.0.0"`.
- [ ] **Step 2: Run them.** `python3 -m pytest tests/scripts/test_migrate_upgrade_simplified.py tests/scenarios/test_migration_tools.py -q`.
  Expected: the step's tests fail (no module), and `@r24` fails (`FROZEN.md` not written). `@r14` and `@r19` already
  pass, because `migration_old.plugin()` copies the plugin at `TARGET` while `plugin.json` is below it.
- [ ] **Step 3: Implement D13**, add the step to `STEPS`, and set `plugin.json` to 2.0.0 (D22).
- [ ] **Step 4: The gate.** Expected:
  - Suite: no failure. The collection diff removes nothing and adds the new tests and `@r24`.
  - `model lexicon --check`: `402 terms, 0 problems`.
  - `model check`: 0/16/0/0.
  - `python3 scripts/migrate status` in this repository: `the repository's plugin version: 1.0.0`, `the plugin's
    version: 2.0.0`, `pending upgrade step 2.0.0 "the workflow simplified": …`.
- [ ] **Step 5: Commit.**
  ```bash
  git add -A scripts tests spec features .claude-plugin/plugin.json README.md CLAUDE.md
  git commit -m "migrate upgrade 2.0.0 \"the workflow simplified\": .shop/work/ frozen, live requests moved, the decisions index rewritten; plugin 2.0.0 (plan 9, Task 9)"
  ```

### Task 10: This repository on 2.0.0, its open work entered again

- [ ] **Step 1: Upgrade.** With a clean tree, run `python3 scripts/migrate upgrade`.
  - Before it, count what the notes must name:
    `grep -L '^status: \(done\|abandoned\)' .shop/work/*/initiative.md | wc -l` (open initiatives) and
    `grep -l '^status: \(open\|awaiting-asker\|awaiting-upstream\|accepted\)' .shop/work/requests/q*.md | xargs grep -l '^asker: internal' | wc -l`
    (internal requests not closed).
  - Expected: `upgraded to 2.0.0: the workflow simplified`, then one `open initiative` note for each of the first
    count, one note for each unapplied proposal, one `internal request` note for each of the second count, and
    `moved request q14 to .shop/requests/`.
  - migrate makes the one commit.
  - Save the output to `/home/vscode/.claude/jobs/7e9ba079/tmp/p9/upgrade.txt` for the report.
- [ ] **Step 2: Verify the upgrade.**
  - `git show --stat HEAD` lists `.shop/plugin-version`, `.shop/work/FROZEN.md`, the rename of
    `.shop/work/requests/q14.md`, and nothing deleted.
  - `spec/decisions/index.md` is unchanged, since it was already current.
  - `python3 scripts/migrate status` lists no pending step.
  - `python3 scripts/model check | tail -1` gives `0 violations, 16 warnings, 0 unresolved references, 0 file
    problems`. If q14 brings a violation, stop, name it in the report, and do not edit q14.
- [ ] **Step 3: Enter the surviving work** (D20), one command each, with `python3 scripts/work idea "<title>" --note
  "from <source> of the frozen queue (.shop/work/…)"`. Each commits itself.
- [ ] **Step 4: Measure the names table** (plan-8 Q2). Run `python3 scripts/conversation_hook names | wc -l` and
  `time python3 scripts/conversation_hook names`. Expected: 4 item rows, under 0.2 s. Record both. No narrowing,
  because it is under 50 rows.
- [ ] **Step 5: The gate**, all figures as the Intended baselines, then `git status --porcelain` empty.

### Task 11: Verification, the implementation report and the records

- [ ] **Step 1: The full verification.** Run:
  - the gate;
  - `python3 -m pytest -m timing -n 0 -q | tail -1` (expected `4 passed`);
  - `python3 -m pytest -q -p no:cacheprovider` twice more, recording any flaky failure by name;
  - `python3 scripts/tools size --limit 300`;
  - `python3 scripts/tools check $(git diff --name-only --diff-filter=d 19e9fee5 -- '*.py' scripts/work scripts/model scripts/measure scripts/migrate scripts/features)`;
  - `ls agents skills`;
  - `git log --oneline 19e9fee5..HEAD`.

  Each figure must be as the Intended baselines. Where `model logic` differs from the expected 4 L5, list each
  finding.
- [ ] **Step 2: The smoke run on a copy** under `/home/vscode/.claude/jobs/7e9ba079/tmp/p9/smoke`. Make it with
  `git clone -q . <dir>`, never `cp` with `rm`. In it, check out `19e9fee5`: a real 1.0 repository
  (`.shop/plugin-version` holds `1.0.0`) with 66 initiatives and 49 requests. Then:
  1. from that directory, run this branch's `migrate upgrade` by the absolute path of the worktree's
     `scripts/migrate`;
  2. check that it exits 0, that `git diff --diff-filter=D HEAD~1` is empty, and that the notes' counts are as
     Task 10 printed.

  Record the wall time.
- [ ] **Step 3: Write `plan-9-implementation.md`** in this folder, in `plan-8-implementation.md`'s form (no
  frontmatter):
  - final state: each figure as measured, beside the baseline;
  - the commits: a table of each task's commit, what was done, its verification and its collection-diff count;
  - the smoke run;
  - deviations, each with its reason;
  - D1-D23, each kept or changed;
  - the "Every item left for plan 9" table, each row settled (with its commit) or open (with its reason);
  - open problems: the 4 open rows, the requests left out by D20 (q14 to resolve), and anything found;
  - files.
- [ ] **Step 4: Index the records.** Add rows to `.shop/records/README.md` after `plan-8-rulings.md`'s:
  - `| \`2026-11-04-workflow-simplification/plan-9-implementation.md\` | plan 9 executed: the old workflow retired (271 lines of 16 capabilities under the-old-workflow-retired, \`work run\`, the queue's commands, \`measure initiative\`, ten agents and six skills deleted), \`.shop/work/\` frozen, live requests in \`.shop/requests/\`, \`migrate upgrade\` 2.0.0 and this repository upgraded, plugin 2.0.0 | report |`;
  - `| \`2026-11-04-workflow-simplification/plan-9-retire.py.txt\` | the helper plan 9 retired requirement lines with: each id into \`retired:\`, its emptied groups removed, their 0.29 ids under \`## Dropped\` | script |`.

  Tick every box of this plan.
- [ ] **Step 5: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-9-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-9-retirement.md
  git commit -m "records: plan 9 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-9-review.md`. It reads `<this plan's
  commit>..HEAD` against this plan's Review Focus and D2-D10, D13 and D17. The whole branch then goes to the person
  as one pull request to `main`.
