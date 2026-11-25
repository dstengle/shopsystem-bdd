<!-- Outputs on this page are from real runs on 2026-11-10, plugin 0.33.0 (commit 7f60e57de), in a scratch clone of
this repository with no remote and the suite's stand-in gh (tests/scripts/stub_gh.py). Item, batch, decision and
quote numbers (b250-b252, batch-34, batch-35, 0092, quote-24) are the clone's. Long paths are cut with `...`.
"Shape a chore" is from a run on 2026-11-18, plugin 0.37.0, in a scratch clone with no remote (its b350). The first
three recipes and "See what a line means" are from runs on 2026-11-19, plugin 0.38.0, in a scratch clone with no remote
(its b359 and b361 written here as b250 and b252). "One verb for several operations" is from runs on 2026-11-20,
plugin 0.41.0 with b420, in its sketch context tests/scripts/fixtures/docs-checklists. -->

# Recipes

Short answers to "how do I ...?", for the developer at the keyboard and the person talking with Claude. Each recipe
gives the situation in one line, the steps, and what you see. Most of the time you'll say the words in **You say**
and Claude runs the commands; they're here so you know what happens, and so you can run them yourself.

Commands are written as `shop work line`, `shop spec check` and so on. [How the commands are
run](reference/commands.md#how-the-commands-are-run) shows how to run them from the plugin's directory. Every command's full contract is its `--help`; the
[command reference](reference/commands.md) has the short version.

**The recipes:** [a vocabulary word](#add-a-word-to-the-vocabulary) ·
[one verb for several operations](#one-verb-for-several-operations) ·
[a relation, given block, universal or upstream](#add-a-relation-row-a-given-block-a-universal-condition-or-an-upstream) ·
[change a delivered line](#change-a-delivered-line) · [a value already in use](#refuse-a-value-already-in-use) ·
[a new capability](#start-a-new-capability) ·
[a chore](#shape-a-chore) ·
[what a line means](#see-what-a-line-means) ·
[an adapter contract behind its lines](#bring-an-adapter-contract-up-to-its-lines) · [ready and blocked](#find-what-is-ready-and-what-blocks-it) ·
[park and answer](#park-a-question-mid-batch-and-answer-it) · [abandon a batch](#abandon-a-batch) ·
[defects and comparisons](#record-a-defect-and-compare-two-batches) ·
[decisions and records](#write-a-design-decision-or-a-record) · [watch requests](#watch-requests-while-you-work) ·
[keep the person's words](#keep-the-persons-words) · [`.shop/delivery.toml`](#set-batch-knobs-and-prices)

## Add a word to the vocabulary

**When:** a line you want needs a word the spec doesn't have yet.

**You say:** "I'd like to give items labels, short words to group them by."

A new word arrives on an item, beside the lines that use it. A word names an element of the
[domain model](reference/domain-model.md), so the item carries the model line too. Here's the whole thing, start
to finish: an item, an object, a relation that says how labels hang off items, a vocabulary entry naming the object,
and a line that uses them.

<!-- docs: context tests/scripts/fixtures/docs-labels -->
```console
$ shop work idea "Items carry labels" --note "the person wants to group items by a short word"
b250 "Items carry labels" idea
$ shop work shape b250
b250 "Items carry labels" shaped
$ shop work line b250 --into items --model "object label"
b250 "Items carry labels": model lines of tracking
$ shop work line b250 --into items --relation "item: has → label (many)"
b250 "Items carry labels": model lines of tracking
$ shop work line b250 --into items --term="- **label** (noun) → object label. A short word the person gives an item, to group it with others."
b250 "Items carry labels": a vocabulary entry of tracking
$ shop work line b250 --into items --group "An item shown returns its labels" "While an item has a label, when the person shows the item, the backlog service shall return every label of the item."
b250 "Items carry labels": items#r31
```

`--into` names the capability; the model lines and the entry go to its `area:` (here `tracking`), into
`spec/model/tracking.md` and `spec/vocabulary/tracking.md` when a batch lays them. A model line in the
[model's syntax](reference/domain-model.md) joins the element the area already declares: `item: has → label` adds a
relation to `object item`. A vocabulary entry has the form `- **<word>** (<part of speech>) → <element>. <one
sentence>.` Leave off the leading `- ` and `work line` tells you so:

```console
$ shop work line b250 --into items --term "**label** (noun) → object label. A short word."
work line: the vocabulary entry **label** (noun) → object label. A short word. is not `- **<word>** (<part of speech>) → <element>. ...`
```

`shop spec parse` in your checkout doesn't know `label` yet: the word lives on the item until a batch lays it into
`spec/`. The [readiness bar](concepts.md#readiness-bar) is where the line is checked, with the item's model lines and
entries laid in on a copy of `spec/`. Rate the item and ready it:

```console
$ shop work rate b250 --value medium-value --urgency low-urgency --size small
b250 "Items carry labels" shaped
$ shop work ready b250
b250 "Items carry labels" ready
```

The first `shop work ready` after a new word takes longer than the ones after it, because the grammar is rebuilt with
the word in it and the spec's lines are parsed again in it, several at once; after that the parses are kept, and it answers
from them.
The line has a precondition ("While an item has a label") because the items capability holds a group on the same
trigger already ("When the person shows an item"); two groups of one capability with the same condition and trigger
are refused (`v15n`), and the bar says which.

**A verb that names an operation** is how a line says a request. The operation goes into the model, under its
service, with its parameters; the verb names it, with a thin frame of word order only:

```text
service backlog
  operation tag(item, label)  outcomes: done
- **tag** (verb, action) → operation backlog.tag. Forms: tags, tagged. Frame: <actor> tags <item>.
```

`verb, action` is something that happens; `verb, state` is something that holds (it can stand in a While clause).
The frame names the slots by the model's elements (`<item>`), and the parameters need none: a line says them after
the object, "with a label", "with the label `l1`", "without a label". With both laid in, a line reads as you'd hope:

<!-- docs: context tests/scripts/fixtures/docs-labels -->
```text
When the person tags an item with a label, the backlog service shall keep the label.
  ...
  when [x2: item, x3: label]
    request(e1, backlog.tag, subject: x1, object: x2)
    param(e1, label, x3)
  response
    keep(e2, subject: x4, object: x3)
```

Give the verb a subject its frame doesn't take ("the person shall keep the label") and the parse stops at the verb,
with `may follow:` listing the verbs the person can do. See
[troubleshooting](troubleshooting.md#the-verb-run-takes-as-its-object-) for reading these.

**A word a pack already has.** The request pack defines `request`, `service`, `reason`, `response`, `check` and a few
verbs. To give one of them your own meaning, mark your entry `Redefines: request`. Without it, `shop spec lexicon
--check` says `v_t16  <word>  <file>: the pack request defines <word> too; mark the entry Redefines: request`; with it,
`shop spec lexicon` lists the word as `<word>  [redefines request]`.

## One verb for several operations

**When:** the person uses a word again for another operation: "list all my checklists", when "list" already names
the request for the notes of one checklist.

**You say:** "List the checklists, and list a checklist: a checklist is a container of things."

Keep the person's word. Don't coin a verb they never said (`browse`): the word gets a second vocabulary entry, naming
the other operation, with a frame that tells it apart. Listing takes a container: one checklist (the frame's
object), the service's whole collection (the frame's own words, "the checklists"), or a part of one thing that its
fixed words name ("the characters of a note"). You wouldn't list a note, but you could list its characters, and
show its length. Here are the model's operations and the entries, two of `list` and `show` beside the third `list`:

<!-- docs: context tests/scripts/fixtures/docs-checklists -->
```text
service checklists
  operation contents(checklist)  outcomes: returned → every note
  operation list()  outcomes: returned → every checklist
  operation characters(note)  outcomes: returned → every character
  operation length(note)  outcomes: returned → the note
  operation show(note)  outcomes: returned → the note
- **list** (verb, action) → operation checklists.contents. Forms: lists, listed. Frame: <actor> lists <checklist>.
- **list** (verb, action) → operation checklists.list. Forms: lists, listed. Frame: <actor> lists the checklists.
- **list** (verb, action) → operation checklists.characters. Forms: lists, listed. Frame: <actor> lists the characters of <note>.
- **show** (verb, action) → operation checklists.length. Forms: shows, shown. Frame: <actor> shows the length of <note>.
- **show** (verb, action) → operation checklists.show. Forms: shows, shown. Frame: <actor> shows <note>.
```

Each entry names its own operation, so the operation's name says what it does (`contents`, `length`) while every
line keeps the person's verb. A line reads by the frame its words fit, one way each:

<!-- docs: context tests/scripts/fixtures/docs-checklists -->
```console
$ shop spec parse --form "When the person lists a checklist, the checklists service shall return every note in the checklist."
shall [x1: agent the person (constant), x3: service the checklists service (constant)]
  when [x2: checklist]
    request(e1, checklists.contents, subject: x1, object: x2)
  response
    every [x4: note]
      in(x4, x2)
      scope
        return(e2, subject: x3, object: x4)
$ shop spec parse --form "When the person lists the checklists, the checklists service shall return every checklist."
shall [x1: agent the person (constant), x2: service the checklists service (constant)]
  when
    request(e1, checklists.list, subject: x1, the checklists)
  response
    every [x3: checklist]
      scope
        return(e2, subject: x2, object: x3)
$ shop spec parse --form "When the person lists the characters of a note, the checklists service shall return every character of the note."
shall [x1: agent the person (constant), x3: service the checklists service (constant)]
  when [x2: note]
    request(e1, checklists.characters, subject: x1, the characters of: x2)
  response
    every [x4: character]
      of(x4, x2)
      scope
        return(e2, subject: x3, object: x4)
$ shop spec parse --form "When the person shows the length of a note, the checklists service shall return the note."
shall [x1: agent the person (constant), x3: service the checklists service (constant)]
  when [x2: note]
    request(e1, checklists.length, subject: x1, the length of: x2)
  response
    return(e2, subject: x3, object: x2)
```

"The checklists" can't read as the first frame's object either: a request acts on one thing, so a plural, "every"
or a count in a request's object slot is no reading. Said on purpose, it is refused, and a frame no word fits stops
the parse at the verb:

<!-- docs: context tests/scripts/fixtures/docs-checklists -->
```console
$ shop spec parse "When the person lists every checklist, the checklists service shall return every checklist."
refused: a request acts on one thing: "every checklist" is a plural object of list; say one thing, or the collection by its frame's own words
$ shop spec parse "When the person lists a note, the checklists service shall return the note."
refused: the verb list takes as its object checklist or a kind of it: agent lists checklist
  parsed up to: When the person lists a
  nearest words: note, notes, notifies, notified, no
  may follow: (none)
```

Two frames that a line still fits both ways (two entries whose fixed words overlap) are refused naming the words
that read two ways and both frames with their operations; give one of them other fixed words.

## Add a relation row, a given block, a universal condition or an upstream

**When:** a line needs more than words: how two kinds relate, example data for its scenario, a rule true
everywhere, or another context it depends on.

Each has its own `shop work line` option, and each is checked for its shape before it's committed. Say what you want;
Claude picks the option.

```console
$ shop work line b251 --into backlog --given g37 'the label `l1` holds "docs"'
b251 "work backlog shows labels": a given block of backlog#g37
$ shop work line b251 --universal "A session shall not merge a proposed change."
b251 "work backlog shows labels": universal#U17
$ shop work line b251 --upstream "bounded-context/missingmass.io/shopsystem/labels: the labels every context shares, github: missingmass/labels"
b251 "work backlog shows labels": an upstream entry
```

- **`--relation "<object>: <phrase> → <object> (<cardinality>)"`** goes into the model of the capability's area (see
  the recipe above). Both objects must be in the model. `has → K` reads "the K of x", `holds → K` reads "x holds a
  K", and a single preposition (`under → tag`) reads "a note under a tag". A relation that does not read is refused:

  ```console
  $ shop work line b250 --into items --relation "item: has label"
  work line: the relation item: has label is not `<object>: <phrase> → <object> (<cardinality>)`
  ```
- **`--given <group> '<data>'`** puts example data under one of the item's own groups. Sample values belong
  here, never in a line. The data must look like data: `the <words> <name> holds` and a code span or a quoted
  string, or `the <words> <name> holds:` with a block under it. Anything else is refused:

  ```console
  $ shop work line b251 --into backlog --given g38 'the item has a label'
  work line: the given block the item has a label is malformed: the item has a label is not example data (`the <words> <name> holds:` with data under it, or `the <words> <name> holds` and one code span or quoted string)
  ```

- **`--universal "<line>"`** adds a condition to `spec/universal.md`, true in every state. It takes no `--into`.
  The line must parse like any other:

  ```requirement
  A session shall not merge a proposed change.
  ```

- **`--upstream "<id>: <what it gives>, github: <owner>/<name>"`** adds an entry to `spec/index.md`'s
  `## Upstreams`, so you can raise [requests](concepts.md#request) to it. It takes no `--into` either.

`shop work show b251` prints them all under `## Requirements`, each in the block it will land in (`### backlog`,
`### universal`, `### index`).

## Change a delivered line

**When:** a line in `spec/` is wrong, or no longer says what you want.

**You say:** "Declining an item should keep the item too."

A delivered line is never edited in place. The new wording gets a new id, and the old id is retired:

```console
$ shop work idea "Declining an item keeps it" --note "the decline is kept with the item, as every other move is"
b252 "Declining an item keeps it" idea
$ shop work shape b252
b252 "Declining an item keeps it" shaped
$ shop work line b252 --into items --retires items#r19 "While the status of an item is one of \`idea\` or \`shaped\`, when the person declines the item, the backlog service shall set the status of the item to \`refused\` and keep the item."
b252 "Declining an item keeps it": items#r31 retires items#r19
```

The item now holds `retired: [r19]` and the new line as `r31`. When a batch lays it, r19 goes into the capability's
`retired:` and stays there for good. Why so strict? An id is a name other things hold on to: scenarios are tagged
`@r19`, commits and findings cite it, other contexts' requests quote it. If r19 could come back meaning something
else, every one of those would silently point at the wrong line
([decision 0085](../spec/decisions/0085-requirements-retired-never-edited.md)).

Two items each said `r31` on this page. That's fine: `shop work batch start` renumbers each item's ids past the
capability's and the other picked items' when it lays them. `--retires` names a live line, and only that:

```console
$ shop work line b252 --into items --retires items#r1000 "When the person shows an item, the backlog service shall return the title of the item."
work line: items#r1000 is nonexistent: items holds no live requirement r1000
```

A line retired with nothing in its place takes `--no-line` in place of the new line:

```console
$ shop work line b252 --into items --retires items#r19 --no-line
b252 "Declining an item keeps it": retires items#r19
```

The item holds `retired: [r19]` and no new line; when a batch lays it, r19 and its scenario go.

## Refuse a value already in use

**When:** a request must not name a value another thing already has: two notes with one title, say.

**You say:** "Adding a note with a title another note has should be refused."

Say the value as the other thing's, "the title of another note", in the request's parameters. Any parameter that is
the word of an attribute takes it (construct `param-of`):

<!-- docs: context docs/examples/notes-cli -->
```markdown
- [r5] If the person adds a note with the title of another note, then the notes service shall refuse the request and name the title.
```

No example value is needed (a line with one, "with the title `groceries`", is example data, which `shop spec check`
warns of). The scenario `shop features generate` writes gives the other note a made-up title in a Given and the same
title to the request in the When ("Given a note n2", "And the title of the note n2 is `t1`", "When the person adds a note n1
with the title `t1`"), so the test sets the service's state up and checks its answer, reading no list of notes. And
`shop spec logic` reads the line beside one that names a code on the same request ("If the person adds a note with the
title `t1`, then the notes service shall not refuse the request.") as one request, and finds the clash. See
[the language reference](../grammar/language.md#with-the-t-of-another-k-a-value-in-use).

## Start a new capability

**When:** the behaviour you want doesn't belong in any capability you have.

A new capability starts on an item, like its lines. `shop work line --capability` writes it into the item: its name,
its narrator (who the scenarios are told for), its group (`service`, the default, or `guarantees` with `--group`)
and its purpose, one line. It refuses a name `spec/capabilities/` holds already.

```console
$ shop work line b260 --capability labels --narrator "a person grouping items" "The person gives items short words, labels, to group them, and reads the backlog by them."
b260 "Give items labels": a new capability labels
```

The item now holds the capability's block:

```markdown
### labels

narrator: a person grouping items
group: service
purpose: The person gives items short words, labels, to group them, and reads the backlog by them.
```

Then add its model lines, vocabulary entries and lines through the same item with `shop work line b260 --into labels`,
as in the first recipe; they take the ids `g1` and `r1` on. `shop work ready` checks them with the capability laid over
a copy of `spec/`. When the batch starts, `shop work batch start` writes `spec/capabilities/labels.md` (its id your
context's with `capability/` in front and the name at the end, its title, narrator and group, its `area:` and `specifies:`, `language: codified-2`,
`## Purpose`, `## Behaviour`, the item's lines with their ids in `unbuilt:`), its name in its area's row of the
`| area | kind | capabilities |` table under `spec/index.md`'s `## Composition`, and its feature:

<!-- docs: context tests/scripts/fixtures/docs-labels -->
```gherkin
Feature: Labels
  Narrator: a person grouping items

  @g1 @r1
  Scenario: An item shown returns its labels
    Given an item i1
    And a label l1
    And the item i1 has the label l1
    And a label l2
    And the item i1 has the label l2
    And a label l3
    And the item i1 does not have the label l3
    When the person shows the item i1
    Then the backlog service returns the label l1
    And the backlog service returns the label l2
    And the backlog service does not return the label l3
```

The [capability file reference](reference/capability-file.md) walks through every section.

## Shape a chore

**When:** the work changes no behaviour a scenario could check: a page of the docs, a skill's text, a refactor.

**You say:** "That's a chore: the shaping skill should name `shop work chore`."

An item with no requirement line holds a chore in their place: the files its work changes and a command whose exit
code 0 shows it done. `shop work chore` writes it as the item's `## Chore` and commits the item; run again, it replaces
it.

```console
$ shop work chore b350 --file skills/shaping-items/SKILL.md --check "grep -q 'work chore' skills/shaping-items/SKILL.md"
b350 "The shaping skill names work chore": the chore of b350 "The shaping skill names work chore" (check: `grep -q 'work chore' skills/shaping-items/SKILL.md`)
$ shop work ready b350
b350 "The shaping skill names work chore" ready
```

The item now holds:

```markdown
## Chore

Files:
- skills/shaping-items/SKILL.md

Check: `grep -q 'work chore' skills/shaping-items/SKILL.md`
```

A chore and requirement lines exclude each other, so `shop work line` on the item is refused, naming the chore. A path
under `spec/`, `features/` or `.shop/` is refused too: lines own the first two and `shop work` the third. In a batch,
`shop work batch done` runs the check in the task's worktree after the tests, and refuses the task while it exits
non-zero or while a commit of the task touches a file the chore does not name.

## See what a line means

**When:** you're reading a line and want everything it commits a service to, including what comes from elsewhere.

`shop spec explain` takes a requirement's id and prints the line, then what it also means by the packs' definitions
and the universal conditions:

```console
$ shop spec explain items#r15
items#r15  While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
which also means:
  the backlog service shall change nothing (by U17)
  the backlog service shall name a reason (by U17)
```

A line with nothing more to it prints only itself. For the logical form of a line that isn't in `spec/` yet, use
`shop spec parse --form "<line>"` (see [writing requirements](writing-requirements.md)).

## Bring an adapter contract up to its lines

**When:** `shop spec check` names `v_a5` or `v_a6`: an operation of `spec/adapters/cli.toml` misses a line that governs
it, or still lists one that was retired or no longer requests it.

Each operation's `requirements` are generated from the spec. Write them again and look at what changed:

```console
$ shop spec annotate --check
spec annotate: spec/adapters/cli.toml is stale: its operations do not hold the requirements that govern them; run `spec annotate`
$ shop spec annotate
annotated spec/adapters/cli.toml
```

`shop spec annotate` changes only the `requirements` lists; the commands, options and outcomes are yours, written by
hand. Run it whenever a line that requests an operation is added, reworded or retired, so the contract always
shows the operation's business rules beside its command. [Adapter contracts](reference/adapters.md) has the format.

## Find what is ready and what blocks it

**When:** you want to know what the next batch will pick, and what's holding the rest back.

**You say:** "What's ready?" or "b251 needs b250 first."

```console
$ shop work depend b251 --on b250
b251 "work backlog shows labels" depends on b250 "Items carry labels"
$ shop work backlog
...
## ready (1)

| rank | item | title | provenance | value | urgency | size | score | waiting on |
|---|---|---|---|---|---|---|---|---|
| 1 | b250 | Items carry labels | own | medium-value | low-urgency | small | 3.00 | - |

## shaped (30)
...
| 30 | b251 | work backlog shows labels | own | - | - | - | - | blocked by b250 "Items carry labels" (ready) |
```

Each state is a table, ranked by score (value and urgency over size). **Waiting on** says why an item can't move:
the item it's blocked by, or the question it's waiting for. `shop work batch start` picks `ready` items in rank order
and passes over a blocked one, unless its blocker is picked first. A dependency that closes a loop is refused:

```console
$ shop work depend b250 --on b251
work depend: b250 "Items carry labels" on b251 "work backlog shows labels" closes the cycle b250 "Items carry labels" -> b251 "work backlog shows labels" -> b250 "Items carry labels"
```

`shop work depend b251 --drop b250` takes a dependency off. `shop work backlog --json` prints the same as one JSON
object.

## Park a question mid-batch and answer it

**When:** a batch can't finish an item without a decision only you can make.

The agent running the batch never stops to ask you. It parks the item with its question, and the rest of the batch
carries on:

```console
$ shop work batch park batch-34 b250 --question "Should work show print the labels sorted, or in the order they were given?"
work batch park: t1 b250 "Items carry labels" has uncommitted changes in .shop/worktrees/batch-34-t1: scripts/backlog_view.py; commit them on batch-34-b250 with `Item: b250`, or pass --discard
$ shop work batch park batch-34 b250 --discard --question "Should work show print the labels sorted, or in the order they were given?"
batch-34 b250 "Items carry labels" -> needs-input: Should work show print the labels sorted, or in the order they were given?
```

The item's lines come out of the batch branch, and the question is at the top of `shop work backlog`, under
`## needs-input`. The work so far stays on the task's branch (`batch-34-b250`).

**You say:** "In the order they were given."

```console
$ shop work answer b250 "In the order they were given."
b250 "Items carry labels" shaped
```

The answer is kept on the item, under `## Answers`, for whoever picks it up next. The item is `shaped` again: it
goes through `shop work ready` and into a later batch.

## Abandon a batch

**When:** a batch has gone wrong and you'd rather start again than fix it.

**You say:** "Abandon batch-35."

```console
$ shop work batch abandon batch-35
work batch abandon: t1 b250 "Items carry labels" has uncommitted changes in .shop/worktrees/batch-35-t1: scripts/backlog_view.py; commit them on batch-35-b250 with `Item: b250`, or pass --discard
$ shop work batch abandon batch-35 --discard
batch-35 abandoned
```

Abandoning closes the batch's pull request, sets its in-batch items `ready` again, and removes its worktrees. Work
that isn't committed is in the way, so `abandon` refuses until you commit it or say `--discard`. Committed work is
kept on the items' branches.

## Record a defect and compare two batches

**When:** a fault turns up after a batch merged, or you want to know whether a change to the workflow helped.

**You say:** "That's a bug in what b197 delivered: ..."

```console
$ shop measure defect b197 --says "features generate writes no scenario for a line that says every K under a While clause. Reproduce: such a line, features generate: no scenario for its group."
.shop/batches/32/defect-1.md
```

(The fault above is made up for this page.) The defect goes against the delivered item and the batch that merged it,
and is committed alone. `shop measure batch` counts it, as defects per item. It only takes a delivered item of a merged
batch:

```console
$ shop measure defect b250 --says "x"
measure defect: b250 "Items carry labels" is ready in batch-35, which is abandoned; a defect is of a delivered item of a merged batch
```

**You say:** "How did batch-32 compare with batch-31?"

```console
$ shop measure compare batch-31 batch-32
total              | batch-31                   | batch-32              | ratio
-------------------+----------------------------+-----------------------+------
wall time          | 21 minutes 6 seconds       | 18 minutes 41 seconds | 0.89
session time       | 1 hour 5 minutes 5 seconds | 20 minutes 6 seconds  | 0.31
...
cost               | 13.93                      | 8.45                  | 0.61
defects per item   | 0.00                       | 0.00                  | -
...
items              | 4                          | 1                     | 0.25
changed lines      | 962                        | 796                   | 0.83
```

The ratio is the second over the first, so under 1 means the second batch used less. Each side is a batch's newest
measurement (written by `shop measure batch`). Read the sizes before the costs: batch-32 had a quarter of the items.

## Write a design-decision or a record

**When:** you've settled something worth keeping (a decision), or written up an analysis someone will want later
(a record).

**You say:** "Let's decide labels are free words, no fixed list."

```console
$ shop work decision "Labels are free words" --tier judgement
work decision: a design-decision gives --summary, --decision
$ shop work decision "Labels are free words" --tier judgement --summary "A label is any short word the person chooses; there is no fixed list." --decision "work keeps a label as the person wrote it and checks it against no list." --context "b250 adds labels to items."
spec/decisions/0092-labels-are-free-words.md
```

It's numbered after the highest, `spec/decisions/index.md` is rewritten, and both are committed. The tier says how
the decision is held: `check` (a test enforces it, `--enforced-by`), `requirement` (a line does), or `judgement` (a
reviewer reads for it).

A record is a report kept as a file. Write its body in a file first, then:

```console
$ shop work record "Which items would carry labels" --kind analysis --summary "How many delivered items a label would have grouped" --body labels-body.md
.shop/records/2026-11-10-which-items-would-carry-labels.md
```

Its row goes into `.shop/records/README.md`, committed with it. A committed record is never edited, so the same
title twice is refused (`... exists, and a committed record is never edited: give another --slug`).

## Watch requests while you work

**When:** you've asked another context for something, or one asked you, and you want to know the moment they
answer.

You don't have to remember. When a session starts with a request waiting on the other side, the hook says so:

```text
q14 awaiting-asker: Requests go through one shared tool (https://github.com/ex/ctx/issues/7)
A request waits on the other side: start `work watch --forward` with the Monitor tool, and run `work sync` when it wakes.
```

Claude then starts `shop work watch --forward` with its Monitor tool, so the watch runs beside the conversation. It
wakes on GitHub's events (through `gh webhook forward`) where you administer the repository, and polls GitHub's
notifications where you don't. When a comment arrives, it prints one line and ends:

```console
$ shop work watch --every 1 --polls 2
q14 https://github.com/ex/ctx/issues/7 comment 3: https://github.com/ex/ctx/issues/7#issuecomment-3 (`work sync` records it)
```

(That line is from a plain `shop work watch` against the stand-in gh; `--forward` prints the same.) Then `shop work
sync` records the comment and tells you whose move it is. See [concepts](concepts.md#request) for how a request goes
back and forth.

## Keep the person's words

**When:** the person says something that explains why a piece of work exists, and you want it kept as they said it.

**You say:** "Quote that."

```console
$ shop work quote "I trust you to make some delightful docs."
quote-24 "I trust you to make some delightful docs."
```

The words must be in a message the person sent in this session (the prompt hook remembers which one); otherwise
it's refused: `the person wrote no message with "..." in the session ...; quote their words as they wrote them`.
The quote keeps the message and the turns around it under `.shop/quotes/`, committed, so any clone can show them:

```console
$ shop work show quote-20
quote-20 "Once 4.0 is done, take a new backlog item to make some nice …"
  session: 72e23fa5-6dee-49f3-a1d1-7e79096a0501
  date: 2026-11-10
...
the person, 2026-11-10T04:19:13.250000+00:00, cited:
I'm going offline. Please take care of pull requests and getting to 4.0.

Once 4.0 is done, take a new backlog item to make some nice user documentation for the plugin and then get to work on the backlog item. I trust you to make some delightful docs.
```

## Set batch knobs and prices

**When:** the defaults don't fit your repository: batches too big, a different test command, your own review
checks, or your own prices.

`.shop/delivery.toml` is written by hand, and every key is optional. A file with all of them:

```toml
batch_size = 3

[batch]
tests = "python3 -m pytest -q -p work_items tests/"
push = "env -u GH_TOKEN"
rules = ["Don't chain `cp` and `rm` in one shell command."]

[review]
size = 1500
checks = [
  "python3 {scripts}/features generate --check",
  "python3 {scripts}/spec decisions --check",
]

[prices."claude-opus-5-5"]
input = 4.0
output = 20.0
cache_read = 0.20
```

| key | what it sets | default |
|---|---|---|
| `batch_size` (top level) | how many ready items `shop work batch start` picks | 4 |
| `[batch] tests` | what `shop work batch done` and `review` run | `python3 -m pytest -q -p work_items` |
| `[batch] push` | a prefix the batch's agent puts before every `git push` and `gh` call | none |
| `[batch] worktrees` | where a batch's worktrees go | `.shop/worktrees/` |
| `[batch] rules` | the batch rules of this context's own setup, each written into the batch brief after the plugin's rules, for every agent that runs a batch | none |
| `[review] size` | the changed lines over which the reviewer's brief says "over the limit", and past which `shop work batch start` picks no more items by their estimates | 1000 |
| `[review] checks` | the commands the reviewer's brief runs, with `{scripts}` and `{forked_from}` filled in | `shop tools size --limit 300`, `shop tools check`, `shop features generate --check`, `shop features bindings --unbound`, `shop spec decisions --check` |
| `[prices."<model>"]` | dollars per million tokens: `input`, `output`, `cache_read`, all three | a dated table in `scripts/measure_cost.py` |

`[review] checks` replaces the default list, so copy in the defaults you want to keep. A price is used by
`shop measure batch` for a model the table doesn't know, or over the table's own. A malformed file is refused by the
first command that reads it, naming the key.

Next: the [command reference](reference/commands.md) for every option, [concepts](concepts.md) for the words used
here, or [troubleshooting](troubleshooting.md) when something refuses.
