---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/upgrades
title: Upgrades
narrator: the person
group: service
area: upgrades
specifies: service upgrades
language: codified-2
retired: [g31, r31, g38, r38, g40, r40, g39, r39]
unbuilt: []
---

# Upgrades

## Purpose
A repository moved between plugin releases: its release queried, its upgrade steps applied, a bounded context relocated
to the final layout.

## Behaviour

### [g1] Relocating a bounded context moves every old-layout directory
Restates: migration-tools#r1@0.29, migration-tools#r4@0.29, migration-tools#r5@0.29, migration-tools#r8@0.29, migration-tools#r9@0.29, migration-tools#r12@0.29, migration-tools#r14@0.29.
- [r1] While this repository holds an old-layout directory, when the person relocates a bounded context, the upgrades
  service shall change every old-layout directory and every file that mentions an old-layout directory.
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

### [g2] Relocating a bounded context turns its decision ledger into design-decisions
Restates: migration-tools#r2@0.29, migration-tools#r6@0.29, migration-tools#r11@0.29, migration-tools#r16@0.29.
- [r2] While a decision ledger of this repository has a ledger entry, when the person relocates a bounded context, the
  upgrades service shall keep a design-decision of the ledger entry, keep no decision ledger, change the decisions index
  of this repository and complete the request.
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

### [g3] A superseded ledger entry becomes a superseded design-decision
Restates: migration-tools#r2@0.29.
- [r3] While a ledger entry supersedes another ledger entry, when the person relocates a bounded context, the upgrades
  service shall keep a design-decision of the ledger entry whose status is `superseded` and keep another design-decision
  that supersedes the design-decision.
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

### [g4] A superseding ledger entry's qualifier is kept
Restates: migration-tools#r17@0.29.
- [r4] While a ledger entry that has a qualifier supersedes another ledger entry, when the person relocates a bounded
  context, the upgrades service shall keep a design-decision that holds the qualifier.
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

### [g5] A ledger entry with no number is given one
Restates: migration-tools#r13@0.29.
- [r5] While a ledger entry of a decision ledger has no ledger number, when the person relocates a bounded context, the
  upgrades service shall keep a ledger number of the ledger entry.
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

### [g6] A Behaviour line with no id is given one
Restates: migration-tools#r10@0.29.
- [r6] While a Behaviour line of a capability has no line id, when the person relocates a bounded context, the upgrades
  service shall keep a line id of the Behaviour line.
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

### [g7] A bounded context whose ledger stem clashes with a tracked file is not relocated
Restates: migration-tools#r7@0.29.
- [r7] While a ledger entry has a stem and a tracked file in an old-layout directory has the same stem, if the person
  relocates a bounded context, then the upgrades service shall refuse the request and name the tracked file.
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

### [g8] No bounded context is relocated with an uncommitted change
Restates: migration-tools#r15@0.29.
- [r8] While this repository holds an uncommitted change, if the person relocates a bounded context, then the upgrades
  service shall refuse the request and name the uncommitted change.
```given
the tracked file `decisions/0001-a.md` holds "# a"
```

### [g9] No repository is upgraded with an uncommitted change
Restates: migration-tools#r15@0.29.
- [r9] While this repository holds an uncommitted change, if the person upgrades this repository, then the upgrades
  service shall refuse the request and name the uncommitted change.
```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g10] A query before 0.24.0 gives the release and every upgrade step
Restates: migration-tools#r18@0.29.
- [r10] While the release of this repository is before `0.24.0`, when the person queries this repository, the upgrades
  service shall return the release of this repository and every upgrade step and complete the request.
```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g11] A query with no plugin version file gives every upgrade step
Restates: migration-tools#r19@0.29.
- [r11] While this repository has a shop directory and this repository has no plugin version file, when the person
  queries this repository, the upgrades service shall return every upgrade step.
```given
the tracked file `.shop/records/.keep` holds "kept"
```

### [g12] A query of a plugin version file with no version is refused
Restates: migration-tools#r30@0.29.
- [r12] While a plugin version file of this repository holds no version, if the person queries this repository, then the
  upgrades service shall refuse the request and name the content of the plugin version file.
```given
the tracked file `.shop/plugin-version` holds "banana"
```

### [g13] An upgrade before 0.24.0 renames the work-item files and stage directories
Restates: migration-tools#r20@0.29, migration-tools#r25@0.29, migration-tools#r26@0.29.
- [r13] While the release of this repository is before `0.24.0`, when the person upgrades this repository, the upgrades
  service shall return every upgrade step and change the plugin version file of this repository, every work-item file,
  every stage directory and every initiative log.
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

### [g14] An upgrade from 0.24 rewrites every work-item file
Restates: migration-tools#r29@0.29.
- [r14] While the release of this repository is after `0.23.1` and before `0.25.0`, when the person upgrades this
  repository, the upgrades service shall change every work-item file.
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

### [g15] An upgrade to 0.30.0 restates a capability with no language
- [r15] While the release of this repository is after `0.25.0` and before `0.30.0` and a capability of this repository
  has no language, when the person upgrades this repository, the upgrades service shall keep a restated file, change the
  capability and return the restated file and the capability.
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

