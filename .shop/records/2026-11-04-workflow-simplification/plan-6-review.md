# Plan 6 of the workflow simplification: end-of-branch review

The one end-of-branch reviewer of `plan-6-decision-tiers.md` (decisions in tiers), 2026-11-05. The range is
`bfca3e3b..338739aa` on `workflow-simplification`: commits `b7161178`, `b59780bc`, `727a9f39`, `e20df824` and
`338739aa`. It was read against the plan's Review Focus, Global Constraints, D1-D18 and its sort table, design goal 7,
`recon.md` § Decisions, plan-1..5 rulings, `CLAUDE.md`, `spec/decisions/` and `spec/capabilities/decision-tiers.md`.
The reviewer changed nothing in the repository but this file, and did not commit it. The probes ran in scratch
repositories under `/home/vscode/.claude/jobs/7e9ba079/tmp/review6/`.

## Verdict

**Approve, with five should-fix findings and four questions for the person. Nothing blocks.** Every figure in the
report reproduces. The rules (`w_untiered`, `v_d6`-`v_d8`, the D2 file problems) behave as designed under every probe.
The bar's tier-1 check refuses and then readies as claimed. The edits to the decision files are frontmatter only (46
`status`, 24 `tier`, 17 `enforced_by` lines, plus 0074's `supersedes:`), and no `## Decision` section is touched.

The weak points are these:
- `model decisions --check`, and the bar that uses the same `run`, count a **skipped or xfailed test as holding**.
  They also run an `enforced_by` entry that is a pytest option.
- `run` uses the plugin's interpreter, not the project's.
- In the sort, 0053's `check` covers a stale table, and 0047 names a line (r32) that does not state it.
- A few decisions in force (0042, 0006) are partly broken or obsolete under the new process, and the sort left them as
  they were.

## Verification (report vs got)

The plan's exact invocations, run at `338739aa` on a clean tree.

| Check | Report | Got |
|---|---|---|
| `python3 -m pytest -q` | 1393 passed, 1 skipped, 8 xfailed, 135 subtests (29 s) | `1393 passed, 1 skipped, 8 xfailed, 135 subtests passed in 27.63s` ✔ |
| `python3 -m pytest -m timing -n 0 -q` | `2 passed, 1402 deselected` (5.6 s) | `2 passed, 1402 deselected in 5.52s` ✔ |
| unbuilt (`spec_unbuilt`) | `False 9 []` | `False 9 []` ✔ |
| `model check \| tail -1` | 53 / 16 / 19 / 0 | `53 violations, 16 warnings, 19 unresolved references, 0 file problems` ✔ |
| `model logic \| tail -1` | `11 findings: 6 L5, 5 L6` | same ✔ |
| `model lexicon --check \| tail -1` | `401 terms, 0 problems` | same ✔ |
| `model decisions --check` | index current; 4 holds (0006, 0048, 0053, 0076); exit 0; 2.9 s | same four `holds` lines, `4 check decisions: 4 hold, 0 failing`, exit 0, 2.94 s ✔ |
| `features generate --check` | exit 0 | exit 0 ✔ |
| `features vocab --check \| tail -1` | `every step has one handler` | same ✔ |
| `features bindings --unbound` | `every binding names a scenario` | same ✔ |
| `tools size --limit 300` | silent | silent, exit 0 ✔. `model_work.py` 280 (≤ 285), `model` 218 (≤ 230), `model_report.py` 192 (≤ 205), `readiness_bar.py` 151 (≤ 160), `batch_brief.py` only `CHECKS` changed ✔ |
| `tools check $(git diff --name-only 95178ceb...HEAD -- '*.py')` | clean | ruff `All checks passed!`, vulture `clean`, no import contracts ✔ |
| `git status --porcelain` after all of it | (nothing written) | empty ✔ |
| Smoke run (Task 5 Step 3), redone as probe P1 | `ready` exit 1 naming `design-decision c (check) fails: tests/test_c.py::test_c: exit 1`; `--check` exit 1 `failing  spec/decisions/c.md …`; only `?? spec/decisions/index.md` | identical, `status --porcelain --ignored` shows only `?? spec/decisions/index.md` ✔ |
| Frozen files (`world_nodes.py`, `analysis_tools_handlers.py`, `batches_handlers_more.py`, `design_model_check_handlers*.py`) | unchanged | not in the diff ✔ |
| Module map | `model_decisions.py` row; `decision-tiers` in the handlers row | both present ✔ |

