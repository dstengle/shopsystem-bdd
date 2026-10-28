# gate of requests

Capability-proposal: .shop/work/i45/requests.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: requests#r59
Changes: none
Removes: none
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i45/runs/requests/3-integrate/drafts/round-3/
Base: 10e6a82ef18dc60fb3712e81236e2ea4da33a527
Worktree: /tmp/work-run-i45-7xftq6tl/requests-4-gate
Branch: round/requests-4-gate
Answers the person gave, each with the question it answers:
- Question: Q1 (requests r46): What does `work request` check for "an implementation detail or a term the glossary does not define"? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended, drafted): a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line under `spec/capabilities/` (r46 as above). B (stricter): any word that is not a glossary term: "**If** a line given to `work request` names an implementation detail or uses a word that is not a glossary term, **then** `work request` shall refuse the line, naming the word and why it is refused." (nearly every line refused unless ordinary words are exempt). C: implementation details only: "**If** a line given to `work request` names an implementation detail, **then** `work request` shall refuse the line, naming the word and why it is refused." Recommended: A.
  Answer: 2026-10-28: Q1, r46's check: reading A, a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line (answered by the person, 2026-10-28)
- Question: Q7 (requests r46): Which glossary does `work request` use, since it runs in the asker's repository with no checkout of the upstream's? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended): the upstream's glossary and `spec/capabilities/`: "...a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`..." (replaces r46's wording). B: the glossary and `spec/capabilities/` of the repository it runs in (r46 as drafted). Recommended: A.
  Answer: 2026-10-28: Q7, r46's glossary: reading A, the upstream's glossary and spec/capabilities/ (answered by the person, 2026-10-28)
- Question: Q12 (requests r46): Does "refuse the line" refuse the whole request? Line concerned: [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (added). Readings: A (recommended): yes, as r2: "..., **then** `work request` shall refuse, naming the word and why it is refused, and change nothing." (replaces r46's ending). B: only the line; the other lines are written: r46 as drafted, plus "**When** `work request` refuses a line, `work` shall write the request with its other lines." Recommended: A.
  Answer: 2026-10-28: Q12, r46 refusing a line: reading A, it refuses the whole request and changes nothing, as r2 (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i45/requests.md
- .shop/work/i45/runs/requests/1-gate
- .shop/work/i45/runs/requests/2-apply
- .shop/work/i45/runs/requests/3-integrate
- .shop/work/i45/runs/requests/3-integrate/drafts/round-3/

Run directory: /tmp/work-run-i45-7xftq6tl/requests-4-gate/.shop/scratch/4-gate
Result file: /tmp/work-run-i45-7xftq6tl/requests-4-gate/.shop/scratch/4-gate/result.json

You start in your worktree, /tmp/work-run-i45-7xftq6tl/requests-4-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
