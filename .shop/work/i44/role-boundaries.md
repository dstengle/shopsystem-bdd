---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i44-role-boundaries
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i44
status: approved
argues: [role-boundaries]
date: 2026-10-28
adds: [role-boundaries#r7]
changes: []
removes: []
---

# role-boundaries

The drafts of this proposal are in .shop/work/i44/runs/i44/1-integrate/drafts/round-1/.

## Questions
- Line to add, role-boundaries#r7: "[r7] The plugin's agent definitions shall give the `bdd-branch-reviewer` no shell tool." (an add; no line changed or removed; quoted from q24 line 1). The `bdd-branch-reviewer` is now defined with Bash, and its description says it "runs the suite, the work-items' checks and the plugin's commands itself"; with no shell tool it can no longer do that. Readings: (a) accept r7 as drafted, the branch review reads only, and `work run` runs the suite, scenarios, checks and commands beforehand and puts their text in the reviewer's brief (as supervise_branch_runs.py already describes) (recommended: it matches the line as asked and the planner's r6); (b) refuse r7 and keep the reviewer's shell tool, so it runs the suite itself; (c) accept r7 and also add a line that the branch review's runs are made by `work run` before the review, so the reviewer's brief holds them. Which reading?

## Answers
- 2026-10-28: Reading (a): accept r7 as drafted; the branch review reads only, and work run makes its runs beforehand and gives their text in the brief, as supervision r154-r155 (i43) already say, so (c)'s added line would repeat r154 (answered by the coordinator under the person's delegation of 2026-10-28).
