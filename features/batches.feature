# generated from spec/capabilities/batches.md by features generate; do not edit
Feature: Batches
  Narrator: the person

  @g52 @r52
  Scenario: A batch abandoned keeps no review folder
    Given a batch b1
    And a review folder r1
    And the batch b1 has the review folder r1
    When the person abandons the batch b1
    Then the batches service does not keep the review folder r1

  @g56 @r56
  Scenario: A batch resumed gives its plan and asks nothing
    Given a batch b1
    And the status of the batch b1 is `building`
    And a session s1
    And a batch plan b2
    And the batch b1 has the batch plan b2
    When the session s1 resumes the batch b1
    Then the batches service returns the batch plan b2
    And the batches service does not ask a question

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

  @g77 @r77
  Scenario: A task finishes with its tests run by the workspace's virtual environment
    Given a task t1
    And an item i1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a workspace w1
    And the task t1 has the workspace w1
    And a virtual environment v1
    And the workspace w1 holds the virtual environment v1
    And a scenario s1
    And the item i1 has the scenario s1
    And the scenario s1 succeeds in the workspace w1
    And a session s2
    When the session s2 finishes the task t1
    Then the batches service sets the status of the task t1 to `done`

  @g78 @r78
  Scenario: A task finishes while a scenario its change does not reach breaks
    Given a task t1
    And an item i1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a workspace w1
    And the task t1 has the workspace w1
    And a scenario s1
    And the scenario s1 breaks in the workspace w1
    And a capability c1
    And the scenario s1 has the capability c1
    And the item i1 holds no requirement id in the capability c1
    And no kept change in the workspace w1 touches a feature of the capability c1
    And a session s2
    When the session s2 finishes the task t1
    Then the batches service sets the status of the task t1 to `done`

  @g83 @r83
  Scenario: Amending an item that is not in a batch is refused
    Given an item i1
    And the status of the item i1 is not `in-batch`
    When the person amends the item i1
    Then the batches service refuses this request
    And the batches service names the item i1

  @g84 @r84
  Scenario: `work settings set` writes a setting in its own table
    Given a setting s1
    And a setting value s2
    When the person configures the setting s1 with the setting value s2
    Then the batches service keeps the settings file s3
    And the settings file s3 holds the setting s1
    And the settings file s3 conforms to the delivery settings form
    And the batches service completes this request

  @g85 @r85
  Scenario: `work settings set` refuses a setting the plugin does not read
    Given a setting s1
    And the setting s1 does not conform to the delivery settings form
    When the person configures the setting s1
    Then the batches service refuses this request
    And the batches service names the setting s1

  @g86 @r86
  Scenario: `work settings set` refuses a value of the wrong type
    Given a setting value s2
    And the setting value s2 does not conform to the delivery settings form
    And a setting s1
    When the person configures the setting s1 with the setting value s2
    Then the batches service refuses this request
    And the batches service names the setting value s2

  @g96 @r96
  Scenario: An in-batch item amended that does not meet the readiness bar is refused and nothing changes
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And the item i1 does not meet this readiness bar
    When the person amends the item i1
    Then the batches service refuses this request
    And the batches service names the item i1
    # entailed: U17

  @g98 @r98
  Scenario: A batch opened keeps a brief that holds each batch rule of the settings file
    Given a batch rule b1
    And a settings file s1
    And the settings file s1 holds the batch rule b1
    And a batch b2
    When the person opens the batch b2
    Then the batches service keeps the batch brief b3
    And the batch brief b3 holds the batch rule b1

  @g99 @r99
  Scenario: A batch opened with no batch rule keeps a brief that holds none
    Given no settings file holds a batch rule
    And a batch b1
    And a batch rule b3
    When the person opens the batch b1
    Then the batches service keeps the batch brief b2
    And the batch brief b2 holds no batch rule

  @g100 @r100
  Scenario: Merging a batch's change delivers its items
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a proposed change p1
    And the batch b1 has the proposed change p1
    When the person merges the proposed change p1
    Then the batches service delivers the item i1
    And the batches service sets the status of the batch b1 to `merged`

  @g102 @r102
  Scenario: Every batch summary states its cost and timing
    Given a proposed change p1
    And a batch b1
    And the batch b1 has the proposed change p1
    And a batch summary b2
    And the batch b1 has the batch summary b2
    And a review folder r1
    And the batch b1 has the review folder r1
    When the person merges the proposed change p1
    Then the batches service does not keep the review folder r1
    And the batches service returns the batch summary b2

  @g104 @r104
  Scenario: Every batch brief holds the batch summary form
    Given a batch b1
    And a batch summary form b2
    And a batch brief b3
    When the person opens the batch b1
    Then the batches service keeps the batch brief b3
    And the batch brief b3 holds the batch summary form b2
    And the batches service returns the batch brief b3

  @g105 @r105
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
    Then the batches service resolves the context request c1

  @g109 @r109
  Scenario: A ready item whose new line's scenario passes on the lay is reopened
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And the item i1 has the requirement r1
    And the requirement r1 retires no requirement id
    And a scenario s1
    And the item i1 has the scenario s1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    And the scenario s1 refers to the requirement id r2
    And a workspace w1
    And a batch b1
    And the batch b1 has the workspace w1
    And the scenario s1 succeeds in the workspace w1
    When the person opens the batch b1
    Then the batches service reopens the item i1
    And the batches service names the scenario s1

  @g110 @r110
  Scenario: An item a ready item depends on and that is not ready is not allocated
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
    Then the batches service does not allocate the item i2

  @g111 @r111
  Scenario: An item parked is suspended and the batch goes on
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a session s1
    When the session s1 parks the item i1
    Then the batches service suspends the item i1 with the question q1
    And the batches service does not set the status of the batch b1 to `abandoned`

  @g112 @r112
  Scenario: A batch abandoned restores its items
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
    And the batches service restores the item i1
    And the batches service restores the item i2
    And the batches service does not restore the item i3

  @g125 @r125
  Scenario: An item amended with a review finding keeps a change for the finding, which its review accepts
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a review r1
    And the batch b1 has the review r1
    And a review finding r2
    And the review r1 holds the review finding r2
    When the person amends the item i1 with the review finding r2
    Then the batches service keeps the kept change k1
    And the kept change k1 is for the review finding r2

  @g131 @r131
  Scenario: A ready item whose change would take the batch past the review limit is not allocated, whether or not it meets the bar
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 exceeds the review limit
    And a batch b1
    When the person opens the batch b1
    Then the batches service does not allocate the item i1

  @g135 @r135
  Scenario: A batch awaiting its merge tells the driver to stop
    Given a batch b1
    And the status of the batch b1 is `awaiting-merge`
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `stop`

  @g141 @r141
  Scenario: A batch whose every task is done asks the driver to submit it
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `submit batch`

  @g143 @r143
  Scenario: A batch with a failed task of an in-batch item asks the driver to park the task's item
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `failed`
    And the status of the item i1 is `in-batch`
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `park item`
    And the batches service returns the task t1

  @g144 @r144
  Scenario: A batch with a built running task and no failed task asks the driver to finish the task
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And the status of the item i1 is `in-batch`
    And a workspace w1
    And the task t1 has the workspace w1
    And a kept change k1
    And the kept change k1 cites the item i1
    And the workspace w1 holds the kept change k1
    And no task of the batch b1 whose status is `failed` exists
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `finish task`
    And the batches service returns the task t1

  @g147 @r147
  Scenario: A batch in review asks the driver to review its change with the review folder and its findings file
    Given a batch b1
    And the status of the batch b1 is `in-review`
    And a review folder r1
    And the batch b1 has the review folder r1
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `review change`
    And the batches service returns the review folder r1
    And the batches service returns the findings file f1
    And the review folder r1 holds the findings file f1

  @g148 @r148
  Scenario: A batch with a finding to fix now that no kept change is for asks the driver to fix the finding
    Given a batch b1
    And the status of the batch b1 is `building`
    And a review r1
    And the batch b1 has the review r1
    And a review finding r2
    And the triage of the review finding r2 is `fix now`
    And the review r1 holds the review finding r2
    And no kept change is for the review finding r2
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `fix finding`
    And the batches service returns the review finding r2

  @g150 @r150
  Scenario: A running task whose only kept change citing its item is an amendment asks the driver to build it
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And the status of the item i1 is `in-batch`
    And a workspace w1
    And the task t1 has the workspace w1
    And an amendment a1
    And the amendment a1 cites the item i1
    And the workspace w1 holds the amendment a1
    And a kept change k1
    And the kept change k1 cites the item i1
    And the workspace w1 holds the kept change k1
    And no task of the batch b1 whose status is `failed` exists
    And a batch brief b2
    And the batch b1 has the batch brief b2
    When the driver polls the batch b1
    Then the batches service returns the batch step b3
    And the instruction of the batch step b3 is `build task`
    And the batches service returns the task t1
    And the batches service returns the batch brief b2

  @g153 @r153
  Scenario: A batch with pending tasks and no failed or running task asks the driver to prepare every pending task
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `pending`
    And a task t2
    And the item i1 has the task t2
    And the status of the task t2 is `pending`
    And no task of the batch b1 whose status is `failed` exists
    And no task of the batch b1 whose status is `running` exists
    And a task t3
    And the batch b1 has the task t3
    And the status of the task t3 is `pending`
    And a task t4
    And the batch b1 has the task t4
    And the status of the task t4 is `pending`
    And a task t5
    And the batch b1 has the task t5
    And the status of the task t5 is `done`
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `prepare task`
    And the batches service returns the task t3
    And the batches service returns the task t4
    And the batches service does not return the task t5

  @g158 @r158
  Scenario: A batch whose task branches conflict is polled for the later item's task and the file
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    And an item i1
    And the batch b1 holds the item i1
    And a kept change k1
    And the kept change k1 cites the item i1
    And a file f1
    And the kept change k1 touches the file f1
    And a kept change k2
    And the kept change k1 conflicts with the kept change k2
    And a task t2
    And the item i1 has the task t2
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `fix task`
    And the batches service returns the task t2
    And the batches service returns the file f1

  @g159 @r159
  Scenario: A batch with running tasks none of which is built asks the driver to build every running task with its brief
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a task t2
    And the item i1 has the task t2
    And the status of the task t2 is `running`
    And no task of the batch b1 whose status is `failed` exists
    And no workspace of a task of the batch b1 holds a kept change that cites an item in the batch b1
    And a batch brief b2
    And the batch b1 has the batch brief b2
    And a task t3
    And the batch b1 has the task t3
    And the status of the task t3 is `running`
    And a task t4
    And the batch b1 has the task t4
    And the status of the task t4 is `running`
    And a task t5
    And the batch b1 has the task t5
    And the status of the task t5 is `pending`
    When the driver polls the batch b1
    Then the batches service returns the batch step b3
    And the instruction of the batch step b3 is `build task`
    And the batches service returns the task t3
    And the batches service returns the task t4
    And the batches service does not return the task t5
    And the batches service returns the batch brief b2

  @g161 @r161
  Scenario: A batch whose item's scenario breaks with no fix is polled for the item's task
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `done`
    And a task t2
    And the batch b1 has the task t2
    And the status of the task t2 is `done`
    And a scenario s1
    And the item i1 has the scenario s1
    And a workspace w1
    And the batch b1 has the workspace w1
    And the scenario s1 breaks in the workspace w1
    And no fix exists
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `fix task`
    And the batches service returns the task t1

  @g162 @r162
  Scenario: A batch whose other scenario breaks with no fix is polled to look at the failure
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    And a workspace w1
    And the batch b1 has the workspace w1
    And a scenario s1
    And the scenario s1 breaks in the workspace w1
    And no scenario of an item in the batch b1 breaks in the workspace w1
    And no fix exists
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `look at failure`
    And the batches service returns the scenario s1

  @g163 @r163
  Scenario: A batch whose failure has a fix is polled for its submit
    Given a batch b1
    And the status of the batch b1 is `building`
    And a task t1
    And the batch b1 has the task t1
    And the status of the task t1 is `done`
    And a workspace w1
    And the batch b1 has the workspace w1
    And a scenario s1
    And the scenario s1 breaks in the workspace w1
    And a fix f1
    And the fix f1 exists
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `submit batch`

  @g165 @r165
  Scenario: A building batch whose every item is parked is polled for its abandonment
    Given a batch b1
    And the status of the batch b1 is `building`
    And an item i1
    And the batch b1 holds the item i1
    And the status of the item i1 is `needs-input`
    When the driver polls the batch b1
    Then the batches service returns the batch step b2
    And the instruction of the batch step b2 is `abandon batch`

  @g168 @r168
  Scenario: An item whose port outcomes were unhandled before it is allocated at the opening
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And the item i1 has no dependency
    And the item i1 does not exceed the review limit
    And a port line p1
    And an operation o1
    And the port line p1 governs the operation o1
    And the item i1 holds the port line p1
    And a port line p2
    And the port line p2 governs the operation o1
    And the item i1 does not hold the port line p2
    And an operation outcome o2
    And the operation o1 has the operation outcome o2
    And no core line handles the operation outcome o2
    And no port line excludes the operation outcome o2
    And a batch b1
    When the person opens the batch b1
    Then the batches service allocates the item i1

  @g171 @r171
  Scenario: An in-batch item amended with no review finding given keeps a change for the review finding its batch holds open
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a review r1
    And the batch b1 has the review r1
    And a review finding r2
    And the review r1 holds the review finding r2
    When the person amends the item i1
    Then the batches service keeps the kept change k1
    And the kept change k1 is for the review finding r2

  @g173 @r173
  Scenario: A batch opened supersedes each accepted decision a laid line's retirement leaves unenforced
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And the item i1 holds the requirement r1
    And a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a requirement r2
    And the requirement r2 enforces the design-decision d1
    And a requirement id r3
    And the requirement r2 has the requirement id r3
    And the requirement r1 retires the requirement id r3
    And a batch b1
    When the person opens the batch b1
    Then the batches service sets the status of the design-decision d1 to `superseded`
    And the batches service keeps the design-decision d2
    And the design-decision d2 supersedes the design-decision d1
    And the batches service names the design-decision d2

  @g177 @r177
  Scenario: A batch opened with two items retiring ids of one decision supersedes it by one decision every retiring line enforces
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And the item i1 holds the requirement r1
    And a design-decision d1
    And the status of the design-decision d1 is `accepted`
    And a requirement r2
    And the requirement r2 enforces the design-decision d1
    And a requirement id r3
    And the requirement r2 has the requirement id r3
    And the requirement r1 retires the requirement id r3
    And a requirement r4
    And the requirement r4 enforces the design-decision d1
    And a requirement id r5
    And the requirement r4 has the requirement id r5
    And an item i2
    And the item i2 meets this readiness bar
    And a requirement r6
    And the item i2 holds the requirement r6
    And the requirement r6 retires the requirement id r5
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps the design-decision d2
    And the requirement r6 enforces the design-decision d2

  @g187 @r187
  Scenario: A ready item that no longer meets the readiness bar at opening is reopened naming each bar check it does not meet
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 does not meet this readiness bar
    And the item i1 does not exceed the review limit
    And a batch b1
    And a bar check b2
    And the item i1 does not meet the bar check b2
    And a bar check b3
    And the item i1 does not meet the bar check b3
    When the person opens the batch b1
    Then the batches service reopens the item i1
    And the batches service names the bar check b2
    And the batches service names the bar check b3

  @g190 @r190
  Scenario: An item picked whose requirement id a capability holds keeps its pack term once renumbered
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a term t1
    And a pack p1
    And the pack p1 has the term t1
    And the item i1 holds the term t1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a capability c1
    And the capability c1 holds the requirement id r1
    And a batch b1
    When the person opens the batch b1
    Then the pack p1 has the term t1
    And the batches service keeps the pack p1

  @g191 @r191
  Scenario: An item picked whose requirement id a capability holds keeps its operation table once renumbered
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And an operation table o1
    And the item i1 holds the operation table o1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a capability c1
    And the capability c1 holds the requirement id r1
    And a batch b1
    When the person opens the batch b1
    Then the batches service keeps the adapter contract a1
    And the adapter contract a1 holds the operation table o1

  @g192 @r192
  Scenario: An item picked whose requirement id a capability holds keeps the term it moves once renumbered
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a term t1
    And an element e1
    And the term t1 means the element e1
    And the item i1 moves the term t1
    And an area a1
    And the area a1 holds the element e1
    And a requirement id r1
    And the item i1 holds the requirement id r1
    And a capability c1
    And the capability c1 holds the requirement id r1
    And a batch b1
    When the person opens the batch b1
    Then the area a1 holds the term t1
    And the batches service keeps the area a1

  @g193 @r193
  Scenario: A ready item whose line retires a requirement of another capability is not reopened when its scenario passes on the lay
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the item i1 holds the requirement r1
    And a scenario s1
    And the item i1 has the scenario s1
    And a requirement id r2
    And the requirement r1 has the requirement id r2
    And the scenario s1 refers to the requirement id r2
    And a workspace w1
    And a batch b1
    And the batch b1 has the workspace w1
    And the scenario s1 succeeds in the workspace w1
    And a requirement r3
    And a capability c2
    And the capability c2 has the requirement r3
    And a requirement id r4
    And the requirement r3 has the requirement id r4
    And the requirement r1 retires the requirement id r4
    When the person opens the batch b1
    Then the batches service does not reopen the item i1

  @g194 @r194
  Scenario: An item allocated to a batch is applied to the specification of its task's workspace
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    And the item i1 has no dependency
    And the item i1 does not exceed the review limit
    And a batch b1
    When the person opens the batch b1
    Then the batches service allocates the item i1
    And the batches service keeps the batch b2
    And the batch b2 holds the item i1
    And the batches service keeps the batch plan b3
    And the batch b2 has the batch plan b3
    And the item i1 has the task t1
    And the task t1 has the workspace w1
    And the batches service applies the item i1 to the specification s1
    And the workspace w1 has the specification s1

  @g195 @r195
  Scenario: A specification the specification service has applied an item to is validated with the item
    Given an item i1
    And a specification s1
    And the batches service applies the item i1 to the specification s1
    When the specification service completes the request to apply the item i1 to the specification s1
    Then the batches service validates the specification s1 with the item i1

  @g196 @r196
  Scenario: An item whose task's specification fails validation is reopened naming the rules it violates
    Given a task t1
    And an item i1
    And the item i1 has the task t1
    And a workspace w1
    And the task t1 has the workspace w1
    And a specification s1
    And the workspace w1 has the specification s1
    And the batches service validates the specification s1
    And a rule r2
    And a requirement r3
    And the item i1 has the requirement r3
    And the requirement r3 violates the rule r2
    And a rule r4
    And a requirement r5
    And the item i1 has the requirement r5
    And the requirement r5 violates the rule r4
    And a rule r6
    And a requirement r7
    And the item i1 has the requirement r7
    And the requirement r7 does not violate the rule r6
    When the specification service fails the request to validate the specification s1
    Then the batches service reopens the item i1
    And the batches service names the rule r2
    And the batches service names the rule r4
    And the batches service does not name the rule r6

  @g197 @r197
  Scenario: An item whose task's specification is validated is kept in a change that cites it
    Given a task t1
    And an item i1
    And the item i1 has the task t1
    And a workspace w1
    And the task t1 has the workspace w1
    And a specification s1
    And the workspace w1 has the specification s1
    And the batches service validates the specification s1
    When the specification service completes the request to validate the specification s1
    Then the batches service keeps the kept change k1
    And the kept change k1 cites the item i1

  @g198 @r198
  Scenario: An amended item is applied again to the specification of its task's workspace
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    When the person amends the item i1
    Then the task t1 has the workspace w1
    And the batches service applies the item i1 to the specification s1
    And the workspace w1 has the specification s1

  @g199 @r199
  Scenario: An in-batch item amended has its features written by the generator its task's workspace holds
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a requirement r1
    And the item i1 holds the requirement r1
    And a workspace w1
    And the task t1 has the workspace w1
    And a feature generator f1
    And the workspace w1 has the feature generator f1
    And a feature f2
    And a workspace w2
    When the person amends the item i1
    Then the feature generator f1 has the feature f2
    And the batches service keeps the workspace w2
    And the task t1 has the workspace w2
    And the workspace w2 holds the feature f2

  @g200 @r200
  Scenario: An in-batch item amended keeps a corpus of the corpus form in its task's workspace
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a requirement r1
    And the item i1 holds the requirement r1
    And this corpus holds the requirement r1
    When the person amends the item i1
    Then the batches service keeps the corpus c1
    And the corpus c1 conforms to the corpus form
    And the batches service keeps the workspace w1
    And the task t1 has the workspace w1
    And the workspace w1 holds the corpus c1

  @g201 @r201
  Scenario: An in-batch item amended while its task's feature generator is unresponsive is refused, naming the generator
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And the status of the task t1 is `running`
    And a workspace w1
    And the task t1 has the workspace w1
    And a feature generator f1
    And the workspace w1 has the feature generator f1
    And the responsiveness of the feature generator f1 is `unresponsive`
    When the person amends the item i1
    Then the batches service refuses this request
    And the batches service names the feature generator f1
    # entailed: U17

  @g202 @r202
  Scenario: A dependent item's task workspace holds the lines of the item it depends on
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `in-batch`
    And a task t1
    And the item i1 has the task t1
    And a workspace w1
    And the task t1 has the workspace w1
    And a requirement r1
    And an item i2
    And the item i2 holds the requirement r1
    And a dependency d1
    And the dependency d1 is on the item i2
    And the item i1 has the dependency d1
    When the person opens the batch b1
    Then the workspace w1 holds the requirement r1
    And the batches service keeps the workspace w1
