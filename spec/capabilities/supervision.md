---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started `work run`
group: service
language: codified-1
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
retired: []
---

# Supervision

## Purpose
`work run` takes a bounded context's initiatives through their transitions: `work run <initiative>` that
initiative, `work run` with no initiative every initiative that is neither `done` nor `abandoned`. It starts the
`intake` round of a request this context is the upstream of, starts with `work start` the initiative of such a
request once it is `accepted`, and starts the `integrate` round of an initiative, checks and keeps that round's drafts
and writes the capability-proposals its change list names, starts a capability-proposal's `gate` and `apply` rounds,
runs its `formulate` round as a script, drafts and delivers its work-items, for each stage starting a fresh
`claude -p` worker, reading the worker's result and writing the status itself, starts the initiative's measurement
and analysis and commits them, and sets the initiative `done`, committing it, when what it delivers is closed
(design-decision/the-context-runs-without-a-coordinator). It is a script and takes no judgment; what nobody may
decide goes to the person as a question.

## Terms
- **for** (relation stage → work-item): the work-item a worker's stage is started for.
- **for** (relation stage → initiative): the initiative an `integrate` round, a branch review or an analysis is started for.
- **for** (relation stage → capability-proposal): the capability-proposal a round is started for.
- **for** (relation stage → glossary-proposal): the glossary-proposal a round is started for.
- **for** (relation stage → request): the request an `intake` round is started for.
- **for** (relation stage → question): the question an `answer` stage is started for.
- **on** (relation question → work-item): the work-item a question is written in, under its `## Questions`.
- **on** (relation question → capability-proposal): the capability-proposal a question is written in.
- **on** (relation question → glossary-proposal): the glossary-proposal a question is written in.
- **on** (relation question → request): the request a question is written in.
- **on** (relation stage → work-item branch): the branch an `implement` stage works on.
- **draft** (event): `work run` writes a node with `work add` or from a change list. Forms: drafts, drafted.
- **take** (event): `work run` takes an initiative through the transitions its nodes can make. Forms: takes, took, taken.
- **log** (event): `work run` appends a line to `.shop/work/<initiative>/log.jsonl` with the time, the node, the stage, the agent and the session id. Forms: logs, logged.
- **restore** (event): `work run` puts a file back as its last commit has it, or removes it where that commit has none. Forms: restores, restored.
- **remove** (event): `work run` removes a worktree it made. Forms: removes, removed.
- **output** (kind): what a stage's result gives as its stage's work: a researcher's file set, empty or not; a planner's plan and file set; an implementer's commits on which the work-item's scenarios and the suite pass; a reviewer's findings; an answering session's answer; an `integrate` or `apply` round's change list, or an `apply` round's answers its drafts do not hold; an `intake` round's line outcome or question on each line of its request; a `gate` round's questions.
- **change list** (kind): the list an `integrate` or `apply` round's result gives of the requirement ids and the terms it adds, changes and removes, under each capability and the glossary.
- **draft** (kind): a file an `integrate` round writes under its drafts path, kept on the initiative branch. Plural: drafts.
- **tool list** (kind): what `work run` gives a worker to work with: this plugin's own directory as its plugin; the tools of its agent less any bare Write or Edit, or the stage's `[allowed_tools]` of `.shop/delivery.toml` less any bare Write or Edit; Bash only for `python3 -m pytest`, the plugin's scripts its stage runs, by path, and the git commands its stage needs; and `Skill` for each skill its agent lists.
- **worker brief** (kind): the brief of a worker: it names the work-item, the files to read, where its result goes, the plugin's scripts directory, the initiative branch's base, the worker's worktree and its work-item branch; it tells the worker that it starts in its worktree and never changes directory, and to write its result first with the outcome `PARTIAL` and keep it current; it holds each answer of the work-item with the question it answers; a researcher's gives the work-item's file set and accepted scenarios and a limit of 80 turns; an implementer's says how the suite ended in its worktree before it started and, for a work-item an answer to its reviewer's question returned to `ready`, the reviewer's findings and the answer.
- **round brief** (kind): the brief of a round: an `integrate` round's gives the accepted lines of the request its initiative fulfils, every requirement id that the kept drafts of another initiative, not yet applied, add, and, for a proposal that has answers, its questions and answers and the initiative's ledger; a `gate` round's asks only for the questions on what its proposal adds, changes or removes, each a decision with its readings and the recommended reading marked; a `gate` or `apply` round's gives the path of the kept drafts of the `integrate` round that wrote its proposal, and an `apply` round's the answers.
- **review brief** (kind): the brief of a branch review: each run made at the initiative branch's head before it starts (the suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`) with its command, its exit code and its output and the commit they ran at; the commits from the initiative branch's base to its head, each with the work-item it belongs to or none; the change of that range less `.shop/`; and the files to read: the capabilities the work-items are under, the design-decisions those rest on, and each work-item's plan, implementer's report and review findings.
- **faulty** (condition of session): Means: it ends in an error or at its turn limit, or leaves output that holds no JSON result.
- **meddling** (condition of session): Means: it changes a file under `.shop/work/` outside its stage directory.
- **littering** (condition of session): Means: while it works, a file under `.shop/work/` of the checkout changes and is left uncommitted.
- **crossing** (condition of session): Means: while it works, a session of another initiative that `work run` runs side by side commits a file of that other initiative and a change to a file of its own.
- **outputless** (condition of result): Means: it gives neither a question nor its stage's output.
- **setless** (condition of result): Means: it gives an empty file set.
- **listless** (condition of result): Means: it gives no change list.
- **glossarial** (condition of result): Means: its change list names the glossary.
- **raising** (condition of result): Means: it gives the lines of a request into an upstream.
- **strange** (condition of result): Means: its change list names a capability that neither `spec/capabilities/` nor its drafts have.
- **unheld** (condition of result): Means: it gives an answer that the drafts its stage applied do not hold.
- **fixing** (condition of result): Means: it gives a question listing review findings to fix now.
- **unparsing** (condition of result): Means: a requirement its drafts hold does not parse, or the logic check on the spec with its drafts finds an L1 or an L3.
- **naming** (condition of result): Means: it names a report the session wrote in its worktree.
- **unpushable** (condition of remote): Means: it refuses every push.
- **ahead** (condition of initiative branch): Means: it has commits its remote does not have.
- **reviewed** (condition of initiative branch): Means: a kept branch review has read every commit on it but the kept branch reviews' own.
- **gitless** (condition of initiative branch): Means: the repository it would be in is not a git repository.
- **lost** (condition of work-item branch): Means: its implementer deleted it before `work run` merged it.
- **kept** (condition of work-item branch): Means: `work run` kept it when its work-item became `awaiting-answer`.
- **flaky** (condition of work-item branch): Means: a scenario fails on it once and passes on its second run alone.
- **dirty** (condition of file): Means: it is under `.shop/work/` and differs from its last commit.
- **held** (condition of capability-proposal): Means: a request an `integrate` round raised with its lines is not `delivered`.
- **answered** (condition of capability-proposal): Means: every question a `gate` round gave on it has an answer.
- **answered** (condition of glossary-proposal): Means: every question a `gate` round gave on it has an answer.
- **bare** (condition of initiative): Means: it fulfils a request and has no capability-proposal, no glossary-proposal and no work-item.
- **itemless** (condition of initiative): Means: no work-item is kept in it.
- **codified** (condition of change list): Means: every capability it names has `language: codified-1` in its file.
- **uncodified** (condition of change list): Means: a service capability it names has no `language: codified-1` in its file.

