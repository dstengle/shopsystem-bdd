---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-supervision
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [supervision]
adds: [supervision#r1-r35]
changes: []
removes: []
---

# Supervision: a new capability

What the gate approves: `supervision#r1-r35`, a new capability, as written in `capabilities/supervision.md`.

`work run` is the supervisor the design model names ("workers; a script supervises"). It replaces the controller
session of subagent-driven-development and the plan's execution rules: fresh agents, paths in and results out,
review by risk, fresh fix rounds, further rounds only for the severe, and one session per batch become what a
script does rather than what a controller is asked. Lanes go: implementers with disjoint file sets work at once,
each in its own worktree. What it records (`log.jsonl`, run directories, review-finding records) is what
initiative i12's `measure` reads.

Decisions: design-decision/a-script-supervises-delivery (supersedes design-decision/one-batch-one-session),
design-decision/worker-results-are-files (supersedes design-decision/fresh-agents-short-replies),
design-decision/work-item-lifecycle-as-run (supersedes design-decision/suite-record-holds),
design-decision/review-of-work-items (supersedes design-decision/review-by-risk),
design-decision/the-file-set-is-the-claim (supersedes design-decision/slice-budget-refused-by-plan).

Glossary, added:
- **supervisor**: `work run`, the script that starts the workers and alone writes a work-item's status.
- **worker**: a new `claude -p` session of one agent, started by the supervisor for one stage of one work-item.
