# supervision#r211: **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started.
  @r211
  Scenario Outline: `work run` reads the delegation the request has when it reads it, the delegation given <when> the initiative started
    Pins that a question is answered under the delegation the request holds now, whether the person gave it with the request or after the initiative was already under way.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", given <when> i1 started
    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and no answer
    And the session answering under the delegation answers "Yes.", and every worker gives DONE
    When the person runs `work run i1`
    Then "Does scripts/log.py own the log?" was given to a session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", scripts/log.py, and nothing else
    And w1's answer to "Does scripts/log.py own the log?" is "Yes.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."

    Examples:
      | when   |
      | before |
      | after  |