### [g16] An upgrade to 0.30.0 rewrites old references and deprecated scenarios
- [r16] While the release of this repository is after `0.25.0` and before `0.30.0`, when the person upgrades this
  repository, the upgrades service shall change every work-item file that mentions a requirement and change every
  feature that holds a scenario that has the `@deprecated` tag.
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

### [g17] A session that starts before 0.24.0 is told the release and the upgrade steps
Restates: migration-tools#r22@0.29.
- [r17] While the release of this repository is before `0.24.0`, when a session starts, the upgrades service shall
  notify the session of the release of this repository, every upgrade step and `only on the person's yes`.
```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g18] A session that starts with no shop directory is told nothing
Restates: migration-tools#r28@0.29.
- [r18] While this repository has no shop directory, when a session starts, the upgrades service shall change nothing.
```given
the tracked file `README.md` holds "No shop here."
```

### [g19] A session that starts with a plugin version file of no version is told so
Restates: migration-tools#r31@0.29.
- [r19] While a plugin version file of this repository holds no version, when a session starts, the upgrades service
  shall notify the session of `holds no version` and the content of the plugin version file.
```given
the tracked file `.shop/plugin-version` holds "banana"
```

### [g20] An upgrade to 0.31.0 freezes the work queue
- [r20] While the release of this repository is after `0.29.0` and before `0.31.0`, when the person upgrades this
  repository, the upgrades service shall keep a frozen notice and change the decisions index of this repository.
```given
the tracked file `.shop/plugin-version` holds "0.30.0"
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

### [g21] An upgrade to 0.31.0 relocates each live frozen request of another asker
- [r21] While the release of this repository is after `0.29.0` and before `0.31.0` and the asker of a frozen request is
  not `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person upgrades this
  repository, the upgrades service shall change the frozen request.
```given
the tracked file `.shop/plugin-version` holds "0.30.0"
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

### [g22] An upgrade to 0.31.0 names each open initiative
- [r22] While the release of this repository is after `0.29.0` and before `0.31.0` and an initiative of this repository
  is not `done` or `abandoned`, when the person upgrades this repository, the upgrades service shall return every
  upgrade step whose release is `0.31.0` and the initiative.
```given
the tracked file `.shop/plugin-version` holds "0.30.0"
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

### [g23] An upgrade to 0.31.0 names each live internal frozen request
- [r23] While the release of this repository is after `0.29.0` and before `0.31.0` and the asker of a frozen request is
  `internal` and the frozen request is not `delivered`, `refused` or `withdrawn`, when the person upgrades this
  repository, the upgrades service shall return the frozen request.
```given
the tracked file `.shop/plugin-version` holds "0.30.0"
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

### [g24] An upgrade to 0.32.0 names each term that violates v_t11
- [r24] While the release of this repository is after `0.30.0` and before `0.32.0`, when the person upgrades this
  repository, the upgrades service shall change the index file of this bounded context and return every upgrade step
  whose release is `0.32.0` and every term that violates `v_t11`.
```given
the tracked file `.shop/plugin-version` holds "0.31.0"
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

### [g25] An upgrade to 0.33.0 rewrites the index file and every capability
- [r25] While the release of this repository is after `0.32.0` and before `0.33.0`, when the person upgrades this
  repository, the upgrades service shall change the index file of this bounded context and every capability and return
  every upgrade step whose release is `0.33.0`.
```given
the tracked file `.shop/plugin-version` holds "0.32.1"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  language: codified-1
  ---
  # shop
  ## Glossary
  - **cart** (noun): the goods a shopper picks.
  - **shopper** (noun): a person who buys.
  - **pick** (verb): a shopper puts goods in a cart. Forms: picks, picked. Frame: shopper picks cart.
the tracked file `spec/capabilities/cart.md` holds:
  ---
  id: capability/example.org/acme/shop/cart
  title: Cart
  language: codified-1
  retired: []
  unbuilt: []
  ---
  # Cart
  ## Behaviour
  ### [g1] picking
  - [r1] When a shopper picks a cart, the shopper shall pick the cart.
```

### [g26] An upgrade to 0.34.0 names each term that violates w_value_kind
- [r26] While the release of this repository is `0.33.0`, when the person upgrades this repository, the upgrades service
  shall return every upgrade step whose release is `0.34.0` and every term that violates `w_value_kind`.
```given
the tracked file `.shop/plugin-version` holds "0.33.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  language: codified-2
  ---
  # shop
  ## Glossary
  - **cart** (noun): the goods a shopper picks.
  - **status** (attribute of cart): Values: `open`, `paid`.