## Behaviour

### [g1] `work run` takes every open work-item to green
Restates: r1@0.29, r111@0.29.
- [r1] While a remote is not unpushable, when the person runs `work run` on an initiative, `work run` shall set the status of every open work-item to `green`.

```given
a remote r1
the remote r1 is not unpushable
```

### [g2] A drafted work-item gets a research stage
Restates: r2@0.29.
- [r2] While a work-item is `drafted`, when the person runs `work run` on an initiative, `work run` shall start a `research` stage for the work-item.

```given
a work-item w1 that is `drafted`
```

### [g3] A researched work-item gets a plan stage
Restates: r2@0.29.
- [r3] While a work-item is `researched`, when the person runs `work run` on an initiative, `work run` shall start a `plan` stage for the work-item.

```given
a work-item w1 that is `researched`
```

### [g4] A ready work-item gets an implement stage
Restates: r2@0.29.
- [r4] While a work-item is `ready`, when the person runs `work run` on an initiative, `work run` shall start an `implement` stage for the work-item.

```given
a work-item w1 that is `ready`
```

### [g5] A done work-item gets a review stage
Restates: r2@0.29.
- [r5] While a work-item is `done`, when the person runs `work run` on an initiative, `work run` shall start a `review` stage for the work-item.

```given
a work-item w1 that is `done`
```

### [g6] A worker's stage starts with a worker brief and a tool list
Restates: r11@0.29, r12@0.29, r13@0.29, r14@0.29, r17@0.29, r19@0.29, r25@0.29, r30@0.29, r44@0.29, r57@0.29.
- [r6] While a work-item is `drafted`, when the person runs `work run` on an initiative, `work run` shall give a `research` stage for the work-item a worker brief.
- [r7] While a work-item is `drafted`, when the person runs `work run` on an initiative, `work run` shall give a `research` stage for the work-item a tool list.

```given
a work-item w1 that is `drafted`
```

### [g7] A worker's start and end are logged
Restates: r8@0.29, r62@0.29.
- [r8] When `work run` starts a `research` stage for a work-item, `work run` shall log the stage.
- [r9] When `work run` starts a `research` stage for a work-item, `work run` shall name a transcript.

### [g8] A stage that gives its output makes the next transition
Restates: r130@0.29, r132@0.29.
- [r10] When a session ends a `research` stage for a work-item with a result that is `DONE`, `work run` shall start a `plan` stage for the work-item.

### [g9] An empty file set is a researcher's output
Restates: r185@0.29.
- [r11] While a result is setless, when a session ends a `research` stage for a work-item with the result, `work run` shall start a `plan` stage for the work-item.

```given
a result r1
the result r1 is setless
```
### [g10] The outcome a result gives makes no transition
Restates: r133@0.29.
- [r12] When a session ends a `research` stage for a work-item with a result that is `BLOCKED`, `work run` shall start a `plan` stage for the work-item.

### [g11] A planner's questions make the work-item await an answer
Restates: r129@0.29, r36@0.29.
- [r13] When a session ends a `plan` stage for a work-item with a result that is `QUESTION`, `work run` shall set the status of the work-item to `awaiting-answer`.
- [r14] When a session ends a `plan` stage for a work-item with a result that is `QUESTION`, `work run` shall ask a question on the work-item.

### [g12] A researcher's questions go into the planner's brief
Restates: r129@0.29.
- [r15] When a session ends a `research` stage for a work-item with a result that is `QUESTION`, `work run` shall give a `plan` stage for the work-item a question.

### [g13] A result with no output makes the work-item await an answer
Restates: r131@0.29, r132@0.29.
- [r16] While a result is outputless, when a session ends a `plan` stage for a work-item with the result, `work run` shall set the status of the work-item to `awaiting-answer`.
- [r17] While a result is outputless, when a session ends a `plan` stage for a work-item with the result, `work run` shall ask a question on the work-item.

```given
a result r1
the result r1 is outputless
```
### [g14] A faulty worker's session fails its work-item
Restates: r128@0.29, r45@0.29, r40@0.29.
- [r18] While a session is faulty, when the session ends a `research` stage for a work-item, `work run` shall set the status of the work-item to `failed`.
- [r19] While a session is faulty, when the session ends a `research` stage for a work-item, `work run` shall exit with an error naming the work-item.

