# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow with one spec of capability files per
bounded context, written as codified requirements in a controlled language (a GF grammar built from the glossary),
logic-checked with clingo, Gherkin feature files generated from them as the contract, a backlog of items readied
against that spec, and ready items built in batches, each closed by one reviewed pull request.

Skills: `shaping-items`, `taking-in-a-request`, `raising-a-request`, `building-a-batch`, `analyzing-a-batch`.
Agents: `pr-reviewer`, `architecture-reviewer`, `trial-runner`.
Format: `docs/capability-format.md`. The design model it keeps: `docs/design-model/` (version 5; 2.0 builds on it
with items in place of initiatives).
This repository's own spec: `spec/index.md`; check it with `python3 scripts/model check`.

## Requires

The plugin depends on no other plugin. It needs, in the consuming repository's Python:

- the grammar tools, installed by `python3 scripts/tools install` (Linux x86_64): GF 3.12 under
  `~/.local/share/shopsystem-bdd/gf-3.12/` (or `$SHOPSYSTEM_GF`), and the pinned wheels pgf 1.1 and clingo 5.8.2,
  for `model check`, `model parse`, `model logic`, `features generate` and `work outcome`;
  `tools probe` shows what is installed;
- pytest and pytest-bdd, for the scenarios;
- pytest-xdist, optional, to run the tests in parallel (`pytest.ini`'s `addopts = -n auto`; `-n 0` runs them in one
  process);
- `gh`, logged in, for a batch's pull request and a request's issue.

## Install

```
claude plugin marketplace add dstengle/shopsystem-bdd
claude plugin install shopsystem-bdd@shopsystem-bdd
```

While developing, `claude --plugin-dir <path to this checkout>` loads the working copy instead.

## The layout

A consuming repository keeps (design-decision/final-layout):

- `spec/`: `index.md` (the bounded context: purpose, constraints, composition, glossary), `capabilities/<name>.md`,
  and `decisions/`, one file a decision with its index `decisions/index.md`, written by `model decisions`;
- `features/<name>.feature`, one a capability, the file of its own name, written by `features generate`;
- `.shop/backlog/b<n>.md`, the items; `.shop/batches/<n>/`, the batches; `.shop/requests/q<n>.md`, the requests
  between contexts; `.shop/quotes/<n>.md`, the person's words kept;
- `.shop/records/`: observations, measurements, review findings, decision arguments and the archive;
- `.shop/delivery.toml`, the batch settings and prices, optional;
- `.shop/work/`, plugin 1.x's queue, frozen as history;
- `.shop/scratch/` and `.shop/worktrees/`, drafts, notes and the batches' worktrees, both git-ignored.

## The workflow

- **Work comes in as items.** `shaping-items` turns what the person wants into an item of the backlog
  (`work idea`, `work shape`), its requirement lines written into it (`work line`); `taking-in-a-request` answers a
  request asked of this context, and `raising-a-request` raises one into an upstream.
- **A request is a conversation on one GitHub issue** on the upstream's GitHub repository (its `github:
  <owner>/<name>` under `## Upstreams`; a context's own request on its own repository). Every step is a comment a
  `work` command posts, and each side keeps its record in `.shop/requests/q<n>.md` with the issue's URL; nothing
  reads or writes the other side's repository. The asker asks in its own words (`work request`), the upstream offers
  what may serve with its glossary (`work offer`), the asker says one fits (`work fits`) or proposes lines in the
  upstream's terms (`work propose`, `work turn`), the upstream answers each (`work outcome`, `work ask`, `work turn`;
  an accepted line parses in its grammar and names its capability), and the upstream's person accepts the request,
  which becomes an item (`work accept`); `work resolve` posts the resolution and closes the issue. `work sync`, run
  on either side, records what the other side posted and prints what waits; only a comment's block of fields is
  read.
- **Requirements parse.** Every Behaviour statement is an EARS requirement in the context's grammar (the glossary of
  `spec/index.md` and each capability's `## Terms` are its lexicon), in a requirement group `[g<n>]` with ids
  `[r<n>]`, and parses to exactly one tree (`v_p1`, `v_p2`). `spec/universal.md` holds the universal conditions
  `U<n>`. Each grammar fun translates to facts about its requirement, and `model logic` checks them in one clingo
  solve of `grammar/check.lp` over the pairs of requirements that share vocabulary: clashes (L1), duplicates (L2),
  sets no transition allows and unreachable values (L3, L4), untriggered event obligations (L5).
- **An item is ready when its lines pass the bar.** `work ready` checks them: they parse, the logic check finds
  nothing new, and every question is answered.
- **Groups become scenarios.** `features generate` writes one scenario a group, tagged `@g<n> @r<n>…`, read off
  its requirements' facts with no solver: no session writes a feature file.
