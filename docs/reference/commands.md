<!--
Outputs on this page are from real runs on 2026-11-10: plugin 0.33.0, its scripts as at commit 7f60e57de
(branch plan-docs). Read-only commands ran in this repository. Commands that write ran in two scratch clones of it,
each with a local bare remote as `origin` and the suite's stand-in gh (tests/scripts/stub_gh.py as
$SHOPSYSTEM_WORK_GH), so batches, pull requests and request issues were real runs that touched no GitHub. Long scratch
paths are cut with "...", and long output is cut with "...". The `spec` section's parse, lexicon and explain, and the
item lines' ids, are from plugin 0.38.0 (2026-11-19, branch domain-contract).
-->

# Command reference

This page is for looking things up. The plugin has one command, `shop`, and six subcommands under it (`shop work`,
`shop spec`, `shop features`, `shop tools`, `shop measure` and `shop migrate`). The page lists every command under
them, one subsection a command, so you can find what a command does, what it takes, what it writes and what it
prints. The commands are the CLI adapter of the bounded context's services: each command requests one operation of
the domain model, as [`spec/adapters/cli.toml`](../../spec/adapters/cli.toml) maps them
([adapter contracts](adapters.md)).

You will rarely type these yourself: Claude runs them as you talk (see [Talking with Claude](../talking-with-claude.md)).
They are here for when you want to look, check or do a step by hand.

> **`--help` is the contract.** Every command prints its own usage and rules with `--help`
> (`shop work batch done --help`, `shop spec --help`, `shop --help`). This page is a friendlier summary. Where the two
> differ, `--help` is right and this page is wrong; please file it.

