---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
title: Migration tools
narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases
group: service
language: codified-2
rests_on: [design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/references-are-ids, design-decision/capability-ids-are-context-scoped, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/upgrades-between-plugin-releases, design-decision/work-items-named-by-ids, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked]
retired: [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19, g20, g21, g24, g25, g45, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r45]
unbuilt: []
---

# Migration tools

## Purpose
`scripts/migrate` makes the mechanical changes that take a repository from the old system to the final layout
(design-decision/final-layout) in one `migrate run`, and the upgrades that take a repository on the final layout from
one plugin release to the next (design-decision/upgrades-between-plugin-releases). It is the only code in the plugin
that knows the old layout, and it decides nothing that needs judgment. The plugin's hooks run it to tell a session
what it needs to know at its start and before it is compacted.

## Terms
- **the SessionStart hook** (proper noun): the plugin's hook that runs `migrate status --hook` when a session starts, and
  gives the session what it prints. Kind of: agent.
- **repository** (noun): the repository `migrate` runs in, with its working tree. Plural: repositories. This: the repository the command runs in.
- **tracked file** (noun): a file committed in the repository `migrate` runs in. Kind of: file.
- **uncommitted change** (noun): a change to the working tree of a repository that no commit holds: a file git does not track, or a change to a tracked file. Kind of: text.
- **old-layout directory** (noun): a directory of the old system's layout at the root of a repository: `decisions/`, `work/`, `records/`, `docs/superpowers/plans/`, `docs/superpowers/specs/`, `docs/superpowers/requests/` or `adrs/`. Kind of: file.
- **mention** (verb, state): a text holds the path, a relative link to or the id of a thing. Forms: mentions, mentioned. Frame: text mentions thing.
- **rewrite** (verb, action): `migrate` changes the text of a file in place. Forms: rewrites, rewritten. Frame: `migrate` rewrites file.
- **rename** (verb, action): `migrate` gives a file another name with git. Forms: renames, renamed. Frame: `migrate` renames file.
- **decision ledger** (noun): the old system's ledger of decisions, the file `spec/decisions.md`. Kind of: file.
- **ledger entry** (noun): one entry `## decision/<name>` of a decision ledger. Plural: ledger entries. Kind of: text.
- **supersede** (verb, state): a ledger entry or a design-decision names another, whole or in part, as the one it takes the place of. Forms: supersedes, superseded. Frame: ledger entry supersedes ledger entry.
- **qualifier** (noun): the words after the id a ledger entry supersedes, as `(in part)`. Kind of: text.
- **ledger number** (noun): the `<nnnn>` before the name of a ledger entry. Kind of: text.
- **stem** (noun): the part of the id of a ledger entry after `decision/`, or the name of a tracked file without its directory and its extension. Kind of: text.
- **Behaviour line** (noun): a line of the `## Behaviour` of a capability of the old system. Kind of: text.
- **line id** (noun): the `[r<n>]` of a Behaviour line. Kind of: text.
- **plugin version file** (noun): the file `.shop/plugin-version`, one line naming the plugin release a repository is on. Kind of: file.
- **content** (noun): the text a file holds. Kind of: text.
- **shop directory** (noun): the directory `.shop/` of a repository. Kind of: file.
- **upgrade step** (noun): one step of `migrate upgrade` from one plugin release to the next, named by its title. Kind of: thing.
- **release** (attribute of repository): Values: `0.23.1`, `0.24.0`, `0.25.0`, `0.29.0`, `1.0.0`, `2.0.0`, `3.0.0`, `3.0.1`, `9.0.0`. Order: by number.
- **release** (attribute of upgrade step): Values: `0.24.0`, `0.25.0`, `1.0.0`, `2.0.0`, `3.0.0`. Order: by number.
- **work-item file** (noun): the file `.shop/work/<initiative>/<work-item>.md` of a work-item of plugin 1.x. Kind of: file.
- **stage directory** (noun): the directory `.shop/work/<initiative>/runs/<work-item>/` of a work-item's stages. Kind of: file.
- **initiative log** (noun): the file `.shop/work/<initiative>/log.jsonl` of an initiative of plugin 1.x. Kind of: file.
- **restated file** (noun): the file `spec/restated.json`, the 0.29 requirements by id. Kind of: file.
- **frozen notice** (noun): the file `.shop/work/FROZEN.md`, which says that the queue of plugin 1.x is frozen. Kind of: file.
- **frozen request** (noun): a request of plugin 1.x under `.shop/work/requests/`. Kind of: file.
- **status** (attribute of frozen request): Values: `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`, `refused`, `withdrawn`.
- **asker** (attribute of frozen request): the `asker:` of a frozen request, `internal` when the bounded context asked it of itself, else the id of the bounded context that asked it. Values: `internal`.
- **index file** (noun): the file `spec/index.md` of a bounded context. Kind of: file.
- **`no upgrade step is pending`** (proper noun): what `migrate upgrade` prints when no upgrade step is pending. Kind of: text.
- **`only on the person's yes`** (proper noun): the SessionStart hook's note that a session runs a pending upgrade only on the person's yes. Kind of: text.
- **`update the plugin`** (proper noun): the SessionStart hook's note to a session in a repository on a release after the plugin's. Kind of: text.
- **`holds no version`** (proper noun): the SessionStart hook's note on a plugin version file that holds no version. Kind of: text.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| old-layout directory | in | repository |  |
| uncommitted change | in | repository |  |
| ledger entry | of | decision ledger |  |
| decision ledger | of | repository | one |
| qualifier | of | ledger entry | one |
| ledger number | of | ledger entry | one |
| stem | of | ledger entry | one |
| stem | of | tracked file | one |
| design-decision | of | ledger entry | one |
| qualifier | in | design-decision |  |
| Behaviour line | of | capability |  |
| line id | of | Behaviour line | one |
| tracked file | in | old-layout directory |  |
| plugin version file | of | repository | one |
| version | in | plugin version file | one |
| content | of | plugin version file | one |
| shop directory | of | repository | one |
| capability | of | repository |  |
| scenario | in | feature |  |
| decisions index | of | repository | one |
| frozen notice | of | repository | one |
| initiative | of | repository |  |
| index file | of | bounded context | one |

