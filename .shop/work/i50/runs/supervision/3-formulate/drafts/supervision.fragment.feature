  # [r173] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes.
  @r173
  Scenario: when the gate round `work run` started for a glossary-proposal ends with no question, one question asking the person to approve the terms it adds, changes and removes is written
    Pins that a glossary gate with nothing to decide still reaches the person as a question to answer, so the proposal's terms are not taken as approved unasked.
    Given i1's glossary-proposal g1 is drafted, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    And the gate round's result gives no question, and every round ends
    When the person runs `work run i1`
    Then a round of the kind gate was started for g1
    And one question was written for g1, asking the person to approve the terms "ledger", "shelf" and "loan"