- **Ready items are built in batches.** `building-a-batch` starts a batch of ready items (`work batch start`),
  dispatches one subagent a task in its own worktree, closes each task (`work batch done`), and publishes one pull
  request (`work batch review`), reviewed once by `pr-reviewer`; `measure batch` measures it once merged.
- **The spec checks itself.** `model check` checks the whole repository against the design model.

## Scripts

Python 3, in `scripts/`. `--help` is each one's contract; the plugin's own tests: `python3 -m pytest`.

- `scripts/model`: read a bounded context's spec, feature files, decisions and records as the facts of the
  design model's grammar (`facts`), check them with clingo (`check`), list the rules (`rules`), write the decisions
  index (`decisions`), parse a line in the context's grammar (`parse`), list the lexicon (`lexicon`), check the
  logic of the groups (`logic`), the coverage of the 0.29 ids (`restates`) and every file form a context keeps with
  the command that writes it (`forms`).
- `scripts/features`: `generate` writes (or `--check`s) each codified capability's feature file from its groups;
  `vocab` checks the fixed step vocabulary; `count`, `list`, `bindings` and `deprecated` read feature files without
  the test runner.
- `scripts/work`: the backlog (`idea`, `shape`, `line`, `rate`, `depend`, `refuse`, `ready`, `backlog`), the
  batches (`batch`), the requests between contexts (`request`, `offer`, `fits`, `propose`, `outcome`, `ask`,
  `reply`, `turn`, `accept`, `resolve`, `sync`), a design-decision (`decision`) and a record with its index row
  (`record`), and `list` and `show`.
  - `work quote "<the person's words>"` copies the person's message with the two messages before and after it (no
    tool output) into `.shop/quotes/` and commits it. `work show quote-<n>` prints it. `work names` is the table of
    items and batches by name. The UserPromptSubmit hook keeps the session for `work quote`
    (`conversation_hook quote`), and the SessionStart hook prints the names table (`conversation_hook names`); each
    imports only what it needs and never fails. `work quote --hook` and `work names --hook` do the same.
- `scripts/tools`: the project's analysis tools behind one interface: `probe`, `install` (also the grammar tools), `map`, `tests-of`,
  `untested`, `refs`, `check`, and `size`, the tracked Python files over a line limit.
- `scripts/migrate`: `migrate run --context <owner/product/context>` takes a repository from the old system to
  this layout in one run; `migrate upgrade` takes it from an earlier plugin release to this one.
- `scripts/measure`: `measure batch <batch>` writes a batch's measurement from git and its sessions' transcripts
  (wall time, session time, tokens and cost by role, the pull request's findings by grade, defects, knobs);
  `measure defect <item> --says "<fault>"` records a fault found after the merge; `measure show` prints one as
  tables and `measure compare batch-2 batch-3` two side by side with their ratio.

## Agents: rules enforced by tools

| agent | tools | model | for |
|---|---|---|---|
| `pr-reviewer` | Read, Glob, Grep | opus | a batch's pull request review, from its brief: the batch's own commits, its items' lines, the judgement decisions; changes nothing, and replies with the findings file the batch session saves |
| `architecture-reviewer` | Read, Glob, Grep, Bash | opus | an architecture review when the person asks for one, of the commits or the batch it is given; changes nothing, and replies with the findings file the session saves |
| `trial-runner` | Read, Glob, Grep, Bash, Write | sonnet | one trial of a plugin tool or command on a target; writes only one measurement record |

No agent has the Agent tool (design-decision/the-2-0-agents). A plugin agent's `hooks` and `permissionMode` are
ignored, so a role's limits are its tools.

## 2.3.0: work pushes its commits, requests post after they commit, and work watch

- **`work` pushes every commit it makes** (b51, b56, b57): to the branch's upstream remote, else `origin`. A refused
  push prints `not pushed: <remote>: <reason>` and keeps the commit; a push never prompts, and it gives up after
  `$SHOPSYSTEM_PUSH_TIMEOUT` seconds (default 60). A command that commits is refused on a batch task's branch
  `batch-<n>-b<j>`, naming the task.
- **A request's step is committed before it is posted** (b36): a commit git refuses posts nothing, and a post GitHub
  refuses puts the record back. When GitHub accepts a post and the commit of its URL then fails, the refusal names the
  URL. `work sync`, or the same command run again, records it without posting it again.
- **`work watch`** (b31) polls the issues of the requests not closed, and this context's own open issues, every
  `--every` seconds. It prints each comment a request does not hold and each new ask, then exits, so a session started
  on it wakes when the other side moves.
- **`work reply` and `work turn` check the side** (b30): each is refused on the side of a request that is not this
  repository's. A refused request line needs `--reason` again (b37).
- **`work line --relation`, `--universal`, `--upstream` and `--given`** (b43) write a relation row, a universal
  condition, an upstream entry or a given block onto an item, each checked for its shape.
- **The readiness bar refuses a scenario with an unworded step** (b46), naming the step. `work decision` and `work
  record` refuse an absent argument by name (b45).
- **No upgrade step.**

## 2.2.0: decisions and records written by command

- **`work decision`** writes a design-decision whole from its arguments (b41, decision-tiers r7, r8): `work decision
  "<title>" --summary "<one sentence>" --tier check|requirement|judgement --decision "<text>"`, with `--context`,
  `--alternatives` (text, or `@<file>`), `--source`, `--by` and `--enforced-by`. It numbers the file after the
  highest in `spec/decisions/`, rewrites the decisions index as `model decisions` does, and commits both. With no
  `--tier` it is refused and writes nothing.
- **`work record`** writes a record (design-model-check r56): `work record "<title>" --kind <kind> --summary "<the
  index row>" --body <file>` writes `.shop/records/<date>-<slug>.md` with its frontmatter, adds its row to
  `.shop/records/README.md`, and commits both. A record's supporting files, and a design's or plan's folder, are
  still written by hand (b44).
- **`model forms`** lists each kind of file a context keeps, with its path and the command that writes it
  (design-model-check r55), so a session finds the command instead of copying an existing file. `--json` gives the
  same as one object. The forms with no command yet name the plugin item that will give them one.
- **No upgrade step.**

## 2.1.0: requests exchanged through GitHub issues

- **A request is a conversation on one GitHub issue** on the upstream's repository (b26, requests r27-r41, intake
  r7). Each side keeps its record in its own repository, and nothing reads or writes the other side's checkout:
  - the asker asks in its own words with `work request --ask`, and the upstream answers with `work offer`;
  - the asker ends the request with `work fits`, or writes lines with `work propose`;
  - each side ends its turn with `work turn`, which posts it on the issue;
  - the upstream's person accepts with `work accept`, which writes the item;
  - `work resolve` posts the resolution and closes the issue;
  - `work sync` records what the other side posted. A comment whose block of fields does not parse is printed,
    never acted on.
