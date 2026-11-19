# generated from spec/capabilities/upgrades.md by features generate; do not edit
Feature: Upgrades
  Narrator: the person

  @g1 @r1
  Scenario: Relocating a bounded context moves every old-layout directory
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
    And an old-layout directory o1
    And this repository holds the old-layout directory o1
    And a bounded context b1
    And an old-layout directory o2
    And an old-layout directory o3
    And a file f1
    And an old-layout directory o4
    And the file f1 mentions the old-layout directory o4
    And a file f2
    And an old-layout directory o5
    And the file f2 mentions the old-layout directory o5
    And a file f3
    And an old-layout directory o6
    And the file f3 does not mention the old-layout directory o6
    When the person relocates the bounded context b1
    Then the upgrades service changes the old-layout directory o2
    And the upgrades service changes the old-layout directory o3
    And the upgrades service changes the file f1
    And the upgrades service changes the file f2
    And the upgrades service does not change the file f3

  @g2 @r2
  Scenario: Relocating a bounded context turns its decision ledger into design-decisions
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
    And a decision ledger d1
    And this repository has the decision ledger d1
    And a ledger entry l1
    And the decision ledger d1 has the ledger entry l1
    And a bounded context b1
    When the person relocates the bounded context b1
    Then the upgrades service keeps the design-decision d2
    And the ledger entry l1 has the design-decision d2
    And the upgrades service does not keep a decision ledger
    And the upgrades service changes the decisions index d3
    And this repository has the decisions index d3
    And the upgrades service completes this request

  @g3 @r3
  Scenario: A superseded ledger entry becomes a superseded design-decision
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
    And a ledger entry l1
    And a ledger entry l2
    And the ledger entry l1 supersedes the ledger entry l2
    And a bounded context b1
    And a design-decision d1
    And a design-decision d2
    When the person relocates the bounded context b1
    Then the upgrades service keeps the design-decision d1
    And the ledger entry l2 has the design-decision d1
    And the status of the design-decision d1 is `superseded`
    And the upgrades service keeps the design-decision d2
    And the design-decision d2 supersedes the design-decision d1

  @g4 @r4
  Scenario: A superseding ledger entry's qualifier is kept
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
    And a qualifier q1
    And a ledger entry l1
    And the ledger entry l1 has the qualifier q1
    And a ledger entry l2
    And the ledger entry l1 supersedes the ledger entry l2
    And a bounded context b1
    When the person relocates the bounded context b1
    Then the upgrades service keeps the design-decision d1
    And the design-decision d1 holds the qualifier q1

  @g5 @r5
  Scenario: A ledger entry with no number is given one
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
    And a ledger entry l1
    And a decision ledger d1
    And the decision ledger d1 has the ledger entry l1
    And the ledger entry l1 has no ledger number
    And a bounded context b1
    When the person relocates the bounded context b1
    Then the upgrades service keeps the ledger number l2
    And the ledger entry l1 has the ledger number l2

  @g6 @r6
  Scenario: A Behaviour line with no id is given one
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
    And a Behaviour line b1
    And a capability c1
    And the capability c1 has the Behaviour line b1
    And the Behaviour line b1 has no line id
    And a bounded context b2
    When the person relocates the bounded context b2
    Then the upgrades service keeps the line id l1
    And the Behaviour line b1 has the line id l1

  @g7 @r7
  Scenario: A bounded context whose ledger stem clashes with a tracked file is not relocated
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
    And a stem s1
    And a ledger entry l1
    And the ledger entry l1 has the stem s1
    And a tracked file t1
    And an old-layout directory o1
    And the old-layout directory o1 holds the tracked file t1
    And the tracked file t1 has the stem s1
    And a bounded context b1
    When the person relocates the bounded context b1
    Then the upgrades service refuses this request
    And the upgrades service names the tracked file t1

  @g8 @r8
  Scenario: No bounded context is relocated with an uncommitted change
    Given the tracked file `decisions/0001-a.md` holds "# a"
    And an uncommitted change u1
    And this repository holds the uncommitted change u1
    And a bounded context b1
    When the person relocates the bounded context b1
    Then the upgrades service refuses this request
    And the upgrades service names the uncommitted change u1

  @g9 @r9
  Scenario: No repository is upgraded with an uncommitted change
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And an uncommitted change u1
    And this repository holds the uncommitted change u1
    When the person upgrades this repository
    Then the upgrades service refuses this request
    And the upgrades service names the uncommitted change u1

  @g10 @r10
  Scenario: A query before 0.24.0 gives the release and every upgrade step
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And the release of this repository is `0.23.1`
    And an upgrade step u1
    And an upgrade step u2
    When the person queries this repository
    Then the upgrades service returns the release of this repository
    And the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2
    And the upgrades service completes this request

  @g11 @r11
  Scenario: A query with no plugin version file gives every upgrade step
    Given the tracked file `.shop/records/.keep` holds "kept"
    And a shop directory s1
    And this repository has the shop directory s1
    And this repository has no plugin version file
    And an upgrade step u1
    And an upgrade step u2
    When the person queries this repository
    Then the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2

  @g12 @r12
  Scenario: A query of a plugin version file with no version is refused
    Given the tracked file `.shop/plugin-version` holds "banana"
    And a plugin version file p1
    And this repository has the plugin version file p1
    And the plugin version file p1 holds no version
    When the person queries this repository
    Then the upgrades service refuses this request
    And the upgrades service names the content c1
    And the plugin version file p1 has the content c1

  @g13 @r13
  Scenario: An upgrade before 0.24.0 renames the work-item files and stage directories
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
    And the release of this repository is `0.23.1`
    And an upgrade step u1
    And an upgrade step u2
    And a work-item file w1
    And a work-item file w2
    And a stage directory s1
    And a stage directory s2
    And an initiative log i1
    And an initiative log i2
    When the person upgrades this repository
    Then the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2
    And the upgrades service changes the plugin version file p1
    And this repository has the plugin version file p1
    And the upgrades service changes the work-item file w1
    And the upgrades service changes the work-item file w2
    And the upgrades service changes the stage directory s1
    And the upgrades service changes the stage directory s2
    And the upgrades service changes the initiative log i1
    And the upgrades service changes the initiative log i2

  @g14 @r14
  Scenario: An upgrade from 0.24 rewrites every work-item file
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
    And the release of this repository is `0.24.0`
    And a work-item file w1
    And a work-item file w2
    When the person upgrades this repository
    Then the upgrades service changes the work-item file w1
    And the upgrades service changes the work-item file w2

  @g15 @r15
  Scenario: An upgrade to 0.30.0 restates a capability with no language
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
    And the release of this repository is `0.29.0`
    And a capability c1
    And this repository has the capability c1
    And the capability c1 has no language
    When the person upgrades this repository
    Then the upgrades service keeps the restated file r1
    And the upgrades service changes the capability c1
    And the upgrades service returns the restated file r1
    And the upgrades service returns the capability c1

  @g16 @r16
  Scenario: An upgrade to 0.30.0 rewrites old references and deprecated scenarios
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
    And the release of this repository is `0.29.0`
    And a work-item file w1
    And a requirement r1
    And the work-item file w1 mentions the requirement r1
    And a work-item file w2
    And a requirement r2
    And the work-item file w2 mentions the requirement r2
    And a work-item file w3
    And a requirement r3
    And the work-item file w3 does not mention the requirement r3
    And a feature f1
    And a scenario s1
    And the scenario s1 has `@deprecated`
    And the feature f1 holds the scenario s1
    And a feature f2
    And a scenario s2
    And the scenario s2 has `@deprecated`
    And the feature f2 holds the scenario s2
    And a feature f3
    And a scenario s3
    And the scenario s3 has `@deprecated`
    And the feature f3 does not hold the scenario s3
    When the person upgrades this repository
    Then the upgrades service changes the work-item file w1
    And the upgrades service changes the work-item file w2
    And the upgrades service does not change the work-item file w3
    And the upgrades service changes the feature f1
    And the upgrades service changes the feature f2
    And the upgrades service does not change the feature f3

  @g17 @r17
  Scenario: A session that starts before 0.24.0 is told the release and the upgrade steps
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And the release of this repository is `0.23.1`
    And a session s1
    And an upgrade step u1
    And an upgrade step u2
    When the session s1 starts
    Then the upgrades service notifies the session s1 of the release of this repository
    And the upgrades service notifies the session s1 of the upgrade step u1
    And the upgrades service notifies the session s1 of the upgrade step u2
    And the upgrades service notifies the session s1 of `only on the person's yes`

  @g18 @r18
  Scenario: A session that starts with no shop directory is told nothing
    Given the tracked file `README.md` holds "No shop here."
    And this repository has no shop directory
    And a session s1
    When the session s1 starts
    Then the upgrades service changes nothing

  @g19 @r19
  Scenario: A session that starts with a plugin version file of no version is told so
    Given the tracked file `.shop/plugin-version` holds "banana"
    And a plugin version file p1
    And this repository has the plugin version file p1
    And the plugin version file p1 holds no version
    And a session s1
    When the session s1 starts
    Then the upgrades service notifies the session s1 of `holds no version`
    And the upgrades service notifies the session s1 of the content c1
    And the plugin version file p1 has the content c1

  @g20 @r20
  Scenario: An upgrade to 0.31.0 freezes the work queue
    Given the tracked file `.shop/plugin-version` holds "0.30.0"
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
    And the release of this repository is `0.30.0`
    When the person upgrades this repository
    Then the upgrades service keeps the frozen notice f1
    And the upgrades service changes the decisions index d1
    And this repository has the decisions index d1

  @g21 @r21
  Scenario: An upgrade to 0.31.0 relocates each live frozen request of another asker
    Given the tracked file `.shop/plugin-version` holds "0.30.0"
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
    And the release of this repository is `0.30.0`
    And a frozen request f1
    And the asker of the frozen request f1 is not `internal`
    And the status of the frozen request f1 is not `delivered`
    And the status of the frozen request f1 is not `refused`
    And the status of the frozen request f1 is not `withdrawn`
    When the person upgrades this repository
    Then the upgrades service changes the frozen request f1

  @g22 @r22
  Scenario: An upgrade to 0.31.0 names each open initiative
    Given the tracked file `.shop/plugin-version` holds "0.30.0"
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
    And the release of this repository is `0.30.0`
    And an initiative i1
    And this repository has the initiative i1
    And the status of the initiative i1 is not `done`
    And the status of the initiative i1 is not `abandoned`
    And an upgrade step u1
    And the release of the upgrade step u1 is `0.31.0`
    And an upgrade step u2
    And the release of the upgrade step u2 is `0.31.0`
    And an upgrade step u3
    And the release of the upgrade step u3 is `0.24.0`
    When the person upgrades this repository
    Then the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2
    And the upgrades service does not return the upgrade step u3
    And the upgrades service returns the initiative i1

  @g23 @r23
  Scenario: An upgrade to 0.31.0 names each live internal frozen request
    Given the tracked file `.shop/plugin-version` holds "0.30.0"
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
    And the release of this repository is `0.30.0`
    And a frozen request f1
    And the asker of the frozen request f1 is `internal`
    And the status of the frozen request f1 is not `delivered`
    And the status of the frozen request f1 is not `refused`
    And the status of the frozen request f1 is not `withdrawn`
    When the person upgrades this repository
    Then the upgrades service returns the frozen request f1

  @g24 @r24
  Scenario: An upgrade to 0.32.0 names each term that violates v_t11
    Given the tracked file `.shop/plugin-version` holds "0.31.0"
    And the tracked file `spec/index.md` holds:
      """
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
      """
    And the release of this repository is `0.31.0`
    And an upgrade step u1
    And the release of the upgrade step u1 is `0.32.0`
    And an upgrade step u2
    And the release of the upgrade step u2 is `0.32.0`
    And an upgrade step u3
    And the release of the upgrade step u3 is `0.24.0`
    And a term t1
    And the term t1 violates `v_t11`
    And a term t2
    And the term t2 violates `v_t11`
    And a term t3
    And the term t3 does not violate `v_t11`
    When the person upgrades this repository
    Then the upgrades service changes the index file i1
    And this bounded context has the index file i1
    And the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2
    And the upgrades service does not return the upgrade step u3
    And the upgrades service returns the term t1
    And the upgrades service returns the term t2
    And the upgrades service does not return the term t3

  @g25 @r25
  Scenario: An upgrade to 0.33.0 rewrites the index file and every capability
    Given the tracked file `.shop/plugin-version` holds "0.32.1"
    And the tracked file `spec/index.md` holds:
      """
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
      """
    And the tracked file `spec/capabilities/cart.md` holds:
      """
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
      """
    And the release of this repository is `0.32.1`
    And a capability c1
    And a capability c2
    And an upgrade step u1
    And the release of the upgrade step u1 is `0.33.0`
    And an upgrade step u2
    And the release of the upgrade step u2 is `0.33.0`
    And an upgrade step u3
    And the release of the upgrade step u3 is `0.24.0`
    When the person upgrades this repository
    Then the upgrades service changes the index file i1
    And this bounded context has the index file i1
    And the upgrades service changes the capability c1
    And the upgrades service changes the capability c2
    And the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2
    And the upgrades service does not return the upgrade step u3

  @g26 @r26
  Scenario: An upgrade to 0.34.0 names each term that violates w_value_kind
    Given the tracked file `.shop/plugin-version` holds "0.33.0"
    And the tracked file `spec/index.md` holds:
      """
      ---
      id: bounded-context/example.org/acme/shop
      title: shop
      language: codified-2
      ---
      # shop
      ## Glossary
      - **cart** (noun): the goods a shopper picks.
      - **status** (attribute of cart): Values: `open`, `paid`.
      """
    And the release of this repository is `0.33.0`
    And an upgrade step u1
    And the release of the upgrade step u1 is `0.34.0`
    And an upgrade step u2
    And the release of the upgrade step u2 is `0.34.0`
    And an upgrade step u3
    And the release of the upgrade step u3 is `0.24.0`
    And a term t1
    And the term t1 violates `w_value_kind`
    And a term t2
    And the term t2 violates `w_value_kind`
    And a term t3
    And the term t3 does not violate `w_value_kind`
    When the person upgrades this repository
    Then the upgrades service returns the upgrade step u1
    And the upgrades service returns the upgrade step u2
    And the upgrades service does not return the upgrade step u3
    And the upgrades service returns the term t1
    And the upgrades service returns the term t2
    And the upgrades service does not return the term t3

  @g27 @r27
  Scenario: An upgrade at the plugin's release changes nothing
    Given the release of this repository is `0.34.1`
    And the release of this plugin is `0.34.1`
    When the person upgrades this repository
    Then the upgrades service returns `no upgrade step is pending`
    And the upgrades service does not change a file

  @g28 @r28
  Scenario: A session that starts after the plugin's release is told to update the plugin
    Given the release of this repository is `0.23.1`
    And the release of this plugin is `0.23.0`
    And a session s1
    When the session s1 starts
    Then the upgrades service notifies the session s1 of `update the plugin`

  @g29 @r29
  Scenario: A session that starts at the plugin's release with no open initiative is told nothing (case 1)
    Given the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: done
      ---
      # i1
      """
    And the release of this repository is `0.34.1`
    And the release of this plugin is `0.34.1`
    And an initiative i1
    And this repository has the initiative i1
    And the status of the initiative i1 is `done`
    And a session s1
    When the session s1 starts
    Then the upgrades service does not notify the session s1 of an upgrade step
    And the upgrades service does not notify the session s1 of an initiative

  @g29 @r29
  Scenario: A session that starts at the plugin's release with no open initiative is told nothing (case 2)
    Given the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: done
      ---
      # i1
      """
    And the release of this repository is `0.34.1`
    And the release of this plugin is `0.34.1`
    And an initiative i1
    And this repository has the initiative i1
    And the status of the initiative i1 is `abandoned`
    And a session s1
    When the session s1 starts
    Then the upgrades service does not notify the session s1 of an upgrade step
    And the upgrades service does not notify the session s1 of an initiative

  @g30 @r30
  Scenario: An upgrade at a patch release keeps the new plugin version
    Given the release of this repository is `0.34.0`
    And the release of this plugin is `0.34.1`
    When the person upgrades this repository
    Then the upgrades service returns `no upgrade step is pending`
    And the upgrades service changes the plugin version file p1
    And this repository has the plugin version file p1
    And the upgrades service keeps the plugin version file p1

  @g31 @r31
  Scenario: Founding a bounded context keeps its context scaffold
    Given the tracked file `README.md` holds "A new context."
    And this bounded context has no index file
    And this repository has no shop directory
    And a context id c1
    When the person founds this bounded context with the context id c1
    Then the upgrades service keeps the context scaffold c2
    And this repository has the context scaffold c2
    And the upgrades service completes this request

  @g32 @r32
  Scenario: A bounded context is not founded without a context id
    When the person founds this bounded context without a context id
    Then the upgrades service refuses this request
    And the upgrades service names this bounded context

  @g33 @r33
  Scenario: A bounded context is not founded with a context id that is no bounded context id
    Given a context id c1
    And the context id c1 does not conform to the bounded context id form
    When the person founds this bounded context with the context id c1
    Then the upgrades service refuses this request
    And the upgrades service names the context id c1

  @g34 @r34
  Scenario: A bounded context that has an index file is not founded and nothing changes
    Given the tracked file `spec/index.md` holds "# notes"
    And an index file i1
    And this bounded context has the index file i1
    And a context id c1
    When the person founds this bounded context with the context id c1
    Then the upgrades service refuses this request
    And the upgrades service names the index file i1
    # entailed: U17

  @g35 @r35
  Scenario: A repository that has a shop directory is not founded on and nothing changes
    Given the tracked file `.shop/backlog/b1.md` holds "# b1"
    And a shop directory s1
    And this repository has the shop directory s1
    And a context id c1
    When the person founds this bounded context with the context id c1
    Then the upgrades service refuses this request
    And the upgrades service names the shop directory s1
    # entailed: U17
