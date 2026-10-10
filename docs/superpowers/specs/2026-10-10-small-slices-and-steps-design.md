# Small Slices and Steps Design

Date: 2026-10-10
Status: Approved
Release: 0.11.0
Request: `docs/superpowers/requests/2026-10-10-small-slices-and-steps.md`

## Purpose

No dispatch is ever again as large as the one that ran kb's slice 156. Size becomes something the workflow
measures before the work and holds during it, and every agent's context stays small: work is handed to fresh
subagents wherever that keeps a context from growing, even when the work is serial.

The priorities, in order: a defect is found at the step that causes it; no agent's context grows with the size of
the batch; tokens. As in 0.10.0, every rule is held by the plugin's skills, agents and scripts, and nothing asks a
repository's `CLAUDE.md` to carry operational instructions.

## Evidence

### Slice 156 of kb

From shopsystem-kb, branch `batch32-kb-v2-identity`, commit `bd159cd`; the plan is
`docs/superpowers/plans/2026-10-10-kb-batch32-implementation.md` (Task 3) and the report is under
`.superpowers/sdd/2026-10-10-kb-batch32-implementation/`.

- The slice passed all three of slicing's tests: end to end, thin (six scenarios, one unknown), trimmed.
- One implementer on Opus ran it: 72 files changed (34 under `src/`, 38 under `tests/`), 37 minutes, about 426k
  tokens, 231 tool calls, one commit.
- The task review could not be one reviewer; the controller split it by area.
- Two of the plan's decisions together (one type version held; `kb:` references pinned to a version) leave a
  reference dangling when a base type changes. The implementer removed the tests that covered it so the suite
  stayed green, and reported it as a concern.
- Most of the files were migration of existing code and tests, which no scenario describes and no test of
  slicing counts.
- Slicing could not have seen the size: the slice plan names no modules and slicing reads no code. "Where the
  change lands" is first worked out by writing-plans.

### A scout comparison, 2026-10-10

Four read-only agents ran on a copy of kb at `bd159cd^` with the batch plan removed, two on Haiku and two on
Sonnet, one run each.

**Lands probe** (which existing files depend on the old id form and the old contract fields; 33 production and 36
test files that existed were changed by the commit):

| | Haiku | Sonnet |
|---|---|---|
| Counted (production, test) | 26, 42 | 30, 43 |
| Real files found | 24 of 33, 36 of 36 | 27 of 33, 36 of 36 |
| Tokens, time | 123k, 162 s | 62k, 65 s |

**Task research** (from the slice's scenarios and the plan's decisions 1 to 7: why red, where it lands, and which
existing tests the decisions make impossible to keep):

| | Haiku | Sonnet |
|---|---|---|
| Counted (production, test); the commit: 34, 38 | 34, 43 | 33, 39 |
| The dangling reference (decisions 4 and 5) | found, naming the three tests later removed | missed; called the case unaffected |
| The "kind's type" case the implementer rewrote | missed | found |
| A rule changing from `kind` to `locator` | found | found |
| Tokens, time | 236k, 7.3 min | 264k, 8.6 min |

What it shows:

- Either model puts slice 156 several times over any reasonable budget. A probe at slicing would have stopped it.
- A count from searches runs low: both probes missed 6 to 9 production modules the change reaches indirectly.
  The count is a floor, re-counted when the files are named.
- Asked which tests the decisions break, either model surfaced real conflicts before any code existed. Neither
  found all of them.
- Haiku showed no gap against Sonnet. Its token volume was the same or higher; its price per token is far lower.

## Changes

### 1. Small: a fourth test, measured at slicing

`skills/slicing-into-increments`, `scripts/plan`.

- **Small.** A slice lands in at most 8 production modules and 4 test modules, counting the migration of
  existing code and tests it forces. It joins End to end, Thin and Trimmed, required for every kind.
- **Every slice carries `- Lands: <p> production, <t> test`**, numbers only. The slice plan still names no
  module.