## Probes

| # | Probe | Result |
|---|---|---|
| P1 | A failing `check` decision that `work-queue` rests on (`design-decision/c`), then `work ready b1` | Refused with exit 1 and the reason above. `--check` exit 1 with pytest's tail. No cache or bytecode left. ✔ |
| P2a | A check decision whose test writes `written.txt` in the cwd | `holds`. **`written.txt` is left in the repository** (M1). |
| P2b | A check decision whose only test calls `pytest.skip(...)` | **`holds`**, exit 0 (S1) |
| P2c | A check decision whose only test is `@pytest.mark.xfail` and fails | **`holds`**, exit 0 (S1) |
| P2d | `enforced_by: [--co]` | **`holds`** in `--check`: pytest only collects, exit 0. `model check` does give it as a file problem (`not a file of this repository`) (S2). |
| P2e | A `superseded` decision with `tier: check` | Run by `--check` (`holds`) and would be run by the bar. `model check` gives `v_d6` when it has no test (D3 as written) (M2). |
| P3 | `tier: Check`, `tier: [check]` | A file problem each (`tier 'Check' is not one of …`), and `w_untiered` as well ✔ |
| P3 | `tier:` (empty), no `status:` | `w_untiered` ✔ |
| P3 | `enforced_by:` as a scalar | Read as a one-entry list ✔ |
| P3 | `tier: check`, `enforced_by: []` | `v_d6` ✔ |
| P3 | `tier: requirement`, no entries | `v_d7` ✔ |
| P3 | `requirement` with `work-queue#r1` | Resolves, no row ✔ |
| P3 | `requirement` with `work-queue#r99` and `nosuch#r1` | Two unresolved references naming the decision's file ✔ |
| P3 | `enforced_by: ['tests/test_c.py::test_c[a#b]']` (a parametrised id holding `#`) | Read as a requirement: a file problem, an unresolved reference **and** `v_d6` (M3) |
| P3 | `enforced_by: [../outside.py]` (exists, outside the root) | **No problem at all** (S2) |
| P3 | Chain a → b → c, all accepted; a proposed p → a | `v_d8` gives `[a, b]` and `[b, c]`. p is silent ✔ |
| P3 | `status: superseded` that nothing supersedes | Silent: no `w_untiered`, no row (M6) |
| P4 | Head's `model decisions --check` on the base's `spec/` (`git archive bfca3e3b`) | `index.md is not what model decisions writes`, exit 1: the new `tier` column makes every older index stale (M5) |

## Findings

### Blocking

None.

### Should fix

**S1. A skipped or xfailed test counts as holding.** `scripts/model_decisions.py:79-84` (`Ran.holds` is `code == 0`)
and `:96-100`. `readiness_bar.decision_reasons` (`scripts/readiness_bar.py:132-134`) inherits this.
- Evidence: P2b and P2c each print `holds` and exit 0.
- Review Focus 2's intent is that "a test that does not run must count as failing, never as holding". A skip is
  exactly that, and a strict-less xfail enforces nothing.
- None of the four live check tests skips (`toolchain.require()` fails rather than skips), so nothing is false today.
  In a consumer repository, though, an environment-dependent skip turns a `check` decision into a silent pass.