```given
a session s1
the session s1 is faulty
```
### [g15] An implementer's branch with a green check is merged
Restates: r4@0.29, r15@0.29, r24@0.29.
- [r20] While a work-item branch is green check and a result is naming, when a session ends an `implement` stage for a work-item with the result, `work run` shall merge the work-item branch.
- [r21] While a work-item branch is green check and a result is naming, when a session ends an `implement` stage for a work-item with the result, `work run` shall keep a report.

```given
a result r1
the result r1 is naming
a work-item branch w2
the work-item branch w2 is green check
```

### [g16] An implementer's branch without a green check is not merged
Restates: r4@0.29.
- [r22] While a work-item branch is not green check, when a session ends an `implement` stage for a work-item, `work run` shall not merge the work-item branch.

```given
a work-item branch w2
the work-item branch w2 is not green check
```

### [g17] A merged work-item branch is deleted
Restates: r18@0.29.
- [r23] When `work run` merges a work-item branch, `work run` shall delete the work-item branch.

### [g18] A work-item that awaits an answer keeps its branch
Restates: r26@0.29.
- [r24] When a session ends an `implement` stage for a work-item with a result that is `QUESTION`, `work run` shall keep the work-item branch.

### [g19] An implementer starts on its kept branch
Restates: r58@0.29, r98@0.29.
- [r25] While a work-item branch is kept, when the person runs `work run` on an initiative, `work run` shall start an `implement` stage on the work-item branch.

```given
a work-item branch w2
the work-item branch w2 is kept
```

### [g20] A branch the implementer lost fails the work-item
Restates: r41@0.29.
- [r26] While a work-item branch is lost, when a session ends an `implement` stage for a work-item, `work run` shall set the status of the work-item to `failed`.

```given
a work-item branch w2
the work-item branch w2 is lost
```

### [g21] A flaky scenario is run again before the merge
Restates: r219@0.29, r222@0.29.
- [r27] While a work-item branch is flaky, when a session ends an `implement` stage for a work-item, `work run` shall rerun the scenario.
- [r28] While a work-item branch is flaky, when a session ends an `implement` stage for a work-item, `work run` shall merge the work-item branch.

```given
a work-item branch w2
the work-item branch w2 is flaky
```

### [g22] A worker that changes `.shop/work/` outside its stage directory fails its work-item
Restates: r6@0.29, r34@0.29.
- [r29] While a session is meddling, when the session ends a `research` stage for a work-item, `work run` shall set the status of the work-item to `failed`.
- [r30] While a session is meddling, when the session ends a `research` stage for a work-item, `work run` shall restore the file.

```given
a session s1
the session s1 is meddling
```
### [g23] A change left uncommitted in the checkout fails the work-item
Restates: r218@0.29.
- [r31] While a session is littering, when the session ends a `research` stage for a work-item, `work run` shall set the status of the work-item to `failed`.

```given
a session s1
the session s1 is littering
```
### [g24] Another initiative's changes are left to it
Restates: r214@0.29, r215@0.29, r216@0.29.
- [r32] While a session is crossing, when the session ends a `research` stage for a work-item, `work run` shall start a `plan` stage for the work-item.

```given
a session s1
the session s1 is crossing
```
### [g25] Every transition is committed and pushed
Restates: r7@0.29, r38@0.29.
- [r33] When the person runs `work run` on an initiative, `work run` shall commit every transition and push the commit.

### [g26] A planner's file set is written into the work-item
Restates: r31@0.29.
- [r34] When a session ends a `plan` stage for a work-item with a result that is `DONE`, `work run` shall give the work-item the file set.

### [g27] `work run` exits successfully when the initiative's work is closed
Restates: r212@0.29.
- [r35] While a work-item is closed, when the person runs `work run` on an initiative, `work run` shall exit successfully.
- [r36] While a work-item is closed, when the person runs `work run` on an initiative, `work run` shall print the status of the work-item.

```given
a work-item w1 that is `green`
```

### [g28] `work run` exits with an error while a work-item awaits an answer
Restates: r184@0.29.
- [r37] While a work-item is `awaiting-answer`, when the person runs `work run` on an initiative, `work run` shall exit with an error naming the work-item.

```given
a work-item w1 that is `awaiting-answer`
```

### [g29] `work run` exits with an error while a failed work-item is left
Restates: r52@0.29, r37@0.29.
- [r38] While a work-item is `failed`, when the person runs `work run` on an initiative, `work run` shall exit with an error naming the work-item.
- [r39] While a work-item is `failed`, when the person runs `work run` on an initiative, `work run` shall not start a stage for the work-item.

```given
a work-item w1 that is `failed`
```

### [g30] `work run` exits with an error while a request is in its asker's turn
Restates: r101@0.29.
- [r40] While a request is `asker`, when the person runs `work run` on an initiative, `work run` shall exit with an error naming the request.

```given
a request q1 that is `asker`
```

### [g31] `work run` with no initiative takes every open initiative
Restates: r66@0.29, r82@0.29.
- [r41] When the person runs `work run`, `work run` shall take every open initiative.
- [r42] When the person runs `work run`, `work run` shall exit successfully.

### [g32] `work run` with no initiative exits with an error while a node awaits an answer
Restates: r81@0.29.
- [r43] While a work-item is `awaiting-answer`, when the person runs `work run`, `work run` shall exit with an error naming the initiative.

```given
a work-item w1 that is `awaiting-answer`
an initiative i1
```

### [g33] An initiative branch ahead of its remote is pushed first
Restates: r54@0.29.
- [r44] While an initiative branch is ahead, when the person runs `work run` on an initiative, `work run` shall push the initiative branch.

```given
an initiative branch i2
the initiative branch i2 is ahead
```

