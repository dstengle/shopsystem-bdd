# generated from spec/capabilities/quotes.md by features generate; do not edit
Feature: Quotes
  Narrator: a session

  @g1 @r1
  Scenario: A message quoted is kept as a quote
    Given a session s1
    And a message m1
    When the session s1 quotes the message m1
    Then the conversation service keeps the quote q1
    And the quote q1 is from the session s1
    And the quote q1 cites the message m1

  @g2 @r2
  Scenario: A prompt keeps the session's transcript for quoting
    Given a session s1
    When the person prompts the session s1
    Then the conversation service keeps the transcript t1
    And the session s1 has the transcript t1

  @g3 @r3
  Scenario: A quote read gives the messages it cites
    Given a quote q1
    And a message m1
    And the quote q1 cites the message m1
    And a message m2
    And the quote q1 cites the message m2
    And a message m3
    And the quote q1 does not cite the message m3
    When the person reads the quote q1
    Then the conversation service returns the message m1
    And the conversation service returns the message m2
    And the conversation service does not return the message m3

  @g4 @r4
  Scenario: A queued message quoted is kept as a quote
    Given a session s1
    And a queued message q1
    When the session s1 quotes the queued message q1
    Then the conversation service keeps the quote q2
    And the quote q2 cites the queued message q1
    And the conversation service returns the quote q2
