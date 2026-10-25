# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # r111: **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends.
  @r111
  Scenario: an initiative that a work-item's transition leaves able to be done is set done before `work run` ends
    Pins that a transition made during a delivery is followed by the transitions it makes possible, even of another node, rather than leaving them to the next `work run`.
    Given i1 is started and its work-item w1 is ready
    And a request q2 kept in this context, whose asker is this context, that names i1 and is delivered
    And every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record
    When the person runs `work run i1`
    Then w1 is green
    And i1's transition to done was made after w1's transition to green, before `work run` exited

  # r116: **When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers.
  @r116
  Scenario: a capability-proposal whose every question from its formulate round has an answer is given to a formulate round with the answers
    Pins that the person's answers to a formulation's questions reach a new formulation of the proposal, without anyone starting it by hand.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."
    And every round ends and every worker gives DONE
    When the person runs `work run i1`
    Then a round of the kind formulate was started for p1, given the answer "One place."

  # r114: **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.
  @r114
  Scenario: when the apply round `work run` started for a capability-proposal ends, the proposal's adds, changes and removes are written from the change list the round applied
    Pins that the proposal names what was applied after the answers, not what was drafted before them.
    Given i1's capability-proposal p1 is awaiting-answer, its adds naming thing#r4 and thing#r5, its ## Questions section with "Is thing#r5 kept?", given by its gate round, and its Answers section with "No."
    And the apply round for p1 gives DONE with a change list that adds thing#r4 and changes thing#r2 on thing
    And every other round ends and every worker gives DONE
    When the person runs `work run i1`
    Then p1's adds name thing#r4 and not thing#r5, its changes name thing#r2, and its removes name nothing

  # r83: **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`.
  @r83
  Scenario: when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated
    Pins that a capability-proposal whose lines have been formulated with nothing left to ask is formulated.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."
    And the formulate round for p1 gives DONE with no question
    And every worker gives DONE
    When the person runs `work run i1`
    Then p1's transition to formulated was made once the formulate round had ended

  # r112: **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal's `## Questions`.
  @r112
  Scenario: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions
    Pins that what a formulation could not decide reaches the proposal, where the person answers it.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."
    And the formulate round for p1 gives DONE with the questions "Are returns counted?" and "Is a loan one book or many?"
    When the person runs `work run i1`
    Then p1's ## Questions holds "Are returns counted?" and "Is a loan one book or many?"

  # r113: **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`.
  @r113
  Scenario: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer
    Pins that a capability-proposal whose formulation asked a question waits on its answer instead of going on to be formulated.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book."
    And the apply round for p1 ends, and the formulate round for p1 gives DONE with the question "Are returns counted?"
    When the person runs `work run i1`
    Then p1's transition from approved to awaiting-answer was made once the formulate round had ended
    And p1 is awaiting-answer

  # r115: **If** a round of any kind that `work run` started for a capability-proposal or an initiative gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error.
  @r115
  Scenario Outline: when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error
    Pins that one round stopping holds back only its own node, not the rest of the initiative's delivery.
    Given i1's capability-proposal p1 is drafted and i1's work-item w1 is drafted
    And the gate round for p1 <ending>, and every worker gives DONE
    When the person runs `work run i1`
    Then w1 is green
    And it exits with an error

    Examples:
      | ending                                                                                 |
      | gives BLOCKED, asking "Is a title given twice one book or two?"                         |
      | ends in an error                                                                       |
      | ends at its turn limit                                                                 |
      | ends with no error and before its turn limit, having written no result file            |
