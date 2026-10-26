# formulate of requests

Capability-proposal: .shop/work/i37/requests.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: formulate
Base: 94be81b4c7efa16e4b751858da00db485be242d1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-3-formulate
Branch: round/requests-3-formulate
Answers the person gave, each with the question it answers:
- Question: Decision: narrow r7 (adds r23, r24 are drafted with it). Lines: r23 (added) "**When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's." r24 (added) "**When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker." r7 (changed) "**When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side." Was: "**When** `work turn <request>` is run, `work` shall pass the request's turn to the other side." Readings: (a) narrow r7 as drafted (recommended: r7 and r23 otherwise contradict for an upstream that accepts); (b) leave r7 unchanged, with r23 and r7 contradicting.
  Answer: 2026-10-26: (a) narrow r7 as drafted (q15 delegation: the recommended reading; the person, 2026-10-26: "yes, answer both").
- Question: Decision: the glossary entry term/turn. Reading (a, recommended): change the entry to "- **turn**: the side of a request, its asker or its upstream, whose part of the request is to be written next, passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered." (the old definition disagrees with r23, r24). Reading (b): leave the entry as it is.
  Answer: 2026-10-26: (a) change the glossary entry of turn as drafted (q15 delegation: the recommended reading; the person, 2026-10-26: "yes, answer both").
- Question: Decision: the Not yet entry "The detail of turns, which the person reserved". Readings: (a, recommended) keep it, since this note settles two transitions (r23, r24), not the detail; (b) remove the entry, if this note is taken to give that detail.
  Answer: 2026-10-26: (a) keep the Not yet entry (q15 delegation: the recommended reading; the person, 2026-10-26: "yes, answer both").
- Question: Decision: a line for an already `accepted` request in the asker's turn (q15 itself). Not in the note. Reading (a, recommended): no line. Reading (b): add "**While** a request is `accepted` and its turn is the asker's, **when** `work turn <request>` is run, `work` shall pass the request's turn to its upstream."
  Answer: 2026-10-26: (a) no line (q15 delegation: the recommended reading; the person, 2026-10-26: "yes, answer both").
- Question: Decision: r10's scope of turn (r10 is not changed by the draft; this asks whether to change it). Reading (a, recommended): keep "whichever side's turn it is" (the r10 scenario's given is an accepted request in the asker's turn; narrowing would break it). Reading (b): narrow to "**When** `work resolve <request>` is run in the upstream's turn on an `accepted` request with each accepted line's requirement id and the version that holds it, `work` shall write them as the request's resolution."
  Answer: 2026-10-26: (a) keep r10's whichever side's turn it is (q15 delegation: the recommended reading; the person, 2026-10-26: "yes, answer both").

Read (paths in your worktree):
- .shop/work/i37/requests.md
- .shop/work/i37/runs/requests/1-gate
- .shop/work/i37/runs/requests/2-apply

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-3-formulate/.shop/scratch/3-formulate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/requests-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