### [g34] A remote that refuses the push fails the work-item before its worker starts
Restates: r35@0.29, r39@0.29.
- [r45] While a work-item is `drafted` and a remote is unpushable, when the person runs `work run` on an initiative, `work run` shall set the status of the work-item to `failed`.
- [r46] While a work-item is `drafted` and a remote is unpushable, when the person runs `work run` on an initiative, `work run` shall not start a stage for the work-item.

```given
a work-item w1 that is `drafted`
a remote r1
the remote r1 is unpushable
```

### [g35] A remote that refuses the push starts no branch review
Restates: r51@0.29, r53@0.29.
- [r47] While a work-item is `green` and a remote is unpushable, when the person runs `work run` on an initiative, `work run` shall not start a `branch review` stage for the initiative.
- [r48] While a work-item is `green` and a remote is unpushable, when the person runs `work run` on an initiative, `work run` shall exit with an error naming the remote.

```given
a work-item w1 that is `green`
a remote r1
the remote r1 is unpushable
```

### [g36] `work run` refuses while `.shop/work/` has uncommitted changes
Restates: r46@0.29.
- [r49] While a file is dirty, if the person runs `work run` on an initiative, then `work run` shall exit with an error naming the file and change nothing.

```given
a file `.shop/work/i1/notes.md`
the file `.shop/work/i1/notes.md` is dirty
```

### [g37] `work run` refuses to be started by a worker
Restates: r21@0.29.
- [r50] If a worker runs `work run`, then `work run` shall exit with an error naming the worker and change nothing.

### [g38] `work run` refuses a delivery it cannot start
Restates: r10@0.29.
- [r51] While an initiative branch is gitless, if the person runs `work run` on an initiative, then `work run` shall exit with an error naming the reason and change nothing.

```given
an initiative branch i2
the initiative branch i2 is gitless
```

### [g39] A work-item awaiting an answer gets no worker
Restates: r37@0.29.
- [r52] While a work-item is `awaiting-answer`, when the person runs `work run` on an initiative, `work run` shall not start a stage for the work-item.

```given
a work-item w1 that is `awaiting-answer`
```

### [g40] A work-item blocked by an unfinished work-item gets no worker
Restates: r63@0.29.
- [r53] While a work-item is `drafted`, when the person runs `work run` on an initiative, `work run` shall not start a stage for the work-item.

```given
a work-item w2 that is `awaiting-answer`
a work-item w1 that is `drafted`
the work-item w1 is blocked by the work-item w2
```

### [g41] A green initiative branch gets a branch review
Restates: r27@0.29, r110@0.29, r154@0.29, r155@0.29, r156@0.29, r157@0.29, r47@0.29, r48@0.29, r49@0.29.
- [r54] While a work-item is `green`, when the person runs `work run` on an initiative, `work run` shall start a `branch review` stage for the initiative.
- [r55] While a work-item is `green`, when the person runs `work run` on an initiative, `work run` shall give the `branch review` stage a review brief.
- [r56] While a work-item is `green`, when the person runs `work run` on an initiative, `work run` shall commit the `branch review` stage and push the commit.
- [r57] While a work-item is `green`, when the person runs `work run` on an initiative, `work run` shall log the `branch review` stage.

```given
a work-item w1 that is `green`
```

### [g42] A branch read by a kept review gets no branch review
Restates: r50@0.29.
- [r58] While a work-item is `green` and an initiative branch is reviewed, when the person runs `work run` on an initiative, `work run` shall not start a `branch review` stage for the initiative.

```given
a work-item w1 that is `green`
an initiative branch i2
the initiative branch i2 is reviewed
```

### [g43] An initiative with no work-item is neither reviewed nor measured
Restates: r94@0.29, r97@0.29.
- [r59] While an initiative is itemless, when the person runs `work run` on the initiative, `work run` shall not start a `branch review` stage for the initiative.
- [r60] While an initiative is itemless, when the person runs `work run` on the initiative, `work run` shall not start an `analysis` stage for the initiative.

```given
an initiative i1
the initiative i1 is itemless
```
### [g44] A branch review's findings to fix now get a work-item
Restates: r74@0.29.
- [r61] While a result is fixing, when a session ends a `branch review` stage for an initiative with the result, `work run` shall draft a work-item.

```given
a result r1
the result r1 is fixing
```
### [g45] A branch review that lists nothing to fix is followed by the analysis
Restates: r121@0.29, r75@0.29, r76@0.29, r106@0.29.
- [r62] When a session ends a `branch review` stage for an initiative with a result that is `DONE`, `work run` shall not draft a work-item.
- [r63] When a session ends a `branch review` stage for an initiative with a result that is `DONE`, `work run` shall start an `analysis` stage for the initiative.
- [r64] When a session ends a `branch review` stage for an initiative with a result that is `DONE`, `work run` shall commit a measurement and push the commit.

### [g46] An initiative whose delivery is closed is set done
Restates: r213@0.29, r109@0.29, r111@0.29.
- [r65] While a work-item is `green` and a capability-proposal is `formulated`, when the person runs `work run` on an initiative, `work run` shall set the status of the initiative to `done`.
- [r66] While a work-item is `green` and a capability-proposal is `formulated`, when the person runs `work run` on an initiative, `work run` shall commit the initiative and push the commit.

```given
a work-item w1 that is `green`
a capability-proposal p1 that is `formulated`
```

### [g47] An initiative that changes only the glossary is set done
Restates: r161@0.29.
- [r67] While a glossary-proposal is `approved`, when the person runs `work run` on an initiative, `work run` shall set the status of the initiative to `done`.

```given
a glossary-proposal p1 that is `approved`
```

### [g48] Under a delegation, a question goes to a session of its own
Restates: r210@0.29, r211@0.29, r78@0.29.
- [r68] While a delegation is `written`, when a session ends a `plan` stage for a work-item with a result that is `QUESTION`, `work run` shall start an `answer` stage for the question.
- [r69] While a delegation is `written`, when a session ends a `plan` stage for a work-item with a result that is `QUESTION`, `work run` shall name the delegation.

```given
a delegation d1 that is `written`
```

