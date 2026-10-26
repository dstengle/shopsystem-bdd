# intake of q16

Request: .shop/work/requests/q16.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: intake
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/q16-1-intake
Branch: round/q16-1-intake
Lines of the request:
- 1. **If** a session that `work run` started for a work-item, a capability-proposal, an initiative or a question ends in an error or at its turn limit, or leaves no result `work run` can read, **then** `work run` shall take the session's end as a fault, whatever its result says.
- 2. **When** a session that `work run` started ends with a result that gives questions, `work run` shall send each question where its stage's questions go: a researcher's into the planner's brief, every other stage's under the node's `## Questions`, transitioning the node to `awaiting-answer`.
- 3. **When** a session that `work run` started ends with a result that gives no question and its stage's output, `work run` shall make the node's next transition.
- 4. **When** a session that `work run` started ends with a result that gives neither a question nor its stage's output, `work run` shall write under the node's `## Questions` a question naming the output missing and transition the node to `awaiting-answer`.
- 5. `work run` shall take as a stage's output: a researcher's file set; a planner's plan and file set; an implementer's commits on which the work-item's scenarios and the whole suite pass; a reviewer's findings; an answering session's answer; an integrate or apply round's change list; a formulate round's scenario for each requirement its proposal adds or changes; an intake round's line outcome or question on each line of its request; a gate round's questions.
- 6. `work run` shall make no transition from the outcome a session's result gives.

Read (paths in your worktree):
- .shop/work/requests/q16.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work outcome q16 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work turn q16`.

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/q16-1-intake/.shop/scratch/1-intake
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/q16-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/q16-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
