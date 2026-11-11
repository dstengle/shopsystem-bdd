# generated from spec/capabilities/backlog.md by features generate; do not edit
Feature: Backlog
  Narrator: a person or session keeping the backlog

  @g5 @r5
  Scenario: `work depend` records a dependency
    Given an item i1
    When the person runs `work depend` on the item i1
    Then the item i1 has the dependency d1
    And `work` writes the dependency d1
    And `work` commits the item i1

  @g15 @r15
  Scenario: `work show` names an item by its title
    Given an item i1
    When the person runs `work show` on the item i1
    Then the item i1 has the title t1
    And `work` prints the title t1

  @g22 @r22
  Scenario: `work idea` writes an item
    When the person runs `work idea`
    Then the status of the item i1 is `idea`
    And `work` writes the item i1
    And `work` commits the item i1

  @g25 @r25
  Scenario: `work rate` sets an item's ratings
    Given an item i1
    When the person runs `work rate --value high-value --urgency low-urgency --size small` on the item i1
    Then `work` sets the value of the item i1 to `high-value`
    And `work` sets the urgency of the item i1 to `low-urgency`
    And `work` sets the size of the item i1 to `small`
    And `work` commits the item i1

  @g26 @r26
  Scenario: `work backlog` prints an item with its dependency on an item that is not delivered
    Given an item i1
    And the status of the item i1 is not `delivered`
    And a dependency d1
    And the dependency d1 is on the item i1
    And the dependency d1 exists
    And an item i2
    And the item i2 has the dependency d1
    When the person runs `work backlog`
    Then `work` prints the item i2
    And `work` prints the dependency d1

  @g27 @r27
  Scenario: `work backlog --json` prints one JSON object
    Given a JSON object j1
    When the person runs `work backlog` with the `--json` option
    Then `work` prints the JSON object j1
    And `work` exits successfully

  @g32 @r32
  Scenario: `work idea` keeps its commit and names the remote that rejects its push
    Given a remote r1
    And this repository has the remote r1
    And a push p1
    And this command has the push p1
    And the remote r1 rejects the push p1
    When the person runs `work idea`
    Then the status of the item i1 is `idea`
    And `work` writes the item i1
    And `work` commits the item i1
    And `work` prints the remote r1
    And `work` exits successfully

  @g33 @r33
  Scenario: `work idea` keeps its commit and names the remote that does not answer its push
    Given a remote r1
    And this repository has the remote r1
    And a push p1
    And this command has the push p1
    And the remote r1 does not answer the push p1
    When the person runs `work idea`
    Then the status of the item i1 is `idea`
    And `work` writes the item i1
    And `work` commits the item i1
    And `work` prints the remote r1
    And `work` exits successfully

  @g34 @r34
  Scenario: `work idea` refuses the branch of a task
    Given a git branch g1
    And a task t1
    And the task t1 has the git branch g1
    And this repository checks out the git branch g1
    When the person runs `work idea`
    Then `work` refuses `work idea`
    And `work` names the task t1

  @g35 @r35
  Scenario: `work idea` keeps an upstream branch of another name
    Given a branch name b1
    And a git branch g1
    And the git branch g1 has the branch name b1
    And this repository checks out the git branch g1
    And an upstream branch u1
    And the git branch g1 has the upstream branch u1
    And a branch name b2
    And the upstream branch u1 has the branch name b2
    When the person runs `work idea`
    Then the status of the item i1 is `idea`
    And `work` writes the item i1
    And `work` commits the item i1
    And `work` keeps the upstream branch u1

  @g36 @r36
  Scenario: `work backlog` prints every item with its title, status, provenance and ratings
    Given an item i1
    And the item i1 exists
    When the person runs `work backlog`
    Then `work` prints the item i1
    And the item i1 has the title t1
    And `work` prints the title t1
    And `work` prints the status of the item i1
    And `work` prints the provenance of the item i1
    And `work` prints the value of the item i1
    And `work` prints the urgency of the item i1
    And `work` prints the size of the item i1

  @g37 @r37
  Scenario: `work shape` shapes an idea
    Given an item i1
    And the status of the item i1 is `idea`
    When the person runs `work shape` on the item i1
    Then `work` sets the status of the item i1 to `shaped`

  @g38 @r38
  Scenario: `work shape` refuses an item that is not an idea
    Given an item i1
    And the status of the item i1 is not `idea`
    When the person runs `work shape` on the item i1
    Then `work` refuses `work shape`
    And `work` names the status of the item i1

  @g39 @r39
  Scenario: `work withdraw` withdraws an item that is an idea, shaped, ready or needs input (case 1)
    Given an item i1
    And the status of the item i1 is `idea`
    When the person runs `work withdraw` on the item i1
    Then `work` sets the status of the item i1 to `withdrawn`

  @g39 @r39
  Scenario: `work withdraw` withdraws an item that is an idea, shaped, ready or needs input (case 2)
    Given an item i1
    And the status of the item i1 is `shaped`
    When the person runs `work withdraw` on the item i1
    Then `work` sets the status of the item i1 to `withdrawn`

  @g39 @r39
  Scenario: `work withdraw` withdraws an item that is an idea, shaped, ready or needs input (case 3)
    Given an item i1
    And the status of the item i1 is `ready`
    When the person runs `work withdraw` on the item i1
    Then `work` sets the status of the item i1 to `withdrawn`

  @g39 @r39
  Scenario: `work withdraw` withdraws an item that is an idea, shaped, ready or needs input (case 4)
    Given an item i1
    And the status of the item i1 is `needs-input`
    When the person runs `work withdraw` on the item i1
    Then `work` sets the status of the item i1 to `withdrawn`

  @g40 @r40
  Scenario: `work refuse` refuses an item that is an idea or shaped (case 1)
    Given an item i1
    And the status of the item i1 is `idea`
    When the person runs `work refuse` on the item i1
    Then `work` sets the status of the item i1 to `refused`

  @g40 @r40
  Scenario: `work refuse` refuses an item that is an idea or shaped (case 2)
    Given an item i1
    And the status of the item i1 is `shaped`
    When the person runs `work refuse` on the item i1
    Then `work` sets the status of the item i1 to `refused`

  @g41 @r41
  Scenario: `work answer` returns an item that needs input to shaped
    Given an item i1
    And the status of the item i1 is `needs-input`
    When the person runs `work answer` on the item i1
    Then `work` sets the status of the item i1 to `shaped`
    And `work` commits the item i1

  @g42 @r42
  Scenario: `work backlog` prints the question of an item that needs input
    Given an item i1
    And the status of the item i1 is `needs-input`
    And a question q1
    And the question q1 is on the item i1
    And a question q2
    And the question q2 is on the item i1
    When the person runs `work backlog`
    Then `work` prints the item i1
    And `work` prints the question q1
    And `work` prints the question q2