- Fix: a run holds only when its exit is 0 **and** pytest's summary line counts at least one `passed` and no
  `skipped`, `xfailed`, `xpassed` or `deselected`. The run already uses `-q`, so the summary is the last line of
  stdout. Alternatively, pass `-rA --junitxml=<tmp outside root>` and count the outcomes. Add `skipped` and `xfailed`
  cases to `test_a_test_that_does_not_run_is_failing` (`tests/scripts/test_model_decisions.py`).

**S2. `model decisions --check` and the bar run `enforced_by` entries unchecked, and `wrong()` lets a path escape the
root.** `scripts/model_decisions.py:93` passes `*decision.tests` straight to pytest, and `:46` tests
`(root / test_file(t)).is_file()`.
- Evidence: P2d, where `[--co]` holds. P3 `../outside.py` gives no problem at all.
- `model check` names `--co` as a file problem, but `--check` and `work ready` do not consult `model check`. A typo
  such as `-k`, or an entry naming a test outside the repository, can make a check decision hold vacuously.
- Fix:
  - in `run`, give `Ran(code=None, tail="not a test of this repository: <entry>")` (failing) for any entry that starts
    with `-` or whose file does not resolve under the root, by reusing `wrong()`;
  - in `wrong()`, require `(root / test_file(t)).resolve().is_relative_to(root.resolve())`;
  - one test for each.

**S3. The decisions' tests run under the plugin's interpreter, not the project's.** `scripts/model_decisions.py:93`
(`sys.executable`).
- `tools` already finds the project's interpreter (`scripts/tools_env.py:36-45`: `.venv/bin/python`,
  `venv/bin/python`, `$VIRTUAL_ENV`), and `tools map` runs pytest with it (`scripts/tools_map.py:20-33`).
- In a consumer repository whose pytest and dependencies live in `.venv`, every `check` decision fails with
  `No module named pytest` or an import error. Then `work ready` refuses every item whose capability rests on one.
- Fix: choose the interpreter as `tools_env.interpreter` does. Import it, or move the lookup to a shared helper, since
  `interpreter(args)` takes argparse args. Add a test with a stub `.venv/bin/python`. Until then, the
  `## Implementation, may change` bullet should say `python3`, the interpreter running `model`.

**S4. 0053's `check` covers a decision whose table is stale, through a whole test file.**
`spec/decisions/0053-the-v3-agents.md:7` gives `enforced_by: [tests/scripts/test_agents.py]`.
- 0053's table (line 23) lists `feature-formulator`, which the GF conversion removed. The same file's
  `CodifiedFlow.test_no_feature_formulator_agent` (`tests/scripts/test_agents.py:100`) asserts that it does **not**
  exist.
- The table also lacks 4 of the 13 agents under `agents/`: `batch-analyst`, `delegation-answerer`, `pr-reviewer` and
  `trial-runner`.
