---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-roadmap
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# The workflow simplified: the plans, in order

`design.md` in this folder covers several subsystems that can each be built and tested on their own, so it is built as
nine plans. Each plan is written when the plan before it has merged, against the code as it then stands. Only plan 1
is written now (`plan-1-spec.md`).

The design decides that the new workflow is itself codified (§ "Decided by the person after the builder check"), so
plan 1 writes the requirements of every later plan. Each later plan builds the requirements its capability already
has, and removes them from that capability's `unbuilt:` list as their scenarios pass. A later plan that finds a
requirement wrong retires it and adds a new one. It never edits a line.

| # | plan | builds (design goal) | capability of plan 1 | depends on |
|---|---|---|---|---|
| 1 | The new workflow codified | the lexicon, every capability's lines, the `unbuilt:` mark | all | gf-conversion merged |
| 2 | Items and the backlog | goals 1, 2, 10: item files, states, WSJF rank, dependencies, `work backlog`, names next to ids | `backlog` | 1 |
| 3 | Readiness and intake | goals 3, 4: `work ready`, the brainstorming skill writing lines, negotiation on `work request`/`work outcome` | `readiness`, `intake` | 2 |
| 4 | Batches | goal 5: `work batch` (pick, plan on disk, tasks in worktrees, park, resume, the PR) | `batches` | 3 |
| 5 | Review at the PR | goal 6: the `pr-reviewer` agent, the batch's range, the fix loop, findings recorded | `pr-review`, `brainstorming` | 4 |
| 6 | Decisions in tiers | goal 7: the `tier` field, `model decisions --check`, the 72 sorted | `decision-tiers` | 1 |
| 7 | Telemetry | goal 8: `measure batch`, defects traced to items | `telemetry` | 4 |
| 8 | Conversation and names | goals 9, 10: quotes with their turns, the SessionStart names table | `conversation` | 2 |
| 9 | Retirement and the 2.0 step | the old capabilities' lines retired, the old modules and agents deleted, `.shop/work/` frozen, `migrate upgrade` 2.0.0 | all old | 2-8 |

- **Parallel plans:** 6 and 8 can run beside 3-5.
- **The first usable point:** plans 2-5 give a working loop (backlog → ready → batch → PR). From then on the plugin can
  build its own later plans through it, instead of through the old `work run`.