```

### [g27] An upgrade at the plugin's release changes nothing
Restates: migration-tools#r27@0.29.
- [r27] While the release of this repository is the same as the release of the plugin and the release of this repository
  is after `0.34.0`, when the person upgrades this repository, the upgrades service shall return `no upgrade step is
  pending` and change no file.

### [g28] A session that starts after the plugin's release is told to update the plugin
Restates: migration-tools#r23@0.29.
- [r28] While the release of this repository is after the release of the plugin, when a session starts, the upgrades
  service shall notify the session of `update the plugin`.

### [g29] A session that starts at the plugin's release with no open initiative is told nothing
Restates: migration-tools#r24@0.29.
- [r29] While the release of this repository is the same as the release of the plugin and the release of this repository
  is after `0.24.0` and every initiative of this repository is one of `done` or `abandoned`, when a session starts, the
  upgrades service shall not notify the session of an upgrade step and not notify the session of an initiative.
```given
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  status: done
  ---
  # i1
```

### [g30] An upgrade at a patch release keeps the new plugin version
- [r30] While the release of this repository is `0.34.0` and the release of the plugin is `0.34.1`, when the person
  upgrades this repository, the upgrades service shall return `no upgrade step is pending`, change the plugin version
  file of this repository and keep the plugin version file.

### [g32] A bounded context is not founded without a context id
- [r32] If the person founds this bounded context without a context id, then the upgrades service shall refuse the request and name this bounded context.

### [g33] A bounded context is not founded with a context id that is no bounded context id
- [r33] If the person founds this bounded context with a context id that does not conform to the bounded context id form, then the upgrades service shall refuse the request and name the context id.

### [g34] A bounded context that has an index file is not founded and nothing changes
- [r34] While this bounded context has an index file, if the person founds this bounded context with a context id, then the upgrades service shall refuse the request, name the index file and change no file.

```given
the tracked file `spec/index.md` holds "# notes"
```

### [g35] A repository that has a shop directory is not founded on and nothing changes
- [r35] While this repository has a shop directory, if the person founds this bounded context with a context id, then the upgrades service shall refuse the request, name the shop directory and change no file.

```given
the tracked file `.shop/backlog/b1.md` holds "# b1"
```

### [g36] An upgrade rewrites a scenario conftest of the old form
- [r36] While the release of this repository is before the release of the plugin and the scenario conftest of this repository conforms to the old scenario conftest form, when the person upgrades this repository, the upgrades service shall change the scenario conftest of this repository and keep the scenario conftest.

### [g37] An upgrade names a scenario conftest of neither form and leaves it alone
- [r37] While the release of this repository is before the release of the plugin and the scenario conftest of this repository does not conform to the old scenario conftest form and the scenario conftest of this repository does not conform to the scenario conftest form, when the person upgrades this repository, the upgrades service shall return the scenario conftest and not change the scenario conftest.

### [g41] Founding a bounded context with a context purpose writes it in the index file
- [r41] While this bounded context has no index file and this repository has no shop directory, when the person founds this bounded context with a context id and a context purpose, the upgrades service shall keep an index file that has the context purpose and complete the request.

### [g43] Founding a bounded context leaves an ignore file that conforms as git reads it alone
- [r43] While this bounded context has no index file and this repository has no shop directory and the ignore file of this repository conforms to the ignore file form, when the person founds this bounded context with a context id, the upgrades service shall keep the context scaffold, not change the ignore file and complete the request.

```given
the tracked file `.gitignore` holds:
  .venv
  __pycache__
  .pytest_cache/
  .ruff_cache
```

### [g42] Founding a bounded context adds a name an anchored entry covers only at the top
- [r42] While this bounded context has no index file and this repository has no shop directory and the ignore file of this repository does not conform to the ignore file form, when the person founds this bounded context with a context id, the upgrades service shall change the ignore file of this repository, keep the context scaffold and the ignore file of this repository and complete the request.

```given
the tracked file `.gitignore` holds:
  .venv/
  /__pycache__/
  .pytest_cache/
  .ruff_cache/
```

### [g44] An upgrade rewrites an old command line of an instructions file
- [r44] While the release of this repository is before the release of the plugin and an instructions file of this repository holds an old command line, when the person upgrades this repository, the upgrades service shall change the old command line and keep the instructions file.

### [g45] A bounded context founded imports the base pack
- [r45] While this bounded context has no index file and this repository has no shop directory, when the person founds this bounded context with a context id, the upgrades service shall keep a bounded context that imports the `base` pack and complete the request.

### [g46] A bounded context founded on a branch other than the base branch names the branch
- [r46] While the branch differs from the base branch and this bounded context has no index file and this repository has no shop directory, when the person founds this bounded context with a context id, the upgrades service shall keep the context scaffold of this repository, name the branch and complete the request.

### [g47] An upgrade to 0.45.0 names each term and transition the stricter rules fail and rewrites the Composition
- [r47] While the release of this repository is after `0.34.0` and before `0.45.0` and the release of this repository is before the release of the plugin, when the person upgrades this repository, the upgrades service shall change the index file of this bounded context and return every term that violates `v_t13`, every term that violates `v_t22` and every transition that violates `v_m9`.

```given
the tracked file `.shop/plugin-version` holds "0.44.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  language: codified-2
  ---
  # shop
  ## Composition
  ### Areas
  - cart: the goods a shopper picks.
```

