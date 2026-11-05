---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# The workflow simplified: one item, a backlog, batches, one review at the PR (design, 2026-11-04)

This design comes from a brainstorming conversation on 2026-11-04 between the person and a session. The figures behind
it are in `recon.md` in this folder. It builds on `../2026-10-30-backlog-board-design.md` (the board), which was
designed but never built, and on the codified-requirements work on branch `gf-conversion`
(`../2026-11-03-gf-conversion/`).

## Intent and the why

The GF conversion was built with superpowers' process in place of the plugin's. It cost $150 over 6.4 h, unattended,
with no questions to the person. The same work through `work run` was estimated at $292-$1,682, with 100-1,180 rulings
by the person. The person, 2026-11-04: "Pretty much from the start, superpowers was much faster than the
request/initiative/work-item process. There is a lot of overhead involved now with all of the phases."

The measurements agree (`recon.md`):

- **Gates:** an initiative holds 15-104 min of session time but stays open 18-119 h, waiting on question gates.
- **Task reviews:** the per-task reviewer is the largest single cost (23%), and 28 of its 38 reviews found nothing to
  fix now.
- **Defects:** the defects the superpowers-built work did have were spec and design problems, found after a larger body
  of work existed. Per-stage code review would not have caught them.

The aim is to keep what the plugin does that superpowers does not, and to drop the orchestration between them:

- **Keep:** codified requirements and generated scenarios, traceability, work from other contexts, the checks that
  catch things, a backlog, telemetry, decisions.
- **Drop:** the stages, proposals, gates and per-stage reviews.

## What the person wants kept

In their words, 2026-11-04:

- "The requirements and scenarios handling. With the recent shift to grammaticalframework, there is no formulation
  step."
- "the traceability chain that links work to where it came from"
- "the ability to handle work from outside the bounded context from peer BCs or an overall product system."
- "some of the checks and validation are useful and catch things"
- A backlog, "also something missing from superpowers. This would also require being able to work across sessions."
- Telemetry: "it has been very useful to have time/cost information to analyze."

## Goals

### 1. One kind of top-level item

Request, initiative and capability-proposal become one kind: an **item**. Work-items stop being records the person sees
(goal 5). The person: "maybe a single item type for the top level in different states would be better", and "there
should only be one top level request or initiative and then trees of work-items that handle dependency and ordering".

- **Its states** are the board's stages, renamed to say what they mean:
  - **idea**: raw, possibly one line;
  - **shaped**: has context to work from without the person, such as a note from a brainstorming or a write-up of a
    bug;
  - **ready**: passes the readiness bar (goal 3);
  - **in batch**: being built;
  - **delivered**: merged.
  - **Off the main line:** **needs input** (parked with its question), **refused** and **withdrawn**.
- **Origin is a property, not a type:** this context, a named peer context, or the product system. The person: "It is
  important to differentiate work comes from, but that could also be a state or a property."