- **Where the issue lives:** an upstream's bullet under `## Upstreams` in `spec/index.md` names its repository as
  `github: <owner>/<name>`. A context's own request goes on its own repository, read from `origin`.
- **Retired:** `work intake`, `work outcome --into` on an item, and `work request --lines`. `work outcome accepted`
  now parses the line in this context's grammar and names its capability with `--into`.
- **Not yet:** `work sync` applies a readable comment whoever posted it (b35). Until that is fixed, exchange
  requests only between your own contexts, or on private repositories.
- **No upgrade step.** A 2.0.0 repository needs only `github:` on each upstream it asks. A request it already holds
  has no issue, and is read as before.

## 2.0.0: the workflow simplified

- **One item, a backlog, batches, one review at the pull request** (design-decision/the-workflow-simplified): work is
  an item in `.shop/backlog/`, shaped and readied against the codified spec (`work idea`, `shape`, `line`, `ready`),
  built with other ready items in a batch (`work batch`), and reviewed once, by `pr-reviewer`, at the batch's pull
  request. A peer's request is taken in as an item (`work intake`). `measure batch` measures a merged batch.
- **The old workflow retired** (design-decision/the-old-workflow-retired): `work run` and its stages, initiatives,
  work-items, capability- and glossary-proposals, delegations, `work add`, `retry`, `note`, `status`, `start` and
  `delegate`, `measure initiative` and `model why` are gone, with ten agents and six skills; their capabilities keep
  their files as the record of their ids. The agents are `pr-reviewer`, `architecture-reviewer` and `trial-runner`
  (design-decision/the-2-0-agents).
- **`.shop/work/` frozen** (design-decision/the-2-0-layout): nothing writes it, and `model check` reads only the
  `source` of its initiatives and requests, as citations of observations. Live requests are `.shop/requests/q<n>.md`,
  numbered above the frozen ones.
- **`migrate upgrade` 2.0.0, "the workflow simplified"**: a 1.0.x repository is moved to the new workflow in one
  commit. It writes `.shop/work/FROZEN.md`, moves each open request of a peer to `.shop/requests/` with `git mv`, and
  rewrites `spec/decisions/index.md`. Nothing is deleted. It names each open initiative, each proposal never applied
  and each internal request not closed, to be shaped as items with `work idea`. A 0.29.x repository reaches 2.0.0
  through the 1.0.0 step in the same commit. From 0.29.x, write each scaffold's requirements and the typed glossary
  as `docs/capability-format.md` § Doing it says, checking with `model parse`, `model check`, `model logic` and
  `model restates`, then run `features generate`.

## 1.0.0: codified requirements

- **Requirements are written in a controlled language** (design model v5, `docs/design-model/`): the glossary of
  `spec/index.md` is typed (`- **<term>** (<category>): …`) and is the lexicon of a GF grammar; every Behaviour
  statement is an EARS requirement that parses to exactly one tree, in a requirement group `[g<n>]`; a capability
  file says `language: codified-1`. `spec/universal.md` holds the universal conditions `U<n>`.
