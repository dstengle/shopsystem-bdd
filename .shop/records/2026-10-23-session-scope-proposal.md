---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-23-session-scope
kind: review-finding
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-23
---

# Session scope: a proposal (a Fable agent, at the person's request)

The person, 2026-10-23: "It seems like these session are getting too long if they require compaction. ... conversations
need to be compartmentalized, wrapped up and cleared much faster. There is still far too much tool use in the
interactive session. Sessions in general need to be working with a reasonably fresh set of information." The agent's
reply, as given:

## Files read

CLAUDE.md; spec/index.md; spec/capabilities/supervision.md, work-queue.md, batch-measurement.md, migration-tools.md; spec/decisions/0030, 0037, 0039, 0053, 0059, 0060, 0063, 0064; skills/delivering-an-initiative, integrating-a-proposal, formulating-features, analyzing-a-batch (SKILL.md); agents/initiative-round.md, trial-runner.md; hooks/hooks.json; .shop/records/observations.md (2026-10-21-session-keeps-the-gate, 2026-10-23-hung-worker, -open-initiatives-closed, -decision-0030-misread); .shop/records/2026-10-23-i22-analysis.md; .shop/records/README.md; .shop/records/archive/2026-10-22-0-23-0-handoff.md and ledger-i22-…md; .shop/work/i22…/initiative.md, w94.md; .shop/work/i23…/initiative.md and its design note; docs/design-model/grammar.md (record kinds); .gitignore; `work --help`; `migrate status --hook`; ~/.claude/…/memory/next-0-24-0.md.

## Diagnosis

Every actor in the workflow leaves its state in files that a script reads back (briefs, results, log.jsonl, stage directories, records), except the one that talks to the person. The coordinator's state lives in its context, its compaction summary and memory notes outside the repository, none of which anything verifies. So (a) a claim survived compaction as a fact and nobody re-read 0030, and (b) when `work run` had a gap, the cheapest route was the coordinator's own tools, and nothing refused it. The 0.23.0 hand-off was a 100-line prose file that re-stated the skills' rules; the ledger that 0059 made "the recovery map" is under `.shop/scratch/`, which git ignores, so it is not in the repository until an initiative ends. Note too that `measure --sessions` r43 counts a session only when it *starts* inside the window: the two-day coordinator session was excluded from i22's measurement precisely because it was too long.

## Proposal, ranked

