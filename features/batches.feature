# generated from spec/capabilities/batches.md by features generate; do not edit
Feature: Batches
  Narrator: the person

  @g50 @r50
  Scenario: Merging a batch's change delivers its items
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a proposed change p1
    And the batch b1 has the proposed change p1
    When the person merges the proposed change p1
    Then the batches service sets the status of the item i1 to `delivered`
    And the batches service sets the status of the batch b1 to `merged`

  @g51 @r51
  Scenario: A batch opened keeps and gives its brief
    Given a batch b1
    When the person opens the batch b1
    Then the batches service keeps the batch brief b2
    And the batches service returns the batch brief b2

  @g52 @r52
  Scenario: A batch abandoned keeps no review folder
    Given a batch b1
    And a review folder r1
    And the batch b1 has the review folder r1
    When the person abandons the batch b1
    Then the batches service does not keep the review folder r1

  @g53 @r53
  Scenario: A ready item that meets the bar and depends on nothing open goes into the batch opened
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And the item i1 has no dependency
    And a batch b1
    When the person opens the batch b1
    Then the batches service sets the status of the item i1 to `in-batch`
    And the batches service keeps the batch b2
    And the batch b2 holds the item i1
    And the batches service keeps the batch plan b3
    And the batch b2 has the batch plan b3

  @g54 @r54
  Scenario: A ready item that no longer meets the bar goes back to shaped
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 does not meet this readiness bar
    And a batch b1
    When the person opens the batch b1
    Then the batches service sets the status of the item i1 to `shaped`

  @g55 @r55
  Scenario: An item a ready item depends on and that is not ready stays out of the batch
    Given an item i1
    And the status of the item i1 is not `ready`
    And the status of the item i1 is not `delivered`
    And a dependency d1
    And the dependency d1 is on the item i1
    And the dependency d1 exists
    And an item i2
    And the status of the item i2 is `ready`
    And the item i2 has the dependency d1
    And a batch b1
    When the person opens the batch b1
    Then the batches service does not set the status of the item i2 to `in-batch`

  @g56 @r56
  Scenario: A batch resumed gives its plan and asks nothing
    Given a batch b1
    And the status of the batch b1 is `building`
    And a session s1
    When the session s1 resumes the batch b1
    Then the batches service returns the batch plan b2
    And the batch b1 has the batch plan b2
    And the batches service does not ask a question

  @g57 @r57
  Scenario: An item parked needs input and the batch goes on
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a session s1
    When the session s1 parks the item i1
    Then the batches service sets the status of the item i1 to `needs-input`
    And the batches service keeps the question q1
    And the question q1 is on the item i1
    And the batches service does not set the status of the batch b1 to `abandoned`

  @g58 @r58
  Scenario: A batch abandoned gives its items back as ready
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And an item i2
    And the batch b1 holds the item i2
    And the status of the item i2 is `in-batch`
    And an item i3
    And the batch b1 holds the item i3
    And the status of the item i3 is `shaped`
    When the person abandons the batch b1
    Then the batches service sets the status of the batch b1 to `abandoned`
    And the batches service sets the status of the item i1 to `ready`
    And the batches service sets the status of the item i2 to `ready`
    And the batches service does not set the status of the item i3 to `ready`

  @g59 @r59
  Scenario: A batch whose change is merged keeps no review folder
    Given a proposed change p1
    And a batch b1
    And the batch b1 has the proposed change p1
    And a review folder r1
    And the batch b1 has the review folder r1
    When the person merges the proposed change p1
    Then the batches service does not keep the review folder r1

  @g60 @r60
  Scenario: An item parked has its lines taken out of the batch's workspace
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a workspace w1
    And the batch b1 has the workspace w1
    And a requirement r1
    And the item i1 has the requirement r1
    And the workspace w1 holds the requirement r1
    And a session s1
    When the session s1 parks the item i1
    Then the batches service keeps the workspace w2
    And the batch b1 has the workspace w2
    And the workspace w2 does not hold the requirement r1

  @g61 @r61
  Scenario: A task finishes while a parked item's scenario breaks
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
    And a workspace w1
    And the task t1 has the workspace w1
    And the scenario s1 breaks in the workspace w1
    And a session s2
    When the session s2 finishes the task t1
    Then the batches service sets the status of the task t1 to `done`

  @g62 @r62
  Scenario: A task finishes while another item's scenario succeeds
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
    And a workspace w1
    And the task t1 has the workspace w1
    And the scenario s1 succeeds in the workspace w1
    And a session s2
    When the session s2 finishes the task t1
    Then the batches service sets the status of the task t1 to `done`

  @g63 @r63
  Scenario: A batch monitored gives its items, tasks and their status
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And a task t1
    And the batch b1 has the task t1
    When the person monitors the batch b1
    Then the batches service returns the item i1
    And the batches service returns the task t1
    And the batches service returns the status of the task t1

  @g64 @r64
  Scenario: A batch opened with a universal condition keeps the universal conditions in the language
    Given `universal` does not exist
    And an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a universal condition u1
    And the item i1 holds the universal condition u1
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps `universal`
    And the batches service sets the language of `universal` to `codified-2`

  @g65 @r65
  Scenario: Merging a batch's change resolves the accepted context request of its item
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a request line r1
    And a context request c1
    And the context request c1 has the request line r1
    And the item i1 has the request line r1
    And the status of the context request c1 is `accepted`
    And a proposed change p1
    And the batch b1 has the proposed change p1
    When the person merges the proposed change p1
    Then the batches service sets the status of the context request c1 to `delivered`
    And the batches service keeps the resolution r2
    And the batches service sets the side of the context request c1 to `asker`
    And the batches service keeps the entry e1
    And the entry e1 is on the context request c1

  @g66 @r66
  Scenario: A task whose chore breaks is not finished
    Given a task t1
    And an item i1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a chore c1
    And the item i1 holds the chore c1
    And a workspace w1
    And the task t1 has the workspace w1
    And the chore c1 breaks in the workspace w1
    And a session s1
    When the session s1 finishes the task t1
    Then the batches service refuses this request
    And the batches service names the chore c1

  @g67 @r67
  Scenario: A task that touches a file outside its chore is not finished
    Given a task t1
    And an item i1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a chore c1
    And the item i1 holds the chore c1
    And a workspace w1
    And the task t1 has the workspace w1
    And a kept change k1
    And the workspace w1 holds the kept change k1
    And a file f1
    And the chore c1 does not hold the file f1
    And the kept change k1 touches the file f1
    And a session s1
    When the session s1 finishes the task t1
    Then the batches service refuses this request
    And the batches service names the file f1

  @g68 @r68
  Scenario: A batch opened keeps a brief that holds each chore
    Given an item i1
    And the status of the item i1 is `ready`
    And a chore c1
    And the item i1 holds the chore c1
    And the item i1 meets this readiness bar
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps the batch brief b2
    And the batch brief b2 holds the chore c1

  @g70 @r70
  Scenario: A task finishes while a parked item's line is out of the batch
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
    And a workspace w1
    And the batch b1 has the workspace w1
    And a requirement r1
    And the workspace w1 does not hold the requirement r1
    And the item i2 has the requirement r1
    And a scenario s1
    And the item i2 has the scenario s1
    And a workspace w2
    And the task t1 has the workspace w2
    And the scenario s1 breaks in the workspace w2
    And a session s2
    When the session s2 finishes the task t1
    Then the batches service sets the status of the task t1 to `done`

  @g71 @r71
  Scenario: A batch opened keeps each line's logical form in the corpus
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And the item i1 has the requirement r1
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a batch b1
    When the person opens the batch b1
    Then this corpus holds the logical form l1
    And the batches service keeps the logical form l1

  @g72 @r72
  Scenario: A batch opened takes a retired requirement out of the corpus
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a requirement r2
    And this corpus holds the requirement r2
    And the requirement r2 has the requirement id r1
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps the corpus c1
    And the corpus c1 does not hold the requirement r2

  @g73 @r73
  Scenario: A batch opened keeps the catalogue entry of each rule its lines use
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And the item i1 has the requirement r1
    And a rule r2
    And the requirement r1 uses the rule r2
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps the catalogue entry c1
    And the rule r2 has the catalogue entry c1

  @g74 @r74
  Scenario: A batch opened keeps the construct catalogue its lines use
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And the item i1 has the requirement r1
    And a construct c1
    And the requirement r1 uses the construct c1
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps this construct catalogue

  @g75 @r75
  Scenario: A batch opened keeps no construct catalogue for lines that use no construct
    Given no item whose status is `ready` exists
    And no construct catalogue exists
    And a batch b1
    When the person opens the batch b1
    Then the batches service does not keep a construct catalogue

  @g76 @r76
  Scenario: A new capability is laid in 0.38's form: area:, specifies:, no empty ## Terms, one ## Composition
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a capability c1
    And the item i1 holds the capability c1
    And a batch b1
    When the person opens the batch b1
    Then the capability c1 conforms to the capability form
    And the batches service keeps the capability c1
    And the batches service keeps the index file i2
    And the index file i2 conforms to the index form