- **New tools:** `tools install` installs GF 3.12 and the pinned pgf and clingo; `model parse`, `model lexicon`,
  `model logic` (one clingo solve of `grammar/check.lp` over each requirement's facts: clashes naming both ids,
  duplicates, transitions, reachability, untriggered event obligations) and `model restates` (each 0.29 id
  restated, dropped or moved); `features generate` and `features vocab`.
- **Scenarios are generated**, not written: `features generate` writes one scenario a group, tagged `@g<n> @r<n>…`,
  and step definitions are handlers of a fixed step vocabulary. The agent that wrote feature files is gone, and so are
  `features tag`, `move`, `deprecate`, `retire`, `rebind` and `verify-moved`. `work run`'s formulate round is a script.
- **Requests are codified:** `work request` parses each line in the upstream's grammar and refuses one that does not
  parse, with a hint; the new skill `raising-a-request` writes the lines from English.
- **The 0.29 reader is gone.** `model check` reports a capability file or a `spec/index.md` without
  `language: codified-1` (`v_p0`), and `features generate` (exit 2) and `work request` refuse it, each naming
  `migrate upgrade`.

Upgrading a consuming repository from 0.29: update the plugin, run `python3 scripts/tools install`, then
`python3 scripts/migrate upgrade` on a clean tree. Its 1.0.0 step writes `spec/restated.json` (the text of every 0.29
id), turns each capability's Behaviour into a scaffold of one group per old line with `Restates:` filled and the old
text kept as a comment, deletes `@deprecated` scenarios, rewrites the old references in `.shop/work/` to
`<cap>#r<n>@0.29`, and lists what is left for a session to write: the typed glossary, each scaffold's requirements and
each open capability-proposal. Write those with `integrating-a-proposal` (checking them with `model parse`, `model
check`, `model logic` and `model restates`), then `features generate` and the handlers of the new scenarios.

## 0.29.0: glossary-proposals, delegations given late, and fewer stops from outside a work-item

- **The glossary is a target of spec work** (i46, i50, i51, i64): an integrate round's glossary entries are written as a
  drafted glossary-proposal (supervision r171, r172); an apply round withholds the terms of one the person has not
  approved (spec-integration r55); its gate asks the person to approve its terms even with no question; a question
  naming a glossary term or a glossary-proposal is left for the person under a delegation (r162, r163); a
  glossary-proposal whose apply round applied nothing goes back to an integrate round (r221).
- **A redraft keeps the ids it does not name** (i48, i54; supervision r188, r189): an integrate round that redrafts some
  of a proposal's lines keeps the proposal's other ids and terms. Before, the other ids were dropped and their scenarios,
  accepted by no work-item, failed every whole-suite check.
- **A delegation can be given after a request is raised** (i60): `work delegate` writes it in the request (requests
  r65), `work run` reads the delegation the request has at that moment (supervision r211), and a new UserPromptSubmit
  hook tells a session to write a delegation the person gives in conversation (requests r72).
- **A flaky scenario no longer stops a merge** (i62; supervision r219, r220, r222): a scenario that fails in the
  whole-suite check gets one more run, alone, and a pass lets the merge go ahead. A run with errors, or a failure that is
  not a pytest-bdd scenario, is not taken back; a refused merge's question gives each scenario's runs.
- **An answering session is not faulted for another initiative's changes** under `.shop/work/` (i63; r218).
- **`work list` and `work show`** show requests and observations no initiative names (i54, i55; requests r64), and
  `work run`'s exit names what is open (r212, r213).

Upgrading a consuming repository from 0.28.3: update the plugin and start a session. No file is rewritten; the new
UserPromptSubmit hook comes with the plugin.

## 0.28.3: a branch review that runs nothing

- **`work run` makes the branch review's runs before it starts** (supervision r154, r155): the whole suite, each
  work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and
  `features bindings`, at the branch's head, and gives the reviewer each one's command, how it exited and its output,
  naming the commit.
- **The reviewer is given what to read** (supervision r156, r157): the commits from the initiative's base, each with its
  work-item or none, the change less `.shop/`, and the capabilities, decisions, plans, reports and review findings.
- **The branch reviewer runs nothing and has no shell tool** (review r32-r34, role-boundaries r7): a behaviour only a
  run would show is a finding with the test that would show it, marked not run. review r9 is retired. In i42 a
  branch review took about 33 turns, 6 to 8 of them commands the sandbox refused, and re-ran every check itself.

Upgrading a consuming repository from 0.28.2: update the plugin and start a session. No file is rewritten.

## 0.28.2: answers a round cannot hold go back to integration

- **An apply round names the answers its drafts do not hold** (spec-integration r46): `initiative-round` gives them in
  its result.
