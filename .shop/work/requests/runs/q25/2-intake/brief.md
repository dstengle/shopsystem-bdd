# intake of q25

Request: .shop/work/requests/q25.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-1yhjs9gt/q25-2-intake
Branch: round/q25-2-intake
Lines of the request:
- 1. The plugin's commands, `work`, `measure`, `features`, `model`, `tools` and `migrate`, shall give their output as one JSON object on stdout by default.
- 2. **When** a command of the plugin refuses, finds a fault, finds a check failing or has a question for the person, the command shall exit 0 and give what it found and why in its JSON output.
- 3. **If** a command of the plugin crashes on an error it does not handle, then the command shall exit 1.
- 4. The plugin's agents shall return their output as structured JSON.

Read (paths in your worktree):
- .shop/work/requests/q25.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q25 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q25`.

Run directory: /tmp/work-run-requests-1yhjs9gt/q25-2-intake/.shop/scratch/2-intake
Result file: /tmp/work-run-requests-1yhjs9gt/q25-2-intake/.shop/scratch/2-intake/result.json

You start in your worktree, /tmp/work-run-requests-1yhjs9gt/q25-2-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
