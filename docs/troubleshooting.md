<!-- Outputs on this page are from real runs on 2026-11-10, plugin 4.0.0 (commit 7f60e57de), in a scratch clone of
this repository with a local bare remote and the suite's stand-in gh (tests/scripts/stub_gh.py). Item and batch
numbers (b250-b257, batch-34) are the clone's. Long paths are cut with `...`. -->

# Troubleshooting and FAQ

This page is for anyone who's just been told "no". It's organised by what you see: find the message, read what it
means, then do what it says. Most refusals come from the plugin protecting something on purpose, and each one
names what to fix.

Here's the most common one. You write a line the way you'd say it:

```refused
When an item is readied, `work` shall commit the item.
```

```text
does not parse at item (token 3 of 12)
  parsed up to: When an
  nearest words: item, items, term, stem, cite
  may follow: (none)
```

The parser read "When an" and stopped. Nothing may follow there, because a When clause starts with *who acts*, and
"an item is readied" doesn't say who. Name the one who acts, and the line parses:

```requirement
When the person runs `work ready` on an item, `work` shall commit the item.
```

That's the pattern for the whole page. Read `parsed up to:` for where it stopped, `nearest words:` for words it
knows that look like yours, and `may follow:` for what it would have taken there.

## A line is refused

You'll meet these from `model parse`, `work line` and `work ready`. They're all the same check. For the rules
behind them, see [writing requirements](writing-requirements.md).

### "does not parse at …"

The line uses a word, or an order of words, the grammar doesn't have. Check `nearest words:`: a typo or a plural
shows up there. If your word is missing from the glossary, `model lexicon` lists every word you have. Add the term
first (see [recipes](recipes.md)), then write the line.

### "the verb run takes as its object …"

```refused
When the person runs an item, `work` shall print the item.
```

```text
refused: the verb run takes as its object command or command or command or command or command or command or a kind of it: agent runs command; agent runs command with option; agent runs command on thing; ...
  parsed up to: When the person runs an
  nearest words: item, items, term, stem, cite
  may follow: command
```

Every verb has frames: who does it, to what, and with which prepositions. The message lists them (the repeated
"command or" is a known wording wart). Here, a person runs a *command*, on a thing. Pick a frame and fill it:

```requirement
When the person runs `work show` on an item, `work` shall print the item.
```

You'll also meet this one when you put a state into the trigger, as in "runs `work show` on a shaped item". The
state goes in a While clause instead:

```requirement
While an item is `shaped`, when the person runs `work show` on the item, `work` shall print the status of the item.
```

### "… has no antecedent"

```refused
When the person runs `work show` on an item, `work` shall print the status of the batch.
```

```text
refused: "the batch" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a batch
```

"The batch" means a batch the line has already mentioned, and this line mentions none. Either introduce it first
("a batch", or a relation that gives one, such as "the batch of the item" when a relation says an item has one
batch), or say "a batch".

### "… reads two ways" (R4)

```refused
While an item does not have a dependency, when the person runs `work backlog`, `work` shall print the item.
```

```text
refused: the While clause says "does not have a dependency", which reads two ways: say "has no dependency" or "a dependency that the item does not have"
```

"Does not have a dependency" could mean "has none at all" or "lacks one particular dependency". The message gives
you both wordings. Pick the one you mean:

```requirement
While an item has no dependency, when the person runs `work backlog`, `work` shall print the item.
```

### "more than one meaning"

```refused
When the person runs `work backlog`, `work` shall print every item that has a dependency and the dependency.
```

```text
refused: more than one meaning: "every item that has a dependency and the dependency" reads 2 ways
```

Does the item have "a dependency and the dependency", or does `work` print "every item … and the dependency"? The
quoted words are where the two readings split. Rephrase so only one reading is left:

```requirement
While an item has a dependency, when the person runs `work backlog`, `work` shall print the item and the dependency.
```

### "the line has no trigger" (R12)

```refused
`work` shall commit an item.
```

```text
refused: the line has no trigger and neither "always" nor "never": it would oblige its response in every state
```

A "shall" with no When or If would have to hold every moment. Say what sets it off:

```requirement
When the person runs `work idea`, `work` shall commit an item.
```

A "shall not" or "only" line with no trigger is fine: forbidding something in every state is what it means.

### "the verb … is an action, and a While clause takes a state"

```refused
While the person runs `work backlog`, `work` shall print an item.
```

```text
refused: the verb run is an action, and a While clause takes a state
```

While is for states (is, has, holds); When and If are for actions (runs, commits). Running is something that
happens, so it goes in When:

```requirement
When the person runs `work backlog`, `work` shall print an item.
```

## `work ready` refuses

