# generated from spec/capabilities/conversation.md by features generate; do not edit
Feature: Conversation
  Narrator: the person reading why a piece of work was asked for

  @g1 @r1
  Scenario: `work quote` keeps the turns
    When the session s1 runs `work quote`
    Then `work` writes the quote q1
    And the quote q1 is from the session s1
    And the quote q1 cites the message m1
    And `work` commits the quote q1

  @g2 @r2
  Scenario: The prompt hook gives the session and the transcript
    When the UserPromptSubmit hook runs `work quote --hook`
    Then `work` keeps the session s1

  @g3 @r3
  Scenario: `work show` on a quote prints its messages
    Given a message m1
    And a quote q1
    And the message m1 is cited by the quote q1
    When the person runs `work show` on the quote q1
    Then `work` prints the message m1

  @g4 @r4
  Scenario: The names table at SessionStart
    When the SessionStart hook runs `work names`
    Then `work` prints the item i1
    And `work` prints the title t1
    And the title t1 is of the item i1
    And `work` prints the batch b1