Commands are written short, `shop work backlog` for `python3 "$SHOP/scripts/shop" work backlog`.
[How the commands are run](#how-the-commands-are-run) shows how to set that up.

## How the commands are run

Every console block on this page is what the session runs for you; you never need to. `shop` and its commands are
scripts in the installed plugin's `scripts/` folder, not commands on your `PATH`, so a shell finds no `shop` of its own.
To run it yourself, keep the plugin's folder in `$SHOP`, from `claude plugin list --json`'s `installPath` (a path
that ends in the version, such as `~/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.44.0`; with
`claude --plugin-dir`, the checkout):

```console
$ export SHOP="$(claude plugin list --json | python3 -c 'import json, sys; print(next(p["installPath"] for p in json.load(sys.stdin) if p["id"] == "shopsystem-bdd@shopsystem-bdd"))')"
```

Then give `shop` its short name:

```console
$ alias shop='python3 "$SHOP/scripts/shop"'
```

`shop <command> <args>` runs the plugin's command of that name with the same arguments, its output and exit
unchanged, so a refusal still starts with the command's own name (`work: ...`). The commands' old names, `work`,
`spec` and the rest, run alone too for now; the docs say `shop`'s.

Put the `export` and the `alias` lines in your shell's profile to keep them. The plugin's test plugin lives in
the same folder: a suite runs with `PYTHONPATH="$SHOP/scripts" pytest -p work_items`.

## A first taste

Here is an idea becoming a ready item, in four commands and four commits:

```console
$ shop work idea "work show prints the status of an item" --note "The person wants to see where an item stands at a glance."
b250 "work show prints the status of an item" idea
$ shop work shape b250
b250 "work show prints the status of an item" shaped
$ shop work line b250 --into items --group "An item shown gives its status" 'While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.'
b250 "work show prints the status of an item": items#r31 While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.
$ shop work ready b250
b250 "work show prints the status of an item" ready
```

Each command changed one file under `.shop/backlog/` and committed it alone. From there, `shop work batch start` picks
the item up. The rest of this page goes command by command.

## Things every command shares

- **Exit codes.** `0` success (the outcome `done`, `returned` or `passed`), `1` refused, a check failed, or broken,
  `2` bad usage. A refusal starts with the tool's name, says why, and changes nothing.
- **`--root`.** `shop work` and `shop spec` take `--root <dir>` before the subcommand (default: the current directory).
  `shop features generate` and `shop features vocab` take it after. `shop features` takes `--dir` for its feature files,
  `shop tools` takes `--python` for the project's interpreter.
- **Commits.** A `shop work` command that changes a file commits it, alone, with a message that starts with the command
  (`work shape: b250 ... idea -> shaped`), then pushes the branch to its remote. A refused push prints
  `not pushed: <remote>: <reason>` and keeps the commit.
- **`--json`.** Every command takes it and prints the response envelope, one JSON object: `outcome` (`done`,
  `returned`, `refused`, `passed`, `failed` or `broken`), `content` (what the operation returns), `errors` (each a
  reason and the things it names, by business reference: `parameter:tier`, `item:b12`) and `notices`. A command that
  printed a JSON object of its own before 0.38.0 prints it under `content` now (`shop work backlog --json`, `work batch
  status --json`, `spec check --json`, `features list --json` and the rest): read `.content` where you read the
  object. See [the response](adapters.md#the-response).

## shop work: items, batches, requests and records

`shop work` keeps the backlog (`.shop/backlog/`), the batches (`.shop/batches/`), the requests between bounded contexts
(`.shop/requests/`), the person's words (`.shop/quotes/`), decisions (`spec/decisions/`) and records
(`.shop/records/`). The words it uses (item, batch, request) are explained in [Concepts](../concepts.md).

### Items

#### `shop work idea`

Writes a new item in `idea` and commits it.\
Synopsis: `shop work idea [--provenance {own,peer,product}] [--note NOTE] title`

- `--note`: a line under the item's `## Notes`.
- `--provenance`: who it is for: `own` (the default), `peer` or `product`.

Writes `.shop/backlog/b<n>.md`, numbered after the highest. The example is in [A first taste](#a-first-taste).

#### `shop work shape`

Moves an item from `idea` to `shaped`: it is understood well enough to be given lines. An idea with no shaping note
(nothing under its `## Notes`) is groomed first: `shop work shape` without `--note` refuses it, naming the option.\
Synopsis: `shop work shape [--note NOTE] name`

```console
$ shop work shape b250
b250 "work show prints the status of an item" shaped
```

#### `shop work line`

Writes a requirement line into an item's `## Requirements`, under the capability it goes into, and commits it. It
takes an item that is `idea`, `shaped` or `in-batch`; an in-batch item's changed lines reach its batch with
[`shop work batch amend`](#shop-work-batch-amend).\
Synopsis: `shop work line [--into INTO] [--group GROUP | --in IN_GROUP] [--retires CAP#rN] [--retirement-list FILE] [--no-line] [--reword CAP#rN] [--remove CAP#rN|CAP] [--term TERM] [--recodify CAP] [--relation RELATION] [--model MODEL] [--given GROUP BLOCK] [--universal UNIVERSAL] [--capability CAPABILITY] [--narrator NARRATOR] [--expose TABLES] [--withhold SERVICE.OPERATION] [--remove-model MODEL] [--reword-model HEADER] [--remove-term TERM] [--reword-term TERM] [--pack NAME] [--remove-universal U<n>] [--replace-universal U<n>] [--remove-upstream ID] [--replace-upstream ID] [--remove-given CAP#g<n>] [--replace-given CAP#g<n>] [--serves CAP#gN JOB] [--upstream UPSTREAM] name [text]`

- `--into <capability>`: the codified capability the line goes into.
- `--group "<title>"`: open a new group with this title (default: the item's title). `--in g<n>` joins one of the
  item's groups instead. Both go with a requirement line only; beside another piece they are refused.
- `--retires <cap>#r<n>`: the line replaces a live requirement, whose id goes to `retired:`, and the pair of the
  two to the block's `retires:` line. Ids are never reused. With `--no-line` and no line, the requirement is retired
  with nothing in its place, and no pair is written. Each design-decision whose `enforced_by` names the retired
  requirement is named, with the `shop work decision --amend` that names what holds it now.
- `--retirement-list <file>`: a retirement list, one pair a line, `<cap>#r<n> <line>`: each line retires its live
  requirement as `--retires` does, all in one commit. An id no requirement has refuses the whole list, naming it,
  and the item is left as it was.
- `--reword <cap>#r<n>`: the line takes the place of one of the item's own lines, keeping its id and group, and is
  printed after its id (`<cap>#r<n> reworded: <line>`); a line the item holds with that text already is left as it
  is, nothing committed, and printed `<cap>#r<n> unchanged: <line>`.
  `--remove <cap>#r<n>` takes one of them out, its group with it when it was the last line, and the id its
  `retires:` pair names; an id no pair names stays. Either refuses an id that is no line of the item, a live requirement's among them.
  `--remove <cap>` with no `#r<n>` takes the item's whole block of the capability out, a new capability's
  declaration with it, and the item's model lines of its area unless another of its blocks goes to that area.
- `--remove-model "<header>"`: the item's own element (`object label`, `service notes`) taken out of its model
  lines with its members; given with indented member lines, only those members go. `--reword-model "<header>"
  "<lines>"` puts the model lines given (checked as `--model`'s) in place of the element and its members.
  `--remove-term <term>` takes one of the item's terms out, and `--reword-term <term> "<entry>"` puts the entry,
  its bullet as `--term` takes it, in its place, printing `term <term> reworded: <entry>` (`unchanged`, nothing
  committed, when the item holds that entry already); a term is named by its word, by `<word> → <element>` when two
  entries share the word, or by its whole bullet. A model block left empty goes. Each refuses a model line or a term
  the item does not hold, naming it, and `--into <capability>` picks the area of a model line two areas hold, or of a
  term, as `--term` takes it, the capability's area or its own block.
- `--remove-universal U<n>`, `--remove-upstream <bounded-context id>`, `--remove-given <cap>#g<n>`: the item's own
  universal condition, upstream entry or given block of its group taken out. `--replace-universal U<n> "<statement>"`,
  `--replace-upstream <id> "<entry>"` and `--replace-given <cap>#g<n> "<block>"` put the one given (checked as
  `--universal`'s, `--upstream`'s and `--given`'s are) in its place, a universal condition keeping its id. Each
  refuses a piece the item does not hold, naming it.
- `--term "<bullet>"`: a vocabulary entry (`- **<word>** (<part of speech>) → <element>. ...`) for the vocabulary of
  the capability's area, in place of a line, printed after what was written (`a vocabulary entry of <area>: <entry>`).
  Give `--term` more than once to write several entries in one commit, each printed on a line of its own; one that
  does not read refuses them all.
- `--pack <name> --term "<bullet>"`: a term entry of the context's own pack `spec/packs/<name>.md`, kept in the
  item's `### <name> pack` block; `shop work batch start` appends it to the pack's `## Glossary`, makes the pack when it
  is missing and adds its name to `spec/index.md`'s `imports:`. A term the pack has already is refused, naming the
  term, and so is the name of one of the plugin's own packs, which a pack of the context's would shadow whole.
- `--model "<lines>"`: model lines for the domain model of the capability's area (`object label`, `item: has → label (many)`); an element the area declares already gets the member lines, and an operation it declares already (same service and name) is restated: laid in place of its own line, with the parameters, outcomes and reasons the model line gives, and put back when the item leaves the batch.
- `--relation "<object>: <phrase> → <object> (<cardinality>)"`, `--given`, `--universal`, `--upstream`: the other
  spec pieces an item can carry: a relation of the model, a group's given block, a universal condition, an upstream
  entry.
- `--recodify <cap>`: switch a capability's block to the current language (`codified-2`).
- `--capability <name> --narrator "<who>" [--group service|guarantees] "<purpose>"`: a capability new to the
  context, written as a block of the item (its narrator, group, default `service`, and purpose); refused when
  `spec/capabilities/<name>.md` exists, or when another item holds a block of it, naming that item and the batch
  it is in. `--into <name>` of a capability no file and no block of the item holds names the item that holds it
  and its batch, in place of suggesting `--capability`. Lines and terms go into it with `--into <name>`; `shop work
  batch start` writes its file (with `area:` and `specifies:`) and names it in its area's row under `## Composition` of `spec/index.md`.
- `--serves <cap>#g<n> <job>`: dedicate a requirement group (a live one, or one of the item's own) to a job of the
  product (`shop spec job` declares it), kept as the pair under the item's block of the capability; `shop work
  batch start` writes it as the group's `serves: <job>` line. Beside a requirement line, `--serves <job>` alone
  dedicates the group the line goes into, and the line added is printed before the pair; with `--into`, `--serves`
  takes the job alone and the line may follow it, as `shop work line b1 --into bookings --group "Booking a slot"
  --serves book-repair "<line>"`. Only a first word of the form `<cap>#g<n>` makes it take two. A job the product does not
  hold is refused naming it, and so is a pair the group serves already or another open item holds.
  [`shop spec trace`](#shop-spec-trace) shows what serves a job.
- `--expose '<tables>'`: the tables of one operation for the CLI adapter contract, `[operations."<service>.<operation>"]`
  with its `command` and its `[operations."<service>.<operation>".parameters]`, kept in the item's `### cli adapter`
  block in place of that operation's own; refused when the domain model, with the item's model lines, has no such
  operation. `--expose <service>.<operation>`, the operation alone, writes its tables from the domain model's
  operation: its command named after the operation (after the program the contract's other operations of its service
  are requested by, else the service), and each parameter an option named after it with an example of its type (its
  first value, its object's name, a flag `flag = true`). `--withhold <service>.<operation>` keeps an operation no
  command requests instead. `shop work batch start` lays each into `spec/adapters/cli.toml` (the table in place of the
  operation's own, a withheld operation under `[unexposed]` with its table out), the contract made when there is none.

The line gets the next free id of its capability (`items#r31`). It goes into `spec/` only when a batch starts.
`shop work line` does not parse the line; [`shop work ready`](#shop-work-ready) does.

```console
$ shop work line b250 --into items --group "An item shown gives its status" 'While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.'
b250 "work show prints the status of an item": items#r31 While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.
```

How to write a good line is in [Writing requirements](../writing-requirements.md); the file format is in
[the capability file](capability-file.md).

#### `shop work chore`

Writes a chore into an item in place of requirement lines, and commits the item: the files its work changes and the
command whose exit code 0 shows the work done. For an item with no behaviour a scenario checks (docs, skill text, a
refactor).\
Synopsis: `shop work chore [--file FILE] --check CHECK name`

- `--file <path>`: a file or a directory the work changes; give it once for each. A path under `spec/`,
  `features/` or `.shop/` is refused.
- `--check "<command>"`: the command that fails now and passes once the work is done.

Run again, it replaces the chore. A chore and requirement lines exclude each other: `shop work chore` refuses an item
that holds a requirement, and `shop work line` an item that holds a chore. [`shop work ready`](#shop-work-ready) readies
a chore item without running its check; [`shop work batch done`](#shop-work-batch-done) runs it.

```console
$ shop work chore b34 --file skills/shaping-items/SKILL.md --check "grep -q 'work chore' skills/shaping-items/SKILL.md"
b34 "The shaping skill names work chore": the chore of b34 "The shaping skill names work chore" (check: `grep -q 'work chore' skills/shaping-items/SKILL.md`)
```

#### `shop work rate`

Sets an item's value, urgency or size; the backlog ranks items by the score they make.\
Synopsis: `shop work rate [--value VALUE] [--urgency URGENCY] [--size SIZE] name`

- `--value`: `low-value`, `medium-value` or `high-value`.
- `--urgency`: `low-urgency`, `medium-urgency` or `high-urgency`.
- `--size`: `small`, `medium` or `large`.

```console
$ shop work rate b250 --value medium-value --urgency medium-urgency --size small
b250 "work show prints the status of an item" shaped
```

#### `shop work depend`

Writes that an item depends on another (`--on`), or drops a dependency (`--drop`). A dependency that would close a
cycle is refused.\
Synopsis: `shop work depend (--on ON | --drop DROP) name`

```console
$ shop work depend b251 --on b250
b251 "work show prints an item's dependencies" depends on b250 "work show prints the status of an item"
$ shop work depend b251 --drop b250
b251 "work show prints an item's dependencies" no longer depends on b250 "work show prints the status of an item"
```

#### `shop work ready`

Moves a `shaped` item to `ready` when it passes the readiness bar, and otherwise names every reason it does not. A
`ready` item is checked again: it stays `ready` when it still passes, and every reason is named when it does not.
Any other item is refused, named.\
Synopsis: `shop work ready name`

The bar lays the item's lines over a temporary copy of `spec/` and the construct catalogue and checks that they
parse (using no construct the catalogue has no entry of), that `shop spec logic` finds
no clash naming them, and that `shop features generate` writes their scenarios. A line from a request must be settled.
Readying is the decision to build: a ready item goes into the next batch.

```console
$ shop work ready b250
b250 "work show prints the status of an item" ready
$ shop work ready b253
work ready: b253 "work names prints every item" is not passing:
  items#r32: refused: the verb ready takes a subject, which a passive leaves out: agent readies item
```

What each reason means is in [Troubleshooting](../troubleshooting.md).

#### `shop work reopen`

Moves a `ready` item back to `shaped`, so that `shop work line` can change its lines; `shop work ready` readies it
again. An item that is not `ready` is refused, named.\
Synopsis: `shop work reopen name`

```console
$ shop work reopen b250
b250 "work show prints the status of an item" shaped
```

#### `shop work allocate`

Tracking's operation that gives a `ready` item to a batch's work: the item `in-batch`. `shop work batch start` requests
it of each item it picks; by hand it mends an item a batch command left behind. Each of tracking's operations is one
commit of the item, and an item in another status is refused, named.\
Synopsis: `shop work allocate name`

```console
$ shop work allocate b252
b252 "work show prints the batch of an item" in-batch
```

#### `shop work deliver`

Tracking's operation that moves an `in-batch` item to `delivered`: its change is in the product. `shop work batch
merged` requests it of each item of the batch.\
Synopsis: `shop work deliver name`

```console
$ shop work deliver b252
b252 "work show prints the batch of an item" delivered
```

#### `shop work restore`

Tracking's operation that moves an `in-batch` item back to `ready`, to wait for a batch. `shop work batch abandon`
requests it of each item of the batch.\
Synopsis: `shop work restore name`

```console
$ shop work restore b252
b252 "work show prints the batch of an item" ready
```

#### `shop work suspend`

Tracking's operation that moves an `in-batch` item to `needs-input`, its question under `## Question`; `shop work
answer` answers it. `shop work batch park` requests it.\
Synopsis: `shop work suspend name --question QUESTION`

```console
$ shop work suspend b252 --question "Which reading holds?"
b252 "work show prints the batch of an item" needs-input
```

#### `shop work refuse`

Moves an item that is `idea` or `shaped` to `refused`, with the reason.\
Synopsis: `shop work refuse name reason`

```console
$ shop work refuse b251 "work show prints the dependencies already"
b251 "work show prints an item's dependencies" refused
```

#### `shop work withdraw`

Moves an item to `withdrawn`: nobody wants it any more, writing why under its `## Withdrawn`.\
Synopsis: `shop work withdraw name --reason REASON`

```console
$ shop work withdraw b252 --reason "work backlog's tables are read in a terminal's own colours"
b252 "A colour theme for work backlog" withdrawn
```

#### `shop work merge`

Moves an item that is `idea`, `shaped`, `ready` or `needs-input` to `withdrawn` because another item takes its
place, writing which and why under its `## Withdrawn`. A closed item is refused, named.\
Synopsis: `shop work merge name --into INTO --reason REASON`

```console
$ shop work merge b252 --into b250 --reason "b250 prints the theme too"
b252 "A colour theme for work backlog" withdrawn
```

#### `shop work annotate`

Adds a line to the `## Notes` of an item that is `idea`, `shaped`, `ready` or `needs-input` (a rating's reason, a
finding while shaping), in one commit of the item; a closed item is refused, named.\
Synopsis: `shop work annotate name note`

```console
$ shop work annotate b250 "value high: every session reads the status"
b250 "work show prints the status of an item": a note
```

#### `shop work retitle`

Gives an item that is not `delivered`, `refused` or `withdrawn` a new title, keeping its id, in one commit of the
item; a closed item is refused, named.\
Synopsis: `shop work retitle name title`

```console
$ shop work retitle b250 "work show prints the status and the batch of an item"
b250 "work show prints the status and the batch of an item"
```

#### `shop work split`

Moves requirement lines of an item that is `idea` or `shaped` to a new item, numbered next, that derives from it
(`derives_from:`): each line with its group's id, title and given block, the id it retires with it, and its status,
provenance, ratings, dependencies and request copied; both items in one commit. An item in another state is refused,
named, and so is a line the item does not hold. The new item is titled after the old one; `shop work retitle` names it.\
Synopsis: `shop work split name --requirement CAPABILITY#rN [--requirement ...]`

```console
$ shop work split b250 --requirement items#r12
b251 "work show prints the status of an item (split from b250)" split from b250 "work show prints the status of an item"
```

#### `shop work answer`

Answers the question of an item that is `needs-input` (parked mid-batch), and moves it back to `shaped`.\
Synopsis: `shop work answer name answer`

```console
$ shop work answer b253 "Yes, every item, whatever its status."
b253 "work names prints every item" shaped
```

#### `shop work backlog`

Prints every item, one table a state, in rank order, with what each waits on; an idea with no shaping note waits on
`shop work shape --note`. Writes nothing.\
Synopsis: `shop work backlog [--json]`

```console
$ shop work backlog
...
## shaped (29)

| rank | item | title | provenance | value | urgency | size | score | waiting on |
|---|---|---|---|---|---|---|---|---|
| 1 | b65 | An item with no notes is groomed before it is shaped | own | high-value | medium-urgency | small | 5.00 | - |
| 2 | b66 | A scenario's Given with an unknown condition word is refused | own | high-value | medium-urgency | small | 5.00 | - |
...
```

#### `shop work show`

Prints where an item, a request, a quote or a directive stands. With no target it prints what `shop work list` prints.\
Synopsis: `shop work show [--json] [target]`, where the target is `b<n>`, `q<n>`, `quote-<n>` or `directive-<n>`.

```console
$ shop work show b250
b250 "work show prints the status of an item"
  status: ready
  provenance: own
  value: medium-value
  urgency: medium-urgency
  size: small
  depends on: -

## Notes

The person wants to see where an item stands at a glance.

## Requirements

### items

#### [g31] An item shown gives its status
- [r31] While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.
```

#### `shop work names`

Prints every item and batch with its name beside its id, one table. Writes nothing.\
Synopsis: `shop work names [--hook]`

- `--hook`: the SessionStart hook's form: the table under one line telling the session to name things, nothing
  when there is nothing to show. See [Hooks](#hooks).

```console
$ shop work names
| id | name | status |
|---|---|---|
| b1 | Requests between repositories over GitHub issues | withdrawn |
| b2 | Request lines into an upstream in the downstream's own terms | idea |
...
```

### Batches

A batch builds ready items together: one branch `batch-<n>`, one task (and worktree) an item, one pull request.
These are the commands the batch's driver runs; [Concepts](../concepts.md) draws the states.

#### `shop work batch start`

Picks the ready, unblocked items that pass the bar, in rank order, and starts a batch of them.\
Synopsis: `shop work batch start`

It makes the branch `batch-<n>` in its own worktree, lays the items' lines into `spec/` (their ids into `unbuilt:`),
regenerates the features and commits that, citing each item. On the base branch it commits
`.shop/batches/<n>/plan.md` with the items moved to `in-batch`. It writes the batch brief for the driver (never
committed). It is refused while `spec/` or `features/` has uncommitted changes, and the batch size comes from
`batch_size` in `.shop/delivery.toml`. It stops short of the review limit (`[review] size`, 1000 changed lines): an
item whose estimated change (from its size rating, its requirement lines and its model lines) would take the batch past
it after the items picked before is left out and stays `ready`; the first item is picked whatever its estimate.

```console
$ shop work batch start
batch-34 building: t1 b250 "work show prints the status of an item"
batch brief: .../repo/.shop/worktrees/batch-34-driver/brief.md
```

#### `shop work batch status`

Prints where a batch stands: its items, its tasks, its reviews. With no batch, the open one. Writes nothing.\
Synopsis: `shop work batch status [--json] [batch]`

```console
$ shop work batch status batch-34
batch-34 awaiting-merge, base main, pull request https://github.com/ex/ctx/pull/1
plan: .shop/batches/34/plan.md
reviews: 1, last clean
  b250 "work show prints the status of an item" in-batch
  t1 b250 "work show prints the status of an item": done, branch batch-34-b250
```

#### `shop work batch next`

Prints the next step of a batch for whatever drives it (an agent, a script, a runner): an instruction and what it is
about. The instruction is one of `prepare task` (every pending task, reported through `shop work batch resume`, which
makes their worktrees), `build task` (every running task whose branch holds no commit citing its item since the batch's
lines commit, with the batch brief, so that the tasks are built side by side), `finish task` (a running task whose
branch holds one), `submit batch`, `review change` (the next review's folder and the findings file `findings.md` in
it, where the reviewer's reply is saved for `shop work batch reviewed`), `fix finding` (an open `fix now` finding that
no commit cites yet), `park item` (a failed task), `fix task` (every task done and the last whole-suite run of
`shop work batch review` failed: the task of the item whose change broke the batch's tests, with the failed tests),
`look at failure` (the same, but the failed tests are of no task's item: the failed tests, with no task), `abandon
batch` (a building batch every item of which is parked, `needs-input`, reported through `shop work batch abandon`) or
`stop`. Only the tasks of items still `in-batch` count. The first one that applies is picked, in this order: stop,
review change, abandon batch, fix finding, park item, finish task, build task, prepare task, fix task, look at failure, submit batch. Each task the step
is about has a `task:` line; the last line names the command that reports the step's result, of `build task` one for
each task. With `--json` the step is the envelope's `content`, its tasks under `tasks` and the first of them `task`.
Writes nothing.\
Synopsis: `shop work batch next [--json] batch`

```console
$ shop work batch next batch-34
batch-34 building: finish task
task: t1 b250 (running), branch batch-34-b250
report: shop work batch done batch-34 t1
```

#### `shop work batch resume`

Gives each pending task its worktree, `batch-<n>-t<k>` on the branch `batch-<n>-b<j>`, and prints what each running
task builds. It also gives back a lost worktree, and one for each open review finding.\
Synopsis: `shop work batch resume batch`

```console
$ shop work batch resume batch-34
batch-34 building: plan .shop/batches/34/plan.md
t1 b250 "work show prints the status of an item": running in .shop/worktrees/batch-34-t1 on batch-34-b250: build items#r31; then work batch done batch-34 t1, or work batch park batch-34 b250 --question <text>
```

#### `shop work batch done`

Sets a running task done, once its worktree is clean, its commits cite the item (`Item: b<n>`), its ids have left
`unbuilt:` and the tests pass.\
Synopsis: `shop work batch done batch task`

The tests are `[batch] tests` of `.shop/delivery.toml` (default `python3 -m pytest -q -p work_items`), run in the
task's worktree, only the ones the task's change reaches: a capability's `tests/scenarios/test_<capability>.py` when
the item holds one of its ids or a commit of the task touches its feature, and a `tests/scripts/` test that names a
module the task touches; the pytest plugin `work_items` leaves the others out. `shop work batch review` runs them all.
For an item that holds a chore, it then runs the chore's check there and refuses while it exits non-zero, and refuses a commit of the task that touches a path the chore does not name. A refusal names what is
missing:

```console
$ shop work batch done batch-34 t1
work batch done: t1 b250 "work show prints the status of an item": the tests `python3 -m pytest -q -p work_items` failed in .shop/worktrees/batch-34-t1 (exit 1):
...
$ shop work batch done batch-34 t1
batch-34 t1 b250 "work show prints the status of an item": done
```

#### `shop work batch amend`

Lays an in-batch item's lines again on `batch-<n>` and on its task's branch, after `shop work line` changed them: the
lines it last laid are taken out and its lines as they now read laid in, one commit on each branch citing the item. A new id
is renumbered past the other items' lines on the batch branch (the item committed again on the base), a line laid
before with the same text keeps its place in `unbuilt:`, and a `done` task is set `running` again. Refused for an item
that is not `in-batch`, and while the task's worktree has uncommitted changes.\
Synopsis: `shop work batch amend item`

```console
$ shop work batch amend b253
batch-35 b253 "work names prints every item" amended: laid on batch-35, batch-35-b253
```

#### `shop work batch park`

Sets an item of the batch `needs-input` with a question, and takes its lines out of `batch-<n>`; the rest of the
batch carries on. You answer with [`shop work answer`](#shop-work-answer).\
Synopsis: `shop work batch park --question QUESTION [--discard] batch item`

- `--question`: what the person is asked; `shop work backlog` shows it.
- `--discard`: throw away the uncommitted changes in the item's worktree (refused without it while there are any).

```console
$ shop work batch park batch-35 b253 --question "Should work names print withdrawn items too?"
batch-35 b253 "work names prints every item" -> needs-input: Should work names print withdrawn items too?
```

#### `shop work batch review`

Merges the in-batch items' branches into `batch-<n>`, runs the tests, pushes, and opens the batch's draft pull
request. The batch goes `in-review`.\
Synopsis: `shop work batch review batch`

On a second round it also checks that each fix commit cites an open finding (`Finding: f<k>`) and each open finding
has one.

```console
$ shop work batch review batch-34
next: work batch brief batch-34, the pr-reviewer on it, then work batch reviewed batch-34
https://github.com/ex/ctx/pull/1
```

#### `shop work batch brief`

Writes the brief of the next review of a batch's pull request, for the `pr-reviewer` agent: the range, the items'
lines, the judgement decisions, the rules and the `[review] checks` runs. Nothing is committed.\
Synopsis: `shop work batch brief batch`

```console
$ shop work batch brief batch-34
.shop/worktrees/batch-34-review-1/brief.md
```

#### `shop work batch reviewed`

Records the reviewer's reply, read from the `pr-reviewer` dispatch's transcript (`--reply <transcript>`, else the
newest `pr-reviewer` transcript of the session's store whose prompt names the brief; the reply relayed to the session
has `<`, `>` and `&` escaped), or from the findings file saved where the brief says when no transcript is found: writes
`.shop/batches/<n>/review-<k>.md`, posts it on the pull request, and moves the batch back to `building` while a
finding is open, or to `awaiting-merge` (the pull request marked ready) when none is.\
Synopsis: `shop work batch reviewed batch [--reply transcript]`

```console
$ shop work batch reviewed batch-34
batch-34 review 1: 1 finding -> awaiting-merge; the pull request https://github.com/ex/ctx/pull/1 is ready for the person's merge
```

#### `shop work batch reopen`

Takes a batch that is `awaiting-merge` back to `building` with the person's comment on its pull request, saved as a
findings file (the form `shop work batch reviewed` reads, with at least one `fix now` finding): writes it as
`.shop/batches/<n>/review-<k>.md`, puts the pull request back to a draft, and commits both. A batch in any other
state is refused, naming it.\
Synopsis: `shop work batch reopen batch --finding file`

```console
$ shop work batch reopen batch-34 --finding findings.md
batch-34 review 2: 1 finding, 1 fix now -> building
  open f2 Important b12 "Recover a post whose URL was never committed" src/request_post.py: the post is lost
```

#### `shop work batch merged`

Records the merge of the batch's pull request once GitHub says it is merged and its merge commit is in the base: the
in-batch items become `delivered`, and the batch's worktrees, review folders, brief folder and item branches are
removed.\
Synopsis: `shop work batch merged batch`

```console
$ shop work batch merged batch-34
batch-34 merged
```

#### `shop work batch abandon`

Abandons a batch: its pull request is closed, its in-batch items are `ready` again, and its worktrees are removed.\
Synopsis: `shop work batch abandon [--discard] batch`

- `--discard`: throw away uncommitted changes in its task worktrees (refused without it while there are any).

```console
$ shop work batch abandon batch-35
batch-35 abandoned
```

#### `shop work settings set`

Sets one setting of `.shop/delivery.toml` in its own table, every comment and other key kept, and commits it. The
settings are `base`, `batch_size`, `batch.push`, `batch.tests`, `batch.worktrees`, `batch.rules`, `review.size`,
`review.checks` and `prices.<model>`; a setting the plugin does not read, or a value not of its type, is refused, naming it.\
Synopsis: `shop work settings set setting value`

- `value`: a TOML value (`7`, `["a", "b"]`, `{ input = 3.0, output = 15.0, cache_read = 0.3 }`); a text setting's may
  be the bare text.

```console
$ shop work settings set review.size 1500
.shop/delivery.toml: review.size = 1500
```

#### `shop work context keep`

Keeps a bounded context in this shop under its context id, in `.shop/contexts.toml`, and commits it. The shop's
product id is its product's id, read off `.shop/product/product.toml`; while the product has an id, an id outside it is
refused, naming it, and with none any id is kept. An id the shop keeps already is refused, naming it.\
Synopsis: `shop work context keep id`

```console
$ shop work context keep bounded-context/missingmass.io/shopsystem/language
kept bounded-context/missingmass.io/shopsystem/language
```

#### `shop work context list`

Prints the id of each bounded context this shop keeps, one a line; while it keeps none, this bounded context's id
alone.\
Synopsis: `shop work context list`

```console
$ shop work context list
bounded-context/missingmass.io/shopsystem/shopsystem-bdd
```

### Requests

A request is one bounded context asking another (its upstream, or itself) for behaviour, carried on a GitHub issue.
Each step below commits the request file `.shop/requests/q<n>.md`, then posts the step on the issue and commits its
URL. The examples follow one request, `q48`, that this repository raised to itself.

#### `shop work request`

Asks an upstream (or this context): writes the request, opens its issue, and commits both.\
Synopsis: `shop work request [--from ASKER] [--ask ASK] [--to TO] [--source SOURCE] [--thread THREAD] [--raised-for RAISED_FOR] title`

- `--from`: the asker: this bounded context's id, or `internal` for a request this context raises to itself
  (optional; default: this context).
- `--ask`: what the asker needs, in its own words (default: the title).
- `--to`: the upstream, one of `spec/index.md`'s `## Upstreams` (default: the one upstream, or this context).
- `--source`: the origin of a request this context asks itself; `--thread` or `--raised-for` for one another
  context asks.

```console
$ shop work request "Show an item's status in work show" --from bounded-context/missingmass.io/shopsystem/shopsystem-bdd --source observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-probe-repositories-again --ask "When I run work show on an item, I want to see its status."
q48 https://github.com/ex/ctx/issues/1
```

#### `shop work offer`

The upstream's offer, under `## Offer`: each capability that may serve the request quoted by its groups and
requirements, with only the terms they mention, so the asker can write lines in the upstream's words. With no
`--capability` the offer is the note alone, no vocabulary. It passes the turn to the asker and prints the request, its
status and its turn.\
Synopsis: `shop work offer [--capability CAPABILITY] [--note NOTE] request`

```console
$ shop work offer q48 --capability backlog --note "work show prints an item's title and rating today; the backlog capability would hold the status too."
q48 awaiting-asker asker
```

#### `shop work fits`

The asker's answer to an offer when existing behaviour already serves it: the request is `delivered` and its issue
closed.\
Synopsis: `shop work fits [--serves SERVES] request`

```console
$ shop work fits q49 --serves items#r12
$ shop work show q49
q49 delivered asker
it is the asker's turn, on https://github.com/ex/ctx/issues/2
  resolution line 1: items#r12
```

#### `shop work propose`

The asker's lines, one `--line` each, in the upstream's words; it prints the request, its status and its turn.\
Synopsis: `shop work propose [--line LINES] request`

```console
$ shop work propose q48 --line 'When the person shows an item, the backlog service shall return the status of the item.'
q48 awaiting-asker asker
```

#### `shop work suggest`

The asker's term proposal: terms for the upstream to take into its own vocabulary, each a vocabulary entry
`- **<word>** (<part of speech>) → <model element>. <definition>`. It is kept as the request's next line, posted on
its issue, and settled with `shop work outcome` like any line; `shop work accept` writes the terms of an accepted one
into the item. It prints the request, its status and its turn.\
Synopsis: `shop work suggest --term-proposal TERM_PROPOSAL request`

```console
$ shop work suggest q48 --term-proposal='- **shelf** (noun) → object shelf. A place the person keeps books on.'
q48 awaiting-asker asker
```

#### `shop work turn`

Passes a request's turn to the other side, posts it, and prints the request, its status and its turn.\
Synopsis: `shop work turn request`

```console
$ shop work turn q48
q48 awaiting-upstream upstream
```

#### `shop work ask`

The upstream's question on one line of a request.\
Synopsis: `shop work ask request line question`

```console
$ shop work ask q48 1 "Should the status be the item's state, such as ready?"
```

#### `shop work reply`

The asker's answer to a question of a request; it prints the request, its status and its turn.\
Synopsis: `shop work reply request question answer`

```console
$ shop work reply q48 1 "Yes: the state the backlog shows it under."
$ shop work show q48
q48 awaiting-upstream upstream
it is the upstream's turn, on https://github.com/ex/ctx/issues/1
  line 1: unsettled - When the person shows an item, the backlog service shall return the status of the item.
  question 1: line 1: Should the status be the item's state, such as ready?
  answer 1: Yes: the state the backlog shows it under.
```

#### `shop work outcome`

The upstream's outcome of one line: `accepted`, `rewritten`, `refused`, `question` or `withdrawn`. An accepted line
is parsed in this context's grammar first.\
Synopsis: `shop work outcome [--into INTO] [--group GROUP] [--reason REASON] [--line TEXT] request line outcome`

- `--into <capability>` (and `--group`): where an accepted line goes.
- `--reason`: why, under the request's `## Reasons` (needed for `refused`).
- `--line`: the counter-proposal of a `rewritten` line.

```console
$ shop work outcome q48 1 accepted --into backlog
```

#### `shop work accept`

Accepts a request whose lines are settled: it becomes a `shaped` item with each accepted line under its capability,
and the request is `accepted`.\
Synopsis: `shop work accept request`

```console
$ shop work accept q48
b250 "Show an item's status in work show" shaped
```

#### `shop work resolve`

Writes which requirement holds each accepted line, and in which version; the request is `delivered`.\
Synopsis: `shop work resolve [--line N REQUIREMENT VERSION] request`

```console
$ shop work resolve q48 --line 1 items#r31 0.38.0
```

#### `shop work list`

Prints each request with its status, and each observation no source cites. Writes nothing.\
Synopsis: `shop work list [--json]`

```console
$ shop work list
request q14 accepted
request q48 delivered
request q49 open
observation observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-proposal-argues-many 2026-10-15
...
```

#### `shop work sync`

Brings the requests up to date with their issues: each comment a record does not hold is applied and recorded, a new
ask on this context's own repository becomes a request, and every request is printed with whose move it waits on.\
Synopsis: `shop work sync`

```console
$ shop work sync
q14 "Requests go through one shared tool" accepted: the upstream's turn, waiting on this side
q48 "Show an item's status in work show" delivered
q49 "Print the item's title in work show" open: the upstream's turn, waiting on this side
```

#### `shop work watch`

Watches the open requests' issues and prints each new comment or ask once, then ends. Nothing is committed.\
Synopsis: `shop work watch [--every EVERY] [--polls POLLS] [--forward] [--hook]`

- `--every`: seconds between polls (default 60).
- `--polls`: give up, exit 1, after this many empty polls (default: never).
- `--forward`: wake on GitHub's events through `gh webhook forward`, polling notifications where it cannot. Claude
  runs this one with the Monitor tool.
- `--hook`: the SessionStart hook's form. See [Hooks](#hooks).

```console
$ shop work watch --every 1 --polls 1
work watch: nothing new after 1 poll
```

### The person's words, decisions and records

#### `shop work quote`

Copies the person's message holding these words, with the two messages before and after it, into
`.shop/quotes/<n>.md`, and commits it. Later, `shop work show quote-<n>` prints it.\
Synopsis: `shop work quote [--session SESSION] [--transcript TRANSCRIPT] [--hook] [words]`

- `--session`, `--transcript`: where to look (default: the session the prompt hook kept).
- `--hook`: the UserPromptSubmit hook's form. See [Hooks](#hooks).

```console
$ shop work quote --transcript ~/.claude/projects/-home-vscode-shopsystem-bdd/72e23fa5-6dee-49f3-a1d1-7e79096a0501.jsonl "I trust you to make some delightful docs."
quote-24 "I trust you to make some delightful docs."
$ shop work show quote-20
quote-20 "Once 4.0 is done, take a new backlog item to make some nice …"
  session: 72e23fa5-6dee-49f3-a1d1-7e79096a0501
  date: 2026-11-10
...
```

#### `shop work directive`

Keeps a short-term direction of the person in the repository, never in a session's memory: their words as a quote
(found as `shop work quote` finds them) and a `live` directive citing it, `.shop/directives/<n>.md`, in one commit. With
`--quote`, a directive of a quote already kept.\
Synopsis: `shop work directive [--session SESSION] [--transcript TRANSCRIPT] [--quote QUOTE] [words]`

```console
$ shop work directive --quote quote-42
directive-1 "Merge and release while I am away." citing quote-42
```

#### `shop work directives`

Prints the live directives, each with its id, date, age and words. Writes nothing.\
Synopsis: `shop work directives [--all] [--hook]`

- `--all`: every directive, with its status.
- `--hook`: the SessionStart hook's form: the live directives' words under one line telling the session to follow
  them and pass them on in every brief, nothing when none is live. See [Hooks](#hooks).

#### `shop work promote`

Promotes a live directive to what it became, once the session has written it: an item, a design-decision or a
line of `CLAUDE.md`. A directive that is not live, or a target that does not exist, is refused, naming it.\
Synopsis: `shop work promote --to TO name`

```console
$ shop work promote directive-1 --to b20
directive-1 "Merge and release while I am away." promoted to b20
```

#### `shop work drop`

Drops a live directive, with the reason. A directive that is not live is refused, naming it.\
Synopsis: `shop work drop --why WHY name`

#### `shop work decision`

Writes a design-decision, `spec/decisions/<nnnn>-<slug>.md`, rewrites `spec/decisions/index.md`, and commits both.\
Synopsis: `shop work decision [--amend DECISION] [--summary SUMMARY] [--tier {check,requirement,judgement}] [--decision DECISION] [--context CONTEXT] [--alternatives ALTERNATIVES] [--enforced-by ENFORCED_BY] [--verified-by {scenario,check,judgement,monitor}] [--rests-on RESTS_ON] [--supersedes SUPERSEDES] [--source SOURCE] [--by BY] [--slug SLUG] [--date DATE] [title]`

- `--summary`, `--tier`, `--decision`: required; it is refused, naming each one missing.
- `--context`, `--alternatives`: the other sections. These three take text, or `@<file>`.
- `--enforced-by`: a test (`check` tier) or a requirement (`requirement` tier); repeatable.
- `--rests-on`, `--verified-by`: for a decision that routes a universal condition.
- `--supersedes <id>`: an accepted decision this one replaces (its id, path or number); it is set `superseded`
  and committed with the new one. A decision not accepted, or an id that names none, is refused, naming it; repeatable.
- `--amend <id>`: in place of a title, adds each `--enforced-by` and `--rests-on` an accepted decision (its id, path
  or number) does not name yet, changes nothing else of it, and commits it with the index. When it names every one
  already, it completes and changes no file. A decision not accepted is refused, naming it.

```console
$ shop work decision "The command reference defers to --help" --summary "Where the command reference and --help differ, --help wins." --tier judgement --decision "Each command's --help is its contract; the reference page links to it and never overrides it."
spec/decisions/0093-the-command-reference-defers-to-help.md
```

#### `shop work record`

Writes a record, `.shop/records/<date>-<slug>.md`, adds its row to `.shop/records/README.md`, and commits both. A
record that exists is refused: a committed record is never edited.\
Synopsis: `shop work record [--kind {analysis,design,measurement,review-finding,decision-argument}] [--summary SUMMARY] --body BODY [--about ABOUT] [--slug SLUG] [--date DATE] [--design [DESIGN]] [--plan] title`

- `--body <file>`: the record's text, under its title.
- `--summary`: its row in the index, one line.
- `--about <id>`: the node, item or batch it is about, one this repository holds (default: the bounded context).

```console
$ shop work record "Command reference layout" --kind analysis --summary "Why the command reference has one section a tool" --body body.md
.shop/records/2026-11-10-command-reference-layout.md
```

With `--design` it files a design: the folder `.shop/records/<date>-<slug>/` with its `design.md` and its row in the
index. With `--plan --design <design>` it files a plan, `plan-<k>.md`, in the folder of that design (its folder's
name, path or id); a design that does not exist is refused, naming it.

```console
$ shop work record "Notes app" --design --summary "How the notes app is built" --body design.md
.shop/records/2026-11-21-notes-app/design.md
$ shop work record "Plan 1: the store" --plan --design 2026-11-21-notes-app --body plan.md
.shop/records/2026-11-21-notes-app/plan-1.md
```

#### `shop work observe`

Files an observation: an entry of `.shop/records/observations.md`, its heading the id
`observation/<context path>/<date>-<slug>`, with `about:`, `by:` and `date:` over its text, and commits it.\
Synopsis: `shop work observe [--about ABOUT] [--by BY] [--slug SLUG] [--date DATE] text`

```console
$ shop work observe "The batch brief names no test command when [batch] tests is unset."
observation/example.com/shop/ctx/2026-11-21-the-batch-brief-names-no-test
```

## shop spec: the spec, checked

`shop spec` reads `spec/` and `.shop/`, checks them, and parses lines. It was called `model` before 0.38.0; `model`
still works in 0.38 and prints a notice that it goes in the next release. Only `decisions`, `rules --write` and
`constructs --write` write files, and none of them commits.

### `shop spec parse`

Parses a line in the context's grammar and prints its tree, or its refusal with a hint.\
Synopsis: `shop spec parse [--file FILE] [--form] [--item b<n>] [line]`

- `--form`: print the line's meaning (its logical form) instead of its tree. Read this one.
- `--file`: parse every line of a file, numbered.
- `--item b<n>`: read the line as it reads once the terms, relation rows, lines and model lines the item holds are
  laid into the specification, on a copy, as `shop work ready` lays them; nothing in `spec/` changes. Use it to see why
  a line of an item is refused without running `shop work ready`.

```console
$ shop spec parse --form 'When the person shows an item, the backlog service shall return the status of the item.'
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: item]
    request(e1, backlog.show, subject: x1, object: x2)
  response [x4: status]
    status(x2) = x4
    return(e2, subject: x3, object: x4)
$ shop spec parse 'When an item is readied, the backlog service shall return the status of the item.'
refused: the verb ready takes a subject, which a passive leaves out: agent readies item
  parsed up to: When an
  nearest words: item, items, `item`, term, stem
  may follow: (none)
```

The second line is a counter-example: the grammar has no "an item is readied", so it is refused. How to read a
refusal is in [Writing requirements](../writing-requirements.md).

### `shop spec lexicon`

Lists the context's words by category: actors, kinds, attributes, events, conditions.\
Synopsis: `shop spec lexicon [--check]`

- `--check`: report problems with the terms (`v_t4` to `v_t15`), and exit 1 when there is any.

```console
$ shop spec lexicon
actor (45)
  the person
  ...
  the backlog service
...
event (138)
  refuse  [pack request]
  ...
  return  [pack request]
...
```

### `shop spec explain`

Prints a requirement, what it also means because of other requirements, and what takes precedence over it.\
Synopsis: `shop spec explain requirement`

```console
$ shop spec explain items#r15
items#r15  While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
which also means:
  the backlog service shall change nothing (by U17)
  the backlog service shall name a reason (by U17)
```

### `shop spec check`

Solves the facts of the repository against the design model's rules and prints every violation (`v_...`), then
warnings (`w_...`), unresolved references and file problems. Exits 1 on any violation.\
Synopsis: `shop spec check [--json] [--limit LIMIT] [--item b<n>]`

- `--limit`: rows shown for each rule (the rest are counted).
- `--item b<n>`: check the specification as it reads once the item's lines, terms, model lines and `serves:` pairs
  are laid into it, on a copy, as `shop spec parse --item` reads a line; nothing in `spec/` changes. A job the item's
  groups serve is then no `w_unserved_job`, before any batch lays them. What only a batch's lay writes is not
  reported: no `v_s3` of a group the item lays (its scenarios), no `v_a5` of a requirement it lays (the adapter
  contract's annotations); every other violation of its lines is, and fails the check.

```console
$ shop spec check
warning w_example  a requirement holds example data: a code or quoted string that names no declared constant  (41)
    capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools#r37, .venv/bin/python
...
0 violations, 57 warnings, 0 unresolved references, 0 file problems
```

What each rule guards is in [the design model reference](design-model.md).

### `shop spec logic`

The temporal and entailment check of the codified lines: clashes between requirements (L1 to L8). Give a capability,
or a requirement id for the findings that name it. A requirement it has no translation of is printed
`unread <id>: <what it cannot read>`, and the count says how many are unread in place of `no findings`; the exit is
the findings' alone.\
Synopsis: `shop spec logic [--json] [capability]`

```console
$ shop spec logic backlog
no findings
```

### `shop spec rules`

Prints every rule's code and plain label, violations first.\
Synopsis: `shop spec rules [--json] [--write] [--check]`

- `--write`: write the rule catalogue `grammar/rules.md`; `--check` says whether it is current. The catalogue is
  part of the plugin's specification: each entry's purpose, `Since:` and `Changed:` (items, or a release for the oldest), and its fact sets,
  the entry's test ([the catalogues](design-model.md#the-catalogues-are-specification)).

```console
$ shop spec rules
v2  a standing edge touches something that is not standing
v3  a request's resolution names something that is not a requirement of the spec
...
```

### `shop spec forms`

Prints every file form a context keeps: its name, its path and the command that writes it (or the plugin's item
that will give it one).\
Synopsis: `shop spec forms [--json] [--check]`

- `--json`: print `{"forms": [{"name", "path", "writer", "kind"}]}`, each form's `kind` the kind of its writer:
  `command`, `item` (a plugin item that will give it one) or `hand`.
- `--check`: print nothing and exit 0 unless a form is written by hand; each such form is named on stderr and it
  exits 1.

```console
$ shop spec forms
item                      .shop/backlog/b<n>.md                                work idea
item's requirement line   .shop/backlog/b<n>.md ## Requirements                work line
...
capability                spec/capabilities/<name>.md                          work line --capability
...
```

### `shop spec annotate`

Writes, under each operation of each adapter contract (`spec/adapters/cli.toml`), the requirements that govern it:
each requirement whose trigger requests the operation, its refusals among them, as
`requirements = ["<capability>#r<n>: <line>", ...]`
([adapter contracts](adapters.md)). It prints each contract it wrote (`annotated`) or found
current (`current`) and exits 0.\
Synopsis: `shop spec annotate [<adapter contract> ...] [--check]`

- `--check`: write nothing; each stale contract is named on stderr and it exits 1. `shop spec check` fails the same
  contract too, naming each operation and requirement (`v_a5`, `v_a6`).

```console
$ shop spec annotate
annotated spec/adapters/cli.toml
$ shop spec annotate --check
```

### `shop spec prepare`

Prints this bounded context's contract at a version, in the contract form (`contract.toml`): `context` and `version`,
then a table of each object, of each operation (its parameters, outcomes, reasons, the requirements that govern it as
`shop spec annotate` gathers them, and its properties) and of each event (the operation that raises it and its
properties). It writes nothing and exits 0. A property is written on the operation's or the event's model line:
`idempotent by <parameter>`, `compensated by <operation>`, `followed by <event>`, and an event's `; delivery: <text>`
and `; when: <text>`; `shop spec check` fails one that refers to a parameter, an operation or an event the model does
not declare (`v_m8`).\
Synopsis: `shop spec prepare --contract <version>`

```console
$ shop spec prepare --contract 1.0.0
context = "bounded-context/example.org/fixture/domain-model"
version = "1.0.0"
...
```

### `shop spec publish`

Keeps this bounded context's contract at a version as `.shop/contracts/<version>/contract.toml`, in the contract
form with `status = "published"`, and sets every contract kept as published before it `superseded`, in one commit.
The contract holds what `shop spec prepare` prints, every requirement of the context and every term of its own. With no
`--version` it is kept at the latest kept version's last number one more, else at `1.0.0`. A version a contract is
kept at already is refused, naming the version, and so is a context with a requirement that does not conform to the
language reference, naming the requirement.\
Synopsis: `shop spec publish [--version <version>]`

```console
$ shop spec publish --version 1.2.0
published .shop/contracts/1.2.0/contract.toml
```

### `shop spec fetch`

Prints the contract kept as published, or with `--version` the one kept at that version, as a downstream context
reads it; it writes nothing. A version no contract is kept at is refused, naming the version.\
Synopsis: `shop spec fetch [--version <version>]`

```console
$ shop spec fetch --version 1.2.0
context = "bounded-context/example.org/fixture/domain-model"
version = "1.2.0"
status = "published"
...
```

### `shop spec obtain`

Keeps an upstream's contract, the one it keeps as published or with `--version` the one kept at that version, in
each adapter spec `adapters/<name>/` whose `providers:` name it, at the version the adapter spec pins the provider at
when it pins one: it asks the contract registry to register the contract for each such adapter spec. The shop-folder
adapter keeps it as `provider/<id's path>/<version>/contract.toml` under the adapter spec's folder (its id after
`bounded-context/`, so two upstreams whose ids end alike keep their own), where the adapter spec's provider check
reads it, byte for byte, one commit for each adapter spec; nothing is kept at the repository root, and it keeps no
context request and changes no other contract. The
upstream is a bounded context under `## Upstreams` of `spec/index.md`, read off the GitHub repository its `github:`
names. An id out of the context id form `bounded-context/<domain>/<path>` is refused, naming the id and
`id not in the context id form`; a repository GitHub does not serve (missing, private or not answering), naming the
bounded context and `bounded context unreachable`; an upstream with no contract, naming the bounded context; an
upstream no adapter spec has as its provider, naming the bounded context and `no adapter spec has the provider`; a
registration the registry refuses, naming the adapter spec and `contract not registered`. Obtained again, a contract
kept already is written again with the upstream's bytes, or left as it is when they are the same (`kept already`).\
Synopsis: `shop spec obtain <bounded context> [--version <version>]`

```console
$ shop spec obtain bounded-context/example.org/fixture/inventory
obtained adapters/stock-inventory/provider/example.org/fixture/inventory/1.2.0/contract.toml
```

### `shop spec product`

Declares the product this bounded context belongs to, its id and its purpose, kept in the product file
`.shop/product/product.toml` of the shop with its actors and jobs, in one commit. Declared again with its own id, the
purpose is replaced and the actors and jobs kept. An id not of the product id form, a dotted domain then a path (as
`example.org/notes`), is refused naming the id, and so is an id other than the one the product was declared with.\
Synopsis: `shop spec product <id> --purpose <text>`

```console
$ shop spec product missingmass.io/shopsystem --purpose "Specify, build and run bounded contexts."
declared the product missingmass.io/shopsystem
```

### `shop spec actor`

Declares an actor of the product, one it serves, kept among the product's actors in the product file, in one commit.
While the product has no id (no `shop spec product` yet) it is refused naming the product file; an actor not of the
product actor form, `the` and a noun (as `the writer`), is refused naming the actor.\
Synopsis: `shop spec actor <actor>`

```console
$ shop spec actor "the developer"
declared the product actor the developer
```

### `shop spec job`

Declares a job to be done of the product with its id, its actors, its job statement and the jobs it needs first,
kept in the product file in one commit; a job declared again replaces the one of its id. The product actor is checked
first: a job with no `--actor`, or with an actor the product does not hold, is refused naming `--actor`. The job
statement is checked for the job statement form only, `When <situation>, <actor> wants <motivation>, so they can
<outcome>.`; a statement of another form is refused naming `--statement`, a statement whose actor the product does
not hold naming the actor and `--actor`, a statement whose actor is not one of the job's `--actor`s naming
`--statement`, a need that is no job of the product naming `--needs`, and a need that depends on the job, directly or through the jobs it needs, so
that the needs would close a cycle, naming `--needs`.\
Synopsis: `shop spec job <id> --statement <text> [--actor <actor> ...] [--needs <job> ...]`

```console
$ shop spec job j1 --actor "the developer" --statement "When a change is wanted, the developer wants it specified, so they can build it."
declared the job j1
```

### `shop spec subdomain`

Declares a subdomain of the product's domain map with its id, its subdomain type and the jobs it serves, kept in the
product file in one commit; a subdomain declared again replaces the one of its id. An id not of the subdomain id
form, lower-case words joined by hyphens (as `note-keeping`), is refused naming the id. A type other than `core`,
`supporting` or `generic` is refused naming `--type`, and a job that is no job of the product naming `--serves`.\
Synopsis: `shop spec subdomain <id> --type <type> [--serves <job> ...]`

```console
$ shop spec subdomain specification --type core --serves j1
declared the subdomain specification
```

### `shop spec context`

Declares a bounded context of the product's domain map with its id, the subdomains it addresses and the shop that
keeps it, kept in the product file in one commit; with no `--shop` it is a third-party provider. The id is of the
context id form `migrate init` and `work context` take, `bounded-context/<domain>/<path>`: one of another form is
refused naming it, so one bounded context is never kept under two ids. An id that does not lie under the product's id
is refused naming the id, and a subdomain that is no subdomain of the product naming
`--addresses`.\
Synopsis: `shop spec context <id> [--addresses <subdomain> ...] [--shop <shop>]`

```console
$ shop spec context bounded-context/missingmass.io/shopsystem/shopsystem-bdd --addresses specification --shop missingmass.io/shopsystem/shop
declared the bounded context bounded-context/missingmass.io/shopsystem/shopsystem-bdd kept by missingmass.io/shopsystem/shop
```

### `shop spec trace`

Prints a job's trace, writing nothing: the requirements of the requirement groups that serve the job (their
`serves:` line), every requirement the requests of a requirement in the trace reach (a line triggered on a request it
covers, followed up to three hops), each adapter spec whose `realises:` names a port line in the trace, and the
traces of the jobs it needs (its needs in the product file), each requirement and adapter spec once with why it is
in the trace. A job no requirement group serves is refused naming it.\
Synopsis: `shop spec trace [--json] [--item b<n>] <job>`

- `--item b<n>`: trace the job as the specification reads once the item's lines and `serves:` pairs are laid into
  it, on a copy, as `shop spec parse --item` does; nothing in `spec/` changes. Without it a group the item dedicates
  to the job (`shop work line --serves`) is in no trace until a batch lays the item, and a job only such groups serve
  is refused.

```console
$ shop spec trace j1 --json
```

Each requirement is printed as `<capability>#r<n> (<why>): <its text>`, the why one of `served by <capability>#g<n>`,
`governs the operation <capability>#r<n> uses` and `needed job <job>: ...`, and each adapter spec as
`adapter spec <id> (realises the port line <capability>#r<n>)`. A provider's requirement, which a contract an adapter
spec in the trace holds lists under a provider operation it uses, is printed by its provider and its id,
`<provider id less bounded-context/>:<capability>#r<n> (governs the operation <operation> of <provider>@<version>,
which <adapter spec> uses for <port operation>): <its text>`, so that an id equal to one of this bounded context's
requirements, or of another provider's, is a requirement of its own.

The trace also says the job's coordination (decision 0134), derived from its lines and the domain model, never
declared: `saga` when it requests two operations of a driven port or more that have a `compensated by` property,
`long-running process` when a requirement on the outcome of a port operation it requests uses an operation that
performs a lifecycle transition, `port request` when it requests a port operation whose outcomes no requirement
handles. It is printed as the line `coordination: <kind>` under the trace's heading, and is the content's
`coordination`; a trace that requests no port operation has no coordination, prints no such line, and its content's
`coordination` is null.

### `shop spec coupling`

Prints the coupling between the areas of the domain model (`spec/model/`), writing nothing, each area a bounded
context the disentangling of a shop will make. A coupling is of the area depended on, by another area, and holds
each word the other area's vocabulary borrows (an entry of it meaning an element of the area's model), each element of the area the
other's model refers to, and each requirement of a capability of the other area that uses a word only the area
defines, and each Python file of the other area that imports one of the area's, the areas' Python files declared
in `.shop/modules.toml` (a table `[<area>]` with `modules`, path patterns from the repository's root, `**` across
folders; a file two tables match is the first's, a file none matches no area's). A word two areas' vocabularies
each define for an element of their own is a homonym, no reliance: held apart (of the area of the word's second
entry) and counted in no figure, so a coupling of homonyms only is listed with none.\
Synopsis: `shop spec coupling`

```console
$ shop spec coupling --json
```

Each coupling is printed as `<area> by <other area>: <n> words, <n> elements, <n> requirements, <n> imports`,
then a line of its words, its elements (`object note`), its requirement ids and its imports
(`src/binder_shelf.py -> src/notes_store.py`) and its homonyms, the couplings with the most first. Under `--json` the
content is `{"couplings": [{"area", "by", "words", "elements", "requirements", "imports", "homonyms"}]}`; a context with no domain model
has no coupling.

### `shop spec assign`

Assigns a job of the product to the one bounded context whose capabilities serve it, kept among the bounded
context's jobs in the product file, in one commit. The bounded context is named by its id in the context id form,
`bounded-context/<domain>/<path>`, and is one the product holds (`shop spec context` declares it): an id of another
form is refused naming the id, and a bounded context the product does not hold naming it. A job is assigned once: a job a bounded context holds already is
refused naming the job.\
Synopsis: `shop spec assign <job> --to <bounded context>`

```console
$ shop spec assign j1 --to bounded-context/missingmass.io/shopsystem/shopsystem-bdd
assigned the job j1 to the bounded context bounded-context/missingmass.io/shopsystem/shopsystem-bdd
```

### `shop spec plays`

Maps a product actor to the actor a bounded context's model calls it by, kept among the bounded context's actors in
the product file, in one commit. A product actor the product does not hold is refused naming it before the actor is
checked, a bounded context whose id is not of the context id form naming the id, one the product does not declare
(`shop spec context` declares it) naming the bounded context, and, in this bounded context, an actor its domain model
does not declare naming `--as`.\
Synopsis: `shop spec plays <product actor> --in <bounded context> --as <actor>`

```console
$ shop spec plays "the developer" --in bounded-context/missingmass.io/shopsystem/shopsystem-bdd --as "the person"
mapped the product actor the developer to the person in the bounded context bounded-context/missingmass.io/shopsystem/shopsystem-bdd
```

### `shop spec unassign`

Takes a job back from the bounded context it is assigned to, in one commit of the product file, so it can be assigned
again with `shop spec assign`. A job the bounded context does not hold is refused naming the job.\
Synopsis: `shop spec unassign <job> --from <bounded context>`

```console
$ shop spec unassign j1 --from bounded-context/missingmass.io/shopsystem/shopsystem-bdd
unassigned the job j1 from the bounded context bounded-context/missingmass.io/shopsystem/shopsystem-bdd
```

### `shop spec drop job`

Takes a job out of the product file, in one commit. A job still referred to is refused naming what refers to it: a
job that needs it (the job), a bounded context that holds it (the bounded context; `shop spec unassign` it first) or a
subdomain that serves it (the subdomain). A job the product does not hold is refused naming it.\
Synopsis: `shop spec drop job <job>`

```console
$ shop spec drop job j1
dropped the job j1
```

### `shop spec drop actor`

Takes a product actor out of the product file, in one commit. One a job has (among its actors or in its job
statement) is refused naming the job, one a bounded context maps naming the bounded context, and one the product
does not hold naming it.\
Synopsis: `shop spec drop actor <product actor>`

```console
$ shop spec drop actor "the developer"
dropped the product actor the developer
```

### `shop spec drop subdomain`

Takes a subdomain out of the product's domain map, in one commit. One a bounded context addresses is refused naming
the bounded context, and one the product does not hold naming it.\
Synopsis: `shop spec drop subdomain <subdomain>`

```console
$ shop spec drop subdomain specification
dropped the subdomain specification
```

### `shop spec drop context`

Takes a bounded context out of the product's domain map, in one commit, with the product actors it maps. One that
holds a job is refused naming the job, one the product does not hold naming it, and an id not of the context id
form `bounded-context/<domain>/<path>` naming the id.\
Synopsis: `shop spec drop context <bounded context>`

```console
$ shop spec drop context bounded-context/missingmass.io/shopsystem/shopsystem-bdd
dropped the bounded context bounded-context/missingmass.io/shopsystem/shopsystem-bdd
```

### `shop spec decisions`

Writes `spec/decisions/index.md` from the decision files. Not committed.\
Synopsis: `shop spec decisions [--check]`

- `--check`: write nothing; say whether the index is current, then run the tests of each `check`-tier decision and
  print `holds` or `failing` for each.

```console
$ shop spec decisions --check
spec/decisions/index.md is current
holds    spec/decisions/0018-measure-refuses-unknown-shapes.md (design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-refuses-unknown-shapes): ...
...
9 check decisions: 6 hold, 3 failing
```

### `shop spec facts`

Prints the facts `shop spec check` reads, one a line, in clingo's syntax. For debugging a rule.\
Synopsis: `shop spec facts`

```console
$ shop spec facts
node("bounded-context/missingmass.io/shopsystem/shopsystem-bdd", "bounded-context").
...
```

### `shop spec constructs`

Writes or checks the construct catalogue `grammar/constructs.md`, each example parsed first. Each entry is a
construct a line may use, with its purpose, the item it came by (`Since: b<n>`), those that changed it (`Changed:`) and its example, the
entry's test; a line using a construct with no entry is refused
([the catalogues](design-model.md#the-catalogues-are-specification)).\
Synopsis: `shop spec constructs [--write] [--check]`

```console
$ shop spec constructs --check
grammar/constructs.md is current
```

### `shop spec catalogue entry`

Writes what an entry of the rule or the construct catalogue says into `grammar/catalogue-entries.toml`, and its
`- Purpose:`, `- Since:` and `- Changed:` lines into the catalogue when it holds the entry: its purpose, and the item
it came by, or, once it has one, an item that changed it. An entry of no rule or no construct is refused, naming it.\
Synopsis: `shop spec catalogue entry [--purpose P] [--item b<n>] entry`

- `entry`: `rules#<code>` or `constructs#<code>`.

```console
$ shop spec catalogue entry rules#v_c2 --item b462
wrote grammar/catalogue-entries.toml
wrote grammar/rules.md
```

### `shop spec restates`

For a repository that came from plugin 0.29: whether every old id is restated by a group, dropped or moved.\
Synopsis: `shop spec restates [--json] [capability]`

```console
$ shop spec restates backlog
spec/restated.json has no id of backlog
```

## shop features: the Gherkin

`shop features` writes the feature files from the codified capabilities and reads them back without the test runner. It
reads `features/` (or `--dir`).

### `shop features generate`

Writes `features/<capability>.feature` from each codified capability (all of them when none is named): one scenario a
group, tagged `@g<n> @r<n>`. Feature files are never edited by hand.\
Synopsis: `shop features generate [--check] [--preview FILE] [--root ROOT] [CAPABILITY ...]`

- `--check`: write nothing; exit 1 naming each file that differs from what it would write.
- `--preview <file>`: print the feature of a draft capability file.

```console
$ shop features generate items
wrote features/items.feature
$ shop features generate --check
```

### `shop features vocab`

Prints the step vocabulary: each function of the step grammar with its type. With `--check`, it checks that every
generated step parses and has exactly one handler registered with the plugin's `handler` (`from vocab import
handler`), loading the `world_*.py` and `*_handlers*.py` files under `--tests`. Steps bound with plain pytest-bdd
are not seen, so every one is reported: run your suite instead.\
Synopsis: `shop features vocab [--check] [--tests TESTS] [--root ROOT] [FEATURE ...]`

- `--tests <dir>`: where the step handlers are (default `tests/scenarios`).

```console
$ shop features vocab --check features/items.feature
every step has one handler
```

### `shop features bindings`

Reports each test that binds a scenario title no feature has (it would stop its module collecting), and with
`--unbound` each scenario no test binds.\
Synopsis: `shop features bindings [--tests TESTS] [--unbound [FEATURE ...]] [--json]`

```console
$ shop features bindings
every binding names a scenario
```

### `shop features list`

Lists the scenarios with a tag or a title.\
Synopsis: `shop features list (--tag TAG | --title TITLE) [--json]`

```console
$ shop features list --tag r15
features/checking.feature: Two glossary entries with one term
features/consistency.feature: `model logic` translates only over a relation in a response
features/context-requests.feature: A context request inspected gives its status and request lines
...
```

### `shop features count`

Counts the scenarios under each tag.\
Synopsis: `shop features count --by-tag`

```console
$ shop features count --by-tag
g1 1
g4 1
...
```

### `shop features deprecated`

Lists each deprecated scenario, a leftover of plugin 0.30, and what replaces it.\
Synopsis: `shop features deprecated [--json]`

```console
$ shop features deprecated
none deprecated
```

## shop tools: the grammar tools and code analysis

`shop tools` installs and checks the grammar tools the plugin needs, and gives agents a few code-analysis commands. It
works in the project's own interpreter (`--python`, else `.venv`, `venv` or `$VIRTUAL_ENV`).

### `shop tools install`

Installs any missing analysis tool into the project's virtualenv, then, every time, the grammar tools: GF 3.12, the
pinned `pgf` and `clingo` wheels, and the resource grammar library `gf-rgl`. Linux x86_64 only; elsewhere, set
`$SHOPSYSTEM_GF` to a GF you built. In a project with no Python file yet (a virtualenv's own files are not the
project's) it installs no analysis tool and still installs the grammar tools.\
Synopsis: `shop tools install [--python PYTHON]`

```console
$ shop tools install
every tool is present
pgf 1.1 already installed
clingo 5.8.2 already installed
gf 3.12 already installed
gf-rgl 20250812 already installed
```

### `shop tools probe`

Prints one line a tool, its version or what is missing, then the grammar block. Exits 1 when any is missing. In a
project with no Python file yet it probes the grammar tools alone.\
Synopsis: `shop tools probe [--python PYTHON] [--log] [--json]`

```console
$ shop tools probe
coverage 7.16.2
...
grammar:
  gf 3.12.0 (/home/vscode/.local/share/shopsystem-bdd/gf-3.12/bin/gf)
  pgf 1.1
  clingo 5.8.2
  gf-rgl 20250812 (/home/vscode/.local/share/shopsystem-bdd/gf-rgl-20250812)
```

### `shop tools check`

Runs ruff, vulture and import-linter over the paths given, or the Python files changed since `--base`; with neither,
the Python files changed since the base branch, `base` of `.shop/delivery.toml` or else `main`.\
Synopsis: `shop tools check [--python PYTHON] [--base BASE] [paths ...]`

```console
$ shop tools check scripts/tools_size.py
== ruff ==
All checks passed!
== vulture ==
clean
== import-linter ==
the project states no import contracts
```

### `shop tools size`

Prints each tracked Python file over a line limit (300 by default), and exits 1 when there is any.\
Synopsis: `shop tools size [--python PYTHON] [--limit LIMIT]`

```console
$ shop tools size --limit 300
```

### `shop tools refs`

Prints every reference to a name defined in the project, as `path:line`, following imports and aliases a text
search would miss.\
Synopsis: `shop tools refs [--python PYTHON] [--json] name`

```console
$ shop tools refs gf_binary
scripts/spec_gf.py:81
scripts/tools_grammar.py:115
...
10 references to gf_binary, in 2 production and 3 test files; defined at scripts/tools_grammar.py:81
```

### `shop tools map`

Runs the suite once under coverage, with a context a test, and keeps the map in `.shop/scratch/tools/coverage` for
`tests-of` and `untested`. Arguments after `--` go to pytest.\
Synopsis: `shop tools map [--python PYTHON] [--json] [pytest ...]`

### `shop tools tests-of`

Prints the tests that executed a file, function or line range in the last map.\
Synopsis: `shop tools tests-of [--python PYTHON] [--by-file] [--json] target`, the target `<file>[:<function>|:<line>-<line>]`.

```console
$ shop tools tests-of scripts/tools_size.py
tools: no map: make one with tools map
```

### `shop tools untested`

Prints each function of the files given that no test executed in the last map.\
Synopsis: `shop tools untested [--python PYTHON] [--json] files [files ...]`

## shop measure: what a batch cost

`shop measure` reads git and the sessions' transcripts. See the analyzing-a-batch skill for how Claude uses it.

### `shop measure batch`

Writes a batch's measurement, `.shop/records/measurements/<date>-<batch>.md`: its wall time, session time, tokens and
cost by role, review findings, defects and knobs. It is not committed, and not written over without `--replace`.\
Synopsis: `shop measure batch [--sessions SESSIONS] [--replace] batch`

- `--sessions <dir>`: the transcripts to read (default: Claude Code's store for this directory).

```console
$ shop measure batch batch-34
.shop/records/measurements/2026-11-10-batch-34.md
```

### `shop measure show`

Prints a measurement's figures as tables.\
Synopsis: `shop measure show record`

```console
$ shop measure show .shop/records/measurements/2026-11-10-batch-32.md
totals
total             | value
------------------+----------------------
wall time         | 18 minutes 41 seconds
...
...
```

### `shop measure compare`

Prints two measurements' totals side by side, with the ratio of the second to the first. Each is a record path or
`batch-<n>` (its newest measurement).\
Synopsis: `shop measure compare a b`

```console
$ shop measure compare batch-31 batch-32
total              | batch-31                   | batch-32              | ratio
-------------------+----------------------------+-----------------------+------
wall time          | 21 minutes 6 seconds       | 18 minutes 41 seconds | 0.89
...
cost               | 13.93                      | 8.45                  | 0.61
...
```

### `shop measure defect`

Records a fault found after the merge against its delivered item, `.shop/batches/<n>/defect-<k>.md`, and commits it
alone. `shop measure batch` counts it.\
Synopsis: `shop measure defect --says SAYS item`

```console
$ shop measure defect b250 --says "work show prints the status under the notes when the item has a long title; run work show on b250."
.shop/batches/34/defect-1.md
```

## shop migrate: moving between releases

`shop migrate` founds a new bounded context, and takes a repository from an older plugin release to this one.
[Upgrading](../upgrading.md) walks through it.

### `shop migrate init`

Founds a new bounded context in the repository it is run in: writes its scaffold and commits it in one commit.
`spec/index.md` (the id given, its last part the title, `language: codified-2`, `imports: [base, request]`, and the
`--purpose` given, if any, under its `## Purpose`), `spec/universal.md` (no condition), `spec/model/`, `spec/vocabulary/`, `spec/capabilities/`, `.shop/backlog/`,
`.shop/records/README.md` (an empty records index), `.shop/plugin-version` (the plugin's release),
`.shop/delivery.toml` (every key commented out at its default), `features/` and `tests/scenarios/conftest.py`, each
empty folder with a `.gitkeep`, and `.gitignore` naming `.venv/`, `__pycache__/`, `.pytest_cache/` and
`.ruff_cache/` (an existing one given the names it lacks, a name it holds with or without a leading or a trailing
`/` not lacked; one that lacks none left alone, out of the commit and of what it prints). An existing `features/` or conftest is left as it is. It refuses, changing nothing,
without `--id`, with an id that is not `bounded-context/<domain>/<path>` (its `<domain>` a domain name with a dot,
`example.org`, and its `<path>` one part or more), and in a repository that has a
`spec/index.md` or a `.shop/` already.\
Synopsis: `shop migrate init --id ID [--purpose PURPOSE]`

- `--purpose`: the context purpose, what the bounded context is for in a sentence or two, written under the index
  file's `## Purpose`; with none the section is left empty.

```console
$ shop migrate init --id bounded-context/example.org/notes/notes-cli
wrote .gitignore
wrote .shop/backlog/.gitkeep
...
wrote tests/scenarios/conftest.py
```

### `shop migrate status`

Prints the repository's plugin version, the plugin's, and each pending upgrade step.\
Synopsis: `shop migrate status [--hook]`

- `--hook`: what a session is told at its start; always exits 0. See [Hooks](#hooks).

```console
$ shop migrate status
the repository's plugin version: 0.33.0
the plugin's version: 0.33.0
```

### `shop migrate upgrade`

Applies each pending upgrade step in order (for 0.33.0, the `codified-2` marker, the CLI pack import, verbs'
aspects), commits it all, and reports what is left for you to reword, by file and id. With no step pending and
the repository behind the plugin, it records the plugin's release in `.shop/plugin-version` and commits it.\
Synopsis: `shop migrate upgrade`

```console
$ shop migrate upgrade
no upgrade step is pending
```

### `shop migrate run`

Moves a repository from the old system's layout (before 0.21) to the current one, every mechanical change or none. It is for
repositories on the old system only; nothing is committed.\
Synopsis: `shop migrate run --context CONTEXT`, the context written `<owner>/<product>/<context>`.

## Hooks

The plugin installs five hooks (`hooks/hooks.json`). Each runs at a fixed moment, prints little or nothing, and never
fails a session: any error exits 0 silently.

| when | hook | what it does |
|---|---|---|
| a session starts | `shop migrate status --hook` | says when the repository's plugin version is behind and `shop migrate upgrade` is pending; nothing when it is current |
| a session starts | `conversation_hook names` | prints the `shop work names --hook` table, so the session names items as `b3 "Fix the parser"`, never by id alone |
| a session starts | `conversation_hook directives` | prints the live directives' words (`shop work directives --hook`), to be followed and passed on in every brief; nothing with none |
| a session starts | `request_hook watch` | prints each request waiting on the other side, and the line to start `shop work watch --forward` with the Monitor tool; nothing with none |
| you send a prompt | `conversation_hook quote` | keeps the session and its transcript in the git dir for `shop work quote`; prints nothing, commits nothing |

`conversation_hook` and `request_hook` are small scripts beside `work` that import only the standard library and their
own modules, so a session starts fast. The names hook's start looks like this:

```console
$ shop work names --hook
The names of this repository's items and batches: tell the person each by its name beside its id (b3 "Fix the parser"), never by its id alone.
| id | name | status |
|---|---|---|
| b1 | Requests between repositories over GitHub issues | withdrawn |
...
```

What you see from them, and why, is in [Talking with Claude](../talking-with-claude.md#what-you-see-when-a-session-starts).

Next: [Recipes](../recipes.md) for common tasks, [Concepts](../concepts.md) for the words,
[Troubleshooting](../troubleshooting.md) when something refuses.
