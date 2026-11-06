# generated from spec/capabilities/intake.md by features generate; do not edit
Feature: Intake
  Narrator: a session answering a peer bounded context's request

  @g6 @r6
  Scenario: An item with a request line that is not settled is not readied
    Given an item i1 that is `shaped`
    And a request line r1
    And the request line r1 is of the item i1
    And the request line r1 is not settled
    When the session s1 runs `work ready` on the item i1
    Then `work` exits with an error naming the request line r1
    And `work` changes nothing

  @g7 @r7
  Scenario: A counter-proposal passes the turn to the asker, posted
    Given a request line r1
    And a request q1
    And the request line r1 is proposed in the request q1
    When the session s1 runs `work outcome rewritten` on the request line r1
    Then the request line r1 is `rewritten`
    And `work` writes the request line r2
    And `work` changes the side of the request q1
    And `work` posts the comment c1

  @g8 @r8
  Scenario: `work outcome refused` writes the reason
    Given a request line r1
    And a request q1
    And the request line r1 is proposed in the request q1
    When the session s1 runs `work outcome refused` on the request line r1
    Then the request line r1 is `refused`
    And `work` writes the reason r2
    And `work` commits the request q1

  @g9 @r9
  Scenario: `work outcome refused` refuses a refusal with no reason
    Given the argument `--reason` is absent
    When the session s1 runs `work outcome refused` on the request line r1
    Then `work` exits with an error naming `--reason`