### [g49] Under a delegation, a glossary-proposal's question is left for the person
Restates: r209@0.29.
- [r70] While a delegation is `written`, when a session ends a `gate` stage for a glossary-proposal with a result that is `QUESTION`, `work run` shall not start an `answer` stage for the question.
- [r71] While a delegation is `written`, when a session ends a `gate` stage for a glossary-proposal with a result that is `QUESTION`, `work run` shall set the status of the glossary-proposal to `awaiting-answer`.

```given
a delegation d1 that is `written`
```

### [g50] Under a delegation, an answer asking for a change makes the work-item ready
Restates: r118@0.29, r120@0.29.
- [r72] While a delegation is `written` and an answer is `--change`, when a session ends a `review` stage for a work-item with a result that is `QUESTION`, `work run` shall start an `implement` stage for the work-item.

```given
a delegation d1 that is `written`
an answer a1 that is `--change`
```

### [g51] Under a delegation, an answer accepting the work-item makes it done
Restates: r119@0.29, r120@0.29.
- [r73] While a delegation is `written` and an answer is `--accept`, when a session ends a `review` stage for a work-item with a result that is `QUESTION`, `work run` shall set the status of the work-item to `green`.

```given
a delegation d1 that is `written`
an answer a1 that is `--accept`
```

### [g52] Under a delegation, a faulty answering session leaves the question for the person
Restates: r89@0.29, r90@0.29.
- [r74] While a delegation is `written` and a session is faulty, when the session ends an `answer` stage for a question on a work-item, `work run` shall set the status of the work-item to `awaiting-answer`.
- [r75] While a delegation is `written` and a session is faulty, when the session ends an `answer` stage for a question on a work-item, `work run` shall commit the `answer` stage and push the commit.

```given
a session s1
the session s1 is faulty
a delegation d1 that is `written`
```

### [g53] A request this context is the upstream of gets an intake round
Restates: r67@0.29.
- [r76] While a request is `open`, when the person runs `work run`, `work run` shall start an `intake` stage for the request.

```given
a request q1 that is `open`
```

### [g54] An intake round's question is written in the request
Restates: r100@0.29, r134@0.29.
- [r77] When a session ends an `intake` stage for a request with a result that is `QUESTION`, `work run` shall ask a question on the request.
- [r78] When a session ends an `intake` stage for a request with a result that is `QUESTION`, `work run` shall set the status of the request to `awaiting-asker`.

### [g55] An accepted request gets its initiative
Restates: r103@0.29.
- [r79] While a request is `accepted`, when the person runs `work run`, `work run` shall start an initiative that fulfils the request.

```given
a request q1 that is `accepted`
```

### [g56] A proposed initiative gets an integrate round
Restates: r79@0.29, r84@0.29, r141@0.29, r102@0.29.
- [r80] When the person runs `work run` on an initiative that is `proposed`, `work run` shall start an `integrate` stage for the initiative.
- [r81] When the person runs `work run` on an initiative that is `proposed`, `work run` shall give the `integrate` stage a round brief.
- [r82] When the person runs `work run` on an initiative that is `proposed`, `work run` shall set the status of the initiative to `started`.

```given
an initiative i1 that is `proposed`
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
```
### [g57] A started initiative with nothing drafted gets an integrate round
Restates: r180@0.29.
- [r83] While an initiative is bare, when the person runs `work run` on the initiative, `work run` shall start an `integrate` stage for the initiative.

```given
an initiative i1 that is `started`
the initiative i1 is bare
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
```
### [g58] An integrate round with no change list ends `work run` with an error
Restates: r96@0.29.
- [r84] While a result is listless, when a session ends an `integrate` stage for an initiative with the result, `work run` shall exit with an error naming the stage.

```given
an initiative i1
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
a result r1
the result r1 is listless
```
### [g59] An integrate round's change list drafts a capability-proposal
Restates: r159@0.29, r91@0.29.
- [r85] When a session ends an `integrate` stage for an initiative with a result that is `DONE`, `work run` shall draft a capability-proposal.
- [r86] When a session ends an `integrate` stage for an initiative with a result that is `DONE`, `work run` shall commit every draft and push the commit.

```given
an initiative i1
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
```
### [g60] An integrate round's change to the glossary drafts a glossary-proposal
Restates: r171@0.29, spec-integration#r54@0.29.
- [r87] While a result is glossarial, when a session ends an `integrate` stage for an initiative with the result, `work run` shall draft a glossary-proposal.

```given
an initiative i1
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
a result r1
the result r1 is glossarial
```
### [g61] An integrate round's lines into an upstream are raised
Restates: r135@0.29, spec-integration#r44@0.29.
- [r88] While a result is raising, when a session ends an `integrate` stage for an initiative with the result, `work run` shall raise a request.

```given
an initiative i1
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
a result r1
the result r1 is raising
```
### [g62] A proposal whose raised request is not delivered gets no work-item
Restates: r136@0.29.
- [r89] While a capability-proposal is `formulated` and the capability-proposal is held, when the person runs `work run` on an initiative, `work run` shall not draft a work-item.

```given
a capability-proposal p1 that is `formulated`
the capability-proposal p1 is held
a request q1 that is `open`
```

### [g63] A change list naming an unknown capability ends `work run` with an error
Restates: r107@0.29.
- [r90] While a result is strange, when a session ends an `integrate` stage for an initiative with the result, `work run` shall not draft a capability-proposal.
- [r91] While a result is strange, when a session ends an `integrate` stage for an initiative with the result, `work run` shall exit with an error naming the capability.

```given
an initiative i1
a request q1 that is `accepted`
the initiative i1 fulfils the request q1
a result r1
the result r1 is strange
```
### [g64] Drafts that do not parse are sent back, then asked about
- [r92] While a result is unparsing, when a session ends an `integrate` stage for a capability-proposal with the result, `work run` shall start an `integrate` stage for the capability-proposal.
- [r93] While a result is unparsing, when a session ends an `integrate` stage for a capability-proposal with the result, `work run` shall set the status of the capability-proposal to `awaiting-answer`.

