## Coverage

| id | line | scenario |
|---|---|---|
| r128 | "**If** a session that `work run` started for a work-item, a capability-proposal, an initiative or a question ends in an error or at its turn limit, or leaves no result `work run` can read, **then** `work run` shall take the session's end as a fault, whatever its result says." | Scenario Outline: the <session> for <node> that <ending> is recorded and printed as a fault of <node>, whatever its result says (rows: researcher of w1 at its turn limit; gate round of p1 in an error; apply round of p1 leaving no result; integrate round of i1 at its turn limit; answering session of w1's question in an error) |
| r129 | "**When** a session that `work run` started ends with a result that gives questions, `work run` shall send each question where its stage's questions go: a researcher's into the planner's brief, every other stage's under the node's `## Questions`, transitioning the node to `awaiting-answer`." | Scenario Outline: the questions a <who>'s result gives go <where>, and <node> makes its transition from <from> to <to> (rows: researcher, into the planner's brief, drafted to researched; planner, implementer, reviewer, formulate round, under the node's ## Questions, to awaiting-answer) |

Every other line already has its scenario; nothing was written for them.

## Questions

None. Both lines are formulated under the person's rulings.

## Cases no line mentions

- r128 for a question: the ruling says the fault is "of the node". A question is not a node, so the draft records the fault on the work-item whose question it was (w1). That choice is in the draft and still needs confirming.
- r128 does not say where a fault of a capability-proposal or an initiative is recorded. The `## Faults` section is named only for a work-item (Implementation, may change).
- r129 versus r100: an intake round's question is written in the request (r100), not under a node's `## Questions`, and the request is not transitioned to `awaiting-answer` (r134). r129's "every other stage" does not except it.
- r129 for the integrate round: questions under the initiative's `## Questions` and the initiative transitioning to `awaiting-answer`. It is not clear that an initiative has either.
- r129 for the gate round: r69 already transitions the proposal to `awaiting-answer` on any end. The draft adds no row for it.
- r129 for the apply round: the proposal is already `awaiting-answer` when the round starts, so it is unclear what transition its questions make.
- r129 for an answering session that gives a question in place of an answer: it is unclear where that question goes.
- r129 for the researcher: a researcher whose result gives questions but no file set. r131 would put a "missing output" question under `## Questions`, while r129 sends its questions to the planner.
- r129 for the implementer: a result with questions whose commits fail the tests. It is unclear whether the work-item branch is merged (r4) and whether r131's missing-output question is written as well.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.feature
- /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.reply.md
