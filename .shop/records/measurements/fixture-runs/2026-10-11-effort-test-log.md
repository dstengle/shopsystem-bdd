---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-effort-test-log
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Effort: test log (0.17.0)

The change: `effort: low` in `agents/code-scout.md`, and `measure` recording each dispatch's effort and reasoning
tokens. Scripts: 94 OK, one new test.

## Where output goes

From the transcripts of kb's session that ran batches 32 to 39, every agent at medium effort:

| role | output tokens | of which reasoning |
|---|---|---|
| implementer | 2.00M | 29% |
| task reviewer | 0.98M | 39% |
| branch reviewer | 0.34M | 44% |
| scout | 0.68M | 64% |

## That the setting takes effect

A plugin copy with `effort: low` in the scout's file, one dispatch: every request of the scout is recorded with
effort `low`. Without the line, `medium`.

## The scout at low effort

**Task research on the probe fixture** (`/home/vscode/scratch/shopsystem-bdd/probe/`), Haiku, two scouts a run, three
runs each: 0.16.0 at medium, and this branch at low.

| | medium, 6 dispatches | low, 6 dispatches |
|---|---|---|
| output tokens, mean | 14,237 | 9,358 |
| of which reasoning, mean | 7,829 | 4,160 |
| time, mean | 69 s | 45 s |
| "What the system answers today", with probes marked `run` | 6 of 6 | 6 of 6 |
| a read with a part gives the whole item today | 3 of 3 | 3 of 3 |
| what landing alone produces, listed | 3 of 3 | 3 of 3 |
| defects under their own heading | 6 of 6 | 6 of 6 |
| the checkout clean | 3 of 3 | 3 of 3 |
| lines mentioning a run, both notes | 36 to 45 | 11, 23 and 39 |

Output down 34%, time down 35%. Every part asked for is there. Two of the three low runs set out fewer probes.

**A consequence sweep on kb** (the scratch clone at batch 33's base, the same decision as in the 0.15.0 log),
Haiku, one run each:

| | medium | low |
|---|---|---|
| output tokens | 29,435 | 17,527 |
| of which reasoning | 18,406 | 6,607 |
| time | 154 s | 92 s |
| rows | 42 | 39 |
| reads through the latest version | found | found |
| links restated | found | found |
| export and import | found | found |
| a referred type removed | not found | not found |

Output down 40%, the same three of four.

## Tried and not kept: `Effort: low` on a steps-only task

A line in the task and a rule for the controller to dispatch at it, on the steps fixture
(`/home/vscode/scratch/shopsystem-bdd/stubs/`), an implementer on Sonnet, three runs.

- The controller passed the effort in one run of three.
- It made no difference: the implementer's output was 4,505, 5,136 and 4,585 tokens against 4,433, 5,107 and 5,089
  before, and its reasoning 280 to 310 tokens against 210 to 460. On Sonnet a steps-only task hardly reasons.

kb's steps-only dispatches reasoned for 2.5k to 6.5k tokens each, but those ran on Opus; 0.13.0 already sends such
tasks to Sonnet. The line was taken out.

## Not tested

- The scout at low effort on task research at kb's size, and on Opus, which kb's batch 39 used for its scout.
- Whether fewer probes at low effort lose a defect a medium run would find. The number to watch on a batch:
  hand-backs for an unlisted test, and findings of the kind "what the system already did", beside the scouts'
  output and reasoning in `measure show`.
- Reviewers and implementers at another effort.
