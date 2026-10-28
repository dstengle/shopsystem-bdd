# formulated from spec/capabilities/spec-integration.md
Feature: Spec integration
  Narrator: the person at the gate

  @r44
  Scenario: a round of the kind integrate that drafts a line needing what the named upstream does not yet give gives a request into that upstream, in its terms
    Pins that a need the context cannot meet itself reaches the person as the lines of a request to the upstream that would meet it, worded as that upstream speaks.
    Given spec/index.md names the bounded-context billing as an upstream
    And billing does not yet give a refund of an order
    And billing's glossary names a refund of an order a credit note
    And an approved note asks that the customer sees the refund of a returned order
    When work run starts a round of the kind integrate on that note
    Then the round drafts a line that needs a refund of an order
    And the round's result gives the lines of a request into billing
    And those lines ask for a credit note, in billing's terms

  @r45
  Scenario: a round of the kind integrate given answers that ask for a line the request's accepted lines do not drafts that line under the capability the answers name
    Pins that what the answers ask beyond the request's accepted lines reaches the person as a drafted line, under the capability the answers name, rather than being left out because the request did not ask for it.
    Given a request whose accepted lines ask that the customer sees the status of an order
    And none of those lines asks that the customer is told when an order ships
    And an answer that asks that the customer is told when an order ships
    And that answer names the capability notifications
    When work run starts a round of the kind integrate given that request and that answer
    Then the round drafts, under notifications, a line that the customer is told when an order ships

  @r46
  Scenario: a round of the kind apply gives in its result each answer of the capability-proposal that the drafts it applied do not hold
    Pins that an answer the person gave but the applied drafts left out reaches the result of the round, rather than being lost once the drafts are applied.
    Given a capability-proposal whose answers are that the customer sees the status of an order and that the customer is told when an order ships
    And drafts that hold a line that the customer sees the status of an order
    And no line of those drafts holds that the customer is told when an order ships
    When work run starts a round of the kind apply on that capability-proposal with those drafts
    Then the round applies those drafts
    And the round's result gives the answer that the customer is told when an order ships
    And the round's result does not give the answer that the customer sees the status of an order