**1. The hand-off is computed, not remembered: `work status <initiative>` printed at SessionStart.** (work-queue lines; hooks/hooks.json; a decision superseding 0059's ledger sentence.) `work status` prints, from files only: the initiative and its proposals' statuses, each work-item with status and open questions, the initiative branch and whether the remote has it, uncommitted changes, `model check`'s last line, the last ten ledger lines, and the one line "next: <job>" (the last ledger line that names one). The ledger moves to `.shop/work/<initiative>/ledger.md`, tracked, and `work note <initiative> <line>` appends and commits it like `log.jsonl` (the person's answers given under delegation, decisions taken, what the next session does). The SessionStart hook runs `migrate status --hook` then `work status --hook` for every initiative not `done`. Replaces: the compaction summary, memory notes as state, prose hand-off files, the coordinator reading `runs/` to learn where things stand. Measured: compactions per initiative (see 5) falls to 0; the coordinator's cache-read tokens against the stages' (0037's own 23-55% figure is the baseline form) fall; sessions per initiative rise to the number of jobs.

**2. A session is one job; each coordinator skill ends with a wrap-up.** (The four skills; a light decision.) The jobs with a file-recorded exit: *gate* (integrate rounds → gate page → apply, ends at the spec commit); *formulate* (ends at the feature-file commit); *delivery* (one `work run` until it exits; on exit 3 the session shows the questions, writes the answers with `work answer`, notes the ledger and ends, the rerun is the next session's; on a branch review, ends when fix work-items are drafted); *analysis* (ends at the record's commit). The wrap-up is three lines in every skill: `work note … "next: <job>"`, nothing uncommitted (`git status --porcelain` empty), then tell the person the job is done and the next starts in a new session. A `PreCompact` hook (hooks.json) appends `compacted` to the open initiative's ledger and prints "wrap up and clear instead of compacting". Replaces: multi-day sessions, the ledger-after-the-fact. Measured: compactions = 0; each session's round trips and new-input tokens bounded (take i22's sessions table as baseline once 5 counts it).

**3. Take the coordinator's hands off the files: close the routes around `work run`.** (integrating-a-proposal, formulating-features, delivering-an-initiative; supervision lines; i23's part 2.)
- Delete both small-change paths. "The session writes its two lines itself" is the single largest source of coordinator Edit/sed/pytest work; a round is cheap (its context ends) and the 30M-token argument the skill makes against rounds-in-session applies to two lines too. `initiative-round`'s `integrate` job takes the lines or a finding as its input, not only a note.
- No direct `claude -p` dispatch and no hand merge; a work-item `work run` cannot deliver is a question to the person, and its two i22 causes already have homes: a disallowed tool is `[allowed_tools]` in delivery.toml (r30); a change to `work run` itself is still a work-item (the worker runs the checkout's scripts, so this is a check, not new code). i22's C1, C2, I1 all came from work with no task review.
- A branch review's fix-now findings become drafted work-items by `work run` itself (one line in supervision: when the reviewer's result lists findings to fix now, draft a work-item for them naming the findings file) and appear in its printout, so the session never opens findings.md.
- Work-item files are written by `work` only; `work run` r46 already refuses uncommitted `.shop/work/`, which a hand edit is.
What stays with the session: publishing the gate and reading answers; `work answer`; starting `work run` and dispatching rounds, the trial-runner and the analysis; `work note`; appending an observation in the person's words; release steps on request. Nothing else, and never pytest, merge, sed or a source file. Measured: tool uses by tool name in the coordinator's sessions (see 5): Edit/Write outside `.shop/records/` = 0, Bash pytest/merge = 0; branch-review Critical findings from unreviewed work = 0.

**4. A citation is a reading, in this session.** (One sentence in each coordinator skill and printed by `work status`; a light decision.) A decision, Behaviour line or record is cited only after its file was read in the current session; a summary, a memory note or an earlier session's claim is not a citation. `work status` prints the summary line of every decision the open initiative's proposals `rest_on`, so the reading costs one command. Replaces: the 0030 misread's mechanism. Measured weakly: observations of the "misread/correction" kind per initiative; say so in the analysis rather than invent a figure.

**5. Measure the coordinator, then judge 1-4 on i23's batch.** (batch-measurement lines; prerequisite, built first.) `measure initiative --sessions` gives, for each non-stage session *active* in the window (not only started in it), its round trips, tool uses by tool name, dispatches, and compactions (the transcript's compact-summary entries), and `compare` carries them. Re-measure i22 for the baseline (its coordinator is in the transcripts, just outside r43's window rule), then deliver i23 under 1-4 and compare. The decision is the person's on those two records, per the memory rule, not on this argument.

## What I would not do

- A turn or token budget that stops the session: the plugin cannot enforce it, turns say nothing about context, and the PreCompact hook catches the symptom directly.
- A coordinator agent or a "session supervisor": 0037 rejected a controller that decides nothing, and the person talks to the session.
- Prose hand-off files like 0.23.0's: they restate the skills and drift; rules live in the skills, state in `work status`.
- Keeping memory notes as the state carrier: the rules in them that are not already in CLAUDE.md or a skill get moved there once; the rest is deleted.
- Fixture scenarios for this: i23 part 6 decides 0030's fate; this is judged on i23's real batch.
- A statusline: the concern is what the session holds, not what it shows.

## The agent's second reply, to the person's follow-up on "job" and on removing the interactive session

You're right that "job" is taken: design model v3 makes **job** a standing artifact (`when [situation], [narrator] wants [outcome]`, grammar.md:17, 247), and `initiative-round` already misuses the word for its modes (`integrate`, `gate`, `apply`, `formulate`). I withdraw "job" as the session's unit and would rename initiative-round's "job" too. Here is the answer to the larger question, from the model's own files.

## What the model already gives you

- Two typed ways work enters a bounded context from outside: a **job-thread** that `enters` the context (product → context, grammar.md:65-68) and a **cross-context-request** `from CAP across SEAM needs TEXT` (context → context, grammar.md:69-71, 261). Both are parts of an initiative; the request has a lifecycle `open → accepted | refused → delivered` decided by the upstream owner, and a `resolution` that is a requirement id. Nothing new has to be invented for "a request from outside".
- One question-and-answer protocol, already built for work-items: `## Questions` with readings, `awaiting-answer`, `work answer`, the answer written in the person's words with its date, the node returned to the stage that asked (0063, 0064, work-queue r13-r14). The gate is the same shape by hand: `initiative-round gate` writes cards, the person answers, `apply` takes "the approval in the person's words with its date".

So the context already contains no activity that needs a chat, except the one it never defined: turning what the person wants into a request.

## Definitions I would propose (the person decides the words)

- **question**: what a node asks of a role the scripts cannot stand in for, written in the node under `## Questions` with its readings; the node waits (`awaiting-answer`) until an answer is written. Not: query, clarification. (Only *answer* is defined today.)
- **request**: the one way work enters a bounded context: a job-thread entering it or a cross-context-request across one of its seams, each a part of an initiative, taken in by the script and answered through questions. Not: ask, ticket, chat.
- **interactive work**: work whose output is a request. It happens outside the context (at the product level, or by the person with an intake skill) and ends when the request file exists. After that, every exchange with a person is a question and its answer on a node.
- **round**: keep the term; initiative-round's modes become "the round's kind" (integrate, gate, apply, formulate), never "job".

With these, the "unit of a session" question disappears: a session is a worker or a dispatch (a brief in, a result out) or an intake session (prose in, a request out). None needs a transcript to survive.

## Can the interactive session go? Yes, inside the context, on three conditions

1. **`work run` becomes the context's loop over every node kind, not only work-items.** Each node with a transition the script can make gets a dispatch with a brief: a request `open` → intake round (capability-proposals drafted; questions back on the request); a proposal `drafted` → gate cards written as questions on the proposal; `approved` → apply and formulate rounds; `formulated` → work-items drafted by the script (delivering-an-initiative's drafting is already "from the spec alone", mechanical); work-items → stages as today; all green → branch review, then measure and the analysis dispatch, the record committed. The person's whole surface is `work answer <node> …`, `work show`/`work status`, and `work run`. The ledger, moved under `.shop/work/<initiative>/` and tracked, holds what the person decided.
2. **Delegation becomes a brief, not a session.** "Drafting decisions delegated to the coordinator" was the misread's vector: a long-lived session answered from memory. Under the loop, a delegated answer is given by a short dispatch whose brief names the files to read and the delegation, and the answer carries `by:` naming it, logged like any other. Decisions are then cited only from files the brief named, which is how workers already work; the citation rule from my item 4 is a brief rule, not a session rule.
3. **The product level owns intake and brainstorming.** This is where the person talks: a skill (or the product repository's session) that ends by writing a job-thread or request into the lead context's `.shop/work/`. "Why did the batch cost that", "what is left", "measure this" are requests too, answered by records; analyzing-a-batch is already a dispatch that leaves a record and replies in lines.

What this costs, honestly: the gate becomes a page of questions answered by command or an answers file rather than a conversation (the i22 answers were already one-liners under delegation, so this is the practice, formalised); a person who wants to think aloud mid-delivery does it in intake, as a new request, not by steering a worker; and Claude Code still needs *a* session to run the loop, but it is a terminal running a script, not a model holding state.

## What this does to the ranked proposal

- Items 1 (`work status`, tracked ledger, SessionStart print) and 5 (measure the non-stage sessions, count compactions and tool uses, count sessions active in the window) stand and come first: they are cheap, they are the hand-off the loop needs anyway, and they give the baseline that judges the rest.
- Items 2 and 3 (session wrap-up, closing the routes around `work run`) are absorbed: with no coordinator in the context there is nothing to wrap up and no hands to keep off the files. The small-change path still goes, since it is the one place a skill tells the session to write spec itself.
- Prove before specifying: the skeleton is i23's own gate run with no coordinator, as a trial: cards written as questions on the proposals, answered with `work answer`, applied and formulated by rounds started from a script, and measured against i22's `--sessions` figures (coordinator cache-read tokens → 0; compactions → 0; the person's answer latency as the new cost to watch). If that works on a real gate, the loop and the intake skill are the next initiative; if the person finds answering by command worse than the page, that is the measurement that says so.

I would not try to keep a reduced "interactive coordinator" alongside the loop: a session that may do a little will do more when a script has a gap, which is the whole history of the last two days. The gap goes to the person as a question on the node, and the script grows a line for it.

No file was changed.

## The agent's third reply, to the person's chain of requests (request → initiative, no tree across seams; internal requests)

Yes, it makes sense, and it is a change to design model v3 as written, not a reading of it. Let me say exactly what v3 says, where your version differs, and what I think is missing.

## What v3 says today (design-model.md §3, grammar.md v_b1-v_b3, v_k1-v_k5)

- The initiative is the root: "never `part_of` anything", the only node with `priority` and `source`; its tree "is its work-breakdown". Kinds `job` and `job-path` root at the product level with a job-proposal or job-thread as first part; `capability-change` and `defect` root in a context.
- "A part may be owned by a different bounded-context than its initiative; it is still part of it." A cross-context-request's fulfilment, "the upstream's capability-proposal and work-items — is `part_of` the request" (v_b2). So one product-level initiative's tree reaches through seams into other contexts' work-items. And the upstream "sequences [inbound requests] by their initiatives' priorities", i.e. by a rank set by someone else's owner.

So I was reporting v3, and v3 is what you are objecting to. Your objection is right on two counts: one tree across repositories is unworkable for scripts that read one `.shop/work/` (every guard like "every part under it closed" needs the other contexts' files), and a priority set by the downstream's owner has no standing in the upstream.

## Your version, made precise

Chain, not tree: **job-thread** (product) → **request** across a seam into a context → **initiative** (that context) → capability-proposals → work-items; a work-item's need across a further seam raises a request that the next context fulfils with its own initiative. The request is the only artifact that crosses a seam; `part_of` never does.

- A request `fulfilled_by` at most one initiative, and an initiative fulfils exactly one request (or is internal, below). The request's `delivered` guard becomes "its initiative is `done`"; a thread's `built` becomes "every request it raised is `delivered`". Each context ranks its own initiatives; the product level ranks threads through the vision's `orders`.
- "Satisfies the request entirely": then initiative `done` ⇔ request `delivered`, which is what makes the chain checkable from either end. An initiative cannot be a work-breakdown because its scope is fixed by the request; the breakdown is the work-items with `blocked_by`, `depends_on` and file-set claims, which is already what `work run` executes. The initiative keeps only `source`, `priority`, `status`, and the measurement at close.
- The initiative kinds collapse: `job` and `job-path` are threads at the product level, not initiatives; a context's initiative is `capability-change` (first part a proposal, one gate) or `defect` (first part a work-item, no gate). v_k1/v_k2 go; v_k3/v_k4 stay.
- Where the request file lives needs one answer: the asker writes it and owns its status; the upstream's intake holds a reference by id (the request's `needs` text copied into its initiative's `source`), and `work status` on both sides shows the pair. Two files that both claim the status is the failure mode to rule out.

## Observations and internal work: what v3 leaves open

v3 says origins "have no rank and appear in nobody's queue"; triage is "an owner starts an initiative from origins"; a review refactor is "not an initiative: an enabling work-item `for:` … or an observation if nothing needs it yet" (§3, use-case table line 224). `w_uncited_obs` (grammar.md:201) already warns on an observation nothing cites. What is missing is exactly what you name: nothing turns an uncited observation into followed-up work, nothing bounds how much of a batch such work takes, and i22/i23 show the result: "initiatives" that are triage bundles with no request behind them.

I would add one node, not a new queue:

- **internal request**: a request whose asker is the context itself, raised from one or more origins (observation, review-finding, measurement) that it cites, with the same lifecycle (`open → accepted | refused → delivered`) and the same fulfilment (one initiative, `capability-change` or `defect`). Accepting it is the owner's triage; refusing it closes the observation with a reason. External and internal requests sit in one ranked list per context: `.shop/work/requests/` with the ranking as a field the owner sets, printed by `work status`. The "intake backlog" v3 names in §3 becomes this file set.
- Follow-up: an observation is *open* while no request cites it; `w_uncited_obs` becomes the list of open observations, aged. That gives the chatter a home: a bug, a review's deferred finding, a measurement that looks off each become one line in observations.md and either get a request or get refused, in writing.
- Budget: supervision's Not yet already lists "spending limits and budgets". Per the measure-first rule I would not enforce one yet: `measure` already attributes cost per initiative, so first add the request's origin (external/internal) to the measurement and the analysis report ("share of the release's cost on internal requests"), run two releases, then set the share in `.shop/delivery.toml` and let the loop refuse to start an internal initiative above it. The number has to come from i23 and the next, not from here.

## What I think you may be missing

1. **A request is the typed replacement for intake chat, so its form must carry what brainstorming produced**: the need in the asker's words, the origins cited, the seam (or "internal"), and the acceptance in the asker's terms (for a thread, the entry scenario; for an internal request, the observation's repro or the figure that should move). Without the last, "satisfies the request entirely" is unjudgeable, and `delivered` is a formality.
2. **Refusal and escalation stay**: a refused request with a thread still needing it is v3's `refused-still-needed` map-escalation; internal requests can simply be refused.
3. **i23 as the first proof**: its six parts are at least four requests (parallel stages; drafting fixes; measure's refusals; model check's gaps; part 6 is a decision, not work). Writing them as internal request files, each with an initiative that must satisfy it entirely, is the cheap trial of the form before the loop is built, and it tells you whether "entirely" is the right constraint when a request turns out larger than one batch.
4. **One tree per repository is a prerequisite for removing the coordinator**: the loop I proposed reads one `.shop/work/`; your chain gives it that. Cross-seam state is only the request pair.

This is a v4 of the model, or a decision superseding §3's "one tree" and the `job`/`job-path` kinds; it is the person's to make. No file was changed.
