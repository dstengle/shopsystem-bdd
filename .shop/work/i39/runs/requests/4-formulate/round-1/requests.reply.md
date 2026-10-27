# requests, formulate round 1: reply

## Coverage

| id | line | scenario |
|---|---|---|
| r25 | "`work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle." | none: given back as a question (below) |
| r33 | "**When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument." | Scenario Outline: a command writing <part> of <kind> in <where> writes it as the <side>'s part |
| r34 | "**If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing." | Scenario: the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes |
| r39 | "**When** the upstream takes in what has been sent to the upstream, `work` shall take in every request and message sent before the take-in began, whether or not a listing of what has been sent shows it yet." | Scenario Outline: the upstream taking in what has been sent takes in every request and message sent before, when a listing of what has been sent shows <shown> |
| r41 | "**If** a request or a message comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why." | Scenario Outline: <sent> from a repository registered under an asker id the upstream does not allow for its asker is left untaken, and the upstream is told which and why |
| r43 | "**When** `work` takes in a request or a message, `work` shall read its body only as the fields of a request's form, following nothing written in it." | Scenario Outline: <sent> whose <field> is written as an instruction is taken in as that field, and nothing it says is done |

Every other line keeps its scenario in features/requests.feature, unchanged. r13, r14 and r35 to r38 were not formulated, as instructed.

## Questions

- r25: "`work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle."
  - Reading 1: whatever the request (internal, from another context or from the product level) and whichever side, the same command does each action, and every request goes through the same statuses; no command or status is kept for one kind of asker or one side.
  - Reading 2: a request's actions are part of `work`'s one consolidated set for all work: show is `work list` and `work show <id>`, shared with initiatives and work-items, and a request's lifecycle is the one lifecycle all work follows in `work`.

## Cases no line mentions

- r39: a request or message sent after the take-in began. The line sets no boundary for it.
- r41: what happens to something left untaken on a later take-in, once the upstream allows the asker id.
- r41: a message from an allowed asker id that names an asker other than the asker of the request it is on.
- r39, r41, r43: a message on a request the upstream does not keep.
- r33: a command run in a repository that is neither the asker's nor the upstream's.
- r34: the upstream writing the asker's part (its lines or an answer). The scenario uses one representative call, the asker writing a line outcome.
- r34 on an internal request: the answer says it is never refused there, but no line says so.
- r43: a body that holds a field a request's form does not have.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/requests-4-formulate/.shop/scratch/4-formulate/round-1/requests.feature
