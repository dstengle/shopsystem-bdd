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

  @r54
  Scenario: a round of the kind integrate that drafts a change to the glossary gives the terms it adds, changes and removes in the change list's entry for the glossary and in no entry for a capability
    Pins that the person at the gate finds every term a round drafts in the one place the glossary's change is listed, and never mixed into the lines listed for a capability.
    Given spec/index.md's glossary has the terms order and basket
    And an approved note asks that the customer sees the refund of a returned order
    And that note adds the term refund, changes the term order and removes the term basket
    When work run starts a round of the kind integrate on that note
    Then the round drafts a line under the capability returns that the customer sees the refund of a returned order
    And the round drafts a change to the glossary
    And the change list's entry for the glossary gives refund as added, order as changed and basket as removed
    And the change list's entry for returns gives none of the terms refund, order and basket

  @r55
  Scenario: while the person has not approved the terms of a glossary-proposal, no round applies any of them to spec/index.md
    Pins that a term reaches the glossary only through the gate: a glossary-proposal the person has not approved leaves spec/index.md as it was, even while a round applies other drafts of the same initiative.
    Given spec/index.md's glossary has the term order and no term refund
    And an initiative with a glossary-proposal that adds the term refund and changes the term order
    And the person has not approved the terms of that glossary-proposal
    And a capability-proposal of that initiative the person has approved
    When work run starts a round of the kind apply on that capability-proposal
    Then the round applies the capability-proposal's drafts
    And spec/index.md's glossary has no term refund
    And spec/index.md's glossary has the term order as it was before the round
