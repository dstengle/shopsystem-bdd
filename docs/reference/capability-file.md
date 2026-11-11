<!-- Outputs on this page come from plugin 4.0.0, commit 28abbd977 of branch plan-docs, run 2026-11-10 in a scratch
clone of this repository (no remote). Every requirement line quoted here is a live line of this repository's spec. -->

# The files of a spec

This page is for the developer who builds against the generated features, and for anyone who writes or reviews
requirement lines. It walks through the files a bounded context keeps under `spec/` and `features/`, one real file
at a time, and says which of them a command writes for you and which you write by hand.

Every example is this repository's own spec, in `language: codified-2`. Files that still say `codified-1` are
refused by plugin 4.0; [upgrading](../upgrading.md) shows how `migrate upgrade` moves them over.

## The layout at a glance

```text
spec/
  index.md                 the bounded context: id, language, packs, glossary, relations, upstreams
  capabilities/<name>.md   one capability: its terms, relations and groups of requirement lines
  universal.md             the universal conditions, true everywhere
  decisions/<nnnn>-<slug>.md   one design-decision each
  decisions/index.md       the decisions' table, generated
features/
  <name>.feature           one capability's scenarios, generated
```

A **capability** is one file under `spec/capabilities/`: one thing the context does, told as groups of lines. Its
**feature** is the Gherkin file `features generate` writes from it. You never edit a feature by hand.

## A capability file, section by section

Here is `spec/capabilities/backlog.md`, abridged. Each part is explained below it.

### Frontmatter

```yaml
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/backlog
title: Backlog
narrator: a person or session keeping the backlog
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g6, r6, ..., g20, r20, g21, r21]
unbuilt: []
---
```

| key | what it holds |
|---|---|
| `id` | `capability/<context path>/<file name>`. The context path is the one in `spec/index.md`'s `id`. |
| `title` | The heading, and the feature's `Feature:` name. |
| `narrator` | Who the capability is told for. It becomes the feature's `Narrator:` line. |
| `group` | `service` (its scenarios run as tests) or `guarantees` (checked by script tests, not scenarios). |
| `language` | `codified-2`. A file without it is not read as a codified capability. |
| `rests_on` | The design-decisions the capability stands on. |
| `retired` | Group and requirement ids that are no longer live. They are never used again. |
| `unbuilt` | Requirement ids laid by a batch whose code isn't built yet. Their scenarios run as strict expected failures. |

