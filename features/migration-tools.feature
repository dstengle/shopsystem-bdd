# generated from spec/capabilities/migration-tools.md by features generate; do not edit
Feature: Migration tools
  Narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases

  @g27 @r27
  Scenario: `migrate run` relocates every old-layout directory and rewrites every file that mentions one
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
    And an old-layout directory o2
    And an old-layout directory o3
    And a file f1
    And an old-layout directory o4
    And the file f1 mentions the old-layout directory o4
    And a file f2
    And an old-layout directory o5
    And the file f2 mentions the old-layout directory o5
    When the person runs `migrate run` on the bounded context b1
    Then `migrate` relocates the old-layout directory o2
    And `migrate` relocates the old-layout directory o3
    And `migrate` rewrites the file f1
    And `migrate` rewrites the file f2

  @g28 @r28
  Scenario: `migrate run` writes a design-decision of each ledger entry, removes the decision ledger and rewrites the decisions index
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
    When the person runs `migrate run` on the bounded context b1
    Then the ledger entry l1 has the design-decision d2
    And `migrate` writes the design-decision d2
    And `migrate` removes the decision ledger d1
    And this repository has the decisions index d3
    And `migrate` rewrites the decisions index d3
    And `migrate` exits successfully

  @g29 @r29
  Scenario: `migrate run` writes the design-decision of a ledger entry that another supersedes with the status `superseded`
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
    When the person runs `migrate run` on the bounded context b1
    Then the ledger entry l2 has the design-decision d1
    And the design-decision d1 is `superseded`
    And `migrate` writes the design-decision d1

  @g30 @r30
  Scenario: `migrate run` writes a design-decision that supersedes the design-decision of the ledger entry another supersedes
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
    When the person runs `migrate run` on the bounded context b1
    Then the ledger entry l2 has the design-decision d1
    And the design-decision d2 supersedes the design-decision d1
    And `migrate` writes the design-decision d2

  @g31 @r31
  Scenario: `migrate run` writes the qualifier of a supersedes in part into the design-decision that supersedes
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
    When the person runs `migrate run` on the bounded context b1
    Then the design-decision d1 holds the qualifier q1
    And `migrate` writes the design-decision d1

  @g32 @r32
  Scenario: `migrate run` gives each ledger entry with no ledger number a ledger number
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
    When the person runs `migrate run` on the bounded context b1
    Then `migrate` gives the ledger number l2 to the ledger entry l1

  @g33 @r33
  Scenario: `migrate run` gives each Behaviour line with no line id a line id
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
    When the person runs `migrate run` on the bounded context b2
    Then `migrate` gives the line id l1 to the Behaviour line b1

  @g34 @r34
  Scenario: `migrate run` refuses a ledger entry whose design-decision would take the place of a tracked file
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
    When the person runs `migrate run` on the bounded context b1
    Then `migrate` refuses `migrate run`
    And `migrate` names the tracked file t1

  @g35 @r35
  Scenario: `migrate run` refuses a repository with an uncommitted change, naming it
    Given the tracked file `decisions/0001-a.md` holds "# a"
    And an uncommitted change u1
    And this repository holds the uncommitted change u1
    When the person runs `migrate run` on the bounded context b1
    Then `migrate` refuses `migrate run`
    And `migrate` names the uncommitted change u1

  @g36 @r36
  Scenario: `migrate upgrade` refuses a repository with an uncommitted change, naming it
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And an uncommitted change u1
    And this repository holds the uncommitted change u1
    When the person runs `migrate upgrade`
    Then `migrate` refuses `migrate upgrade`
    And `migrate` names the uncommitted change u1

  @g37 @r37
  Scenario: `migrate status` prints the release of a repository before 0.24.0 and every upgrade step
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And this repository is `0.23.1`
    And an upgrade step u1
    And an upgrade step u2
    When the person runs `migrate status`
    Then `migrate` prints the release of this repository
    And `migrate` prints the upgrade step u1
    And `migrate` prints the upgrade step u2
    And `migrate` exits successfully

  @g38 @r38
  Scenario: `migrate status` on a repository with a shop directory and no plugin version file prints every upgrade step, as on 0.23.1
    Given the tracked file `.shop/records/.keep` holds "kept"
    And a shop directory s1
    And this repository has the shop directory s1
    And this repository has no plugin version file
    And an upgrade step u1
    And an upgrade step u2
    When the person runs `migrate status`
    Then `migrate` prints the upgrade step u1
    And `migrate` prints the upgrade step u2

  @g39 @r39
  Scenario: `migrate status` refuses a plugin version file that holds no version, naming what it holds
    Given the tracked file `.shop/plugin-version` holds "banana"
    And a plugin version file p1
    And this repository has the plugin version file p1
    And the plugin version file p1 holds no version
    When the person runs `migrate status`
    Then `migrate` refuses `migrate status`
    And the plugin version file p1 has the content c1
    And `migrate` names the content c1

  @g40 @r40
  Scenario: `migrate upgrade` on a repository before 0.24.0 prints every upgrade step and rewrites the plugin version file
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
    And this repository is `0.23.1`
    And an upgrade step u1
    And an upgrade step u2
    When the person runs `migrate upgrade`
    Then `migrate` prints the upgrade step u1
    And `migrate` prints the upgrade step u2
    And this repository has the plugin version file p1
    And `migrate` rewrites the plugin version file p1

  @g41 @r41
  Scenario: `migrate upgrade` on a repository before 0.24.0 renames every work-item file and stage directory to `w<n>` and rewrites every initiative log
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
    And this repository is `0.23.1`
    And a work-item file w1
    And a work-item file w2
    And a stage directory s1
    And a stage directory s2
    And an initiative log i1
    And an initiative log i2
    When the person runs `migrate upgrade`
    Then `migrate` renames the work-item file w1
    And `migrate` renames the work-item file w2
    And `migrate` renames the stage directory s1
    And `migrate` renames the stage directory s2
    And `migrate` rewrites the initiative log i1
    And `migrate` rewrites the initiative log i2

  @g42 @r42
  Scenario: `migrate upgrade` on a repository on the plugin's release says that no upgrade step is pending and changes nothing
    Given the tracked file `.shop/plugin-version` holds "3.0.1"
    And this repository is `3.0.1`
    When the person runs `migrate upgrade`
    Then `migrate` prints `no upgrade step is pending`
    And `migrate` does not change a file

  @g43 @r43
  Scenario: `migrate upgrade` on a repository from 0.24.0 and before 0.25.0 rewrites every work-item file
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
    And this repository is `0.24.0`
    And a work-item file w1
    And a work-item file w2
    When the person runs `migrate upgrade`
    Then `migrate` rewrites the work-item file w1
    And `migrate` rewrites the work-item file w2

  @g44 @r44
  Scenario: `migrate upgrade` on a repository before 1.0.0 writes the restated file and rewrites each capability with no language
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
    And this repository is `0.29.0`
    And a capability c1
    And this repository has the capability c1
    And the capability c1 has no language
    When the person runs `migrate upgrade`
    Then `migrate` writes the restated file r1
    And `migrate` rewrites the capability c1
    And `migrate` prints the restated file r1
    And `migrate` prints the capability c1

  @g46 @r46
  Scenario: `migrate upgrade` on a repository before 1.0.0 writes each reference of a work-item file to a requirement with its release
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
    And this repository is `0.29.0`
    And a work-item file w1
    And a requirement r1
    And the work-item file w1 mentions the requirement r1
    And a work-item file w2
    And a requirement r2
    And the work-item file w2 mentions the requirement r2
    When the person runs `migrate upgrade`
    Then `migrate` rewrites the work-item file w1
    And `migrate` rewrites the work-item file w2

  @g47 @r47
  Scenario: the SessionStart hook tells a session to offer the upgrade steps of a repository before 0.24.0, and to run them only on the person's yes
    Given the tracked file `.shop/plugin-version` holds "0.23.1"
    And this repository is `0.23.1`
    And an upgrade step u1
    And an upgrade step u2
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints the release of this repository
    And `migrate` prints the upgrade step u1
    And `migrate` prints the upgrade step u2
    And `migrate` prints `only on the person's yes`

  @g48 @r48
  Scenario: the SessionStart hook tells a session to tell the person to update the plugin
    Given the tracked file `.shop/plugin-version` holds "9.0.0"
    And this repository is `9.0.0`
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints `update the plugin`

  @g49 @r49
  Scenario: the SessionStart hook tells a session nothing on the plugin's release when no initiative is open (case 1)
    Given the tracked file `.shop/plugin-version` holds "3.0.1"
    And the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: done
      ---
      # i1
      """
    And this repository is `3.0.1`
    And an initiative i1
    And this repository has the initiative i1
    And the initiative i1 is `done`
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` exits successfully
    And `migrate` does not print an upgrade step
    And `migrate` does not print an initiative

  @g49 @r49
  Scenario: the SessionStart hook tells a session nothing on the plugin's release when no initiative is open (case 2)
    Given the tracked file `.shop/plugin-version` holds "3.0.1"
    And the tracked file `.shop/work/i1/initiative.md` holds:
      """
      ---
      id: initiative/example.org/acme/shop/i1
      kind: initiative
      status: done
      ---
      # i1
      """
    And this repository is `3.0.1`
    And an initiative i1
    And this repository has the initiative i1
    And the initiative i1 is `abandoned`
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` exits successfully
    And `migrate` does not print an upgrade step
    And `migrate` does not print an initiative

  @g50 @r50
  Scenario: the SessionStart hook tells a session nothing in a repository with no shop directory
    Given the tracked file `README.md` holds "No shop here."
    And this repository has no shop directory
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` exits successfully

  @g51 @r51
  Scenario: the SessionStart hook tells a session that the plugin version file holds no version
    Given the tracked file `.shop/plugin-version` holds "banana"
    And a plugin version file p1
    And this repository has the plugin version file p1
    And the plugin version file p1 holds no version
    When the SessionStart hook runs `migrate status --hook`
    Then `migrate` prints `holds no version`
    And the plugin version file p1 has the content c1
    And `migrate` prints the content c1

  @g52 @r52
  Scenario: `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 writes the frozen notice and rewrites the decisions index
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
    And this repository is `1.0.0`
    When the person runs `migrate upgrade`
    Then `migrate` writes the frozen notice f1
    And this repository has the decisions index d1
    And `migrate` rewrites the decisions index d1

  @g53 @r53
  Scenario: `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 relocates each frozen request another bounded context asked that is not closed
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
    And this repository is `1.0.0`
    And a frozen request f1
    And the frozen request f1 is not `internal`
    And the frozen request f1 is not `delivered`
    And the frozen request f1 is not `refused`
    And the frozen request f1 is not `withdrawn`
    When the person runs `migrate upgrade`
    Then `migrate` relocates the frozen request f1

  @g54 @r54
  Scenario: `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 names the upgrade step and each initiative that is not closed
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
    And this repository is `1.0.0`
    And an initiative i1
    And this repository has the initiative i1
    And the initiative i1 is not `done`
    And the initiative i1 is not `abandoned`
    And an upgrade step u1
    And the upgrade step u1 is `2.0.0`
    And an upgrade step u2
    And the upgrade step u2 is `2.0.0`
    When the person runs `migrate upgrade`
    Then `migrate` prints the upgrade step u1
    And `migrate` prints the upgrade step u2
    And `migrate` prints the initiative i1

  @g55 @r55
  Scenario: `migrate upgrade` on a repository from 1.0.0 and before 2.0.0 names each frozen request it asked of itself that is not closed
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
    And this repository is `1.0.0`
    And a frozen request f1
    And the frozen request f1 is `internal`
    And the frozen request f1 is not `delivered`
    And the frozen request f1 is not `refused`
    And the frozen request f1 is not `withdrawn`
    When the person runs `migrate upgrade`
    Then `migrate` prints the frozen request f1

  @g56 @r56
  Scenario: `migrate upgrade` on a repository from 2.0.0 and before 3.0.0 rewrites the index file with each term's part of speech and names each term that violates `v_t11`
    Given the tracked file `.shop/plugin-version` holds "2.0.0"
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
    And this repository is `2.0.0`
    And an upgrade step u1
    And the upgrade step u1 is `3.0.0`
    And an upgrade step u2
    And the upgrade step u2 is `3.0.0`
    And a term t1
    And the term t1 violates `v_t11`
    And a term t2
    And the term t2 violates `v_t11`
    When the person runs `migrate upgrade`
    Then this bounded context has the index file i1
    And `migrate` rewrites the index file i1
    And `migrate` prints the upgrade step u1
    And `migrate` prints the upgrade step u2
    And `migrate` prints the term t1
    And `migrate` prints the term t2

  @g57 @r57
  Scenario: `migrate upgrade` on a repository before 1.0.0 removes each scenario that has the `@deprecated` tag from its feature
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
    And this repository is `0.29.0`
    And a feature f1
    And a scenario s1
    And the scenario s1 has `@deprecated`
    And the feature f1 holds the scenario s1
    And a feature f2
    And a scenario s2
    And the scenario s2 has `@deprecated`
    And the feature f2 holds the scenario s2
    When the person runs `migrate upgrade`
    Then `migrate` rewrites the feature f1
    And `migrate` rewrites the feature f2
