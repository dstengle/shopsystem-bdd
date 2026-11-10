# Changelog

What changed in each release of shopsystem-bdd, newest first. Each section is the release's note as it was written
when the release shipped, so older sections use the words of their day: a command or file an old note names may have
been renamed or retired since.

- Upgrading from 3.x? The steps are in [Upgrading from 3.x to 4.0](docs/upgrading.md); `migrate upgrade` applies
  every pending step in order.
- New here? Start at the [README](README.md).

| Line | Releases |
|---|---|
| 4.x | [4.0.0](#400-the-controlled-language-4) |
| 3.x | [3.0.1](#301-features-generate-writes-the-scenario-of-a-negated-response-with-a-recipient) · [3.0.0](#300-verb-frames-parts-of-speech-in-the-glossary-and-verbs-typed-by-kind) |
| 2.x | [2.4.0](#240-the-request-watch-wakes-on-githubs-events-and-starts-with-the-session) · [2.3.1](#231-a-batch-runs-in-one-fresh-agent-and-a-parked-item-leaves-the-batch-at-once) · [2.3.0](#230-work-pushes-its-commits-requests-post-after-they-commit-and-work-watch) · [2.2.0](#220-decisions-and-records-written-by-command) · [2.1.0](#210-requests-exchanged-through-github-issues) · [2.0.0](#200-the-workflow-simplified) |
| 1.x | [1.0.0](#100-codified-requirements) |
| 0.x | [0.29.0](#0290-glossary-proposals-delegations-given-late-and-fewer-stops-from-outside-a-work-item) · [0.28.3](#0283-a-branch-review-that-runs-nothing) · [0.28.2](#0282-answers-a-round-cannot-hold-go-back-to-integration) · [0.28.1](#0281-work-run-stops-visibly-on-questions-and-spends-less-agent-time) · [0.28.0](#0280-one-set-of-request-commands-work-list-and-work-show-and-answers-that-redraft) · [0.27.0](#0270-transitions-from-how-a-session-ended-and-the-turn-of-an-accepted-request) · [0.26.0](#0260-requests-and-the-context-loop) · [0.25.0](#0250-work-items-side-by-side-answers-and-guarantees) · [0.24.0](#0240-work-items-named-by-ids-and-upgrades-between-plugin-releases) · [0.23.1](#0231---work-item-keeps-tests-that-are-not-scenarios) · [0.23.0](#0230-faults-settled-query-output-as-json-the-session-keeps-the-gate-measurement-on-v3) · [0.22.0](#0220-one-requirement-per-scenario-faults-and-the-lessons-of-a-blind-formulation) · [0.21.0](#0210-the-final-layout-and-delivery-by-work-run) |

## 4.0.0: the controlled language 4

- **One language, grammar 4** (b112, b240; design `.shop/records/2026-11-09-cnl-4/`): a requirement line is read by a
  grammar over GF's resource grammar library, generated per context from its glossary, and has one meaning or is
  refused (`model parse` names why: a verb's frame, a verb's aspect, two readings, a reading rule). A file says
  `language: codified-2`; the old grammar of `codified-1` is gone, and `model check`, `features generate`, the
  readiness bar and the request lines refuse a `codified-1` file, naming `migrate upgrade` (design-model-check r287).
- **The glossary**: a verb says its aspect, `(verb, action)` or `(verb, state)`: an action in a trigger or a
  response, a state in a While clause or a relative clause (v_t14). Packs of words are imported by `spec/index.md`
  (`imports: [cli, time]`): `cli` (tool, command, option, run, print, exit, refuse, name, conform), `time`, `spec`;
  a word of the context's own spelled as a pack's carries `Redefines: <pack>` (v_t16). A relation row's word is a
  preposition or a role noun.
- **The reading rules R1-R12 and the logical form** (`grammar/language.md`): what "a", "the", "no", "every", "only",
  "its", "one" and a negated clause mean, checked on every line; `model parse --form` prints a line's referents,
  atoms and boxes; `model explain <cap>#r<n>` what the other lines force with it. `model logic` reads the form (L1-L7,
  L8: a Then other lines entail); `features generate` writes the steps from it in the step grammar 4.
- **New constructs** (`grammar/constructs.md`, each a code `model constructs` checks): conformance to a named
  artifact, ordered comparison ("after `3.0.0` and before `4.0.0`"), value sets and a value's absence ("is one of",
  "has no"), the number of Ks, identity and distinctness ("another", "two", "the same"), existence, a command's
  options in the trigger ("runs `x` with the `--json` option"), the run's own things ("this K", `This:`), counts,
  modality ("may", "always", "never") and time (the time pack).
- **Example data out of lines**: a code or quoted string that names no declared constant is a parameter, bound in
  its group's given block (`w_example`).
- **`migrate upgrade` 4.0.0, "the controlled language 4"** (b161, migration-tools r61): writes each file's marker
  `codified-2`, imports the CLI pack when a line uses its words, and gives each verb its aspect where its lines
  decide it. It prints, by file and id, what a session rewords: each line grammar 4 refuses with the reason ("the"
  with no antecedent and a negated indefinite in a While clause among them), each condition (adjective) and the
  lines using it (grammar 4 reads no adjective: say the state with a structure), each line holding example data,
  each "exit with an error naming" ("refuse the command and name" says it shorter), each verb whose aspect its lines
  do not decide (v_t14), each relation row of no cardinality on of, for, with, on or in (the old check read it as
  one: write `one` where one is meant) and each term the CLI pack defines too (v_t16). It rewords no line. After it,
  reword each line it names under a new id with its old id in `retired:`; then run `model check`, `model logic` and
  `features generate`.
- **Known limits** (`grammar/language.md`, "What the language cannot say yet"; a corpus line traces `Known limit:
  #<n>`): #3 one above the highest; #6 a value compared with another thing's value; #8 a change of an attribute's
  value; #10 for each X its Y, each of the Ks, one thing counted for each of another's; #11 the outcome of the
  response's own act; #12 an option set to a value of an attribute; #13 what a command would write; #14 ordered
  choice and up to a number in rank order; #15 an adjunct of a verb's frame; #16 liveness, an answer within a time,
  history and moments in `model logic` and `features generate`; #17 a default value; #18 the ratio of two figures.

## 3.0.1: `features generate` writes the scenario of a negated response with a recipient

- **A negated response with a recipient gets its scenario** (b103, feature-file-tools r20): "`feed` shall not return
  the video to the caller" is written as the Then "`feed` does not return the video v1 to the caller c1" (the step
  template `ThenDoesToNot`). In 3.0.0 its group got no scenario and `model check` reported v_s3. Run `features
  generate` again, and give a consumer's `ThenDoesToNot` steps their handler.
- **No upgrade step.**

## 3.0.0: verb frames, parts of speech in the glossary, and verbs typed by kind

- **Every glossary term names its part of speech** (b83, design-model-check r67): `(noun)` for a kind, `(proper
  noun)` for an actor, `(adjective of <kind>)` for a condition, `(attribute of <kind>)` for an attribute with values,
  `(noun, exclusive)` for a resource and `(verb)` for an event. Plugin 2.x's categories (`kind`, `event`,
  `condition of …`) are refused, each term named with the label it is to carry.
- **A verb's entry gives its frame** (b82, r60): a `Frame:` field in the order the verb is read, its kinds glossary
  terms: `Frame: caller requests video.`, `Frame: feed returns video to caller.`, `Frame: session ends.`. `model check`
  refuses a verb with no frame (v_t11), and a condition whose definition names another kind (v_t12): a relation
  between two kinds is a verb between them. `model parse` refuses a line whose verb is missing its object (r58) or its
  recipient (r59), naming the verb.
- **Verbs typed by kind** (b84, r63): the generic verb funs are gone; each verb's subject, object and recipient take
  a noun of the frame's kind or a kind under it (`Kind of:`). A line that gives a verb a noun of another kind is
  refused, naming the term.
- **Verbs in conditions, positive and negated** (b85, r64): "a user does not subscribe to a channel" parses. **The
  passive with no agent is refused** (r65): "a channel is not subscribed" names no subscriber; the active clause is
  the one form.
- **A trigger with a recipient** (b86, r66): "when a feed returns a video to a caller", object then "to" recipient,
  the one order.
- **`migrate upgrade` 3.0.0, "verb frames"** (b87, migration-tools r25): writes each glossary entry's and each
  capability term's category as its part of speech, and prints each verb that needs a `Frame:` (v_t11), each
  relational condition (v_t12) and each requirement that no longer parses, by file and id. It rewords no line. After
  it, give each verb its frame, write each relational condition as a verb, and reword each line it names, a changed
  line under a new id with its old id in `retired:`; then run `model check`, `model parse` and `features generate`.

## 2.4.0: the request watch wakes on GitHub's events and starts with the session

- **`work watch --forward`** (b78, requests r57, r58) wakes on GitHub's events instead of a 60-second poll. On each
  repository the account administers, it forwards the repository's issue and comment events to a local port with
  `gh webhook forward` (the `cli/gh-webhook` extension). On the others, such as an upstream's repository, it polls
  GitHub's notifications, which cost no rate limit when nothing changed. `--every` is then the longest wait. It
  prints each comment a request does not hold and each new ask, then exits, as `work watch` does.
- **The skills start the watch with Claude Code's Monitor tool** (raising-a-request, taking-in-a-request,
  building-a-batch), and start it again after each `work sync`.
- **A SessionStart hook names the requests waiting on the other side** (b79, requests r54-r56): `request_hook watch`
  (`work watch --hook`) prints each sent request awaiting the upstream and each received one awaiting the asker, so a
  new session starts the watch. It prints nothing when every request is closed, and never fails a session start.
- **No upgrade step.**

## 2.3.1: a batch runs in one fresh agent, and a parked item leaves the batch at once

- **A batch runs in one fresh agent** (b55, batches r14): `work batch start` writes a batch brief,
  `batch-<n>-driver/brief.md` under the worktrees directory (never committed), and prints its path. The session hands
  that brief to one fresh agent, which runs the batch to a clean pull request (building-a-batch, step 2). An optional
  `[batch] push` in `.shop/delivery.toml` gives the prefix the brief puts on every push and gh call.
- **A parked item's lines leave at once** (b47, batches r17, r18): `work batch park` takes the item's lines out of
  `batch-<n>`, and `work batch done` runs a task's tests with every parked item's lines out, so a park no longer
  breaks the other tasks.
- **`work batch merged` and `abandon` remove the batch's folders** (b58, batches r15, r16): each
  `batch-<n>-review-<k>` folder, and the driver's brief folder.
- **`work sync` applies only the poster's side of a comment** (b35, requests r52, r53): every comment is still
  recorded, but a late comment no longer changes a delivered, refused or withdrawn request.
- **No upgrade step.**

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
  `spec/index.md` is typed (`- **<term>** (<part of speech>): …`) and is the lexicon of a GF grammar; every Behaviour
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
