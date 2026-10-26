# research of w201

Work-item: .shop/work/i38/w201.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: 50a40103b15d1b9455b9d609ddb1a96cf799a11d
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w201-1-research
Branch: none (a detached checkout)
Work-item branch: work/w201
Accepted scenarios:
- features/supervision.feature: an implementer whose result gives no question has its branch merged only if the work-item's scenarios and the whole suite pass on it: <case>
- features/supervision.feature: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question
- features/supervision.feature: `work run` prints a question that has no answer yet, and not one that has an answer
- features/supervision.feature: implementers working at the same time have the branches r4 merges merged one at a time, in the order they ended
- features/supervision.feature: a planner's result with a `fileset` writes that file set into the work-item as it makes the transition to planned
- features/supervision.feature: a question goes into the work-item's ## Questions, before a section that follows it
- features/supervision.feature: no worker is started for a work-item that is <status>
- features/supervision.feature: no worker is started for a work-item after its transition to awaiting-answer
- features/supervision.feature: a worker whose session <ending> makes the work-item's transition to failed, recording how the session ended
- features/supervision.feature: the <session> for <node> that <ending> is recorded and printed as a fault of <node>, whatever its result says
- features/supervision.feature: the questions a <who>'s result gives go <where>, and <node> makes its transition from <from> to <to>
- features/supervision.feature: a <who> whose result gives no question and its stage's output makes the work-item's transition from <from> to <next>
- features/supervision.feature: a <who> whose result gives neither a question nor <missing> puts a question naming it under <node>'s ## Questions and makes <node> awaiting-answer
- features/supervision.feature: a <stage>'s result giving <output> is taken as its stage's output
- features/supervision.feature: a researcher whose result gives the outcome BLOCKED with its file set and no question is moved on by its output, not stopped by its outcome
- features/supervision.feature: when an intake round gives a question, the request's status stays as `work turn` set it
- features/supervision.feature: when a session started under a delegation to answer a question <ending>, the question is left unanswered for the person
- features/supervision.feature: when a session started under a delegation to answer a question <ending>, its stage directory and log lines are committed
- features/supervision.feature: when a round `work run` started for a capability-proposal ends at its turn limit, the proposal keeps its status
- features/supervision.feature: the <kind> round of <node> that <ending> brings no transition
- features/supervision.feature: the <kind> round of <node> that <ending> ends `work run` with an error naming the round and how it ended
- features/supervision.feature: when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error

Read (paths in your worktree):
- .shop/work/i38/w201.md
- spec/capabilities/supervision.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w201-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w201-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w201-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