- **`work run` starts a new integrate round for them** (supervision r150, r151): when an apply round gives an answer
  its drafts do not hold, the proposal goes back to integration, and no formulate round starts for it until the new
  integrate round has been applied. r140 is retired for r150.
- **A formulate round that formulates nothing because the answers change lines not in `spec/`** (supervision r149,
  r152, r153) starts a new integrate round, keeps the proposal's status and counts as the round's output, where before
  the proposal was set `formulated` with nothing formulated.

Upgrading a consuming repository from 0.28.1: update the plugin and start a session. No file is rewritten.

## 0.28.1: `work run` stops visibly on questions, and spends less agent time

- **`work run <initiative>` prints each capability-proposal with its status**, and one awaiting an answer with its open
  questions, exiting 3; before, an initiative with no work-item yet exited 0 printing nothing.
- **An initiative is not set `done` while a capability-proposal of it is neither formulated, withdrawn nor merged**, by
  `work run` or by `work withdraw`.
- **A researcher's empty file set** (no file to change) is its output, not a missing one.
- **Less agent time, quality kept** (from a measurement of 801 sessions): a branch review is started only when an
  unread commit touches the initiative's own files, not for another initiative's commits on a shared branch; a
  work-item's worker is refused `pytest --whole-suite` (`work run` runs the suite at the merge); a task reviewer's brief
  gives the merged `Commits:` and the `Suite record:`; the researcher locates the change (one run of the accepted
  scenarios, no probes); the branch reviewer runs the whole suite once.

Upgrading a consuming repository from 0.28.0: update the plugin and start a session. No file is rewritten.

## 0.28.0: one set of request commands, `work list` and `work show`, and answers that redraft

- **`work list` and `work show <id>`** (work-queue r34-r39, decision 0072): `work list` lists every initiative, request
  and work-item with its status; `work show <initiative>` gives where an initiative stands (what `work status
  <initiative>` gave), `work show <work-item>` a work-item's status and open questions, `work show <request>` a
  request. `work status` and the old `work show` are retired in the spec; `work status` still runs in this release
  and is removed in a later one.
- **Requests** (requests r25, r29-r34, r44, r45; q14 lines 1, 5-7, 10-12): one set of commands and one lifecycle for
  every request; `work request` refuses, changing nothing, a request from another asker raised with `--source` or with
  neither `--raised-for` nor `--thread`, and an asker that is not the context or product whose repository raises it;
  `--raised-for <request>` names the request it is raised for. The side that writes a part of a request is taken from
  the repository, and `work outcome`, `ask` and `resolve` refuse a side writing the other side's part. Requests between
  repositories (q14 lines 2-4, 13-16, 18, 20-22) are not in this release: they will travel as GitHub issues. Until then another
  context cannot raise a request into this repository with `work request`, which raises only as the repository it runs
  in; `work run`'s raise is the one way a request reaches an upstream.
- **An integrate round that needs an upstream** (spec-integration r44; supervision r135, r136; work-queue r39; q14 lines
  23-26): the round gives the lines of a request into the upstream named in `spec/index.md`; `work run` raises them,
  raised for the request the initiative fulfils and with its delegation, holds the proposal's work-items until that
  request is `delivered`, and `work list` shows the initiative waiting on it.
- **`model check`** (design-model-check r120, r121; q14 lines 8-9): no `v17` for a request that is part of a job-thread
  kept in another repository, and neither `v17` nor `v18` for a request raised for a request of another context.
- **Answers that ask for what the drafts do not hold are redrafted** (supervision r140-r148, spec-integration r45):
  an apply round that applies nothing because of its answers sends the proposal back to a new integrate round, given
  its questions, answers and the initiative's ledger; that round drafts the lines the answers ask for, and the ids it
  writes for another capability are added to that capability's proposal, never written over it. An apply round also
  gives in its result (`unheld_answers`, spec-integration r46) each answer its applied drafts do not hold.

Upgrading a consuming repository from 0.27.0: update the plugin and start a session. No file is rewritten. Use `work
list` and `work show <id>` in place of `work show` and `work status`.

## 0.27.0: transitions from how a session ended, and the turn of an accepted request

- **`work run` moves a node by how its session ended and what its result holds** (supervision r128-r134), never by
  the outcome word a result gives (r133). A session that ends in an error, at its turn limit or with no result
  `work run` can read is a fault, whatever its result says (r128): a work-item goes to `failed`; a round's or an
  answering session's fault is recorded under its node's `## Faults` and printed, the node keeping its status. A
  result that gives questions sends them where its stage's questions go (r129): a researcher's into the planner's
  brief, the work-item moving on to `researched`; every other stage's under the node's `## Questions`, the node
  `awaiting-answer`. A result with no question and its stage's output makes the next transition (r130); one with
  neither gets a question naming the missing output (r131). Each stage's output (r132): a researcher's file set, a
  planner's plan and file set, an implementer's commits on which the work-item's scenarios and the whole suite pass,
  a reviewer's findings, an answer, an integrate or apply round's change list, a formulate round's scenario for each
  requirement its proposal adds or changes (none for a requirement of a guarantees capability, none for a term), an
  intake round's line outcome or question on each line, a gate round's questions. So a formulate round's question
  waits for its answer whatever the round reports (q13). Supervision r3, r5, r16, r112 and r113 are removed; "fault",
  "outcome" and "stage" in the glossary now speak of every session.
