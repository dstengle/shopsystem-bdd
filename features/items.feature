# generated from spec/capabilities/items.md by features generate; do not edit
Feature: Items
  Narrator: the person

  @g1 @r1
  Scenario: A shaped item that meets the readiness bar is readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And the item i1 meets this readiness bar
    When the person readies the item i1
    Then the backlog service sets the status of the item i1 to `ready`

  @g2 @r2
  Scenario: An item that does not meet the readiness bar is refused, naming each bar check it does not meet
    Given an item i1
    And the status of the item i1 is `shaped`
    And the item i1 does not meet this readiness bar
    And a bar check b1
    And the item i1 does not meet the bar check b1
    And a bar check b2
    And the item i1 does not meet the bar check b2
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the bar check b1
    And the backlog service names the bar check b2

  @g4 @r4
  Scenario: Readying an item asks the person nothing
    Given an item i1
    When the person readies the item i1
    Then the backlog service does not ask a question

  @g5 @r5
  Scenario: An item a term of which violates a rule is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a term t1
    And the item i1 holds the term t1
    And a rule r1
    And the term t1 violates the rule r1
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the term t1
    And the backlog service names the rule r1

  @g6 @r6
  Scenario: An item a requirement of which has no translation is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a requirement r1
    And the item i1 holds the requirement r1
    And the requirement r1 has no translation
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the requirement r1

  @g7 @r7
  Scenario: An item a universal condition of which has no translation is not readied
    Given `universal` does not exist
    And an item i1
    And the status of the item i1 is `shaped`
    And a universal condition u1
    And the item i1 holds the universal condition u1
    And the universal condition u1 has no translation
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the universal condition u1

  @g8 @r8
  Scenario: Every requirement of an item that has no parse and every one that has no translation is named at once
    Given an item i1
    And the status of the item i1 is `shaped`
    And a requirement r1
    And the item i1 holds the requirement r1
    And the requirement r1 has no parse
    And a requirement r2
    And the item i1 holds the requirement r2
    And the requirement r2 has no translation
    And a requirement r3
    And the item i1 holds the requirement r3
    And the requirement r3 has no parse
    And a requirement r4
    And the item i1 holds the requirement r4
    And the requirement r4 has no parse
    And a requirement r5
    And the requirement r5 has no parse
    And the item i1 does not hold the requirement r5
    And a requirement r6
    And the item i1 holds the requirement r6
    And the requirement r6 has no translation
    And a requirement r7
    And the item i1 holds the requirement r7
    And the requirement r7 has no translation
    And a requirement r8
    And the requirement r8 has no translation
    And the item i1 does not hold the requirement r8
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the requirement r3
    And the backlog service names the requirement r4
    And the backlog service does not name the requirement r5
    And the backlog service names the requirement r6
    And the backlog service names the requirement r7
    And the backlog service does not name the requirement r8

  @g9 @r9
  Scenario: A shaped item that holds a chore and no requirement is readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a chore c1
    And the item i1 holds the chore c1
    And the item i1 holds no requirement
    When the person readies the item i1
    Then the backlog service sets the status of the item i1 to `ready`

  @g10 @r10
  Scenario: An item a requirement group of which violates a rule is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a requirement group r1
    And the item i1 holds the requirement group r1
    And a rule r2
    And the requirement group r1 violates the rule r2
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the requirement group r1
    And the backlog service names the rule r2

  @g11 @r11
  Scenario: A dependency linked to an item is kept
    Given an item i1
    When the person links the item i1
    Then the backlog service keeps the dependency d1
    And the dependency d1 is on the item i1

  @g12 @r12
  Scenario: An item shown gives its title
    Given an item i1
    And a title t1
    And the item i1 has the title t1
    When the person shows the item i1
    Then the backlog service returns the title t1

  @g13 @r13
  Scenario: An idea noted is kept as an item
    Given an idea i1
    When the person notes the idea i1
    Then the backlog service keeps the item i2
    And the status of the item i2 is `idea`

  @g14 @r14
  Scenario: An idea shaped becomes shaped
    Given an item i1
    And the status of the item i1 is `idea`
    When the person shapes the item i1
    Then the backlog service sets the status of the item i1 to `shaped`

  @g15 @r15
  Scenario: Only an idea is shaped
    Given an item i1
    And the status of the item i1 is not `idea`
    When the person shapes the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g16 @r16
  Scenario: An item rated keeps its value, urgency and size
    Given an item i1
    When the person rates the item i1 with the value `high-value` and the urgency `low-urgency` and the size `small`
    Then the backlog service sets the value of the item i1 to `high-value`
    And the backlog service sets the urgency of the item i1 to `low-urgency`
    And the backlog service sets the size of the item i1 to `small`
    And the backlog service keeps the item i1

  @g17 @r17
  Scenario: The backlog gives an open item's dependencies
    Given an item i1
    And the status of the item i1 is not `delivered`
    And a dependency d1
    And the dependency d1 is on the item i1
    And the dependency d1 exists
    And an item i2
    And the item i2 has the dependency d1
    When the person lists this backlog
    Then the backlog service returns the item i2
    And the backlog service returns the dependency d1

  @g18 @r18
  Scenario: An open item withdrawn becomes withdrawn (case 1)
    Given an item i1
    And the status of the item i1 is `idea`
    When the person withdraws the item i1
    Then the backlog service sets the status of the item i1 to `withdrawn`

  @g18 @r18
  Scenario: An open item withdrawn becomes withdrawn (case 2)
    Given an item i1
    And the status of the item i1 is `shaped`
    When the person withdraws the item i1
    Then the backlog service sets the status of the item i1 to `withdrawn`

  @g18 @r18
  Scenario: An open item withdrawn becomes withdrawn (case 3)
    Given an item i1
    And the status of the item i1 is `ready`
    When the person withdraws the item i1
    Then the backlog service sets the status of the item i1 to `withdrawn`

  @g18 @r18
  Scenario: An open item withdrawn becomes withdrawn (case 4)
    Given an item i1
    And the status of the item i1 is `needs-input`
    When the person withdraws the item i1
    Then the backlog service sets the status of the item i1 to `withdrawn`

  @g19 @r19
  Scenario: An idea or a shaped item declined becomes refused (case 1)
    Given an item i1
    And the status of the item i1 is `idea`
    When the person declines the item i1
    Then the backlog service sets the status of the item i1 to `refused`

  @g19 @r19
  Scenario: An idea or a shaped item declined becomes refused (case 2)
    Given an item i1
    And the status of the item i1 is `shaped`
    When the person declines the item i1
    Then the backlog service sets the status of the item i1 to `refused`

  @g20 @r20
  Scenario: An item that needs input answered becomes shaped
    Given an item i1
    And the status of the item i1 is `needs-input`
    When the person answers the item i1
    Then the backlog service sets the status of the item i1 to `shaped`
    And the backlog service keeps the item i1

  @g21 @r21
  Scenario: The backlog gives the questions of an item that needs input
    Given an item i1
    And the status of the item i1 is `needs-input`
    And a question q1
    And the question q1 is on the item i1
    And a question q2
    And the question q2 is on the item i1
    And a question q3
    And the question q3 is not on the item i1
    When the person lists this backlog
    Then the backlog service returns the item i1
    And the backlog service returns the question q1
    And the backlog service returns the question q2
    And the backlog service does not return the question q3

  @g22 @r22
  Scenario: An idea is kept while the shared store rejects a change
    Given the availability of this shared store is `rejecting`
    And an idea i1
    When the person notes the idea i1
    Then the backlog service keeps the item i2
    And the status of the item i2 is `idea`
    And the backlog service names this shared store
    And the backlog service completes this request

  @g23 @r23
  Scenario: An idea is kept while the shared store does not answer
    Given the availability of this shared store is `unreachable`
    And an idea i1
    When the person notes the idea i1
    Then the backlog service keeps the item i2
    And the status of the item i2 is `idea`
    And the backlog service names this shared store
    And the backlog service completes this request

  @g24 @r24
  Scenario: No idea is noted in the workspace of a task
    Given a workspace w1
    And a task t1
    And the task t1 has the workspace w1
    And the workspace w1 holds this repository
    And an idea i1
    When the person notes the idea i1
    Then the backlog service refuses this request
    And the backlog service names the task t1

  @g25 @r25
  Scenario: An idea noted in a workspace keeps its shared workspace of another name
    Given a workspace name w2
    And a workspace w1
    And the workspace w1 has the workspace name w2
    And the workspace w1 holds this repository
    And a shared workspace s1
    And the workspace w1 has the shared workspace s1
    And a workspace name w3
    And the shared workspace s1 has the workspace name w3
    And an idea i1
    When the person notes the idea i1
    Then the backlog service keeps the item i2
    And the status of the item i2 is `idea`
    And the backlog service keeps the shared workspace s1

  @g26 @r26
  Scenario: The backlog gives each item's title, status, provenance and ratings
    Given an item i1
    And the item i1 exists
    And a title t1
    And the item i1 has the title t1
    When the person lists this backlog
    Then the backlog service returns the item i1
    And the backlog service returns the title t1
    And the backlog service returns the status of the item i1
    And the backlog service returns the provenance of the item i1
    And the backlog service returns the value of the item i1
    And the backlog service returns the urgency of the item i1
    And the backlog service returns the size of the item i1

  @g27 @r27
  Scenario: An idea with no shaping note is not shaped without a note
    Given an item i1
    And the status of the item i1 is `idea`
    And the item i1 has no shaping note
    When the person shapes the item i1 without a note
    Then the backlog service refuses this request
    And the backlog service names the note

  @g28 @r28
  Scenario: The backlog names the note an idea with no shaping note waits on
    Given an item i1
    And the status of the item i1 is `idea`
    And the item i1 has no shaping note
    When the person lists this backlog
    Then the backlog service returns the item i1
    And the backlog service names the note

  @g29 @r29
  Scenario: A session that starts is told every item and batch
    Given a session s1
    And an item i1
    And an item i2
    And a title t1
    And an item i3
    And the item i3 has the title t1
    And a title t2
    And an item i4
    And the item i4 has the title t2
    And a title t3
    And an item i5
    And the item i5 does not have the title t3
    And a batch b1
    And a batch b2
    When the session s1 starts
    Then the backlog service notifies the session s1 of the item i1
    And the backlog service notifies the session s1 of the item i2
    And the backlog service notifies the session s1 of the title t1
    And the backlog service notifies the session s1 of the title t2
    And the backlog service does not notify the session s1 of the title t3
    And the backlog service notifies the session s1 of the batch b1
    And the backlog service notifies the session s1 of the batch b2

  @g30 @r30
  Scenario: An item with a request line not settled is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a request line r1
    And the item i1 has the request line r1
    And the line outcome of the request line r1 is not `accepted`
    And the line outcome of the request line r1 is not `refused`
    And the line outcome of the request line r1 is not `withdrawn`
    And a session s1
    When the session s1 readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the request line r1

  @g31 @r31
  Scenario: A ready item reopened becomes shaped
    Given an item i1
    And the status of the item i1 is `ready`
    When the person reopens the item i1
    Then the backlog service sets the status of the item i1 to `shaped`
    And the backlog service keeps the item i1

  @g32 @r32
  Scenario: Only a ready item is reopened
    Given an item i1
    And the status of the item i1 is not `ready`
    When the person reopens the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g33 @r33
  Scenario: An open item merged into another item is withdrawn (case 1)
    Given an item i1
    And the status of the item i1 is `idea`
    When the person merges the item i1 with a successor and a reason
    Then the backlog service sets the status of the item i1 to `withdrawn`
    And the backlog service keeps the item i1

  @g33 @r33
  Scenario: An open item merged into another item is withdrawn (case 2)
    Given an item i1
    And the status of the item i1 is `shaped`
    When the person merges the item i1 with a successor and a reason
    Then the backlog service sets the status of the item i1 to `withdrawn`
    And the backlog service keeps the item i1

  @g33 @r33
  Scenario: An open item merged into another item is withdrawn (case 3)
    Given an item i1
    And the status of the item i1 is `ready`
    When the person merges the item i1 with a successor and a reason
    Then the backlog service sets the status of the item i1 to `withdrawn`
    And the backlog service keeps the item i1

  @g33 @r33
  Scenario: An open item merged into another item is withdrawn (case 4)
    Given an item i1
    And the status of the item i1 is `needs-input`
    When the person merges the item i1 with a successor and a reason
    Then the backlog service sets the status of the item i1 to `withdrawn`
    And the backlog service keeps the item i1

  @g34 @r34
  Scenario: A closed item is not merged (case 1)
    Given an item i1
    And the status of the item i1 is `delivered`
    When the person merges the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g34 @r34
  Scenario: A closed item is not merged (case 2)
    Given an item i1
    And the status of the item i1 is `refused`
    When the person merges the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g34 @r34
  Scenario: A closed item is not merged (case 3)
    Given an item i1
    And the status of the item i1 is `withdrawn`
    When the person merges the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g35 @r35
  Scenario: A ready item that meets the readiness bar is checked again
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 meets this readiness bar
    When the person readies the item i1
    Then the backlog service completes this request
    And the backlog service keeps the item i1

  @g36 @r36
  Scenario: A ready item that does not meet the readiness bar is refused, naming each bar check it does not meet
    Given an item i1
    And the status of the item i1 is `ready`
    And the item i1 does not meet this readiness bar
    And a bar check b1
    And the item i1 does not meet the bar check b1
    And a bar check b2
    And the item i1 does not meet the bar check b2
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the bar check b1
    And the backlog service names the bar check b2

  @g37 @r37
  Scenario: An item that is neither shaped nor ready is not readied
    Given an item i1
    And the status of the item i1 is not `shaped`
    And the status of the item i1 is not `ready`
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g38 @r38
  Scenario: A note on an open item is kept (case 1)
    Given an item i1
    And the status of the item i1 is `idea`
    When the person annotates the item i1 with a note
    Then the backlog service keeps the item i1

  @g38 @r38
  Scenario: A note on an open item is kept (case 2)
    Given an item i1
    And the status of the item i1 is `shaped`
    When the person annotates the item i1 with a note
    Then the backlog service keeps the item i1

  @g38 @r38
  Scenario: A note on an open item is kept (case 3)
    Given an item i1
    And the status of the item i1 is `ready`
    When the person annotates the item i1 with a note
    Then the backlog service keeps the item i1

  @g38 @r38
  Scenario: A note on an open item is kept (case 4)
    Given an item i1
    And the status of the item i1 is `needs-input`
    When the person annotates the item i1 with a note
    Then the backlog service keeps the item i1

  @g39 @r39
  Scenario: A closed item takes no note (case 1)
    Given an item i1
    And the status of the item i1 is `delivered`
    When the person annotates the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g39 @r39
  Scenario: A closed item takes no note (case 2)
    Given an item i1
    And the status of the item i1 is `refused`
    When the person annotates the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g39 @r39
  Scenario: A closed item takes no note (case 3)
    Given an item i1
    And the status of the item i1 is `withdrawn`
    When the person annotates the item i1
    Then the backlog service refuses this request
    And the backlog service names the item i1

  @g40 @r40
  Scenario: An item a requirement of which uses a construct the construct catalogue does not define is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a requirement r1
    And the item i1 holds the requirement r1
    And a construct c1
    And the construct c1 has no catalogue entry
    And the requirement r1 uses the construct c1
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the requirement r1
    And the backlog service names the construct c1

  @g41 @r41
  Scenario: An item a model line of which violates a rule is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a model line m1
    And the item i1 holds the model line m1
    And a rule r1
    And the model line m1 violates the rule r1
    When the person readies the item i1
    Then the backlog service refuses this request
    And the backlog service names the model line m1
    And the backlog service names the rule r1
