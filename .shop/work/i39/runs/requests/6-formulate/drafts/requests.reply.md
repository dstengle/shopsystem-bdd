I wrote one scenario for r25, tagged `@r25`. It uses the gate's reading (a), so there is no question.

## Coverage table

| line | scenario | kind |
|---|---|---|
| r25 | requests from another context, from the product level and from the upstream itself are each taken through the same work commands and the same statuses | Scenario (one, with a data table of steps) |

The scenario has three askers: another context (ctx-a), the product level (p1) and the upstream itself (ctx-u). Each one's request goes through the same steps:

- raise
- take in
- ask
- pass the turn
- answer
- pass the turn
- take in
- give a line outcome
- pass the turn
- resolve
- show

That covers both sides and all eight actions the line names. Every step is run as the same command for all three requests. The Then lines check four things:

- Every step exits successfully.
- Each step is one command of work's set, and it is the same command for all three requests.
- Every request's status goes open, awaiting-asker, awaiting-upstream, accepted, delivered.
- The turn goes the upstream's, the asker's, the upstream's, the upstream's, the asker's.

Where I could, I reused the existing step wording ("asks the question … on line 1", "answers that question with …", "takes in what has been sent to it", the `work resolve` giving, `--thread t1`).

## Questions

None. The gate's reading (a) removes the ambiguity.

## Cases no line mentions

- **No command names for three actions.** The spec does not name the commands for taking in, asking or answering. The scenario only says that each is "one command of work's set, the same for the three requests", so the step code must work out which command was used.
- **Take-in on an internal request.** When the upstream raised the request itself, nothing was sent, so no line says what taking in does for it. The scenario only needs the take-in to exit successfully; the status sequence is unchanged.
- **The take-in after the asker passes the turn.** I put a second take-in after the asker passes the turn, so the upstream sees the answer and the turn whether or not answers reach the upstream through a take-in. No line says whether that take-in is needed.
- **Statuses the scenario does not reach.** `refused` (r9) is a different path through the same lifecycle. `withdrawn` has no command yet (it is in Not yet).

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/requests-6-formulate/.shop/scratch/6-formulate/drafts/requests.feature.fragment
