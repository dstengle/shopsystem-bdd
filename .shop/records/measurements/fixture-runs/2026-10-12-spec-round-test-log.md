---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-12-spec-round-test-log
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-12
---

# A controller for each spec round: test log (0.18.0)

From: `/home/vscode/shopsystem-knowledge/docs/superpowers/reports/2026-10-12-batch19-analysis.md`, its third
candidate. Scripts: 94 OK.

## What the report's number is made of

The session `cf311c41` in shopsystem-knowledge, read from its transcript:

| phase | controller requests | cache read | context |
|---|---|---|---|
| the brainstorm | 77 | 9.2M | 48k to 180k |
| integration, three rounds | 22 | 4.5M | 181k to 226k |
| formulation, three rounds, 17 formulators | 53 | 15.5M | 228k to 344k |
| after a compaction | 13 | 0.9M | 68k to 76k |

- Integration and formulation ran in the session that had brainstormed the note, so every turn of theirs began at
  181k or more.
- A writer or formulator that finishes wakes the controller for a turn. Seventeen formulators and five writer
  rounds are most of the 75 turns.
- The agents' replies were small (6k tokens for all 22). What grew the context was the controller's own reading of
  drafts (35k), the notifications and the person's answers (40k), and its messages (30k).

## That an agent can dispatch another

A plugin agent given the Agent tool dispatched a `code-scout` and relayed its reply; the scout's transcript is
recorded at depth 2, in the same session's directory, where `measure` reads it.

## Before and after

Fixture `/home/vscode/scratch/shopsystem-bdd/round/` (`make_spec.py`, `run.sh`, `score.py`): a `shelf` spec with
one capability, formulated and passing, and an approved note about lending. Two cases.

- **Integration to the gate.** The note is to be integrated; the run stops at the gate.
- **Formulation.** The note's lines and four more new capabilities are approved and committed in `spec/`, six
  capabilities to formulate, one of them a changed line whose scenario passes today.

The controller (Sonnet) first reads six files of about 40k tokens each, standing for the brainstorm it would be
holding, and so works at about 270k. Cache read is for the whole run, controller and agents.

| | 0.17.0 | 0.18.0 |
|---|---|---|
| integration: cache read | 1.57M, 1.57M | 0.32M, 0.90M, 1.20M |
| integration: controller requests | 8, 8 | 3, 5, 6 |
| integration: output tokens | 11.7k, 10.8k | 15.0k, 17.0k, 19.0k |
| formulation: cache read | 4.94M, 5.77M | 2.08M, 1.40M, 1.80M |
| formulation: controller requests | 19, 22 | 8, 5, 7 |
| formulation: output tokens | 26.4k, 28.4k | 32.5k, 34.0k, 33.2k |

Means: integration 1.57M to 0.81M, formulation 5.36M to 1.76M. Output rises by about 6k tokens a round, the
round's own writing.

Every formulation run ended the same way on both versions: the feature files committed, the old count scenario
held and rebound, `features bindings` clean, the suite `3 passed`. The lend-items feature has 3 to 6 scenarios
across the runs, on both versions, by how many of its lines a formulator returned as questions.

In the 0.18.0 runs the controller's turns after its reading were: load the skill, dispatch the round, one turn
when it finished, and its message to the person, with a `git show` before the dispatch in some. The six
formulators are recorded at depth 2 under the round.

## What the first try showed

The first version of `spec-round` dispatched its six formulators and, in two runs of two, ended its turn while they
ran. Their completions then went to the controller, which took a turn for each ("Two more formulators reported"),
and resumed the round to finish. Formulation still fell, to 2.4M and 2.9M, but by less. (Those two runs and their
two baselines, 3.5M and 3.9M, stopped at the first question with nothing written, as their prompt asked; the table
above is from the runs after, whose prompt let the work finish.)

The agents run in the background and their finishing is not certain to wake a nested agent. So each brief now
names a reply file, which the writer or formulator writes last, and `spec-round` waits in one shell command until
every reply file exists. In the five runs since, no formulator reported to the controller.

## In a session that holds little

Without the six files, on the note's two capabilities, the controller on 0.17.0 took 5 to 11 requests and the
whole run read 0.16M to 0.45M. A round adds its own context, about 0.1M to 0.4M read and 6k output, so there it
saves nothing. The rule is not made conditional: a session cannot be relied on to know its own size, and the cost
where it is not needed is small beside the cost where it is.

## Not tested

- **A second round with the person's answers, and `apply`.** The runs stop at the gate, or start after it. No run
  carried an answer into round 2, and no run applied approved drafts through the round.
- **A formulation question going back to integration** and returning as a formulation round for one capability.
- **The recommendation to start a new session** when the note was brainstormed in this one.
- **A `BLOCKED` round**: an agent that never writes its reply file.
- **Opus as the controller**, which the real sessions used. The turns counted are the same; the tokens a turn are
  the model's.
