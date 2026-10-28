  # [r180] **When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils.
  @r180
  Scenario: a started initiative fulfilling a request, with neither a capability-proposal, a glossary-proposal nor a work-item, is given to an integrate round with the accepted lines of the request
    Pins that an initiative whose integration left nothing behind, not even a glossary-proposal, is integrated again, from the lines its upstream accepted and no other.
    Given i1 is started, has neither a capability-proposal, a glossary-proposal nor a work-item, and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for i1, given q1's lines 1 and 3, and not line 2
