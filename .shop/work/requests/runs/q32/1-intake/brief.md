# intake of q32

Request: .shop/work/requests/q32.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-j5bm0em1/q32-1-intake
Branch: round/q32-1-intake
Lines of the request:
- 1. **When** the person approves drafted lines at a gate that a session keeps, `work` shall write a capability-proposal for each capability the drafts change, with the requirement ids it adds, changes and removes.
- 2. **When** the drafts that the person approves at a gate a session keeps change the glossary, `work` shall write a glossary-proposal with the terms the drafts add, change and remove.
- 3. **When** `work` writes a proposal from a gate that a session kept, `work` shall write the proposal as `approved` and log each of its moves, naming the gate and the commit that applied its drafts.
- 4. **When** `work` writes the first proposal of a `proposed` initiative from a gate that a session kept, `work` shall move the initiative to `started`.
- 5. **When** a session keeps the gate of an initiative, `integrating-a-proposal` shall hand the approved drafts to `work run` through `work`, writing no proposal file by hand.

Read (paths in your worktree):
- .shop/work/requests/q32.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q32 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q32`.

Run directory: /tmp/work-run-requests-j5bm0em1/q32-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-j5bm0em1/q32-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-j5bm0em1/q32-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