```given
a result r1
the result r1 is unparsing
```
### [g65] A redrafted capability-proposal is drafted again
Restates: r142@0.29, r143@0.29, r148@0.29, r187@0.29, r188@0.29, spec-integration#r45@0.29.
- [r94] When a session ends an `integrate` stage for a capability-proposal with a result that is `DONE`, `work run` shall set the status of the capability-proposal to `drafted`.
- [r95] When a session ends an `integrate` stage for a capability-proposal with a result that is `DONE`, `work run` shall not draft a capability-proposal.

### [g66] A redrafted glossary-proposal is drafted again
Restates: r189@0.29.
- [r96] When a session ends an `integrate` stage for a glossary-proposal with a result that is `DONE`, `work run` shall set the status of the glossary-proposal to `drafted`.

### [g67] A drafted capability-proposal gets a gate round
Restates: r68@0.29, r168@0.29, r108@0.29.
- [r97] While a capability-proposal is `drafted`, when the person runs `work run` on an initiative, `work run` shall start a `gate` stage for the capability-proposal.
- [r98] While a capability-proposal is `drafted`, when the person runs `work run` on an initiative, `work run` shall give the `gate` stage a round brief.

```given
a capability-proposal p1 that is `drafted`
```

### [g68] A drafted glossary-proposal gets a gate round
Restates: r164@0.29, r170@0.29.
- [r99] While a glossary-proposal is `drafted`, when the person runs `work run` on an initiative, `work run` shall start a `gate` stage for the glossary-proposal.
- [r100] While a glossary-proposal is `drafted`, when the person runs `work run` on an initiative, `work run` shall give the `gate` stage a round brief.

```given
a glossary-proposal p1 that is `drafted`
```

### [g69] A gate round's questions make the capability-proposal await an answer
Restates: r85@0.29, r69@0.29.
- [r101] When a session ends a `gate` stage for a capability-proposal with a result that is `QUESTION`, `work run` shall set the status of the capability-proposal to `awaiting-answer`.
- [r102] When a session ends a `gate` stage for a capability-proposal with a result that is `QUESTION`, `work run` shall ask a question on the capability-proposal.

### [g70] A gate round with no question asks for the approval of the lines
Restates: r117@0.29.
- [r103] When a session ends a `gate` stage for a capability-proposal with a result that is `DONE`, `work run` shall ask a question on the capability-proposal.

### [g71] A gate round with no question asks for the approval of the terms
Restates: r169@0.29, r173@0.29.
- [r104] When a session ends a `gate` stage for a glossary-proposal with a result that is `DONE`, `work run` shall set the status of the glossary-proposal to `awaiting-answer`.
- [r105] When a session ends a `gate` stage for a glossary-proposal with a result that is `DONE`, `work run` shall ask a question on the glossary-proposal.

### [g72] An answered capability-proposal gets an apply round
Restates: r70@0.29, r108@0.29.
- [r106] While a capability-proposal is answered, when the person runs `work run` on an initiative, `work run` shall start an `apply` stage for the capability-proposal.
- [r107] While a capability-proposal is answered, when the person runs `work run` on an initiative, `work run` shall give the `apply` stage a round brief.

```given
a capability-proposal p1 that is `awaiting-answer`
the capability-proposal p1 is answered
```

### [g73] An answered glossary-proposal gets an apply round
Restates: r165@0.29, r170@0.29.
- [r108] While a glossary-proposal is answered, when the person runs `work run` on an initiative, `work run` shall start an `apply` stage for the glossary-proposal.

```given
a glossary-proposal p1 that is `awaiting-answer`
the glossary-proposal p1 is answered
```

### [g74] A glossary-proposal with a question unanswered gets no apply round
Restates: r172@0.29, spec-integration#r55@0.29.
- [r109] While a glossary-proposal is not answered, when the person runs `work run` on an initiative, `work run` shall not start an `apply` stage for the glossary-proposal.

```given
a glossary-proposal p1 that is `awaiting-answer`
the glossary-proposal p1 is not answered
```

### [g75] An apply round's answers its drafts do not hold go back to integration
Restates: r150@0.29, r151@0.29, r147@0.29, spec-integration#r46@0.29.
- [r110] While a result is unheld, when a session ends an `apply` stage for a capability-proposal with the result, `work run` shall start an `integrate` stage for the capability-proposal.
- [r111] While a result is unheld, when a session ends an `apply` stage for a capability-proposal with the result, `work run` shall not start a `formulate` stage for the capability-proposal.

```given
a result r1
the result r1 is unheld
```
### [g76] A glossary apply round's answers its drafts do not hold go back to integration
Restates: r221@0.29.
- [r112] While a result is unheld, when a session ends an `apply` stage for a glossary-proposal with the result, `work run` shall start an `integrate` stage for the glossary-proposal.

```given
a result r1
the result r1 is unheld
```
### [g77] An applied glossary-proposal is approved
Restates: r166@0.29, r167@0.29.
- [r113] When a session ends an `apply` stage for a glossary-proposal with a result that is `DONE`, `work run` shall set the status of the glossary-proposal to `approved`.
- [r114] When a session ends an `apply` stage for a glossary-proposal with a result that is `DONE`, `work run` shall not start a `formulate` stage for the glossary-proposal.

### [g78] An applied capability-proposal is formulated by `features generate`
Restates: r144@0.29, r145@0.29, r146@0.29, r83@0.29, formulation#r1@0.29, formulation#r2@0.29, formulation#r6@0.29, formulation#r7@0.29, formulation#r11@0.29.
- [r115] While a change list is codified, when a session ends an `apply` stage for a capability-proposal with a result that is `DONE`, `work run` shall start a `formulate` stage for the capability-proposal.
- [r116] While a change list is codified, when a session ends an `apply` stage for a capability-proposal with a result that is `DONE`, `work run` shall set the status of the capability-proposal to `formulated`.
- [r117] While a change list is codified, when a session ends an `apply` stage for a capability-proposal with a result that is `DONE`, `work run` shall commit the feature and push the commit.