- **An accepted request stays in the upstream's turn** (requests r23, r24, r7 narrowed): the delivery an acceptance
  promises is the upstream's, so `work` keeps the turn there when it sets a request `accepted`, and passes it to the
  asker when the request is `delivered`.

Upgrading a consuming repository from 0.26.0: update the plugin and start a session. No file is rewritten. A request
already `accepted` in the asker's turn stays there until it is resolved, which passes the turn to the asker as before.
Workers are still asked for an outcome word; it is kept for reports.

## 0.26.0: requests and the context loop

- **Requests** (capability requests, decision 0067): the one way work enters a bounded context. `work request <title>
  --from <asker> --lines <file>` takes one in (strict EARS lines; `--source` or `--thread`; `--delegation <text>` for
  questions a session may answer in the person's place). The upstream writes each line's outcome with `work outcome`
  and its questions with `work ask`; the asker answers with `work reply`; `work turn` passes the turn; `work resolve`
  writes the requirement and version that hold each accepted line. `work start <request>` writes the initiative an
  accepted request begins. `work delegate <request> <delegation>` writes, replaces and commits a request's delegation
  (refused for a delivered, refused or withdrawn request); a UserPromptSubmit hook tells a session, in a repository
  that keeps an open request, to write a delegation the person gives with it, in the same reply. Requests are kept as
  `.shop/work/requests/q<n>.md`.
- **The context runs without a coordinator** (decision 0068): `work run` with no initiative takes every open request and
  initiative through every transition it can: the intake round of a request, the initiative of an accepted one, its
  integrate round (drafts kept on the branch, one capability-proposal a capability, ids above those other initiatives'
  drafts hold), the gate (its questions on the proposal, or one asking for approval), answers under the request's
  delegation, the apply round (the proposal's ids rewritten from what it applied), the formulate round (a question
  sends the proposal back to awaiting-answer), drafting (deprecated scenarios listed under `## Retires` by their
  `Deprecated for:`), delivery, the branch review again after its fixes, the measurement and analysis, committed, and
  the initiative set `done` once it has a green work-item and nothing open. A round that stops does not stop the
  other nodes.
- **A reviewer's question reaches implementation** (decision 0069, superseding 0063's row): `work answer <work-item>
  --change <answer>` returns the work-item to `ready` with the findings and the answer in the implementer's brief;
  `--accept` returns it to `done`. One of them is required on a reviewer's question.
- **Sessions start from the repository's state**: `work status` prints where each open initiative stands; `work note`
  appends to the initiative's ledger, now tracked as `.shop/work/<initiative>/ledger.md` (decision 0066). The
  SessionStart hook gives a new session `work status`; a PreCompact hook logs the compaction and asks for a hand-off.
- **`measure initiative`** gives each session's round trips, tool uses, dispatches and compactions, and whether the
  request behind the initiative was internal or external.
- **`work run`** delivers a work-item whose requirements are all of guarantees capabilities; a researcher's limit is
  80 turns; `work start` commits the initiative; `work add` refuses a done initiative; `work answer
  <initiative>/<name>` names a node of one initiative.
- **`model check`** reads requests: a request's form, an initiative dated after 2026-10-23 that fulfils none, a request
  neither part of a job-thread nor citing an origin, a delivered request naming a requirement the spec lacks.
- **Skills**: `delivering-an-initiative` starts `work run` and shows what it printed; `integrating-a-proposal` and
  `formulating-features` have no small-change path: every change goes through rounds.

Upgrading a consuming repository from 0.25.0: update the plugin and start a session; accept the offered upgrade (or
run `migrate upgrade` with a clean checkout). There is no file to rewrite: initiatives dated before 2026-10-24 need no
request, and a ledger under `.shop/scratch/` stays where it is while new lines go to the initiative's `ledger.md`.

## 0.25.0: work-items side by side, answers, and guarantees

- **`work run` runs work-items side by side** (supervision r59-r63): research and plan stages of independent
  work-items start at the same time, up to `workers` in `.shop/delivery.toml` (4 where it gives none). Implementers'
  branches merge one at a time. A work-item whose `blocked_by` names one that is not `green`, in any initiative, gets
  no worker. Each stage's `session.json` records the path of its transcript.