- **The numbers are measured where the slice changes something existing code depends on** (a contract field, an
  id's form, a shared helper's shape): a `code-scout` (change 4) searches for what depends on the old form, and
  its searches and counts are logged, `plan log "Probe: <search> -> <p> production, <t> test"`. For a slice that
  only adds, the numbers are slicing's estimate of what it adds.
- **The budget is hard.** A slice over it is split, or cut expand, migrate, contract (change 2), before any task
  is written. Steps (change 3) are not a way to keep an over-budget slice.
- **The count is a floor.** writing-plans names the files, so it re-counts. A task whose "where the change lands"
  is over the budget is not written: it goes back to slicing as a re-slice, logged.
- Rationalization added: "It's one unknown, so it's one slice" → "One unknown can still be forty files. Count
  where it lands."
- Red flags added: a slice with no `Lands:` line; a `Lands:` over the budget; a plan task whose "where the change
  lands" names more than the budget, or says "every step module".

### 2. A breaking change is cut expand, migrate, contract

`skills/slicing-into-increments`, in step 2.

When a slice would change something many existing scenarios or step modules depend on, the plan cuts:

- **Expand:** the new form added beside the old, as enabling slices. Check: the suite green.
- **Migrate:** callers moved in groups, each an enabling slice whose check names the group: the suite green, and
  a search showing the group no longer uses the old form. Where tests spell the old form, a test seam comes
  first: helpers that return today's form, and the test modules moved onto them a group at a time.
- **The capability slices**, each now small, against the expanded form.
- **Contract:** the old form removed, its own enabling slice. Check: the suite green, and the search over the
  whole tree.

Each is placed by the existing ordering rules. The walking skeleton is the first capability slice after expand.
The request's nine-step cut of slice 156 goes in the skill as the worked example, shortened.

### 3. Tasks carry research and Steps

`skills/slicing-into-increments`, "The Hand-off to writing-plans".

- **Research is a scout's.** For each task, the planner dispatches a `code-scout` (change 4) with the slice and
  the decisions taken, and reads the notes file it writes, not the source. The notes hold what the task already
  carries (why each scenario is red, where the change lands with its counts, steps and fixtures to reuse) and one
  new part.
- **Tests the decisions break.** Each task lists every existing test the plan's decisions make impossible to
  keep as it is: the test, the decisions, and what the plan decides (rewritten to what, deferred to which slice,
  or a `QUESTION FOR THE SPEC:`). The planner decides these; the scout only finds them. A test listed there is
  the only kind an implementer may change in meaning.
- **Steps.** A task whose change lands in more than about 5 files is written as ordered Steps. Each step has
  what it does, its own check (a marker green, a plain test, a search) and its own "where it lands", about 5
  files. A task at or under that size has no Steps and is one dispatch.
- Steps are not slices. They share the slice's scenarios, and the slice is green only after the last. No step
  gets a slice number or a tag.
- The task's `Review:` and `Model:` lines stand for all its steps. A step may carry its own `Model:` line.
- The plan's Global Constraints carry the execution rules of change 7, so the controller dispatches by them.

### 4. A scout agent for reading

New `agents/code-scout.md`.

- Tools: Read, Glob, Grep, Bash, Write. Model: haiku. A dispatch may name another model.
- It reads the repository the dispatch names and changes nothing in it. Its one Write is its notes file, under
  `.superpowers/scout/<run>/` in that repository, which the dispatch names. It runs searches and the red
  scenarios the dispatch names, never the whole suite, and builds nothing.
- Two dispatches:
  - **Lands probe** (slicing): given the old form and the new, the files that depend on the old form, each search
    with what it matched, and the two counts.
  - **Task research** (writing-plans): the four parts of change 3, with file and function names, following the
    repository's `CLAUDE.md`.
- Its reply is the counts, one line per conflict found, and the notes path, under ten lines.
- `.superpowers/` is git-ignored in the consuming repository; slicing adds the line if it is missing, as the spec
  skills already do.

### 5. The implementer: step mode, fix mode, PARTIAL, and tests kept

