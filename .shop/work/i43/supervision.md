---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i43-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i43
status: formulated
argues: [supervision]
date: 2026-10-28
adds: [supervision#r154, supervision#r155, supervision#r156, supervision#r157]
changes: []
removes: []
---

# supervision

The drafts of this proposal are in .shop/work/i43/runs/i43/1-integrate/drafts/round-1/.

## Questions
- supervision#r155: "**When** `work run` starts a branch review, `work run` shall give the branch reviewer each run r154 names with its command, how it exited and its output, naming the commit they ran at." How should a run's exit be worded? Reading A (recommended, drafted): keep "how it exited" and add the Implementation line "r155: how a run exited is given as its exit code." Reading B: put it in the line: "each run r154 names with its command, exit code and output, naming the commit they ran at."
- supervision#r156 'each with the work-item it belongs to or none'. Reading 1: a commit belongs to the work-item whose work or status it commits (implementer commits, merge of its branch, work run's transition commits). Reading 2: only commits made on the work-item's branch belong to it; transition commits and merges on the initiative branch belong to none.

## Answers
- 2026-10-28: supervision#r155: Reading A, keep 'how it exited' and add the Implementation line 'r155: how a run exited is given as its exit code.' (answered by the coordinator under the person's delegation of 2026-10-28).
- 2026-10-28: supervision#r156: Reading 1, a commit belongs to the work-item whose work or status it commits (implementer commits, merge of its branch, work run's transition commits), so that 'none' holds only commits no work-item made, which the branch reviewer reports (answered by the coordinator under the person's delegation of 2026-10-28; no reading was recommended).