- **Answers, not rulings** (decisions 0063, 0064): the status `awaiting-ruling` is `awaiting-answer`.
  `work answer <work-item> <answer>` (or `<initiative>/<name>`, naming the initiative) writes a one-line answer under the work-item's `## Answers` and returns it to the
  status the stage that asked started from, so `work run` takes it up again. On an awaiting-answer capability-proposal
  it writes the answer under the proposal's `## Answers` and commits the proposal's file alone.
- **Workflow capabilities are guarantees** (decision 0065, superseding 0030 and 0043): the ten workflow capabilities
  have no scenarios and are checked by `measure` on real batches.
  `--work-item` still refuses a work-item with no scenarios: deliver such a work-item outside `work run`.
- **`measure`** counts round trips, reads an empty `session.json`, Unicode line breaks in transcripts and times
  ending in `Z`. The analysis tools answer with `--json`.
- **`model check`**'s own gaps are fixed; a capability-proposal argues one capability.
- **`delivering-an-initiative`** lists a proposal's `## Retires`, and stops before drafting when the formulation
  added or reworded a scenario that no requirement of the initiative accepts.
- **`tools install` pins ruff**; `tools check` is clean.
- **Design model v4** is written in `docs/design-model/`: requests are the one way work enters a bounded context.
  `model check` still checks the v3 rules until a later release implements v4.

Upgrading a consuming repository from 0.24.0: update the plugin and start a session; accept the offered upgrade (or
run `migrate upgrade` with a clean checkout). Its step "answers, not rulings" renames `awaiting-ruling` to
`awaiting-answer` in work-items and `log.jsonl`, and `## Rulings` to `## Answers`.

## 0.24.0: work-items named by ids, and upgrades between plugin releases

- **Work-items are named by ids** (decision 0061): `work add <initiative> <title>` drafts `w<n>`, `<n>` one above the
  highest of any work-item in the bounded context, writes the title as its heading and prints the id. Every command
  that names a work-item takes the id (`work retry`, `work withdraw`, `--work-item`, `work run`'s branches and stage
  directories). `model check` prints a work-item whose file is not `w<n>.md`, and two with one id.
- **Upgrades between plugin releases** (decision 0062): a repository records its plugin version in
  `.shop/plugin-version` (none means 0.23.1). `migrate status` prints the repository's version, the plugin's and each
  pending upgrade step; `migrate upgrade` applies them, records the version and commits it all in one commit, and
  refuses on uncommitted changes. When a session starts, the plugin's SessionStart hook offers the person the upgrade
  when a step is pending, and asks for a plugin update when the repository is ahead of it.
- **The first upgrade step**, "work-items named by ids": every work-item becomes `w<n>`, numbered by initiative and
  then file name; its file and `runs/` directory are renamed, its old name kept as its heading, and its name rewritten
  in its initiative's `log.jsonl` and in every work-item's `blocked_by`, `depends_on` and `for`.
- **A researcher's limit is 40 turns** (supervision r19), up from 25: researchers that finished used 14 to 30.

Upgrading a consuming repository from 0.23.x: update the plugin and start a session; accept the offered upgrade (or
run `migrate upgrade` with a clean checkout). Scripts or skills that call `work add <initiative> <name>` now pass a
title and read the printed id.

## 0.23.1: `--work-item` keeps tests that are not scenarios

- **`--work-item` keeps tests that are not scenarios** (supervision r55, r56): the option `work run` gives every
  worker's pytest now keeps a probe file or a script's test it collects, deselects only the scenarios the work-item
  does not accept, and refuses only a run that collected scenarios and none the work-item accepts. A researcher's
  probes run again, the cause of research stages ending at their turn limit since 0.22.0
  (`.shop/records/measurements/2026-10-22-research-at-the-limit.md`).
- **Still known**: work-item names repeat across initiatives, and `--work-item` takes the first initiative's
  work-item of a name; 0.24.0 gives work-items `w<n>` ids.

Upgrading a consuming repository from 0.23.0: a worker's `python3 -m pytest -q` under `--work-item` now also runs the
repository's tests that are not scenarios; nothing needs to change.

## 0.23.0: faults settled, query output as JSON, the session keeps the gate, measurement on v3