- **The thread back to where it came from:**
  - An item's requirement lines carry its id, and its batch, PR and commits name it. This is the traceability chain.
  - Its source (a conversation, a peer's request, an observation) is linked from the item (goal 9).

### 2. A backlog across sessions

- **Where it lives:** items are kept in the repository, so any session can read or change them.
- **Ranking:** order is the board's WSJF, as the person decided on 2026-10-30. Value, urgency and size are each low,
  medium or high (L=1, M=2, H=3). The score is (value + urgency) / size, and ties go to the item added first.
- **Bugs** add risk and likelihood. The session gives first ratings with reasons, and the person corrects them.
- **Dependencies:** an item may depend on other items. It is never put in a batch while something it depends on is not
  delivered, unless that item is in the same batch.
- **The view:** one command prints the backlog as tables by state, in rank order. Each row shows the item's name, origin,
  ratings and blockers, and for an item in a batch, how far the batch is along. The person: "I want to see progress
  happening in the system but I don't care how it gets broken down into implementation work as long as I can understand
  what is being worked on from the backlog and how far it is from being done."

### 3. Questions move to the front: a readiness bar

There are no question gates during building. The person: "The current system has so many question gates and that should
go", and "another balance to be struck is the minimum quality of the input to allow autonomous execution".

- **The bar:** an item becomes **ready** only when it passes a mechanical check, and most of that check already exists:
  - its requirement lines parse in the context's grammar;
  - `model logic` reports no L1 or L0 for them over the spec with the lines laid in;
  - `features generate` writes their scenarios;
  - the tier-1 decision checks (goal 7) hold for any constraint the item states.
- **Tunable:** where the bar sits is tuned against the goals of goal 8.
- **A question while building:** it parks the item as **needs input** with the question on its row, and the item goes
  back to intake. The rest of the batch carries on.

### 4. Two ways in

- **Brainstorming with the person:** a conversation like the one this design came from. It ends in shaped items whose
  requirement lines can be checked against the bar, not in a long design document. For larger work a design record is
  still written.
- **Negotiation with another system:** a peer context or the product system proposes lines. This context answers each
  one: accept, refuse with a reason, or counter-propose. The exchange repeats until the item is ready or refused, with no
  person in the loop unless the two sides cannot agree. The person: "a negotiation with another system as opposed to a
  human." Today's request, reply and outcome commands are the starting point, slimmed down.

### 5. Batches, like a sprint

- **Picking:** a batch takes several ready, unblocked items in rank order, which may be unrelated, and builds them
  together. The person: "Is it possible to have possibly disparate work done together in batches much the way that a dev
  team will pick stories to do in sprints? It's almost like the superpowers execution model mixed with the requirements
  and request model."
- **Inside a batch:**
  - The batch writes its own plan. The tasks in it are internal and disposable, never backlog entries.
  - Tasks run in parallel where they are independent, through worktrees and subagents, as superpowers'
    subagent-driven development and workflows do.
  - Each item's generated scenarios are the batch's acceptance tests.
- **Bounded sessions:** the batch's plan and each task's status are written to disk, so a session can stop and any
  later session can carry on. The person: "I do want to figure out if things can be bounded so that they aren't
  required to be in the same session."
- **One batch is one branch and one PR.**

### 6. One adversarial review, at the PR

- **One review per batch:** there is no review after each stage or task. The batch's PR gets one adversarial review.
  The person: "it's almost faster to find them after a larger amount of implementation and refactor to correct rather
  than reviewing every single implementation stage", and "Maybe it makes sense to have the review at the PR level and
  the system can create feedback loops there on both the implementation correctness as well as providing feedback on
  engineering quality in terms of coding standards and change/PR size."
- **What it checks:**
  - **correctness against the items' requirements;**
  - **engineering quality:** the repository's standards, the tier-3 decisions (goal 7), and the size of the change.
- **Range:** the review reads only the batch's own commits, from the branch's base to its head, and none of `main`.
- **Fixes:** fix-now findings are fixed on the same branch, and the review re-reads only what the fix touched.
- **Findings feed back:** they are recorded with their grade. Findings that keep recurring are a signal for a new
  decision, a new check, or a higher readiness bar.

### 7. Decisions in three tiers

Decisions return. The person: "Another thing that is missing is decisions. The system stopped generating new decisions
at some point. These are important, but the types of decisions should be shifted."

- **Tier 1, checkable.** For example "python will be used as the implementation language", the 300-line limit, and
  import rules. Each names the check that enforces it, and the check runs with the suite and at the PR.
- **Tier 2, a requirement.** Behaviour and contracts are written as requirement lines in the spec, with generated
  scenarios.
- **Tier 3, judgement.** Code patterns and design choices. The person: "How do you test if a pattern should have been
  used but has not been? This should be taken into account during implementation, though." These go to the batch's
  plan as context, and the PR review checks the change against them.

A decision record is short: what was decided, its tier, and for tiers 1 and 2 the check or requirement that enforces it.
The 72 existing decisions are sorted into the tiers once. Superseded ones are marked superseded, and obsolete ones are
retired.

### 8. Telemetry and tuning

- **What `measure` records:** for each batch, wall time, session time, tokens and cost by role (planning, implementing,
  review, fixing). It also records defects: those the PR review found, and those found after merge, each traced to its
  item.
- **Goals in tension:** the system's goals are stated as figures that pull against each other: wall time, token cost
  and defect rate. The person: "All of these things should be tuned over time through some overall goals/metrics
  balanced against each other, like wall-time, token cost, defect rates, etc."
- **The knobs:** batch size, review depth, and the readiness bar. A change to a knob is made as a decision, with the
  figures before and after.

### 9. Conversation context behind a quote

A quoted statement from the person links to the conversation it came from, and the turns around it can be shown: the
person's and the session's words, without tool output. The person: "Quoting the user is important, but I would
appreciate being able to see the conversation context around a statement. This is more about conversation turns than a
full transcript with tool output."

### 10. Names, not opaque ids, for the person

The person reads names, not `i39`, `w212` or `r135`. The ids stay in files for the tools. The person: "I don't like how
the current system consistently uses opaque ids to refer to things in the system, but that could probably be handled by
a hook rather than wasting tokens."

## Non-goals

- **Slices or jobs-to-be-done** at this level. The person: "Lets leave slices out of this for now. It doesn't seem
  useful at the bounded context level we're working at." The backlog is flat. Ordering comes from dependencies and rank.
- **Translating the old queue.** The 64 initiatives, 246 work-items and 47 requests are not converted (see Migration).
- **A browser board or a TUI**: tables in the session only, as the board design decided.
- **The log of temporary rules** from q31 stays out, as in the board design.

## Anti-goals

- **Question gates come back** in another form, for example a batch that waits on a person.
- **Per-stage or per-task review returns** as a default.
- **New artifact kinds multiply.** The person sees items, batches, PRs and decisions, and nothing else.
- **A backlog that is just the queue again:** adding an idea must not start work.
- **Opaque ids shown to the person.**
- **Checks kept because they exist.** Each check left after the change has caught something, or enforces a decision.

## Constraints

- **The repository's rules:** the 300-line limit on Python files and the module map (`CLAUDE.md`) hold.
- **Retire, never edit:** spec lines are never edited, only retired and replaced. The supervision, work-queue and
  requests capabilities' lines for the old process are retired, not rewritten.
- **State in the repository:** what the plugin keeps is kept in the repository.
- **Order of work:** the plan is written after `gf-conversion` has merged to `main`, because the readiness bar is the
  grammar, the logic check and the generator.
- **How it is built:** with superpowers' process (a plan, then subagent-driven development and workflows), not through
  `work run`, so the old machinery is never in the way.

## What is kept and what goes

**Kept:**

- **The requirements stack:** `grammar/`, `scripts/spec_*`, `features generate` and the vocabulary,
  `tests/scenarios/vocab.py` and the world handlers.
- **`model logic`.**
- **`model check`, trimmed** to its rules about the spec and items.
- **The code tools:** `tools` (size, check, refs, map) and `features`.
- **`measure`**, repointed to batches.
- **The `migrate upgrade` framework**, for this release's step.
- **The hooks**, rewritten for goals 9 and 10.
- **Kept only where simpler than superpowers':** the log, request/reply/outcome, and the worktree and merge plumbing of
  `scripts/supervise_*`.

**Goes:**

- **The stage pipeline:** the integrate, gate, apply and formulate rounds, and research, plan, implement and task
  review per work-item, with their briefs and result files.
- **Capability-proposals and glossary-proposals.**
- **Delegations and question gates.**
- **The agents built for the old stages:** code-scout, bdd-planner, bdd-task-reviewer, initiative-round,
  capability-writer, feature-formulator, spec-checker and delegation-answerer, with the skills that only drive them.

## Migration

This is a new major version of this plugin, in this repository.

- **The old queue:** `.shop/work/` is frozen as read-only history, kept for tracing why, never translated. Its open
  work is entered again by hand as backlog items: the open requests, the deferred i39 work, and the board design's own
  items.
- **The old capabilities:** their requirements are retired in bulk under one decision.
- **Upgrade:** repositories using the plugin get a `migrate upgrade` step that freezes their queue the same way.

## Decided by the person after the builder check (2026-11-04)

- **Who writes the lines.** The session writes an item's requirement lines, in a brainstorming or at intake. An item
  whose lines pass the bar is ready. The person sees the lines in the backlog and in the PR and may skim them, but
  nothing waits on the person's reading.
- **The merge.** The system opens the batch's PR on GitHub and runs the review and fix loop. When no fix-now finding is
  left, it marks the PR ready. The person merges. This is the one place the person is needed, and it comes at the end.
  The item becomes delivered at the merge.
- **The new workflow is itself codified.** Its capabilities (item, backlog, batch, intake and negotiation, readiness,
  PR review, decisions, telemetry) are written as requirement lines in `spec/`, logic-checked, with generated scenarios
  as their tests. The old capabilities' lines are retired as they are replaced. The plan's first phase is therefore
  writing and checking those lines, and extending the lexicon, grammar or step vocabulary where they need it.
- **Conversation turns are committed.** For each quote, a few turns around it are copied into `.shop/` and committed:
  the person's and the session's words, with no tool output. This lets any clone or session show the context. The
  quote keeps its session id and turn as well.

## The session's calls (not agreed by the person)

- **One batch is one branch and one PR.**
- **The readiness bar** is mechanical only, at the start.
- **State names:** the board's five stages kept, under the names idea, shaped, ready, in batch and delivered.
- **The middle-path migration:** freeze the queue, do not translate it. It was recommended to the person, who did not
  object and asked what would be kept.
- **PR review fixes** happen on the batch's branch, and the review re-reads only what the fix touched.
- **Knob changes** are recorded as decisions.
- **Where a ready item's lines live:** they stay on the item until its batch merges, and are checked by laying them over
  `spec/` the way drafts are laid over it today (`spec_context`). The bar is checked again when a batch picks the item,
  against `main` as it then stands, together with the other items in the batch. An item that fails that check goes back
  to shaped. The lines enter `spec/` with the batch's merge.
- **Keeping items separable in a batch:** a batch keeps each item's commits apart (one worktree or one commit series per
  item, merged into the batch branch). An item parked as needs input mid-batch has its commits left out of the PR and
  kept on its own branch for when it returns.
- **Who answers a peer:** a peer's lines are answered by a session started when the backlog command runs intake, as
  today's intake rounds are, with no person in it. No compatibility layer is kept for peers on 1.x; the repositories of
  the product upgrade together.
- **The Kept list is a ceiling, not a floor:** the builder may drop more of it where superpowers' process already
  covers the need, as long as goals 1-10 still hold.

## Left to the builder

- **Formats and commands:** the item file format, the backlog and batch commands, and how a batch is started and how it
  resumes.
- **The review:** how the PR review is run (agent or skill), and its prompt.
- **The hooks:** how the id-expanding hook works, and how the conversation hook stores the session and turn of a quote.
- **The decisions' first sort:** which of the 72 land in which tier.
- **`model check`:** which of its rules survive.
- **Superpowers:** how much is reused from it, and how much reimplemented.
