# integrate of i38

Initiative: .shop/work/i38/initiative.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: integrate
Request: q16
Accepted lines of the request:
- 1. **If** a session that `work run` started for a work-item, a capability-proposal, an initiative or a question ends in an error or at its turn limit, or leaves no result `work run` can read, **then** `work run` shall take the session's end as a fault, whatever its result says.
- 2. **When** a session that `work run` started ends with a result that gives questions, `work run` shall send each question where its stage's questions go: a researcher's into the planner's brief, every other stage's under the node's `## Questions`, transitioning the node to `awaiting-answer`.
- 3. **When** a session that `work run` started ends with a result that gives no question and its stage's output, `work run` shall make the node's next transition.
- 4. **When** a session that `work run` started ends with a result that gives neither a question nor its stage's output, `work run` shall write under the node's `## Questions` a question naming the output missing and transition the node to `awaiting-answer`.
- 5. `work run` shall take as a stage's output: a researcher's file set; a planner's plan and file set; an implementer's commits on which the work-item's scenarios and the whole suite pass; a reviewer's findings; an answering session's answer; an integrate or apply round's change list; a formulate round's scenario for each requirement its proposal adds or changes; an intake round's line outcome or question on each line of its request; a gate round's questions.
- 6. `work run` shall make no transition from the outcome a session's result gives.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99, supervision#r125, supervision#r126, supervision#r127
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/i38-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 50a40103b15d1b9455b9d609ddb1a96cf799a11d
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/i38-1-integrate
Branch: round/i38-1-integrate

Read (paths in your worktree):
- .shop/work/i38/initiative.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/i38-1-integrate/.shop/scratch/1-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/i38-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/i38-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
