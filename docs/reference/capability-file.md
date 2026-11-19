<!-- Outputs on this page come from plugin 0.38.0, branch domain-contract, run 2026-11-19 in this repository and in a
scratch clone of it (no remote). Every requirement line quoted here is a live line of this repository's spec. -->

# The files of a spec

This page is for the developer who builds against the generated features, and for anyone who writes or reviews
requirement lines. It walks through the files a bounded context keeps under `spec/` and `features/`, one real file
at a time, and says which of them a command writes for you and which you write by hand.

Every example is this repository's own spec, in `language: codified-2`. Files that still say `codified-1` are
refused since plugin 0.33, and a context with no domain model since 0.38; [upgrading](../upgrading.md) shows how
`migrate upgrade` moves them over.

## The layout at a glance

```text
spec/
  index.md                     the bounded context: id, language, packs, purpose, composition, upstreams
  model/<area>.md              the domain model of one area: objects, lifecycles, relations, services, operations
  vocabulary/<area>.md         the words of one area, each naming one element of the model
  vocabulary/shared.md         the words every area reads
  capabilities/<name>.md       one capability: its groups of requirement lines
  universal.md                 the universal conditions, true everywhere
  decisions/<nnnn>-<slug>.md   one design-decision each
  decisions/index.md           the decisions' table, generated
  adapters/<port>.toml         one adapter's contract: the CLI's commands and options for each operation
  moves.json                   the capability moves: an old id and the id it moved to
features/
  <name>.feature               one capability's scenarios, generated
```

The specification has four parts: the **domain model**, the **vocabulary**, the **requirements** (the capabilities
and the universal conditions) and the **decisions**; the adapter contracts sit beside them. The model and the
vocabulary have their own reference, [the domain model](domain-model.md); the adapter contracts theirs,
[adapter contracts](adapters.md). A **capability** is one file under `spec/capabilities/`: the rules about one service
or one object's lifecycle, told as groups of lines. Its **feature** is the Gherkin file `features generate` writes
from it. You never edit a feature by hand.

## A capability file, section by section

Here is `spec/capabilities/items.md`, abridged. Each part is explained below it.

### Frontmatter

```yaml
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/items
title: Items
narrator: the person
group: service
area: tracking
specifies: object item, service backlog, the readiness policy
language: codified-2
retired: []
unbuilt: []
---
```

- **`id`**: `capability/` and the context's path, then the file's name. Its groups and lines are written
  `items#g14` and `items#r14` from anywhere else.
