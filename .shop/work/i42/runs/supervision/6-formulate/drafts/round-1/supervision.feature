# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # r150 (replaces the scenario of r140, placed where it stood, after @r116): **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
  @r150
  Scenario: an apply round that gives an answer the drafts it applied do not hold is followed by a new integrate round for the proposal
    Pins that an answer asking for what the drafts never held goes back to integration, without anyone starting it by hand.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And every other round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for p1 after the apply round had ended

  # r151 (after @r150): **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied.
  @r151
  Scenario: an apply round that gives an answer the drafts it applied do not hold is followed by no formulate round for the proposal before the new integrate round's drafts are applied
    Pins that lines the answers have sent back to integration are not formulated while their new drafts are still awaiting their gate and apply.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And the integrate round for p1 gives DONE with a change list that adds thing#r4 and thing#r6 on thing
    And every other round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for p1 after the apply round had ended
    And no round of the kind formulate was started for p1

  # r149 (after @r83): **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
  @r149
  Scenario: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal
    Pins that answers changing lines spec/ does not hold go back to integration, without anyone starting it by hand.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "A list, and a shelf's books are listed in the order they were shelved."
    And the formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/
    And every other round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for p1 after the formulate round had ended

  # r152 (after @r149): **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status.
  @r152
  Scenario: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ leaves the proposal's status as it was
    Pins that a proposal sent back to integration by its formulation is not taken as formulated, nor given any other status, by that round.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "A list, and a shelf's books are listed in the order they were shelved."
    And the formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/
    And every other round ends
    When the person runs `work run i1`
    Then p1 was awaiting-answer when the formulate round for p1 had ended
    And no transition of p1 was made between the start of the formulate round for p1 and the start of the integrate round for p1

  # r153 (after @r152): **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output.
  @r153
  Scenario: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ has given its output
    Pins that a formulate round sending the proposal back to integration is not taken as one that left its output out, so the person is asked nothing about missing scenarios.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "A list, and a shelf's books are listed in the order they were shelved."
    And the formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/, and no scenario
    And every other round ends
    When the person runs `work run i1`
    Then no question naming the formulate round's output as missing was written under p1's ## Questions
