# Requests and the context loop (design note, 2026-10-23)

Source: the person's words of 2026-10-23 ("sessions are getting too long if they require compaction … conversations
need to be compartmentalized, wrapped up and cleared much faster … far too much tool use in the interactive session")
and the discussion that followed; observations 2026-10-23-decision-0030-misread, 2026-10-23-open-initiatives-closed,
2026-10-21-session-keeps-the-gate; the i22 analysis (.shop/records/2026-10-23-i22-analysis.md). Drafted by the
coordinator for the person's reading; nothing here is approved.

The diagnosis in one paragraph: every actor in the workflow leaves its state in files a script reads back, except the
session that talks to the person. Its state lives in its context, its compaction summary and memory notes outside the
repository, none of which anything verifies; and when `work run` had a gap, the cheapest route was that session's own
tools, and nothing refused it. The remedy is not a smaller coordinator but none: work enters a bounded context only as
a request, the context's script takes every node through its transitions, and every exchange with a person is a
question on a node and its answer.

## 1. Design model v4: the changes to docs/design-model/

v3 is `docs/design-model/`, "the reference". Its move to shopsystem-knowledge (observation 2026-10-16, decisions
0027 and 0051) never happened; under v4 the model is a product-level artifact and the product level has no
repository yet. v4 is written where v3 is; the move is a later request. The changes:

1. **A chain of per-context trees, not one tree.** `part_of` never crosses a seam. A job-thread (product) raises a
   request into a context; the request is fulfilled by one initiative of that context (`fulfils`, a new edge, exactly
   one request an initiative); the initiative's work-items may raise further requests, each fulfilled by the next
   context's own initiative. v3's "a part may be owned by a different bounded-context than its initiative" and "its
   fulfilment … is `part_of` the request" go.
2. **Done-ness composes through requests only.** A thread is built when every request it raised is delivered; a
   request is delivered when its initiative is done; an initiative is done when its own work is green and every
   request it raised is delivered. A context reads its own files and the status of the requests it raised, nothing
   else of another context. The other context's work-items are observability, never a dependency.