- So the check holds while the decision's text is false, which D7's own rule ("a test fails when the decision is
  broken") does not support for the table. The general rule is enforced, by `RoleBoundaries` r1-r7: tools exactly the
  role's, `model:` named.
- Fix:
  - narrow the entry to `tests/scripts/test_agents.py::RoleBoundaries`, which holds today;
  - note in the report's open problems that 0053's table is stale and that plan 9 supersedes 0053 with the new agent
    set.

**S5. The `requirement` entries of 0047 (and 0036, 0027) are weak, and plan 9 retires them.**
`spec/decisions/0047-references-are-ids.md:7`, `0036-one-requirement-form.md:7` and the entries of `0027-…`.
- design-model-check r32 (`dangling`: "a capability-proposal that adds or removes an id its capability neither has nor
  lists as retired") is about a proposal's ids being in its capability. It does not say "a frontmatter field names a
  file by its id, never by a path", so it does not state 0047. The report says r32 "refuses a proposal's adds that
  names no id", which misreads the condition.
- r31 (`misreferenced`) and r33 (`unresolving`) state 0047 only for a work-item's `accepts` and `under`. 0036's only
  entry is r31, and 0027's r37 is `misidentified` on a work-item.
- Every one of these lines is about a work-item or a capability-proposal, the kinds plan 9 retires. When their lines
  retire, `test_the_live_decisions_keep_their_tiers` turns red on the unresolved entries.
- Fix:
  - drop r32 from 0047 (leave `[design-model-check#r31, design-model-check#r33]`);
  - add an open problem for plan 9: re-point 0027, 0036 and 0047 to lines on items (for example a backlog line that
    refuses an `--into`/reference not in `<capability>#r<n>` form), or drop them to `judgement`, in the same commit
    that retires r31, r33 and r37.

### Minor

**M1. "`--check` writes nothing" is promised beyond what it can keep.** `scripts/model` (the contract's `decisions`
paragraph: "no cache or bytecode written") and `spec/capabilities/decision-tiers.md`'s D5 bullet ("and nothing is
written there").
- Evidence: P2a. A test that writes into the cwd leaves its file in the repository.
- Fix: word it "writes nothing of its own (no `.pytest_cache`, no bytecode); what a decision's tests write is the
  tests'". Running in a throwaway copy is not worth its cost.

**M2. A tiered `superseded` or `rejected` decision is still run.** `scripts/model_decisions.py:109` and
`scripts/readiness_bar.py:124` filter on `tier == "check"` only.
- D3 lets `v_d6`/`v_d7` apply to tiered history. Running history's tests in the bar or in `--check`, though, makes a
  superseded decision able to refuse an item.
- `test_the_sort_holds_its_totals` forbids tiered history in this repository, so nothing bites today.
- Fix: run only decisions whose status is not `superseded` or `rejected`, matching `w_untiered`'s notion of "in force".

**M3. A pytest id with `#` is read as a requirement.** `scripts/model_decisions.py:25`. P3 gives three reports for one
entry.
- Fix: classify an entry as a requirement only when it matches `resolve_req`'s form (`…#r<n>` / `#r<a>-r<b>`), or
  accept the edge case and say so in the Implementation bullet.

**M4. A stale count in the spec.** `spec/capabilities/decision-tiers.md:58` reads "`w_untiered` is a warning while plan
6 sorts the 74 decisions into their tiers". There are 75 now, and the design said 72. The sort is done.
- Fix (in place, P10): "`w_untiered` is a warning; a decision gives its tier as `tier:` in its frontmatter."

**M5. The `tier` column makes every older index stale.** `scripts/model_report.py:26-27`.
- Evidence: P4. Head's `model decisions --check` on the base's `spec/` exits 1.
- Every pull request brief whose base predates plan 6 shows base exit 1 for this check (plan-5 S5 runs the head's
  scripts at the base). Every consumer repository fails `--check` after the plugin upgrade until it runs
  `model decisions`.
- Fix: note it for plan 9's `migrate upgrade` 2.0.0 step, which regenerates `spec/decisions/index.md`. Optionally,
  add a sentence in `pr-reviewer`'s brief that a base exit of 1 there is expected across a format change.

**M6. `status: superseded` with no superseder passes silently.** P3. Writing `superseded` silences `w_untiered` with
nothing pointing at it.
- Live: all 46 superseded decisions have a superseder. 9 of them are reached only through a decision that is itself
  superseded (0007, 0008, 0009, 0010, 0012, 0013, 0023, 0059, 0063), which is fine as history.
- Fix: a later `w_unsuperseded` warning needs a line first. Raise it as an idea; do not add it now (no line, no rule).

**M7. Deviation 3 loses per-case reporting.** `test_a_wrong_enforced_by_is_named` and `test_v_d8_…` loop with
`reset()` instead of `subTest`, so a failure names only the first failing case. That is acceptable for keeping the
subtest count at 135, but a `subTest` would cost one count per case and say which case failed. It is the person's
call; no change is needed.

### Questions for the person (with recommended rulings)

**Q1 (D6). design-model-check r52 against decision-tiers r5.**
- The facts:
  - r52 reads "Where `--check` is given, when the person runs `model decisions` on a decisions index, `model` shall
    exit successfully" (`spec/capabilities/design-model-check.md:273`). Note that it says "a decisions index", not "a
    current" one.
  - r51 (stale → error) already contradicts r52's letter in exactly the way r5 does. The two have coexisted since the
    codification, under the reading that an unwanted-behaviour `If … then` line overrides the plain `When` line.
  - That reading is stated nowhere in this context: not in `spec/index.md`, and not in 0051, which lists the EARS
    patterns but no precedence.
- **Recommended ruling:** keep r52 unchanged (it is merged; retiring it buys nothing that r51 does not already need).
  Write the precedence rule down once, as one sentence in `spec/index.md`'s Testing (or Constraints) section: "An
  unwanted-behaviour line (`If … then`) of a capability takes precedence over an event-driven or ubiquitous line of
  the same command where both apply." The plan-1 definitions there may be fixed in place (P10). If the person prefers
  the letter fixed, plan 9 (which retires design-model-check's old-kind lines anyway) retires r52 and adds "…on a
  decisions index that is not stale, while every `check` design-decision holds, … shall exit successfully".

**Q2. 0042 (superpowers-not-a-dependency) is in force as `judgement`, and the new process already contradicts it.**
- 0042 says "No skill, agent or script of the plugin names a superpowers skill … delivery is `delivering-an-initiative`
  and `work run`".
- `skills/shaping-items/SKILL.md:16` names `superpowers:brainstorming` (plan 3, before this range). Design goal 5
  builds batches "as superpowers' subagent-driven development". Delivery is now `building-a-batch`.
- The `pr-reviewer` now reads 0042 as a judgement decision (plan 5 D6), so it will flag any batch that touches those
  skills.
- **Recommended ruling:** supersede 0042 now with a new `0077-superpowers-composed-not-required.md`. It keeps
  "`.claude-plugin/plugin.json` has no `dependencies`, and the README names clingo, pytest and pytest-bdd". It says "a
  skill may name a superpowers skill it composes with, and never requires it". It is `tier: judgement`, or `check` with
  a small test that `plugin.json` has no `dependencies`. This takes the frontmatter-only path that 0075 took for 0046.
  The alternative is to add 0042 to plan 9's list.

**Q3. 0006 (feature-files-read-only-in-red-green) is `check` on a test that enforces a different, newer rule.**
- 0006's text is about bdd-red-green: no `.feature` opened for writing, except `features retire` of a deprecated
  scenario under `Retires:`, with HAND-BACK log entries. Deprecation, `Retires:` and HAND-BACK are old process.
- Its test (`features generate --check`) enforces "feature files are what the generator writes", the GF-era rule.
- The batch subagent's brief still names bdd-red-green's rules (plan-4 S4), so 0006 still governs something.
- **Recommended ruling:** keep it as is until plan 9. In plan 9, supersede 0006 with a `check` decision "a feature file
  is written only by `features generate`" carrying the same test. Add this to the open problems.

**Q4. 0026 (work-file-forms) is superseded by 0074, but part of it survives.**
- Its `records/observations.md` form (one `## <id>` heading per observation, with `about:`, `by:` and `date:`) and
  "other records: frontmatter id, kind, about" still govern `.shop/records/`, which stays and which `w_uncited_obs`
  reads.
- The `.shop/work/` forms do go, frozen in plan 9.
- **Recommended ruling:** leave it superseded (history). Plan 9's decision on the 2.0 layout restates the forms that
  survive: `.shop/backlog/b<n>.md`, `.shop/batches/<n>/`, the records and observations. Add this to the open problems.

No other of the 27 decisions superseded by 0074 governs code that stays after plan 9 (see the audit below).

## Sort audit

The sample covers all 4 `check`, 14 of the 15 `requirement` (all but 0049, whose migration-tools r1 was read and
states it), all 8 `judgement` and 15 of the 27 superseded by 0074. Each row
is judged against design goal 7 and D7's rules.

| # | applied | `enforced_by` | judgement |
|---|---|---|---|
| 0006 | check | `test_decision_checks.py::test_the_features_are_what_features_generate_writes` | Holds; it enforces the rule's effect, but the text is old process (Q3) |
| 0048 | check | `test_bound.py::BoundTest::test_every_scenario_has_exactly_one_test` | Right: the decision names this test. Its first paragraph ("step definitions in that module") is stale against the vocab registry, but the check part is exact. |
| 0053 | check | `tests/scripts/test_agents.py` | Narrow it to `::RoleBoundaries`; the table is stale (S4) |
| 0076 | check | `test_decision_checks.py::test_every_tracked_python_file_is_300_lines_or_fewer` | Right: design goal 7's own example |
| 0001 | requirement | dmc#r36, #r38 | Acceptable: r38 states the pairing by name. "One spec, never a second" has no line, and that part is judgement. |
| 0018 | requirement | batch-measurement#r6, #r7 | Right: the refusal of an unknown shape, naming it |
| 0024 | requirement | dmc#r4 | Right in part: a retired id is not reused. "Joins when the proposal is merged" is old process. |
| 0025 | requirement | dmc#r47, #r48 | Right: r48 is "says how to install clingo" |
| 0027 | requirement | dmc#r36, #r37 | Right today; r37 is a work-item line that plan 9 retires (S5) |
| 0033 | requirement | dmc#r22-r24 | Right: exactly `v_t1`-`v_t3` |
| 0036 | requirement (moved up) | dmc#r31 | Acceptable today, for `accepts` only; plan 9 retires r31 (S5). The move up is evidenced as D7 asks. |
| 0045 | requirement | dmc#r42 | Acceptable: the old layout refused, naming `scripts/migrate` |
| 0047 | requirement | dmc#r31, #r32, #r33 | Drop r32, which does not state it; the others are work-item lines (S5) |
| 0051 | requirement | dmc#r25 | Right: a line outside the EARS grammar is `v_p1` |
| 0054 | requirement | dmc#r10, #r11 | Right: r11 is overtagged, r10 is untested |
| 0060 | requirement | batch-measurement#r1 | Right until plan 7 (open problem noted) |
| 0062 | requirement | migration-tools#r13, #r14 | Right |
| 0075 | requirement | decision-tiers#r1-r3 | Right |
| 0016 | judgement | — | Right: an experiment per release; tuning is plan 7's |
| 0035 | judgement | — | Right: dependencies taken as needed |
| 0042 | judgement | — | Partly contradicted by the new skills (Q2) |
| 0058 | judgement | — | Right. Arguably partly `requirement`, since the grammar allows only "exit successfully"/"with an error", but no single line states it. |
| 0065 | judgement | — | Right until plan 9 narrows it (noted) |
| 0067 | judgement | — | Right |
| 0071 | judgement (moved down) | — | Right: requests r42 and r57 are 0.29 ids under `## Dropped` (`spec/capabilities/requests.md:211,217`) |
| 0074 | judgement | — | Right |
| 0002 | superseded (0074) | — | Right: the gate is replaced by the readiness bar |
| 0004 | superseded (0074) | — | Right: blind spec-writer agents; the agents' tools stay under 0053 |
| 0005 | superseded (0074) | — | Right: the planner stage goes; a batch writes its own plan |
| 0011 | superseded (0074) | — | Right: `@deprecated` was deleted in 1.0 |
| 0026 | superseded (0074) | — | Mostly right; the records part survives (Q4) |
| 0034 | superseded (0074) | — | Acceptable: the integrate and formulate rounds go, and the skill's own description keeps "on demand only" |
| 0044 | superseded (0074) | — | Right: the planner goes |
| 0050 | superseded (0074) | — | Right: a migration of living plans to work-items; `migrate run` keeps it as history |
| 0061 | superseded (0074) | — | Right: work-items go, and items are `b<n>` under backlog's lines |
| 0064 | superseded (0074) | — | Right: rulings and answers on work-items |
| 0066 | superseded (0074) | — | Right: the initiative ledger |
| 0068 | superseded (0074) | — | Right: `work run` as the coordinator |
| 0072 | superseded (0074) | — | Right: `work show <item>` is governed by backlog's lines now |
| 0073 | superseded (0074, was proposed) | — | Right: its standing part is 0033's, which is in force; glossary-proposals go |

The totals check out: 75 decisions, `{accepted: 27, superseded: 46, rejected: 2}`, and in force
`{check: 4, requirement: 15, judgement: 8}`. Every live `superseded` decision has a superseder, 37 directly by an
accepted one.

## The deviations

| # | Deviation | Judgement |
|---|---|---|
| 1 | Task 1's figure is 71 violations, not 72 (0049 supersedes the rejected 0032) | Correct arithmetic; the plan miscounted |
| 2 | `test_the_decisions_run_side_by_side` is marked `timing` | Right, per the repository's rule for time ceilings (plan-3 S5) |
| 3 | Parametrised cases as loops in `ModelTest` | Acceptable (M7) |
| 4 | Dropping `-B` alone stays green | A correct observation; keeping both guards is right |
| 5 | The 0012 mutation turned into 0019 | Right: 0012's superseder 0038 is itself superseded now, so `w_untiered` is what fires, and the replacement shows a live `v_d8` |
| 6 | 0075's and 0076's `source` written in full | Right, and the live guard caught it: a good sign for D17 |
| 7 | The local Then keyed `("ThenDoes", "test")` | Right: local keys are (template, kind) |
| 8 | `Ran.timeout`, `PYTEST_ADDOPTS` dropped, `wrong()` in `model_decisions` | All improvements; dropping `PYTEST_ADDOPTS` closes a real hole in Review Focus 2 |
| 9 | Smoke times taken through Python | Harmless |
| Sort | 0071 down, 0036 up, 0047 re-pointed | 0071 and 0036 are evidenced and right. 0047's r32 is a misreading (S5). |

## Review Focus, item by item

1. **A check that writes in the repository.** Cache and bytecode are held: P1, `status --ignored` clean. What a test
   writes itself is not held (M1).
2. **The repository's pytest settings.** `addopts` and `PYTEST_ADDOPTS` are cleared, and exits 4 and 5 and a timeout
   are failing. **A skip and an xfail hold (S1).**
3. **An `enforced_by` written wrong.** Every case of the plan is named. A path escaping the root, and an option entry
   at run time, are not (S2).
4. **History and supersession.** Every case holds, the A → B → C chain included. A superseded decision with no
   superseder is silent (M6).
5. **The bar's match against `rests_on`.** Both forms match, a decision not rested on is not run, and each runs once
   a process: the tests exist and pass, and P1 confirms. Note that today only the old capabilities rest on a `check`
   decision. The new capabilities rest only on 0074, so the bar's tier-1 check runs for no item into backlog,
   readiness, batches or pr-review. That is by design (D13), and worth knowing when tuning the bar.

## Open problems to add for plans 7-9

These are in addition to the report's list:
- S4: 0053's table is stale, and plan 9 supersedes it with the new agent set.
- S5: re-point 0027, 0036 and 0047 when design-model-check r31, r33 and r37 retire.
- Q3: 0006 superseded by a "features are generated" `check` decision.
- Q4: the forms that survive into 2.0, restated in a decision.
- M5: the 2.0.0 upgrade step regenerates `spec/decisions/index.md`.
