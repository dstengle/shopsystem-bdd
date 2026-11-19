# generated from spec/capabilities/directives.md by features generate; do not edit
Feature: Directives
  Narrator: a session

  @g1 @r1
  Scenario: A directive given is kept with its quote
    Given a session s1
    And a directive d1
    When the session s1 gives the directive d1
    Then the quote q1 cites the message m1
    And the conversation service keeps the directive d2
    And the directive d2 has the quote q1

  @g2 @r2
  Scenario: A session that starts is told every live directive
    Given a session s1
    And a directive d1
    And the status of the directive d1 is `live`
    And a directive d2
    And the status of the directive d2 is `live`
    When the session s1 starts
    Then the conversation service notifies the session s1 of the quote q1
    And the directive d1 has the quote q1
    And the conversation service notifies the session s1 of the quote q2
    And the directive d2 has the quote q2

  @g3 @r3
  Scenario: A live directive promoted to an item becomes promoted
    Given a directive d1
    And the status of the directive d1 is `live`
    And a session s1
    And an item i1
    When the session s1 promotes the directive d1 to the item i1
    Then the conversation service sets the status of the directive d1 to `promoted`
    And the conversation service keeps the directive d1

  @g4 @r4
  Scenario: A live directive dropped with its reason becomes dropped
    Given a directive d1
    And the status of the directive d1 is `live`
    And a session s1
    When the session s1 drops the directive d1 with a reason
    Then the conversation service sets the status of the directive d1 to `dropped`
    And the conversation service keeps the directive d1

  @g5 @r5
  Scenario: A directive that is not live is not promoted
    Given a directive d1
    And the status of the directive d1 is not `live`
    And a session s1
    And an item i1
    When the session s1 promotes the directive d1 to the item i1
    Then the conversation service refuses this request
    And the conversation service names the directive d1

  @g6 @r6
  Scenario: A directive is not promoted to an item that does not exist
    Given an item i1
    And the item i1 does not exist
    And a session s1
    And a directive d1
    When the session s1 promotes the directive d1 to the item i1
    Then the conversation service refuses this request
    And the conversation service names the item i1

  @g7 @r7
  Scenario: A directive that is not live is not dropped
    Given a directive d1
    And the status of the directive d1 is not `live`
    And a session s1
    When the session s1 drops the directive d1 with a reason
    Then the conversation service refuses this request
    And the conversation service names the directive d1
