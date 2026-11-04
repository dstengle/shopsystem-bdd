# generated from spec/capabilities/batches.md by features generate; do not edit
Feature: Batches
  Narrator: a person or session building a batch

  @g1 @r1
  Scenario: `work batch start` picks ready items
    Given an item i1 that is `ready`
    And the item i1 is passing
    And the item i1 is not blocked
    When the person runs `work batch start`
    Then `work` writes the batch b1
    And the batch b1 is `building`
    And `work` writes the batch plan b2
    And the item i1 is `in-batch`

  @g2 @r2
  Scenario: A ready item that is no longer passing is returned
    Given an item i1 that is `ready`
    And the item i1 is not passing
    When the person runs `work batch start`
    Then the item i1 is `shaped`

  @g3 @r3
  Scenario: A blocked item is not picked
    Given an item i1 that is `ready`
    And the item i1 is blocked
    When the person runs `work batch start`
    Then the item i1 is not `in-batch`

  @g4 @r4
  Scenario: `work batch status` prints where the batch stands
    Given an item i1
    And a batch b1
    And the item i1 is in the batch b1
    And a task t1
    And the task t1 is of the batch b1
    When the person runs `work batch status` on the batch b1
    Then `work` prints the item i1
    And `work` prints the task t1
    And `work` prints the status of the task t1

  @g5 @r5
  Scenario: `work batch resume` carries on without a person
    Given a batch b1 that is `building`
    When the session s1 runs `work batch resume` on the batch b1
    Then `work` uses the batch plan b2
    And `work` does not ask the question q1

  @g6 @r6
  Scenario: A park leaves the rest building
    Given an item i1 that is `in-batch`
    When the batch b1 parks the item i1
    Then the item i1 is `needs-input`
    And the batch b1 is not `abandoned`

  @g7 @r7
  Scenario: A parked item's commits stay out of the pull request
    Given an item i1
    And a batch b1
    And the item i1 is in the batch b1
    And the item i1 is `needs-input`
    When the person runs `work batch review` on the batch b1
    Then `work` publishes the pull request p1
    And the pull request p1 is of the batch b1

  @g8 @r8
  Scenario: `work batch review` publishes the pull request
    Given a batch b1 that is `building`
    When the person runs `work batch review` on the batch b1
    Then `work` publishes the pull request p1
    And the pull request p1 is of the batch b1
    And the batch b1 is `in-review`

  @g9 @r9
  Scenario: The merge delivers
    Given an item i1
    And a batch b1
    And the item i1 is in the batch b1
    And the item i1 is `in-batch`
    And a pull request p1
    And the pull request p1 is of the batch b1
    When the person merges the pull request p1
    Then the item i1 is `delivered`

  @g10 @r10
  Scenario: `work batch abandon` returns the batch's items
    Given a batch b1 that is `building`
    And an item i1
    And the item i1 is in the batch b1
    When the person runs `work batch abandon` on the batch b1
    Then the batch b1 is `abandoned`
    And the item i1 is `ready`
