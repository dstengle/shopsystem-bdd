# gate of supervision

Capability-proposal: .shop/work/i51/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r209, supervision#r210
Changes: none
Removes: supervision#r162, supervision#r163
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i51/runs/supervision/6-integrate/drafts/round-6/
Base: 3c43389a5a12ce6f84d8556d2d86945c5fd901aa
Worktree: /tmp/work-run-i51-66fnayzb/supervision-7-gate
Branch: round/supervision-7-gate
Answers the person gave, each with the question it answers:
- Question: Question 1 (r174, r175; replace retired r162, r163): what does "mentions the glossary" mean? r174 (added, replaces r162): **When** a question of an initiative mentions the glossary, `work run` shall leave the question for the person, giving it to no session under a delegation. r175 (added, replaces r163): **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that does not mention the glossary to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise. Retired: r162 (names a term of the glossary or a glossary-proposal), r163 (names neither). Readings: (a) [recommended] The question's text names the glossary itself, which r176 makes every question about a term do; lines stand as drafted. (b) The question is about the glossary: it names the glossary, a term of it or a glossary-proposal. r174 would read: "**When** a question of an initiative names the glossary, a term of the glossary or a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation." and r175 "... that names neither the glossary, a term of the glossary nor a glossary-proposal ..."
  Answer: 2026-10-28: Question 1, mentions the glossary: reading (a), the question's text names the glossary itself; lines as drafted (answered by the person, 2026-10-28)
- Question: Question 2 (r176): who does "a round or a worker" cover? r176 (added): **When** a round or a worker writes a question on the definition of a term or on a proposed term, the round or the worker shall name the glossary in the question. Readings: (a) [recommended] Only rounds and workers `work run` starts (the glossary's worker is a session for one stage of one work-item); as drafted. (b) Also the branch reviewer and answering sessions. r176 would read: "**When** a session that `work run` started writes a question on the definition of a term or on a proposed term, the session shall name the glossary in the question."
  Answer: 2026-10-28: Question 2, r176's sessions: reading (b), every session work run starts, the branch reviewer and answering sessions included (answered by the person, 2026-10-28)
- Question: Are the lines of supervision approved as drafted? Readings: approve supervision as drafted (recommended), or change its lines.
  Answer: 2026-10-29: Change its lines: the person replaces the 'mentions the glossary' rule with a check triggered by a change to the glossary. A question of a glossary-proposal, or a question one of whose readings adds, changes or removes a term/<term>, is left for the person and given to no session under a delegation; every other question of the initiative is given to a session under the delegation, whatever words it uses. r174 and r175 are redrafted to say so, and r176 (a question on a term names the glossary) is dropped, since the check no longer reads the question's words. No word of the question is matched against the glossary's terms. (answered by the person, 2026-10-29)

Read (paths in your worktree):
- .shop/work/i51/supervision.md
- .shop/work/i51/runs/supervision/1-gate
- .shop/work/i51/runs/supervision/2-apply
- .shop/work/i51/runs/supervision/3-integrate
- .shop/work/i51/runs/supervision/4-gate
- .shop/work/i51/runs/supervision/5-apply
- .shop/work/i51/runs/supervision/6-integrate
- .shop/work/i51/runs/supervision/6-integrate/drafts/round-6/

Run directory: /tmp/work-run-i51-66fnayzb/supervision-7-gate/.shop/scratch/7-gate
Result file: /tmp/work-run-i51-66fnayzb/supervision-7-gate/.shop/scratch/7-gate/result.json

You start in your worktree, /tmp/work-run-i51-66fnayzb/supervision-7-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
