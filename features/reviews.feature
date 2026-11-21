# generated from spec/capabilities/reviews.md by features generate; do not edit
Feature: Reviews
  Narrator: the person

  @g1 @r1
  Scenario: A batch submitted keeps a change that cites its items
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the proposed change p1 cites the item i1

  @g2 @r2
  Scenario: A batch's change holds no kept change of a parked item
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `needs-input`
    And a kept change k1
    And the kept change k1 cites the item i1
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the proposed change p1 does not hold the kept change k1

  @g3 @r3
  Scenario: A batch with a task not done is not submitted
    Given a task t1
    And a batch b1
    And the batch b1 has the task t1
    And the status of the task t1 is not `done`
    When the person submits the batch b1
    Then the batches service refuses this request
    And the batches service names the task t1

  @g4 @r4
  Scenario: A batch with a kept change that cites no item is not submitted
    Given a task t1
    And a batch b1
    And the batch b1 has the task t1
    And a workspace w1
    And the task t1 has the workspace w1
    And a kept change k1
    And the kept change k1 cites no item
    And the workspace w1 holds the kept change k1
    When the person submits the batch b1
    Then the batches service refuses this request
    And the batches service names the kept change k1

  @g5 @r5
  Scenario: A batch whose tasks are done is submitted for review
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the batches service sets the status of the batch b1 to `in-review`

  @g6 @r6
  Scenario: A batch is submitted with its tests run by the batch's virtual environment
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    And a workspace w1
    And the batch b1 has the workspace w1
    And a virtual environment v1
    And the workspace w1 holds the virtual environment v1
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the batches service sets the status of the batch b1 to `in-review`
