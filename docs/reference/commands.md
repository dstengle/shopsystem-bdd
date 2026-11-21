<!--
Outputs on this page are from real runs on 2026-11-10: plugin 0.33.0, its scripts as at commit 7f60e57de
(branch plan-docs). Read-only commands ran in this repository. Commands that write ran in two scratch clones of it,
each with a local bare remote as `origin` and the suite's stand-in gh (tests/scripts/stub_gh.py as
$SHOPSYSTEM_WORK_GH), so batches, pull requests and request issues were real runs that touched no GitHub. Long scratch
paths are cut with "...", and long output is cut with "...". The `spec` section's parse, lexicon and explain, and the
item lines' ids, are from plugin 0.38.0 (2026-11-19, branch domain-contract).
-->

# Command reference

This page is for looking things up. It lists every command of the plugin's six tools, one subsection a command, so
you can find what a command does, what it takes, what it writes and what it prints. The tools and their commands are
the CLI adapter of the bounded context's services: each command requests one operation of the domain model, as
[`spec/adapters/cli.toml`](../../spec/adapters/cli.toml) maps them ([adapter contracts](adapters.md)).

You will rarely type these yourself: Claude runs them as you talk (see [Talking with Claude](../talking-with-claude.md)).
They are here for when you want to look, check or do a step by hand.

> **`--help` is the contract.** Every command prints its own usage and rules with `--help`
> (`work batch done --help`, `spec --help`). This page is a friendlier summary. Where the two differ, `--help` is
> right and this page is wrong; please file it.

