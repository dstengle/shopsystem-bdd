# generated from spec/capabilities/intake.md by features generate; do not edit
Feature: Intake
  Narrator: a session answering a peer bounded context's request

  @g1 @r1
  Scenario: A peer's request becomes an item
    Given a request q1 that is `open`
    When the session s1 runs `work intake` on the request q1
    Then `work` writes the item i1
    And the item i1 is `shaped`
    And the item i1 is asked by the bounded context b1
    And the item i1 is `peer`
    And `work` commits the item i1

  @g2 @r2
  Scenario: An accepted line stays on the item
    Given a request line r1
    And an item i1
    And the request line r1 is of the item i1
    When the session s1 runs `work outcome accepted` on the request line r1
    Then the request line r1 is `accepted`
    And `work` commits the item i1

  @g3 @r3
  Scenario: A refused line is written with its reason
    Given a request line r1
    And an item i1
    And the request line r1 is of the item i1
    When the session s1 runs `work outcome refused` on the request line r1
    Then the request line r1 is `refused`
    And `work` writes the reason r2
    And `work` commits the item i1

  @g4 @r4
  Scenario: A counter-proposal passes the turn to the asker
    Given a request line r1
    And a request q1
    And the request line r1 is proposed in the request q1
    When the session s1 runs `work outcome rewritten` on the request line r1
    Then the request line r1 is `rewritten`
    And `work` writes the request line r2
    And `work` changes the side of the request q1

  @g5 @r5
  Scenario: No person in the loop
    Given a request q1 that is `awaiting-upstream`
    When the session s1 runs `work intake` on the request q1
    Then `work` does not ask the question q2

  @g6 @r6
  Scenario: An item with a request line that is not settled is not readied
    Given an item i1 that is `shaped`
    And a request line r1
    And the request line r1 is of the item i1
    And the request line r1 is not settled
    When the session s1 runs `work ready` on the item i1
    Then `work` exits with an error naming the request line r1
    And `work` changes nothing
