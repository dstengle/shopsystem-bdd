# Gate, round 1: q21 (i55)

Drafts: `.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/{requests,supervision,work-queue}.md`

## requests (retired gains r13, r34, r39, r41, r43)

Removed:
- [r13] **When** `work show` is run, `work` shall print each request with its status and whose turn it is. (replaced by r50; q21 line 1)
- [r34] **If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing. (replaced by r55; q21 line 6)
- [r39] **When** the upstream takes in what has been sent to the upstream, `work` shall take in every request and message sent before the take-in began, whether or not a listing of what has been sent shows it yet. (replaced by r56; q21 line 7)
- [r41] **If** a request or a message comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why. (replaced by r57; q21 line 8)
- [r43] **When** `work` takes in a request or a message, `work` shall read its body only as the fields of a request's form, following nothing written in it. (replaced by r58; q21 line 9)

Added:
- [r50] **When** `work list` is run, `work` shall print each request with its status and whose turn it is. (q21 line 1)
- [r51] **When** `work show <request>` is run in the asker's repository while the request is in the asker's turn, `work` shall print that it is the asker's turn, with each question the asker has not answered. (q21 line 2)
- [r52] **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in. (q21 line 3)
- [r53] **While** the upstream holds a line outcome or a question it has not sent with the turn, `work show <request>` run in the upstream's repository shall print that the asker has not seen it. (q21 line 4)
- [r54] **When** `work show <request>` is run in the asker's repository after the upstream resolves the request, `work` shall print each accepted line's requirement id and the version that holds it. (q21 line 5)
- [r55] **If** a side writes a part of a request that is the other side's part, and the request's asker is not the upstream itself, **then** `work` shall refuse, naming the side that writes that part, and change nothing. (q21 line 6)
- [r56] **When** the upstream takes in what has been sent to it, `work` shall take in every request, answer and turn sent before the take-in began, whether or not a listing of what has been sent shows it yet. (q21 line 7)
- [r57] **If** a request, an answer or a turn comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why. (q21 line 8)
- [r58] **When** `work` takes in a request, an answer or a turn, `work` shall read its body only as the fields of a request's form, following nothing written in it. (q21 line 9)

Implementation line "r41, r42" becomes "r57, r42" (no Behaviour change).

## supervision

Added:
- [r184] **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall exit with an error, printing each with its open questions. (q21 line 10; "exit with code 3" is drafted as "exit with an error" under design-decision/exits-are-successful-or-errors, the code being held by Implementation: "3 awaiting an answer")
- [r185] **When** a researcher's result gives an empty file set, `work run` shall take it as the researcher's file set. (q21 line 12)
- [r186] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. (q21 line 13)

## work-queue

Added:
- [r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`. (q21 line 11)

## Glossary

No entry added, changed or removed.

## Decisions

None.

## Questions

1. **requests r14** (`work status` observations). The delegation says r14 "is retired with work status", but no accepted line retires it. Readings: (a, recommended) retire r14 and add "[r59] **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names."; (b) retire r14, no replacement; (c) keep r14.
2. **supervision r186 vs r149** (word for word the same). Readings: (a, recommended) retire r149, keep r186, so a work-item is drafted for the fault i39 met; (b) drop r186, keep r149; (c) keep both. r152 and r153 do not conflict and stay.
3. **supervision r184 vs r32, r81, r9.** r184 covers r32 and conflicts with r9 when every work-item is done while a capability-proposal is `awaiting-answer`. Readings: (a, recommended) retire r32 and r9, adding "[r187] **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status."; (b) keep r32 and r9, r184 taking precedence; (c) keep r32 and r184, retire r9 only. r81 stays (recommended) or also prints each proposal's open questions.
4. **supervision r184, exit code.** Readings: (a, recommended) as drafted, the code in Implementation only; (b) add an Implementation line "r184: the exit code is 3".
5. **work-queue r47 vs r23, and supervision r105** (done set with no condition on capability-proposals). Readings: (a, recommended) retire work-queue r23 for "[r48] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." and retire supervision r105 for the same condition as r188; (b) keep r23 and r105, r47 the exception; (c) change only r23.
6. **work-queue r47, `merged` proposals.** Readings: (a, recommended) as drafted, word for word; (b) "neither `formulated`, `merged` nor `withdrawn`".
7. **supervision r185 vs r132/r131.** Readings: (a, recommended) keep r132 and r131, r185 beside them; (b) retire r132 for "a researcher's file set, empty or not" and drop r185. An empty planner's file set: (a, recommended) nothing drafted; (b) add "[r189] **When** a planner's result gives an empty file set, `work run` shall take it as the planner's file set."
8. **requests r50 vs work-queue r34** (`work list` already prints requests with status). Readings: (a, recommended) keep both; (b) fold r50 into r34 (retire r34).
9. **requests r52, "on either side".** Readings: (a, recommended) `work show <request>` run in the asker's and in the upstream's repository both print it; (b) shown as awaiting on both sides of its turn. `--json` for "not yet taken in": (a, recommended) nothing drafted.
10. **requests r55 vs r16.** r55 exempts a request whose asker is the upstream itself; r16 has no exemption. Readings: (a, recommended) keep r16; (b) retire r16 for a line with the same exception.

## Cut sentences

1. The note's title "Requests shown by work list and work show, and the faults i39 met".
