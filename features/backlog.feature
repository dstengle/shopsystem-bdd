# generated from spec/capabilities/backlog.md by features generate; do not edit
Feature: Backlog
  Narrator: a person or session keeping the backlog

  @g1 @r1
  Scenario: `work idea` writes an item
    When the person runs `work idea`
    Then `work` writes the item i1
    And the item i1 is `idea`
    And `work` commits the item i1

  @g2 @r2
  Scenario: `work shape` shapes an idea
    Given an item i1 that is `idea`
    When the person runs `work shape` on the item i1
    Then the item i1 is `shaped`

  @g3 @r3
  Scenario: `work shape` refuses an item that is not an idea
    Given an item i1
    And the item i1 is not `idea`
    When the person runs `work shape` on the item i1
    Then `work` exits with an error naming the status of the item i1
    And `work` changes nothing

  @g4 @r4
  Scenario: `work rate` sets an item's ratings
    Given `--value high-value --urgency low-urgency --size small` is given
    When the person runs `work rate` on the item i1
    Then the item i1 is `high-value`
    And the item i1 is `low-urgency`
    And the item i1 is `small`
    And `work` commits the item i1

  @g5 @r5
  Scenario: `work depend` records a dependency
    When the person runs `work depend` on the item i1
    Then `work` writes the dependency d1
    And the dependency d1 is of the item i1
    And `work` commits the item i1

  @g6 @r6
  Scenario: `work backlog` prints the backlog, each item by its title
    When the person runs `work backlog`
    Then `work` prints the item i1
    And `work` prints the title t1
    And the title t1 is of the item i1
    And `work` prints the status of the item i1
    And `work` prints the provenance of the item i1
    And `work` prints the value of the item i1
    And `work` prints the urgency of the item i1
    And `work` prints the size of the item i1

  @g7 @r7
  Scenario: `work backlog` marks a blocked item
    Given an item i1
    And the item i1 is not `delivered`
    And a dependency d1
    And the dependency d1 is on the item i1
    And an item i2
    And the item i2 is blocked
    And the dependency d1 is of the item i2
    When the person runs `work backlog`
    Then `work` prints the item i2
    And `work` prints the dependency d1

  @g8 @r8
  Scenario: `work backlog --json` prints one JSON object
    Given `--json` is given
    When the person runs `work backlog`
    Then `work` prints the JSON object j1
    And `work` exits successfully

  @g9 @r9
  Scenario: `work withdraw` withdraws an idea
    Given an item i1 that is `idea`
    When the person runs `work withdraw` on the item i1
    Then the item i1 is `withdrawn`

  @g10 @r10
  Scenario: `work withdraw` withdraws a shaped item
    Given an item i1 that is `shaped`
    When the person runs `work withdraw` on the item i1
    Then the item i1 is `withdrawn`

  @g11 @r11
  Scenario: `work withdraw` withdraws a ready item
    Given an item i1 that is `ready`
    When the person runs `work withdraw` on the item i1
    Then the item i1 is `withdrawn`

  @g12 @r12
  Scenario: `work withdraw` withdraws an item that needs input
    Given an item i1 that is `needs-input`
    When the person runs `work withdraw` on the item i1
    Then the item i1 is `withdrawn`

  @g13 @r13
  Scenario: `work refuse` refuses an idea
    Given an item i1 that is `idea`
    When the person runs `work refuse` on the item i1
    Then the item i1 is `refused`

  @g14 @r14
  Scenario: `work refuse` refuses a shaped item
    Given an item i1 that is `shaped`
    When the person runs `work refuse` on the item i1
    Then the item i1 is `refused`

  @g15 @r15
  Scenario: `work show` names an item by its title
    When the person runs `work show` on the item i1
    Then `work` prints the title t1
    And the title t1 is of the item i1

  @g16 @r16
  Scenario: `work answer` returns an item that needs input to shaped
    Given an item i1 that is `needs-input`
    When the person runs `work answer` on the item i1
    Then the item i1 is `shaped`
    And `work` commits the item i1

  @g17 @r17
  Scenario: `work backlog` prints the question of an item that needs input
    Given an item i1 that is `needs-input`
    When the person runs `work backlog`
    Then `work` prints the item i1
    And `work` prints the question q1
    And the question q1 is on the item i1

  @g18 @r18
  Scenario: `work idea` keeps its commit and names a remote it cannot push to
    Given a remote r1
    And the remote r1 is unpushable
    When the person runs `work idea`
    Then `work` writes the item i1
    And the item i1 is `idea`
    And `work` commits the item i1
    And `work` prints the remote r1
    And `work` exits successfully

  @g19 @r19
  Scenario: `work idea` keeps its commit and names a remote that does not answer
    Given a remote r1
    And the remote r1 is silent
    When the person runs `work idea`
    Then `work` writes the item i1
    And the item i1 is `idea`
    And `work` commits the item i1
    And `work` prints the remote r1
    And `work` exits successfully

  @g20 @r20
  Scenario: `work idea` refuses the branch of a task
    Given a repository r1
    And the repository r1 is tasked
    When the person runs `work idea`
    Then `work` exits with an error naming the task t1
    And `work` changes nothing

  @g21 @r21
  Scenario: `work idea` keeps the upstream branch of the branch checked out
    Given a repository r1
    And the repository r1 is tracking
    When the person runs `work idea`
    Then `work` writes the item i1
    And the item i1 is `idea`
    And `work` commits the item i1
    And `work` keeps the upstream branch u1
