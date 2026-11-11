# generated from spec/capabilities/intake.md by features generate; do not edit
Feature: Intake
  Narrator: a session answering a peer bounded context's request

  @g10 @r10
  Scenario: An item with a request line not settled is not readied
    Given an item i1
    And the status of the item i1 is `shaped`
    And a request line r1
    And the item i1 has the request line r1
    And the line outcome of the request line r1 is not `accepted`
    And the line outcome of the request line r1 is not `refused`
    And the line outcome of the request line r1 is not `withdrawn`
    And a session s1
    When the session s1 runs `work ready` on the item i1
    Then `work` refuses `work ready`
    And `work` names the request line r1

  @g11 @r11
  Scenario: A counter-proposal passes the turn to the asker, posted
    Given a request line r1
    And a request r2
    And the request r2 has the request line r1
    And a session s1
    When the session s1 runs `work outcome rewritten` on the request line r1
    Then `work` sets the line outcome of the request line r1 to `rewritten`
    And the request r2 has the request line r3
    And the request line r3 counters the request line r1
    And `work` writes the request line r3
    And `work` sets the side of the request r2 to `asker`
    And the comment c1 is on the request r2
    And `work` posts the comment c1

  @g12 @r12
  Scenario: `work outcome refused` writes the reason
    Given a request line r1
    And a request r2
    And the request r2 has the request line r1
    And a session s1
    When the session s1 runs `work outcome refused` on the request line r1
    Then `work` sets the line outcome of the request line r1 to `refused`
    And the reason r3 is for the request line r1
    And `work` writes the reason r3
    And `work` commits the request r2

  @g13 @r13
  Scenario: `work outcome refused` refuses a refusal with no reason
    Given a session s1
    And a request line r1
    When the session s1 runs `work outcome refused` without the `--reason` option on the request line r1
    Then `work` refuses `work outcome refused`
    And `work` names the `--reason` option
