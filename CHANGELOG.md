# Changelog

What changed in each release of shopsystem-bdd, newest first. Each section is the release's note as it was written
when the release shipped, so older sections use the words of their day: a command or file an old note names may have
been renamed or retired since.

- Upgrading? The steps, and the old and new numbers of the releases renumbered in 0.34.1, are in
  [Upgrading](docs/upgrading.md); `migrate upgrade` applies every pending step in order.
- New here? Start at the [README](README.md).

| Line | Releases |
|---|---|
| 0.42 | [0.42.0](#0420-a-request-acts-on-one-thing-one-verb-for-several-operations-and-a-made-thing-introduced-by-the-when) |
| 0.41 | [0.41.0](#0410-a-fresh-contexts-scenarios-run-with-plain-pytest-and-a-responses-owned-thing-given-before-the-when) |
| 0.40 | [0.40.0](#0400-a-new-context-built-by-command-and-the-docs-as-prompts-to-the-session) |
| 0.39 | [0.39.0](#0390-each-operation-carries-its-lines-the-catalogues-as-specification-migrate-init-and-the-docs-revised) |
| 0.38 | [0.38.0](#0380-the-domain-contract) |
| 0.37 | [0.37.0](#0370-whole-spec-faults-caught-before-a-batch-chores-new-capabilities-by-command-and-model-logics-precision) |
| 0.36 | [0.36.0](#0360-migrate-records-the-version-orders-after-any-act-line-commands-groomed-ideas-and-requests-resolved-offered-and-confirmed) |
| 0.35 | [0.35.1](#0351-collections-on-any-responses-object) · [0.35.0](#0350-collections-comparisons-and-orders) |
| 0.34 | [0.34.1](#0341-the-version-reset-and-the-givens-of-a-triggers-referents) · [0.34.0](#0340-released-as-410-value-kinds-adjective-or-noun-and-gherkin-in-the-full-form) |
| 0.33 | [0.33.0](#0330-released-as-400-the-controlled-language-4) |
| 0.32 | [0.32.1](#0321-released-as-301-features-generate-writes-the-scenario-of-a-negated-response-with-a-recipient) · [0.32.0](#0320-released-as-300-verb-frames-parts-of-speech-in-the-glossary-and-verbs-typed-by-kind) |
| 0.31 | [0.31.5](#0315-released-as-240-the-request-watch-wakes-on-githubs-events-and-starts-with-the-session) · [0.31.4](#0314-released-as-231-a-batch-runs-in-one-fresh-agent-and-a-parked-item-leaves-the-batch-at-once) · [0.31.3](#0313-released-as-230-work-pushes-its-commits-requests-post-after-they-commit-and-work-watch) · [0.31.2](#0312-released-as-220-decisions-and-records-written-by-command) · [0.31.1](#0311-released-as-210-requests-exchanged-through-github-issues) · [0.31.0](#0310-released-as-200-the-workflow-simplified) |
| 0.30 | [0.30.0](#0300-released-as-100-codified-requirements) |
| 0.29 and before | [0.29.0](#0290-glossary-proposals-delegations-given-late-and-fewer-stops-from-outside-a-work-item) · [0.28.3](#0283-a-branch-review-that-runs-nothing) · [0.28.2](#0282-answers-a-round-cannot-hold-go-back-to-integration) · [0.28.1](#0281-work-run-stops-visibly-on-questions-and-spends-less-agent-time) · [0.28.0](#0280-one-set-of-request-commands-work-list-and-work-show-and-answers-that-redraft) · [0.27.0](#0270-transitions-from-how-a-session-ended-and-the-turn-of-an-accepted-request) · [0.26.0](#0260-requests-and-the-context-loop) · [0.25.0](#0250-work-items-side-by-side-answers-and-guarantees) · [0.24.0](#0240-work-items-named-by-ids-and-upgrades-between-plugin-releases) · [0.23.1](#0231---work-item-keeps-tests-that-are-not-scenarios) · [0.23.0](#0230-faults-settled-query-output-as-json-the-session-keeps-the-gate-measurement-on-v3) · [0.22.0](#0220-one-requirement-per-scenario-faults-and-the-lessons-of-a-blind-formulation) · [0.21.0](#0210-the-final-layout-and-delivery-by-work-run) |

## 0.42.0: a request acts on one thing, one verb for several operations, and a made thing introduced by the When

- **A request acts on one thing** (b420, parsing#r13-r16): a verb names an operation by each of its frames, so
  "the person lists a checklist" and "the person lists the checklists" are two requests of one word, each read one
  way. A request's object is one thing: a line whose request has a plural object ("the person deletes two
  checklists") no longer parses and is refused naming the line; a collection is said by the frame's own words. A
  line that reads two ways is refused naming the words that read two ways and, where two frames of a verb read
  them, each frame. Lines of the old form need rewording: say the collection in a frame of its own.
- **measurement#r4 and #r8 retired for #r10 and #r11** (b420): `measure compare` of two batches, and of two
  measurements, is one request returning two measurements (or two total rows) and a ratio.
- **One verb for several operations** (b429): shaping keeps the person's verb and gives it a second entry with a
  frame that tells it apart, never a coined verb; [recipes](docs/recipes.md#one-verb-for-several-operations) shows the
  entries and their lines.
- **A request can name a value another thing has** (b418, parsing#r17, #r18, consistency#r34, scenarios#r36-#r43): a
  line can say that a request names a title another checklist has (a value in use, `param-of`), not only an example
  value; its logical form keeps it, `spec logic` reads it and a code of the same value as one request, and the
  generated scenario gives the code to a Given and to the When. [Recipes](docs/recipes.md#refuse-a-value-already-in-use)
  shows it.
- **Generated features of operations that make their object change once** (b418, scenarios#r37): the thing an
  operation makes is introduced by the When ("the person adds the checklist c1 ..."), not by a Given, so the scenario
  no longer says the thing exists before the request that makes it. Regenerate your features
  (`features generate`) after upgrading; handlers that keyed on a Given of the made thing take it from the When.
- **`migrate upgrade` rewrites an old scenario conftest** (b423, upgrades#r36, #r37): a `tests/scenarios/conftest.py`
  that is still the form `migrate init` wrote before 0.41.0 is rewritten to the one that loads `work_items`, so plain
  pytest warns of no unknown mark; a conftest of neither form is named and left alone.
- **A response's thing owned by an indexical or a While part's thing is brought in before the When** (b421,
  scenarios#r34, #r35): "the items of this backlog" and the like get a Given and its row, so no step names an
  instance no Given introduces.
- **The prompt hook keeps the session in a repository `migrate init` founds in that same turn** (b417): `work quote`
  works on the person's first words in a fresh repository with no `--transcript`.
- **A decision may cite the person's words** (b435): `spec check` resolves a `quote-<n>` in a decision's `source` to
  `.shop/quotes/<n>.md` when that file is kept.

## 0.41.0: a fresh context's scenarios run with plain pytest, and a response's owned thing given before the When

- **A response's thing that a trigger's thing has is brought in before the When** (b416, scenarios#r33): for a line
  such as "return the items of the checklist", `features generate` writes the item and its row to the checklist as
  Givens before the When, so no step mentions an instance no Given introduces.
- **A fresh context's scenarios run with plain pytest** (b419): the plugin's pytest plugin `work_items` registers
  each `@g<n>` and `@r<n>` tag of the context's `features/*.feature` as a mark, and the `tests/scenarios/conftest.py`
  that `migrate init` writes loads `work_items` itself, finding the plugin's scripts on `PYTHONPATH`, else in
  `$CLAUDE_PLUGIN_ROOT`, else in the plugin cache's folder of the release `.shop/plugin-version` names. Plain
  `python -m pytest` then runs the scenarios with no unknown-mark warning and an unbuilt scenario as a strict
  expected failure; [getting started](docs/getting-started.md) shows that command. A context founded before 0.41.0
  keeps its old conftest (b423).
- **A Given of a text attribute's value says its code** (b413): a value no entry lists, such as a title, is written
  "the title of the checklist c1 is `groceries`", not as a placeholder.
- **`work line --into` a capability no file holds names `--capability`** (b414): the refusal says a new capability
  is given to an item with `work line <item> --capability <name>`.
- **`migrate init` with no git identity is refused before it writes** (b415), naming `git config` and saying to ask
  the person for their name and email.

## 0.40.0: a new context built by command, and the docs as prompts to the session

- **A new capability on an item takes model lines and vocabulary entries** (b387, b354): `work line --into
  <capability> --model ...` and `--term ...` keep them on the item for a capability the item itself adds with
  `work line --capability`, in the area its block names, else its own name; the lay makes `spec/model/<area>.md`
  when the context has none, and the unlay takes it out again. Nothing under `spec/model/` or `spec/vocabulary/` is
  written by hand, from `migrate init` to `work ready`.
- **A new capability is laid in 0.38's form** (b391): its file says `area:` and `specifies:` and holds no empty
  `## Terms`; `spec/index.md` keeps one `## Composition` whose `| area | kind | capabilities |` table names it in its
  area's row. An index still in the old `| capability | narrator | group |` tables is written in that form, its
  other subsections (a retired list) kept, and the unlay puts it back byte for byte.
- **`tools install` and `tools probe` in a project with no source file yet** (b388) reach the grammar tools: probe
  prints the grammar block and says the analysis tools are not probed, install installs GF, pgf, clingo and the RGL;
  a virtualenv's files are not the project's.
- **The lay writes the construct catalogue only for a line that cites a construct** (b390): a code counts as a
  citation after "uses" (or in its list), not as a backticked value such as a status `done`.
- **A fresh context's first batch** (b389): the batch brief runs the acceptance tests with `-p work_items` and, for a
  context with no step bindings or no `spec/adapters/cli.toml`, says how the first task makes the bindings, the
  program and the adapter contract, and that `work batch review` needs a remote and gh.
- **The user docs lead with prompts to the session** (b397): the [README](README.md) and
  [getting started](docs/getting-started.md) say what the person says and what the session does, not commands they
  run; the commands are in the [command reference](docs/reference/commands.md#how-the-commands-are-run). shaping-items
  sets up a repository with no spec (`tools install`, `migrate init`, the first capability by `work line`) and writes
  0.38's model lines, relations and vocabulary entries.

## 0.39.0: each operation carries its lines, the catalogues as specification, migrate init, and the docs revised

- **Each adapter contract's operation carries its business rules** (b368): `spec annotate` writes under each
  operation of `spec/adapters/cli.toml` the requirement lines that govern it (a line governs an operation when its
  trigger requests it), its refusals among them, as `requirements = ["<capability>#r<n>: <line>", ...]`; `--check`
  names a stale contract and writes nothing. `spec check` fails an operation that misses a governing line (`v_a5`)
  or holds one that no longer governs it (`v_a6`). [Adapter contracts](docs/reference/adapters.md).
- **The capability reading is renamed parsing** (b369), its construct-by-construct lines replaced by the language
  service's general behaviour: a line parsed to one meaning or refused naming why, its logical form returned, a line
  that uses a construct the construct catalogue has no entry of refused naming the construct.
- **The catalogues are specification** (b370): the construct catalogue (`grammar/constructs.md`) and the rule
  catalogue (`grammar/rules.md`) specify the language and the checks, each entry with a purpose, `Since:` and
  `Changed:` naming delivered items (or, for the 18 entries from before items were tracked, the release `0.38.0`, a
  section of this file), and its example as its test; the purposes and items are kept in
  `grammar/catalogue-entries.toml`. `spec check` holds them: `v_c1` a line naming a rule with no entry, `v_c2` an
  entry with no purpose, `v_c3` one naming neither an item nor a release, `v_c4` one naming an item not delivered.
  Checking's rule-by-rule lines are retired for general ones (a violation of an error rule fails the check naming
  the rule, a warning is named and the request completes). [The catalogues](docs/reference/design-model.md#the-catalogues-are-specification).
- **The documentation revised** (b371) around the specification's four parts (domain model, vocabulary,
  requirements, decisions), services and operations, adapters and their contracts, the catalogues and the records
  policy: the [README](README.md), [concepts](docs/concepts.md), [getting started](docs/getting-started.md), the
  references, recipes, upgrading and [the notes-cli example](docs/examples/notes-cli/README.md).
- **A new bounded context in one command** (b318): `migrate init --id <bounded context id>` writes and commits the
  context scaffold (`spec/index.md` in `language: codified-2` importing `request`, `spec/universal.md`, `spec/model/`,
  `spec/vocabulary/`, `spec/capabilities/`, `.shop/`, `features/` and `tests/scenarios/conftest.py`), refused where
  an index file or a shop directory exists. [migrate init](docs/reference/commands.md#migrate-init).
- **holds-exactly in a precondition** (b309) is read by `spec logic` and `features generate`, whose scenario brings
  in a thing outside the restriction that the collection does not hold.
- **An order on a collection orders its members** (b334): "print a worktree that holds a file, ordered by version,
  in descending order" puts the `ordered` atom on the files the worktree holds, in an every box, not on the worktree.
- **Fixes**: `backlog_lines.renumber` keeps an item's model blocks (b378); the readiness bar and the batch's lay
  annotate the adapter contract on the laid copy, so an item adding service lines is no longer refused with `v_a5`
  (b379).

## 0.38.0: the domain contract

A requirement used to say how a command-line tool is run: "When the person runs `work shape` on the item, `work`
shall ...". The business rule and its one interface were one sentence, so the rule could not outlive the interface.
0.38.0 separates them, ports and adapters: the specification is the domain's (a model, a vocabulary, requirements
and decisions), and each interface is an adapter with its own contract.

- **The domain model** (`spec/model/<area>.md`): one file per area of a bounded context (core, supporting or
  generic), a ` ```model ` block of its objects with their attributes, lifecycles and relations, its services with
  their operations (parameters, the kinds of outcome, the refusal reasons), its events and actors; the structure,
  no rules. `spec check` holds it to itself (`v_m8`) and every line to it: a word naming no element (`v_m1`), a
  parameter or value an operation does not declare (`v_m2`), a requester it does not allow (`v_m3`), a refusal reason
  no line states (`v_m4`), a transition no line causes (`w_m5`) or the lifecycle forbids (`v_m6`), an operation no
  line requests (`v_m7`). [The domain model](docs/reference/domain-model.md).
- **The vocabulary** (`spec/vocabulary/<area>.md` and `shared.md`): each word names one element of the model, `-
  **shape** (verb, action) → operation backlog.shape. Frame: <actor> shapes <item>.`; a frame is word order only, the
  kinds come from the model; one layer per area, so one word may name two elements in two areas. `## Glossary`, `##
  Terms` and `## Relations` are gone (`v_t18`-`v_t20` check the entries).
- **Operations with parameters in the grammar.** A verb that names an operation is a request, its parameters after
  its object: "When the person enters a design-decision with the tier `check`, ...", "If the person enters a
  design-decision without a tier, then the decisions service shall refuse the request and name the tier." The logical
  form says `request(e1, decisions.enter, ...)` with `param` and `noparam`; `spec logic` unifies two requests by
  operation and parameters, and names every kind by its model element, qualified by its area.
- **The request pack** (`grammar/packs/request.md`) replaces the CLI pack in every context's `imports:`: request,
  parameter, service, reason, response, check; refuse, name, return, notify, complete, fail, keep. The CLI pack's
  reading (a run with its options, the run frames, the bridge) stays live beside the request reading until b356, and
  `imports: [cli]` is refused only in a context with a domain model (`v_t21`); the upgrade scaffolds one.
- **The response envelope.** Every operation answers with `{outcome, content, errors, notices}`: `done`, `returned`,
  `refused`, `passed` or `failed` (a failure of the infrastructure, `broken`, is outside the domain), its errors
  naming business references (`parameter:tier`, `item:b12`). Every command takes `--json` and prints it.
- **The CLI adapter's contract** (`spec/adapters/cli.toml`): each operation's command, each parameter's option or
  place, how each outcome shows (exit 0 or 1, stdout or stderr), the hooks and the environment. `spec check` reads
  each program's argparse (in a process of its own) and holds the two to each other both ways (`v_a1`-`v_a4`). The
  protocol driver `tests/scenarios/driver_cli.py` makes a request through it and reads the envelope back; the
  generated scenarios do not use it yet: their request steps are re-keyed to the CLI handlers, which read text and
  exit codes, until b358. [Adapter contracts](docs/reference/adapters.md).
- **This repository's spec moved whole**: six areas (specification, tracking, execution, measurement, analysis,
  upgrades), 22 capabilities by service and lifecycle, every live line reworded under a new id, the old ids retired
  with a `## Moved` table and `spec/moves.json` (old id to new id, read wherever an old id is named). U12, U14 and U15
  are U17-U19 in request words; U13 and U16 retired into design-decisions. Mechanisms left the requirements for
  design-decisions: the CLI, GitHub issues, pull requests, git as the store, the files, the hooks, the envelope.
- **`model` is `spec`**: the command checks the specification, and "model" now means the domain model. `scripts/model`
  still works for this release, with a notice on stderr.
- **Records are kept, never cited**: a new item's `source:` naming a record is refused (`v_r1`; older ones warn,
  `w_r1`).
- **The upgrade step** 0.38.0 "the domain contract": `migrate upgrade` scaffolds the model, the vocabulary and the
  CLI contract from a context's glossary, relations and the commands its lines run, imports the request pack, and
  names by file and id each line a session rewords. [Upgrading](docs/upgrading.md#0380-the-domain-contract).
- **`work line` lays model lines and vocabulary entries** (`--model`, `--relation "<object>: <phrase> → <object>
  (<cardinality>)"`, `--term "<entry>"`) into `spec/model/` and `spec/vocabulary/` with the item's lines, through the
  readiness bar and `work batch start`.

### Breaking

- **Every line in 0.37's words is refused** until reworded: a command, an option, print or exit in a line does not
  parse (`v_p1`) or names no element (`v_m1`). `migrate upgrade` names each.
- **`imports: [cli]` is refused** in a context with a domain model (`v_t21`).
- **The `--json` shapes changed.** Each command that printed a JSON object of its own now prints the envelope, the
  old object under `content`: `work backlog`, `work batch status`, `work list`, `work show`, `spec rules`, `spec
  check`, `spec logic`, `spec restates`, `spec forms`, `features list`, `features deprecated`, `features bindings`,
  `tools probe`, `tools map`, `tools tests-of`, `tools untested`, `tools refs`. Read `.content` where you read the
  object.
- **`model` is `spec`.** The alias `scripts/model` goes in the next release.
- **The generated scenarios changed**: a When is a request ("When the person shapes the item i1"), a Then the
  response ("Then the backlog service refuses this request"); step handlers keyed on a command re-key on the operation.

## 0.37.0: whole-spec faults caught before a batch, chores, new capabilities by command, and model logic's precision

- **`work ready` refuses every model check violation its lines bring** (b333, PR #69): a laid item could break the
  whole spec (a group holding statements of different conditions, v15k and v15l; a 0.29 id no group restates once a retire removed
  its group) and nothing said so until every task of the batch failed its first `work batch done`. Now the readiness
  bar runs every rule of `model check` on the copy of `spec/` before and after the lay, and refuses each violation
  the lay brings that names one of the item's groups or requirements, naming the group and the rule; v15n, which
  0.36.0's bar ran alone (readiness#r49), is one of them (readiness#r58). `work batch start` does the bookkeeping in
  its lay's one commit, so no task writes it and no two tasks conflict over it, where the repository keeps these files: a block in `grammar/corpus/spec/` of
  each laid line with its logical form, the block of each retired id removed, `grammar/rules.md` and
  `grammar/constructs.md` regenerated, and a retire that removes a group writes each 0.29 id the group restated
  under `## Dropped`.
- **`work ready` names every failing line in one run** (b305, PR #66): it stopped at the first stage with a reason,
  so a line that did not parse hid another that `model logic` could not read, and two rewordings took three runs.
  Now every stage runs over every line (the parse, `model logic`, `features generate`), each line named by the first
  stage that refuses it.
- **A chore item** (b316, PR #67): an item with no behaviour a scenario checks (docs, a skill's text, a refactor)
  could not be readied, since the bar refused an item with no requirement line. `work chore b<n> --file <path>
  --check "<command>"` writes its `## Chore`, the files its work changes and the command whose exit 0 shows it done;
  `work ready` readies it with no line. `work batch done` runs the check in the task's worktree and refuses a commit
  of the task that touches a file the chore does not name; the batch briefs name the chore in place of ids. A chore
  and requirement lines exclude each other, and a path under `spec/`, `features/` or `.shop/` is refused.
- **A new capability by command** (b317, PR #67): a reader was told to write `spec/capabilities/<name>.md` by hand.
  Now `work line b<n> --capability <name> --narrator "<who>" [--group service|guarantees] "<purpose>"` writes it as a
  block of the item, refused when the capability exists; the bar lays it with the item's lines, and `work batch
  start` writes the file, its row under `## Composition` and its feature. `model forms --check` exits 1 naming each
  file form still written by hand.
- **Directives** (b20, PR #67): a short-term direction the person gives a session was kept nowhere but a session's
  memory. Now `work directive "<words>"` keeps the words as a quote and a `live` directive, `.shop/directives/<n>.md`,
  in one commit; `work directives` lists the live ones; a new SessionStart hook shows them to every session; `work
  promote directive-<n> --to <b<n>, a decision or CLAUDE.md>` and `work drop directive-<n> --why "<reason>"` review
  one, a directive not live refused.
- **Shaping several items at once** (b346, PR #69): `skills/shaping-items/parallel-brief.md` is the brief of one
  agent per item, run in parallel when each writes only its own item, and the shaping skill says when to use it.
- **No `git stash` in a batch** (b289, PR #69): every worktree of a repository shares one stash list, and two task
  agents' stashes were swapped. The batch brief's subagent rules and the batch skill now forbid it.
- **A parked item's lines taken out as they were laid** (b324, PR #69): an item parked and then reshaped on the
  base left its laid lines in a running task's tested tree, since they were cut by the item's new text, and the
  task's `work batch done` failed. Now they are taken out as `work batch start` laid them.
- **`work line --remove` keeps a retired id** (b323, PR #68): which line retires which id was read from commit
  subjects, so removing a line whose id was reused dropped another line's `retired:` id. The item's block now keeps
  `retires:` pairs, and `--remove` takes out only the id its own line retires.
- **A state verb in a response refused as the response's** (b175, PR #66): "... `model` shall unify the
  requirement." was refused as if the verb were in the trigger. Now the refusal names the response and the verb.
- **A closing comma after an order** (b301, PR #68): "give every file, ordered by version, in ascending order, to
  the person" did not parse at "to"; only the form with no comma before the recipient did. Now both read.
- **`model logic`'s precision** (b314, PR #66; b315, PR #67; b232, PR #68): no L1 between "return a
  worktree that holds nothing" (or "holds no file") and "shall not return a worktree that holds a file", whose
  objects no worktree meets both of (b314); a clash of "print a stage whose status is `open`" with "shall not print a
  stage whose status is not `done`" found (b232); holds-exactly on a response's object whose relative clause reaches
  a second thing ("... holds exactly the files that cover the line of a stage") read, where it was `unread` (b315),
  and its scenario gets the file outside the restriction.
- **A counter-example of a count on a written thing** (b296, PR #66): "write a file that holds at most three notes"
  got no Givens a program writing too many could fail. Now its scenario brings in one note past the bound.
- **Upgrading:** a y release (decision 0092): no upgrade step. `work ready` and `work batch start` now refuse an item
  whose lines bring any violation of a `model check` rule naming its group or requirement, not only v15n's shared
  condition and trigger: fix the group the refusal names. Run `features generate`: a count on a written thing and
  holds-exactly whose restriction reaches a second thing get new Givens and scenarios to write handlers for. New
  commands: `work chore`, `work line --capability`, `work directive`, `work directives`, `work promote`, `work drop`
  and `model forms --check`, and the SessionStart hook of the directives. A repository's tests pin
  `pytest==9.1.1` and `pytest-bdd==8.1.0`, as [Getting started](docs/getting-started.md) says: with pytest-bdd 9,
  `unbuilt:` ids are no longer marked as expected failures. See
  [From 0.36.0 to 0.37.0](docs/upgrading.md#from-0360-to-0370).

## 0.36.0: migrate records the version, orders after any act, line commands, groomed ideas, and requests resolved, offered and confirmed

- **`migrate upgrade` records the release** (b303, PR #61): on a repository behind the plugin's release with no
  upgrade step pending, it printed `no upgrade step is pending` and left `.shop/plugin-version` as it was, so
  `migrate status` kept showing the repository behind the plugin. Now it writes the plugin's version, commits and
  pushes it; with the two releases the same it still changes nothing.
- **Every over a negated value in a precondition** (b310, PR #61): "While every work-item is not `ready`, ..."
  crashed `model logic` and `features generate` (and so `work ready`). Now `model logic` translates it and the
  scenario's Givens meet it.
- **`work line --reword` and `--remove`** (b14, PR #61): `--reword <cap>#r<n> "<line>"` puts a new text in place of
  one of an item's own lines, keeping its id and group; `--remove <cap>#r<n>` takes one out, its group too when it
  was the last line. Each refuses an id that is no line of the item, a live requirement's among them.
- **`spec/universal.md` written in `codified-2`** (b203, PR #61): laying an item's universal conditions on a spec
  with no `spec/universal.md` (`work ready`, `work batch start`) wrote it as `codified-1`, so its conditions were
  read in no grammar and never checked. Now it is written as `codified-2`.
- **`work decision --supersedes`** (b179, PR #62): a decision is amended by a new one that names it; the old one is
  set `superseded` and committed with the new one. A decision not accepted, or an id that names none, is refused.
- **`work line --retires <cap>#r<n> --no-line`** (b271, PR #62): a live requirement retired with no line in its
  place, its id under the item's `retired:`.
- **"Every K, ordered by ..." after any act** (b300, PR #62; b328, PR #64): an order on a printed every read only
  after a verb whose frame takes `thing`, such as `print`; "return every video from the channel, ordered by ..." did
  not parse, and with a frame naming the collection's kind it got no scenario. Now it reads after any verb whose
  frame takes K, and gets its Then of the order and its counter-example. "Every K in the Y, ordered by T" after such
  a verb reads one way, with the order on the Ks (b328; 0.35.1 put it on the Y).
- **An idea is groomed before it is shaped** (b65, PR #63): `work shape` on an idea with no shaping note under
  `## Notes` and no `--note` shaped it all the same. Now it refuses, naming `--note`, and `work backlog` prints such an
  idea with `--note` beside it.
- **The readiness bar runs v15n** (b77, PR #63): an item whose group repeated another group's condition and trigger
  went `ready`, and `model check` found the two groups (v15n) only once the lines were laid on a batch. Now `work
  ready` refuses the item, naming its group and `v15n`.
- **The merge resolves the request** (b6, PR #63): `work batch merged` set each item `delivered` and left the request
  it was taken in from `accepted` until someone ran `work resolve`. Now it resolves each `accepted` request of a
  delivered item: the request `delivered`, its resolution written and posted, its issue closed. A request not
  `accepted` is left as it is and named, and so is one whose item was accepted before 0.36.0 (it records no request
  line): resolve those with `work resolve`.
- **The things a printed thing holds brought in** (b286, PR #63): the scenario of "print a worktree that holds a
  file" said "the worktree w1 holds the file f1" with no Given of either, and an order on a collection ("a worktree
  that holds a file, ordered by version, ...") added a fourth file beside the three members. Now both things are
  brought in by a Given before the When, and the file the line names is the first member.
- **Requests' output** (b39, PR #64): `work show <request>` prints each line's reason beside its outcome; `work sync`
  records a comment that does not conform to the comment form under the record's `## Comments`, applying nothing of
  it, and so prints it once, not on every run; `work offer`, `propose`, `reply` and `turn` print the request and its
  status; `work request` takes `--from` as optional, this context its default.
- **An offer quotes lines, not files** (b40, PR #64): `work offer --capability` pasted the capability file whole,
  frontmatter, prose and given blocks too, and the glossary with it. Now it quotes each named capability's groups
  and requirements and only the terms they mention; an offer with no `--capability` posts no glossary.
- **`work quote` finds a message sent mid-turn** (b52, PR #64): a message the person sent while the session worked
  is kept in the transcript apart from the prompts, and `work quote` refused its words. Now it quotes and cites it.
- **Upgrading:** a y release, because regenerated features change for lines that read the same (decision 0092):
  no upgrade step; `migrate upgrade` now records the release even when nothing is pending. Run
  `features generate`: a line that crashed it or got no scenario now gets one, and a scenario of a printed thing
  that holds another, or of an order on a collection, gains the Givens of both things ("a file f1", "a worktree w1"),
  for which a repository with no Given of those kinds writes a handler. An item already `ready` whose group shares
  another group's condition and trigger (v15n) is now refused at its next `work ready` or `work batch start`: put
  the two groups' lines in one. `work shape` now needs `--note` on an idea
  with no shaping note. An offer with no `--capability` posts no glossary. See
  [From 0.35.1 to 0.36.0](docs/upgrading.md#from-0351-to-0360).

## 0.35.1: collections on any response's object

- **Holds-exactly with a relative clause or a negated value, and holds nothing, on a response's object** (b297, PR #59): in 0.35.0
  holds-exactly on a response's object read only a value restriction ("a worktree that holds exactly the files whose
  version is `2.0.0`"); with a relative clause or a negated value ("... the files that a session keeps") `model logic`
  and `features generate` had no translation of it. Now its only half is read for a value, a negated value, or a
  relative clause over one row or state to a thing of its own ("that a session keeps", "that do not cover a line"),
  and its scenario gets the file that fails the restriction and the Then that the worktree does not hold it.
  "A worktree that holds nothing" on a response's object had no translation either; now `model logic` reads it and
  its scenario says "the worktree w1 holds nothing". Both hold on the object of any act, `print` or another.
- **An order on the object of any verb** (b298, PR #59): an order on a collection (`order-by`) had no scenario when
  the act's verb has a frame that names the collection's kind and no frame on `thing` ("return a worktree that
  holds every file, ordered by version, in descending order to the person"). Now it gets its Then of the order and
  its counter-example, as on `print`. An order after "every K" of such a verb is still refused or gets no scenario
  (b300, b312).
- **Holds no K on a response's object** (b299, PR #59): "a worktree that holds no file" on a response's object had
  no scenario ("no Then of not"). Now its Then says "the worktree w1 holds no file", after the act that brings the
  worktree in, and a counter-example brings in a file the worktree does not hold.
- **`work ready` refuses what `model logic` cannot read** (b307, PR #59): an item a requirement of which
  `model logic` names `unread` is refused, naming the requirement, where the bar passed it before.
- **Upgrading:** no upgrade step. Run `features generate` and write the handlers of the new scenarios; `work ready`
  may now refuse an item `model logic` cannot read. See [From 0.35.0 to 0.35.1](docs/upgrading.md#from-0350-to-0351).

## 0.35.0: collections, comparisons and orders

- **`model logic` reads what parses** (b272, PR #54): only and a count over a relation in a response ("print only
  worktrees that hold a file", "a batch that holds at most three items") are translated for `model logic` and
  `features generate`, and `model logic` names each requirement it has no translation of (`unread <id>: ...`)
  instead of printing `no findings` over lines it skipped.
- **Generated scenarios that can fail** (b273, PR #54): an every or only line's scenario gets a counter-example,
  the Givens of a thing that fails the restriction and a negated Then of it, which a program that ignores the
  restriction fails. A count on what a response prints gets one thing past an upper bound, and its Then states the
  count ("`notes` prints at most three notes"); a count that restricts a written thing gets none. An every in a
  condition, and two Ks, get the Givens that meet them.
- **Exact membership, nothing, and the member's side** (b274, PR #54): "a worktree that holds exactly the files
  whose version is `2.0.0`" (`holds-exactly`), "a worktree holds nothing" (`nothing`, no thing of any kind a row
  `K | in | S` lets it hold) and "a file is in a worktree" (`is-in`, the row read from the member's side).
- **The Thens of a response's thing after its act** (b268, PR #54): `features generate` writes the Thens that
  restrict a thing the response brings in after the act that brings it in, not before.
- **Value order, comparisons and orders** (b275, PR #55; b287, b288, PR #56): an attribute's value order is its
  `Order:` or the type its new `Type: number|time|text` declares, whose values are any literal of the type. Two
  things' values compare, "the release of this repository is after the release of `migrate`" (`value-compare`) and
  "is the same as" (`value-same`), also across two senses of one word whose entries have one value order. An order,
  ", ordered by <attribute>, in ascending order" or "in descending order", on a collection (`order-by`) or on a
  printed every (`order-by-every`), is kept as one atom; two opposite orders on one trigger are an L1, and the
  scenario gets a Then that states the order, which a handler checks by a sorted comparison. An order, or an
  after/before comparison, on an attribute with no value order is refused, naming the attribute.
- **An order only in what a response prints** (b285, PR #56): an order in a precondition, in the trigger, or in an
  act under "shall not" is refused, naming the order.
- **This repository**: migration-tools' release lines compare the repository's release with the release of
  `migrate` (r77, r78, r79 retired for r81, r82, r83: b284, PR #57), so they no longer take a new id when the
  plugin's release moves on.
- **Upgrading:** no upgrade step. Regenerate the features and update the step handlers they now need: see
  [From 0.34.1 to 0.35.0](docs/upgrading.md#from-0341-to-0350).

## 0.34.1: the version reset and the Givens of a trigger's referents

- **Versions are 0.y.z until 1.0** (design-decision 0092, b264): the releases made as 1.0.0-4.1.0 are renumbered into
  the 0.y.z series, continuing the tagged 0.1-0.29 releases. y counts a large or incompatible change (past .9 to .10),
  z a non-breaking update; 1.0.0 is a decision of its own. Each section below keeps the number it was released as in
  brackets. The upgrade steps of `migrate upgrade` are keyed by the new numbers:

  | released as | now |
  |---|---|
  | 1.0.0 codified requirements | 0.30.0 |
  | 2.0.0 the workflow simplified | 0.31.0 |
  | 2.1.0 requests exchanged through GitHub issues | 0.31.1 |
  | 2.2.0 decisions and records written by command | 0.31.2 |
  | 2.3.0 work pushes its commits | 0.31.3 |
  | 2.3.1 a batch runs in one fresh agent | 0.31.4 |
  | 2.4.0 the request watch wakes on GitHub's events | 0.31.5 |
  | 3.0.0 verb frames | 0.32.0 |
  | 3.0.1 the scenario of a negated response with a recipient | 0.32.1 |
  | 4.0.0 the controlled language 4 | 0.33.0 |
  | 4.1.0 value kinds | 0.34.0 |

- **A Given for each referent of the trigger** (b263, PR #51): `features generate` writes, after the Givens of the
  While and Where parts, a Given of each referent of the trigger's event not yet brought in
  (`scripts/spec_steps4.py`), so that every instance a When names has a Given that brings it in.
- **Upgrading:** `migrate` has no translation of an old number. A consuming repository rewrites its
  `.shop/plugin-version` by hand with the table above (a repository on 3.0.1 writes `0.32.1`), then reinstalls the
  plugin: Claude Code keeps installs by version and may not move from 4.1.0 down to 0.34.1. No upgrade step.

## 0.34.0 (released as 4.1.0): value kinds, adjective or noun, and Gherkin in the full form

- **An attribute declares its values adjectives or nouns** (b257): `Values (adjective):` lists the values that read
  after "is" as an adjective or a participle (`shaped`, `in-batch`), `Values (noun):` every other (a noun, a verb
  phrase, a release: `idea`, `needs-input`, `check`, `0.30.0`); one entry may give both. `model lexicon` prints each
  value with its kind.
- **The short form only for an adjective**: "an item is `shaped`" parses; "an item is `idea`" is refused, naming the
  full form, "the status of the item is `idea`" or "an item whose status is `idea`" (construct `adjective-value`;
  `attribute-is` is the full form, which any value takes). A plain `Values:` declares neither and keeps 0.33's
  reading, so nothing that parsed under 0.33 is refused until its attribute declares a value a noun; `model check`
  warns `w_value_kind` of each such attribute.
- **Generated Gherkin is always the full form**: `features generate` writes every value step as "the status of the
  item i1 is `idea`", whatever the value's kind, and a value of "no K" as "no item whose status is `idea` exists",
  so whoever binds a step reads the attribute in it. The step's template, kind and attribute are as before
  (`GivenK_A`, `ThenK_A`); a handler that read the thing out of the step's text reads `step.subject`. Regenerate
  the features after the upgrade (`features generate`).
- **This repository**: every attribute declared; 17 lines that said a noun or verb-phrase value in the short form
  (backlog r23, r24, r28-r31; batches r27, r33; decision-tiers r14-r17, r23; pr-review r4, r13-r15) reworded to the
  full form under new ids, the old ones retired.
- **Upgrade step 0.34.0 "value kinds"** changes no file: it names each attribute whose values are declared neither
  way and each line that says one of its values in the short form, by file and id, for a session to declare the
  values and reword each line whose value is a noun.

## 0.33.0 (released as 4.0.0): the controlled language 4

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
  artifact, ordered comparison ("after `0.32.0` and before `0.33.0`"), value sets and a value's absence ("is one of",
  "has no"), the number of Ks, identity and distinctness ("another", "two", "the same"), existence, a command's
  options in the trigger ("runs `x` with the `--json` option"), the run's own things ("this K", `This:`), counts,
  modality ("may", "always", "never") and time (the time pack).
- **Example data out of lines**: a code or quoted string that names no declared constant is a parameter, bound in
  its group's given block (`w_example`).
- **`migrate upgrade` 0.33.0, "the controlled language 4"** (b161, migration-tools r61): writes each file's marker
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

## 0.32.1 (released as 3.0.1): `features generate` writes the scenario of a negated response with a recipient

- **A negated response with a recipient gets its scenario** (b103, feature-file-tools r20): "`feed` shall not return
  the video to the caller" is written as the Then "`feed` does not return the video v1 to the caller c1" (the step
  template `ThenDoesToNot`). In 0.32.0 its group got no scenario and `model check` reported v_s3. Run `features
  generate` again, and give a consumer's `ThenDoesToNot` steps their handler.
- **No upgrade step.**

## 0.32.0 (released as 3.0.0): verb frames, parts of speech in the glossary, and verbs typed by kind

- **Every glossary term names its part of speech** (b83, design-model-check r67): `(noun)` for a kind, `(proper
  noun)` for an actor, `(adjective of <kind>)` for a condition, `(attribute of <kind>)` for an attribute with values,
  `(noun, exclusive)` for a resource and `(verb)` for an event. Plugin 0.31's categories (`kind`, `event`,
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
- **`migrate upgrade` 0.32.0, "verb frames"** (b87, migration-tools r25): writes each glossary entry's and each
  capability term's category as its part of speech, and prints each verb that needs a `Frame:` (v_t11), each
  relational condition (v_t12) and each requirement that no longer parses, by file and id. It rewords no line. After
  it, give each verb its frame, write each relational condition as a verb, and reword each line it names, a changed
  line under a new id with its old id in `retired:`; then run `model check`, `model parse` and `features generate`.

## 0.31.5 (released as 2.4.0): the request watch wakes on GitHub's events and starts with the session

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

## 0.31.4 (released as 2.3.1): a batch runs in one fresh agent, and a parked item leaves the batch at once

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

## 0.31.3 (released as 2.3.0): work pushes its commits, requests post after they commit, and work watch

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

## 0.31.2 (released as 2.2.0): decisions and records written by command

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

## 0.31.1 (released as 2.1.0): requests exchanged through GitHub issues

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
- **No upgrade step.** A 0.31.0 repository needs only `github:` on each upstream it asks. A request it already holds
  has no issue, and is read as before.

## 0.31.0 (released as 2.0.0): the workflow simplified

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
- **`migrate upgrade` 0.31.0, "the workflow simplified"**: a 0.30.x repository is moved to the new workflow in one
  commit. It writes `.shop/work/FROZEN.md`, moves each open request of a peer to `.shop/requests/` with `git mv`, and
  rewrites `spec/decisions/index.md`. Nothing is deleted. It names each open initiative, each proposal never applied
  and each internal request not closed, to be shaped as items with `work idea`. A 0.29.x repository reaches 0.31.0
  through the 0.30.0 step in the same commit. From 0.29.x, write each scaffold's requirements and the typed glossary
  as `docs/capability-format.md` § Doing it says, checking with `model parse`, `model check`, `model logic` and
  `model restates`, then run `features generate`.

## 0.30.0 (released as 1.0.0): codified requirements

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
`python3 scripts/migrate upgrade` on a clean tree. Its 0.30.0 step writes `spec/restated.json` (the text of every 0.29
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
