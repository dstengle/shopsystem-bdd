# b112 phase 3, share d: migration-tools, backlog, batches, batch-measurement, telemetry

71 requirement lines: migration-tools 23, backlog 21, batches 18, batch-measurement 5, telemetry 4. One row each in
`d.tsv`. I ran every changed candidate through `python3 scripts/model parse` on main to see which parse today.

## Counts

**Pattern:** effect 58, refusal 8, transition 4, bounded 1. No invariant, precedence or liveness lines. The 4 transitions
are batches r6, r9, r16 and r17. Each is set off by a domain event (a batch parks an item, the person merges a pull
request), not by a command run. The one bounded line is backlog r19: "silent" hides the push timeout.

**Route:** all 71 are `scenario`. Every line is a next-step response to one trigger. Two lines come close to being
another pattern:

- batches r5 ("`work batch resume` never asks a question") is close to an invariant.
- backlog r20, refusing on a task's branch, is one instance of a rule that holds for every committing `work` command.
  A universal statement routed to a check after each scenario could carry it.

**Example data:** 24 lines carry it (`y`): 18 of the 23 migration-tools lines, all 5 of batch-measurement, and
backlog r4 and telemetry r4. In migration-tools the example data often *is* the rule. Some examples:

- r1 lists eleven fixture paths in place of "relocate every old-layout directory".
- r5's path `0008-b.md` encodes "one above the highest number".
- r15's `w1.md` stands for "replace `awaiting-ruling` with `awaiting-answer`".
- batch-measurement's `m1.md`, `m2.md` and `m3.md` stand for "a measurement that gives round trips / no round trips /
  sessions".

**Constructs** (lines needing each):

| Construct | Lines | Note |
|---|---|---|
| OF | 27 | mostly "the release of a repository is `x`" (13 migration-tools lines) |
| EXAMPLE-DATA-OUT | 24 | |
| STATE-MOVE | 14 | a state on the trigger's object moves into While (backlog r2, r3, r9-r14, r16; batches r6, r10, r18; telemetry r1); a Where used for a command option (backlog r8) |
| NEG-EXIST | 12 | "has no shop directory", "holds no version", "has no number", "ask no question", "answers no push" |
| SENSE | 11 | a second frame with a thing as subject: names, gives, includes, holds, refuses, fails, answers |
| HAS | 9 | all in migration-tools ("a repository has an untracked file / a decision ledger / no shop directory") |
| RC-SUBJ | 9 | |
| COMPARE | 7 | "another entry / the other entry", "after the release", "a different name" |
| NP-LIST, VP-COORD-NEG, COUNT, REL-COPULA, ADJUNCT-PP | 3-4 each | |
| AGGREGATE (new) | 2 | migration-tools r5, r6 |
| CONFORMS | 2 | batches r1, r2: "passes the readiness bar" |
| VALUE-SET (new) | 1 | migration-tools r24; would also merge backlog r9-r12 and r13-r14 |
| POSS, WITH-ARG, WHOSE-REL | 1 each | |
| none | 13 | the 12 unchanged lines, plus backlog r17 |

New construct names:

- **AGGREGATE**: the highest (or next) of a set of values, and arithmetic on it. Examples: "one above the highest number
  of the decision ledger", "the next id of the capability".
- **VALUE-SET**: a disjunction of values of one attribute, as in "a request that is `open`, `awaiting-asker`,
  `awaiting-upstream` or `accepted`". It takes the place of a coined complement such as "not closed".

**Parses today:** 27 of 71. That is the 12 lines left as they are, plus 15 rewrites:

- backlog r2, r3, r8, r9-r14, r16, r17;
- batches r3, r7, r10.

Every one of those 15 is a STATE-MOVE or drops a coined adjective by using a relation row that already exists.
Examples: "a dependency of the item is on an item that is not `delivered`" for blocked, and "a pull request of the batch
with no commit of the item". **No migration-tools candidate parses.** All 13 release lines stop at "the release of a
repository **is**" (OF with an attribute as subject). The rest stop at "has", where HAS is missing.

**Adjectives removed:** 26 words, 27 senses, since passing has two:

- **migration-tools (19 words):** unmigrated, ledgered, superseding, qualified, numberless, idless, conflicting,
  uncommitted, behind, unversioned, misversioned, current, outdated, uncodified, ahead, idle, shopless, queued, unframed.
- **backlog and batches (7 words):** blocked, unpushable, silent, tracking, tasked, passing (item sense and scenario
  sense), uncited.

