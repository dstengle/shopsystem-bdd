# generated from spec/capabilities/migration-tools.md by features generate; do not edit
Feature: Migration tools
  Narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases

  @g1 @r1 @r2 @r3
  Scenario: `migrate run` relocates `decisions/`, `work/` and each `records/<x>`, with git
    Given the tracked file `decisions/0001-a.md` holds:
      """
      ---
      id: decision/0001-a
      status: accepted
      ---
      # a
      """
    And the tracked file `work/i1-cart/initiative.md` holds:
      """
      ---
      id: initiative/i1-cart
      status: done
      ---
      """
    And the tracked file `records/notes/one.md` holds:
      """
      # one
      A note of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      And a third line.
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` relocates `decisions/`
    And `migrate` relocates `work/`
    And `migrate` relocates `records/`

  @g2 @r4 @r5 @r6 @r7
  Scenario: `migrate run` relocates `docs/superpowers/` and `adrs/` under `.shop/records/`, with git, each about the context
    Given the tracked file `docs/superpowers/plans/2025-01-01-cart.md` holds:
      """
      # The cart plan
      A plan of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      """
    And the tracked file `docs/superpowers/specs/2025-01-01-cart-design.md` holds:
      """
      # The cart design
      A design note of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      """
    And the tracked file `docs/superpowers/requests/2025-01-02-pay.md` holds:
      """
      # Pay
      A request of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      """
    And the tracked file `adrs/0001-use-git.md` holds:
      """
      # Use git
      An ADR of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` relocates `docs/superpowers/plans/`
    And `migrate` relocates `docs/superpowers/specs/`
    And `migrate` relocates `docs/superpowers/requests/`
    And `migrate` relocates `adrs/`

  @g3 @r8 @r9
  Scenario: `migrate run` replaces a ledger with one decision file for each entry, and removes it
    Given the tracked file `spec/decisions.md` holds:
      """
      # Decisions
      ## decision/0007-a
      We do a.
      date: 2025-03-01
      source: alice
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` relocates `spec/decisions.md`
    And `migrate` rewrites `spec/decisions/index.md`

  @g4 @r10 @r11
  Scenario: `migrate run` gives a decision file its entry's supersedes, and the entry it supersedes the status `superseded`
    Given the tracked file `spec/decisions.md` holds:
      """
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
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/decisions/0007-a.md`
    And `migrate` rewrites `spec/decisions/0008-b.md`

  @g5 @r12
  Scenario: `migrate run` writes a qualified supersedes as the decision's id alone, the qualifier going to `by`
    Given the tracked file `spec/decisions.md` holds:
      """
      ## decision/0007-a
      We do a.
      date: 2025-03-01
      source: alice
      ## decision/0008-b
      We do b.
      date: 2025-03-02
      source: bob
      supersedes: decision/0007-a (in part)
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/decisions/0008-b.md`

  @g6 @r13
  Scenario: `migrate run` numbers each ledger entry with no number from one above the ledger's highest
    Given the tracked file `spec/decisions.md` holds:
      """
      ## decision/0007-a
      We do a.
      date: 2025-03-01
      source: alice
      ## decision/b
      We do b.
      date: 2025-03-02
      source: bob
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/decisions/0008-b.md`

  @g7 @r14
  Scenario: `migrate run` gives `spec/index.md` the id `bounded-context/<path>`
    Given the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/shop
      title: shop
      ---
      # shop
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/index.md`

  @g8 @r15
  Scenario: `migrate run` rewrites each path, link and id that names what it relocated or renamed
    Given the tracked file `README.md` holds:
      """
      See [the note](records/notes/one.md) and work/i1-cart/initiative.md.
      """
    And the tracked file `records/notes/one.md` holds:
      """
      # one
      A note of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      """
    And the tracked file `work/i1-cart/initiative.md` holds:
      """
      ---
      id: initiative/i1-cart
      status: done
      ---
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `README.md`

  @g9 @r16 @r17
  Scenario: `migrate run` gives a capability, a decision file and a relocated record the type-first id of its kind
    Given the tracked file `spec/capabilities/thing.md` holds:
      """
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
      """
    And the tracked file `decisions/0001-a.md` holds:
      """
      ---
      id: decision/0001-a
      status: accepted
      ---
      # a
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/capabilities/thing.md`
    And `migrate` rewrites `spec/decisions/0001-a.md`

  @g10 @r18
  Scenario: `migrate run` numbers each Behaviour line with no id from one above the highest its capability has used
    Given the tracked file `spec/capabilities/thing.md` holds:
      """
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
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/capabilities/thing.md`

  @g11 @r19
  Scenario: after `migrate run`, `model check` prints no unresolved reference or file problem
    Given the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/shop
      title: shop
      ---
      # shop
      """
    And the tracked file `spec/decisions.md` holds:
      """
      ## decision/0007-a
      We do a.
      date: 2025-03-01
      source: alice
      """
    And the tracked file `records/notes/one.md` holds:
      """
      # one
      A note of the old system, long enough that git sees the rename after migrate adds an id.
      It has a second line.
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` exits successfully

  @g12 @r20
  Scenario: `migrate run` that cannot make every change names it and changes no file
    Given the tracked file `spec/decisions.md` holds:
      """
      ## decision/0007-a
      We do a.
      date: 2025-03-01
      source: alice
      """
    And the tracked file `decisions/0007-a.md` holds:
      """
      ---
      id: decision/0007-a
      status: accepted
      ---
      # a, already there
      """
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` exits with an error naming `spec/decisions/0007-a.md`
    And `migrate` changes nothing

  @g13 @r21
  Scenario: `migrate run` refuses a repository with uncommitted changes, naming them
    Given the tracked file `decisions/0001-a.md` holds "# a"
    And the untracked file `notes.md` holds "not committed"
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` exits with an error naming the untracked file `notes.md`
    And `migrate` changes nothing

  @g14 @r22
  Scenario: `migrate upgrade` refuses a repository with uncommitted changes, naming them
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And the untracked file `notes.md` holds "not committed"
    When the person runs `migrate upgrade`
    Then `migrate` exits with an error naming the untracked file `notes.md`
    And `migrate` changes nothing

  @g15 @r23 @r24
  Scenario: `migrate status` prints both versions and each pending upgrade step
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    When the person runs `migrate status`
    Then `migrate` prints "0.23.1", "0.24.0" and "work-items named by ids"
    And `migrate` exits successfully

  @g16 @r25
  Scenario: a repository with `.shop/` and no `.shop/plugin-version` is on 0.23.1
    Given the tracked file `.shop/records/.keep` holds "kept"
    When the person runs `migrate status`
    Then `migrate` prints "0.23.1"

  @g17 @r26 @r27
  Scenario: `migrate upgrade` applies each pending step, writes the plugin's version and commits it all in one commit
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    When the person runs `migrate upgrade`
    Then `migrate` rewrites `.shop/plugin-version`
    And `migrate` prints "work-items named by ids" and "answers, not rulings"

  @g18 @r28 @r29
  Scenario: `migrate upgrade` with no pending step says so and changes nothing
    Given the tracked file `.shop/plugin-version` holds "1.0.0"
    When the person runs `migrate upgrade`
    Then `migrate` prints "no upgrade step is pending"
    And `migrate` changes nothing

  @g19 @r30
  Scenario: `migrate status` refuses a `.shop/plugin-version` that holds no version, naming what it holds
    Given the tracked file `.shop/plugin-version` holds "banana"
    When the person runs `migrate status`
    Then `migrate` exits with an error naming "banana"
    And `migrate` changes nothing

  @g20 @r31 @r32 @r33
  Scenario: the upgrade step "work-items named by ids" names each work-item `w<n>` and renames its file and stage directories
    Given the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/example.org/acme/shop
      title: shop
      ---
      # shop
      """
    And the tracked file `.shop/plugin-version` holds "0.23.1"
    And the tracked file `.shop/work/i1/size-check.md` holds:
      """
      ---
      id: work-item/example.org/acme/shop/size-check
      kind: work-item
      status: drafted
      ---
      # size-check
      """
    And the tracked file `.shop/work/i1/runs/size-check/1-research/notes.md` holds "Notes."
    And the tracked file `.shop/work/i1/log.jsonl` holds:
      """
      {"time": "t", "work-item": "size-check", "event": "start"}
      """
    When the person runs `migrate upgrade`
    Then `migrate` renames `.shop/work/i1/size-check.md`
    And `migrate` renames `.shop/work/i1/runs/size-check/`
    And `migrate` rewrites `.shop/work/i1/log.jsonl`

  @g21 @r34
  Scenario: the upgrade step after 0.24.0 renames `awaiting-ruling` to `awaiting-answer` and `## Rulings` to `## Answers`
    Given the tracked file `.shop/plugin-version` holds "0.24.0"
    And the tracked file `.shop/work/i1/w1.md` holds:
      """
      ---
      id: work-item/example.org/acme/shop/w1
      kind: work-item
      status: awaiting-ruling
      ---
      # w1
      ## Rulings
      - yes
      """
    When the person runs `migrate upgrade`
    Then `migrate` rewrites `.shop/work/i1/w1.md`

  @g22 @r35
  Scenario: the SessionStart hook tells a session to offer a pending upgrade, and to run it only on the person's yes
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "0.23.1", "work-items named by ids" and "only on the person's yes"

  @g23 @r36
  Scenario: the SessionStart hook tells a session to tell the person to update the plugin
    Given the tracked file `.shop/plugin-version` holds "9.0.0"
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "update the plugin"

  @g24 @r46 @r47
  Scenario: the SessionStart hook tells a session nothing when nothing is pending and no initiative is open
    Given the tracked file `.shop/plugin-version` holds "1.0.0"
    And the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: done
      ---
      # i1
      """
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` does not print "migrate upgrade"
    And `migrate` does not print "i1"

  @g25 @r48
  Scenario: the SessionStart hook tells a session nothing in a repository without `.shop/`
    Given the tracked file `README.md` holds "No shop here."
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` exits successfully

  @g26 @r49
  Scenario: the SessionStart hook tells a session that `.shop/plugin-version` holds no version
    Given the tracked file `.shop/plugin-version` holds "banana"
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "holds no version" and "banana"

  @g27 @r50
  Scenario: the SessionStart hook gives a session what `work status` prints for each open initiative
    Given the tracked file `.shop/plugin-version` holds "1.0.0"
    And the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: started
      ---
      # i1
      """
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "initiative i1"

  @g28 @r51 @r52
  Scenario: the PreCompact hook appends `compacted` to the ledger of each open initiative and tells the session to hand off
    Given the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: started
      ---
      # i1
      """
    And the tracked file `.shop/work/i1/ledger.md` holds "- 2026-01-02: began"
    When the PreCompact hook runs `migrate compacting`
    Then `migrate` appends "compacted"
    And `migrate` prints "work note" and "instead of being compacted"

  @g29 @r53 @r54 @r55 @r56
  Scenario: the upgrade step "codified requirements" writes `spec/restated.json`, scaffolds each uncodified capability, deletes deprecated scenarios and writes old references with their release
    Given the tracked file `.shop/plugin-version` holds "0.29.0"
    And the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/example.org/acme/shop
      title: shop
      ---
      # shop
      """
    And the tracked file `spec/capabilities/cart.md` holds:
      """
      ---
      id: capability/example.org/acme/shop/cart
      title: Cart
      retired: []
      ---
      # Cart
      ## Behaviour
      - [r1] **When** the shopper applies a code, `cart` shall take ten percent off.
      """
    And the tracked file `features/cart.feature` holds:
      """
      Feature: Cart
        @r1 @deprecated
        Scenario: a code takes ten percent off (deprecated)
          Given a cart
      """
    And the tracked file `.shop/work/i1/w2.md` holds:
      """
      ---
      id: work-item/example.org/acme/shop/w2
      kind: work-item
      accepts: [cart#r1]
      ---
      # w2
      """
    When the person runs `migrate upgrade`
    Then `migrate` prints "spec/restated.json" and "spec/capabilities/cart.md"
    And `migrate` rewrites `spec/capabilities/cart.md`
    And `migrate` rewrites `features/cart.feature`
    And `migrate` rewrites `.shop/work/i1/w2.md`
