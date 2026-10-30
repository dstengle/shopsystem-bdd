  # [r188] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids of the proposal that the round's change list does not name.
  @r188
  Scenario: an integrate round started for a capability-proposal that redrafts some of its lines leaves the proposal holding the requirement ids its change list does not name
    Pins that redrafting a few of a proposal's lines does not lose the proposal's other lines from what it adds, changes and removes.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1, for thing, is awaiting-answer, its adds naming thing#r4 and thing#r5, its changes naming thing#r2 and its removes naming thing#r3
    And p1's ## Questions section holds "Is a title given twice one book or two?", given by its gate round, and its Answers section "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And the integrate round for p1 redrafts thing#r5 and gives DONE with a change list that adds thing#r5 on thing
    And every other round ends
    When the person runs `work run i1`
    Then p1's adds name thing#r4 and thing#r5, its changes name thing#r2, and its removes name thing#r3

  # [r189] **When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name.
  @r189
  Scenario: an integrate round started for a glossary-proposal that redrafts some of its terms leaves the proposal holding the terms its change list does not name
    Pins that redrafting a few of a glossary-proposal's terms does not lose its other terms from what it adds, changes and removes.
    Given spec/index.md's Glossary holds the terms "shelf", "loan" and "reader"
    And i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's glossary-proposal g1 is awaiting-answer, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    And g1's ## Questions section holds "Is a ledger one file or one line an event?", given by its gate round, and its Answers section "One line an event."
    And a round of the kind integrate is started for g1, redrafts the term "ledger" and gives DONE with a change list that adds the term "ledger" in the glossary
    And every other round ends
    When the person runs `work run i1`
    Then g1's adds name the term "ledger", its changes the term "shelf", and its removes the term "loan"
