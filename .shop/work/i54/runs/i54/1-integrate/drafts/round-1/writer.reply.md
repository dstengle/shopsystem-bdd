/tmp/work-run-i54-249ng9qn/i54-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/work-queue.md
/tmp/work-run-i54-249ng9qn/i54-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source (q20) |
|---|---|---|---|---|
| added | work-queue | r48 | **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution. | line 1: "**When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution." |
| removed | work-queue | r34 | **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status. (retired; listed in `retired`) | line 2, which replaces it (delegation: "line 2 replaces work-queue r34, retired, not edited") |
| added | work-queue | r49 | **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status. | line 2: "**When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status." |
| added | supervision | r187 | **When** a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds. | line 3: "**When** a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds." |

Placement: work-queue r49 stands where r34 stood, r48 after r37 (the `work show` lines); supervision r187 directly after r159. Drafted: work-queue frontmatter (r34 added to `retired`) and Behaviour whole; supervision Behaviour whole (frontmatter unchanged).

No glossary term added, changed or removed. No decision file.

## Questions

1. work-queue r35 (not edited): it says `--json` makes `work list` print "each initiative, request and work-item with its status", which contradicts r49 (no requests). If requests leave the JSON too: retire r35 and add r50 "**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object." If the JSON keeps requests: keep r35 as it is (the text and JSON outputs then differ). Recommended: retire r35 and add r50, so that a test can check the two outputs agree.
2. supervision r159 against r187: r159 says to write a `drafted` capability-proposal for each capability the change list names, and that includes a capability the initiative already holds a proposal for, which is the case r187 covers. If r187 is meant as the exception: retire r159 and add r188 "**When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names for which the initiative holds no capability-proposal, with the requirement ids it adds, changes and removes on that capability." If not: leave r159 as it is. Recommended: the first, since a test can check that no second proposal is written.
3. supervision r187 wording: the line is drafted verbatim from the request in its strict form ("started for a capability-proposal", with no "that `work run` started", unlike r159, and with field names `adds`/`changes`/`removes`, as r145 already uses). If the person wants it to match r159's form, it would read "**When** a round of the kind `integrate` that `work run` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add to that proposal the requirement ids the change list adds, changes and removes on that capability, keeping the ids the proposal holds." with the fields named in Implementation. Recommended: verbatim, as accepted.

## Cut sentences

- Title: "Follow-ups of i39: work show of a request, work list without requests, and a redraft keeping another proposal's ids" (a heading, not a rule).
- Delegation: "Lines 1 and 2 are i39's gate-round-7 answers that apply round 8 dropped (work-queue r48, and r34 retired for a list without requests, which requests r46 lists)" (history; its r34 retirement is carried out above).
- Delegation: "Line 3 states the merge w206 implemented (reading B)." (history).