- **Faults settled** (the 0.22.0 review's deferred findings, decision 0057): a fault decides a work-item's status
  whatever its worker's outcome; a session that exits with an error or prints no JSON result is a fault;
  `work withdraw <work-item>`; `work retry` returns to the status `log.jsonl` gives before `failed`; the branch
  review's directory is kept under `.shop/work/<initiative>/runs/branch-review/<k>/`, committed, logged and pushed,
  and not run again while only its own commit is new; a run first pushes an initiative branch that is ahead of its
  remote; a run with a `failed` work-item exits with an error naming each fault. The glossary gains fault, remote and
  work-item branch.
- **Query commands answer in their output** (decision 0058, superseding 0055): `--json` prints a query's whole
  result as one JSON object for `features list`, `deprecated` and `bindings`, `model why` and `rules`, and
  `work show`; a query that finds nothing exits successfully (`features list`, `model why`). The `tools` query
  commands follow in a later release.
- **The session keeps the gate** (decision 0059): `initiative-round` gains a `gate` job and appends to the
  initiative's ledger; `delivering-an-initiative` sends fixes through `work run` and new scenario rows to the blind
  formulator; a new agent, `trial-runner`, runs one trial and writes a measurement record.
- **Measurement on v3** (decision 0060): `measure initiative <initiative>` measures an initiative's deliveries from
  `work run`'s log, the stages' sessions and git, with `--sessions` for the sessions around them; `measure show` and
  `measure compare` read the records. The old `measure batch` is removed; `analyzing-a-batch` follows.
- **Known**: a researcher under `work run` can end at its turn limit, because the `--work-item` option `work run`
  gives every worker's pytest refuses the researcher's probe files
  (`.shop/records/measurements/2026-10-22-research-at-the-limit.md`); work-item names repeat across initiatives.
  Both are next. Until then, deliver a work-item whose researcher fails by a direct `bdd-implementer`.

Upgrading a consuming repository from 0.22.0: scripts that read the exit of `features list` or `model why` on an
empty answer now see success (read the output, or use `--json`); records written by the old `measure batch` cannot be
read by `measure show` (measure an initiative instead); nothing else needs to change.

## 0.22.0: one requirement per scenario, faults, and the lessons of a blind formulation

- **One requirement per scenario** (decision 0054): a scenario names exactly one `@r<n>`; `model check` reports a
  scenario naming more (v_s2); `features tag` replaces the requirement tag. Steps are shared in code.
- **Exits in words** (decision 0055): a line and its scenario say a command exits successfully or with an error;
  exit codes live in a capability's Implementation section.
- **Faults** (decision 0056): `failed`, `work retry`, a push check before every worker and a push after every commit,
  worktrees removed on exit, a session ending in an error or at its turn limit is a fault, results start as
  `PARTIAL`, and expected red before a merge. `work add` and `work retry` commit what they change.
- **Small work-items**: `delivering-an-initiative` gives a work-item at most five requirements.
- **The spec's language**: a glossary in which each term has one meaning (run, delivery, stage directory, status,
  outcome, result, brief, input, template, transition, failed, ...), and five lessons in `docs/capability-format.md`
  that the spec-checker and the reviewers check (spec-consistency r22-r27, review r29-r30).
- **Records**: formulators' questions, reviews, run reports and gate verdicts kept under `.shop/records/`; bulky
  data (slim transcript exports) in a separate records repository, scanned by gitleaks before every push.

Upgrading a consuming repository from 0.21.0: give its initiative branches a pushable remote and run `work run` with
your push credentials; split any scenario that names two requirements (`model check` lists them under v_s2); reword
scenario steps that name exit codes as "exits successfully" or "exits with an error"; commit `.shop/work/` before each
`work run`.

## 0.21.0: the final layout and delivery by `work run`

What changes for a consuming repository:

- **The layout.** `spec/` (with `decisions/` one file a decision, where 0.20.0 had the ledger
  `spec/decisions.md`), `features/`, and `.shop/` for work, records, scratch and worktrees. `docs/superpowers/`
  and top-level `decisions/`, `work/` and `records/` are gone; `model` reads only the new layout.
- **Delivery is v3.** Slicing, slice plans, lanes and steps, `scripts/plan` and the `slicing-into-increments` skill
  are removed, and so is the dependency on superpowers (design-decision/superpowers-not-a-dependency).
  An initiative's work-items are drafted by `delivering-an-initiative` and delivered by `work run`.
- **EARS.** Behaviour lines are EARS requirements with "shall"; `model check` reports any that is not.
- **`migrate run`** makes every mechanical change of the move in one run, or none: moves, decision files from the
  ledger, ids, `@holding` scenarios to `@deprecated`, rewritten references.
- **pytest-bdd and xdist.** The plugin's scenarios run as pytest-bdd step definitions, every scenario bound
  exactly once (`features bindings --unbound`), in parallel under pytest-xdist.
- **`tools size`.** Tracked Python files stay at 300 lines or fewer; `tools size --limit 300` lists those over it,
  and the reviewers run it.

To upgrade: install 0.21.0, `python3 -m pip install clingo pytest pytest-bdd` (and pytest-xdist), and from a clean
checkout with nothing in progress ask Claude to migrate the repository: the `migrating-to-capabilities` skill runs
`migrate run`, re-pairs what needs judgment, and stops at its one gate. Then git-ignore `.shop/scratch/` and
`.shop/worktrees/`, and give pytest a `--work-item` option or set `[tests]` in `.shop/delivery.toml` before the first
`work run`. Earlier releases' notes are in git's history of this file.
