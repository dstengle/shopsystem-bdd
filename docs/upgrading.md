<!-- Outputs on this page are from real runs on 2026-11-10, plugin 4.0.0 (commit 7f60e57de): a 3.0.1 repository
built from the 4.0.0 upgrade's test fixture (tests/scripts/test_migrate_upgrade_cnl4.py), upgraded and reworded. -->

# Upgrading from 3.x to 4.0

This page is for the maintainer of a repository on plugin 3.x. It takes you from `migrate status` to a green suite
on 4.0, one step at a time. Most of the work is rewording lines, and Claude can do that with you.

Here is the whole job in one picture. `migrate upgrade` changes what is mechanical and names, by file and id, every
line you have to reword:

```console
$ migrate upgrade
upgraded to 4.0.0: the controlled language 4
...
the controlled language 4: spec/capabilities/buy.md r4 says a negated indefinite in a While clause: refused: the While clause says "does not own a cart", which reads two ways: say "owns no cart" or "a cart that the shopper does not own"
...
```

You then write a new line under a new id, and the old id is retired:

```text
before  [r4] While a shopper does not own a cart, when the shopper picks a cart, the shopper shall watch a till.
after   [r9] While a shopper owns no cart, when the shopper picks a cart, the shopper shall watch a till.
```

(These two lines use the fixture's glossary, a toy shop with shoppers, carts and tills, so they parse there, not in
this repository.)

## What changed in 4.0

The full note is [4.0.0 in the changelog](../CHANGELOG.md#400-the-controlled-language-4). What it means for you:

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
started on 3.x lays lines in the old language.

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

Run `tools install` again even if 3.x had it working. Grammar 4 is built on GF's resource grammar library, the
`gf-rgl` line, which 3.x never installed. Grammar 4 is compiled against it.

Then ask what is pending:

```console
$ migrate status
the repository's plugin version: 3.0.1
the plugin's version: 4.0.0
pending upgrade step 4.0.0 "the controlled language 4": write each file's marker codified-2, import the CLI pack and give each verb its aspect where its lines decide it, and name by file and id each line that no longer parses and what else a session rewords
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
+- **pick** (verb, action): a shopper puts goods in a cart. Forms: picks, picked. Frame: shopper picks cart.
+- **own** (verb, state): a shopper has a cart. Forms: owns, owned. Frame: shopper owns cart.
  - **guard** (verb): a shopper keeps a cart. Forms: guards, guarded. Frame: shopper guards cart.
```

`guard` was left alone: one line uses it as a state and another as an action, so a person decides.

Everything it cannot decide, it prints. This is the fixture's full report, which also goes into the commit message:

```console
$ migrate upgrade
upgraded to 4.0.0: the controlled language 4
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
$ work shape b1
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
now a Given of its own:

```gherkin
  @g2 @r9 @r10 @r11 @r12 @r13
  Scenario: Reword buy for grammar 4
    Given a shopper s1
    And the shopper s1 owns no cart
    When the shopper s1 picks the cart c1
    Then the shopper s1 watches the till t1
```

`features vocab --check` lists each step no handler matches. Write a handler for each, then run your suite:

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

## Older than 3.0?

`migrate upgrade` applies every pending step in order, oldest first, in one commit. `migrate status` lists them:

```console
$ migrate status
the repository's plugin version: 1.0.0
the plugin's version: 4.0.0
pending upgrade step 2.0.0 "the workflow simplified": freeze .shop/work/, move the live requests to .shop/requests/ and write the decisions index
pending upgrade step 3.0.0 "verb frames": write each glossary entry's category as its part of speech and name each verb with no Frame:, each relational condition and each requirement that no longer parses
pending upgrade step 4.0.0 "the controlled language 4": write each file's marker codified-2, import the CLI pack and give each verb its aspect where its lines decide it, and name by file and id each line that no longer parses and what else a session rewords
```

**From 2.x**, the 3.0.0 step runs first. It writes each glossary term's part of speech and names each verb with no
`Frame:` and each condition that relates two kinds. Give each verb its frame by hand before you read the 4.0 notes:
a verb with no frame can't be given an aspect. See [3.0.0](../CHANGELOG.md#300-verb-frames-parts-of-speech-in-the-glossary-and-verbs-typed-by-kind).

**From 1.x**, the 2.0.0 step runs before that. It freezes plugin 1.x's `.shop/work/`, moves the live requests to
`.shop/requests/` and writes the decisions index. Nothing there needs rewording. See
[2.0.0](../CHANGELOG.md#200-the-workflow-simplified).

## On the old system?

A repository from before 0.21, with no `spec/` and `.shop/` layout, moves first with `migrate run`. It makes every
mechanical change of the move in one run, or none, and commits nothing:

```console
$ migrate run --context <owner/product/context>
```

Review and commit what it did. Then `migrate upgrade` takes the repository from there through every step to 4.0.

Next: [writing requirements](writing-requirements.md) for the language you're rewording into,
[troubleshooting](troubleshooting.md) when a line keeps being refused, or the [changelog](../CHANGELOG.md).
