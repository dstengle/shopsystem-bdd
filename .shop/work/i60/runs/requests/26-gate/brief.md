# gate of requests

Capability-proposal: .shop/work/i60/requests.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: requests#r72
Changes: none
Removes: requests#r69
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i60/runs/requests/25-integrate/drafts/round-1/
Base: ae85edd3a2ce3488f4d930ac5814845eea5e6178
Worktree: /tmp/work-run-i60-wzn42g_j/requests-26-gate
Branch: round/requests-26-gate
Answers the person gave, each with the question it answers:
- Question: requests#r60 (added): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request." On which branch is the request committed? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." Reading B: r60 stays as drafted.
  Answer: 2026-10-29: Reading A, as the person delegated (2026-10-29: answer every question with its recommended reading): r60 becomes "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: Whose part is the delegation, and may either side run `work delegate` (concerns r59: "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.", and r4)? Reading A: only the asker's side: "**If** a side other than the request's asker runs `work delegate`, **then** `work delegate` shall refuse, naming the side that writes the delegation, and change nothing." (r4 then names `work delegate`.) Reading B: either side, no line.
  Answer: 2026-10-29: Reading B: either side may run work delegate, no line; a delegation is the person handing over decisions, mostly the upstream's gate questions (answered by the person, 2026-10-29)
- Question: Does `work delegate` keep to turns as r16 does (concerns r59)? Reading A: "**If** `work delegate` is run in the other side's turn, **then** `work delegate` shall refuse, because it is the other side's turn, and change nothing." Reading B (recommended, since a delegation comes from the person at any moment): "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is."
  Answer: 2026-10-29: Reading B: When `work delegate` is run, `work` shall write the delegation whichever side's turn it is (the delegation comes from the person at any moment, so it does not keep to turns as r16 does). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: Does `work delegate` change a request's status or turn (concerns r59 and r60)? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn." Reading B: no line.
  Answer: 2026-10-29: Reading A, as the person's delegation directs (2026-10-28 'I take recommendations'; 2026-10-29 answer every question with its recommended reading): 'When `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn.' by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: requests#r62 (added): "**If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing." It names `withdrawn`, a status this spec does not yet name. Reading A (recommended): keep as drafted. Reading B: drop it until it exists: "...`delivered` or `refused`...".
  Answer: 2026-10-29: Reading A, as recommended and under the person's delegation of 2026-10-29: keep r62 as drafted, naming delivered, refused or withdrawn. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: requests#r63 (added): "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Its narrator is a session; requests' narrator is a context taking in or raising a request. Reading A (recommended): stay in requests. Reading B: move to role-boundaries.
  Answer: 2026-10-29: Reading A: r63 stays in requests, as the person's delegation of 2026-10-28/29 says to take the recommended reading. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: Do r16 and r55 reach `work delegate`? Lines concerned: [r70] "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is." (added) and the person's answer that either side may run `work delegate`; r16 ("a command other than `work resolve` ... in the other side's turn ... refuse") and r55 (a side writing the other side's part is refused when the asker is not the upstream itself). Reading A (recommended): the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes. Reading B: r16 and r55 are retired and redrafted with "other than `work resolve` and `work delegate`".
  Answer: 2026-10-29: Reading A: the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes (the person, 2026-10-29: answer every question with its recommended reading). by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- Question: requests#r69: "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Reading 1: the session puts the date into the text it gives `work delegate`, so the request holds the person's words followed by the date. Reading 2: the request holds the person's words alone, word for word, and the date is written beside it, apart from the delegation.
  Answer: 2026-10-29: r69: reading 1, the session puts the date into the text it gives work delegate, as every delegation is written now (The person, <date>: "<words>") (answered by the person, 2026-10-29)

Read (paths in your worktree):
- .shop/work/i60/requests.md
- .shop/work/i60/runs/requests/1-gate
- .shop/work/i60/runs/requests/10-answer
- .shop/work/i60/runs/requests/11-answer
- .shop/work/i60/runs/requests/12-answer
- .shop/work/i60/runs/requests/13-answer
- .shop/work/i60/runs/requests/14-answer
- .shop/work/i60/runs/requests/15-answer
- .shop/work/i60/runs/requests/16-answer
- .shop/work/i60/runs/requests/17-answer
- .shop/work/i60/runs/requests/18-apply
- .shop/work/i60/runs/requests/19-integrate
- .shop/work/i60/runs/requests/2-answer
- .shop/work/i60/runs/requests/20-gate
- .shop/work/i60/runs/requests/21-answer
- .shop/work/i60/runs/requests/22-apply
- .shop/work/i60/runs/requests/23-formulate
- .shop/work/i60/runs/requests/24-formulate
- .shop/work/i60/runs/requests/25-integrate
- .shop/work/i60/runs/requests/3-answer
- .shop/work/i60/runs/requests/4-answer
- .shop/work/i60/runs/requests/5-answer
- .shop/work/i60/runs/requests/6-answer
- .shop/work/i60/runs/requests/7-answer
- .shop/work/i60/runs/requests/8-answer
- .shop/work/i60/runs/requests/9-answer
- .shop/work/i60/runs/requests/25-integrate/drafts/round-1/

Run directory: /tmp/work-run-i60-wzn42g_j/requests-26-gate/.shop/scratch/26-gate
Result file: /tmp/work-run-i60-wzn42g_j/requests-26-gate/.shop/scratch/26-gate/result.json

You start in your worktree, /tmp/work-run-i60-wzn42g_j/requests-26-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
