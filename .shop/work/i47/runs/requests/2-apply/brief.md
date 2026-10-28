# apply of requests

Capability-proposal: .shop/work/i47/requests.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Compare each answer below with the drafts you applied, and give each answer they do not hold in your result's `unheld_answers`, a list of the answers' texts, also when you applied some of the drafts; leave out an answer they hold.
Drafts path: .shop/work/i47/runs/i47/1-integrate/drafts/round-1/
Base: edcfb0c266fb1d7417f5244a620bf7053adf08f7
Worktree: /tmp/work-run-i47-ee1m2t30/requests-2-apply
Branch: round/requests-2-apply
Answers the person gave, each with the question it answers:
- Question: requests, r48 against r18: line 3 of q33 says 'passes a request's turn' without saying which side. When the asker passes the turn to the upstream with every line withdrawn, r18 sets awaiting-upstream and r48 sets withdrawn. Lines: [r47] When the upstream ends its turn on a request that is not delivered whose every line has the line outcome refused or withdrawn and at least one line refused, work shall set the request's status to refused (replaces r9, retired). [r48] When work turn passes a request's turn with every line's line outcome withdrawn, work shall set the request's status to withdrawn. Reading A (recommended): r48 holds for either side; change r18 to '[r18] When work turn passes a request's turn to its upstream with a line whose line outcome is not withdrawn, work shall set the request's status to awaiting-upstream.' and keep r48 as drafted. Reading B: r48 holds only for the upstream's turn: '[r48] When work turn passes a request's turn to its asker with every line's line outcome withdrawn, work shall set the request's status to withdrawn.' and r18 stays.
  Answer: 2026-10-28: Q1, r48 against r18: reading A, r48 holds for either side and r18 changes to name a line whose outcome is not withdrawn (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: requests, r48 and delivered: r9 and r47 apply only to a request that is not delivered; line 3 does not say whether r48 does. Line: [r48] When work turn passes a request's turn with every line's line outcome withdrawn, work shall set the request's status to withdrawn. Reading A (recommended): yes: '[r48] When work turn passes the turn of a request that is not delivered with every line's line outcome withdrawn, work shall set the request's status to withdrawn.' Reading B: no: r48 as drafted.
  Answer: 2026-10-28: Q2, r48 and delivered: reading A, r48 holds only for a request that is not delivered (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: requests, r48 and the turn: r7 still passes the turn of a request r48 sets withdrawn to the other side; line 3 does not say where the turn goes. Line: [r48] as above. Reading A: the turn stays with the side that ran work turn: add '[r49] When work sets a request's status to withdrawn, work shall keep the request's turn with the side that ran work turn.', and r7 gets the same exception it makes for accepted. Reading B (recommended): nothing changes.
  Answer: 2026-10-28: Q3, r48 and the turn: reading B, nothing changes (answered by the coordinator under the person's delegation, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i47/requests.md
- .shop/work/i47/runs/requests/1-gate
- .shop/work/i47/runs/i47/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i47-ee1m2t30/requests-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i47-ee1m2t30/requests-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i47-ee1m2t30/requests-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
