<!-- Outputs on this page are from real runs on 2026-11-10, plugin 0.33.0 (commit 7f60e57de): a 0.32.1 repository
built from the 0.33.0 upgrade's test fixture (tests/scripts/test_migrate_upgrade_cnl4.py), upgraded and reworded. -->

# Upgrading

This page takes a repository from an older plugin release to this one. Read [Versions](#versions) first if your
`.shop/plugin-version` says a number from 1.0.0 to 4.1.0.

## Versions

The plugin's versions are 0.y.z until 1.0 (design-decision 0092, "Versions are 0.y.z until 1.0"):

- **y** goes up for a large or incompatible change: one that needs `migrate upgrade`, or rewording lines, or that
  removes a command, or changes the scenarios `features generate` writes so that a repository's handlers must
  change. It counts past .9 to .10 (0.9, 0.10, 0.11).
- **z** goes up for a non-breaking update: a fix, or something new that changes nothing that works.
- **1.0.0** is a decision of its own, taken when the plugin is ready for it, not the next step of y.

A release bumps `version` in `.claude-plugin/plugin.json` by that rule, and its section in the
[changelog](../CHANGELOG.md) is headed with the new number.

The releases made as 1.0.0 to 4.1.0 were renumbered into this series in 0.34.1, continuing the releases 0.1 to 0.29:

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

`migrate` reads only the new numbers. A repository whose `.shop/plugin-version` holds an old one reads as above
the plugin, and the session is told to update the plugin. Rewrite the file by hand with the table: a repository on
3.0.1 writes `0.32.1`, one on 4.1.0 writes `0.34.0`. Commit it, then reinstall the plugin once: Claude Code keeps
installs by version and may not move from 4.1.0 down to 0.34.1. `migrate status` then lists what is pending, if
anything.

## From 0.32 to 0.33

This page's walk-through is for the maintainer of a repository on plugin 0.32. It takes you from `migrate status` to a green suite
on 0.33, one step at a time. Most of the work is rewording lines, and Claude can do that with you.

Here is the whole job in one picture. `migrate upgrade` changes what is mechanical and names, by file and id, every
line you have to reword:

```console
$ migrate upgrade
upgraded to 0.33.0: the controlled language 4
...
the controlled language 4: spec/capabilities/buy.md r4 says a negated indefinite in a While clause: refused: the While clause says "does not own a cart", which reads two ways: say "owns no cart" or "a cart that the shopper does not own"
...
```

You then write a new line under a new id, and the old id is retired:

<!-- docs: context tests/scripts/fixtures/docs-shop -->
```refused
While a shopper does not own a cart, when the shopper picks a cart, the shopper shall watch a till.
```

becomes r9:

<!-- docs: context tests/scripts/fixtures/docs-shop -->
```requirement
While a shopper owns no cart, when the shopper picks a cart, the shopper shall watch a till.
```

(These lines use the fixture's glossary, a toy shop with shoppers, carts and tills, so they are read there, not in
this repository.)

## What changed in 0.33

The full note is [0.33.0 in the changelog](../CHANGELOG.md#0330-released-as-400-the-controlled-language-4). What it means for you:

- **One grammar.** Lines are read by grammar 4, built from your glossary. A line has one meaning or is refused.
- **A new marker.** Spec files say `language: codified-2`. Every tool refuses a `codified-1` file and names
  `migrate upgrade`.
- **Verbs say their aspect.** `(verb, action)` goes in a trigger or a response; `(verb, state)` in a While clause.
- **Packs of words.** `spec/index.md` imports `cli`, `time` or `spec`. A word of yours that a pack also has carries
  `Redefines: <pack>`.
- **No adjectives.** A coined condition like "full" is gone. Say the state with a structure, such as an attribute
  and its value.
- **Reading rules.** "the", "no", "every" and "only" mean one thing each. "The till" needs a till said before it.
- **Example data moves out.** A sample value in a line goes into its group's given block.
- **New constructs.** Counts, "two", "another", "is one of", "has no", a command's options in the trigger, time.
- **New checks.** `model parse --form` shows a line's meaning, `model explain` what other lines force with it, and
  `model logic` gains L8: a Then that other lines already say.
- **Known limits.** Some things the language cannot say yet. They're listed in
  [the language reference](../grammar/language.md).

## Before you start

Start from a clean checkout of your default branch, with no batch building. `migrate upgrade` commits, and a batch
started on 0.32 lays lines in the old language.

## Step 1: update the plugin and the grammar tools

```console
$ claude plugin update shopsystem-bdd@shopsystem-bdd
$ tools install
$ tools probe
...
grammar:
  gf 3.12.0 (/home/vscode/.local/share/shopsystem-bdd/gf-3.12/bin/gf)
  pgf 1.1
  clingo 5.8.2
  gf-rgl 20250812 (/home/vscode/.local/share/shopsystem-bdd/gf-rgl-20250812)
```

Run `tools install` again even if 0.32 had it working. Grammar 4 is built on GF's resource grammar library, the
`gf-rgl` line, which 0.32 never installed. Grammar 4 is compiled against it.

Then ask what is pending:

```console
$ migrate status
the repository's plugin version: 0.32.1
the plugin's version: 0.33.0
pending upgrade step 0.33.0 "the controlled language 4": write each file's marker codified-2, import the CLI pack and give each verb its aspect where its lines decide it, and name by file and id each line that no longer parses and what else a session rewords
```

A new session tells Claude the same thing, and Claude offers you the upgrade. It runs it only when you say yes.

## Step 2: run `migrate upgrade`

`migrate upgrade` applies every pending step and commits it all as one commit. It rewords no line. It writes three
kinds of change:

- each spec file's marker, `codified-1` to `codified-2`;
- `imports: [cli]` in `spec/index.md`, when a line uses the pack's words (run, print, refuse, name, ...);
- each verb's aspect, where its lines decide it: a verb used only in triggers and responses is an action, one used
  only in While clauses a state.

Here is the change it made to the fixture's glossary:

```diff
-- **pick** (verb): a shopper puts goods in a cart. Forms: picks, picked. Frame: shopper picks cart.
-- **own** (verb): a shopper has a cart. Forms: owns, owned. Frame: shopper owns cart.
-- **watch** (verb): a shopper looks at a till. Forms: watches, watched. Frame: shopper watches till.
+- **pick** (verb, action): a shopper puts goods in a cart. Forms: picks, picked. Frame: shopper picks cart.
+- **own** (verb, state): a shopper has a cart. Forms: owns, owned. Frame: shopper owns cart.
+- **watch** (verb, action): a shopper looks at a till. Forms: watches, watched. Frame: shopper watches till.
  - **guard** (verb): a shopper keeps a cart. Forms: guards, guarded. Frame: shopper guards cart.
```

`guard` was left alone: one line uses it as a state and another as an action, so a person decides.

Everything it cannot decide, it prints. This is the fixture's full report, which also goes into the commit message:

```console
$ migrate upgrade
upgraded to 0.33.0: the controlled language 4
the controlled language 4: v_t14 guard, spec/index.md: a state in r7 and an action in r8; write (verb, state) or (verb, action)
the controlled language 4: spec/capabilities/buy.md r3 says "the" with no antecedent: refused: "the till" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a till
the controlled language 4: spec/capabilities/buy.md r4 says a negated indefinite in a While clause: refused: the While clause says "does not own a cart", which reads two ways: say "owns no cart" or "a cart that the shopper does not own"
the controlled language 4: spec/capabilities/buy.md r5 no longer parses: does not parse at quickly (token 7 of 15)
the controlled language 4: spec/capabilities/buy.md r6 no longer parses: does not parse at is (token 4 of 20)
the controlled language 4: spec/capabilities/buy.md r7 no longer parses: does not parse at guards (token 4 of 21)
the controlled language 4: spec/capabilities/buy.md r8 no longer parses: does not parse at guards (token 4 of 14)
the controlled language 4: spec/index.md full is a condition (adjective) grammar 4 reads no definition of; say it with a structure in each line using it: spec/capabilities/buy.md r6
the controlled language 4: spec/capabilities/buy.md r2 holds example data: `apples`; give it in its group's given block
the controlled language 4: spec/capabilities/buy.md r2 says "exit with an error naming": "refuse the command and name" says it shorter
the controlled language 4: spec/index.md the row till | for | shopper has no cardinality, which the old check read as one: write `one` where one is meant
the controlled language 4: v_t16 command, spec/index.md: the pack cli defines it too; mark the entry Redefines: cli
```

Each kind of note, and what to do about it:

| the report says | what you do |
|---|---|
| `v_t14 <verb> ...: a state in ... and an action in ...` | write `(verb, state)` or `(verb, action)` in the glossary |
| `<line> says "the" with no antecedent` | say the thing with "a" first, or reach it through a relation |
| `<line> says a negated indefinite in a While clause` | "owns no cart", or "a cart that the shopper does not own" |
| `<line> no longer parses: does not parse at <word>` | reword the line; `model parse` shows where it stops |
| `<term> is a condition (adjective) ...: <lines>` | replace the adjective with a structure, then reword each line named |
| `<line> holds example data: <value>` | move the value into the group's given block |
| `<line> says "exit with an error naming"` | "shall refuse the command and name X" |
| `the row <row> has no cardinality` | write `one` in the row where one is meant |
| `v_t16 <term> ...: the pack cli defines it too` | add `Redefines: cli.` to the entry |

## Step 3: fix the glossary, then reword the lines as an item

**The glossary first, by hand.** `spec/index.md`'s glossary entries and relation rows have no command yet, so edit
them and commit. For the fixture that was four edits: `Redefines: cli.` on `command`, `(verb, state)` on `guard`,
`one` in the `till | for | shopper` row, and the adjective `full` replaced by an attribute:

```text
- **load** (attribute of cart): how much a cart holds. Values: `empty`, `full`.
```

Some lines parse again once the glossary is right. The fixture's r7 did, after `guard` became a state. A line that
parses unchanged and means the same keeps its id.

**Then the lines, as one item.** A line in `spec/` is never edited in place. Each named line gets a new line with a
new id, and its old id goes to the capability's `retired:`. `work line --retires` does both:

<!-- docs: context tests/scripts/fixtures/docs-shop -->
```console
$ work idea "Reword buy for grammar 4"
b1 "Reword buy for grammar 4" idea
$ work line b1 --into buy --retires buy#r4 "While a shopper owns no cart, when the shopper picks a cart, the shopper shall watch a till."
b1 "Reword buy for grammar 4": buy#r9 retires buy#r4
$ work line b1 --into buy --in g2 --retires buy#r3 "When a shopper picks a cart, the shopper shall watch a till for the shopper."
b1 "Reword buy for grammar 4": buy#r10 retires buy#r3
```

Put every named line of a capability into the one item. The readiness bar checks the whole capability with the
item's lines laid in, so a line left behind stops it:

```console
$ work shape b1 --note "Reword the lines of buy that grammar 4 refuses."
b1 "Reword buy for grammar 4" shaped
$ work ready b1
work: work ready: b1 "Reword buy for grammar 4" is not passing:
  buy: buy#r3: refused: "the till" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a till
```

With r2, r3, r5, r6 and r8 reworded too, `work ready b1` passes, and `work batch start` lays the lines into `spec/`.
The old ids land in `retired:`, the new ones in `unbuilt:` until the batch builds them.

Two pairs from this repository's own spec show the most common rewordings. "Exit with an error naming" still
parses, but the refusal says it shorter and reads as one act:

```requirement
While an analysis tool is `missing`, when the person runs `tools probe`, `tools` shall exit with an error naming the analysis tool.
While an analysis tool is `missing`, if the person runs `tools probe`, then `tools` shall refuse the command and name the analysis tool.
```

"The item" with nothing before it is refused:

```refused
When the person runs `work shape` on the item, `work` shall set the status of the item to `shaped`.
```

```requirement
When the person runs `work shape` on an item, `work` shall set the status of the item to `shaped`.
```

[Writing requirements](writing-requirements.md) has the full set of pairs, and how to read a refusal. Claude knows
them too: say "reword the lines `migrate upgrade` named" and the [shaping-items](../skills/shaping-items/SKILL.md)
skill writes the item with you.

## Step 4: check, generate, and bind the new steps

In the batch's worktree, where the lines are laid, run the checks:

```console
$ model check
...
warning w_example  a requirement holds example data: a code or quoted string that names no declared constant  (1)
    capability/example.org/acme/shop/buy#r14, apples
...
$ model logic
L8 buy#r1 says nothing other requirements do not: Then 1 by buy#r10 and buy#r11
...
$ features generate
```

Read the findings as a list of small jobs. `w_example` is the reworded r2 still holding `apples`: give its group a
given block with `work line --given` (see [the given block](reference/capability-file.md)). L8 says r1 is now said
by r10 and r11 together, so retire r1 or narrow the new lines.

`features generate` rewrites each feature from grammar 4's reading, so expect new step wording. The reworded r4 is
now a Given of its own. Here is the scenario of the item's group `g2` with r9 and r10 in it:

<!-- docs: context tests/scripts/fixtures/docs-shop -->
```gherkin
  @g2 @r9 @r10
  Scenario: Reword buy for grammar 4
    Given a shopper s1
    And the shopper s1 owns no cart
    And a cart c1
    When the shopper s1 picks the cart c1
    Then the shopper s1 watches the till t1
    And the shopper s1 watches the till t2
    And the till t2 is for the shopper s1
```

If your handlers are registered with the plugin's `handler` (`from vocab import handler`, in `world_*.py` and
`*_handlers*.py` files under `tests/scenarios`), `features vocab --check` lists each step no handler matches.
Write a handler for each, then run your suite. If you bind steps with plain pytest-bdd, as
[getting started](getting-started.md) does, `--check` cannot see your steps and reports every one: skip it and
run your suite, whose missing steps fail by name.

```console
$ features vocab --check
.../features/buy.feature:7: the shopper s1 picks the cart c1 | no handler for WhenHappens pick
.../features/buy.feature:8: the shopper s1 watches the till t1 | no handler for ThenDoes watch
...
$ pytest -p work_items
```

A new id in `unbuilt:` runs as an expected failure until it is built. A reworded line whose behaviour already exists
may pass at once: check its steps test the line as now worded, then take its id out of `unbuilt:`. The handlers of a
retired line's steps that no scenario reaches any more can go.

## From 0.33 to 0.34

0.34 changes no line that parses: `migrate upgrade` applies the step 0.34.0 "value kinds", which writes no file and
names each attribute whose `Values:` declares neither kind and each line that says one of its values the short way
("an item is `idea`"), by file and id. Declare each attribute's values in the glossary, `Values (adjective):` for
those that read after "is" as an adjective (`shaped`, `in-batch`) and `Values (noun):` for the rest (`idea`,
`needs-input`, a release), then reword each named line whose value is a noun to the full form, "the status of an
item is `idea`", as an item with `work line --retires`. Until you declare them, `model check` warns `w_value_kind`
and every line parses as before.

`features generate` now writes every value step the full way, "the status of the item i1 is `idea`" (and "no item
whose status is `idea` exists" for "no K"). Regenerate your features; a handler keyed by `GivenK_A` or `ThenK_A`
keeps its key, and one that read the thing out of the step's text reads `step.subject` instead.

## From 0.34.0 to 0.34.1

No upgrade step. If `.shop/plugin-version` holds an old number, rewrite it first (see [Versions](#versions)). Then
run `features generate`: a scenario now has a Given for each thing its When names that no earlier Given brought in.

## From 0.34.1 to 0.35.0

No upgrade step, and no line that parsed before is refused.
It is a y release because the scenarios `features generate` writes change in ways a consuming repository's step
handlers must meet. Run `features generate`, then run the suite and update the handlers it fails on:

- **A Then after the act that brings its thing in.** The Thens that restrict a thing a response brings in now come
  after the act that brings it in, not before. A handler that read the thing before that act reads it after.
- **Counter-examples.** An every or only line's scenario now gives a thing that fails the restriction, and a
  negated Then of it:

  ```gherkin
  @g7 @r7
  Scenario: `work show` on a quote prints its messages
    Given a quote q1
    And a message m1
    And the quote q1 cites the message m1
    And a message m2
    And the quote q1 cites the message m2
    And a message m3
    And the quote q1 does not cite the message m3
    When the person runs `work show` on the quote q1
    Then `work` prints the message m1
    And `work` prints the message m2
    And `work` does not print the message m3
  ```

  Each negated Then needs a handler that brings its thing into the world (here a message the quote does not cite)
  and checks that the output does not hold it. A handler that passes whatever the output is lets the scenario pass
  a program that ignores the restriction. The Givens of a counter-example are negated too: a Given handler must
  accept "X does not V Y" (here "the quote q1 does not cite the message m3") and "the T of X is not `v`" ("the
  colour of the note n4 is not `red`").
- **A count's Then.** A count on what a response prints, with an upper bound, now gives one thing past the bound,
  and its Then states the count ("`notes` prints at most three notes"). Its handler counts the Ks in the output.
  A count that restricts a written thing ("write a batch that holds at most three items") gets no counter-example.
- **An order's Then.** A `ThenPrints` whose `step.order` is set, a (term, direction) pair, states an order. Its
  handler checks the output's order against the values the Givens set, not strictly, so that members with one value
  pass in either order.
- **`unread <id>`.** `model logic` now names each requirement it has no translation of, `unread <id>: ...`, with
  a count after the findings, where it printed `no findings` before over lines it skipped. Each one it names is a
  line `model logic` does not check; reword it if a construct it has a translation of says the same.

Two things are new to write. An attribute entry may say `Type: number.`, `Type: time.` or `Type: text.`: any
literal of the type is a value of it, and the type orders them, with no `Values:` or `Order:`. And a line may
compare two things' values ("the release of this repository is after the release of `migrate`") or print a
collection in an order (", ordered by release, in ascending order"). An order, or an after/before comparison, on
an attribute whose entry gives no value order, neither `Order:` nor `Type:`, is refused, naming the attribute;
"is the same as" takes any attribute. See
[Writing requirements](writing-requirements.md#3-collections-counts-comparisons-and-orders).

## From 0.35.0 to 0.35.1

No upgrade step, and no scenario `features generate` wrote in 0.35.0 changes. On a response's object, of `print` or any other
act, holds-exactly with a relative clause or a negated value as its restriction and "holds nothing" are now read by
`model logic`, and they, "holds no K" and an order on the object of a verb whose frame names the collection's kind
now get scenarios. `features generate` only warned of the last two in 0.35.0 (`no scenario: ...`) and exited 0, so a
repository may hold such lines: after the upgrade `features generate --check` finds its features stale until it is
run. Run `features generate` and write the
handlers of the new scenarios. `work ready` now refuses an item a requirement of which `model logic` names
`unread`, naming the requirement.

## From 0.35.1 to 0.36.0

A y release: no upgrade step, but regenerated features change for lines that read the same, and step
handlers may need a Given (below). Run `migrate upgrade` once: where 0.35.1 printed `no upgrade step is pending` and left
`.shop/plugin-version` behind, it now writes the release, commits and pushes it.

Run `features generate`. A line with "every K is not `v`" in a While clause, or "every K, ordered by ..." after a
verb whose frame names K, no longer crashes or goes without a scenario: write the handlers of their new scenarios.
"Every K in the Y, ordered by T" after such a verb reads one way, with the order on the Ks (0.35.1 put it on
the Y). A scenario of
a printed thing that holds another ("print a worktree that holds a file"), or of an order on a collection, now
brings both things in by a Given before the When ("a file f1", "a worktree w1"), and an order's first member is the
thing the line names: a repository whose handlers have no Given of those kinds writes one.

An item already `ready` whose group shares another group's condition and trigger (v15n) is refused at its next
`work ready` or `work batch start`: put the two groups' lines in one group. `work batch merged` resolves only a request
whose item `work accept` wrote from 0.36.0 on; resolve a request accepted before with `work resolve`.

Two commands ask for more. `work shape` on an idea with no shaping note under `## Notes` refuses without `--note`;
`work backlog` names `--note` beside such an idea. `work offer` with no `--capability` posts no glossary; with one,
it quotes the capability's requirements and only the terms they mention, so name each capability the asker needs.

## From 0.36.0 to 0.37.0

A y release: no upgrade step. Run `migrate upgrade` once to record the release.

`work ready` and `work batch start` now run every rule of `model check` on the item's lines laid over a copy of
`spec/`, and refuse each violation the lay brings that names one of the item's groups or requirements, naming the
group and the rule (v15k, v15l, v15n and the rest; 0.36.0 ran v15n alone). An item already `ready` may be refused at
its next `work ready` or `work batch start`: fix the group it names. Where a repository keeps a spec corpus
(`grammar/corpus/spec/`) or the catalogues `grammar/rules.md` and `grammar/constructs.md`, `work batch start` now
writes the laid lines' corpus blocks and regenerates the catalogues itself.

`work line --remove` now reads which id a line retires from the `retires:` pairs `work line --retires` writes into
the item. An item shaped before 0.37.0 has no such pairs: removing its `--retires` line keeps the retired id under
`retired:`, which would retire the live line with nothing in its place. After the removal, take that id out of the
block's `retired:` by hand.

Run `features generate`. A count on a thing a response writes ("write a file that holds at most three notes") gets
a Given of one thing past the bound, and holds-exactly whose restriction reaches a second thing gets a scenario
where it had none: write the handlers of their new steps.

New to use: `work chore` for an item with no requirement line, `work line --capability` for a new capability in
place of writing its file, `model forms --check`, and the directives (`work directive`, `work directives`,
`work promote`, `work drop`), which a new SessionStart hook shows. A repository's tests pin `pytest==9.1.1` and
`pytest-bdd==8.1.0` ([Getting started](getting-started.md)).

## Older than 0.32?

`migrate upgrade` applies every pending step in order, oldest first, in one commit. `migrate status` lists them:

```console
$ migrate status
the repository's plugin version: 0.30.0
the plugin's version: 0.33.0
pending upgrade step 0.31.0 "the workflow simplified": freeze .shop/work/, move the live requests to .shop/requests/ and write the decisions index
pending upgrade step 0.32.0 "verb frames": write each glossary entry's category as its part of speech and name each verb with no Frame:, each relational condition and each requirement that no longer parses
pending upgrade step 0.33.0 "the controlled language 4": write each file's marker codified-2, import the CLI pack and give each verb its aspect where its lines decide it, and name by file and id each line that no longer parses and what else a session rewords
```

**From 0.31**, the 0.32.0 step runs first. It writes each glossary term's part of speech and names each verb with no
`Frame:` and each condition that relates two kinds. Give each verb its frame by hand before you read the 0.33 notes:
a verb with no frame can't be given an aspect. See [0.32.0](../CHANGELOG.md#0320-released-as-300-verb-frames-parts-of-speech-in-the-glossary-and-verbs-typed-by-kind).

**From 0.30**, the 0.31.0 step runs before that. It freezes plugin 0.30's `.shop/work/`, moves the live requests to
`.shop/requests/` and writes the decisions index. Nothing there needs rewording. See
[0.31.0](../CHANGELOG.md#0310-released-as-200-the-workflow-simplified).

## On the old system?

A repository from before 0.21, with no `spec/` and `.shop/` layout, moves first with `migrate run`. It makes every
mechanical change of the move in one run, or none, and commits nothing:

```console
$ migrate run --context <owner/product/context>
```

Review and commit what it did. Then `migrate upgrade` takes the repository from there through every step to 0.33.

Next: [writing requirements](writing-requirements.md) for the language you're rewording into,
[troubleshooting](troubleshooting.md) when a line keeps being refused, or the [changelog](../CHANGELOG.md).
