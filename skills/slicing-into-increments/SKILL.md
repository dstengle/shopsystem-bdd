---
name: slicing-into-increments
description: Use when approved Gherkin feature files exist and implementation has not started, when a plan must be made from feature files, or when bdd-red-green has handed a slice back with a HAND-BACK entry in the plan log. Also use when tempted to "resolve" a hand-back by correcting a scenario, when a plan is turning into a design document, or when "set up the project" is about to become a slice.
---

# Slicing Into Increments

## Overview

The plan is an ordered list of thin vertical slices: which scenarios go green next, what someone can observe when they do, what is unknown about building them, and what non-behavioural work rides along. It says nothing about how. This skill owns the plan and is the only place that decides whether the contract has changed. It supersedes superpowers:test-driven-development for deciding what gets built next.

**Violating the letter of these rules is violating the spirit of these rules.**

## What a Slice Is

A slice is a unit of incremental work with an observable done. What makes it done is one of two things:

- **Scenarios** from the approved feature files, for behaviour of the system being built. This is BDD.
- **A check**: a command someone runs and the result it must give, written in the plan. It fails before the slice and passes after. `python -m pytest -q` collects the feature files; `python -c "import kb"` succeeds from the client's checkout; search over a generated corpus of five thousand artifacts returns inside a bound.

Three kinds, keyed to what the slice delivers, never to what its unknown is about:

- **capability**: verified by scenarios. Someone can do one new thing. Every slice cut from a feature file is this, including its refusals and error paths, whatever technology its unknown concerns.
- **enabling**: verified by a check. The environment, packaging, wiring, or tooling the next slices stand on. "The development environment works" is this.
- **stack**: verified by a check. A property of the running system the spec states outside any user scenario: transport, throughput, load time, contention. Cut from the spec's non-functional sentences, and only when the spec states a bound or the skeleton needs it.

Three tests, all required, for every kind:
- **End to end.** Scenarios pass against the system's real entry point with real storage and real side effects behind it; a check runs against the real thing, not a mock. Internals may be hard-coded or stubbed only where nothing in the slice asserts on them.
- **Thin.** One done. A slice with an unknown is usually one scenario or one check, and more than one only when they share step definitions and none is observable without the others. Once the unknowns are spent, scenarios that share a feature and step definitions bundle into one slice.
- **Trimmed.** It contains no work its scenarios or its check don't need.

Not a slice: anything with no scenario and no check. A layer, a module, or a library is not a done; "the module imports" is.

## Process

1. **Run the feature suite** (`python -m pytest -q`, or the project's equivalent) and paste its summary line into the log as `Suite: <N> passed, <M> failed`. Every scenario that passes is credited to the slice whose work made it pass, or to a "Satisfied by existing behaviour" line citing that run. It never appears in a later slice. Reading the step definitions is not a run.
2. **Cut slices** by the three tests. Capability slices come from the feature files. Enabling slices come from what the skeleton stands on: a runnable package, the suite wired up, a dependency installed, a contract file generating code. Stack slices come from the spec's non-functional sentences. Give each slice one unknown: the question building it will settle. A candidate with two unknowns is two slices. A candidate with none bundles with its neighbours in the same feature that share step definitions.
3. **Order slices.** First the enabling slice the skeleton stands on, if any. Then the walking skeleton: the shortest path through every layer that someone can observe. Then by implementation risk, the slice with the largest unknown first, so a surprise arrives while the least code depends on it. Value breaks ties. Dependency is a constraint, not an ordering: a slice may not need another slice's code to pass, so it comes later or the two merge.
4. **Write the plan** in the shape below, in the project's one living plan file. If `docs/superpowers/plans/*-slices.md` exists, extend it; never start a second plan file.
5. **Mark the scenarios.** Write a tag `@slice-<n>` on every scenario a capability slice assigns, one tag per scenario, replacing any earlier slice tag. This is the only edit this skill ever makes to a feature file: a tag line, never a Given, When, or Then. pytest-bdd turns the tag into a marker, so `pytest -m slice<n>` runs a slice.
6. **Invoke superpowers:writing-plans** with the plan file as its input and this constraint: one task per slice, in slice order, no task that isn't a slice. That is where module names, signatures, and fixture layouts belong. Skip this step while any feature awaits approval.

## The Plan File

```
# <topic> slices

## Slice <n>: <name>
- Kind: capability | enabling | stack
- Scenarios: <repo or feature> / <scenario name>; ...      (capability)
- Check: `<command>` -> <the result it must give>            (enabling, stack)
- Observable: <one sentence: what someone can do or see when this is green>
- Unknown: <the one question building this settles> | none
- Needs: <non-behavioural work, needed by which scenario> | none
- Status: planned | in progress | green | blocked: <why>

## Satisfied by existing behaviour
- <feature> / <scenario name>: passed on <date> with no slice

## Log
- <date> Suite: <N> passed, <M> failed
- <date> <one line per checkpoint, hand-back, or re-slice>
```

A slice has Scenarios or Check, never both. The plan names scenarios, checks, observables, unknowns, and what rides along. It contains no module, class, function, fixture, or variable names, no expressions, no diagrams, and no "target design" or "modelling decisions" section. If you have written any of those, you are doing writing-plans' job in the wrong file.

## Re-planning After a Hand-back

Read the HAND-BACK entry. Then do exactly one of these:

| Change needed | Who does it |
|---|---|
| Re-order or split remaining slices | This skill, alone |
| Drop a slice whose unknown is already settled | This skill, alone |
| Change what any Given, When, or Then line says, add a scenario, or remove one | **Not this skill.** Invoke `formulating-features` for that feature. The human approves the result. |

The test for the third row is mechanical: would any Given, When, or Then line differ afterwards, including a number. If yes, it is the third row. This skill never decides what a scenario should have said.

When the third row applies: append a `RE-FORMULATE` entry to the log naming the feature, the scenario, and the hand-back evidence, commit the plan, and invoke `formulating-features`. When it returns, finish cutting and ordering every slice that does not contain that scenario, mark the slice that does `blocked: awaiting approval`, commit, and stop. Do not invoke writing-plans: its tasks would derive from an unapproved contract. writing-plans runs once the human has approved the feature.

## Semantics the Scenarios Don't Cover

The plan does not choose them. "Clamp rather than raise", "keep the first code when the second is rejected", "check unknown before expired" are contract decisions. They go in the log as `QUESTION FOR THE SPEC:` lines, and a slice that cannot be cut without answering one is blocked, not guessed.

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
| "The rest of the plan doesn't depend on that line, so I went on to writing-plans" | Slicing the independent parts is fine. Tasks are not: writing-plans waits for the approval. |
| "It's the safe default, and I noted it in the log" | A default no scenario asserts is a contract decision. Log it as a question, don't plan it. |
| "The implementer will need this design to start" | The implementer gets a task from writing-plans. The slice plan is not that document. |
| "I can see from the step definitions that it passes" | You can see that steps exist. Only a run shows they pass. Run it. |
| "Setting up the transport and the store is one slice" | That's two unknowns. Two slices, each demoable on its own. |
| "The contract is infrastructure, so its slices are stack" | The contract is behaviour a client observes, verified by scenarios. Capability. Stack is only what no scenario covers. |
| "Error handling is a stack concern" | A refusal is part of the capability it refuses. Capability. |
| "This scenario can't go first, it needs the store" | Then it isn't the skeleton. The skeleton is whatever is observable with the least behind it. |

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
- A slice named after a layer or a library with no check
- `Kind: stack` on a slice that has a Scenarios line
- A Kind line that follows the repository instead of the verification

**Any of these: undo it, and take the row of the table that applies.**