3. **The request is the only thing that crosses a seam, in either direction.** What crosses: the contract (the
   upstream's published spec at a pinned version) and the request as one node. The upstream's standing artifacts
   name no client, as before (how-we-got-here.md, "Citation direction"): no line is justified by "context X needs
   it"; demand lives in the request, the tie is its `resolution`.
4. **A request is written in EARS, negotiated line by line, two ways.** Its body is proposed lines against the
   upstream's capabilities, in the job's narrator and the upstream's published terms. The upstream answers each
   line: accepted as written, rewritten (shown), refused (with the reason), or a question with its readings; the
   asker answers, revises or withdraws lines in its turn, and confirms a rewritten line still meets its need. The
   status alternates (`open` → `awaiting-asker` ↔ `awaiting-upstream`) until every line is accepted, refused or
   withdrawn; then `accepted` (an initiative starts) → `delivered` (the `resolution` names each accepted line's
   requirement id and the version that holds it), or `refused`/`withdrawn` as a whole. The upstream's gate judges its
   own capability-proposal, which the accepted lines become. v3's `needs TEXT` goes.
5. **Narrators are product-level actors, shared across a seam.** A narrator is a role from a job, never a context;
   a request's lines keep it. Terms stay owned by each context (its glossary is part of its contract).
6. **Internal requests.** A request whose asker is the context itself, citing one or more origins (observations,
   review-findings, measurements). Same form, same protocol, same fulfilment. External and internal requests make
   one ranked list a context; an observation is open while no request or initiative cites it. A budget for internal
   work is measured first (cost share by origin, two releases), then set, per the measure-then-change rule.
7. **Initiative kinds collapse to `capability-change` and `defect`.** `job` and `job-path` are threads at the
   product level. v_k1 and v_k2 go; v_k3 and v_k4 stay. An initiative is not a work-breakdown: its scope is its
   request's lines; the breakdown is the work-items with `blocked_by`, `depends_on` and claims.
8. **Trace.** From any work-item: `part_of` → capability-proposal → initiative → `fulfils` → request → `part_of` a
   job-thread, or an internal request citing origins. Two rules make it complete: every initiative fulfils exactly
   one request; every request is part of a thread or cites an origin. A request carries only the asker's context
   and request id, so the trace reaches the thread without reaching the asker's work-items.
9. **Terms.** *question*: what a node asks of a role the scripts cannot stand in for, under `## Questions` with its
   readings; the node waits until an answer is written. *request*: the one way work enters a bounded context.
   *interactive work*: work whose output is a request; it happens outside the context and ends when the request
   exists. `initiative-round`'s "job" (integrate, gate, apply, formulate) is renamed "the round's kind".

## 2. The requests

Six, written here by hand in the form of 1.4 because no intake exists yet; R3 makes the form script-held. The
asker of R1-R5 is the person at the product level (direct requests, no thread), each citing origins. The lines are
the asker's proposal, in gist; the capability-writer makes them the context's in an `integrate` round, checked by
v_e1/v_e2 before the gate. Order: R1 and R2 first (no model change; they give the baseline), v4 then R3 and R4,
R5 after R3. R6 is outside this context.

### R1. Measure the sessions around a delivery

Capability: batch-measurement. Source: i22 analysis "Not counted" (the coordinator session started before the
window and was left out; direct dispatches had tokens only); 2026-10-23-decision-0030-misread.

- **Where** `--sessions <dir>` names a directory of transcripts, `measure initiative` shall also give each session
  found there that is active inside the initiative's window: one that starts inside it, or starts before it and has
  a message inside it.
- **Where** `--sessions <dir>` is given, `measure initiative` shall give, for each session it gives, its round trips,
  its tool uses by tool name, the sessions it dispatched, and the number of compactions its transcript holds.
- **When** `measure show <record>` is run on a measurement that gives sessions, `measure` shall print each session's
  round trips, tool uses, dispatches and compactions beside its tokens.
- **When** `measure compare <a> <b>` is run on measurements that give sessions, `measure` shall print the sessions'
  totals (round trips, tool uses, compactions) side by side with the ratio of the second to the first.
- (after R4) `measure initiative` shall give the origin of the initiative's request, internal or external, so the
  analysis can give the release's cost share by origin.

It worked if: i22 re-measured with `--sessions` gives the coordinator's figures (the baseline), and i23's or the
next batch's compare shows them.

### R2. A session starts from the repository's state

Capabilities: work-queue; the plugin's hooks (today under migration-tools r22-r31). Source:
2026-10-23-decision-0030-misread (a claim survived compaction as fact), 2026-10-21-session-keeps-the-gate (the
ledger as recovery map; it lives under `.shop/scratch/`, which git ignores, until an initiative ends).

- **When** `work status <initiative>` is run, `work` shall print the initiative's status, each of its
  capability-proposals with its status, each of its work-items with its status and its open questions, the
  initiative branch and whether the remote has every commit of it, each file uncommitted in the checkout, the last
  ten lines of the initiative's ledger, and the ledger's last line that begins `next:`.
- **When** `work status` is run with no initiative, `work` shall print that for every initiative that is neither
  `done` nor `abandoned`.
- **Where** `--json` is given, `work status` shall print its result as one JSON object.
- **When** `work note <initiative> <line>` is run, `work` shall append the line, with the date, to
  `.shop/work/<initiative>/ledger.md` and commit it on the current branch.
- **If** the line given to `work note` has a newline in it, then `work` shall exit with an error, saying that a note
  is one line, and change nothing.
- **When** a session starts in a repository with an initiative that is neither `done` nor `abandoned`, the plugin's
  SessionStart hook shall give the session what `work status` prints for it.
- **When** a session is about to be compacted in a repository with such an initiative, the plugin's PreCompact hook
  shall append `compacted`, with the time, to that initiative's ledger and tell the session to write its hand-off
  with `work note` and end instead.

Also: a decision superseding the ledger sentence of 0059 (the ledger is `.shop/work/<initiative>/ledger.md`, tracked,
archived with the initiative); delivering-an-initiative and initiative-round write it with `work note`; the
coordinator's memory notes outside the repository are retired, their standing rules moved into skills or CLAUDE.md
once. It worked if: compactions per initiative (R1) fall to 0 and no hand-off prose file is written.

### R3. Requests, intake and the two-way protocol

Capability: new, `requests` (narrator: a context taking in or raising a request); design-model-check for the file
form. Source: 2026-10-23-open-initiatives-closed (initiatives with no request behind them),
2026-10-21-session-keeps-the-gate.

The file: `.shop/work/requests/q<n>.md`, frontmatter `id: request/<context path>/q<n>`, `kind: request`, `asker`
(a context id, `internal`, or the product level), `part_of` (a job-thread) or `source` (origins), `status`,
`turn` (asker | upstream). Sections: `## Lines` (the asker's), `## Outcomes` (the upstream's, one a line),
`## Questions`, `## Answers`, `## Resolution` (the upstream's).

- **When** `work request <title> --from <asker> --lines <file>` is run, `work` shall write
  `.shop/work/requests/q<n>.md` as an `open` request with the file's lines under `## Lines`, its asker and its
  sources or thread, with the turn the upstream's, and print its id.
- **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), then `work
  request` shall refuse, naming the line, and change nothing.
- **If** a request names neither a job-thread nor an origin, then `work request` shall refuse, saying so, and change
  nothing.
- **When** `work turn <request>` is run, `work` shall verify that only the sections of the side whose turn it is
  changed since the last turn, write the turn to the other side, and commit the request file.
- **If** a section of the other side changed, or no section changed, then `work turn` shall refuse, naming the
  sections, and change nothing.
- **When** every line of a request has an outcome accepted, refused or withdrawn and the upstream ends its turn,
  `work` shall transition the request to `accepted` where a line is accepted, else to `refused`.
- **When** `work resolve <request>` is run on an `accepted` request, naming each accepted line's requirement id and
  the version that holds it, `work` shall write them under `## Resolution`, transition the request to `delivered`,
  and commit.
- **When** `work show` is run, `work` shall print each request with its status and whose turn it is.
- **When** `work status` is run, `work` shall print each observation that no request or initiative cites, with its
  date.
- `model check` shall report a request file not of this form as a file problem.

Questions for the gate: where the request file lives between two repositories (proposal: in the upstream's
`.shop/work/requests/`, written there by the asker once, then in turns; the asker reads it); whether a line's
outcome is edited by hand and sealed by `work turn`, or written by a `work outcome` command.

### R4. An initiative fulfils one request

Capabilities: design-model-check, work-queue. Source: 2026-10-23-open-initiatives-closed.

- **When** `work start <request>` is run on an `accepted` request, `work` shall write
  `.shop/work/<initiative>/initiative.md` as a `proposed` initiative of kind `capability-change` that fulfils the
  request, with the request's origins as its source, and print its id.
- `model check` shall report, as rules with ids: an initiative that fulfils no request; an initiative `done` whose
  request is not `delivered` or that raised a request not `delivered`; a request that neither is part of a job-thread
  nor cites an origin; a `delivered` request whose resolution names a requirement the spec does not have; an id in
  this context's files that resolves to a node under another context's `.shop/work/`; an initiative of kind `job` or
  `job-path`.
- **When** every work-item of an initiative is `green` or `withdrawn` and every request it raised is `delivered`,
  `work` shall transition the initiative to `done`.

Also: the i23 parts still open are rewritten as internal requests in R3's form before they are delivered, as the
trial of the form; the existing initiatives i1-i23 are left as they are (history), with a rule exemption by date or a
migration, the gate's choice.

### R5. The context runs without a coordinator

Capabilities: supervision, delivery, spec-integration, formulation; the skills. Source:
2026-10-23-decision-0030-misread, i22 analysis candidates 2 and 3 (hand merges and work with no task review),
2026-10-21-session-keeps-the-gate.

- **When** `work run` is started with no initiative, `work run` shall take every initiative that is neither `done`
  nor `abandoned` through every transition its nodes can make, one dispatch at a time where they would share files.
- **When** a request is `open` or `awaiting-upstream` and this context is its upstream, `work run` shall start an
  `initiative-round` session of the kind `intake`, given the request, which writes each line's outcome or question
  under `## Outcomes` and ends the turn with `work turn`.
- **When** a capability-proposal is `drafted`, `work run` shall write its gate as questions under the proposal's
  `## Questions`, one a decision with its readings and the recommended one marked, and transition the proposal to
  `awaiting-answer`.
- **When** every question of a capability-proposal has an answer, `work run` shall start a round of the kind `apply`
  given the answers, then a round of the kind `formulate`.
- **When** a capability-proposal is `formulated`, `work run` shall draft its work-items with `work add`, one a
  capability, each accepting every requirement of the proposal's `adds` and `changes` on that capability and naming
  under `## Retires` each `@deprecated` scenario whose requirement it accepts.
- **When** a kept branch review's result lists findings to fix now, `work run` shall draft one work-item for them,
  naming the findings file, under the proposal the findings' work-item is part of.
- **When** every work-item of an initiative is `green` or `withdrawn` and the kept branch review lists nothing to fix
  now, `work run` shall run `measure initiative` and start an analysis session that writes the analysis record.
- **Where** the request an initiative fulfils gives a delegation, `work run` shall have a question the delegation
  covers answered by a dispatch given the delegation, the files the question names and nothing else, the answer
  written with the delegation in its `by`.

Also, in the skills: the small-change paths of integrating-a-proposal and formulating-features go (the one place a
skill tells a session to write spec itself); "If the person is talking to you" sections go with the coordinator;
delivering-an-initiative's drafting moves into `work run`; direct `claude -p` dispatches and hand merges are not a
practice (a tool `work run` disallows is `[allowed_tools]`; a change `work run` cannot deliver is a question);
analyzing-a-batch is started by `work run`. The person's surface is `work status`, `work answer`, `work note`,
`work turn`, `work run`.

Question for the gate: the delegation line, since "what nobody may decide goes to the person" (supervision's
Purpose); the alternative is that every question waits for the person.

It worked if: R1's figures for the next batch show no interactive session active in the window with tool uses
beyond `work` commands, compactions 0, and the branch review's fix-now findings from unreviewed work 0.

### R6. Intake at the product level (outside this context)

A skill, or the product repository's session, where interactive work happens: identifying the request,
brainstorming, and ending by writing a request in R3's form into the lead context's intake (through `work request`).
And the move of the design model to its owner, as a request from this context when a product repository or
shopsystem-knowledge's final layout exists to receive it.

## 3. What is not proposed

- A turn or token budget that stops a session: unenforceable by the plugin; the PreCompact hook catches the symptom.
- A coordinator agent or a reduced interactive coordinator: a session that may do a little does more when a script
  has a gap (decision 0037's reasoning; the last two days' history).
- Prose hand-off files like 2026-10-22-0-23-0-handoff.md: rules live in skills, state in `work status`.
- Memory notes outside the repository as a state carrier.
- A budget for internal work before two releases have measured the share.
- Fixture scenarios for this: judged on real batches with `measure`.
