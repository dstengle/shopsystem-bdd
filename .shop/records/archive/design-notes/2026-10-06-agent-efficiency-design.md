# Agent Efficiency Design

Date: 2026-10-06
Status: Approved

## Purpose

Make the agents that run this workflow spend less wall-clock time, fewer tokens and less repeated work on the
same outcome, with every rule held by the plugin: its skills, its agents and the scripts it ships. Nothing here
asks a repository's `CLAUDE.md` or a batch plan to carry operational instructions; where a repository must
change, the plugin's own workflow finds it and cuts the slice.

The priorities, in order: wall-clock, then tokens, then repeated work. Each change is the smallest one that
removes the cost its evidence shows; a script is shipped only where hand edits went wrong or repeated.

## Evidence

From a diagnosis of one shop-knowledge session on shopsystem-bdd 0.9.0 (875cf22f, 2026-10-05/06: a migration to
`spec/`, a kb pin bump, formulation, slicing, a nine-task batch under subagent-driven development, a fix wave).
The report is kept at
`~/.superpowers/diagnosing-superpowers/875cf22f-366c-4628-b5b9-c0e63fb6c61d/report.md`, every finding cited to a
transcript line.

- **The suite.** It took 100–206 s a run and ran about 34 times, about 67 minutes. 0.9.0 already runs the
  slice's marker during red-green and the whole suite once per slice; the extra runs came from what 0.9.0 left
  in place: `agents/bdd-implementer.md` still says "Run the whole suite at the start and once before you
  commit"; the batch plan added "record the failing list at each slice's start"; an enabling slice whose check
  is the suite iterated on it (12 runs in one task); reviewers and the controller ran it again on a commit
  already run. The suite ran serially and started the command under test as a subprocess, against "Keep the
  Suite Fast", with no reason in the repository's `CLAUDE.md`, and nothing checked it before the batch.
- **A dependency read, not probed.** The controller read kb's operate-a-store capability with a `sed` range
  ending at "## Not yet", which cut off the line listing `kb serve` as not built, and told the Task 3
  implementer it was installed. Cost: a hand-back, two re-slices, and 137 lines of test code written, patched
  in the fix wave, then deleted.
- **A rule-decided split handed back.** Task 4 was handed back green only because `cli.py` crossed the size
  limit, though the repository's rules already said where new code goes; one extra round trip.
- **A behaviour defect graded Minor.** Task 4's per-task review found a refused lookup read as "found and not
  empty" (starting a second store), graded it Minor because no scenario covered it, and it was carried to
  Task 5 and resurfaced at the branch review.
- **The controller's context.** One turn ran integration, migration, formulation, slicing, planning, the batch,
  the branch review, the fix wave and the push. Main's context reached about 507k tokens per call, so every late
  turn re-read half a million tokens; that turn holds 83% of main's new tokens. Into it went the spec agents'
  returns: the capability-writer returned every capability file and the whole ledger on each of three rounds
  (about 141k output tokens), five transcript lines over 100 KB.
- **Hand edits of the plan and features.** The controller edited the living slice plan about 8 times and probed
  it about 11 times with one-off `sed` and Python, once corrupting it; counted scenarios per tag by looping
  `pytest --collect-only` over 40 tags, twice; and hand-wrote the scenario re-pairing and its verification for
  the migration.

What the evidence does not call for: per-task review of every task. The batch-end tasks (1, 7, 8, 9) had no task
review by 0.9.0's review-by-risk, and the branch review found their two Important issues in one fix wave. That
is the design working: a per-task review buys earlier detection with an Opus agent per task and serial
wall-clock, and pays only when a later task builds on the defect, which is the risk per-task review is already
assigned by.

## Changes

### 1. A fast suite before the batch

The suite's speed multiplies every run that remains, so it is fixed first, not left to a later batch.

