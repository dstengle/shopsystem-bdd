<!--
Outputs on this page are from real runs on 2026-11-10: plugin 4.0.0, its scripts as at commit 7f60e57de
(branch plan-docs). Read-only commands ran in this repository. Commands that write ran in two scratch clones of it,
each with a local bare remote as `origin` and the suite's stand-in gh (tests/scripts/stub_gh.py as
$SHOPSYSTEM_WORK_GH), so batches, pull requests and request issues were real runs that touched no GitHub. Long scratch
paths are cut with "...", and long output is cut with "...".
-->

# Command reference

This page is for looking things up. It lists every command of the plugin's six tools, one subsection a command, so
you can find what a command does, what it takes, what it writes and what it prints.

You will rarely type these yourself: Claude runs them as you talk (see [Talking with Claude](../talking-with-claude.md)).
They are here for when you want to look, check or do a step by hand.

> **`--help` is the contract.** Every command prints its own usage and rules with `--help`
> (`work batch done --help`, `model --help`). This page is a friendlier summary. Where the two differ, `--help` is
> right and this page is wrong; please file it.

Commands are written short, `work backlog` for `python3 "$SHOP/scripts/work" backlog`.
[Getting started](../getting-started.md#3-how-commands-are-run) shows how to set that up.

## A first taste

Here is an idea becoming a ready item, in four commands and four commits:

```console
$ work idea "work show prints the status of an item" --note "The person wants to see where an item stands at a glance."
b250 "work show prints the status of an item" idea
$ work shape b250
b250 "work show prints the status of an item" shaped
$ work line b250 --into backlog --group "work show prints an item's status" 'When the person runs `work show` on an item, `work` shall print the status of the item.'
b250 "work show prints the status of an item": backlog#r37
$ work ready b250
b250 "work show prints the status of an item" ready
```

Each command changed one file under `.shop/backlog/` and committed it alone. From there, `work batch start` picks
the item up. The rest of this page goes command by command.

## Things every command shares

- **Exit codes.** `0` success, `1` refused (or a check found something), `2` bad usage. A refusal starts with the
  tool's name, says why, and changes nothing.
- **`--root`.** `work` and `model` take `--root <dir>` before the subcommand (default: the current directory).
  `features generate` and `features vocab` take it after. `features` takes `--dir` for its feature files, `tools`
  takes `--python` for the project's interpreter.
- **Commits.** A `work` command that changes a file commits it, alone, with a message that starts with the command
  (`work shape: b250 ... idea -> shaped`), then pushes the branch to its remote. A refused push prints
  `not pushed: <remote>: <reason>` and keeps the commit.
- **`--json`.** Where a command prints a table or a report, `--json` usually prints one JSON object instead.

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

Moves an item from `idea` to `shaped`: it is understood well enough to be given lines.\
Synopsis: `work shape [--note NOTE] name`

```console
$ work shape b250
b250 "work show prints the status of an item" shaped
```

#### `work line`

Writes a requirement line into an item's `## Requirements`, under the capability it goes into, and commits it.\
Synopsis: `work line [--into INTO] [--group GROUP | --in IN_GROUP] [--retires CAP#rN] [--term TERM] [--recodify CAP] [--relation RELATION] [--given GROUP BLOCK] [--universal UNIVERSAL] [--upstream UPSTREAM] name [text]`

- `--into <capability>`: the codified capability the line goes into.
- `--group "<title>"`: open a new group with this title (default: the item's title). `--in g<n>` joins one of the
  item's groups instead.
- `--retires <cap>#r<n>`: the line replaces a live requirement, whose id goes to `retired:`. Ids are never reused.
- `--term "<bullet>"`: a glossary term for the capability's `## Terms`, in place of a line.
- `--relation`, `--given`, `--universal`, `--upstream`: the other spec pieces an item can carry: a relation row, a
  group's given block, a universal condition, an upstream entry.
- `--recodify <cap>`: switch a capability's block to the current language (`codified-2`).

The line gets the next free id of its capability (`backlog#r37`). It goes into `spec/` only when a batch starts.
`work line` does not parse the line; [`work ready`](#work-ready) does.

```console
$ work line b250 --into backlog --group "work show prints an item's status" 'When the person runs `work show` on an item, `work` shall print the status of the item.'
b250 "work show prints the status of an item": backlog#r37
```

How to write a good line is in [Writing requirements](../writing-requirements.md); the file format is in
[the capability file](capability-file.md).

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

Moves a `shaped` item to `ready` when it passes the readiness bar, and otherwise names every reason it does not.\
Synopsis: `work ready name`

The bar lays the item's lines over a temporary copy of `spec/` and checks that they parse, that `model logic` finds
no clash naming them, and that `features generate` writes their scenarios. A line from a request must be settled.
Readying is the decision to build: a ready item goes into the next batch.

```console
$ work ready b250
b250 "work show prints the status of an item" ready
$ work ready b253
work: work ready: b253 "work names prints every item" is not passing:
  backlog#r39: does not parse at item (token 3 of 15); parsed up to: When an; nearest words: item, items, term, stem, cite
```

What each reason means is in [Troubleshooting](../troubleshooting.md).

#### `work refuse`

Moves an item that is `idea` or `shaped` to `refused`, with the reason.\
Synopsis: `work refuse name reason`

```console
$ work refuse b251 "work show prints the dependencies already"
b251 "work show prints an item's dependencies" refused
```

#### `work withdraw`

Moves an item to `withdrawn`: nobody wants it any more.\
Synopsis: `work withdraw name`

```console
$ work withdraw b252
b252 "A colour theme for work backlog" withdrawn
```

#### `work answer`

Answers the question of an item that is `needs-input` (parked mid-batch), and moves it back to `shaped`.\
Synopsis: `work answer name answer`

```console
$ work answer b253 "Yes, every item, whatever its status."
b253 "work names prints every item" shaped
```

#### `work backlog`

Prints every item, one table a state, in rank order, with what each waits on. Writes nothing.\
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

Prints where an item, a request or a quote stands. With no target it prints what `work list` prints.\
Synopsis: `work show [--json] [target]`, where the target is `b<n>`, `q<n>` or `quote-<n>`.

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

### backlog

#### [g37] work show prints an item's status
- [r37] When the person runs `work show` on an item, `work` shall print the status of the item.
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
`[batch] batch_size` in `.shop/delivery.toml`.

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
t1 b250 "work show prints the status of an item": running in .shop/worktrees/batch-34-t1 on batch-34-b250: build backlog#r37; then work batch done batch-34 t1, or work batch park batch-34 b250 --question <text>
```

#### `work batch done`

Sets a running task done, once its worktree is clean, its commits cite the item (`Item: b<n>`), its ids have left
`unbuilt:` and the tests pass.\
Synopsis: `work batch done batch task`

The tests are `[batch] tests` of `.shop/delivery.toml` (default `python3 -m pytest -q -p work_items`), run in the
task's worktree. A refusal names what is missing:

```console
$ work batch done batch-34 t1
work: work batch done: t1 b250 "work show prints the status of an item": the tests `python3 -m pytest -q -p work_items` failed in .shop/worktrees/batch-34-t1 (exit 1):
...
$ work batch done batch-34 t1
batch-34 t1 b250 "work show prints the status of an item": done
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

### Requests

A request is one bounded context asking another (its upstream, or itself) for behaviour, carried on a GitHub issue.
Each step below commits the request file `.shop/requests/q<n>.md`, then posts the step on the issue and commits its
URL. The examples follow one request, `q48`, that this repository raised to itself.

#### `work request`

Asks an upstream (or this context): writes the request, opens its issue, and commits both.\
Synopsis: `work request --from ASKER [--ask ASK] [--to TO] [--source SOURCE] [--thread THREAD] [--raised-for RAISED_FOR] title`

- `--from`: the asker, a bounded context or product id.
- `--ask`: what the asker needs, in its own words (default: the title).
- `--to`: the upstream, one of `spec/index.md`'s `## Upstreams` (default: the one upstream, or this context).
- `--source`: the origin of a request this context asks itself; `--thread` or `--raised-for` for one another
  context asks.

```console
$ work request "Show an item's status in work show" --from bounded-context/missingmass.io/shopsystem/shopsystem-bdd --source observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-probe-repositories-again --ask "When I run work show on an item, I want to see its status."
q48 https://github.com/ex/ctx/issues/1
```

#### `work offer`

The upstream's offer: the capabilities that may serve the request, quoted whole under `## Offer` with the glossary,
so the asker can write lines in the upstream's words.\
Synopsis: `work offer [--capability CAPABILITY] [--note NOTE] request`

```console
$ work offer q48 --capability backlog --note "work show prints an item's title and rating today; the backlog capability would hold the status too."
```

#### `work fits`

The asker's answer to an offer when existing behaviour already serves it: the request is `delivered` and its issue
closed.\
Synopsis: `work fits [--serves SERVES] request`

```console
$ work fits q49 --serves backlog#r15
$ work show q49
q49 delivered asker
it is the asker's turn, on https://github.com/ex/ctx/issues/2
  resolution line 1: backlog#r15
```

#### `work propose`

The asker's lines, one `--line` each, in the upstream's words.\
Synopsis: `work propose [--line LINES] request`

```console
$ work propose q48 --line 'When the person runs `work show` on an item, `work` shall print the status of the item.'
```

#### `work turn`

Passes a request's turn to the other side, and posts it.\
Synopsis: `work turn request`

```console
$ work turn q48
```

#### `work ask`

The upstream's question on one line of a request.\
Synopsis: `work ask request line question`

```console
$ work ask q48 1 "Should the status be the item's state, such as ready?"
```

#### `work reply`

The asker's answer to a question of a request.\
Synopsis: `work reply request question answer`

```console
$ work reply q48 1 "Yes: the state the backlog shows it under."
$ work show q48
q48 awaiting-upstream upstream
it is the upstream's turn, on https://github.com/ex/ctx/issues/1
  line 1: unsettled - When the person runs `work show` on an item, `work` shall print the status of the item.
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
$ work resolve q48 --line 1 backlog#r37 4.1.0
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

#### `work decision`

Writes a design-decision, `spec/decisions/<nnnn>-<slug>.md`, rewrites `spec/decisions/index.md`, and commits both.\
Synopsis: `work decision [--summary SUMMARY] [--tier {check,requirement,judgement}] [--decision DECISION] [--context CONTEXT] [--alternatives ALTERNATIVES] [--enforced-by ENFORCED_BY] [--verified-by {scenario,check,judgement,monitor}] [--rests-on RESTS_ON] [--source SOURCE] [--by BY] [--slug SLUG] [--date DATE] title`

- `--summary`, `--tier`, `--decision`: required; it is refused, naming each one missing.
- `--context`, `--alternatives`: the other sections. These three take text, or `@<file>`.
- `--enforced-by`: a test (`check` tier) or a requirement (`requirement` tier); repeatable.
- `--rests-on`, `--verified-by`: for a decision that routes a universal condition.

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
- `--about <id>`: the node it is about (default: the bounded context).

```console
$ work record "Command reference layout" --kind analysis --summary "Why the command reference has one section a tool" --body body.md
.shop/records/2026-11-10-command-reference-layout.md
```

## model: the spec, checked

`model` reads `spec/` and `.shop/`, checks them, and parses lines. Only `decisions`, `rules --write` and
`constructs --write` write files, and none of them commits.

### `model parse`

Parses a line in the context's grammar and prints its tree, or its refusal with a hint.\
Synopsis: `model parse [--file FILE] [--form] [line]`

- `--form`: print the line's meaning (its logical form) instead of its tree. Read this one.
- `--file`: parse every line of a file, numbered.

```console
$ model parse --form 'When the person runs `work show` on an item, `work` shall print the status of the item.'
shall [x1: agent the person (constant), x2: command `work show` (parameter), x4: tool `work` (constant)]
  when [x3: item]
    run(e1, subject: x1, object: x2, on: x3)
  response [x5: status]
    status(x3) = x5
    print(e2, subject: x4, object: x5)
$ model parse 'When an item is readied, `work` shall print the status of the item.'
does not parse at item (token 3 of 15)
  parsed up to: When an
  nearest words: item, items, term, stem, cite
  may follow: (none)
```

How to read a refusal is in [Writing requirements](../writing-requirements.md).

### `model lexicon`

Lists the context's words by category: actors, kinds, attributes, events, conditions.\
Synopsis: `model lexicon [--check]`

- `--check`: report problems with the terms (`v_t4` to `v_t15`), and exit 1 when there is any.

```console
$ model lexicon
actor (39)
  the person
  `work run`
  `work`
...
event (95)
  run  [pack cli]
  print  [pack cli]
...
```

### `model explain`

Prints a requirement, what it also means because of other requirements, and what takes precedence over it.\
Synopsis: `model explain requirement`

```console
$ model explain backlog#r24
backlog#r24  While an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
which also means:
  `work` shall exit with an error (by the definition of refuse in the pack cli)
  `work` shall change nothing (by U12)
  `work` shall exit with an error (by U12)
```

### `model check`

Solves the facts of the repository against the design model's rules and prints every violation (`v_...`), then
warnings (`w_...`), unresolved references and file problems. Exits 1 on any violation.\
Synopsis: `model check [--json] [--limit LIMIT]`

- `--limit`: rows shown for each rule (the rest are counted).

```console
$ model check
warning w_example  a requirement holds example data: a code or quoted string that names no declared constant  (41)
    capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools#r37, .venv/bin/python
...
0 violations, 57 warnings, 0 unresolved references, 0 file problems
```

What each rule guards is in [the design model reference](design-model.md).

### `model logic`

The temporal and entailment check of the codified lines: clashes between requirements (L1 to L8). Give a capability,
or a requirement id for the findings that name it.\
Synopsis: `model logic [--json] [capability]`

```console
$ model logic backlog
no findings
```

### `model rules`

Prints every rule's code and plain label, violations first.\
Synopsis: `model rules [--json] [--write] [--check]`

- `--write`: write the rule catalogue `grammar/rules.md`; `--check` says whether it is current.

```console
$ model rules
v2  a standing edge touches something that is not standing
v3  a request's resolution names something that is not a requirement of the spec
...
```

### `model forms`

Prints every file form a context keeps: its name, its path and the command that writes it (or "by hand").\
Synopsis: `model forms [--json]`

```console
$ model forms
item                      .shop/backlog/b<n>.md                                work idea
item's requirement line   .shop/backlog/b<n>.md ## Requirements                work line
...
capability                spec/capabilities/<name>.md                          plugin item b13 (no command yet)
...
```

### `model decisions`

Writes `spec/decisions/index.md` from the decision files. Not committed.\
Synopsis: `model decisions [--check]`

- `--check`: write nothing; say whether the index is current, then run the tests of each `check`-tier decision and
  print `holds` or `failing` for each.

```console
$ model decisions --check
spec/decisions/index.md is current
holds    spec/decisions/0018-measure-refuses-unknown-shapes.md (design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-refuses-unknown-shapes): ...
...
9 check decisions: 6 hold, 3 failing
```

### `model facts`

Prints the facts `model check` reads, one a line, in clingo's syntax. For debugging a rule.\
Synopsis: `model facts`

```console
$ model facts
node("bounded-context/missingmass.io/shopsystem/shopsystem-bdd", "bounded-context").
...
```

### `model constructs`

Writes or checks the construct catalogue `grammar/constructs.md`, each example parsed first.\
Synopsis: `model constructs [--write] [--check]`

```console
$ model constructs --check
grammar/constructs.md is current
```

### `model restates`

For a repository that came from plugin 0.29: whether every old id is restated by a group, dropped or moved.\
Synopsis: `model restates [--json] [capability]`

```console
$ model restates backlog
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
$ features generate backlog
wrote features/backlog.feature
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
$ features vocab --check features/backlog.feature
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
$ features list --tag r24
features/backlog.feature: `work shape` refuses an item that is not an idea
features/batch-measurement.feature: `measure show` prints the stage rows of a measurement whose stage row has no round trip without a round trip
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

Lists each deprecated scenario, a leftover of plugin 1.x, and what replaces it.\
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
`$SHOPSYSTEM_GF` to a GF you built.\
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

Prints one line a tool, its version or what is missing, then the grammar block. Exits 1 when any is missing.\
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

Runs ruff, vulture and import-linter over the paths given, or the Python files changed since `--base`.\
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

`migrate` takes a repository from an older plugin release to this one. [Upgrading](../upgrading.md) walks through it.

### `migrate status`

Prints the repository's plugin version, the plugin's, and each pending upgrade step.\
Synopsis: `migrate status [--hook]`

- `--hook`: what a session is told at its start; always exits 0. See [Hooks](#hooks).

```console
$ migrate status
the repository's plugin version: 4.0.0
the plugin's version: 4.0.0
```

### `migrate upgrade`

Applies each pending upgrade step in order (for 4.0.0, the `codified-2` marker, the CLI pack import, verbs'
aspects), commits it all, and reports what is left for you to reword, by file and id.\
Synopsis: `migrate upgrade`

```console
$ migrate upgrade
no upgrade step is pending
```

### `migrate run`

Moves a repository from the pre-1.0 layout to the current one, every mechanical change or none. It is for
repositories on the old system only; nothing is committed.\
Synopsis: `migrate run --context CONTEXT`, the context written `<owner>/<product>/<context>`.

## Hooks

The plugin installs four hooks (`hooks/hooks.json`). Each runs at a fixed moment, prints little or nothing, and never
fails a session: any error exits 0 silently.

| when | hook | what it does |
|---|---|---|
| a session starts | `migrate status --hook` | says when the repository's plugin version is behind and `migrate upgrade` is pending; nothing when it is current |
| a session starts | `conversation_hook names` | prints the `work names --hook` table, so the session names items as `b3 "Fix the parser"`, never by id alone |
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
