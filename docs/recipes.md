<!-- Outputs on this page are from real runs on 2026-11-10, plugin 0.33.0 (commit 7f60e57de), in a scratch clone of
this repository with no remote and the suite's stand-in gh (tests/scripts/stub_gh.py). Item, batch, decision and
quote numbers (b250-b252, batch-34, batch-35, 0092, quote-24) are the clone's. Long paths are cut with `...`. -->

# Recipes

Short answers to "how do I ...?", for the developer at the keyboard and the person talking with Claude. Each recipe
gives the situation in one line, the steps, and what you see. Most of the time you'll say the words in **You say**
and Claude runs the commands; they're here so you know what happens, and so you can run them yourself.

Commands are written as `work line`, `model check` and so on. [Getting started](getting-started.md#3-how-commands-are-run)
shows how to run them from the plugin's directory. Every command's full contract is its `--help`; the
[command reference](reference/commands.md) has the short version.

**The recipes:** [a glossary word](#add-a-word-to-the-glossary) ·
[a relation, given block, universal or upstream](#add-a-relation-row-a-given-block-a-universal-condition-or-an-upstream) ·
[change a delivered line](#change-a-delivered-line) · [a new capability](#start-a-new-capability) ·
[what a line means](#see-what-a-line-means) · [ready and blocked](#find-what-is-ready-and-what-blocks-it) ·
[park and answer](#park-a-question-mid-batch-and-answer-it) · [abandon a batch](#abandon-a-batch) ·
[defects and comparisons](#record-a-defect-and-compare-two-batches) ·
[decisions and records](#write-a-design-decision-or-a-record) · [watch requests](#watch-requests-while-you-work) ·
[keep the person's words](#keep-the-persons-words) · [`.shop/delivery.toml`](#set-batch-knobs-and-prices)

## Add a word to the glossary

**When:** a line you want needs a word the spec doesn't have yet.

**You say:** "I'd like to give items labels, short words to group them by."

A new word arrives on an item, beside the lines that use it. Here's the whole thing, start to finish: an item, a
term, a relation row that says how labels hang off items, and a line that uses both.

<!-- docs: context tests/scripts/fixtures/docs-labels -->
```console
$ work idea "Items carry labels" --note "the person wants to group items by a short word"
b250 "Items carry labels" idea
$ work shape b250
b250 "Items carry labels" shaped
$ work line b250 --into backlog --term="- **label** (noun): a short word the person gives an item, to group it with others. Kind of: text."
b250 "Items carry labels": a term of backlog
$ work line b250 --into backlog --relation "| label | of | item | many |"
b250 "Items carry labels": a relation row of backlog
$ work line b250 --into backlog --group "work show prints an item's labels" "When the person runs \`work show\` on an item, \`work\` shall print every label of the item."
b250 "Items carry labels": backlog#r43
```

A term bullet has the form `- **<term>** (<part of speech>): <one sentence>. Kind of: <kind>.` Leave off the
leading `- ` and `work line` tells you so:

```console
$ work line b250 --into backlog --term "**label** (noun): a short word the person gives an item, to group it with others. Kind of: text."
work: work line: the term bullet **label** (noun): a short word ... Kind of: text. is not a term entry `- **<term>** (<part of speech>): <text>`
```

`model parse` in your checkout doesn't know `label` yet: the word lives on the item until a batch lays it into
`spec/`. The [readiness bar](concepts.md#readiness-bar) is where the line is checked, with the item's term laid in on
a copy of `spec/`. Rate the item and ready it:

```console
$ work rate b250 --value medium-value --urgency low-urgency --size small
b250 "Items carry labels" shaped
$ work ready b250
b250 "Items carry labels" ready
```

The first `work ready` after a new word takes a few minutes, because the grammar is rebuilt with the word in it.

**A verb** needs its frames too: who does it, to what, and with which preposition. Copy the shape of the
glossary's own verbs:

```text
- **merge** (verb, action): the person merges a pull request into its base branch on GitHub. Forms: merges, merged. Frame: the person merges pull request.
- **give** (verb, action): a session or a tool gives a text a thing it lacks, such as a grade to a review finding. Forms: gives, given. Frame: agent gives thing to text.
```

`verb, action` is something that happens; `verb, state` is something that holds (it can stand in a While clause).
Each `Frame:` names the subject's kind, the verb, the object's kind and any preposition. With the entry
`- **tag** (verb, action): a tool gives an item a label. Forms: tags, tagged. Frame: tool tags item with label.`
laid in, a line that fills the frame reads as you'd hope:

<!-- docs: context tests/scripts/fixtures/docs-labels -->
```text
When the person runs `work label` on an item, `work` shall tag the item with a label and commit the item.
  ...
  response [x5: label]
    tag(e2, subject: x4, object: x3, with: x5)
    commit(e3, subject: x4, object: x3)
```

Give the verb a subject its frame doesn't take ("the person shall tag ...") and the parse stops at the verb, with
`may follow:` listing the verbs the person can do. See
[troubleshooting](troubleshooting.md#the-verb-run-takes-as-its-object-) for reading these.

**A word a pack already has.** The CLI pack defines `tool`, `command`, `option`, `reason`, `output` and a few
verbs. To give one of them your own meaning, mark your entry `Redefines: cli`. Without it, `model lexicon --check`
says:

```console
$ model lexicon --check
v_t16  option  spec/capabilities/labels.md: the pack cli defines option too; mark the entry Redefines: cli
393 terms, 1 problems
```

With `... Kind of: text. Redefines: cli.` on the entry, it prints `393 terms, 0 problems`, and `model lexicon` lists
the word as `option  [redefines cli]`.

## Add a relation row, a given block, a universal condition or an upstream

**When:** a line needs more than words: how two kinds relate, example data for its scenario, a rule true
everywhere, or another context it depends on.

Each has its own `work line` option, and each is checked for its shape before it's committed. Say what you want;
Claude picks the option.

```console
$ work line b251 --into backlog --given g37 'the label `l1` holds "docs"'
b251 "work backlog shows labels": a given block of backlog#g37
$ work line b251 --universal "A session shall not merge a pull request."
b251 "work backlog shows labels": universal#U17
$ work line b251 --upstream "bounded-context/missingmass.io/shopsystem/labels: the labels every context shares, github: missingmass/labels"
b251 "work backlog shows labels": an upstream entry
```

- **`--relation "| from | word | to | cardinality |"`** goes into the capability's `## Relations` (see the recipe
  above). Both kinds must be in the lexicon. `one` in the last cell means each thing has at most one; leave it empty
  for the prepositions `of`, `for`, `with`, `on` and `in` to mean the same.
- **`--given <group> '<data>'`** puts example data under one of the item's own groups. Sample values belong
  here, never in a line. The data must look like data: `the <words> <name> holds` and a code span or a quoted
  string, or `the <words> <name> holds:` with a block under it. Anything else is refused:

  ```console
  $ work line b251 --into backlog --given g38 'the item has a label'
  work: work line: the given block the item has a label is malformed: the item has a label is not example data (`the <words> <name> holds:` with data under it, or `the <words> <name> holds` and one code span or quoted string)
  ```

- **`--universal "<line>"`** adds a condition to `spec/universal.md`, true in every state. It takes no `--into`.
  The line must parse like any other:

  ```requirement
  A session shall not merge a pull request.
  ```

- **`--upstream "<id>: <what it gives>, github: <owner>/<name>"`** adds an entry to `spec/index.md`'s
  `## Upstreams`, so you can raise [requests](concepts.md#request) to it. It takes no `--into` either.

`work show b251` prints them all under `## Requirements`, each in the block it will land in (`### backlog`,
`### universal`, `### index`).

## Change a delivered line

**When:** a line in `spec/` is wrong, or no longer says what you want.

**You say:** "`work refuse` should commit the item too."

A delivered line is never edited in place. The new wording gets a new id, and the old id is retired:

```console
$ work idea "work refuse commits the item"
b252 "work refuse commits the item" idea
$ work shape b252
b252 "work refuse commits the item" shaped
$ work line b252 --into backlog --retires backlog#r40 "While the status of an item is one of \`idea\` or \`shaped\`, when the person runs \`work refuse\` on the item, \`work\` shall set the status of the item to \`refused\` and commit the item."
b252 "work refuse commits the item": backlog#r43 retires backlog#r40
```

The item now holds `retired: [r40]` and the new line as `r43`. When a batch lays it, r40 goes into the capability's
`retired:` and stays there for good. Why so strict? An id is a name other things hold on to: scenarios are tagged
`@r40`, commits and findings cite it, other contexts' requests quote it. If r40 could come back meaning something
else, every one of those would silently point at the wrong line
([decision 0085](../spec/decisions/0085-requirements-retired-never-edited.md)).

Three items each said `r43` on this page. That's fine: `work batch start` renumbers each item's ids past the
capability's and the other picked items' when it lays them. `--retires` names a live line, and only that:

```console
$ work line b252 --into backlog --retires backlog#r1 "When the person runs \`work show\` on an item, \`work\` shall print the title of the item."
work: work line: backlog#r1 is nonexistent: backlog holds no live requirement r1
```

## Start a new capability

**When:** the behaviour you want doesn't belong in any capability you have.

There's no command for this yet (`model forms` says `plugin item b13 (no command yet)`), so you write the file by
hand: `spec/capabilities/<name>.md`, with frontmatter, a purpose, and empty sections.

```markdown
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/labels
title: Labels
narrator: a person grouping items
group: service
language: codified-2
retired: []
unbuilt: []
---

# Labels

## Purpose
The person gives items short words, labels, to group them, and reads the backlog by them.

## Terms

## Behaviour
```

The `id` is your context's id (the `id:` of `spec/index.md`) with `capability/` in front and the file's name at the
end. `narrator` is who the scenarios are told for, and `group` is its kind of capability (`service` or `guarantees`),
as the tables of `spec/index.md`'s `## Composition` list them. Run `model check`: an empty capability passes with `0 violations`. Commit it, then add terms and lines
through items with `work line <item> --into labels`, as in the first recipe.

Once a group is laid, `model check` wants its scenario (`v_s3  a group has no scenario`) until `features generate`
writes it:

```console
$ features generate labels
wrote features/labels.feature
```

<!-- docs: context tests/scripts/fixtures/docs-labels -->
```gherkin
Feature: Labels
  Narrator: a person grouping items

  @g1 @r1
  Scenario: `work show` prints the labels of an item
    Given an item i1
    And a label l1
    And the item i1 has the label l1
    And a label l2
    And the item i1 has the label l2
    When the person runs `work show` on the item i1
    Then `work` prints the label l1
    And `work` prints the label l2
```

The [capability file reference](reference/capability-file.md) walks through every section.

## See what a line means

**When:** you're reading a line and want everything it commits `work` to, including what comes from elsewhere.

`model explain` takes a requirement's id and prints the line, then what it also means by the packs' definitions
and the universal conditions:

```console
$ model explain backlog#r38
backlog#r38  While the status of an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
which also means:
  `work` shall exit with an error (by the definition of refuse in the pack cli)
  `work` shall change nothing (by U12)
  `work` shall exit with an error (by U12)
```

A line with nothing more to it prints only itself. For the logical form of a line that isn't in `spec/` yet, use
`model parse --form "<line>"` (see [writing requirements](writing-requirements.md)).

## Find what is ready and what blocks it

**When:** you want to know what the next batch will pick, and what's holding the rest back.

**You say:** "What's ready?" or "b251 needs b250 first."

```console
$ work depend b251 --on b250
b251 "work backlog shows labels" depends on b250 "Items carry labels"
$ work backlog
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
the item it's blocked by, or the question it's waiting for. `work batch start` picks `ready` items in rank order
and passes over a blocked one, unless its blocker is picked first. A dependency that closes a loop is refused:

```console
$ work depend b250 --on b251
work: work depend: b250 "Items carry labels" on b251 "work backlog shows labels" closes the cycle b250 "Items carry labels" -> b251 "work backlog shows labels" -> b250 "Items carry labels"
```

`work depend b251 --drop b250` takes a dependency off. `work backlog --json` prints the same as one JSON object.

## Park a question mid-batch and answer it

**When:** a batch can't finish an item without a decision only you can make.

The agent running the batch never stops to ask you. It parks the item with its question, and the rest of the batch
carries on:

```console
$ work batch park batch-34 b250 --question "Should work show print the labels sorted, or in the order they were given?"
work: work batch park: t1 b250 "Items carry labels" has uncommitted changes in .shop/worktrees/batch-34-t1: scripts/backlog_view.py; commit them on batch-34-b250 with `Item: b250`, or pass --discard
$ work batch park batch-34 b250 --discard --question "Should work show print the labels sorted, or in the order they were given?"
batch-34 b250 "Items carry labels" -> needs-input: Should work show print the labels sorted, or in the order they were given?
```

The item's lines come out of the batch branch, and the question is at the top of `work backlog`, under
`## needs-input`. The work so far stays on the task's branch (`batch-34-b250`).

**You say:** "In the order they were given."

```console
$ work answer b250 "In the order they were given."
b250 "Items carry labels" shaped
```

The answer is kept on the item, under `## Answers`, for whoever picks it up next. The item is `shaped` again: it
goes through `work ready` and into a later batch.

## Abandon a batch

**When:** a batch has gone wrong and you'd rather start again than fix it.

**You say:** "Abandon batch-35."

```console
$ work batch abandon batch-35
work: work batch abandon: t1 b250 "Items carry labels" has uncommitted changes in .shop/worktrees/batch-35-t1: scripts/backlog_view.py; commit them on batch-35-b250 with `Item: b250`, or pass --discard
$ work batch abandon batch-35 --discard
batch-35 abandoned
```

Abandoning closes the batch's pull request, sets its in-batch items `ready` again, and removes its worktrees. Work
that isn't committed is in the way, so `abandon` refuses until you commit it or say `--discard`. Committed work is
kept on the items' branches.

## Record a defect and compare two batches

**When:** a fault turns up after a batch merged, or you want to know whether a change to the workflow helped.

**You say:** "That's a bug in what b197 delivered: ..."

```console
$ measure defect b197 --says "features generate writes no scenario for a line that says every K under a While clause. Reproduce: such a line, features generate: no scenario for its group."
.shop/batches/32/defect-1.md
```

(The fault above is made up for this page.) The defect goes against the delivered item and the batch that merged it,
and is committed alone. `measure batch` counts it, as defects per item. It only takes a delivered item of a merged
batch:

```console
$ measure defect b250 --says "x"
measure defect: b250 "Items carry labels" is ready in batch-35, which is abandoned; a defect is of a delivered item of a merged batch
```

**You say:** "How did batch-32 compare with batch-31?"

```console
$ measure compare batch-31 batch-32
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
measurement (written by `measure batch`). Read the sizes before the costs: batch-32 had a quarter of the items.

## Write a design-decision or a record

**When:** you've settled something worth keeping (a decision), or written up an analysis someone will want later
(a record).

**You say:** "Let's decide labels are free words, no fixed list."

```console
$ work decision "Labels are free words" --tier judgement
work decision: a design-decision gives --summary, --decision
$ work decision "Labels are free words" --tier judgement --summary "A label is any short word the person chooses; there is no fixed list." --decision "work keeps a label as the person wrote it and checks it against no list." --context "b250 adds labels to items."
spec/decisions/0092-labels-are-free-words.md
```

It's numbered after the highest, `spec/decisions/index.md` is rewritten, and both are committed. The tier says how
the decision is held: `check` (a test enforces it, `--enforced-by`), `requirement` (a line does), or `judgement` (a
reviewer reads for it).

A record is a report kept as a file. Write its body in a file first, then:

```console
$ work record "Which items would carry labels" --kind analysis --summary "How many delivered items a label would have grouped" --body labels-body.md
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

Claude then starts `work watch --forward` with its Monitor tool, so the watch runs beside the conversation. It
wakes on GitHub's events (through `gh webhook forward`) where you administer the repository, and polls GitHub's
notifications where you don't. When a comment arrives, it prints one line and ends:

```console
$ work watch --every 1 --polls 2
q14 https://github.com/ex/ctx/issues/7 comment 3: https://github.com/ex/ctx/issues/7#issuecomment-3 (`work sync` records it)
```

(That line is from a plain `work watch` against the stand-in gh; `--forward` prints the same.) Then `work sync`
records the comment and tells you whose move it is. See [concepts](concepts.md#request) for how a request goes
back and forth.

## Keep the person's words

**When:** the person says something that explains why a piece of work exists, and you want it kept as they said it.

**You say:** "Quote that."

```console
$ work quote "I trust you to make some delightful docs."
quote-24 "I trust you to make some delightful docs."
```

The words must be in a message the person sent in this session (the prompt hook remembers which one); otherwise
it's refused: `the person wrote no message with "..." in the session ...; quote their words as they wrote them`.
The quote keeps the message and the turns around it under `.shop/quotes/`, committed, so any clone can show them:

```console
$ work show quote-20
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

[review]
size = 1500
checks = [
  "python3 {scripts}/features generate --check",
  "python3 {scripts}/model decisions --check",
]

[prices."claude-opus-5-5"]
input = 4.0
output = 20.0
cache_read = 0.20
```

| key | what it sets | default |
|---|---|---|
| `batch_size` (top level) | how many ready items `work batch start` picks | 4 |
| `[batch] tests` | what `work batch done` and `review` run | `python3 -m pytest -q -p work_items` |
| `[batch] push` | a prefix the batch's agent puts before every `git push` and `gh` call | none |
| `[batch] worktrees` | where a batch's worktrees go | `.shop/worktrees/` |
| `[review] size` | the changed lines over which the reviewer's brief says "over the limit" | 1000 |
| `[review] checks` | the commands the reviewer's brief runs, with `{scripts}` and `{forked_from}` filled in | `tools size --limit 300`, `tools check`, `features generate --check`, `features bindings --unbound`, `model decisions --check` |
| `[prices."<model>"]` | dollars per million tokens: `input`, `output`, `cache_read`, all three | a dated table in `scripts/measure_cost.py` |

`[review] checks` replaces the default list, so copy in the defaults you want to keep. A price is used by
`measure batch` for a model the table doesn't know, or over the table's own. A malformed file is refused by the
first command that reads it, naming the key.

Next: the [command reference](reference/commands.md) for every option, [concepts](concepts.md) for the words used
here, or [troubleshooting](troubleshooting.md) when something refuses.
