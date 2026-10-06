# Agent Efficiency Design

Date: 2026-10-06
Status: Draft for review

## Purpose

Make the agents that run this workflow spend less wall-clock time, fewer tokens and less repeated work on the
same outcome, with every rule held by the plugin: its skills, its agents and scripts it ships. Nothing here
asks a repository's `CLAUDE.md` or a batch plan to carry operational instructions; where a repository must
change, the plugin's own review finds it and cuts the slice.

The priorities, in order: wall-clock, then tokens, then repeated work.

## Evidence

From a diagnosis of one shop-knowledge session (875cf22f, 2026-10-05/06: a migration to `spec/`, a kb pin bump,
formulation, slicing, a nine-task batch under subagent-driven development, a fix wave). The report is kept at
`~/.superpowers/diagnosing-superpowers/875cf22f-366c-4628-b5b9-c0e63fb6c61d/report.md`, every finding cited to a
transcript line.

- The whole suite (100–206 s a run) ran about 34 times, about 67 minutes. 0.9.0's red-green says once per slice,
  but `agents/bdd-implementer.md` says "Run the whole suite at the start and once before you commit"; the batch
  plan added "record the failing list at each slice's start"; an enabling slice whose check is the suite
  iterated on it (12 runs in one task). The suite ran serially and started the command under test as a
  subprocess, against "Keep the Suite Fast", with no reason given in the repository's `CLAUDE.md`; nothing
  checked it.
- A slice was planned on a dependency capability (`kb serve`) read from the dependency's spec, not probed at the
  pinned version, where it was listed under Not yet. Cost: a hand-back, two re-slices, and 137 lines of test code
  written, patched in the fix wave, then deleted.
- An implementer handed back a green slice only because a module crossed the size limit, though the repository's
  rules already said where new code goes; one extra round trip.
- A behaviour defect (a refused lookup read as "found and not empty", starting a second store) was reviewed as
  Minor because no scenario covered it, carried to the next task, and resurfaced at the branch review.
- The capability-writer returned every capability file and the whole ledger on each of three rounds (about 141k
  output tokens). Spec agents' returns landed in the controller's context (five transcript lines over 100 KB),
  which every later turn re-read; the controller's context reached about 507k tokens.
- The controller edited the living slice plan about 8 times and probed it about 11 times with one-off `sed` and
  Python, once corrupting it; counted scenarios per tag by looping `pytest --collect-only` over 40 tags, twice;
  and hand-wrote the scenario re-pairing and its verification for the migration.

## Changes

### Running the suite

1. **One whole run per slice.** `agents/bdd-implementer.md` drops "at the start". The task's starting failing
   list is the last recorded result at the commit it starts from (script `suite`, below), which the controller
   names in the dispatch. While iterating: the slice's marker and the test modules the change touches
   (`suite --affected`). The whole suite once, before the slice's last commit. `skills/bdd-red-green` says the
   same in one place, and the agent cites it rather than restating it.
2. **A result holds for its commit.** A recorded suite result carries the commit and the working tree's state.
   Whoever holds a result for the current state uses it: the task reviewer, the branch reviewer, the controller
   before a push, slicing's step 1. The branch reviewer runs the suite once and records it; the controller pushes
   on that record. Changes in `skills/bdd-red-green`, `skills/slicing-into-increments`,
   `agents/bdd-task-reviewer.md`, `agents/bdd-branch-reviewer.md`.
3. **An enabling slice iterates on the affected modules.** Where its check is the suite, the check cycle in
   `skills/bdd-red-green` iterates with `suite --affected` and runs the whole suite once at the end.
4. **"Keep the Suite Fast" is checked.** `agents/bdd-branch-reviewer.md` reports the suite's wall time and whether
   it runs in parallel and drives the entry point in-process. A suite that does neither, with no reason in the
   repository's `CLAUDE.md`, is a finding that `skills/slicing-into-increments` cuts as an enabling slice in the
   next batch, by risk like any other.
5. **Plans carry no run protocol.** The hand-off to writing-plans (`skills/slicing-into-increments`) gives each task
   its markers and expected counts only; when to run what is the agents' and the scripts'. A plan that restates
   run rules is a red flag.

### Planning on what exists

6. **A dependency capability is probed at the pin.** A slice whose Needs names something a dependency provides
   carries a probe (script `probe`) run against the installed version while planning; a failing probe marks the
   slice blocked in the plan, with the request to the dependency logged, before any task is written for it. A
   reading of the dependency's spec is not a probe. `skills/slicing-into-increments`.

### Fewer round trips