## Behaviour

### [g27] `migrate run` relocates every old-layout directory and rewrites every file that mentions one
Restates: r1@0.29, r4@0.29, r5@0.29, r8@0.29, r9@0.29, r12@0.29, r14@0.29.
- [r27] While this repository holds an old-layout directory, when the person runs `migrate run` on a bounded context, `migrate` shall relocate every old-layout directory and rewrite every file that mentions an old-layout directory.

```given
the tracked file `decisions/0001-a.md` holds:
  ---
  id: decision/0001-a
  status: accepted
  ---
  # a
the tracked file `work/i1-cart/initiative.md` holds:
  ---
  id: initiative/i1-cart
  status: done
  ---
the tracked file `records/notes/one.md` holds:
  # one
  A note of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
  And a third line.
the tracked file `docs/superpowers/plans/2025-01-01-cart.md` holds:
  # The cart plan
  A plan of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `docs/superpowers/specs/2025-01-01-cart-design.md` holds:
  # The cart design
  A design note of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `docs/superpowers/requests/2025-01-02-pay.md` holds:
  # Pay
  A request of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `adrs/0001-use-git.md` holds:
  # Use git
  An ADR of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/shop
  title: shop
  ---
  # shop
the tracked file `README.md` holds:
  See [the note](records/notes/one.md) and work/i1-cart/initiative.md.
the tracked file `spec/capabilities/thing.md` holds:
  ---
  title: thing
  narrator: a client
  group: service
  rests_on: []
  retired: []
  ---
  # thing
  ## Purpose
  Something.
  ## Behaviour
  - [r1] **When** a, `thing` shall a.
```

