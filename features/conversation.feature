# generated from spec/capabilities/conversation.md by features generate; do not edit
Feature: Conversation
  Narrator: the person reading why a piece of work was asked for

  @g1 @r1
  Scenario: `work quote` keeps the turns
    Given a session s1
    When the session s1 runs `work quote`
    Then `work` writes the quote q1
    And the quote q1 is from the session s1
    And the quote q1 cites the message m1
    And `work` commits the quote q1

  @g6 @r6
  Scenario: The prompt hook writes down the session and its transcript
    When the prompt hook runs `work quote` with the `--hook` option
    Then this session has the transcript t1
    And `work` writes the file f1
    And this git directory holds the file f1
    And the file f1 lists the transcript t1

  @g7 @r7
  Scenario: `work show` on a quote prints its messages
    Given a quote q1
    And a message m1
    And the quote q1 cites the message m1
    And a message m2
    And the quote q1 cites the message m2
    And a message m3
    And the quote q1 does not cite the message m3
    When the person runs `work show` on the quote q1
    Then `work` prints the message m1
    And `work` prints the message m2
    And `work` does not print the message m3

  @g8 @r8
  Scenario: The names table at SessionStart
    Given an item i1
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
    When the SessionStart hook runs `work names`
    Then `work` prints the item i1
    And `work` prints the item i2
    And `work` prints the title t1
    And `work` prints the title t2
    And `work` does not print the title t3
    And `work` prints the batch b1
    And `work` prints the batch b2

  @g9 @r9
  Scenario: `work quote` finds a message sent mid-turn
    Given a session s1
    And a queued message q1
    When the session s1 runs `work quote` on the queued message q1
    Then `work` writes the quote q2
    And the quote q2 cites the queued message q1
    And `work` commits the quote q2

  @g10 @r10
  Scenario: The SessionStart hook shows the live directives
    Given a directive d1
    And the status of the directive d1 is `live`
    And a directive d2
    And the status of the directive d2 is `live`
    When the SessionStart hook runs `work directives` with the `--hook` option
    Then `work` prints the quote q1
    And the directive d1 has the quote q1
    And `work` prints the quote q2
    And the directive d2 has the quote q2

  @g11 @r11
  Scenario: `work promote` promotes a live directive to what it became
    Given an item i1
    And a directive d1
    And the status of the directive d1 is `live`
    And a session s1
    When the session s1 runs `work promote` with the `--to` option set to the item i1 on the directive d1
    Then `work` sets the status of the directive d1 to `promoted`
    And `work` commits the directive d1

  @g12 @r14
  Scenario: `work drop` drops a live directive with its reason
    Given a directive d1
    And the status of the directive d1 is `live`
    And a session s1
    When the session s1 runs `work drop` with the `--why` option on the directive d1
    Then `work` sets the status of the directive d1 to `dropped`
    And `work` commits the directive d1

  @g13 @r12
  Scenario: `work promote` refuses a directive that is not live
    Given a directive d1
    And the status of the directive d1 is not `live`
    And a session s1
    When the session s1 runs `work promote` with the `--to` option on the directive d1
    Then `work` refuses `work promote`
    And `work` names the directive d1

  @g14 @r13
  Scenario: `work promote` refuses an item that does not exist
    Given an item i1
    And the item i1 does not exist
    And a session s1
    And a directive d1
    When the session s1 runs `work promote` with the `--to` option set to the item i1 on the directive d1
    Then `work` refuses `work promote`
    And `work` names the item i1

  @g15 @r15
  Scenario: `work drop` refuses a directive that is not live
    Given a directive d1
    And the status of the directive d1 is not `live`
    And a session s1
    When the session s1 runs `work drop` with the `--why` option on the directive d1
    Then `work` refuses `work drop`
    And `work` names the directive d1

  @g16 @r16
  Scenario: `work directive` keeps the person's words as a live directive
    Given a session s1
    When the session s1 runs `work directive`
    Then the quote q1 cites the message m1
    And `work` writes the directive d1
    And the directive d1 has the quote q1
    And `work` commits the directive d1
