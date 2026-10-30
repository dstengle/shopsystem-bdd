# answer

Agent: delegation-answerer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: none
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-answer
Branch: none (a detached checkout)
Question: Q2 (r64, r65 against docs/capability-format.md): the format document still says "A changed line keeps its id" until r64 is delivered. Lines: added [r64] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id.; added [r65] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id.; removed [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id. A (recommended): no further line; r64's work-item changes the format. B: a Not yet entry: "Rounds follow r65 over `docs/capability-format.md`'s Requirement ids — trigger: r64 delivered."
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
- docs/capability-format.md
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-answer/.shop/scratch/6-answer
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-answer/.shop/scratch/6-answer/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-6-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
