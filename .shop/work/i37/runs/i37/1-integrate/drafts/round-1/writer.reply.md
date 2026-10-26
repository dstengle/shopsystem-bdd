/home/vscode/shopsystem-bdd/.shop/worktrees/i37-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/requests.md

## Change list

| change | capability | id | line | from the note |
|---|---|---|---|---|
| added | requests | r23 | **When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's. | Line 1: "**When** the upstream ends its turn on a request and `work` sets the request to `accepted`, `work` shall keep the request's turn the upstream's." |
| added | requests | r24 | **When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker. | Line 2: "**When** `work` sets a request to `delivered`, `work` shall pass the request's turn to its asker." |
| changed | requests | r7 | new: **When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side. old: **When** `work turn <request>` is run, `work` shall pass the request's turn to the other side. | Line 1 (as above). r7 contradicted it: the upstream ends its turn by running `work turn`, and r7 passed the turn every time, including when r8 sets the request to `accepted`. The change narrows r7 to the runs that do not accept the request. |

No glossary term added, changed or removed. No decision file.

Placement: r23 goes after r8, r24 after r11. Only the Behaviour section is drafted. The frontmatter is unchanged (`retired: [r6]`).

## Questions

1. requests, r7: should r7 be narrowed, or should it stay as it is with r23 taking precedence over it? Narrowed, the line is the one in the change list: "**When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side." Unchanged, r7 stays as it was, and r7 and r23 contradict each other for an upstream that accepts a request. The @r7 scenarios in features/requests.feature use a line whose line outcome is question, so they hold under either answer.
2. Glossary, term/turn: its definition says the turn is "passed to the other side by `work turn`", but r24 also passes it when the request is delivered, and r23 keeps it on acceptance. The note gives no change to the term. If it should change: "- **turn**: the side of a request, its asker or its upstream, whose part of the request is to be written next, passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered." If not, the entry stays as it is.
3. requests, Not yet: the entry "The detail of turns, which the person reserved" is still there. Does this note give that detail? If yes, the entry is removed. If no, it stays (as drafted).
4. requests: a request that is already `accepted` in the asker's turn (q15 itself is one) is not covered by the note. If `work` should move it to the upstream's turn: "**While** a request is `accepted` and its turn is the asker's, **when** `work turn <request>` is run, `work` shall pass the request's turn to its upstream." If not, no line.
5. requests, r10: "whichever side's turn it is" can stay as it is, or become "in the upstream's turn" now that r23 keeps an accepted request in the upstream's turn. If the person narrows it: "**When** `work resolve <request>` is run in the upstream's turn on an `accepted` request with each accepted line's requirement id and the version that holds it, `work` shall write them as the request's resolution." If not, r10 stays (as drafted). The r10 scenario's given is an accepted request in the asker's turn, so narrowing r10 would break that scenario.

## Cut sentences

- "An accepted request stays in the upstream's turn until delivered" (the title; r23 and r24 already give it)
- The delegation: "Run the work. And then we need to fix that turn problem because the state doesn't make sense for the work to be accepted but then appear to be in the askers court." Answer every question with its recommended reading; where no reading is recommended, choose the one a test can check. (rationale and instruction, not spec)
