---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/workflow-scenarios-run-as-fixture-sessions
summary: "A workflow capability's scenarios run as headless claude -p sessions of the plugin against a fixture repository, several runs each, and judge the behaviour by what the runs left; none is grouped as guarantees to spare the cost."
date: 2026-10-16
status: accepted
revisit_when: "a scenario's runs disagree often enough that its verdict changes from one suite run to the next"
revisit_signal: requests
source: [initiative/i1]
by: "question 1; the person, 2026-10-16; records/measurements/fixture-runs/"
---

# 0030. Workflow scenarios run as fixture sessions

## Decision

The capabilities that describe what an agent does under a skill (spec-integration, formulation, spec-migration, slicing, code-research, red-green, review, batch-analysis) get Gherkin scenarios like the script capabilities. A scenario's Given builds a fixture repository, its When runs the skill or agent headless with `claude -p --plugin-dir` on that fixture, and its Then checks what the session left: files, git state, the transcript. Each scenario runs several times, because one run of an agent proves little, and a change to the plugin's workflow is judged by those runs before it is made, as the fixture-run test logs have done by hand since 0.1.0.

## Context

The plugin's skills and agents run in every consuming repository, so a wrong rule costs there, many times over. The alternative was cheaper: group these capabilities as guarantees and check them with `measure` on real batches, which finds a fault only after a batch has paid for it.

## Alternatives

Group them as guarantees, checked by `measure` against a bound; a mix, with scenarios only where a script can check a session's output cheaply.

## Consequences

The fixture generators and run harness, kept until now outside the repository, move into it so a scenario can be rerun. These scenarios cost model usage on every run, so they run apart from `python3 -m unittest discover -s tests/scripts`. How many runs a scenario takes, and how many must pass, is still open (i1).