`retired:` and `unbuilt:` are the two keys you'll see change most. Commands write both; the one hand edit is a
task taking its id out of `unbuilt:` in the commit that makes its scenario pass (see
[ids](#ids-groups-requirements-and-retired) below).

### Purpose

```markdown
## Purpose
`work` keeps the backlog of a bounded context in the repository, so that any session can read or change it: one item
for each piece of work, whatever its provenance, from a raw idea to its delivery (design goals 1 and 2). ...
```

Plain prose, for people. No tool reads it. Say what the capability is for and what it leaves out.

### Terms

```markdown
## Terms
- **title** (noun): the name of an item that the person reads beside its id. Kind of: text.
- **git branch** (noun): a branch of a git repository. Plural: git branches. Kind of: thing.
- **upstream branch** (noun): the branch of a remote that a git branch pushes to. Kind of: thing.
- **check out** (verb, state): a repository has a git branch as the one its working tree is on. Forms: checks out, checked out. Frame: repository checks out git branch.
- **reject** (verb, state): a remote declines a push made to it. Forms: rejects, rejected. Frame: remote rejects push.
```

Terms are words only this capability uses. Words the whole context shares go in `spec/index.md`'s glossary
instead. Each bullet has the same shape:

- **the word** in bold, then its **part of speech** in brackets: `noun`, `proper noun`, `attribute of <kind>`,
  `verb, action` or `verb, state`.
- one sentence that says what it means;
- then fields: `Kind of:` (the kind it is one of), `Plural:`, `Forms:` (a verb's other forms), `Frame:` (a verb's
  subject, object and recipient by kind), `Values:` (an attribute's values), `Not:` (words to avoid),
  `Redefines:` (a pack's word this entry takes over).

The grammar is built from these entries, so a term is a word you can use in a line. `model lexicon` lists every word
the context has, by category.

### Relations

```markdown
## Relations

| from | word | to | cardinality |
|---|---|---|---|
| title | of | item | one |
| git branch | of | task | one |
| upstream branch | of | git branch | one |
```

A row says which kinds a preposition joins. `title | of | item | one` is what lets a line say "the title of the
item", and `one` says an item has one title. Without the row, "the title of the item" is refused. Here's a line
that leans on the row `git branch | of | task`, with its meaning as `model parse --form` prints it:

```reading
While this repository checks out a git branch of a task, if the person runs `work idea`, then `work` shall refuse the command and name the task.
shall [x1: repository "the repository the command runs in" (indexical), x4: agent the person (constant), x5: command `work idea` (parameter), x6: tool `work` (constant)]
  while [x2: git branch, x3: task]
    of(x2, x3)
    check out(subject: x1, object: x2)
  if
    run(e1, subject: x4, object: x5)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x3)
```

`of(x2, x3)` is the relation row; `check out` is the state verb from the Terms above.

### Behaviour: groups of lines

This is the part everything else is generated from. Two groups from `backlog.md`:

```markdown
## Behaviour

### [g23] `work shape` shapes an idea
- [r23] While an item is `idea`, when the person runs `work shape` on the item, `work` shall set the status of the item to `shaped`.

### [g24] `work shape` refuses an item that is not an idea
- [r24] While an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
```

A **group** is a heading `### [g<n>] <title>`. Its title becomes the scenario's name, so write it as a short
sentence a reader can scan. Under it are one or more **requirement lines**, each a bullet `- [r<n>] <line>`. A
line is one sentence of the controlled language; [writing requirements](../writing-requirements.md) teaches it.

Every line must parse to exactly one meaning. Here is what g23's line means:

```reading
While an item is `idea`, when the person runs `work shape` on the item, `work` shall set the status of the item to `shaped`.
shall [x2: agent the person (constant), x3: command `work shape` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    status(x1) = `idea`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response
    initiates(e2, subject: x4, status(x1) = `shaped`)
```

And g24's, the refusal:

```reading
While an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
shall [x2: agent the person (constant), x3: command `work shape` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    not
      status(x1) = `idea`
  if
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: status]
    refuse(e2, subject: x4, object: x3)
    status(x1) = x5
    name(e3, subject: x4, object: x5)
```

A line can mean more than it says. `model explain` shows what else follows, here from the CLI pack's meaning of
"refuse" and from the universal condition U12:

```console
$ model explain 'backlog#r24'
backlog#r24  While an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
which also means:
  `work` shall exit with an error (by the definition of refuse in the pack cli)
  `work` shall change nothing (by U12)
  `work` shall exit with an error (by U12)
```

That's why g24 doesn't say "exit with an error and change nothing": it would only repeat what is already true.

### The sections after Behaviour

`backlog.md` ends with two sections of prose that no tool parses:

- **`## Implementation, may change`**: how the code does it today (`.shop/backlog/b<n>.md`, the score formula, the
  table order). It helps a builder, but nothing here is a requirement, and a batch may change it.
- **`## Not yet`**: what was asked and deliberately left out, with why.

Some older capabilities also have a **`## Dropped`** section and **`Restates:`** lines. They tie the file to the ids
of plugin 0.29 frozen in `spec/restated.json`: `Restates: r56@0.29.` under a group says it carries that old line,
and a `## Dropped` bullet says why an old id went. You only meet them in a repository that came from 0.29.

## A given block: example data for a group

Some behaviour needs a concrete value to test against. A sample value never goes in a line; it goes in the group's
fenced `given` block. From `spec/capabilities/batch-measurement.md`:

````markdown
### [g24] `measure show` prints the stage rows of a measurement whose stage row has no round trip without a round trip
Restates: r56@0.29.
- [r24] When the person runs `measure show` on a measurement that has a stage row that has no round trip, `measure` shall print every stage row of the measurement and not print a round trip.

```given
the measurement `m2` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
```
````

A given line has one shape: `the <words> <name> holds:` with indented data under it (a docstring or a `|` table),
or `the <words> <name> holds` followed by one code span or quoted string. Any other given line restates something
the line already says, and `model check` flags it. The block becomes the scenario's first Given, data and all (see
[the feature](#the-generated-feature-beside-its-lines)).

## `spec/index.md`: the bounded context

`spec/index.md` is the context's front page. This repository's, abridged:

```markdown
---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
language: codified-2
imports: [cli, spec]
---

# shopsystem-bdd

## Purpose
A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: ...

## Constraints
## Composition
## Testing

## Glossary
- **the person** (proper noun): the human who asks, answers and approves. Kind of: agent.
- **`work`** (proper noun): the command that writes statuses, transitions and requests. Kind of: tool.
- **tool** (noun): any of the commands `work`, `features`, `tools`, `measure`, `migrate` and `model`. Kind of: agent. Redefines: cli.
- **item** (noun): one file of the backlog, `.shop/backlog/b<n>.md`: ... Kind of: file.
- **status** (attribute of item): Values: `idea`, `shaped`, `ready`, `in-batch`, `delivered`, `needs-input`, `refused`, `withdrawn`.
- **commit** (verb, action): a session or a tool records changed files, ... Forms: commits, committed. Frame: agent commits text.
...

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| dependency | on | item | one |
| item | in | batch | one |
| task | of | batch | one |
...
```

The frontmatter:

- **`id`**: `bounded-context/<owner>/<product>/<context name>`. Every other id in the context starts from this path.
- **`language: codified-2`**: the language the context is written in. Plugin 4.0 reads only this.
- **`imports:`**: the packs the grammar starts from. A pack is a ready-made vocabulary: `cli` (commands, options,
  exit, refuse), `spec`, `time`. Their words are in [`grammar/packs/`](../../grammar/packs/). A glossary entry that
  takes a pack's word over says `Redefines: cli`.

The sections:

- **Purpose, Constraints, Composition, Testing**: prose for people. Composition usually lists the capabilities as
  tables of `capability | narrator | group`.
- **`## Glossary`**: the words every capability shares, in the same bullet shape as a capability's Terms. The
  `status` entry above is what makes `` `idea` `` and `` `shaped` `` legal values in g23.
- **`## Relations`**: rows shared by every capability, in the same table shape.
- **`## Upstreams`**: the contexts this one asks for things, one bullet each. This repository has none, so here is
  the shape `work line --upstream` checks, from the plugin's tests:

  ```markdown
  ## Upstreams
  - bounded-context/ex.com/prod/up: the upstream, github: ex/up
  ```

  The `github:` part is where `work request` opens its issue.

## `spec/universal.md`: true everywhere

Universal conditions are lines that hold in every state of every run. They're written once here and never repeated
in a capability. Its frontmatter has `retired:` too; its Behaviour is bullets with `U` ids:

```markdown
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-2
retired: [U1, U2, U3, U6, U9, U10, U11, U4, U5, U7, U8]
---
...
## Behaviour

- [U12] If a tool refuses a command, then the tool shall exit with an error naming a reason and change nothing.
- [U13] When `work` writes a transition, `work` shall commit the transition and push the commit of the transition.
...
```

`model logic` adds each one to the background of every check, and `model explain` names it where it applies (the
"by U12" above). Add one with `work line --universal`.

## A decision file

A design-decision is one file under `spec/decisions/`, named `<nnnn>-<slug>.md`. `work decision` writes it whole
and regenerates `spec/decisions/index.md`; don't write one by hand. Here's `0091-one-refusal-path.md`, abridged:

```markdown
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/one-refusal-path
summary: "Every refusal of every command reaches one base exception, shop_refused.Refused, and leaves through one catch a tool that exits 1 naming the reason and changes nothing."
date: 2026-11-10
status: accepted
tier: check
enforced_by: [tests/scripts/test_refusal_path.py::test_every_refusal_class_reaches_the_one_base, ...]
verified_by: [check]
rests_on: [U12]
by: "the plan for b145, 2026-11-10"
---

# 0091. One refusal path

## Context
...
## Decision
Every refusal of every command is a `shop_refused.Refused` ...
```

`tier:` is one of `check` (tests named in `enforced_by:` hold it, and `model decisions --check` runs them),
`requirement` (requirement lines hold it) or `judgement` (a reviewer holds it). The `## Decision` section is
standing; the rest of the file is record. A capability's `rests_on:` points at these ids.

## The generated feature, beside its lines

`features generate` reads each group and writes one scenario, tagged with the group's id and its lines' ids. Here are
g23 and g24 again, then what they became in `features/backlog.feature`:

```markdown
### [g23] `work shape` shapes an idea
- [r23] While an item is `idea`, when the person runs `work shape` on the item, `work` shall set the status of the item to `shaped`.

### [g24] `work shape` refuses an item that is not an idea
- [r24] While an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
```

```gherkin
# generated from spec/capabilities/backlog.md by features generate; do not edit
Feature: Backlog
  Narrator: a person or session keeping the backlog
  ...

  @g23 @r23
  Scenario: `work shape` shapes an idea
    Given an item i1
    And the item i1 is `idea`
    When the person runs `work shape` on the item i1
    Then `work` sets the status of the item i1 to `shaped`

  @g24 @r24
  Scenario: `work shape` refuses an item that is not an idea
    Given an item i1
    And the item i1 is not `idea`
    When the person runs `work shape` on the item i1
    Then `work` refuses `work shape`
    And `work` names the status of the item i1
```

Read them side by side:

- **While** became the Givens: the item, then its state. "an item" turns into a named instance, `i1`, so later
  steps can point at it.
- **When** or **If** became the When.
- **shall** became the Thens, one a response. "refuse the command and name ..." became two Thens.
- The group's title became the scenario's name, and `@g24 @r24` tie it back to its lines.

A given block comes first, as a Given with a docstring. batch-measurement's g24 opens like this:

```gherkin
  @g24 @r24
  Scenario: `measure show` prints the stage rows of a measurement whose stage row has no round trip without a round trip
    Given the measurement `m2` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
      """
    And a stage row s1
    ...
```

The output is byte-stable: generate twice and you get the same file. `features generate --check` prints nothing and
exits 0 when every feature matches its capability, which makes it a good CI step:

```console
$ features generate --check backlog
$ features generate backlog
wrote features/backlog.feature
```

Your step definitions bind these steps with pytest-bdd. Run pytest with `-p work_items` and every scenario whose
requirement is in `unbuilt:` becomes a strict expected failure: red is expected until it's built, and a pass fails
the run until the id leaves `unbuilt:`.

## Ids: groups, requirements and `retired:`

Ids are short and local to their file: `g23` and `r23` in `backlog.md`, written `backlog#r23` from elsewhere.
Universal conditions are `U<n>`. Three rules keep them meaningful:

1. **A line is never edited in place.** A changed line gets a new id, and the old id goes to `retired:`. A scenario
   tagged `@r15` always means the same sentence.
2. **A retired id is never reused.** `retired:` is the list of ids that are gone for good.
3. **Lines reach `spec/` only through a batch.** You write them on an item; `work batch start` lays them in.

Here is the whole path in a scratch clone of this repository. Say you want `work show` to print the status as well
as the title. That changes `backlog#r15`, so the new line retires it:

```console
$ work idea '`work show` prints the status too'
b250 "`work show` prints the status too" idea
$ work shape b250
b250 "`work show` prints the status too" shaped
$ work line b250 --into backlog --retires 'backlog#r15' --group '`work show` names an item by its title and status' 'When the person runs `work show` on an item, `work` shall print the title of the item and the status of the item.'
b250 "`work show` prints the status too": backlog#r37 retires backlog#r15
```

`work line` gave the line the next free ids of the capability, and the item now holds a block for `backlog`:

```markdown
## Requirements

### backlog

retired: [r15]

#### [g37] `work show` names an item by its title and status
- [r37] When the person runs `work show` on an item, `work` shall print the title of the item and the status of the item.
```

Meanwhile a second item, b251, also took a line for `backlog`. It was written before b250 reached `spec/`, so it got
`r37` too:

```console
$ work line b251 --into backlog 'When the person runs `work show` on an item, `work` shall print the provenance of the item.'
b251 "`work show` prints the provenance": backlog#r37
```

That's fine. Ids on an item are provisional. When both are rated, readied and picked, **`work batch start`
renumbers** each item's ids past the capability's live and retired ids and past the items picked before it, and
says so:

```console
$ work batch start
batch-34 building: t1 b250 "`work show` prints the status too", t2 b251 "`work show` prints the provenance"
batch brief: .../.shop/worktrees/batch-34-driver/brief.md
b251 "`work show` prints the provenance" renumbered: backlog#g37 -> backlog#g38, backlog#r37 -> backlog#r38
```

On the new branch `batch-34`, `backlog.md` changed like this (from `git diff`):

```diff
-retired: [g1, r1, ..., g21, r21]
-unbuilt: []
+retired: [g1, r1, ..., g21, r21, g15, r15]
+unbuilt: [r37, r38]
...
-### [g15] `work show` names an item by its title
-- [r15] When the person runs `work show` on an item, `work` shall print the title of the item.
...
+### [g37] `work show` names an item by its title and status
+- [r37] When the person runs `work show` on an item, `work` shall print the title of the item and the status of the item.
+
+### [g38] `work show` prints the provenance
+- [r38] When the person runs `work show` on an item, `work` shall print the provenance of the item.
```

Four things happened in one commit:

- `r15` went to `retired:`, and its group `g15` with it, since the group had no line left.
- `r37` and `r38` went into `unbuilt:`. Their scenarios run as expected failures until the task that builds each
  takes its id out, in the commit that makes it pass.
- The feature was regenerated: `@g15 @r15` is gone, and `@g37 @r37` and `@g38 @r38` are new.
- The commit cites both items (`Item: b250`, `Item: b251`).

## Who writes which file

`model forms` prints every file form a context keeps, its path, and the command that writes it. Where it says "no
command yet", you write the file by hand. This is its output at 4.0.0, verbatim:

```console
$ model forms
item                      .shop/backlog/b<n>.md                                work idea
item's requirement line   .shop/backlog/b<n>.md ## Requirements                work line
item's term bullet        .shop/backlog/b<n>.md ## Requirements                work line --term
requirement line in spec  spec/capabilities/<name>.md ## Behaviour             work batch start
batch plan                .shop/batches/<n>/plan.md                            work batch start
review record             .shop/batches/<n>/review-<k>.md                      work batch reviewed
defect                    .shop/batches/<n>/defect-<k>.md                      measure defect
batch measurement         .shop/records/measurements/<date>-<batch>.md         measure batch
request                   .shop/requests/q<n>.md                               work request
quote                     .shop/quotes/<n>.md                                  work quote
design-decision           spec/decisions/<nnnn>-<slug>.md                      work decision
decisions index           spec/decisions/index.md                              model decisions
rule catalogue            grammar/rules.md                                     model rules --write
record                    .shop/records/<date>-<slug>.md                       work record
records index row         .shop/records/README.md                              work record
feature                   features/<capability>.feature                        features generate
plugin version            .shop/plugin-version                                 migrate upgrade
restated ids              spec/restated.json                                   migrate upgrade
capability                spec/capabilities/<name>.md                          plugin item b13 (no command yet)
glossary term             spec/index.md ## Glossary                            plugin item b13 (no command yet)
relation row              spec/capabilities/<name>.md ## Relations             work line --relation
glossary relation row     spec/index.md ## Relations                           plugin item b13 (no command yet)
universal condition       spec/universal.md                                    work line --universal
upstream entry            spec/index.md ## Upstreams                           work line --upstream
given block               spec/capabilities/<name>.md, a group's fenced given  work line --given
observation               .shop/records/observations.md ## <id>                by hand (no command yet)
delivery settings         .shop/delivery.toml                                  by hand (no command yet)
```

In short: a new capability file, a glossary term and a glossary relation row are by hand today, and so are the
prose sections (Purpose, Implementation, Not yet). Lines, terms of a capability, relation rows of a capability,
given blocks, universal conditions and upstreams go on an item with `work line`, and reach `spec/` through
`work batch start`. After a hand edit, run `model check` and `model lexicon --check` to catch a malformed entry.

Next: [writing requirements](../writing-requirements.md) for the language of a line,
[the commands](commands.md) for every option of `work line` and `features generate`, or
[the design model](design-model.md) for the rules `model check` holds these files to.