7. **A split the rules decide is the implementer's.** `agents/bdd-implementer.md`: when a module would cross a
   size limit and the repository's rules already say where the code goes (a new concern gets a new module and a
   row), the implementer makes the split and records it in the checkpoint. It hands back only when no rule
   decides it.
8. **A behaviour defect is never Minor.** `agents/bdd-task-reviewer.md`: behaviour that contradicts a Behaviour
   line or a capability's Purpose goes to the controller as a plan action, whether or not a scenario covers it.

### Spec agents' output

9. **Only what changed comes back.** `agents/capability-writer.md`, `agents/feature-formulator.md`,
   `skills/integrating-a-proposal`, `skills/formulating-features`: the ledger is append-only, so new entries only;
   a capability or feature file in full only when it is new, otherwise the changed sections or scenarios.
10. **Drafts go to a file.** The capability-writer and the feature-formulator may write under one scratch path
    (`.superpowers/spec-drafts/<run>/`) and nowhere else; they still read only `spec/`, `features/` and `docs/`.
    Their reply is the change list and the paths. The controller reads what it checks and applies it with the
    scripts (`ledger`, `features`). Their tool lists gain Write restricted to that path.

## Scripts

Shipped in the plugin under `scripts/`, called by path from the skills and agents that use them, as superpowers'
subagent-driven development ships its own. Plain Python 3 from the standard library, plus the project's own test
runner; each prints a short result and exits non-zero on failure. Each script's `--help` is its contract; the
skills name the commands, never their internals.

1. **`suite`**, for runs and their evidence.
   - `suite` runs the project's test command and records the summary line, the failing list, the commit and
     a digest of the working tree in `.superpowers/suite/last.json`. If the commit and digest match the record,
     it prints the record and does not run.
   - `suite --affected` runs the slice's marker (`--marker slice-N`) and the test modules the working tree's
     diff touches.
   - `suite --compare` prints the scenarios that left or joined the failing list since the record a task
     started from.
   - The project's test command comes from the project's usual place (`Makefile` target `test`, else
     `python -m pytest -q`), never from an instruction file.
2. **`features`**, for feature files read without the test runner.
   - `features count --by-tag` and `features list --tag T | --title S` parse Gherkin directly; outlines count
     their Examples rows.
   - `features tag "<title>" slice-N` replaces or adds a scenario's slice tag and touches nothing else, the
     slicer's one permitted edit.
   - `features move` and `features verify-moved --from <dir>` move scenarios verbatim and check that every
     Background-plus-scenario block before equals one after, for re-pairing.
3. **`plan`**, for the living slice plan.
   - `plan log`, `plan status <n> <status>`, `plan add-slice`, `plan backlog`, `plan archive <batch>`.
   - `plan show --open | --backlog | --requests`, the last listing the requests logged for other repositories.
   - It keeps the plan's sections and order valid, and refuses an edit that would break them.
4. **`ledger`**, for `spec/decisions.md`.
   - `ledger add <id> --line ... --date ... [--supersedes ...] [--revisit-when ...] [--source ...]` appends one
     entry in the capability format and refuses a duplicate id. It never edits an existing entry.
   - `ledger show <id>`.
5. **`shape`**, for the structural checks.
   - `shape` reports modules over the size limit and imports outside an allowlist, both read from a
     `[tool.shopsystem-bdd]` section the plugin defines (in `pyproject.toml` or the stack's equivalent). That
     section is data the scripts read, not instructions an agent follows.
   - The branch reviewer and enabling slices call it instead of hand-typed `wc` and `grep` lines.
6. **`probe`**, for change 6.
   - `probe "<command>" --expect "<substring or exit status>" --slice <n>` runs the command against the
     installed dependency and records the result beside the slice in the plan (through `plan`).

## Not yet

- **Parallel lanes.** File-disjoint slices could run at once; batch 14's mostly independent tasks ran strictly
  in sequence for 1 h 49 min. Subagent-driven development forbids parallel implementers, and a lane needs a
  checkout with its own virtualenv. Promoted when superpowers' wave execution (obra/superpowers#2368) lands.
- **Work stopping while the person is away.** A command in one session held for about 17 hours with no recorded
  cause; this is the harness's or the environment's, not the workflow's, and is tracked separately.

## Verification

- The scripts each carry their own tests in the plugin, on a fixture repository with features, a plan and a
  ledger.
- On the next shop-knowledge batch: whole-suite runs at most one per slice plus one by the branch reviewer; no
  hand-back caused by a missing dependency capability or a rule-decided split; spec agents' replies under a few
  KB each; no one-off plan, feature or ledger edits in the controller's Bash calls.
