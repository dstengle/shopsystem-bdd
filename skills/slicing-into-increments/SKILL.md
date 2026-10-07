---
name: slicing-into-increments
description: Use when approved Gherkin feature files exist and implementation has not started, when a plan must be made from feature files, or when bdd-red-green has handed a slice back with a HAND-BACK entry in the plan log. Also use when tempted to "resolve" a hand-back by correcting a scenario, when a plan is turning into a design document, or when "set up the project" is about to become a slice.
---

# Slicing Into Increments

## Overview

The plan is an ordered list of thin vertical slices: which scenarios go green next, what someone can observe when they do, what is unknown about building them, and what non-behavioural work rides along. It says nothing about how. This skill owns the plan and is the only place that decides whether the contract has changed. It supersedes superpowers:test-driven-development for deciding what gets built next.

Scripts: this plugin's `scripts/`, at `<this skill's base directory>/../../scripts/`, run with `python3`. `plan` edits and reads the living plan; `features` counts, lists and tags scenarios. Their `--help` is their contract.

**Violating the letter of these rules is violating the spirit of these rules.**

## What a Slice Is

A slice is a unit of incremental work with an observable done. What makes it done is one of two things:

- **Scenarios** from the approved feature files, for behaviour of the system being built. This is BDD.
- **A check**: a command someone runs and the result it must give, written in the plan. It fails before the slice and passes after. `python -m pytest -q` collects the feature files; `python -c "import kb"` succeeds from the client's checkout; search over a generated corpus of five thousand artifacts returns inside a bound.

Three kinds, keyed to what the slice delivers, never to what its unknown is about:

- **capability**: verified by scenarios. Someone can do one new thing. Every slice cut from a feature file is this, including its refusals and error paths, whatever technology its unknown concerns.
- **enabling**: verified by a check. The environment, packaging, wiring, or tooling the next slices stand on. "The development environment works" is this.
- **stack**: verified by a check. A property of the running system the spec states outside any user scenario: transport, throughput, load time, contention. Cut from the bounds among the constraints in `spec/index.md`, and only when a bound is stated or the skeleton needs it.

Three tests, all required, for every kind:
- **End to end.** Scenarios pass against the system's real entry point with real storage and real side effects behind it; a check runs against the real thing, not a mock. Internals may be hard-coded or stubbed only where nothing in the slice asserts on them.
- **Thin.** One done. A slice with an unknown is usually one scenario or one check, and more than one only when they share step definitions and none is observable without the others. Once the unknowns are spent, scenarios that share a feature and step definitions bundle into one slice.
- **Trimmed.** It contains no work its scenarios or its check don't need.

Not a slice: anything with no scenario and no check. A layer, a module, or a library is not a done; "the module imports" is.

## Process

1. **Take the suite's result.** If `plan show --last-suite --current` says `current`, that record is this step's run. Otherwise run the feature suite (`python -m pytest -q`, or the project's equivalent), timed, and record it with `plan log` as bdd-red-green's suite record (its "The Suite Record"). Every scenario that passes is credited to the slice whose work made it pass, or to a "Satisfied by existing behaviour" line citing that run. It never appears in a later slice. Reading the step definitions is not a run.
   **Check the suite is fast.** If the record's time is over 60 s, and either the test command does not run in parallel or the step definitions start the entry point as a program in more than one test per command, and `CLAUDE.md` gives no reason, the batch needs an enabling slice that makes it fast: `Check: the suite -> <N> passed, <M> failed, in under <bound> s`.
2. **Cut slices** by the three tests. Capability slices come from the feature files. Enabling slices come from what the skeleton stands on: a runnable package, the suite wired up, a dependency installed, a contract file generating code. Stack slices come from the bounds in `spec/index.md`. Give each slice one unknown: the question building it will settle. A candidate with two unknowns is two slices. A candidate with none bundles with its neighbours in the same feature that share step definitions.
   **Probe what a dependency provides.** A slice whose Needs names something another project provides gets a probe: a command run now, against the installed version, whose result shows the thing exists (`<command> --help` exits 0; a call returns). Log it, `plan log "Probe: <command> -> <result>"`. A failing probe makes the slice `blocked: awaiting <project>`, with `plan log "REQUEST <project>: <what is needed>"`; no task is written for it. Reading the project's spec is not a probe. Where you read it, read the capability file whole: what is not built is listed under Not yet.
3. **Order slices.** First the enabling slice that makes the suite fast, when step 1 calls for one; then the enabling slice the skeleton stands on, if any. Then the walking skeleton: the shortest path through every layer that someone can observe. Then by implementation risk, the slice with the largest unknown first, so a surprise arrives while the least code depends on it. Value breaks ties. Dependency is a constraint, not an ordering: a slice may not need another slice's code to pass, so it comes later or the two merge. The order of building in `spec/index.md` is such a constraint.
   A scenario added after the plan was cut, from a review, a hand-back, or a
   spec amendment, is placed by its unknown among the remaining slices,
   never ahead of all of them. Only work the next slice needs precedes it.
   A plan is numbered in the order it runs. A slice placed between two
   existing slices takes a dotted number under the one before it (1.1, 1.2
   after 1, before 2), so existing numbers and tags stay valid; order is
   numeric with sub-slices after their parent. Whole numbers are renumbered,
   and tags rewritten, only when whole slices change order.
4. **Write the plan** in the shape below, in the project's one living plan file. If `docs/superpowers/plans/*-slices.md` exists, extend it; never start a second plan file. Every edit goes through `plan` (`add-slice`, `status`, `log`, `backlog`); never `sed`, a heredoc or a one-off script on the plan.
5. **Mark the scenarios.** Write a tag `@slice-<n>` on every scenario a capability slice assigns, one tag per scenario, replacing any earlier slice tag. This is the only edit this skill ever makes to a feature file: a tag line, never a Given, When, or Then. pytest-bdd turns the tag into a marker, so `pytest -m "slice-<n>"` runs a slice. Tag with `features tag "<title>" slice-<n>`; `features count --by-tag` gives each slice's count.
6. **Shape is reviewed at each batch's end**, by the
   `shopsystem-bdd:bdd-branch-reviewer`, which checks the code against the
   project's `CLAUDE.md` and its coupling to the projects it depends on as
   well as the batch's defects. Every refactor it calls for is cut as its own
   enabling slice with a measurable check (the suite green and the structural
   target met), placed by its risk among the next batch's slices. A module
   that has crossed a size limit the project's conventions state is split by
   an enabling slice before the slice that would grow it. The separate
   `architecture-reviewer` runs only when the person asks for one.
7. **Invoke superpowers:writing-plans** with the plan file as its input and the constraint below. Skip this step while a `RE-FORMULATE` entry or a `QUESTION FOR THE SPEC:` a slice depends on is unanswered.

## The Hand-off to writing-plans

The plan carries no code. The planner plans; the implementer writes the code under bdd-red-green. Give writing-plans this constraint, in these words or their equal:

- One task per slice, in slice order, no task that isn't a slice.
- No code blocks, file contents, diffs, or step-definition bodies. writing-plans' own template shows code; here that code is the implementer's to write. Nothing is built in a scratch copy first, and no plan is replayed.
- What each task carries instead: the slice's scenarios or check; why each scenario is red today, found by reading the current code and running the red scenarios (the suite's result from its record; running the red scenarios and probing current behaviour is allowed, building the change is not); where the change lands by the project's conventions (`CLAUDE.md`'s module map) and which of its rules the task implements once; the decisions the capability's Behaviour leaves open, each stated as a decision with the line or ledger entry it rests on, so the implementer does not decide them alone; the existing step definitions and fixtures the scenarios can reuse, by name; the verification commands, with expected counts derived from the tags (`features count --by-tag`), never from a build; and the checkpoint the implementer logs.
- Each task carries a `Review:` line and a `Model:` line. `Review: per-task` and `Model: opus` for a task that touches concurrency, the published contract, data integrity, or moving stored data; `Review: batch-end` and `Model: sonnet` for every other task, refactors and small slices included. A batch-end task gets no task review: the batch's branch review covers it. Say this in the plan's Global Constraints so the controller dispatches by it.
- Each task names its markers and expected counts. When to run what is bdd-red-green's and the agents': a plan that says when to run the suite, or to record a failing list, is wrong.
- The plan's Global Constraints carry `Scripts: <absolute path of this plugin's scripts/>`, so every task brief carries it.
- A genuine unknown may be answered by a throwaway spike whose result is a sentence in the plan, never its code.
- Questions for the spec found while probing go in the plan's Review Focus with a reproduction.
- Paths in commands are relative to the checkout, never absolute temporary paths.

When writing-plans asks how to execute, recommend a new session that reads the plan file. This session holds integration, formulation and slicing, which no task needs and every later turn would re-read.

A plan that carries code makes red a performance: the implementer pastes what already went green elsewhere, the reviewer checks a diff against a plan instead of code against a scenario, and hand-backs stop happening because the plan pre-authorised every stop condition. A plan that carries intent keeps the red run an observation.

## The Plan File

```
# <topic> slices

## Slice <n>: <name>            (<n> is 2, or 1.3 for a slice placed after 1)
- Kind: capability | enabling | stack
- Scenarios: <repo or feature> / <scenario name>; ...      (capability)
- Check: `<command>` -> <the result it must give>            (enabling, stack)
- Observable: <one sentence: what someone can do or see when this is green>
- Unknown: <the one question building this settles> | none
- Needs: <non-behavioural work, needed by which scenario> | none
- Status: planned | in progress | green | blocked: <why>

## Satisfied by existing behaviour
- <feature> / <scenario name>: passed on <date> with no slice

## Backlog
- <date> <hardening finding, one line, with its reproduction> (from <review>)

## Log
- <date> Suite: <N> passed, <M> failed at <short hash> in <seconds> s[; failing: <titles>]
- <date> Probe: <command> -> <result>
- <date> REQUEST <project>: <what is needed>
- <date> <one line per checkpoint, hand-back, or re-slice>
```

The living plan holds the slices not yet green, the backlog, and the log since the last batch closed. When a batch's branch review is done, run `plan archive <batch>`, which moves the green slices and the log (requests stay) to `docs/superpowers/plans/archive/<plan name>-<batch>.md` and leaves one log line naming the file and the batch's last `Suite:` line, so every agent that reads the plan reads only what is still open.

A slice has Scenarios or Check, never both. The plan names scenarios, checks, observables, unknowns, and what rides along. It contains no module, class, function, fixture, or variable names, no expressions, no diagrams, and no "target design" or "modelling decisions" section. If you have written any of those, you are doing writing-plans' job in the wrong file.

## Re-planning After a Hand-back

Read the HAND-BACK entry. Then do exactly one of these:

| Change needed | Who does it |
|---|---|
| Re-order or split remaining slices | This skill, alone |
| Drop a slice whose unknown is already settled | This skill, alone |
| Change what any Given, When, or Then line says, add a scenario, or remove one | **Not this skill.** Invoke `formulating-features` for that feature. A question it returns goes to the person and then to `integrating-a-proposal`. |

The test for the third row is mechanical: would any Given, When, or Then line differ afterwards, including a number. If yes, it is the third row. This skill never decides what a scenario should have said.

When the third row applies: append a `RE-FORMULATE` entry to the log naming the feature, the scenario, and the hand-back evidence, commit the plan, and invoke `formulating-features`. When it returns a rewritten scenario, the line decided it: slicing resumes with that scenario in its slice. When it returns a question, finish cutting and ordering every slice that does not contain that scenario, mark the slice that does `blocked: awaiting the spec`, commit, and stop. Do not invoke writing-plans: its tasks would derive from an undecided contract. writing-plans runs once the line is changed and the scenario re-formulated from it.

A scenario removed because its capability line was removed is logged; its step definitions and code are left for the batch's branch review to flag.

## Review Findings

A review's finding is triaged before anything is cut from it:

- **Correctness or data loss** (a refusal answered as a crash, a wrong answer, a write that should not land, a regression): fixed now, in the batch's one fix wave or as a slice of the next batch, through the small-change path when it needs a line.
- **Hardening** (an input no client sends today, an edge case no line names, robustness against a dependency changing): one line in the plan's `## Backlog` with its reproduction. It is cut as a slice only when the person asks for it or when it bites.

Polish (wording, naming, a test that could be stronger) is fixed in the fix wave when it is cheap, and otherwise dropped.

## Semantics the Scenarios Don't Cover

The plan does not choose them. "Clamp rather than raise", "keep the first code when the second is rejected", "check unknown before expired" are contract decisions. They go in the log as `QUESTION FOR THE SPEC:` lines, then to the person and, with their answer, to `integrating-a-proposal`, so the answer lands in a capability line or the ledger. A slice that cannot be cut without answering one is blocked, not guessed.

## Rationalizations That Do Not Hold

| Excuse | Reality |
|---|---|
| "It's a formulation typo, not a pricing rule" | You are looking at the number the human approved. Whether it's a typo is theirs to say. Re-formulate. |
| "Slice 1 already establishes 2 × 9.99 = 19.98" | Then the two scenarios contradict each other, and the contract needs a decision. Not yours. |
| "Nothing in the feature or README describes a surcharge" | Absence of a rule in the docs you can see isn't evidence about the rule. |
| "It's the only .feature change" | One changed Then line is a changed contract. The approval on that file is void. A tag line is the only edit you make. |
| "I verified the scenario passes with the corrected line" | Passing against a line you wrote proves nothing about the line they wrote. |
| "The hand-back said slicing or formulating decides" | Slicing decides which row of the table applies. Formulating decides what the line says. |
| "They're away for an hour, so I made the call" | Re-formulate and stop. The plan waits; the contract doesn't get edited to save an hour. |
| "The rest of the plan doesn't depend on that line, so I went on to writing-plans" | Slicing the independent parts is fine. Tasks for a scenario awaiting its line are not: writing-plans waits for the changed line. |
| "writing-plans' template has code in every step, so the plan should too" | The template shows a shape, not this workflow's division of labour. The code is the implementer's; a plan with code makes red performed rather than observed. Hand off with the constraint above. |
| "I'll build it in a scratch copy first so the plan's counts are right" | Counts come from the tags. A scratch build is the implementation done on the wrong model by the wrong role, and its code leaks into the plan. |
| "It's the safe default, and I noted it in the log" | A default no scenario asserts is a contract decision. Log it as a question, don't plan it. |
| "The implementer will need this design to start" | The implementer gets a task from writing-plans. The slice plan is not that document. |
| "I can see from the step definitions that it passes" | You can see that steps exist. Only a run shows they pass. Run it. |
| "Setting up the transport and the store is one slice" | That's two unknowns. Two slices, each demoable on its own. |
| "The contract is infrastructure, so its slices are stack" | The contract is behaviour a client observes, verified by scenarios. Capability. Stack is only what no scenario covers. |
| "Error handling is a stack concern" | A refusal is part of the capability it refuses. Capability. |
| "This scenario can't go first, it needs the store" | Then it isn't the skeleton. The skeleton is whatever is observable with the least behind it. |
| "It came from a review, so it goes before everything" | A review finding is a scenario like any other. Place it by its unknown; the plan's head stays the plan's head. |
| "Only the plan changed since the record, but a fresh run is safer" | The record holds while nothing outside `docs/superpowers/plans/` changed; `plan show --last-suite --current` says so. It is the run. |
| "The suite is slow but it works" | Every run in the batch pays for it. Over 60 s and serial, it is the batch's first slice. |
| "The dependency's spec describes the command, so it is there" | A spec says what is meant; its Not yet says what is not built; only a probe at the installed version says what is there. Probe it. |
| "The tasks are written now; execution waits for the dependency" | A task for a blocked slice plans on a command that does not exist. Log the `REQUEST`; write tasks for the slices that can run. |
| "Subagent-driven execution can run from here" | Every turn here re-reads integration, formulation and slicing. A new session reads the plan file and nothing else. |

## Red Flags

- Any diff under `features/` other than `@slice-<n>` tag lines
- The words "typo", "obviously", "RESOLVED" in a log entry about a scenario
- A section titled "Target design", "Modelling decisions", "Dependency graph", or "Definition of done" in the slice plan
- A method signature, a `quantize(...)`, a fixture name, or a file path under `src/` or `tests/` in the slice plan
- A second `*-slices.md` file
- "Safe default" for a case no scenario covers
- "passed" or "already green" in the plan with no `Suite:` line from a real run in the log
- A slice whose Unknown line has an "and" in it
- A run of one-scenario slices with `Unknown: none` from the same feature
- A batch of new slices inserted ahead of the whole remaining plan
- Slice numbers that do not read in execution order, dotted sub-slices counted after their parent
- A slice named after a layer or a library with no check
- `Kind: stack` on a slice that has a Scenarios line
- A Kind line that follows the repository instead of the verification
- A slice planned on a dependency's command with no `Probe:` line
- A dependency's capability read by a section range
- A task written for a `blocked` slice
- `sed`, a heredoc or `python -c` on the slice plan or on a tag line
- A plan task that says when to run the whole suite

**Any of these: undo it, and take the row of the table that applies.**
