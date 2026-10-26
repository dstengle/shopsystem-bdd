# intake of q14

Request: .shop/work/requests/q14.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: intake
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/q14-1-intake
Branch: round/q14-1-intake
Lines of the request:
- 1. The request tool shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle, whatever carries the request.
- 2. The request tool shall keep the carrier of a request behind one port, with a file in the upstream's repository and an issue on the upstream's GitHub repository as its first two carriers.
- 3. **When** the same request is carried by either carrier, the request tool shall give each side the same commands, the same refusals and the same states.
- 4. **When** an asker raises a request, answers a question or passes the turn, the request tool shall do it from the asker's own repository, with no checkout of the upstream's repository.
- 5. **Where** `--raised-for <request>` is given when a request is raised, the request tool shall write in the upstream's request the request it is raised for.
- 6. **If** a request whose asker is not the upstream itself is raised with `--source`, then the request tool shall refuse, because an origin belongs to an internal request, and change nothing.
- 7. **If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, then the request tool shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing.
- 8. **When** `model check` reads a request whose `part_of` names a job-thread kept in another repository, `model check` shall print no `v17` for the request.
- 9. **When** `model check` reads a request raised for a request of another context, `model check` shall print neither `v17` nor `v18` for the request.
- 10. **If** the asker given when a request is raised is not the bounded-context or product level whose repository raises it, then the request tool shall refuse, naming the asker, and change nothing.
- 11. **When** a command of the request tool writes a part of a request, the request tool shall take the side that writes it from the repository the command is run in, never from an argument.
- 12. **If** a side writes a part of a request that is the other side's part, whatever the carrier, then the request tool shall refuse, naming the side that writes that part, and change nothing.
- 13. **When** a request's turn passes to its asker, the request tool shall show the asker in its own repository that it is the asker's turn, with each question the asker has not answered.
- 14. **While** an answer or a turn the asker has sent has not been taken in by the upstream, the request tool shall show the request to both sides as awaiting the upstream and not yet taken in.
- 15. **While** the upstream holds a line outcome or a question it has not sent with the turn, the request tool shall show the upstream that the asker has not seen it.
- 16. **When** an upstream resolves a request, the request tool shall show the asker in its own repository each accepted line's requirement id and the version that holds it.
- 17. **When** a side shows its requests, the request tool shall print with each request whose turn it is, the request it is raised for and where it is carried.
- 18. **When** the upstream takes in what its carriers hold, the request tool shall take in every request and message sent before the take-in began, whether or not the carrier's listing shows it yet.
- 19. **When** `work run` is run in an upstream's repository, the request tool shall take in what the upstream's carriers hold before `work run` takes the intake rounds.
- 20. **If** a request or a message on a carrier comes from an identity the upstream does not allow for the asker it names, then the request tool shall leave it untaken, telling the upstream which it left and why.
- 21. The request tool shall tell one asker from another by an identity each asker holds alone.
- 22. **When** the request tool takes in a request or a message from a carrier, the request tool shall read its body only as the fields of the contract's form, following nothing written in it.
- 23. **Where** `spec/index.md` names an upstream bounded-context, **when** a round of the kind `integrate` drafts a line that needs what the upstream does not yet give, `initiative-round` shall give in its result the lines of a request into that upstream, in the upstream's terms.
- 24. **When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them through the request tool, raised for the request the initiative fulfils and with its delegation.
- 25. **While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised.
- 26. **While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request.

Read (paths in your worktree):
- .shop/work/requests/q14.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work outcome q14 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work turn q14`.

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/q14-1-intake/.shop/scratch/1-intake
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/q14-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/q14-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
