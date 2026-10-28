  # r171
  @r171
  Scenario: an integrate round that ends with a change list naming the glossary gives a drafted glossary-proposal with the terms it adds, changes and removes in the glossary
    Pins that the terms an integration proposes for the glossary come to the gate as a glossary-proposal, holding each term the change list adds, changes or removes there.
    Given spec/index.md's Glossary holds the terms "shelf", "loan" and "reader"
    And i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And the integrate round for i1 gives DONE with a change list that adds the term "ledger", changes the term "shelf" and removes the term "loan" in the glossary
    And every other round ends
    When the person runs `work run i1`
    Then the commit that wrote i1's glossary-proposal wrote one, drafted, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    And it names the term "reader" in none of its adds, changes and removes

  # r172
  @r172
  Scenario: a glossary-proposal awaiting-answer with a question from its gate round that has no answer is given to no apply round
    Pins that the terms of a glossary-proposal are not applied while any question its gate raised on them waits on the person, even when the other questions have answers.
    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?" and "Is the term shelf kept?", given by its gate round, and its Answers section with "One file." only
    And every round ends
    When the person runs `work run i1`
    Then no round of the kind apply was started for g1