Kept: codified (it names the language marker) and open (of initiative, a defined condition that parses in Def). Status
values (`idea`, `in-batch`, `merged`, `own` and the rest) stay as values and are not counted.

Six of migration-tools' adjectives are each a pure synonym of one release value: behind, outdated, current, ahead,
queued, and uncodified in part. "While a repository is `0.23.1`" already parses, so they were never needed.

Terms no line in this share uses:

- migration-tools: busy, append.
- batch-measurement: unwritten, requestless, overfulfilling, present, and the attributes content, availability,
  standing and ending, with their nouns (initiative log, session file, transcript, fulfilled request, logged stage).
  These are all left from r1-r17, retired in 2.0.0.

## Hard lines

- **migration-tools r4** ("supersedes another in part"). "in part" qualifies a relation. No construct gives a relation an
  attribute or a manner adjunct.
- **migration-tools r7** (conflicting: "a file where `migrate run` *would* relocate another"). The state is
  counterfactual: it is computed from the command's own plan. The candidate has to make the plan into nouns
  (relocation, destination).
- **migration-tools r25.** `3.0.0` and 2.x are not values of release, whose values stop at `1.0.0`, `own` and `newer`.
  "After `1.0.0` and before `3.0.0`" therefore needs release to become an ordered version, not an enum. The better model
  is "the upgrade step 'verb frames' is pending" (HISTORY).
- **migration-tools r10, r13, r16, r24.** Each line is several rules under one trigger: two upgrade steps in r13, four
  parts each in r16 and r24. Each also has thin responses ("rewrite <path>") where the group title holds the content.
  Splitting into one line per step is the honest fix.
- **backlog r4** (`work rate`). The rule binds a command argument to an attribute value ("set the value of the item to
  the one given"). No construct says "the one given", so the values stay in the line as example data or the rule goes
  unsaid.
- **backlog r7.** It restates half of blocked's definition and then uses blocked too, which is circular. "not in the
  same batch" needs identity of referents (COMPARE). Without a reading rule, "not in a batch of the item" is a negated
  indefinite.
- **batch-measurement r22** compares `m3.md` with itself, so "two measurements" (COUNT, distinct) is false of the test.
- **batches r18** never says that the task is not the parked item's, yet that is the group's whole point. **batches r4**
  "its status" parses but gives 3 trees, so POSS does not resolve it.

## Words in more than one meaning

- **passing**:
  - the glossary's item sense: well-formed and every request line settled;
  - red-green's scenario sense: the test passes. batches r18 uses this sense, in the same capability as r1 and r2.
- **uncommitted**:
  - migration-tools: "an untracked file whose text no commit holds", which is redundant, because the glossary's
    untracked file already includes "a change not committed";
  - design-model-check: another sense.

  The noun *untracked file* itself merges git's untracked and modified.
- **merge**: its gloss ("`work run` merges a work-item branch into the initiative branch") contradicts its frame ("the
  person merges pull request"). batches r9 and r16 use the frame's sense.
- **relocate / rename**:
  - relocate is used for splitting a ledger (r2);
  - rename is used for moving requests between directories (r24).
- **include** (telemetry r1, r2): the frame makes `measure` the subject, so the agent is wrong (as phase 2 found).
- **publish**: used of a commit in batches r7, outside its gloss (a branch as a pull request).
- **park and pick**: their glosses already state the responses that batches r6 and r2 then repeat. Those Thens are
  entailed by the verb's definition.
- **"the repository"**: a definite with no antecedent, in migration-tools r13-r16, r24 and r25.
- **"not ... a"**: negated indefinites where "no" is meant: batches r5 ("not ask a question"), r18 ("a scenario ... is
  not passing"), and backlog r19 as written in silent's definition.

## What the candidate form cannot say

1. **Time bounds**: backlog r19's "no answer within the push timeout". No construct exists. It needs a named setting or
   a BOUNDED-TIME form.
2. **Binding a command argument to a value** (backlog r4) and **referring to the same thing twice** (r22's self-compare).
3. **Attributes on relations** ("supersedes in part").
4. **Counterfactual or plan-based states** (r7's "would relocate").
5. **Ordered values**: release as a version, for r25 and for "after the release of the repository" in r10 and r17.
6. **Aggregates**: "the next id", "one above the highest", and telemetry r2's "counted by grade", which the line
   weakens to "includes the grade".
7. **Content the lines never had.** Group titles often say more than their line: batch_size in batches r1, "every
   pending step in one commit" in migration r13, "tells the session nothing" in migration r20. A rewrite can surface
   this only by adding to the line.