Commands are written short, `work backlog` for `python3 "$SHOP/scripts/work" backlog`.
[How the commands are run](#how-the-commands-are-run) shows how to set that up.

## How the commands are run

Every console block on this page is what the session runs for you; you never need to. The tools are scripts in the
installed plugin's `scripts/` folder, not commands on your `PATH`, so a shell finds no `work` or `tools` of its own.
To run one yourself, keep the plugin's folder in `$SHOP`, from `claude plugin list --json`'s `installPath` (a path
that ends in the version, such as `~/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.44.0`; with
`claude --plugin-dir`, the checkout):

```console
$ export SHOP="$(claude plugin list --json | python3 -c 'import json, sys; print(next(p["installPath"] for p in json.load(sys.stdin) if p["id"] == "shopsystem-bdd@shopsystem-bdd"))')"
```

Then give each tool a short name:

```console
$ alias work='python3 "$SHOP/scripts/work"' spec='python3 "$SHOP/scripts/spec"' features='python3 "$SHOP/scripts/features"'
$ alias tools='python3 "$SHOP/scripts/tools"' measure='python3 "$SHOP/scripts/measure"' migrate='python3 "$SHOP/scripts/migrate"'
```

Put the `export` and the two `alias` lines in your shell's profile to keep them. The plugin's test plugin lives in
the same folder: a suite runs with `PYTHONPATH="$SHOP/scripts" pytest -p work_items`.

## A first taste

Here is an idea becoming a ready item, in four commands and four commits:

```console
$ work idea "work show prints the status of an item" --note "The person wants to see where an item stands at a glance."
b250 "work show prints the status of an item" idea
$ work shape b250
b250 "work show prints the status of an item" shaped
$ work line b250 --into items --group "An item shown gives its status" 'While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.'
b250 "work show prints the status of an item": items#r31
$ work ready b250
b250 "work show prints the status of an item" ready
```

Each command changed one file under `.shop/backlog/` and committed it alone. From there, `work batch start` picks
the item up. The rest of this page goes command by command.

## Things every command shares

- **Exit codes.** `0` success (the outcome `done`, `returned` or `passed`), `1` refused, a check failed, or broken,
  `2` bad usage. A refusal starts with the tool's name, says why, and changes nothing.
- **`--root`.** `work` and `spec` take `--root <dir>` before the subcommand (default: the current directory).
  `features generate` and `features vocab` take it after. `features` takes `--dir` for its feature files, `tools`
  takes `--python` for the project's interpreter.
- **Commits.** A `work` command that changes a file commits it, alone, with a message that starts with the command
  (`work shape: b250 ... idea -> shaped`), then pushes the branch to its remote. A refused push prints
  `not pushed: <remote>: <reason>` and keeps the commit.
- **`--json`.** Every command takes it and prints the response envelope, one JSON object: `outcome` (`done`,
  `returned`, `refused`, `passed`, `failed` or `broken`), `content` (what the operation returns), `errors` (each a
  reason and the things it names, by business reference: `parameter:tier`, `item:b12`) and `notices`. A command that
  printed a JSON object of its own before 0.38.0 prints it under `content` now (`work backlog --json`, `work batch
  status --json`, `spec check --json`, `features list --json` and the rest): read `.content` where you read the
  object. See [the response](adapters.md#the-response).

## work: items, batches, requests and records

`work` keeps the backlog (`.shop/backlog/`), the batches (`.shop/batches/`), the requests between bounded contexts
(`.shop/requests/`), the person's words (`.shop/quotes/`), decisions (`spec/decisions/`) and records
(`.shop/records/`). The words it uses (item, batch, request) are explained in [Concepts](../concepts.md).

### Items

#### `work idea`

Writes a new item in `idea` and commits it.\
Synopsis: `work idea [--provenance {own,peer,product}] [--note NOTE] title`

- `--note`: a line under the item's `## Notes`.
- `--provenance`: who it is for: `own` (the default), `peer` or `product`.

Writes `.shop/backlog/b<n>.md`, numbered after the highest. The example is in [A first taste](#a-first-taste).

#### `work shape`

Moves an item from `idea` to `shaped`: it is understood well enough to be given lines. An idea with no shaping note
(nothing under its `## Notes`) is groomed first: `work shape` without `--note` refuses it, naming the option.\
Synopsis: `work shape [--note NOTE] name`

```console
$ work shape b250
b250 "work show prints the status of an item" shaped
```

#### `work line`

Writes a requirement line into an item's `## Requirements`, under the capability it goes into, and commits it. It
takes an item that is `idea`, `shaped` or `in-batch`; an in-batch item's changed lines reach its batch with
[`work batch amend`](#work-batch-amend).\
Synopsis: `work line [--into INTO] [--group GROUP | --in IN_GROUP] [--retires CAP#rN] [--retirement-list FILE] [--no-line] [--reword CAP#rN] [--remove CAP#rN|CAP] [--term TERM] [--recodify CAP] [--relation RELATION] [--model MODEL] [--given GROUP BLOCK] [--universal UNIVERSAL] [--capability CAPABILITY] [--narrator NARRATOR] [--expose TABLES] [--withhold SERVICE.OPERATION] [--remove-model MODEL] [--reword-model HEADER] [--remove-term TERM] [--reword-term TERM] [--pack NAME] [--remove-universal U<n>] [--replace-universal U<n>] [--remove-upstream ID] [--replace-upstream ID] [--remove-given CAP#g<n>] [--replace-given CAP#g<n>] [--upstream UPSTREAM] name [text]`

- `--into <capability>`: the codified capability the line goes into.
- `--group "<title>"`: open a new group with this title (default: the item's title). `--in g<n>` joins one of the
  item's groups instead. Both go with a requirement line only; beside another piece they are refused.
- `--retires <cap>#r<n>`: the line replaces a live requirement, whose id goes to `retired:`, and the pair of the
  two to the block's `retires:` line. Ids are never reused. With `--no-line` and no line, the requirement is retired
  with nothing in its place, and no pair is written. Each design-decision whose `enforced_by` names the retired
  requirement is named, with the `work decision --amend` that names what holds it now.
- `--retirement-list <file>`: a retirement list, one pair a line, `<cap>#r<n> <line>`: each line retires its live
  requirement as `--retires` does, all in one commit. An id no requirement has refuses the whole list, naming it,
  and the item is left as it was.
- `--reword <cap>#r<n>`: the line takes the place of one of the item's own lines, keeping its id and group.
  `--remove <cap>#r<n>` takes one of them out, its group with it when it was the last line, and the id its
  `retires:` pair names; an id no pair names stays. Either refuses an id that is no line of the item, a live requirement's among them.
  `--remove <cap>` with no `#r<n>` takes the item's whole block of the capability out, a new capability's
  declaration with it, and the item's model lines of its area unless another of its blocks goes to that area.
- `--remove-model "<header>"`: the item's own element (`object label`, `service notes`) taken out of its model
  lines with its members; given with indented member lines, only those members go. `--reword-model "<header>"
  "<lines>"` puts the model lines given (checked as `--model`'s) in place of the element and its members.
  `--remove-term <term>` takes one of the item's terms out, and `--reword-term <term> -- "<entry>"` puts the entry
  in its place (`--` before an entry that opens with `-`); a term is named by its word, by `<word> → <element>` when
  two entries share the word, or by its whole bullet. A model block left empty goes. Each refuses a model line or a
  term the item does not hold, naming it, and `--into <capability>` picks the area of a model line two areas hold.
- `--remove-universal U<n>`, `--remove-upstream <bounded-context id>`, `--remove-given <cap>#g<n>`: the item's own
  universal condition, upstream entry or given block of its group taken out. `--replace-universal U<n> "<statement>"`,
  `--replace-upstream <id> "<entry>"` and `--replace-given <cap>#g<n> "<block>"` put the one given (checked as
  `--universal`'s, `--upstream`'s and `--given`'s are) in its place, a universal condition keeping its id. Each
  refuses a piece the item does not hold, naming it.
- `--term "<bullet>"`: a vocabulary entry (`- **<word>** (<part of speech>) → <element>. ...`) for the vocabulary of
  the capability's area, in place of a line. Give `--term` more than once to write several entries in one commit;
  one that does not read refuses them all.
- `--pack <name> --term "<bullet>"`: a term entry of the context's own pack `spec/packs/<name>.md`, kept in the
  item's `### <name> pack` block; `work batch start` appends it to the pack's `## Glossary`, makes the pack when it
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
  and its batch, in place of suggesting `--capability`. Lines and terms go into it with `--into <name>`; `work batch start` writes
  its file (with `area:` and `specifies:`) and names it in its area's row under `## Composition` of `spec/index.md`.
- `--expose '<tables>'`: the tables of one operation for the CLI adapter contract, `[operations."<service>.<operation>"]`
  with its `command` and its `[operations."<service>.<operation>".parameters]`, kept in the item's `### cli adapter`
  block in place of that operation's own; refused when the domain model, with the item's model lines, has no such
  operation. `--expose <service>.<operation>`, the operation alone, writes its tables from the domain model's
  operation: its command named after the operation (after the program the contract's other operations of its service
  are requested by, else the service), and each parameter an option named after it with an example of its type (its
  first value, its object's name, a flag `flag = true`). `--withhold <service>.<operation>` keeps an operation no command requests instead. `work batch start`
  lays each into `spec/adapters/cli.toml` (the table in place of the operation's own, a withheld operation under
  `[unexposed]` with its table out), the contract made when there is none.

The line gets the next free id of its capability (`items#r31`). It goes into `spec/` only when a batch starts.
`work line` does not parse the line; [`work ready`](#work-ready) does.

```console
$ work line b250 --into items --group "An item shown gives its status" 'While an item is `shaped`, when the person shows the item, the backlog service shall return the status of the item.'
b250 "work show prints the status of an item": items#r31
```

How to write a good line is in [Writing requirements](../writing-requirements.md); the file format is in
[the capability file](capability-file.md).

#### `work chore`

Writes a chore into an item in place of requirement lines, and commits the item: the files its work changes and the
command whose exit code 0 shows the work done. For an item with no behaviour a scenario checks (docs, skill text, a
refactor).\
Synopsis: `work chore [--file FILE] --check CHECK name`

- `--file <path>`: a file or a directory the work changes; give it once for each. A path under `spec/`,
  `features/` or `.shop/` is refused.
- `--check "<command>"`: the command that fails now and passes once the work is done.

Run again, it replaces the chore. A chore and requirement lines exclude each other: `work chore` refuses an item that
holds a requirement, and `work line` an item that holds a chore. [`work ready`](#work-ready) readies a chore item
without running its check; [`work batch done`](#work-batch-done) runs it.

```console
$ work chore b34 --file skills/shaping-items/SKILL.md --check "grep -q 'work chore' skills/shaping-items/SKILL.md"
b34 "The shaping skill names work chore": the chore of b34 "The shaping skill names work chore" (check: `grep -q 'work chore' skills/shaping-items/SKILL.md`)
```

#### `work rate`

Sets an item's value, urgency or size; the backlog ranks items by the score they make.\
Synopsis: `work rate [--value VALUE] [--urgency URGENCY] [--size SIZE] name`

- `--value`: `low-value`, `medium-value` or `high-value`.
- `--urgency`: `low-urgency`, `medium-urgency` or `high-urgency`.
- `--size`: `small`, `medium` or `large`.

```console
$ work rate b250 --value medium-value --urgency medium-urgency --size small
b250 "work show prints the status of an item" shaped
```

#### `work depend`

Writes that an item depends on another (`--on`), or drops a dependency (`--drop`). A dependency that would close a
cycle is refused.\
Synopsis: `work depend (--on ON | --drop DROP) name`

```console
$ work depend b251 --on b250
b251 "work show prints an item's dependencies" depends on b250 "work show prints the status of an item"
$ work depend b251 --drop b250
b251 "work show prints an item's dependencies" no longer depends on b250 "work show prints the status of an item"
```

#### `work ready`

Moves a `shaped` item to `ready` when it passes the readiness bar, and otherwise names every reason it does not. A
`ready` item is checked again: it stays `ready` when it still passes, and every reason is named when it does not.
Any other item is refused, named.\
Synopsis: `work ready name`

The bar lays the item's lines over a temporary copy of `spec/` and the construct catalogue and checks that they
parse (using no construct the catalogue has no entry of), that `spec logic` finds
no clash naming them, and that `features generate` writes their scenarios. A line from a request must be settled.
Readying is the decision to build: a ready item goes into the next batch.

```console
$ work ready b250
b250 "work show prints the status of an item" ready
$ work ready b253
work ready: b253 "work names prints every item" is not passing:
  items#r32: refused: the verb ready takes a subject, which a passive leaves out: agent readies item
```

What each reason means is in [Troubleshooting](../troubleshooting.md).

#### `work reopen`

Moves a `ready` item back to `shaped`, so that `work line` can change its lines; `work ready` readies it again. An
item that is not `ready` is refused, named.\
Synopsis: `work reopen name`

```console
$ work reopen b250
b250 "work show prints the status of an item" shaped
```

#### `work refuse`

Moves an item that is `idea` or `shaped` to `refused`, with the reason.\
Synopsis: `work refuse name reason`

```console
$ work refuse b251 "work show prints the dependencies already"
b251 "work show prints an item's dependencies" refused
```

#### `work withdraw`

Moves an item to `withdrawn`: nobody wants it any more, writing why under its `## Withdrawn`.\
Synopsis: `work withdraw name --reason REASON`

```console
$ work withdraw b252 --reason "work backlog's tables are read in a terminal's own colours"
b252 "A colour theme for work backlog" withdrawn
```

#### `work merge`

Moves an item that is `idea`, `shaped`, `ready` or `needs-input` to `withdrawn` because another item takes its
place, writing which and why under its `## Withdrawn`. A closed item is refused, named.\
Synopsis: `work merge name --into INTO --reason REASON`

```console
$ work merge b252 --into b250 --reason "b250 prints the theme too"
b252 "A colour theme for work backlog" withdrawn
```

#### `work annotate`

Adds a line to the `## Notes` of an item that is `idea`, `shaped`, `ready` or `needs-input` (a rating's reason, a
finding while shaping), in one commit of the item; a closed item is refused, named.\
Synopsis: `work annotate name note`

```console
$ work annotate b250 "value high: every session reads the status"
b250 "work show prints the status of an item": a note
```

#### `work retitle`

Gives an item that is not `delivered`, `refused` or `withdrawn` a new title, keeping its id, in one commit of the
item; a closed item is refused, named.\
Synopsis: `work retitle name title`

```console
$ work retitle b250 "work show prints the status and the batch of an item"
b250 "work show prints the status and the batch of an item"
```

#### `work split`

Moves requirement lines of an item that is `idea` or `shaped` to a new item, numbered next, that derives from it
(`derives_from:`): each line with its group's id, title and given block, the id it retires with it, and its status,
provenance, ratings, dependencies and request copied; both items in one commit. An item in another state is refused,
named, and so is a line the item does not hold. The new item is titled after the old one; `work retitle` names it.\
Synopsis: `work split name --requirement CAPABILITY#rN [--requirement ...]`

```console
$ work split b250 --requirement items#r12
b251 "work show prints the status of an item (split from b250)" split from b250 "work show prints the status of an item"
```

#### `work answer`

Answers the question of an item that is `needs-input` (parked mid-batch), and moves it back to `shaped`.\
Synopsis: `work answer name answer`

```console
$ work answer b253 "Yes, every item, whatever its status."
b253 "work names prints every item" shaped
```

#### `work backlog`

Prints every item, one table a state, in rank order, with what each waits on; an idea with no shaping note waits on
`work shape --note`. Writes nothing.\
Synopsis: `work backlog [--json]`

```console
$ work backlog
...
## shaped (29)

| rank | item | title | provenance | value | urgency | size | score | waiting on |
|---|---|---|---|---|---|---|---|---|
| 1 | b65 | An item with no notes is groomed before it is shaped | own | high-value | medium-urgency | small | 5.00 | - |
| 2 | b66 | A scenario's Given with an unknown condition word is refused | own | high-value | medium-urgency | small | 5.00 | - |
...
```

#### `work show`

Prints where an item, a request, a quote or a directive stands. With no target it prints what `work list` prints.\
Synopsis: `work show [--json] [target]`, where the target is `b<n>`, `q<n>`, `quote-<n>` or `directive-<n>`.

```console
$ work show b250
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

#### `work names`

Prints every item and batch with its name beside its id, one table. Writes nothing.\
Synopsis: `work names [--hook]`

- `--hook`: the SessionStart hook's form: the table under one line telling the session to name things, nothing
  when there is nothing to show. See [Hooks](#hooks).

```console
$ work names
| id | name | status |
|---|---|---|
| b1 | Requests between repositories over GitHub issues | withdrawn |
| b2 | Request lines into an upstream in the downstream's own terms | idea |
...
```

### Batches

A batch builds ready items together: one branch `batch-<n>`, one task (and worktree) an item, one pull request.
These are the commands the batch's driver runs; [Concepts](../concepts.md) draws the states.

#### `work batch start`

Picks the ready, unblocked items that pass the bar, in rank order, and starts a batch of them.\
Synopsis: `work batch start`

It makes the branch `batch-<n>` in its own worktree, lays the items' lines into `spec/` (their ids into `unbuilt:`),
regenerates the features and commits that, citing each item. On the base branch it commits
`.shop/batches/<n>/plan.md` with the items moved to `in-batch`. It writes the batch brief for the driver (never
committed). It is refused while `spec/` or `features/` has uncommitted changes, and the batch size comes from
`batch_size` in `.shop/delivery.toml`. It stops short of the review limit (`[review] size`, 1000 changed lines): an
item whose estimated change (from its size rating, its requirement lines and its model lines) would take the batch past
it after the items picked before is left out and stays `ready`; the first item is picked whatever its estimate.

```console
$ work batch start
batch-34 building: t1 b250 "work show prints the status of an item"
batch brief: .../repo/.shop/worktrees/batch-34-driver/brief.md
```

#### `work batch status`

Prints where a batch stands: its items, its tasks, its reviews. With no batch, the open one. Writes nothing.\
Synopsis: `work batch status [--json] [batch]`

```console
$ work batch status batch-34
batch-34 awaiting-merge, base main, pull request https://github.com/ex/ctx/pull/1
plan: .shop/batches/34/plan.md
reviews: 1, last clean
  b250 "work show prints the status of an item" in-batch
  t1 b250 "work show prints the status of an item": done, branch batch-34-b250
```

#### `work batch resume`

Gives each pending task its worktree, `batch-<n>-t<k>` on the branch `batch-<n>-b<j>`, and prints what each running
task builds. It also gives back a lost worktree, and one for each open review finding.\
Synopsis: `work batch resume batch`

```console
$ work batch resume batch-34
batch-34 building: plan .shop/batches/34/plan.md
t1 b250 "work show prints the status of an item": running in .shop/worktrees/batch-34-t1 on batch-34-b250: build items#r31; then work batch done batch-34 t1, or work batch park batch-34 b250 --question <text>
```

#### `work batch done`

Sets a running task done, once its worktree is clean, its commits cite the item (`Item: b<n>`), its ids have left
`unbuilt:` and the tests pass.\
Synopsis: `work batch done batch task`

The tests are `[batch] tests` of `.shop/delivery.toml` (default `python3 -m pytest -q -p work_items`), run in the
task's worktree, only the ones the task's change reaches: a capability's `tests/scenarios/test_<capability>.py` when
the item holds one of its ids or a commit of the task touches its feature, and a `tests/scripts/` test that names a
module the task touches; the pytest plugin `work_items` leaves the others out. `work batch review` runs them all. For an item that holds a chore, it then runs the chore's check there and refuses while it exits
non-zero, and refuses a commit of the task that touches a path the chore does not name. A refusal names what is
missing:

```console
$ work batch done batch-34 t1
work batch done: t1 b250 "work show prints the status of an item": the tests `python3 -m pytest -q -p work_items` failed in .shop/worktrees/batch-34-t1 (exit 1):
...
$ work batch done batch-34 t1
batch-34 t1 b250 "work show prints the status of an item": done
```

#### `work batch amend`

Lays an in-batch item's lines again on `batch-<n>` and on its task's branch, after `work line` changed them: the lines
it last laid are taken out and its lines as they now read laid in, one commit on each branch citing the item. A new id
is renumbered past the other items' lines on the batch branch (the item committed again on the base), a line laid
before with the same text keeps its place in `unbuilt:`, and a `done` task is set `running` again. Refused for an item
that is not `in-batch`, and while the task's worktree has uncommitted changes.\
Synopsis: `work batch amend item`

```console
$ work batch amend b253
batch-35 b253 "work names prints every item" amended: laid on batch-35, batch-35-b253
```

#### `work batch park`

Sets an item of the batch `needs-input` with a question, and takes its lines out of `batch-<n>`; the rest of the
batch carries on. You answer with [`work answer`](#work-answer).\
Synopsis: `work batch park --question QUESTION [--discard] batch item`

- `--question`: what the person is asked; `work backlog` shows it.
- `--discard`: throw away the uncommitted changes in the item's worktree (refused without it while there are any).

```console
$ work batch park batch-35 b253 --question "Should work names print withdrawn items too?"
batch-35 b253 "work names prints every item" -> needs-input: Should work names print withdrawn items too?
```

#### `work batch review`

Merges the in-batch items' branches into `batch-<n>`, runs the tests, pushes, and opens the batch's draft pull
request. The batch goes `in-review`.\
Synopsis: `work batch review batch`

On a second round it also checks that each fix commit cites an open finding (`Finding: f<k>`) and each open finding
has one.

```console
$ work batch review batch-34
next: work batch brief batch-34, the pr-reviewer on it, then work batch reviewed batch-34
https://github.com/ex/ctx/pull/1
```

#### `work batch brief`

Writes the brief of the next review of a batch's pull request, for the `pr-reviewer` agent: the range, the items'
lines, the judgement decisions, the rules and the `[review] checks` runs. Nothing is committed.\
Synopsis: `work batch brief batch`

```console
$ work batch brief batch-34
.shop/worktrees/batch-34-review-1/brief.md
```

#### `work batch reviewed`

Records the findings file (the reviewer's reply, saved where the brief says): writes
`.shop/batches/<n>/review-<k>.md`, posts it on the pull request, and moves the batch back to `building` while a
finding is open, or to `awaiting-merge` (the pull request marked ready) when none is.\
Synopsis: `work batch reviewed batch`

```console
$ work batch reviewed batch-34
batch-34 review 1: 1 finding -> awaiting-merge; the pull request https://github.com/ex/ctx/pull/1 is ready for the person's merge
```

#### `work batch merged`

Records the merge of the batch's pull request once GitHub says it is merged and its merge commit is in the base: the
in-batch items become `delivered`, and the batch's worktrees, review folders, brief folder and item branches are
removed.\
Synopsis: `work batch merged batch`

```console
$ work batch merged batch-34
batch-34 merged
```

#### `work batch abandon`

Abandons a batch: its pull request is closed, its in-batch items are `ready` again, and its worktrees are removed.\
Synopsis: `work batch abandon [--discard] batch`

- `--discard`: throw away uncommitted changes in its task worktrees (refused without it while there are any).

```console
$ work batch abandon batch-35
batch-35 abandoned
```

#### `work settings set`

Sets one setting of `.shop/delivery.toml` in its own table, every comment and other key kept, and commits it. The
settings are `base`, `batch_size`, `batch.push`, `batch.tests`, `batch.worktrees`, `batch.rules`, `review.size`,
`review.checks` and `prices.<model>`; a setting the plugin does not read, or a value not of its type, is refused, naming it.\
Synopsis: `work settings set setting value`

- `value`: a TOML value (`7`, `["a", "b"]`, `{ input = 3.0, output = 15.0, cache_read = 0.3 }`); a text setting's may
  be the bare text.

```console
$ work settings set review.size 1500
.shop/delivery.toml: review.size = 1500
```

### Requests

A request is one bounded context asking another (its upstream, or itself) for behaviour, carried on a GitHub issue.
Each step below commits the request file `.shop/requests/q<n>.md`, then posts the step on the issue and commits its
URL. The examples follow one request, `q48`, that this repository raised to itself.

#### `work request`

Asks an upstream (or this context): writes the request, opens its issue, and commits both.\
Synopsis: `work request [--from ASKER] [--ask ASK] [--to TO] [--source SOURCE] [--thread THREAD] [--raised-for RAISED_FOR] title`

- `--from`: the asker: this bounded context's id, or `internal` for a request this context raises to itself
  (optional; default: this context).
- `--ask`: what the asker needs, in its own words (default: the title).
- `--to`: the upstream, one of `spec/index.md`'s `## Upstreams` (default: the one upstream, or this context).
- `--source`: the origin of a request this context asks itself; `--thread` or `--raised-for` for one another
  context asks.

```console
$ work request "Show an item's status in work show" --from bounded-context/missingmass.io/shopsystem/shopsystem-bdd --source observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-probe-repositories-again --ask "When I run work show on an item, I want to see its status."
q48 https://github.com/ex/ctx/issues/1
```

#### `work offer`

The upstream's offer, under `## Offer`: each capability that may serve the request quoted by its groups and
requirements, with only the terms they mention, so the asker can write lines in the upstream's words. With no
`--capability` the offer is the note alone, no vocabulary. It passes the turn to the asker and prints the request, its
status and its turn.\
Synopsis: `work offer [--capability CAPABILITY] [--note NOTE] request`

```console
$ work offer q48 --capability backlog --note "work show prints an item's title and rating today; the backlog capability would hold the status too."
q48 awaiting-asker asker
```

#### `work fits`

The asker's answer to an offer when existing behaviour already serves it: the request is `delivered` and its issue
closed.\
Synopsis: `work fits [--serves SERVES] request`

```console
$ work fits q49 --serves items#r12
$ work show q49
q49 delivered asker
it is the asker's turn, on https://github.com/ex/ctx/issues/2
  resolution line 1: items#r12
```

#### `work propose`

The asker's lines, one `--line` each, in the upstream's words; it prints the request, its status and its turn.\
Synopsis: `work propose [--line LINES] request`

```console
$ work propose q48 --line 'When the person shows an item, the backlog service shall return the status of the item.'
q48 awaiting-asker asker
```

#### `work turn`

Passes a request's turn to the other side, posts it, and prints the request, its status and its turn.\
Synopsis: `work turn request`

```console
$ work turn q48
q48 awaiting-upstream upstream
```

#### `work ask`

The upstream's question on one line of a request.\
Synopsis: `work ask request line question`

```console
$ work ask q48 1 "Should the status be the item's state, such as ready?"
```

#### `work reply`

The asker's answer to a question of a request; it prints the request, its status and its turn.\
Synopsis: `work reply request question answer`

```console
$ work reply q48 1 "Yes: the state the backlog shows it under."
$ work show q48
q48 awaiting-upstream upstream
it is the upstream's turn, on https://github.com/ex/ctx/issues/1
  line 1: unsettled - When the person shows an item, the backlog service shall return the status of the item.
  question 1: line 1: Should the status be the item's state, such as ready?
  answer 1: Yes: the state the backlog shows it under.
```

#### `work outcome`

The upstream's outcome of one line: `accepted`, `rewritten`, `refused`, `question` or `withdrawn`. An accepted line
is parsed in this context's grammar first.\
Synopsis: `work outcome [--into INTO] [--group GROUP] [--reason REASON] [--line TEXT] request line outcome`

- `--into <capability>` (and `--group`): where an accepted line goes.
- `--reason`: why, under the request's `## Reasons` (needed for `refused`).
- `--line`: the counter-proposal of a `rewritten` line.

```console
$ work outcome q48 1 accepted --into backlog
```

#### `work accept`

Accepts a request whose lines are settled: it becomes a `shaped` item with each accepted line under its capability,
and the request is `accepted`.\
Synopsis: `work accept request`

```console
$ work accept q48
b250 "Show an item's status in work show" shaped
```

#### `work resolve`

Writes which requirement holds each accepted line, and in which version; the request is `delivered`.\
Synopsis: `work resolve [--line N REQUIREMENT VERSION] request`

```console
$ work resolve q48 --line 1 items#r31 0.38.0
```

#### `work list`

Prints each request with its status, and each observation no source cites. Writes nothing.\
Synopsis: `work list [--json]`

```console
$ work list
request q14 accepted
request q48 delivered
request q49 open
observation observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-proposal-argues-many 2026-10-15
...
```

#### `work sync`

Brings the requests up to date with their issues: each comment a record does not hold is applied and recorded, a new
ask on this context's own repository becomes a request, and every request is printed with whose move it waits on.\
Synopsis: `work sync`

```console
$ work sync
q14 "Requests go through one shared tool" accepted: the upstream's turn, waiting on this side
q48 "Show an item's status in work show" delivered
q49 "Print the item's title in work show" open: the upstream's turn, waiting on this side
```

#### `work watch`

Watches the open requests' issues and prints each new comment or ask once, then ends. Nothing is committed.\
Synopsis: `work watch [--every EVERY] [--polls POLLS] [--forward] [--hook]`

- `--every`: seconds between polls (default 60).
- `--polls`: give up, exit 1, after this many empty polls (default: never).
- `--forward`: wake on GitHub's events through `gh webhook forward`, polling notifications where it cannot. Claude
  runs this one with the Monitor tool.
- `--hook`: the SessionStart hook's form. See [Hooks](#hooks).

```console
$ work watch --every 1 --polls 1
work watch: nothing new after 1 poll
```

### The person's words, decisions and records

#### `work quote`

Copies the person's message holding these words, with the two messages before and after it, into
`.shop/quotes/<n>.md`, and commits it. Later, `work show quote-<n>` prints it.\
Synopsis: `work quote [--session SESSION] [--transcript TRANSCRIPT] [--hook] [words]`

- `--session`, `--transcript`: where to look (default: the session the prompt hook kept).
- `--hook`: the UserPromptSubmit hook's form. See [Hooks](#hooks).

```console
$ work quote --transcript ~/.claude/projects/-home-vscode-shopsystem-bdd/72e23fa5-6dee-49f3-a1d1-7e79096a0501.jsonl "I trust you to make some delightful docs."
quote-24 "I trust you to make some delightful docs."
$ work show quote-20
quote-20 "Once 4.0 is done, take a new backlog item to make some nice …"
  session: 72e23fa5-6dee-49f3-a1d1-7e79096a0501
  date: 2026-11-10
...
```

#### `work directive`

Keeps a short-term direction of the person in the repository, never in a session's memory: their words as a quote
(found as `work quote` finds them) and a `live` directive citing it, `.shop/directives/<n>.md`, in one commit. With
`--quote`, a directive of a quote already kept.\
Synopsis: `work directive [--session SESSION] [--transcript TRANSCRIPT] [--quote QUOTE] [words]`

```console
$ work directive --quote quote-42
directive-1 "Merge and release while I am away." citing quote-42
```

#### `work directives`

Prints the live directives, each with its id, date, age and words. Writes nothing.\
Synopsis: `work directives [--all] [--hook]`

- `--all`: every directive, with its status.
- `--hook`: the SessionStart hook's form: the live directives' words under one line telling the session to follow
  them and pass them on in every brief, nothing when none is live. See [Hooks](#hooks).

#### `work promote`

Promotes a live directive to what it became, once the session has written it: an item, a design-decision or a
line of `CLAUDE.md`. A directive that is not live, or a target that does not exist, is refused, naming it.\
Synopsis: `work promote --to TO name`

```console
$ work promote directive-1 --to b20
directive-1 "Merge and release while I am away." promoted to b20
```

#### `work drop`

Drops a live directive, with the reason. A directive that is not live is refused, naming it.\
Synopsis: `work drop --why WHY name`

#### `work decision`

Writes a design-decision, `spec/decisions/<nnnn>-<slug>.md`, rewrites `spec/decisions/index.md`, and commits both.\
Synopsis: `work decision [--amend DECISION] [--summary SUMMARY] [--tier {check,requirement,judgement}] [--decision DECISION] [--context CONTEXT] [--alternatives ALTERNATIVES] [--enforced-by ENFORCED_BY] [--verified-by {scenario,check,judgement,monitor}] [--rests-on RESTS_ON] [--supersedes SUPERSEDES] [--source SOURCE] [--by BY] [--slug SLUG] [--date DATE] [title]`

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
$ work decision "The command reference defers to --help" --summary "Where the command reference and --help differ, --help wins." --tier judgement --decision "Each command's --help is its contract; the reference page links to it and never overrides it."
spec/decisions/0093-the-command-reference-defers-to-help.md
```

#### `work record`

Writes a record, `.shop/records/<date>-<slug>.md`, adds its row to `.shop/records/README.md`, and commits both. A
record that exists is refused: a committed record is never edited.\
Synopsis: `work record --kind {analysis,design,measurement,review-finding,decision-argument} --summary SUMMARY --body BODY [--about ABOUT] [--slug SLUG] [--date DATE] title`

- `--body <file>`: the record's text, under its title.
- `--summary`: its row in the index, one line.
- `--about <id>`: the node, item or batch it is about, one this repository holds (default: the bounded context).

```console
$ work record "Command reference layout" --kind analysis --summary "Why the command reference has one section a tool" --body body.md
.shop/records/2026-11-10-command-reference-layout.md
```

## spec: the spec, checked

`spec` reads `spec/` and `.shop/`, checks them, and parses lines. It was called `model` before 0.38.0; `model` still
works in 0.38 and prints a notice that it goes in the next release. Only `decisions`, `rules --write` and
`constructs --write` write files, and none of them commits.

### `spec parse`

Parses a line in the context's grammar and prints its tree, or its refusal with a hint.\
Synopsis: `spec parse [--file FILE] [--form] [--item b<n>] [line]`

- `--form`: print the line's meaning (its logical form) instead of its tree. Read this one.
- `--file`: parse every line of a file, numbered.
- `--item b<n>`: read the line as it reads once the terms, relation rows, lines and model lines the item holds are
  laid into the specification, on a copy, as `work ready` lays them; nothing in `spec/` changes. Use it to see why
  a line of an item is refused without running `work ready`.

```console
$ spec parse --form 'When the person shows an item, the backlog service shall return the status of the item.'
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: item]
    request(e1, backlog.show, subject: x1, object: x2)
  response [x4: status]
    status(x2) = x4
    return(e2, subject: x3, object: x4)
$ spec parse 'When an item is readied, the backlog service shall return the status of the item.'
refused: the verb ready takes a subject, which a passive leaves out: agent readies item
  parsed up to: When an
  nearest words: item, items, `item`, term, stem
  may follow: (none)
```

The second line is a counter-example: the grammar has no "an item is readied", so it is refused. How to read a
refusal is in [Writing requirements](../writing-requirements.md).

### `spec lexicon`

Lists the context's words by category: actors, kinds, attributes, events, conditions.\
Synopsis: `spec lexicon [--check]`

- `--check`: report problems with the terms (`v_t4` to `v_t15`), and exit 1 when there is any.

```console
$ spec lexicon
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

### `spec explain`

Prints a requirement, what it also means because of other requirements, and what takes precedence over it.\
Synopsis: `spec explain requirement`

```console
$ spec explain items#r15
items#r15  While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
which also means:
  the backlog service shall change nothing (by U17)
  the backlog service shall name a reason (by U17)
```

### `spec check`

Solves the facts of the repository against the design model's rules and prints every violation (`v_...`), then
warnings (`w_...`), unresolved references and file problems. Exits 1 on any violation.\
Synopsis: `spec check [--json] [--limit LIMIT]`

- `--limit`: rows shown for each rule (the rest are counted).

```console
$ spec check
warning w_example  a requirement holds example data: a code or quoted string that names no declared constant  (41)
    capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools#r37, .venv/bin/python
...
0 violations, 57 warnings, 0 unresolved references, 0 file problems
```

What each rule guards is in [the design model reference](design-model.md).

### `spec logic`

The temporal and entailment check of the codified lines: clashes between requirements (L1 to L8). Give a capability,
or a requirement id for the findings that name it. A requirement it has no translation of is printed
`unread <id>: <what it cannot read>`, and the count says how many are unread in place of `no findings`; the exit is
the findings' alone.\
Synopsis: `spec logic [--json] [capability]`

```console
$ spec logic backlog
no findings
```

### `spec rules`

Prints every rule's code and plain label, violations first.\
Synopsis: `spec rules [--json] [--write] [--check]`

- `--write`: write the rule catalogue `grammar/rules.md`; `--check` says whether it is current. The catalogue is
  part of the plugin's specification: each entry's purpose, `Since:` and `Changed:` (items, or a release for the oldest), and its fact sets,
  the entry's test ([the catalogues](design-model.md#the-catalogues-are-specification)).

```console
$ spec rules
v2  a standing edge touches something that is not standing
v3  a request's resolution names something that is not a requirement of the spec
...
```

### `spec forms`

Prints every file form a context keeps: its name, its path and the command that writes it (or the plugin's item
that will give it one).\
Synopsis: `spec forms [--json] [--check]`

- `--json`: print `{"forms": [{"name", "path", "writer", "kind"}]}`, each form's `kind` the kind of its writer:
  `command`, `item` (a plugin item that will give it one) or `hand`.
- `--check`: print nothing and exit 0 unless a form is written by hand; each such form is named on stderr and it
  exits 1.

```console
$ spec forms
item                      .shop/backlog/b<n>.md                                work idea
item's requirement line   .shop/backlog/b<n>.md ## Requirements                work line
...
capability                spec/capabilities/<name>.md                          work line --capability
...
```

### `spec annotate`

Writes, under each operation of each adapter contract (`spec/adapters/cli.toml`), the requirements that govern it:
each requirement whose trigger requests the operation, its refusals among them, as
`requirements = ["<capability>#r<n>: <line>", ...]`
([adapter contracts](adapters.md)). It prints each contract it wrote (`annotated`) or found
current (`current`) and exits 0.\
Synopsis: `spec annotate [<adapter contract> ...] [--check]`

- `--check`: write nothing; each stale contract is named on stderr and it exits 1. `spec check` fails the same
  contract too, naming each operation and requirement (`v_a5`, `v_a6`).

```console
$ spec annotate
annotated spec/adapters/cli.toml
$ spec annotate --check
```

### `spec decisions`

Writes `spec/decisions/index.md` from the decision files. Not committed.\
Synopsis: `spec decisions [--check]`

- `--check`: write nothing; say whether the index is current, then run the tests of each `check`-tier decision and
  print `holds` or `failing` for each.

```console
$ spec decisions --check
spec/decisions/index.md is current
holds    spec/decisions/0018-measure-refuses-unknown-shapes.md (design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-refuses-unknown-shapes): ...
...
9 check decisions: 6 hold, 3 failing
```

### `spec facts`

Prints the facts `spec check` reads, one a line, in clingo's syntax. For debugging a rule.\
Synopsis: `spec facts`

```console
$ spec facts
node("bounded-context/missingmass.io/shopsystem/shopsystem-bdd", "bounded-context").
...
```

### `spec constructs`

Writes or checks the construct catalogue `grammar/constructs.md`, each example parsed first. Each entry is a
construct a line may use, with its purpose, the item it came by (`Since: b<n>`), those that changed it (`Changed:`) and its example, the
entry's test; a line using a construct with no entry is refused
([the catalogues](design-model.md#the-catalogues-are-specification)).\
Synopsis: `spec constructs [--write] [--check]`

```console
$ spec constructs --check
grammar/constructs.md is current
```

### `spec catalogue entry`

Writes what an entry of the rule or the construct catalogue says into `grammar/catalogue-entries.toml`, and its
`- Purpose:`, `- Since:` and `- Changed:` lines into the catalogue when it holds the entry: its purpose, and the item
it came by, or, once it has one, an item that changed it. An entry of no rule or no construct is refused, naming it.\
Synopsis: `spec catalogue entry [--purpose P] [--item b<n>] entry`

- `entry`: `rules#<code>` or `constructs#<code>`.

```console
$ spec catalogue entry rules#v_c2 --item b462
wrote grammar/catalogue-entries.toml
wrote grammar/rules.md
```

### `spec restates`

For a repository that came from plugin 0.29: whether every old id is restated by a group, dropped or moved.\
Synopsis: `spec restates [--json] [capability]`

```console
$ spec restates backlog
spec/restated.json has no id of backlog
```

## features: the Gherkin

`features` writes the feature files from the codified capabilities and reads them back without the test runner. It
reads `features/` (or `--dir`).

### `features generate`

Writes `features/<capability>.feature` from each codified capability (all of them when none is named): one scenario a
group, tagged `@g<n> @r<n>`. Feature files are never edited by hand.\
Synopsis: `features generate [--check] [--preview FILE] [--root ROOT] [CAPABILITY ...]`

- `--check`: write nothing; exit 1 naming each file that differs from what it would write.
- `--preview <file>`: print the feature of a draft capability file.

```console
$ features generate items
wrote features/items.feature
$ features generate --check
```

### `features vocab`

Prints the step vocabulary: each function of the step grammar with its type. With `--check`, it checks that every
generated step parses and has exactly one handler registered with the plugin's `handler` (`from vocab import
handler`), loading the `world_*.py` and `*_handlers*.py` files under `--tests`. Steps bound with plain pytest-bdd
are not seen, so every one is reported: run your suite instead.\
Synopsis: `features vocab [--check] [--tests TESTS] [--root ROOT] [FEATURE ...]`

- `--tests <dir>`: where the step handlers are (default `tests/scenarios`).

```console
$ features vocab --check features/items.feature
every step has one handler
```

### `features bindings`

Reports each test that binds a scenario title no feature has (it would stop its module collecting), and with
`--unbound` each scenario no test binds.\
Synopsis: `features bindings [--tests TESTS] [--unbound [FEATURE ...]] [--json]`

```console
$ features bindings
every binding names a scenario
```

### `features list`

Lists the scenarios with a tag or a title.\
Synopsis: `features list (--tag TAG | --title TITLE) [--json]`

```console
$ features list --tag r15
features/checking.feature: Two glossary entries with one term
features/consistency.feature: `model logic` translates only over a relation in a response
features/context-requests.feature: A context request inspected gives its status and request lines
...
```

### `features count`

Counts the scenarios under each tag.\
Synopsis: `features count --by-tag`

```console
$ features count --by-tag
g1 1
g4 1
...
```

### `features deprecated`

Lists each deprecated scenario, a leftover of plugin 0.30, and what replaces it.\
Synopsis: `features deprecated [--json]`

```console
$ features deprecated
none deprecated
```

## tools: the grammar tools and code analysis

`tools` installs and checks the grammar tools the plugin needs, and gives agents a few code-analysis commands. It
works in the project's own interpreter (`--python`, else `.venv`, `venv` or `$VIRTUAL_ENV`).

### `tools install`

Installs any missing analysis tool into the project's virtualenv, then, every time, the grammar tools: GF 3.12, the
pinned `pgf` and `clingo` wheels, and the resource grammar library `gf-rgl`. Linux x86_64 only; elsewhere, set
`$SHOPSYSTEM_GF` to a GF you built. In a project with no Python file yet (a virtualenv's own files are not the
project's) it installs no analysis tool and still installs the grammar tools.\
Synopsis: `tools install [--python PYTHON]`

```console
$ tools install
every tool is present
pgf 1.1 already installed
clingo 5.8.2 already installed
gf 3.12 already installed
gf-rgl 20250812 already installed
```

### `tools probe`

Prints one line a tool, its version or what is missing, then the grammar block. Exits 1 when any is missing. In a
project with no Python file yet it probes the grammar tools alone.\
Synopsis: `tools probe [--python PYTHON] [--log] [--json]`

```console
$ tools probe
coverage 7.16.2
...
grammar:
  gf 3.12.0 (/home/vscode/.local/share/shopsystem-bdd/gf-3.12/bin/gf)
  pgf 1.1
  clingo 5.8.2
  gf-rgl 20250812 (/home/vscode/.local/share/shopsystem-bdd/gf-rgl-20250812)
```

### `tools check`

Runs ruff, vulture and import-linter over the paths given, or the Python files changed since `--base`; with neither,
the Python files changed since the base branch, `base` of `.shop/delivery.toml` or else `main`.\
Synopsis: `tools check [--python PYTHON] [--base BASE] [paths ...]`

```console
$ tools check scripts/tools_size.py
== ruff ==
All checks passed!
== vulture ==
clean
== import-linter ==
the project states no import contracts
```

### `tools size`

Prints each tracked Python file over a line limit (300 by default), and exits 1 when there is any.\
Synopsis: `tools size [--python PYTHON] [--limit LIMIT]`

```console
$ tools size --limit 300
```

### `tools refs`

Prints every reference to a name defined in the project, as `path:line`, following imports and aliases a text
search would miss.\
Synopsis: `tools refs [--python PYTHON] [--json] name`

```console
$ tools refs gf_binary
scripts/spec_gf.py:81
scripts/tools_grammar.py:115
...
10 references to gf_binary, in 2 production and 3 test files; defined at scripts/tools_grammar.py:81
```

### `tools map`

Runs the suite once under coverage, with a context a test, and keeps the map in `.shop/scratch/tools/coverage` for
`tests-of` and `untested`. Arguments after `--` go to pytest.\
Synopsis: `tools map [--python PYTHON] [--json] [pytest ...]`

### `tools tests-of`

Prints the tests that executed a file, function or line range in the last map.\
Synopsis: `tools tests-of [--python PYTHON] [--by-file] [--json] target`, the target `<file>[:<function>|:<line>-<line>]`.

```console
$ tools tests-of scripts/tools_size.py
tools: no map: make one with tools map
```

### `tools untested`

Prints each function of the files given that no test executed in the last map.\
Synopsis: `tools untested [--python PYTHON] [--json] files [files ...]`

## measure: what a batch cost

`measure` reads git and the sessions' transcripts. See the analyzing-a-batch skill for how Claude uses it.

### `measure batch`

Writes a batch's measurement, `.shop/records/measurements/<date>-<batch>.md`: its wall time, session time, tokens and
cost by role, review findings, defects and knobs. It is not committed, and not written over without `--replace`.\
Synopsis: `measure batch [--sessions SESSIONS] [--replace] batch`

- `--sessions <dir>`: the transcripts to read (default: Claude Code's store for this directory).

```console
$ measure batch batch-34
.shop/records/measurements/2026-11-10-batch-34.md
```

### `measure show`

Prints a measurement's figures as tables.\
Synopsis: `measure show record`

```console
$ measure show .shop/records/measurements/2026-11-10-batch-32.md
totals
total             | value
------------------+----------------------
wall time         | 18 minutes 41 seconds
...
...
```

### `measure compare`

Prints two measurements' totals side by side, with the ratio of the second to the first. Each is a record path or
`batch-<n>` (its newest measurement).\
Synopsis: `measure compare a b`

```console
$ measure compare batch-31 batch-32
total              | batch-31                   | batch-32              | ratio
-------------------+----------------------------+-----------------------+------
wall time          | 21 minutes 6 seconds       | 18 minutes 41 seconds | 0.89
...
cost               | 13.93                      | 8.45                  | 0.61
...
```

### `measure defect`

Records a fault found after the merge against its delivered item, `.shop/batches/<n>/defect-<k>.md`, and commits it
alone. `measure batch` counts it.\
Synopsis: `measure defect --says SAYS item`

```console
$ measure defect b250 --says "work show prints the status under the notes when the item has a long title; run work show on b250."
.shop/batches/34/defect-1.md
```

## migrate: moving between releases

`migrate` founds a new bounded context, and takes a repository from an older plugin release to this one.
[Upgrading](../upgrading.md) walks through it.

### `migrate init`

Founds a new bounded context in the repository it is run in: writes its scaffold and commits it in one commit.
`spec/index.md` (the id given, its last part the title, `language: codified-2`, `imports: [request]`, and the
`--purpose` given, if any, under its `## Purpose`), `spec/universal.md` (no condition), `spec/model/`, `spec/vocabulary/`, `spec/capabilities/`, `.shop/backlog/`,
`.shop/records/README.md` (an empty records index), `.shop/plugin-version` (the plugin's release),
`.shop/delivery.toml` (every key commented out at its default), `features/` and `tests/scenarios/conftest.py`, each
empty folder with a `.gitkeep`, and `.gitignore` naming `.venv/`, `__pycache__/`, `.pytest_cache/` and
`.ruff_cache/` (an existing one given the names it lacks, a name it holds with or without a leading or a trailing
`/` not lacked; one that lacks none left alone, out of the commit and of what it prints). An existing `features/` or conftest is left as it is. It refuses, changing nothing,
without `--id`, with an id that is not `bounded-context/<domain>/<path>` (its `<domain>` a domain name with a dot,
`example.org`, and its `<path>` one part or more), and in a repository that has a
`spec/index.md` or a `.shop/` already.\
Synopsis: `migrate init --id ID [--purpose PURPOSE]`

- `--purpose`: the context purpose, what the bounded context is for in a sentence or two, written under the index
  file's `## Purpose`; with none the section is left empty.

```console
$ migrate init --id bounded-context/example.org/notes/notes-cli
wrote .gitignore
wrote .shop/backlog/.gitkeep
...
wrote tests/scenarios/conftest.py
```

### `migrate status`

Prints the repository's plugin version, the plugin's, and each pending upgrade step.\
Synopsis: `migrate status [--hook]`

- `--hook`: what a session is told at its start; always exits 0. See [Hooks](#hooks).

```console
$ migrate status
the repository's plugin version: 0.33.0
the plugin's version: 0.33.0
```

### `migrate upgrade`

Applies each pending upgrade step in order (for 0.33.0, the `codified-2` marker, the CLI pack import, verbs'
aspects), commits it all, and reports what is left for you to reword, by file and id. With no step pending and
the repository behind the plugin, it records the plugin's release in `.shop/plugin-version` and commits it.\
Synopsis: `migrate upgrade`

```console
$ migrate upgrade
no upgrade step is pending
```

### `migrate run`

Moves a repository from the old system's layout (before 0.21) to the current one, every mechanical change or none. It is for
repositories on the old system only; nothing is committed.\
Synopsis: `migrate run --context CONTEXT`, the context written `<owner>/<product>/<context>`.

## Hooks

The plugin installs five hooks (`hooks/hooks.json`). Each runs at a fixed moment, prints little or nothing, and never
fails a session: any error exits 0 silently.

| when | hook | what it does |
|---|---|---|
| a session starts | `migrate status --hook` | says when the repository's plugin version is behind and `migrate upgrade` is pending; nothing when it is current |
| a session starts | `conversation_hook names` | prints the `work names --hook` table, so the session names items as `b3 "Fix the parser"`, never by id alone |
| a session starts | `conversation_hook directives` | prints the live directives' words (`work directives --hook`), to be followed and passed on in every brief; nothing with none |
| a session starts | `request_hook watch` | prints each request waiting on the other side, and the line to start `work watch --forward` with the Monitor tool; nothing with none |
| you send a prompt | `conversation_hook quote` | keeps the session and its transcript in the git dir for `work quote`; prints nothing, commits nothing |

`conversation_hook` and `request_hook` are small scripts beside `work` that import only the standard library and their
own modules, so a session starts fast. The names hook's start looks like this:

```console
$ work names --hook
The names of this repository's items and batches: tell the person each by its name beside its id (b3 "Fix the parser"), never by its id alone.
| id | name | status |
|---|---|---|
| b1 | Requests between repositories over GitHub issues | withdrawn |
...
```

What you see from them, and why, is in [Talking with Claude](../talking-with-claude.md#what-you-see-when-a-session-starts).

Next: [Recipes](../recipes.md) for common tasks, [Concepts](../concepts.md) for the words,
[Troubleshooting](../troubleshooting.md) when something refuses.