`work ready` runs the readiness bar on a copy of `spec/` with the item's lines laid in. It lists every reason at
once, so you can fix them in one go.

### An L1 clash

```console
$ work ready b250
work: work ready: b250 "work show hides the title" is not passing:
  L1 backlog#r15 and #r37 clash: on "the person runs `work show` on an item", r15 obliges and r37 forbids `work` to print
```

Your new line (r37) and a delivered one (r15) can't both hold: one says print, the other says don't. If you mean to
change r15, say so: `work line b250 --into backlog --retires backlog#r15 "<the new line>"` puts r15 under
`retired:` and your line takes its place. If you didn't mean to contradict it, narrow your line with a While.

### A group with no scenario

```console
$ work ready b255
work: work ready: b255 "probe steps 3" is not passing:
  backlog: backlog#r38: refused: no translation of no there
```

The line parses, but `features generate` can't write its scenario, so nothing could test it. The bar names the
line. A group whose lines translate but that no step can say is named as `<capability>#g<n> has no scenario: <why>`.
Reword it with a construct the step grammar has. The simplest fix is usually to split a negated relative clause
("no dependency that another item has") into a While clause of its own.

### An unsettled request line

```console
$ work ready b252
work: work ready: b252 "work show prints the status, asked" is not passing:
  line 1 of request q15 is unanswered, not settled: When the person runs `work show` on an item, `work` shall print the status of the item.
```

The item came in from a request, and the request still has a line with no outcome. Give it one with `work outcome`
(accepted, a counter-proposal, or another outcome), or ask Claude to take in the request. An item doesn't get built
while its asker is still waiting on an answer.

## A batch stops

These come from the commands the batch's driver runs. You'll usually see them in Claude's report, not your
terminal.

### `work batch done`: uncommitted changes

```console
$ work batch done batch-34 t1
work: work batch done: t1 b251 "work show prints the status" has uncommitted changes in .shop/worktrees/batch-34-t1: scripts/backlog_cli.py
```

A task is done only when everything in its worktree is committed. Commit the file or throw the change away.

### `work batch done`: a commit cites no item

```console
$ work batch done batch-34 t1
work: work batch done: t1 b251 "work show prints the status": a commit on batch-34-b251 cites no item (an `Item: b251` line): b5c6deced "work show: print the status"
```

Every commit on a task's branch ends with a last paragraph `Item: b251`, so the history says why it was made. Amend
the commit's message (or reword it during a rebase) to add that line.

### `work batch done`: still in `unbuilt:`

```console
$ work batch done batch-34 t1
work: work batch done: t1 b251 "work show prints the status": still in unbuilt: backlog#r37
```

`work batch start` put the item's ids into the capability's `unbuilt:`, so their scenarios run as expected
failures. The commit that makes a scenario pass takes its id out of `unbuilt:`. Until then, the task isn't built.

### `work batch done`: the tests failed

```console
$ work batch done batch-34 t1
work: work batch done: t1 b251 "work show prints the status": the tests `python3 -m pytest -q -p work_items tests/scenarios/test_backlog.py` failed in .shop/worktrees/batch-34-t1 (exit 1):
...
E       AssertionError: ('`work` prints the status of the item i1', 'b1 "Title of i1"\n  status: idea\n ...')
...
FAILED tests/scenarios/test_backlog.py::test_work_show_prints_the_status - As...
1 failed, 21 passed in 4.80s
```

The last twenty lines of the run come with the refusal. The command is `[batch] tests` of `.shop/delivery.toml`
(default `python3 -m pytest -q -p work_items`). Fix the code, commit, run `done` again.

### `work batch review`: a branch does not merge

```console
$ work batch review batch-34
work: work batch review: t1 b251 "work show prints the status": batch-34-b251 does not merge: CONFLICT (content): Merge conflict in README.md into batch-34
```

Two branches changed the same lines. `review` puts everything back as it was, so nothing is half-merged. Resolve
it on the task's branch (rebase it onto `batch-34`, or change the file so it merges), then run `review` again.

### `work batch review`: a fix cites no finding

```console
$ work batch review batch-34
work: work batch review: batch-34: f1 b251 "work show prints the status" (fix now) has no commit citing it; fix it on batch-34-b251 with Finding: f1, or park b251
```

After a review with "fix now" findings, each fix commit carries `Finding: f1` beside its `Item:` line, and each open
finding needs a commit that cites it. The opposite case is refused too:

```text
work: work batch review: batch-34: 669c007c0 "README: the task edit taken out" on batch-34-b251 cites no open finding (a Finding: f<m> line); the open findings are f1 (b251)
```

`work batch resume batch-34` prints where to fix each finding.

