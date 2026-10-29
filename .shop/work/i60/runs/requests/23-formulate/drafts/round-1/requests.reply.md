## Coverage

| id | line | scenario |
|---|---|---|
| r65 | "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has." | Scenario Outline: delegate given a request that holds <before> writes the delegation given in the request, in place of any it had |
| r66 | "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." | Scenario: delegate writing a delegation in a request commits the request on the current branch |
| r67 | "**If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing." | Scenario: delegate given an empty delegation is refused, and nothing changes |
| r68 | "**If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing." | Scenario Outline: delegate given a request that is <status> is refused, naming <status>, and nothing changes |
| r69 | "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." | none: returned as a question (below) |
| r70 | "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is." | Scenario Outline: delegate run in the <side>'s turn writes the delegation |
| r71 | "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn." | Scenario: delegate writing a delegation in a request keeps the request's status and turn |

## Questions

- r69: "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date."
  - Reading 1: the session puts the date into the text it gives `work delegate`, so the delegation the request holds is the person's words followed by the date (r65 gives `work delegate` only a request and a delegation).
  - Reading 2: the delegation the request holds is the person's words alone, word for word, and the date is written beside it in the request as something apart from the delegation.

## Cases no line mentions

- Which side may run `work delegate`: the upstream in its own repository only, or also the asker from its repository (r28 lists what the asker does from its own repository, and does not name delegating). The drafts have the upstream run it.
- Whether a delegation is a part of a request: if it is, r16 (a command other than `work resolve` writing a part in the other side's turn is refused) contradicts r70; if it is the asker's part, r4 (the asker's part written only by `work request` or an answer) contradicts r65.
- `work delegate` given a request the upstream does not keep.
- `work delegate` given a delegation of only spaces or blank lines: whether that is empty under r67.
- No way to remove a delegation once given, since r67 refuses an empty one.
- Whether `work show <request>` or `work list` prints a request's delegation.
- The person giving a session a delegation for a request not yet raised (r69).
- r12 lists the commands that commit a changed request and does not name `work delegate`; r66 adds it separately.

## Drafts

- /tmp/work-run-i60-47epophg/requests-23-formulate/.shop/scratch/23-formulate/drafts/round-1/requests.feature
- /tmp/work-run-i60-47epophg/requests-23-formulate/.shop/scratch/23-formulate/drafts/round-1/requests.reply.md
