# Phase 3, share b: requests, intake, conversation, readiness

64 requirement lines: requests 44, intake 4, conversation 4, readiness 12. One row each in `b.tsv`. Every
candidate that differs from today's line was put through `python3 scripts/model parse` on main (2026-11-08).

## Counts

**Pattern.** effect 38, refusal 25, invariant 1 (readiness#r4, "`work ready` shall never ask a question"). There
are no transition, precedence, bounded or liveness lines. Requests r45-r47 are counted as refusals: they are
unwanted-behaviour If lines ("shall not post an issue") with no error clause.

**Route.** All 64 go to `scenario`. Each is a next-step effect of one command run. readiness#r4 is an invariant
over a command, and a scenario run with no input still tests it, as it does today.

**Changed or not.** 8 lines stay as they are (`=`). 56 get a candidate. Of those, 11 parse today (requests r14, r15,
r17, r18, r24, r29, r31, r34, r56; intake r7; readiness r3). Most of these 11 only move a state out of the trigger
("on a request that is `open`" becomes "While a request is `open`, ... on the request"), or replace "change the side"
with "set the side of the request to `upstream`". 11 lines need no construct.

**Constructs** (number of lines):

| Construct | Lines | Where |
|---|---|---|
| STATE-MOVE | 18 | "on a request that is `<status>`" moved into While (requests ×15, intake r9, readiness r3) |
| WITH-ARG | 14 | the four `Where --x is given` lines of readiness, plus r2, r6-r9, r28, intake r9 |
| **THIS** (new) | 12 | received, sent, downstream, foreign, untaken: every one depends on which context is "here" |
| OF | 11 | mostly "close the issue of the request" (r30, r37, r41, r46, r47) |
| SENSE | 11 | hold with a request as subject (unrecorded), names with an entry as subject, git refuses a commit |
| RC-OBJ | 9 | "every comment that its request does not hold", "every message that the quote cites" |
| COMPARE | 8 | "another bounded context" (received, sent, foreign) |
| CONFORMS | 7 | comment schema (r33, r44, r57), requirement grammar (r38), the three "malformed" forms of readiness |
| VP-COORD-NEG | 7 | "print the comment and not write the comment" |
| NEG-EXIST, POSS | 7 each | |
| HAS, WHOSE-REL | 6 each | |
| ADJUNCT-PP | 5 | "write the relation row onto the item", "record the session in the git directory" |
| NP-LIST, NEVER/ALWAYS, RC-SUBJ | 1 each | |

**New construct, THIS:** a fixed noun phrase for the bounded context whose repository the command runs in ("this
bounded context"). Today "While a bounded context is downstream" reads as *any* bounded context, because an
indefinite in While means any. The line means the one the command runs in. Five coined adjectives of requests
(downstream, foreign, received, sent, untaken) all hide this deictic reference. `this` could be a proper-noun
actor in the glossary rather than a grammar construct. Either way the logic has to know that it is one individual.

**Adjectives removed** (19 words over 31 line-uses): unrecorded 5, downstream 3, unreadable 3, uncommittable 3,
received 3, sent 3, malformed 3 (three senses), originless 2, untaken 2, passing 2, sourced, foreign, uncited,
unhosted, unparsed, absent, unworded. **Kept:** settled (5 uses; its definition parses: accepted, refused or
withdrawn), closed (2; it parses, but see below), and the status values. `foreign entry` stays as a compound noun.
`passing` also parses as a definition, but it rests on `well-formed`, which is prose for four checks. The candidate
says "passes the readiness bar" instead: a named artifact and a verb, no grammar change.

**Example data:** none. The share has no paths, versions or test strings. Arguments such as `rewritten` and
`accepted` in `work outcome` are line outcomes, so they are part of the rule.

## Lines that were hard, and why

- **requests#r16 means something other than what it says.** "While a bounded context is downstream, `work outcome`
  is refused." A context that has an upstream can still be the upstream of a request it received, and it may write
  that request's outcome. The meant condition is r51's "sent": the request's upstream is another context. The
  adjective hid the wrong structure. Writing it out exposes the error.
- **requests#r7 and its group title disagree.** The title says "a request to an upstream cites no observation". The
  line refuses only `--source` combined with `--thread` or `--raised-for`, which is what "sourced" is defined as.
  requests#r8 follows from r6, which refuses an originless request in every context, so r8's While adds nothing.
- **requests#r28 (unhosted)** never ties the unhosted context to the command. As written, any unhosted upstream
  refuses every `work request`. The candidate needs "to the bounded context" as an argument of the trigger.
- **requests#r45-r47 (uncommittable)** describe the environment: a failing hook or a held lock. The candidate makes
  git the agent ("While git refuses every commit in a repository"). The parse refuses it: refuse's frame is
  "tool refuses command". That needs a second sense, plus git as an actor.
- **requests#r52 and r53.** In r52 the candidate repeats "holds" ("a comment that its request does not hold holds a
  foreign entry"). In r53, "the request does not hold a comment on the request" needs the existential reading:
  *some* comment it does not hold. That is today's reading of a negated indefinite. A reading rule that changed it
  to "holds no comment" (ACE's reading) would break this line. The reading rules have to be written per construct
  and tested against lines like this one.
- **requests#r37** keeps "a request line ... is `refused` and every request line ... is `refused`". The first
  conjunct is there only to rule out a vacuous "every" over no lines. A written rule that every presupposes at least
  one would drop it.
- **requests#r36 and r39** share a three-conjunct While: open, every line settled, one accepted. Naming that
  composite state would bring back a coined adjective. This is the one place the share argues for named composite
  states, as defined conditions whose definitions parse.

## Words used in more than one meaning

- **change:** glossed "agent changes file", but used on an attribute ("change the side of the request": r34, r36,
  r41, r53, intake r7). "set the side of the request to `upstream`" parses today, names the value and can be checked.
- **closed:** a request is closed when it is delivered, refused or withdrawn; capability-proposal, glossary-proposal
  and work-item each have their own "closed". The verb **close** also closes an *issue*, so in requests "closed" can
  mean either one.
- **open:** a status value of request, a defined condition of initiative and work-item, and GitHub's state of an
  issue (inside untaken's definition).
- **malformed:** three senses in readiness alone (relation row, upstream entry, given block). Each becomes
  conformance to its own schema.
- **keep:** conversation#r2 uses it for "store". The gloss says "leave as it was". (Phase 2 found the same.)
- **write:** in r52 and r53, "write the comment" means record it under `## Comments`. "not write the foreign entry"
  means not apply it to a section. These are two operations under one verb.
- **uncited, unparsed:** second senses in batches and design-model-check (phase 2).
- **hold:** used for a request holding a comment, a comment holding an entry and an issue holding an ask. No frame
  for any of them; each needs a relation row or a sense.

## Inconsistencies the rewrite exposed

- **Agents:** `work outcome` is run by "the person" in r14-r16 and by "a session" in r38 and intake r7-r9.
  `work ready` is run by a session in intake r6 and by the person in readiness.
- **"change nothing":** missing on six refusals (requests r48-r51, intake r9, readiness r12), and r45-r47 have no error clause at all.
  U11 supplies it only if "exit with an error" counts as the tool refusing the command. Without a written
  entailment rule, the stated and the unstated refusals read differently.
- **Commits:** "commit the request" is stated on some effects and left to U4 on others (r34, r35, r36, r37, intake r7).
- **Overlaps:** requests#r18 (work reply on an awaiting-asker request) clashes with r49 (refused on a received
  request) unless r18 also requires a sent request. readiness r2 covers intake r6, and r12 should be one of the
  readiness bar's checks. requests r44/r57 and r43/r58 differ only by `--forward`.
- **Indefinites with no link:** "close an issue" (r30, r37, r41, r46, r47), "post a comment" (where?), "naming the
  reason" (readiness r2, as U11) and "write a relation row" (onto what?). OF and ADJUNCT-PP fix them one by one.
  A rule that refuses an unlinked definite would catch them.

## What the candidate form cannot say

- **Which context is here** (THIS, above). This is the most frequent need in requests that phase 2's list does not
  have.
- **Where for options.** EARS's Where is for a feature of the product. Here it is used for a command's option
  (requests r2, readiness r5-r11). WITH-ARG in the trigger is the honest form. It needs a kind for options, or
  arguments as noun phrases.
- **The object of a command versus its argument.** readiness r6/r9/r11 say "runs `work line` on a relation row"
  when the command runs on an item and takes the row as an argument. The trigger has one "on" slot.
- **readiness#r4's subject is a command** ("`work ready` shall never ask"). Actors are tools, so a per-command
  invariant has to be said as a When.
- **r56 under-states the behaviour.** The hook is silent whenever no request waits on the other side, which is a
  wider condition than "every request is closed". Saying the real condition needs the waiting relation
  (sent and awaiting-upstream, or received and awaiting-asker) as a negated existential over a disjunction:
  "no request whose upstream is another bounded context is `awaiting-upstream` and ...". The form can say it, but
  only at great length.
