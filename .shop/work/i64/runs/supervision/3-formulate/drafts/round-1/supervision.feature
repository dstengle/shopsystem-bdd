# [r221] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold for a glossary-proposal, `work run` shall start a new round of the kind `integrate` for the glossary-proposal.
  @r221
  Scenario: an apply round that gives an answer the drafts it applied do not hold for a glossary-proposal is followed by a new integrate round for the glossary-proposal
    Pins that an answer on a glossary-proposal asking for what its drafts never held goes back to integration, without anyone starting it by hand.
    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", given by its gate round, and its Answers section with "One line an event, and a ledger is the file of those lines."
    And the apply round for g1 applies nothing, giving that g1's answers give what its drafts do not hold
    And every other round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for g1 after the apply round had ended