`agents/bdd-implementer.md`, `skills/bdd-red-green`.

- **Step mode.** A dispatch may name one step of the brief. The implementer reads the brief and the task's report
  file, does only that step, appends to the report, commits, and replies. The report file is the task's memory
  across steps: what each step changed, its check before and after, its suite record, and what the next step
  needs to know.
- **A step ends green.** Its check passes, and the whole suite is run once before its commit: nothing that
  passed in the task's starting record fails, though the slice's own scenarios may still be red. The record goes
  in the report, and the next step starts from it. Only the last step makes the checkpoint commit (the slice's
  Status and the plan's `Suite:` entry).
- **Fix mode.** Review findings go to a fresh implementer, dispatched with the report file and a findings file.
  It fixes the findings, re-runs the scenarios that cover the change, runs the whole suite once after the last
  fix commit, logs the record, and appends a fix report. This replaces "if resumed with review findings".
- **PARTIAL.** A new status. An implementer that has touched more than about 15 files (`git status --porcelain`
  and its own commits in the task) stops at its next green commit, writes what is done and the next step to the
  report, and replies `PARTIAL`. The controller dispatches a fresh implementer to continue from the report.
  PARTIAL is not failure; `BLOCKED` stays for decisions.
- **A test is never deleted or weakened to stay green.** Removing a test function or a parametrize case,
  loosening an assertion, or adding a skip or an xfail, to a test the brief does not list under "Tests the
  decisions break", is a stop condition: `BLOCKED`, with the test and the decisions that break it named. It is
  never a concern on a finished task. `skills/bdd-red-green` gains it among its stop conditions, with a
  rationalization ("the brief's decisions make it impossible, so I removed it and said so" → "Then the plan has a
  decision missing. Stop with the test named.").

### 6. Reviewers: scoped reviews, findings to a file, removed tests listed

`agents/bdd-task-reviewer.md`, `agents/bdd-branch-reviewer.md`.

- **Scoped by area.** A dispatch may give paths. The reviewer then reads the diff for its area,
  `git diff <base> <head> -- <paths>`, not the whole package, and says what it did not review. A large diff is
  split by area across reviewers run in parallel.
- **One review per task.** A task run as steps is reviewed once after its last step, from the commit before its
  first.
- **Removed and weakened tests.** Both reviewers list every removed or weakened test in the diff (a deleted test
  function or parametrize case, an assertion loosened, a skip or xfail added) and whether the brief lists it
  under "Tests the decisions break". One it does not list is Important. The branch reviewer has the rule because
  a batch-end task has no task review.
- **Findings to a file.** The task reviewer gains Write, for the one findings file the dispatch names. Its reply
  is the verdict, one line per issue with its grade, the backlog lines, and the path. Bash could already write
  files, so the tool adds no power the reviewer lacked; the README's table and its "what stays a request" list
  say so. The branch reviewer is unchanged in this.

### 7. A thin controller, and lanes

The plan's Global Constraints (written by the hand-off), and the README.

The plugin has no controller skill: a controller reads the plan. The hand-off has writing-plans put these rules
in the plan's Global Constraints.

- **Paths in, short replies out.** The controller dispatches with paths (brief, report, findings, review package)
  and reads replies, `plan show` and `git log --oneline`. It does not open a diff, a report, a findings file or
  source. It writes a review package by redirecting `git` output to a file. The exception is a `BLOCKED` reply:
  it reads the part of the report the reply names, to decide or to take the question to the person.
- **By step.** A task with Steps is dispatched one step at a time, each to a fresh implementer, one implementer
  at a time in a worktree. `PARTIAL` is answered with a fresh implementer.
- **Fresh fixes.** A review's findings go to a fresh implementer in fix mode, then to a scoped re-review.
- **Lanes.** The planner gives a task a `Lane: <letter>` line when its files are disjoint from every task in
  another lane and neither needs the other's code. Tasks with no `Lane:` run in order in the main worktree.
  Lanes may run at once, each in its own git worktree and branch with its own virtualenv. This overrides
  subagent-driven-development's rule against parallel implementers, and the constraint says so.
- **A lane's checkpoint is the controller's.** In a lane the implementer makes no checkpoint commit; its suite
  record goes in its report. The controller merges lanes one at a time, runs the suite after each merge, and
  writes the Status and the `Suite:` entry itself with `plan`. Checkpoints written in each lane would conflict
  in the plan's log at every merge.
- **Split reviews.** A diff over the slice budget is reviewed by area, in parallel.

### 8. `plan` holds and checks the count

`scripts/plan`, `tests/scripts/test_plan.py`.

- A slice may carry `- Lands: <p> production, <t> test`. `plan add-slice` takes it as it takes the other lines.
- `plan check`, and so every write, refuses a `Lands:` that is malformed or over 8 production or 4 test,
  naming the slice and the budget. A slice with no `Lands:` line stays valid, so plans written before 0.11.0
  still load.
- The budget is two constants in the script; the skill states the same numbers.

### 9. Release

- `.claude-plugin/plugin.json` and `marketplace.json` to 0.11.0.
- README: a section "Small slices, steps and fresh agents (0.11.0)"; `code-scout` in the agents list and table;
  the task reviewer's row gains Write; the note on running under subagent-driven-development points to the
  plan's Global Constraints.
- `docs/superpowers/specs/2026-10-06-agent-efficiency-design.md` is left as it is. Its "Parallel lanes" entry
  under Not yet is answered by change 7 here.

## Not yet

- **A tool-call budget for PARTIAL.** The request proposed about 100 calls. An agent cannot count its calls
  reliably; files touched can be read from git. Promoted if a session shows a long run over few files.
- **A controller skill.** The rules reach the controller through the plan. Promoted if a session shows a
  controller not following Global Constraints.
- **Lanes found by a script.** The planner marks them from the tasks' file lists. Promoted if lanes are marked
  wrongly by hand.
- **A second, conflicts-only scout.** Across this release's runs each model named kb's dangling reference in
  about half its runs, and a dispatch for "Tests the decisions break" alone did no better (2 of 3). The
  implementer's stop on an unlisted test is the guard. Promoted if a way of asking is found that raises the rate.
- **A scout on the small-change path.** At most two lines in existing capabilities; the controller's own reading
  is cheaper than a dispatch.

## Verification

Each changed skill and agent is tested as this repository's are: a headless baseline on a fixture before the
edit, the same prompt after, logged under `docs/superpowers/testing/`. Pinned cases:

- **Slicing a breaking change.** A fixture where one slice changes an id's form that many step modules spell.
  Before: one slice. After: a logged `Probe:`, `Lands:` lines within budget, and an expand, migrate, contract cut.
- **The scout comparison, repeated.** The two dispatches of the Evidence section on kb at `bd159cd^`, three runs
  per model, scored against the commit's files and the report's removed tests. Haiku stays the default unless it
  misses what Sonnet finds in most runs.
- **A test the decisions break.** An implementer whose brief's decisions make an unlisted existing test fail.
  Before: the test removed, a concern. After: `BLOCKED` with the test and the decisions named.
- **Step mode and PARTIAL.** A task with three Steps run by three dispatches, the report carrying each step's
  record; and a whole-task dispatch over the file budget that stops `PARTIAL` at a green commit.
- **Fix mode.** A fresh implementer fixing two findings from a findings file and the report alone.
- **A reviewer on a deleted test.** A diff that removes one parametrize case the brief does not list. After: it is
  listed and graded Important, in the findings file, with a short reply. And a scoped dispatch that reviews only
  its paths.
- **`plan`.** Tests for `Lands:` accepted, malformed, over budget, absent, and kept by `archive`.
- **On kb's next batch**, run superpowers:diagnosing-superpowers and compare: no implementer dispatch over about
  15 files or 150k tokens; the controller's peak context; no removed test outside a task's listed ones; every
  slice within its `Lands:`.