### [g28] `migrate run` writes a design-decision of each ledger entry, removes the decision ledger and rewrites the decisions index
Restates: r2@0.29, r6@0.29, r11@0.29, r16@0.29.
- [r28] While a decision ledger of this repository has a ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision of the ledger entry, remove the decision ledger, rewrite the decisions index of this repository and exit successfully.

```given
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions.md` holds:
  # Decisions
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
the tracked file `records/notes/one.md` holds:
  # one
  A note of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
```

### [g29] `migrate run` writes the design-decision of a ledger entry that another supersedes with the status `superseded`
Restates: r2@0.29.
- [r29] While a ledger entry supersedes another ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision of the ledger entry whose status is `superseded`.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/0008-b
  We do b instead.
  date: 2025-03-02
  source: bob
  supersedes: decision/0007-a
  revisit_when: the cart grows
```

### [g30] `migrate run` writes a design-decision that supersedes the design-decision of the ledger entry another supersedes
Restates: r2@0.29.
- [r30] While a ledger entry supersedes another ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision that supersedes a design-decision of the ledger entry.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/0008-b
  We do b instead.
  date: 2025-03-02
  source: bob
  supersedes: decision/0007-a
  revisit_when: the cart grows
```

### [g31] `migrate run` writes the qualifier of a supersedes in part into the design-decision that supersedes
Restates: r17@0.29.
- [r31] While a ledger entry that has a qualifier supersedes another ledger entry, when the person runs `migrate run` on a bounded context, `migrate` shall write a design-decision that holds the qualifier.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/0008-b
  We do b.
  date: 2025-03-02
  source: bob
  supersedes: decision/0007-a (in part)
```

### [g32] `migrate run` gives each ledger entry with no ledger number a ledger number
Restates: r13@0.29.
- [r32] While a ledger entry of a decision ledger has no ledger number, when the person runs `migrate run` on a bounded context, `migrate` shall give a ledger number to the ledger entry.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/b
  We do b.
  date: 2025-03-02
  source: bob
```

### [g33] `migrate run` gives each Behaviour line with no line id a line id
Restates: r10@0.29.
- [r33] While a Behaviour line of a capability has no line id, when the person runs `migrate run` on a bounded context, `migrate` shall give a line id to the Behaviour line.

```given
the tracked file `spec/capabilities/thing.md` holds:
  ---
  title: thing
  narrator: a client
  group: service
  rests_on: []
  retired: [r4]
  ---
  # thing
  ## Purpose
  Something.
  ## Behaviour
  - [r2] **When** a, `thing` shall a.
  - **When** b, `thing` shall b.
```

### [g34] `migrate run` refuses a ledger entry whose design-decision would take the place of a tracked file
Restates: r7@0.29.
- [r34] While a ledger entry has a stem and a tracked file in an old-layout directory has the same stem, if the person runs `migrate run` on a bounded context, then `migrate` shall refuse the command and name the tracked file.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
the tracked file `decisions/0007-a.md` holds:
  ---
  id: decision/0007-a
  status: accepted
  ---
  # a, already there
```

### [g35] `migrate run` refuses a repository with an uncommitted change, naming it
Restates: r15@0.29.
- [r35] While this repository holds an uncommitted change, if the person runs `migrate run` on a bounded context, then `migrate` shall refuse the command and name the uncommitted change.

```given
the tracked file `decisions/0001-a.md` holds "# a"
```

### [g36] `migrate upgrade` refuses a repository with an uncommitted change, naming it
Restates: r15@0.29.
- [r36] While this repository holds an uncommitted change, if the person runs `migrate upgrade`, then `migrate` shall refuse the command and name the uncommitted change.

