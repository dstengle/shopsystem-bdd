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

  @g7 @r7
  Scenario: A batch whose task branches touch one file without a conflict is submitted, merged in task order
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    And an item i1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a kept change k1
    And a file f1
    And the kept change k1 touches the file f1
    And the kept change k1 cites the item i1
    And a kept change k2
    And the kept change k2 touches the file f1
    And an item i2
    And the batch b1 holds the item i2
    And the status of the item i2 is `in-batch`
    And the kept change k2 cites the item i2
    And no kept change conflicts with a kept change
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the proposed change p1 holds the kept change k2
    And the batches service sets the status of the batch b1 to `in-review`

  @g8 @r8
  Scenario: A batch whose task branches conflict is not submitted, naming the file and both items
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a kept change k1
    And the kept change k1 cites the item i1
    And an item i2
    And the batch b1 holds the item i2
    And the status of the item i2 is `in-batch`
    And a kept change k2
    And the kept change k2 cites the item i2
    And the kept change k1 conflicts with the kept change k2
    And a file f1
    And the kept change k2 touches the file f1
    And an item i3
    And a kept change k3
    And the batch b1 holds the item i3
    And the kept change k3 conflicts with the kept change k2
    And the kept change k3 cites the item i3
    And an item i4
    And a kept change k4
    And the batch b1 holds the item i4
    And the kept change k4 conflicts with the kept change k2
    And the kept change k4 cites the item i4
    And an item i5
    And a kept change k5
    And the batch b1 holds the item i5
    And the kept change k5 conflicts with the kept change k2
    And the kept change k5 does not cite the item i5
    When the person submits the batch b1
    Then the batches service refuses this request
    And the batches service names the file f1
    And the batches service names the item i2
    And the batches service names the item i3
    And the batches service names the item i4
    And the batches service does not name the item i5

  @g9 @r9
  Scenario: A batch awaiting its merge whose branch merged its base is submitted for review again
    Given a batch b1
    And the status of the batch b1 is `awaiting-merge`
    And a workspace w1
    And the batch b1 has the workspace w1
    And a base merge b2
    And the workspace w1 holds the base merge b2
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the batches service sets the status of the batch b1 to `in-review`

  @g10 @r10
  Scenario: A batch awaiting its merge with no base merge is not submitted
    Given a batch b1
    And the status of the batch b1 is `awaiting-merge`
    And a workspace w1
    And the batch b1 has the workspace w1
    And the workspace w1 holds no base merge
    When the person submits the batch b1
    Then the batches service refuses this request
    And the batches service names the batch b1

  @g11 @r11
  Scenario: A person's finding on a batch awaiting its merge reopens the batch
    Given a batch b1
    And the status of the batch b1 is `awaiting-merge`
    And a review finding r1
    When the person reopens the batch b1 with the review finding r1
    Then the batches service keeps the review r2
    And the batch b1 has the review r2
    And the review r2 holds the review finding r1
    And the batches service sets the status of the batch b1 to `building`

  @g12 @r12
  Scenario: A batch not awaiting its merge is not reopened
    Given a batch b1
    And the status of the batch b1 is not `awaiting-merge`
    And a review finding r1
    When the person reopens the batch b1 with the review finding r1
    Then the batches service refuses this request
    And the batches service names the batch b1

  @g13 @r13
  Scenario: A batch whose amended line its task built is submitted with the line built
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t2
    And the batch b1 has the task t2
    And the status of the task t2 is `done`
    And a workspace w1
    And the batch b1 has the workspace w1
    And an amendment a1
    And the amendment a1 cites the item i1
    And the workspace w1 holds the amendment a1
    And a scenario s1
    And the item i1 has the scenario s1
    And a task t1
    And the item i1 has the task t1
    And a workspace w2
    And the task t1 has the workspace w2
    And the scenario s1 succeeds in the workspace w2
    When the person submits the batch b1
    Then the batches service keeps the proposed change p1
    And the batch b1 has the proposed change p1
    And the batches service sets the status of the batch b1 to `in-review`