```given
a change list c1
the change list c1 is codified
```

### [g79] A capability that is not codified is the formulate round's fault
Restates: formulation#r22@0.29.
- [r118] While a change list is uncodified, when a session ends an `apply` stage for a capability-proposal with a result that is `DONE`, `work run` shall set the status of the capability-proposal to `approved`.
- [r119] While a change list is uncodified, when a session ends an `apply` stage for a capability-proposal with a result that is `DONE`, `work run` shall exit with an error naming the capability.

```given
a change list c1
the change list c1 is uncodified
```

### [g80] A faulty round makes no transition and the initiative's other nodes go on
Restates: r86@0.29, r87@0.29, r88@0.29, r115@0.29.
- [r120] While a session is faulty, when the session ends a `gate` stage for a capability-proposal, `work run` shall set the status of the capability-proposal to `drafted`.
- [r121] While a session is faulty, when the session ends a `gate` stage for a capability-proposal, `work run` shall exit with an error naming the stage.
- [r122] While a session is faulty, when the session ends a `gate` stage for a capability-proposal, `work run` shall set the status of every open work-item to `green`.

```given
a session s1
the session s1 is faulty
```
### [g81] A formulated capability-proposal gets its work-items
Restates: r72@0.29.
- [r123] While a capability-proposal is `formulated` and the capability-proposal is not held, when the person runs `work run` on an initiative, `work run` shall draft a work-item.

```given
a capability-proposal p1 that is `formulated`
the capability-proposal p1 is not held
```

### [g82] The rounds that change the spec hold the spec lock
Restates: r95@0.29.
- [r124] Every `integrate` stage shall hold the spec lock.
- [r125] Every `apply` stage shall hold the spec lock.
- [r126] Every `formulate` stage shall hold the spec lock.

### [g83] A stage that is no worker's holds its initiative
Restates: r66@0.29.
- [r127] Every `integrate` stage shall hold the initiative lock.
- [r128] Every `gate` stage shall hold the initiative lock.
- [r129] Every `apply` stage shall hold the initiative lock.
- [r130] Every `formulate` stage shall hold the initiative lock.
- [r131] Every `answer` stage shall hold the initiative lock.
- [r132] Every `branch review` stage shall hold the initiative lock.
- [r133] Every `analysis` stage shall hold the initiative lock.

### [g84] A worker's stage holds a worker slot
Restates: r20@0.29, r59@0.29, r60@0.29.
- [r134] Every `research` stage shall hold a worker slot.
- [r135] Every `plan` stage shall hold a worker slot.
- [r136] Every `implement` stage shall hold a worker slot.
- [r137] Every `review` stage shall hold a worker slot.

### [g85] An implementer holds the claim of its work-item, and a merge the merge lock
Restates: r20@0.29, r61@0.29.
- [r138] Every `implement` stage shall hold a claim.
- [r139] `work run` shall hold the merge lock.

### [g86] A delivery removes the worktrees it made
Restates: r33@0.29, r23@0.29.
- [r140] When the person runs `work run` on an initiative, `work run` shall remove every worktree.

## Implementation, may change
- The work-item's scenarios and the suite alike run in parallel with pytest-xdist (`-n auto`) (design-decision/plugin-takes-the-dependencies-it-needs).
- A worker is `claude -p "Read the brief file <brief path> and do what it says." --agent shopsystem-bdd:<agent>
  --session-id <uuid> --output-format json --permission-mode acceptEdits`; the executable is `$SHOPSYSTEM_WORK_CLAUDE`, else `claude` (the plugin's tests
  set a stub). The agents of the stages: `code-scout` (research), `bdd-planner` (plan), `bdd-implementer`
  (implement), `bdd-task-reviewer` (review), `bdd-branch-reviewer` (branch review), `initiative-round`
  (`intake`, `integrate`, `gate`, `apply`), `delegation-answerer` (answer) and a session of `analyzing-a-batch`
  (analysis). The `formulate` round is a script with no session (design §13).