```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g37] `migrate status` prints the release of a repository before 0.24.0 and every upgrade step
Restates: r18@0.29.
- [r37] While the release of this repository is before `0.24.0`, when the person runs `migrate status`, `migrate` shall print the release of this repository and every upgrade step and exit successfully.

```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g38] `migrate status` on a repository with a shop directory and no plugin version file prints every upgrade step, as on 0.23.1
Restates: r19@0.29.
- [r38] While this repository has a shop directory and this repository has no plugin version file, when the person runs `migrate status`, `migrate` shall print every upgrade step.

```given
the tracked file `.shop/records/.keep` holds "kept"
```

### [g39] `migrate status` refuses a plugin version file that holds no version, naming what it holds
Restates: r30@0.29.
- [r39] While a plugin version file of this repository holds no version, if the person runs `migrate status`, then `migrate` shall refuse the command and name the content of the plugin version file.

```given
the tracked file `.shop/plugin-version` holds "banana"
```

### [g40] `migrate upgrade` on a repository before 0.24.0 prints every upgrade step and rewrites the plugin version file
Restates: r20@0.29, r25@0.29, r26@0.29.
- [r40] While the release of this repository is before `0.24.0`, when the person runs `migrate upgrade`, `migrate` shall print every upgrade step and rewrite the plugin version file of this repository.

```given
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `.shop/plugin-version` holds "0.23.1"
the tracked file `.shop/work/i1/size-check.md` holds:
  ---
  id: work-item/example.org/acme/shop/size-check
  kind: work-item
  status: drafted
  ---
  # size-check
the tracked file `.shop/work/i1/runs/size-check/1-research/notes.md` holds "Notes."
the tracked file `.shop/work/i1/log.jsonl` holds:
  {"time": "t", "work-item": "size-check", "event": "start"}
```

### [g41] `migrate upgrade` on a repository before 0.24.0 renames every work-item file and stage directory to `w<n>` and rewrites every initiative log
Restates: r20@0.29, r25@0.29, r26@0.29.
- [r41] While the release of this repository is before `0.24.0`, when the person runs `migrate upgrade`, `migrate` shall rename every work-item file and every stage directory and rewrite every initiative log.

```given
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `.shop/plugin-version` holds "0.23.1"
the tracked file `.shop/work/i1/size-check.md` holds:
  ---
  id: work-item/example.org/acme/shop/size-check
  kind: work-item
  status: drafted
  ---
  # size-check
the tracked file `.shop/work/i1/runs/size-check/1-research/notes.md` holds "Notes."
the tracked file `.shop/work/i1/log.jsonl` holds:
  {"time": "t", "work-item": "size-check", "event": "start"}
```

### [g42] `migrate upgrade` on a repository on the plugin's release says that no upgrade step is pending and changes nothing
Restates: r27@0.29.
- [r42] While the release of this repository is `3.0.1`, when the person runs `migrate upgrade`, `migrate` shall print `no upgrade step is pending` and change no file.

```given
the tracked file `.shop/plugin-version` holds "3.0.1"
```

### [g43] `migrate upgrade` on a repository from 0.24.0 and before 0.25.0 rewrites every work-item file
Restates: r29@0.29.
- [r43] While the release of this repository is after `0.23.1` and before `0.25.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite every work-item file.

```given
the tracked file `.shop/plugin-version` holds "0.24.0"
the tracked file `.shop/work/i1/w1.md` holds:
  ---
  id: work-item/example.org/acme/shop/w1
  kind: work-item
  status: awaiting-ruling
  ---
  # w1
  ## Rulings
  - yes
```

### [g44] `migrate upgrade` on a repository before 1.0.0 writes the restated file and rewrites each capability with no language
- [r44] While the release of this repository is after `0.25.0` and before `1.0.0` and a capability of this repository has no language, when the person runs `migrate upgrade`, `migrate` shall write a restated file, rewrite the capability and print the restated file and the capability.

```given
the tracked file `.shop/plugin-version` holds "0.29.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/capabilities/cart.md` holds:
  ---
  id: capability/example.org/acme/shop/cart
  title: Cart
  retired: []
  ---
  # Cart
  ## Behaviour
  - [r1] **When** the shopper applies a code, `cart` shall take ten percent off.