### "not pushed: <remote>: <reason>"

```console
$ work idea "an idea while the remote is away"
not pushed: origin: fatal: '.../gone.git' does not appear to be a git repository
b257 "an idea while the remote is away" idea
```

This one isn't a refusal. The command did its work and committed it; only the push failed, and the reason is git's
own. Fix the remote (network, credentials, a renamed repository) and `git push`. A push that hangs gives up after
`$SHOPSYSTEM_PUSH_TIMEOUT` seconds (default 60).

## A file says `codified-1`

```console
$ features generate
features: spec/capabilities/notes.md says `language: codified-1`: run `migrate upgrade`
$ model check
v_p0  a spec file is not codified (no `language: codified-2`, or a capability in `codified-1`): run `migrate upgrade`  (1)
    spec/capabilities/notes.md
```

Plugin 4.0 reads only `codified-2`. Run `migrate status` to see the pending steps and `migrate upgrade` to apply
them. [Upgrading from 3.x](upgrading.md) walks through the lines it asks you to reword.

## The tools

### `tools probe` says a grammar tool is missing

```console
$ tools probe
...
grammar:
  gf missing: requirements cannot be parsed: `work request` and `model check` refuse
  pgf 1.1
  clingo 5.8.2
  gf-rgl missing: the grammar over GF's RGL cannot be compiled
```

Run `tools install`. It installs GF 3.12 and the resource grammar library under `~/.local/share/shopsystem-bdd/`,
and the pinned `pgf` and `clingo` wheels into your project's interpreter. Off Linux x86_64, build GF yourself and
point `$SHOPSYSTEM_GF` at its `gf`.

### The first parse after a glossary change is slow

The grammar is built from your glossary and capability terms. Change a term and the next parse compiles it again.
In this repository that took 34 seconds, and the parse after it took 0.3 seconds. So write your terms first, then
your lines, and you'll wait once rather than after every word.

## FAQ

**Why can't I edit a line in `spec/`?** Scenarios, commits, reviews and requests cite a line by its id. If the
words under `backlog#r15` changed, every one of those would quietly point at something else. So a changed line
gets a new id and the old id goes under `retired:`: `work line <item> --into <capability> --retires <cap>#r<n>`.

**Why does every line name who acts?** Every scenario needs a When step, and a When step needs someone doing
something: the person, a session, a tool. "When an item is readied" leaves a test with no one to call.

**Why aren't sample values in lines?** A line says what holds for every item, not one. The example data a scenario
runs with goes in the group's given block (`work line <item> --into <capability> --given g<n> "<block>"`).

**Why one review per batch, not per task?** One reviewer reads the whole pull request, so it sees how the tasks fit
together, and every task has already passed its tests at `work batch done`. It's also cheaper: in batch-32 the
review was 0.87 of 8.45 dollars.

**Do I have to use GitHub?** Not for the backlog, the lines, `model` or `features`: those work in any git
repository, with or without a remote. A batch ends in a pull request and a request is an issue, both through `gh`
(or whatever `$SHOPSYSTEM_WORK_GH` names).

**What does the plugin keep outside my repository?** The grammar tools in `~/.local/share/shopsystem-bdd/` (or
`$XDG_DATA_HOME`) and its wheels in your interpreter; compiled grammars and parses in `~/.cache/shopsystem-bdd/`;
and, in your git directory, the hooks' small state (the session `work quote` reads, what `work watch` printed) and
the batch lock. Batch worktrees sit in `.shop/worktrees/`, which is ignored.

**Can two sessions work at once?** Yes, with two limits. Batch commands take a lock, so several `done`s land one
after another. One batch is open at a time:

```console
$ work batch start
work: work batch start: batch-34 is building; one batch is open at a time
```

And `work` commits nothing from a task's branch, so the backlog only moves on the base branch:

```text
work: batch-34-b251 is the branch of task t1 of batch-34; work commits nothing on a task's branch: run it in the base branch's checkout
```

**What does a batch cost, and how do I find out?** Ask Claude "what did that batch cost?", or run `measure batch`
after the merge, then `measure show` on its record:

```console
$ measure show .shop/records/measurements/2026-11-10-batch-32.md
totals
total             | value
------------------+----------------------
wall time         | 18 minutes 41 seconds
session time      | 20 minutes 6 seconds
...
cost              | 8.45
...
```

Cost is in US dollars at the dated price table in `scripts/measure_cost.py`. You can set your own prices under
`[prices]` in `.shop/delivery.toml`.

Next: [writing requirements](writing-requirements.md) for the rules behind these refusals,
[recipes](recipes.md) for the everyday fixes, or the [command reference](reference/commands.md).
