---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-71/review-1
kind: review
batch: batch-71
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/95
head: 04fbfeb99d7f21f58391f8275202edf57df048ba
range: 3a31e267980564e161502a6d4fe824430eb39959..04fbfeb99d7f21f58391f8275202edf57df048ba
result: fix-now
---

# batch-71 review 1

## Verdict

Both items are built. b516 lets an item whose only lines are universal conditions through the readiness bar's lineless gate, and its two scenarios (r53, r54) are generated and bound. b34's agent definition, its step in the skill and its test meet the chore. One finding needs a fix: under b516 the batch also changes `spec check`, which no line asks for. It also re-commits decision 0114 by hand.

## Findings

### f1 Important fix now: spec check now resolves backlog item ids, which no line of the batch asks for
- item: b516
- where: scripts/model_facts.py:276
Commit 1da064f5e cites b516 and adds this rule to `Model.check_refs`: a reference `item/<this context>/b<n>` whose `.shop/backlog/b<n>.md` exists counts as resolved, and no dangling reference is reported.
```
item = re.fullmatch(r"item/%s/(b\d+)" % re.escape(self.path or ""), str(ident))
if item and (self.root / ".shop" / "backlog" / ("%s.md" % item.group(1))).is_file():
    continue        # an item of this context's backlog, kept as .shop/backlog/b<n>.md (b516)
```
This changes what `spec check` reports, so it is behaviour you can see. b516's lines (items#r53, items#r54) are only about `work ready` on an item that holds universal conditions. No line asks for item ids to resolve, and no scenario or script test covers the new rule. The commit message gives the reason: decision 0113's `source: [item/.../b34]` was dangling. That makes it a workaround for a decision's citation, not part of b516.
It also weakens a check: from now on any decision or other artifact can cite a backlog item as its source without a finding. Decision 0114's own context says a decision citing an item "names nothing `spec check` resolves". The comment calling it "(b516)" is wrong too.
Fix: take the change out of b516's branch. If item ids should resolve, raise an item with a line for it (`work idea`). 0113 is superseded, and 0114 already restates it citing quote-42.

### f2 Minor observation: decision 0114 is written by hand on the batch branch, under b516
- item: b516
- where: spec/decisions/0114-the-four-batch-agents.md:1
Commit 0a74c2d7c ("as on main") adds `spec/decisions/0114-the-four-batch-agents.md` and its index row, and sets 0113 to `superseded`, all by hand. CLAUDE.md says a design-decision is written by `work decision`, never by hand. main already holds the same decision from `work decision` (b2ed6ae56). The frontmatter fields I compared match: status, supersedes, source and by. So the merge should add nothing new, unless the bytes differ.
The commit cites b516, which has nothing to do with the batch agents. The total counts changed in tests/scripts/test_decision_checks.py:47 (113 decisions, 59 superseded) follow from this copy. They hold only as long as it is the same file as main's.
Fix if wanted: drop the commit and merge main into the batch branch so the decision comes in from `work decision`'s commit.

### f3 Minor observation: test_agents' docstring still names the superseded decision 0113
- item: b34
- where: tests/scripts/test_agents.py:1
The module docstring says the agents are checked by "design-decision/the-batch-agents, 0113". In this batch, 0113 is superseded by 0114 "the four batch agents", whose `enforced_by` is this test's `RoleBoundaries`. The text is stale, and the file is one of the chore's files. Fix: name the-four-batch-agents, 0114.

### f4 Minor observation: the batch brief still lists the task rules that batch-implementer now carries
- item: -
- where: scripts/batch_driver.py:23
building-a-batch step 4 now says the rules live in `agents/batch-implementer.md` and the task's brief carries only what is its own. `batch_driver.RULES` still writes the same rules into every batch brief: red first, `unbuilt:` handling, the `Item:` trailer, no stash, and the rest. That keeps two copies that can drift apart. The script is outside b34's chore files, so this is not the batch's to fix. Recorded so a later item can make one of them the single source.