the tracked file `features/cart.feature` holds:
  Feature: Cart
    @r1 @deprecated
    Scenario: a code takes ten percent off (deprecated)
      Given a cart
the tracked file `.shop/work/i1/w2.md` holds:
  ---
  id: work-item/example.org/acme/shop/w2
  kind: work-item
  accepts: [cart#r1]
  ---
  # w2
```

### [g57] `migrate upgrade` on a repository before 1.0.0 removes each scenario that has the `@deprecated` tag from its feature
- [r57] While the release of this repository is after `0.25.0` and before `1.0.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite every feature that holds a scenario that has the `@deprecated` tag.

```given
the tracked file `.shop/plugin-version` holds "0.29.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/capabilities/cart.md` holds:
  ---
  id: capability/example.org/acme/shop/cart
  title: Cart
  retired: []
  ---
  # Cart
  ## Behaviour
  - [r1] **When** the shopper applies a code, `cart` shall take ten percent off.
the tracked file `features/cart.feature` holds:
  Feature: Cart
    @r1 @deprecated
    Scenario: a code takes ten percent off (deprecated)
      Given a cart
the tracked file `.shop/work/i1/w2.md` holds:
  ---
  id: work-item/example.org/acme/shop/w2
  kind: work-item
  accepts: [cart#r1]
  ---
  # w2
```

### [g46] `migrate upgrade` on a repository before 1.0.0 writes each reference of a work-item file to a requirement with its release
- [r46] While the release of this repository is after `0.25.0` and before `1.0.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite every work-item file that mentions a requirement.

```given
the tracked file `.shop/plugin-version` holds "0.29.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/capabilities/cart.md` holds:
  ---
  id: capability/example.org/acme/shop/cart
  title: Cart
  retired: []
  ---
  # Cart
  ## Behaviour
  - [r1] **When** the shopper applies a code, `cart` shall take ten percent off.
the tracked file `features/cart.feature` holds:
  Feature: Cart
    @r1 @deprecated
    Scenario: a code takes ten percent off (deprecated)
      Given a cart
the tracked file `.shop/work/i1/w2.md` holds:
  ---
  id: work-item/example.org/acme/shop/w2
  kind: work-item
  accepts: [cart#r1]
  ---
  # w2
```

### [g47] the SessionStart hook tells a session to offer the upgrade steps of a repository before 0.24.0, and to run them only on the person's yes
Restates: r22@0.29.
- [r47] While the release of this repository is before `0.24.0`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print the release of this repository, every upgrade step and `only on the person's yes`.

```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g48] the SessionStart hook tells a session to tell the person to update the plugin
Restates: r23@0.29.
- [r48] While the release of this repository is after `3.0.1`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print `update the plugin`.

```given
the tracked file `.shop/plugin-version` holds "9.0.0"
```

### [g49] the SessionStart hook tells a session nothing on the plugin's release when no initiative is open
Restates: r24@0.29.
- [r49] While the release of this repository is `3.0.1` and every initiative of this repository is one of `done` or `abandoned`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit successfully, print no upgrade step and print no initiative.

```given
the tracked file `.shop/plugin-version` holds "3.0.1"
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  status: done
  ---
  # i1
```

### [g50] the SessionStart hook tells a session nothing in a repository with no shop directory
Restates: r28@0.29.
- [r50] While this repository has no shop directory, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit successfully.

```given
the tracked file `README.md` holds "No shop here."
```

### [g51] the SessionStart hook tells a session that the plugin version file holds no version
Restates: r31@0.29.
- [r51] While a plugin version file of this repository holds no version, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print `holds no version` and the content of the plugin version file.

```given
the tracked file `.shop/plugin-version` holds "banana"
```

### [g52] `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 writes the frozen notice and rewrites the decisions index
- [r52] While the release of this repository is after `0.29.0` and before `2.0.0`, when the person runs `migrate upgrade`, `migrate` shall write a frozen notice and rewrite the decisions index of this repository.

```given
the tracked file `.shop/plugin-version` holds "1.0.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions/0001-one.md` holds:
  ---
  id: design-decision/example.org/acme/shop/one
  summary: One decision.
  status: accepted
  tier: judgement
  ---
  # One
  ## Decision
  One.
the tracked file `spec/decisions/index.md` holds:
  # Decisions
  Written by hand, with no tier.
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  title: A cart
  status: started
  ---
  # i1
the tracked file `.shop/work/requests/q1.md` holds:
  ---
  id: request/example.org/acme/shop/q1
  kind: request
  asker: internal
  status: open
  turn: upstream
  ---
  # An intention
the tracked file `.shop/work/requests/q2.md` holds:
  ---
  id: request/example.org/acme/shop/q2
  kind: request
  asker: bounded-context/example.org/acme/web
  status: open
  turn: upstream
  ---
  # A peer's request
```

### [g53] `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 relocates each frozen request another bounded context asked that is not closed
- [r53] While the release of this repository is after `0.29.0` and before `2.0.0` and the asker of a frozen request is not `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person runs `migrate upgrade`, `migrate` shall relocate the frozen request.

```given
the tracked file `.shop/plugin-version` holds "1.0.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions/0001-one.md` holds:
  ---
  id: design-decision/example.org/acme/shop/one
  summary: One decision.
  status: accepted
  tier: judgement
  ---
  # One
  ## Decision
  One.
the tracked file `spec/decisions/index.md` holds:
  # Decisions
  Written by hand, with no tier.
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  title: A cart
  status: started
  ---
  # i1
the tracked file `.shop/work/requests/q1.md` holds:
  ---
  id: request/example.org/acme/shop/q1
  kind: request
  asker: internal
  status: open
  turn: upstream
  ---
  # An intention
the tracked file `.shop/work/requests/q2.md` holds:
  ---
  id: request/example.org/acme/shop/q2
  kind: request
  asker: bounded-context/example.org/acme/web
  status: open
  turn: upstream
  ---
  # A peer's request
```

### [g54] `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 names the upgrade step and each initiative that is not closed
- [r54] While the release of this repository is after `0.29.0` and before `2.0.0` and an initiative of this repository is not `done` or `abandoned`, when the person runs `migrate upgrade`, `migrate` shall print every upgrade step whose release is `2.0.0` and the initiative.

```given
the tracked file `.shop/plugin-version` holds "1.0.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions/0001-one.md` holds:
  ---
  id: design-decision/example.org/acme/shop/one
  summary: One decision.
  status: accepted
  tier: judgement
  ---
  # One
  ## Decision
  One.
the tracked file `spec/decisions/index.md` holds:
  # Decisions
  Written by hand, with no tier.
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  title: A cart
  status: started
  ---
  # i1
the tracked file `.shop/work/requests/q1.md` holds:
  ---
  id: request/example.org/acme/shop/q1
  kind: request
  asker: internal
  status: open
  turn: upstream
  ---
  # An intention
the tracked file `.shop/work/requests/q2.md` holds:
  ---
  id: request/example.org/acme/shop/q2
  kind: request
  asker: bounded-context/example.org/acme/web
  status: open
  turn: upstream
  ---
  # A peer's request
```

### [g55] `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 names each frozen request it asked of itself that is not closed
- [r55] While the release of this repository is after `0.29.0` and before `2.0.0` and the asker of a frozen request is `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person runs `migrate upgrade`, `migrate` shall print the frozen request.

```given
the tracked file `.shop/plugin-version` holds "1.0.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions/0001-one.md` holds:
  ---
  id: design-decision/example.org/acme/shop/one
  summary: One decision.
  status: accepted
  tier: judgement
  ---
  # One
  ## Decision
  One.
the tracked file `spec/decisions/index.md` holds:
  # Decisions
  Written by hand, with no tier.
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  title: A cart
  status: started
  ---
  # i1
the tracked file `.shop/work/requests/q1.md` holds:
  ---
  id: request/example.org/acme/shop/q1
  kind: request
  asker: internal
  status: open
  turn: upstream
  ---
  # An intention
the tracked file `.shop/work/requests/q2.md` holds:
  ---
  id: request/example.org/acme/shop/q2
  kind: request
  asker: bounded-context/example.org/acme/web
  status: open
  turn: upstream
  ---
  # A peer's request
```

### [g56] `migrate upgrade` on a repository from 2.0.0 and before 3.0.0 rewrites the index file with each term's part of speech and names each term that violates `v_t11`
- [r56] While the release of this repository is after `1.0.0` and before `3.0.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite the index file of this bounded context and print every upgrade step whose release is `3.0.0` and every term that violates `v_t11`.

```given
the tracked file `.shop/plugin-version` holds "2.0.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  language: codified-1
  ---
  # shop
  ## Glossary
  - **cart** (kind): the goods a shopper picks.
  - **shopper** (kind): a person who buys.
  - **pick** (event): a shopper puts goods in a cart. Forms: picks, picked.
```

## Implementation, may change
- r17's `by`: the entry's source, then `; supersedes <id> <qualifier>`.
- Python 3 with the standard library; it relocates with `git mv`; `migrate run` does not commit, `migrate upgrade`
  does. Every change is computed first, then written. A relocation onto a file that exists is a change it cannot make.
- The destinations under `.shop/records/` (archive, measurements, decision-arguments) and the record ids are
  design-decision/final-layout's; a decision file is `spec/decisions/<nnnn>-<name>.md` with an id, summary, date
  and status, and `spec/decisions/index.md` as `model decisions` writes it.
- `.shop/plugin-version` is one line holding the version. The plugin's SessionStart hook runs `migrate status` to
  learn what it tells the session.

- The relocations, each with `git mv`: `decisions/` to `spec/decisions/`, `work/` to `.shop/work/`, each
  `records/<x>` to `.shop/records/<x>`, `docs/superpowers/plans/` to `.shop/records/archive/plans/`,
  `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`, `docs/superpowers/requests/` to
  `.shop/records/archive/requests/` and `adrs/` to `.shop/records/decision-arguments/`. A relocated record with no
  `about` gets `about: bounded-context/<path>`.
- A ledger entry `## decision/<nnnn>-<slug>` becomes `spec/decisions/<nnnn>-<slug>.md`: its summary is the entry's
  first paragraph, its Decision the entry's whole text, its status `superseded` when another entry supersedes it and
  `accepted` otherwise, and its `date`, `by`, `supersedes` and `revisit_when` the entry's. An entry with no number is
  numbered in ledger order from one above the ledger's highest. The ledger is removed once it holds nothing but its
  entries and a title. `migrate run` adds every file it wrote or relocated to git and writes `spec/decisions/index.md`.
- Ids are `<kind>/<path>/<name>`, the name being the file's stem without a decision file's number: `capability`,
  `design-decision`, `initiative-archive` for a relocated plan or request, `decision-argument` for a relocated
  design note or ADR, and `measurement` for a relocated test log (`*-test-log.md`). Behaviour lines with no id are
  numbered in Behaviour order from one above the highest id the capability has used or retired.
- What `migrate run` relocates or renames is rewritten wherever a repository-relative path, a relative Markdown link
  or a frontmatter id names it, in every tracked text file.
- The 0.24.0 step "work-items named by ids" numbers work-items from 1 by their initiative's number and then their file
  name, renames each file to `w<n>.md` and `runs/<name>/` to `runs/w<n>/`, writes the id
  `work-item/<context path>/w<n>`, keeps or writes the heading, and rewrites the old name in `log.jsonl` and in every
  `blocked_by`, `depends_on` and `for`; free text in records is left as it is. The 0.25.0 step renames
  `awaiting-ruling` to `awaiting-answer` and `## Rulings` to `## Answers`.
- The 1.0.0 step "codified requirements" (`migrate_upgrade_codified.py`): when `spec/restated.json` is missing, it
  writes it from the live `[r<n>]` lines of each capability without `language: codified-1`, keyed `<cap>#r<n>` with the
  line's text (a table row's lead sentence and cells) and line number. Each such capability's Behaviour becomes one
  `### [g<n>]` group for each old line with `Restates: r<n>@0.29.` and the old text as an HTML comment, no requirement
  bullets and no marker; its `retired:` becomes `[]` and it gains `## Dropped`. A codified capability is left as it
  is. Every scenario tagged `@deprecated` in `features/` is deleted (a docstring's lines are text). Every
  `<cap>#r<n>` (bare, or `capability/[<context path>/]<cap>`) of a tracked file under `.shop/work/` becomes
  `<cap>#r<n>@0.29`, a range id by id: in every file when the step writes `spec/restated.json`, else in the lines a
  file had at the commit that added `spec/restated.json`. It prints, and the commit message lists, what is left for
  a session to write: each scaffolded capability, and the glossary of an index without `language: codified-1`.
- The 2.0.0 step "the workflow simplified" (`migrate_upgrade_simplified.py`): when `.shop/work/` exists, it writes
  `.shop/work/FROZEN.md`, which says that the queue of plugin 1.x is frozen and where items, batches and live requests
  are. Each request of `.shop/work/requests/` that is not closed (`open`, `awaiting-asker`, `awaiting-upstream`,
  `accepted`) and whose asker is neither `internal` nor this context is moved to `.shop/requests/` with `git mv`, its
  name and id unchanged; a destination that exists is a change it cannot make. When `spec/decisions/` exists, it
  rewrites `spec/decisions/index.md` as `model decisions` writes it. Nothing is deleted, and nothing else under
  `.shop/work/` changes. It prints, and the commit message lists, each initiative neither `done` nor `abandoned`, each
  capability- or glossary-proposal never applied, each internal request not closed, and each request moved. In the
  same upgrade as the 1.0.0 step, the 1.0.0 step's "left for a session to write" of a proposal under `.shop/work/` is
  dropped: the queue is frozen, and the 2.0.0 step's note names the proposal.
- `migrate upgrade` refuses, before it plans any step, when git has no author or committer identity
  (`git var GIT_AUTHOR_IDENT`, `GIT_COMMITTER_IDENT`), naming `git config user.name` and `user.email`.
- `migrate status` and `migrate upgrade` refuse a `.shop/plugin-version` that holds no version, naming an empty file
  as empty and otherwise what it holds; the SessionStart hook tells the session the same.

## Not yet
- `migrate plan` (a living plan to work-items and observations), `--dry-run`, and product-level repositories (see
  skeleton-notes.md).
- Upgrade steps for releases before 0.24.0, a repository before it being taken as 0.23.1 and earlier upgrades having
  been by hand — trigger: a repository on a release before 0.23.1 needs an upgrade.

## Dropped
- r3@0.29: the `@holding` tag is the old system's, and `migrate run` deprecated a held scenario through `features deprecate`, which is removed: the generator owns the feature files (the GF conversion's design §15), and the 1.0.0 upgrade deletes deprecated scenarios
- r32@0.29: retired with migration-tools#r22 in 2.0.0 (the-old-workflow-retired).
- r33@0.29: retired with migration-tools#r23 in 2.0.0 (the-old-workflow-retired).
- r34@0.29: retired with migration-tools#r23 in 2.0.0 (the-old-workflow-retired).