- `skills/slicing-into-increments` step 1 already runs the suite. It also records the run's wall time in the
  `Suite:` log line, and whether the project's test command runs in parallel and the step definitions drive
  the entry point in-process (one test per command as a program, per `skills/bdd-red-green`'s "Keep the Suite
  Fast").
- A suite that takes over 60 s and fails either property, with no reason in the repository's `CLAUDE.md`, gets
  an enabling slice cut **first** in the batch. Its check: the same passed and failed counts, and the wall time
  under the bound the slice states.
- `agents/bdd-branch-reviewer.md` reports the suite's wall time beside its summary line, so a suite that has
  slowed again is visible at the next slicing.

### 2. Each suite run counts once

Removes the leftovers 0.9.0 did not clean up, and lets a recorded result stand for its commit.

- `agents/bdd-implementer.md` drops "at the start". The task's starting state is the last recorded result,
  which the controller names in the dispatch. While iterating: the slice's marker and the test module the
  scenario lives in, as `skills/bdd-red-green` says. The whole suite once, before the slice's last commit.
- **A result holds for its commit.** The `Suite:` line, wherever it is recorded (the implementer's report, the
  plan's log, the branch review), carries the commit's short hash: `Suite: <N> passed, <M> failed at <hash>`,
  with the failing list beside it when non-zero. A record names the commit that was run, so it is written after
  that commit: the implementer commits the change, then commits its checkpoint and `Suite:` line to the plan's
  log. A record holds at `HEAD` when nothing outside `docs/superpowers/plans/` differs between its commit,
  `HEAD` and the working tree (`plan show --last-suite --current` says so). Whoever needs a result and finds
  one that holds uses it rather than running again: the task reviewer (who already does not re-run), the
  branch reviewer for its baseline, the controller before a push, slicing's step 1. Installing or upgrading a
  dependency without a commit invalidates the record; run again.
- The branch reviewer runs the suite once, at the batch's head, and records it; the controller pushes on that
  record when nothing has been committed since. A fix wave's last commit gets one whole run by its implementer,
  which then stands for the push.
- **An enabling slice iterates on what it touches.** Where its check is the suite, `skills/bdd-red-green`'s check
  cycle iterates on the test modules the change affects and the ones the check's failure names, and runs the
  whole suite once at the end.
- **Plans carry no run protocol.** The hand-off to writing-plans (`skills/slicing-into-increments`) gives each
  task its markers and expected counts only; when to run what is `skills/bdd-red-green`'s and the agents'. A
  plan that restates run rules is a red flag, listed in the skill.

Changes in `agents/bdd-implementer.md`, `skills/bdd-red-green`, `skills/slicing-into-increments`,
`agents/bdd-task-reviewer.md`, `agents/bdd-branch-reviewer.md`.

### 3. Plan on what exists

- **A dependency capability is probed at the pin.** `skills/slicing-into-increments`: a slice whose Needs names
  something a dependency provides carries a probe, a command run against the installed version whose output
  shows the thing exists (`kb serve --help` exits 0). Run while planning; the command and its result go in the
  plan's log. A failing probe marks the slice `blocked: awaiting <dependency>`, with the request to the
  dependency logged, before any task is written for it.
- A reading of the dependency's spec is not a probe. Where its spec is read at all, the capability file is read
  whole, never a section range: "Not yet" is where the missing thing is listed. Both go in the skill's
  rationalizations table.

### 4. Fewer round trips

- **A split the rules decide is the implementer's.** `agents/bdd-implementer.md`: when a module would cross a
  size limit and the repository's rules already say where the code goes (a new concern gets a new module and a
  row in the module map), the implementer makes the split and records it in the checkpoint. It hands back only
  when no rule decides it. The size-limit stop condition is narrowed to that case.
- **A behaviour defect is never Minor.** `agents/bdd-task-reviewer.md` and `agents/bdd-branch-reviewer.md`:
  behaviour that contradicts a Behaviour line or a capability's Purpose is Important, whether or not a scenario
  covers it. Where no scenario covers it, it is also a question for the spec: the fix lands in this batch's fix
  wave, or the next batch through the small-change path, with the line that makes it a scenario. It is never
  carried to a later task as a minor.
- Review-by-risk stays as 0.9.0 has it.

### 5. A smaller controller context

- **Execution starts in a fresh session.** `skills/slicing-into-increments`, at the hand-off to writing-plans:
  once the plan is written and committed, recommend executing it in a new session that reads the plan file,
  not in the session that integrated, formulated and sliced. The plan already carries everything a task needs;
  the earlier context is cost, not input. The person chooses; the skill states the recommendation and why.
- **Spec agents' drafts go to a file.** `agents/capability-writer.md` and `agents/feature-formulator.md` gain
  Write, for one scratch path only: `.superpowers/spec-drafts/<run>/`. They still read only `spec/`,
  `features/`, `docs/` (and `adrs/` when named). A capability or feature file is drafted in full only when it
  is new, otherwise the changed sections or scenarios; the ledger is append-only, so new entries only. Their
  reply is the change list and the paths, under a few KB.
- The path is held the way the read limits already are: by the agent's instructions, and by the controller's
  existing check of returned files against the change list (`skills/integrating-a-proposal`,
  `skills/formulating-features`), extended to "every file written is under the drafts path". The controller
  reads what it checks and applies it.
- `.superpowers/` is git-ignored in the consuming repository; the skill that first writes under it adds the
  line to `.gitignore` if missing.

## Scripts

Two, where hand edits went wrong or repeated. Shipped in the plugin under `scripts/`, plain Python 3 from the
standard library, each with `--help` as its contract and its own tests on a fixture repository. Each prints a
short result and exits non-zero on failure, and refuses an edit that would leave its file invalid.

A skill names a script by its path relative to the skill's base directory (`../../scripts/features`), which a
loaded skill knows. An agent that needs one gets its absolute path in the dispatch: slicing, which knows its
base directory, writes `Scripts: <absolute path>` into the plan's Global Constraints, which every task brief
carries. The skills name the commands, never their internals.

1. **`features`**, for feature files read and edited without the test runner.
   - `features count --by-tag` and `features list --tag T | --title S` parse Gherkin directly; outlines count
     their Examples rows.
   - `features tag "<title>" slice-N` replaces or adds a scenario's slice tag and touches nothing else: the
     slicer's one permitted edit.
   - `features move` and `features verify-moved --from <dir>` move scenarios verbatim and check that every
     Background-plus-scenario block before equals one after, for migration's re-pairing.
   - Used by `skills/slicing-into-increments`, `skills/migrating-to-capabilities`, `skills/formulating-features`.
2. **`plan`**, for the living slice plan.
   - `plan log "<line>"`, `plan status <n> <status>`, `plan add-slice`, `plan backlog "<line>"`,
     `plan archive <batch>`.
   - `plan show --open | --backlog | --requests | --last-suite`, the third listing the requests logged for other
     repositories, the last printing the latest `Suite:` line and its commit.
   - It keeps the plan's sections and order valid.
   - Used by `skills/slicing-into-increments`, the controller's checkpoints and the implementer's checkpoint
     line.

## Not yet

- **A `suite` script** recording runs with a working-tree digest. The hash on the `Suite:` line and a clean tree
  cover the evidence; promoted if runs on a dirty tree turn out to be common.
- **`probe`, `ledger` and `shape` scripts.** A probe is one command and its output in the log; the ledger is
  append-only by instruction and checked at the gate; the size check is one command the branch reviewer runs.
  Promoted when a diagnosis shows one of them going wrong by hand.
- **Parallel lanes.** File-disjoint slices could run at once; batch 14's tasks ran strictly in sequence for
  1 h 49 min. Subagent-driven development forbids parallel implementers, and a lane needs a checkout with its
  own virtualenv. Promoted when superpowers' wave execution (obra/superpowers#2368) lands.
- **The 17.4 h hold.** One Bash call in the branch reviewer took 17.4 h to return an immediate zsh error. Whether
  the machine slept between 2026-10-05 23:19Z and 2026-10-06 16:43Z decides whether it is the environment's or
  the harness's; it is not the workflow's, and is tracked separately.

## Verification

- Each changed skill and agent is tested as this repository's skills are: a headless baseline on a fixture
  before the edit, the same prompt after, logged under `docs/superpowers/testing/`. Pinned cases: an implementer
  that would run the suite at the start; a dependency slice whose capability lists the need under Not yet; a
  module about to cross its size limit with a module map that places the code; an uncovered behaviour defect
  in a task's diff; a capability-writer round on an existing spec.
- The two scripts carry their own tests on a fixture repository with features, an outline and a plan.
- On the next shop-knowledge batch, run superpowers:diagnosing-superpowers again and compare: whole-suite runs
  at most one per slice plus one by the branch reviewer, and their total time; no hand-back caused by a missing
  dependency capability or a rule-decided split; the controller's peak context; spec agents' replies under a
  few KB each; no one-off plan or feature edits in the controller's Bash calls.
