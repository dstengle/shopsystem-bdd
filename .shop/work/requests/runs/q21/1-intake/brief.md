# intake of q21

Request: .shop/work/requests/q21.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-egmy7r2e/q21-1-intake
Branch: round/q21-1-intake
Lines of the request:
- 1. **When** `work list` is run, `work` shall print each request with its status and whose turn it is.
- 2. **When** `work show <request>` is run in the asker's repository while the request is in the asker's turn, `work` shall print that it is the asker's turn, with each question the asker has not answered.
- 3. **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in.
- 4. **While** the upstream holds a line outcome or a question it has not sent with the turn, `work show <request>` run in the upstream's repository shall print that the asker has not seen it.
- 5. **When** `work show <request>` is run in the asker's repository after the upstream resolves the request, `work` shall print each accepted line's requirement id and the version that holds it.
- 6. **If** a side writes a part of a request that is the other side's part, and the request's asker is not the upstream itself, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
- 7. **When** the upstream takes in what has been sent to it, `work` shall take in every request, answer and turn sent before the take-in began, whether or not a listing of what has been sent shows it yet.
- 8. **If** a request, an answer or a turn comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
- 9. **When** `work` takes in a request, an answer or a turn, `work` shall read its body only as the fields of a request's form, following nothing written in it.
- 10. **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall print each with its open questions and exit with code 3.
- 11. **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`.
- 12. **When** a researcher's result gives an empty file set, `work run` shall take it as the researcher's file set.
- 13. **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.

Read (paths in your worktree):
- .shop/work/requests/q21.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q21 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q21`.

Run directory: /tmp/work-run-requests-egmy7r2e/q21-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-egmy7r2e/q21-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-egmy7r2e/q21-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