- `work run` writes the brief in the worker's worktree, as `.shop/scratch/<k>-<stage>/brief.md`, and the worker writes
  its result and its other files beside it. When the worker ends, `work run` copies that directory into the stage
  directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`, which then holds `brief.md`, `result.json`,
  `session.json` (with the path of the session's transcript) and the worker's notes, plan, report or findings, and
  each file the worker's result names (a field that is a sentence longer than a file name may be names no file). The
  implementer works in `.shop/worktrees/<work-item>/`, on its work-item branch from the initiative branch's head,
  rebased before its scenarios and the suite run. Where the repository is inside the plugin's own directory, each
  worker's worktree is made in a temporary directory outside it. `work run` removes every worktree it made when it
  exits.
- A result's `questions` given as one string is read as one question.
- The transitions from `planned` to `ready` and from `ready` to `claimed` have no guard beyond the lifecycle's.
- Commit message `work: <work-item> <before> -> <after>`. Exit code 0 every work-item `green` or `withdrawn`, 3 awaiting an answer, 1 otherwise.
- The commands for the work-item's scenarios and the suite: `python3 -m pytest -q -p work_items --work-item <name>` (the plugin's `scripts/work_items.py` on `PYTHONPATH`) and `python3 -m pytest -q -rfEx -p work_items --work-item <name> --whole-suite`, `-n auto` where pytest-xdist is there; `.shop/delivery.toml`'s `[tests]` replaces them. Every pytest command `work run` starts, and every worker's (through `PYTEST_ADDOPTS`), is given `--work-item <name>`, which selects the scenarios the work-item accepts: a test that is not a scenario is kept; when it collects scenarios and none that the work-item accepts, it refuses, saying so, unless every requirement the work-item accepts is of a guarantees capability, when it deselects each scenario and a run left with no test exits successfully (`tests/scripts/test_work_items.py`).
- `--whole-suite` keeps every test and marks as xfail each scenario counted as expected: one whose requirement a work-item other than the one being merged accepts that is neither `green` nor `withdrawn`, or a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes (also in the whole-suite run before an implementer starts). A scenario whose failure would keep the merge from happening is run once more, alone; when it fails again, both runs are given in the question written for the work-item.
- A guarantees capability is one whose frontmatter has `group: guarantees` (design-decision/workflow-capabilities-are-guarantees).
- The push is verified by `git push --dry-run` to the initiative branch's upstream remote, else `origin`, before every worker and the branch reviewer start; a repository `work run` delivers has that remote. A fault is recorded under the work-item's `## Faults`. The n-th bullet of `## Answers` answers the n-th of `## Questions`.
- `log.jsonl` also gets a `push verified` line for each push verification, and a `suite` line for each whole-suite run before a merge.
- A failed commit of a fault's transition ends `work run` as a refused delivery does, with an error saying why, not with a traceback.
- The `intake` round writes each line outcome with `work outcome` (requests), which `work` keeps under the request's `## Outcomes` (design-decision/requests-written-through-work); `work run` writes its question with `work`'s question command in the upstream's turn, before the round's `work turn`, and leaves the request's status as `work turn` writes it.
- The `gate` round gives its gate in its `result.json` and writes nothing on the capability-proposal; `work run` writes the questions under the proposal's `## Questions`.
- An answer under a delegation names the delegation in its `by`. The session answering a reviewer's question gives in its result whether its answer asks for a change or accepts the work-item as it is. `work run` reads the delegation the request has when it reads it, given before or after the initiative started.
- A request's asker is this context when its `asker` is `internal` or this context's id; the open questions are every question with no answer under the request's `## Answers`. `work run` exits with an error printing each node awaiting an answer, each request in its asker's turn with its open questions, each failed work-item with its fault, or, started with no initiative, the status of each initiative it took.
- How a run before the branch review exited is given as its exit code. The branch reviewer's directory is copied into `.shop/work/<initiative>/runs/branch-review/<k>/` and committed on the initiative branch.
- A planner's `fileset` is written into the work-item as `fileset:` as it makes the transition to `planned`.
- An `integrate` round started for a capability-proposal adds the round's ids for another capability for which the initiative holds a capability-proposal to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds; a redrafted proposal keeps the ids and terms its round's change list does not name, its earlier drafts kept in their round's directory, and its status is kept while its round runs.
- The `integrate` round's drafts are checked by `work run` itself (design §13): every drafted requirement must parse, and `model logic` on the spec with the drafts must find no L1 or L3. A refused round is sent back with the refusal text, at most twice, and then its proposals each get a question whose answer goes back to integration.
- The `formulate` round runs `features generate` for each service capability of the proposal, then `features generate --check` and `model check` with no row it did not give before, and commits only `features/`; it shows nothing to the person. A guarantees capability is passed over.
- A work-item is drafted for each capability a formulated proposal's `adds` and `changes` name, accepting every requirement they name on that capability; a work-item retiring the scenarios of the proposal's `removes` has the check `python3 -m pytest`. A kept branch review's findings to fix now get one work-item, naming the findings file, under the capability-proposal of the work-item they concern.
- After the branch review that lists nothing to fix now, `work run` runs `measure initiative` and then starts the session of `analyzing-a-batch` that writes the analysis record; both are committed on the initiative branch.
- An initiative is set `done` when it is not `done`, has a `green` work-item, every work-item is `green` or `withdrawn`, every capability-proposal is `formulated` or `withdrawn`, its kept branch review lists nothing to fix now, its measurement and analysis record are committed and every request kept in this context whose asker is this context and that names it is `delivered`; or when it changes only the glossary, its glossary-proposal is `approved` and its terms are committed to `spec/index.md`.

## Not yet
- Retries, refused claims, the guards between work-items, fix work-items and re-reviews, time and spending limits and
  budgets, the lock, interruption, `work step`, and the full log of each session's cost (see skeleton-notes.md).
- A researcher's findings kept when it stops, for the next delivery (i8, delivery 1).

## Dropped
- r42@0.29: restated U6 (a stage that ends with no result is discarded: its work-item becomes `failed`).
- r22@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r55@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r56@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r64@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r65@0.29: the `--work-item` option of the pytest plugin, moved to Implementation; tested by `tests/scripts/test_work_items.py`.
- r29@0.29: `.shop/delivery.toml`'s `[tests]`, moved to Implementation; every scenario's repository runs its tests through it.
- r43@0.29: what the suite counts as expected to fail, and the question with both runs of a failing scenario, moved to Implementation; tested by `tests/scripts/test_work_items.py` and `tests/scripts/test_supervise*.py`.
- r122@0.29: what the suite counts as expected to fail, and the question with both runs of a failing scenario, moved to Implementation; tested by `tests/scripts/test_work_items.py` and `tests/scripts/test_supervise*.py`.
- r220@0.29: what the suite counts as expected to fail, and the question with both runs of a failing scenario, moved to Implementation; tested by `tests/scripts/test_work_items.py` and `tests/scripts/test_supervise*.py`.
- r73@0.29: deprecated scenarios are gone (design §14: the generator owns the feature files); a work-item retiring scenarios comes from the proposal's `removes`.
- r123@0.29: deprecated scenarios are gone (design §14: the generator owns the feature files); a work-item retiring scenarios comes from the proposal's `removes`.
- r124@0.29: deprecated scenarios are gone (design §14: the generator owns the feature files); a work-item retiring scenarios comes from the proposal's `removes`.
- r116@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r186@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r152@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
- r153@0.29: the `formulate` round is a script and gives no question, and a formulation that formulates nothing is gone (design §13.1).
