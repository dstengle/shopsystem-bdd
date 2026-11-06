# generated from spec/capabilities/migration-tools.md by features generate; do not edit
Feature: Migration tools
  Narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases

  @g1 @r1
  Scenario: `migrate run` relocates the old layout with git, rewrites what names it and gives each file the id of its kind
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
    And the tracked file `docs/superpowers/plans/2025-01-01-cart.md` holds:
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
    And the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/shop
      title: shop
      ---
      # shop
      """
    And the tracked file `README.md` holds:
      """
      See [the note](records/notes/one.md) and work/i1-cart/initiative.md.
      """
    And the tracked file `spec/capabilities/thing.md` holds:
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
    And a repository r1
    And the repository r1 is unmigrated
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` relocates `decisions/`
    And `migrate` relocates `work/`
    And `migrate` relocates `records/`
    And `migrate` relocates `docs/superpowers/plans/`
    And `migrate` relocates `docs/superpowers/specs/`
    And `migrate` relocates `docs/superpowers/requests/`
    And `migrate` relocates `adrs/`
    And `migrate` rewrites `spec/index.md`
    And `migrate` rewrites `README.md`
    And `migrate` rewrites `spec/capabilities/thing.md`
    And `migrate` rewrites `spec/decisions/0001-a.md`

  @g2 @r2
  Scenario: `migrate run` replaces a ledger with one decision file for each entry, removes it, and leaves no unresolved reference
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
      # Decisions
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
    And a repository r1
    And the repository r1 is ledgered
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` relocates `spec/decisions.md`
    And `migrate` rewrites `spec/decisions/index.md`
    And `migrate` exits successfully

  @g3 @r3
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
    And a repository r1
    And the repository r1 is superseding
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/decisions/0007-a.md`
    And `migrate` rewrites `spec/decisions/0008-b.md`

  @g4 @r4
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
    And a repository r1
    And the repository r1 is qualified
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/decisions/0008-b.md`

  @g5 @r5
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
    And a repository r1
    And the repository r1 is numberless
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/decisions/0008-b.md`

  @g6 @r6
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
    And a repository r1
    And the repository r1 is idless
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` rewrites `spec/capabilities/thing.md`

  @g7 @r7
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
    And a repository r1
    And the repository r1 is conflicting
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` exits with an error naming `spec/decisions/0007-a.md`
    And `migrate` changes nothing

  @g8 @r8
  Scenario: `migrate run` refuses a repository with uncommitted changes, naming them
    Given the tracked file `decisions/0001-a.md` holds "# a"
    And an untracked file u1
    And the untracked file u1 is uncommitted
    When the person runs `migrate run --context example.org/acme/shop`
    Then `migrate` exits with an error naming the untracked file u1
    And `migrate` changes nothing

  @g9 @r9
  Scenario: `migrate upgrade` refuses a repository with uncommitted changes, naming them
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And an untracked file u1
    And the untracked file u1 is uncommitted
    When the person runs `migrate upgrade`
    Then `migrate` exits with an error naming the untracked file u1
    And `migrate` changes nothing

  @g10 @r10
  Scenario: `migrate status` prints both versions and each pending upgrade step
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And a repository r1
    And the repository r1 is behind
    When the person runs `migrate status`
    Then `migrate` prints "0.23.1"
    And `migrate` prints "0.24.0"
    And `migrate` prints "work-items named by ids"
    And `migrate` exits successfully

  @g11 @r11
  Scenario: a repository with `.shop/` and no `.shop/plugin-version` is on 0.23.1
    Given the tracked file `.shop/records/.keep` holds "kept"
    And a repository r1
    And the repository r1 is unversioned
    When the person runs `migrate status`
    Then `migrate` prints "0.23.1"

  @g12 @r12
  Scenario: `migrate status` refuses a `.shop/plugin-version` that holds no version, naming what it holds
    Given the tracked file `.shop/plugin-version` holds "banana"
    And a repository r1
    And the repository r1 is misversioned
    When the person runs `migrate status`
    Then `migrate` exits with an error naming "banana"
    And `migrate` changes nothing

  @g13 @r13
  Scenario: `migrate upgrade` applies each pending step in one commit: work-items are named `w<n>` with their files and stage directories
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
    And a repository r1
    And the repository r1 is behind
    When the person runs `migrate upgrade`
    Then `migrate` rewrites `.shop/plugin-version`
    And `migrate` prints "work-items named by ids"
    And `migrate` prints "answers, not rulings"
    And `migrate` renames `.shop/work/i1/size-check.md`
    And `migrate` renames `.shop/work/i1/runs/size-check/`
    And `migrate` rewrites `.shop/work/i1/log.jsonl`

  @g14 @r14
  Scenario: `migrate upgrade` with no pending step says so and changes nothing
    Given the tracked file `.shop/plugin-version` holds "2.3.1"
    And a repository r1
    And the repository r1 is current
    When the person runs `migrate upgrade`
    Then `migrate` prints "no upgrade step is pending"
    And `migrate` changes nothing

  @g15 @r15
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
    And a repository r1
    And the repository r1 is outdated
    When the person runs `migrate upgrade`
    Then `migrate` rewrites `.shop/work/i1/w1.md`

  @g16 @r16
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
    And a repository r1
    And the repository r1 is uncodified
    When the person runs `migrate upgrade`
    Then `migrate` prints "spec/restated.json"
    And `migrate` prints "spec/capabilities/cart.md"
    And `migrate` rewrites `spec/capabilities/cart.md`
    And `migrate` rewrites `features/cart.feature`
    And `migrate` rewrites `.shop/work/i1/w2.md`

  @g17 @r17
  Scenario: the SessionStart hook tells a session to offer a pending upgrade, and to run it only on the person's yes
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And a repository r1
    And the repository r1 is behind
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "0.23.1"
    And `migrate` prints "work-items named by ids"
    And `migrate` prints "only on the person's yes"

  @g18 @r18
  Scenario: the SessionStart hook tells a session to tell the person to update the plugin
    Given the tracked file `.shop/plugin-version` holds "9.0.0"
    And a repository r1
    And the repository r1 is ahead
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "update the plugin"

  @g19 @r19
  Scenario: the SessionStart hook tells a session nothing when nothing is pending and no initiative is open
    Given the tracked file `.shop/plugin-version` holds "2.3.1"
    And the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: done
      ---
      # i1
      """
    And a repository r1
    And the repository r1 is idle
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` exits successfully
    And `migrate` does not print "migrate upgrade"
    And `migrate` does not print "i1"

  @g20 @r20
  Scenario: the SessionStart hook tells a session nothing in a repository without `.shop/`
    Given the tracked file `README.md` holds "No shop here."
    And a repository r1
    And the repository r1 is shopless
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` exits successfully

  @g21 @r21
  Scenario: the SessionStart hook tells a session that `.shop/plugin-version` holds no version
    Given the tracked file `.shop/plugin-version` holds "banana"
    And a repository r1
    And the repository r1 is misversioned
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints "holds no version"
    And `migrate` prints "banana"

  @g24 @r24
  Scenario: the upgrade step "the workflow simplified" freezes `.shop/work/`, moves the live requests to `.shop/requests/` and writes the decisions index
    Given the tracked file `.shop/plugin-version` holds "1.0.0"
    And the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/example.org/acme/shop
      title: shop
      ---
      # shop
      """
    And the tracked file `spec/decisions/0001-one.md` holds:
      """
      ---
      id: design-decision/example.org/acme/shop/one
      summary: One decision.
      status: accepted
      tier: judgement
      ---
      # One
      ## Decision
      One.
      """
    And the tracked file `spec/decisions/index.md` holds:
      """
      # Decisions
      Written by hand, with no tier.
      """
    And the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      title: A cart
      status: started
      ---
      # i1
      """
    And the tracked file `.shop/work/requests/q1.md` holds:
      """
      ---
      id: request/example.org/acme/shop/q1
      kind: request
      asker: internal
      status: open
      turn: upstream
      ---
      # An intention
      """
    And the tracked file `.shop/work/requests/q2.md` holds:
      """
      ---
      id: request/example.org/acme/shop/q2
      kind: request
      asker: bounded-context/example.org/acme/web
      status: open
      turn: upstream
      ---
      # A peer's request
      """
    And a repository r1
    And the repository r1 is queued
    When the person runs `migrate upgrade`
    Then `migrate` writes `.shop/work/FROZEN.md`
    And `migrate` renames `.shop/work/requests/q2.md`
    And `migrate` rewrites `spec/decisions/index.md`
    And `migrate` prints "the workflow simplified"
    And `migrate` prints "i1"
    And `migrate` prints "q1"