- **`title`**: the feature's name.
- **`narrator`**: who the scenarios are told for, written under the feature's title.
- **`group`**: `service` (what a service does when it is asked) or `guarantees` (what holds of an agent's work).
- **`area`**: the area of the domain model the lines are read in: the words of its vocabulary layer, the layers it
  imports and `shared`.
- **`specifies`**: what the capability is about, in words a person reads: a service, an object, a policy.
- **`language: codified-2`**: the lines are in grammar 4, the plugin's controlled language.
- **`retired`**: ids that are gone for good; **`unbuilt`**: ids whose code is not written yet, their scenarios run
  as expected failures. A file may also say **`rests_on:`**, the design-decisions it stands on.

### Purpose

```markdown
## Purpose
The backlog's items through their lifecycle: noted as ideas, shaped, rated, linked, readied against the readiness bar,
declined, withdrawn, answered and listed.
```

One paragraph for people. No tool reads it. A capability has no `## Terms` and no `## Relations`: its words are the
vocabulary's and its relations the model's.

### Behaviour: groups of lines

This is the part everything else is generated from. Two groups from `items.md`:

```markdown
## Behaviour

### [g14] An idea shaped becomes shaped
- [r14] While the status of an item is `idea`, when the person shapes the item, the backlog service shall set the status of the item to `shaped`.

### [g15] Only an idea is shaped
- [r15] While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
```

`### [g<n>] <title>` opens a group; the title becomes the scenario's name. `- [r<n>] <line>` is one requirement.
A group may hold several lines, which make one scenario together; two groups of one capability may not share their
features, condition and trigger (`v15n`). A long line may be wrapped, its later lines indented two spaces.

Every line must parse to exactly one meaning. Here is what g14's line means:

```reading
While the status of an item is `idea`, when the person shapes the item, the backlog service shall set the status of the item to `shaped`.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `idea`
  when
    request(e1, backlog.shape, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `shaped`)
```

"The person shapes the item" is a request of the operation `backlog.shape`, which `spec/model/tracking.md` declares
with its outcomes (`done | refused: item not an idea, no note`). g15's line states the refusal `item not an idea`; a
refusal reason no line states is a violation (`v_m4`). `spec explain` prints what else a line means, here from the
universal condition U17:

```console
$ spec explain items#r15
items#r15  While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
which also means:
  the backlog service shall change nothing (by U17)
  the backlog service shall name a reason (by U17)
```

### The sections after Behaviour

A capability may end with sections of prose that no tool parses:

- **`## Implementation, may change`**: how the code does it today, for the developer; a line never says this.
- **`## Not yet`**: what the capability deliberately leaves out.
- **`## Dropped`**: 0.29 ids not restated, each with why; **`## Moved`**: each old id and the new id it moved to, in
  a capability whose lines moved to another (0.38.0 moved every line; `spec/moves.json` holds the whole map).

## A given block: example data for a group

Sample values never go in a line. They go in a fenced `given` block under the group, from
`spec/capabilities/measurement.md`:

````markdown
### [g6] A measurement viewed gives no round trip of a stage row that has none
Restates: batch-measurement#r56@0.29.
- [r6] When the person views a measurement that has a stage row that has no round trip, the measurement service shall
  return every stage row of the measurement and not return a round trip.
```given
the measurement `m2` holds:
  {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
```
````

Each line of the block is a step of the step grammar: `the <kind> <name> holds:` with data under it, or `the <kind>
<name> holds` and one code span or quoted string. `Restates:` names the 0.29 ids the group stands for. Add a block
with `work line --given`.

## `spec/index.md`: the bounded context

```markdown
---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
language: codified-2
imports: [request, spec]
---

# shopsystem-bdd

## Purpose
A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: ...

## Constraints
## Composition
## Testing
## Upstreams
```

- **`id`**: `bounded-context/` and the context's path: every other id of the context starts from it.
- **`language: codified-2`**: the language of every file that says nothing else.
- **`imports:`**: the packs the grammar starts from. `request` (the words of a request and its response), `spec`,
  `time`; their words are in [`grammar/packs/`](../../grammar/packs/). A vocabulary entry that takes a pack's word over
  says `Redefines: <pack>`. `imports: [cli]` is refused since 0.38.0 (`v_t21`).
- **`## Composition`**: the areas of the context, each with its kind (core, supporting, generic) and its
  capabilities, narrators and groups.
- **`## Upstreams`**: the contexts this one asks for things, each with its `github:` repository; `work line
  --upstream` adds one.

## `spec/universal.md`: true everywhere

Universal conditions are lines that hold in every state of every request. They're written once here and never
repeated in a capability. Its frontmatter has `retired:` too; its Behaviour is bullets with `U` ids:

```markdown
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-2
retired: [U1, U2, U3, U6, U9, U10, U11, U4, U5, U7, U8, U12, U13, U14, U15, U16]
---
...
## Behaviour

- [U17] If a service refuses a request, then the service shall name a reason and change nothing.
- [U18] A session shall not change an item.
- [U19] While a session has a workspace, the session shall change only files in the workspace.
```

`spec logic` adds each one to the background of every check, and `spec explain` names it where it applies (the
"by U17" above). Add one with `work line --universal`.

## A decision file

A design-decision is one file under `spec/decisions/`, named `<nnnn>-<slug>.md`. `work decision` writes it whole
and regenerates `spec/decisions/index.md`; don't write one by hand. Here's `0104-the-response-envelope.md`, abridged:

```markdown
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-response-envelope
summary: "Every operation answers with one envelope of outcome, content, errors and notices, its errors naming business references; a failure of the infrastructure is outside the domain. U16 retires into this decision."
date: 2026-11-19
status: accepted
tier: check
enforced_by: [tests/scripts/test_domain_envelope.py]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u8-is-checked-after-every-scenario-enforced-by-its-test]
---

# 0104. The response envelope

## Decision
...
```

`tier:` is one of `check` (tests named in `enforced_by:` hold it, and `spec decisions --check` runs them),
`requirement` (requirement lines hold it) or `judgement` (a reviewer holds it). The `## Decision` section is
standing; the rest of the file is record. A mechanism (the CLI, git, GitHub issues, pull requests, the files) is a
decision, never a requirement line. A capability's `rests_on:` points at these ids.

## The generated feature, beside its lines

g14 and g15 again, then what they became in `features/items.feature`:

```markdown
### [g14] An idea shaped becomes shaped
- [r14] While the status of an item is `idea`, when the person shapes the item, the backlog service shall set the status of the item to `shaped`.

### [g15] Only an idea is shaped
- [r15] While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
```

```gherkin
# generated from spec/capabilities/items.md by features generate; do not edit
Feature: Items
  Narrator: the person

  # ... the scenarios before g14

  @g14 @r14
  Scenario: An idea shaped becomes shaped
    Given an item i1
    And the status of the item i1 is `idea`
    When the person shapes the item i1
    Then the backlog service sets the status of the item i1 to `shaped`

  @g15 @r15
  Scenario: Only an idea is shaped
    Given an item i1
    And the status of the item i1 is not `idea`
    When the person shapes the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1
```

The While clause became Givens, the request a When, the response Thens. "this request" is the request the When
makes. A given block becomes a docstring, and "every" becomes two instances and their Thens, with a third the line
excludes (g6 of `measurement.md`):

```gherkin
  @g6 @r6
  Scenario: A measurement viewed gives no round trip of a stage row that has none
    Given the measurement `m2` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
      """
    And a stage row s1
    And the stage row s1 has no round trip
    And a measurement m1
    And the measurement m1 has the stage row s1
    And a stage row s2
    And the measurement m1 has the stage row s2
    And a stage row s3
    And the measurement m1 has the stage row s3
    And a stage row s4
    And the measurement m1 does not have the stage row s4
    When the person views the measurement m1
    Then the measurement service returns the stage row s2
    And the measurement service returns the stage row s3
    And the measurement service does not return the stage row s4
    And the measurement service does not return a round trip
```

The output is byte-stable: generate twice and you get the same file. `features generate --check` prints nothing and
exits 0 when every feature is current:

```console
$ features generate --check items
$ features generate items
wrote features/items.feature
```

## Ids: groups, requirements and `retired:`

Ids are short and local to their file: `g14` and `r14` in `items.md`, written `items#r14` from elsewhere. An id is
never reused and a line is never edited in place: a changed line gets a new id and the old one goes to `retired:`
([decision 0085](../../spec/decisions/0085-requirements-retired-never-edited.md)).

Here is the whole path in a scratch clone of this repository. Say you want showing an item to give its status as
well as its title. That changes `items#r12`, so the new line retires it:

```console
$ work idea 'Showing an item gives its status too' --note 'the person wants to see where an item stands beside its title'
b250 "Showing an item gives its status too" idea
$ work shape b250
b250 "Showing an item gives its status too" shaped
$ work line b250 --into items --retires 'items#r12' --group 'An item shown gives its title and status' 'When the person shows an item, the backlog service shall return the title of the item and the status of the item.'
b250 "Showing an item gives its status too": items#r31 retires items#r12
```

`work line` gave the line the next free ids of the capability, and the item now holds a block for `items`:

```markdown
## Requirements

### items

retired: [r12]
retires: [r31 r12]

#### [g31] An item shown gives its title and status
- [r31] When the person shows an item, the backlog service shall return the title of the item and the status of the item.
```

Meanwhile a second item, b251, also took a line for `items`. It was written before b250 reached `spec/`, so it got
the same ids. That's fine: `work batch start` renumbers each item's ids past the capability's and the other picked
items' when it lays them:

```console
$ work line b251 --into items --group 'An item shown gives its provenance' 'When the person shows an item, the backlog service shall return the provenance of the item.'
b251 "Showing an item gives its provenance": items#r31
$ work batch start
batch-34 building: t1 b250 "Showing an item gives its status too", t2 b251 "Showing an item gives its provenance"
b251 "Showing an item gives its provenance" renumbered: items#g31 -> items#g32, items#r31 -> items#r32
```

On the new branch `batch-34`, one commit did four things:

- `r12` went to `retired:`, and its group `g12` with it, since the group had no line left.
- `r31` and `r32` went into `unbuilt:`. Their scenarios run as expected failures until the task that builds each
  takes its id out, in the commit that makes it pass.
- The feature was regenerated: `@g12 @r12` is gone, and `@g31 @r31` and `@g32 @r32` are new.
- The commit cites both items (`Item: b250`, `Item: b251`).

## Who writes which file

`spec forms` prints every file form a context keeps, its path, and the command that writes it. Where it says "no
command yet", it names the plugin's item that will give the form one; `spec forms --check` fails on any form left
to be written by hand. This is its output at 0.38.0, verbatim:

```console
$ spec forms
item                      .shop/backlog/b<n>.md                                   work idea
item's requirement line   .shop/backlog/b<n>.md ## Requirements                   work line
item's chore              .shop/backlog/b<n>.md ## Chore                          work chore
item's term bullet        .shop/backlog/b<n>.md ## Requirements                   work line --term
requirement line in spec  spec/capabilities/<name>.md ## Behaviour                work batch start
batch plan                .shop/batches/<n>/plan.md                               work batch start
review record             .shop/batches/<n>/review-<k>.md                         work batch reviewed
defect                    .shop/batches/<n>/defect-<k>.md                         measure defect
batch measurement         .shop/records/measurements/<date>-<batch>.md            measure batch
request                   .shop/requests/q<n>.md                                  work request
quote                     .shop/quotes/<n>.md                                     work quote
directive                 .shop/directives/<n>.md                                 work directive
design-decision           spec/decisions/<nnnn>-<slug>.md                         work decision
decisions index           spec/decisions/index.md                                 spec decisions
rule catalogue            grammar/rules.md                                        spec rules --write
record                    .shop/records/<date>-<slug>.md                          work record
records index row         .shop/records/README.md                                 work record
feature                   features/<capability>.feature                           features generate
plugin version            .shop/plugin-version                                    migrate upgrade
restated ids              spec/restated.json                                      migrate upgrade
capability                spec/capabilities/<name>.md                             work line --capability
item's model lines        .shop/backlog/b<n>.md ## Requirements ### <area> model  work line --model
domain model area         spec/model/<area>.md                                    plugin item b354 (no command yet)
vocabulary term           spec/vocabulary/<area>.md                               plugin item b13 (no command yet)
adapter contract          spec/adapters/<port>.toml                               plugin item b355 (no command yet)
capability moves          spec/moves.json                                         migrate upgrade
universal condition       spec/universal.md                                       work line --universal
upstream entry            spec/index.md ## Upstreams                              work line --upstream
given block               spec/capabilities/<name>.md, a group's fenced given     work line --given
observation               .shop/records/observations.md ## <id>                   plugin item b44 (no command yet)
delivery settings         .shop/delivery.toml                                     plugin item b44 (no command yet)
design record folder      .shop/records/<date>-<topic>/design.md                  plugin item b44 (no command yet)
plan record folder        .shop/records/<date>-<topic>/plan-<k>.md                plugin item b44 (no command yet)
```

In short: a new capability is written on an item by `work line --capability` and reaches `spec/` through
`work batch start`, as do lines, model lines and vocabulary entries (`work line --model`, `--relation`, `--term`),
given blocks, universal conditions and upstreams, each by its `work line` option. A whole model area, a vocabulary
entry outside an item and an adapter contract wait on plugin items b354, b13 and b355, and the prose sections
(Implementation, Not yet) are edited by hand. After a hand edit, run `spec check` and `spec lexicon --check` to catch
a malformed entry.

Next: [writing requirements](../writing-requirements.md) for the language of a line,
[the commands](commands.md) for every option of `work line` and `features generate`,
[the domain model](domain-model.md) for the model and its words, or [the design model](design-model.md) for the rules
`spec check` holds these files to.
