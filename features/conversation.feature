# generated from spec/capabilities/conversation.md by features generate; do not edit
Feature: Conversation
  Narrator: the person reading why a piece of work was asked for

  @g1 @r1
  Scenario: `work quote` keeps the turns
    Given a session s1
    When the session s1 runs `work quote`
    Then the quote q1 is from the session s1
    And the quote q1 cites the message m1
    And `work` writes the quote q1
    And `work` commits the quote q1

  @g6 @r6
  Scenario: The prompt hook writes down the session and its transcript
    When the prompt hook runs `work quote` with the `--hook` option
    Then this git directory holds the file f1
    And this session has the transcript t1
    And the file f1 lists the transcript t1
    And `work` writes the file f1

  @g7 @r7
  Scenario: `work show` on a quote prints its messages
    Given a quote q1
    And a message m1
    And the quote q1 cites the message m1
    And a message m2
    And the quote q1 cites the message m2
    When the person runs `work show` on the quote q1
    Then `work` prints the message m1
    And `work` prints the message m2

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
    And a batch b1
    And a batch b2
    When the SessionStart hook runs `work names`
    Then `work` prints the item i1
    And `work` prints the item i2
    And `work` prints the title t1
    And `work` prints the title t2
    And `work` prints the batch b1
    And `work` prints the batch b2
