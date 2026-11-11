# generated from spec/capabilities/batches.md by features generate; do not edit
Feature: Batches
  Narrator: a person or session building a batch

  @g9 @r9
  Scenario: The merge delivers
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a pull request p1
    And the batch b1 has the pull request p1
    When the person merges the pull request p1
    Then `work` sets the status of the item i1 to `delivered`
    And `work` sets the status of the batch b1 to `merged`

  @g11 @r11
  Scenario: The pull request cites its items
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    When the person runs `work batch review` on the batch b1
    Then the pull request p1 cites the item i1
    And `work` publishes the pull request p1

  @g14 @r14
  Scenario: `work batch start` writes the batch brief for a fresh agent
    When the person runs `work batch start`
    Then `work` writes the batch brief b1
    And `work` prints the batch brief b1

  @g15 @r15
  Scenario: `work batch abandon` removes the batch's review folders
    Given a review folder r1
    And the batch b1 has the review folder r1
    And a review folder r2
    And the batch b1 has the review folder r2
    When the person runs `work batch abandon` on the batch b1
    Then `work` removes the review folder r1
    And `work` removes the review folder r2

  @g22 @r22
  Scenario: `work batch start` picks a ready item that passes the readiness bar and has no dependency on an item that is not delivered
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 passes this readiness bar
    And the item i1 has no dependency
    When the person runs `work batch start`
    Then `work` picks the item i1
    And `work` sets the status of the item i1 to `in-batch`
    And the status of the batch b1 is `building`
    And `work` writes the batch b1
    And the batch b1 has the batch plan b2
    And `work` writes the batch plan b2

  @g23 @r23
  Scenario: A ready item that no longer passes the readiness bar is returned
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 does not pass this readiness bar
    When the person runs `work batch start`
    Then `work` sets the status of the item i1 to `shaped`

  @g24 @r24
  Scenario: A ready item with a dependency on an item that is neither ready nor delivered is not picked
    Given an item i1
    And the status of the item i1 is not `ready`
    And the status of the item i1 is not `delivered`
    And a dependency d1
    And the dependency d1 is on the item i1
    And the dependency d1 exists
    And an item i2
    And the status of the item i2 is `ready`
    And the item i2 has the dependency d1
    When the person runs `work batch start`
    Then `work` does not pick the item i2

  @g25 @r25
  Scenario: `work batch resume` carries on without a person
    Given a batch b1
    And the status of the batch b1 is `building`
    When the session s1 runs `work batch resume` on the batch b1
    Then the batch b1 has the batch plan b2
    And `work` uses the batch plan b2
    And `work` does not ask a question

  @g26 @r26
  Scenario: `work batch park` parks an item and leaves the rest building
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    When the session s1 runs `work batch park` on the item i1
    Then `work` sets the status of the item i1 to `needs-input`
    And the question q1 is on the item i1
    And `work` writes the question q1
    And `work` does not set the status of the batch b1 to `abandoned`

  @g28 @r28
  Scenario: `work batch abandon` returns the batch's items
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And an item i2
    And the batch b1 holds the item i2
    And the status of the item i2 is `in-batch`
    When the person runs `work batch abandon` on the batch b1
    Then `work` sets the status of the batch b1 to `abandoned`
    And `work` sets the status of the item i1 to `ready`
    And `work` sets the status of the item i2 to `ready`

  @g29 @r29
  Scenario: `work batch review` refuses a batch with a task that is not done
    Given a task t1
    And a batch b1
    And the batch b1 has the task t1
    And the status of the task t1 is not `done`
    When the person runs `work batch review` on the batch b1
    Then `work` refuses `work batch review`
    And `work` names the task t1

  @g30 @r30
  Scenario: `work batch review` refuses a commit that cites no item
    Given a task t1
    And a batch b1
    And the batch b1 has the task t1
    And a git branch g1
    And the task t1 has the git branch g1
    And a commit c1
    And the commit c1 cites no item
    And the git branch g1 has the commit c1
    When the person runs `work batch review` on the batch b1
    Then `work` refuses `work batch review`
    And `work` names the commit c1

  @g31 @r31
  Scenario: The merge removes the batch's review folders
    Given a pull request p1
    And a batch b1
    And the batch b1 has the pull request p1
    And a review folder r1
    And the batch b1 has the review folder r1
    And a review folder r2
    And the batch b1 has the review folder r2
    When the person merges the pull request p1
    Then `work` removes the review folder r1
    And `work` removes the review folder r2

  @g32 @r32
  Scenario: `work batch park` takes the parked item's lines out of the batch
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a git branch g1
    And the batch b1 has the git branch g1
    And a requirement r1
    And the item i1 has the requirement r1
    And the git branch g1 holds the requirement r1
    When the session s1 runs `work batch park` on the item i1
    Then `work` removes the requirement r1 from the git branch g1

  @g34 @r34
  Scenario: Another item's passing scenario does not hold up a task
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And an item i2
    And the batch b1 holds the item i2
    And the status of the item i2 is `in-batch`
    And a scenario s1
    And the item i2 has the scenario s1
    And a worktree w1
    And the task t1 has the worktree w1
    And the scenario s1 passes in the worktree w1
    When the session s2 runs `work batch done` on the task t1
    Then `work` sets the status of the task t1 to `done`

  @g35 @r35
  Scenario: `work batch review` publishes the pull request
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    When the person runs `work batch review` on the batch b1
    Then the batch b1 has the pull request p1
    And `work` publishes the pull request p1
    And `work` sets the status of the batch b1 to `in-review`

  @g36 @r36
  Scenario: `work batch status` prints where the batch stands
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a task t1
    And the batch b1 has the task t1
    When the person runs `work batch status` on the batch b1
    Then `work` prints the item i1
    And `work` prints the task t1
    And `work` prints the status of the task t1

  @g37 @r37
  Scenario: A parked item's commits stay out of the pull request
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `needs-input`
    And a commit c1
    And the commit c1 cites the item i1
    When the person runs `work batch review` on the batch b1
    Then the batch b1 has the pull request p1
    And the pull request p1 does not hold the commit c1
    And `work` publishes the pull request p1

  @g38 @r38
  Scenario: A parked item's failing scenario does not hold up another item's task
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And an item i2
    And the batch b1 holds the item i2
    And the status of the item i2 is `needs-input`
    And a scenario s1
    And the item i2 has the scenario s1
    And a worktree w1
    And the task t1 has the worktree w1
    And the scenario s1 fails in the worktree w1
    When the session s2 runs `work batch done` on the task t1
    Then `work` sets the status of the task t1 to `done`
