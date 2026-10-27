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
