# apply of supervision

Capability-proposal: .shop/work/i51/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Compare each answer below with the drafts you applied, and give each answer they do not hold in your result's `unheld_answers`, a list of the answers' texts, also when you applied some of the drafts; leave out an answer they hold.
Drafts path: .shop/work/i51/runs/i51/1-integrate/drafts/round-1/
Base: 3c43389a5a12ce6f84d8556d2d86945c5fd901aa
Worktree: /tmp/work-run-i51-wv8x5s99/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: Question 1 (r174, r175; replace retired r162, r163): what does "mentions the glossary" mean? r174 (added, replaces r162): **When** a question of an initiative mentions the glossary, `work run` shall leave the question for the person, giving it to no session under a delegation. r175 (added, replaces r163): **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that does not mention the glossary to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise. Retired: r162 (names a term of the glossary or a glossary-proposal), r163 (names neither). Readings: (a) [recommended] The question's text names the glossary itself, which r176 makes every question about a term do; lines stand as drafted. (b) The question is about the glossary: it names the glossary, a term of it or a glossary-proposal. r174 would read: "**When** a question of an initiative names the glossary, a term of the glossary or a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation." and r175 "... that names neither the glossary, a term of the glossary nor a glossary-proposal ..."
  Answer: 2026-10-28: Question 1, mentions the glossary: reading (a), the question's text names the glossary itself; lines as drafted (answered by the person, 2026-10-28)
- Question: Question 2 (r176): who does "a round or a worker" cover? r176 (added): **When** a round or a worker writes a question on the definition of a term or on a proposed term, the round or the worker shall name the glossary in the question. Readings: (a) [recommended] Only rounds and workers `work run` starts (the glossary's worker is a session for one stage of one work-item); as drafted. (b) Also the branch reviewer and answering sessions. r176 would read: "**When** a session that `work run` started writes a question on the definition of a term or on a proposed term, the session shall name the glossary in the question."
  Answer: 2026-10-28: Question 2, r176's sessions: reading (b), every session work run starts, the branch reviewer and answering sessions included (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i51/supervision.md
- .shop/work/i51/runs/supervision/1-gate
- .shop/work/i51/runs/i51/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i51-wv8x5s99/supervision-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i51-wv8x5s99/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i51-wv8x5s99/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
