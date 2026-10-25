# r67 (changed): **When** a request of which this context is the upstream is `open` or `awaiting-upstream`, `work run` shall start an `initiative-round` session of the kind `intake`, given the request, that writes each line's line outcome or a question on it and passes the turn with `work turn`.
  @r67
  Scenario Outline: a request this context is the upstream of that is <status> is given to an intake round that writes each line's line outcome or a question on it
    Pins that a request waiting on this context is taken in without anyone starting a session for it by hand, and that the round may answer a line with a question instead of a line outcome.
    Given a request q1 of which this context is the upstream, <status>, its turn the upstream's, with two lines
    And the intake round writes a line outcome for q1's line 1, gives a question on q1's line 2 and passes the turn with `work turn`
    When the person runs `work run`
    Then an `initiative-round` session of the kind intake was started, given q1, its brief asking for each line's line outcome or a question on it and for the turn passed with `work turn`
    And q1's line 1 has a line outcome, and q1's turn is its asker's

    Examples:
      | status            |
      | open              |
      | awaiting-upstream |

# r100 (added): **When** a round of the kind `intake` that `work run` started gives a question on a line of a request, `work run` shall write the question in the request.
  @r100
  Scenario: a question an intake round gives on a line of a request is written in the request
    Pins that a question the upstream raises on a line reaches the request, where the asker reads it, without anyone copying it there by hand.
    Given a request q1 of which this context is the upstream, open, its turn the upstream's, with two lines
    And the intake round writes a line outcome for q1's line 1, gives the question "Which unit is the limit in?" on q1's line 2 and passes the turn with `work turn`
    When the person runs `work run`
    Then q1 holds the question "Which unit is the limit in?" on its line 2

# r9 (changed): **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status.
  @r9
  Scenario: when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status
    Pins that a delivery whose work-items all ended well, or were set aside, is no failure while no request this context asked waits on it.
    Given i1's work-items w1 is green and w2 is withdrawn
    And a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's
    When the person runs `work run i1`
    Then `work run` prints w1 with green, and w2 with withdrawn
    And it exits successfully

# r101 (added): **When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions.
  @r101
  Scenario: when `work run` ends while a request whose asker is this context is in the asker's turn, it exits with an error, printing the request with its open questions
    Pins that a request this context asked, waiting on this context's own answer, stops the run as something for the person, even when every work-item ended well.
    Given i1's work-item w1 is green
    And a request q2 kept in this context whose asker is this context, awaiting-asker, its turn the asker's, with the question "Which unit is the limit in?" and no answer
    When the person runs `work run i1`
    Then `work run` prints q2 with the question "Which unit is the limit in?"
    And it exits with an error

# r82 (changed): **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and none is `awaiting-answer` or `failed` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing the status of each initiative it took.
  @r82
  Scenario: `work run` started with no initiative, ending with no node awaiting-answer or failed and no request whose asker is this context in the asker's turn, exits successfully, printing the status of each initiative it took
    Pins that a run over every initiative that leaves nothing waiting on the person, and no request this context asked waiting on it, is no failure, and that it reports only the initiatives it took.
    Given i1 is started, none of its nodes can make a transition and none of them is awaiting-answer or failed
    And an initiative i2 under .shop/work/, started, none of whose nodes can make a transition and none of which is awaiting-answer or failed
    And an initiative i3 under .shop/work/ that is done
    And a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's
    When the person runs `work run`
    Then `work run` prints i1 with started and i2 with started, and does not print i3
    And it exits successfully
