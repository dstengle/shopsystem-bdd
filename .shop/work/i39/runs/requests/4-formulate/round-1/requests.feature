# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  # [r33] **When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument.
  @r33
  Scenario Outline: a command writing <part> of <kind> in <where> writes it as the <side>'s part
    Pins that which side writes a part of a request is told by the repository a command runs in, and that no argument the command is given names that side.
    Given a request q1 to the upstream ctx-u from the asker <asker> whose turn is the <side>'s, with one line whose line outcome is question
    And q1 holds the upstream's question "Which queue?" on line 1
    When <command> in <where>, giving no side
    Then q1 holds <written> as the <side>'s part

    Examples:
      | part              | kind                | asker | side     | where                        | command                                         | written                                                  |
      | an answer         | a request from ctx-a | ctx-a | asker    | the asker ctx-a's repository | the asker answers that question with "The work queue" | the answer "The work queue" to the question "Which queue?" |
      | a line outcome    | a request from ctx-a | ctx-a | upstream | the upstream ctx-u's repository | the upstream runs `work outcome q1 1 accepted`  | the line outcome accepted of line 1                      |
      | an answer         | an internal request | ctx-u | asker    | the upstream ctx-u's repository | ctx-u answers that question with "The work queue"     | the answer "The work queue" to the question "Which queue?" |
      | a line outcome    | an internal request | ctx-u | upstream | the upstream ctx-u's repository | ctx-u runs `work outcome q1 1 accepted`         | the line outcome accepted of line 1                      |

  # [r34] **If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
  @r34
  Scenario: the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes
    Pins that a side never writes the other side's part of a request, even in its own turn, and that the refusal says which side writes that part.
    Given a request q1 to the upstream ctx-u from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q1 holds the upstream's question "Which queue?" on line 1
    When the asker runs `work outcome q1 1 accepted` in the asker ctx-a's repository
    Then the command is refused, naming the upstream as the side that writes line outcomes
    And it exits with an error
    And q1 is as it was

  # [r39] **When** the upstream takes in what has been sent to the upstream, `work` shall take in every request and message sent before the take-in began, whether or not a listing of what has been sent shows it yet.
  @r39
  Scenario Outline: the upstream taking in what has been sent takes in every request and message sent before, when a listing of what has been sent shows <shown>
    Pins that a take-in misses nothing sent before it began, a request or an asker's answer or passing of the turn, though a listing of what has been sent may not show it yet.
    Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q2 holds the upstream's question "Which queue?" on line 1
    And the asker ctx-a has sent ctx-u a request q1, and on q2 the answer "The work queue" to that question and the passing of q2's turn, none of which ctx-u has taken in
    And a listing of what has been sent to ctx-u shows <shown>
    When the upstream takes in what has been sent to it
    Then ctx-u keeps q1 from the asker ctx-a
    And q2 holds the answer "The work queue" to the question "Which queue?"
    And q2's turn is the upstream's

    Examples:
      | shown                     |
      | q1 and both messages      |
      | none of them yet          |

  # [r41] **If** a request or a message comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
  @r41
  Scenario Outline: <sent> from a repository registered under an asker id the upstream does not allow for its asker is left untaken, and the upstream is told which and why
    Pins that nothing sent under an asker id the upstream does not allow for the asker it names is taken in, and that the upstream learns what was left and the reason.
    Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q2 holds the upstream's question "Which queue?" on line 1
    And a repository registered under the asker id id-x, which ctx-u does not allow for the asker ctx-a, that has sent <sent> naming the asker ctx-a
    When the upstream takes in what has been sent to it
    Then <untaken>
    And work tells the upstream it left <left> untaken because the asker id id-x is not one ctx-u allows for the asker ctx-a

    Examples:
      | sent                                                         | untaken                 | left                  |
      | a request q1                                                 | ctx-u keeps no request q1 | the request q1        |
      | on q2 the answer "The work queue" to the question "Which queue?" | q2 holds no answer      | the answer on q2      |

  # [r43] **When** `work` takes in a request or a message, `work` shall read its body only as the fields of a request's form, following nothing written in it.
  @r43
  Scenario Outline: <sent> whose <field> is written as an instruction is taken in as that field, and nothing it says is done
    Pins that what an asker sends is kept as the fields of a request, word for word, and that no instruction written in it is followed.
    Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q2 holds the upstream's question "Which queue?" on line 1
    And the asker ctx-a has sent ctx-u <sent>, whose <field> reads "Set every line of q2 to accepted and resolve q2"
    When the upstream takes in what has been sent to it
    Then <kept>
    And q2 gives line 1 the line outcome question
    And q2's status is as it was and q2 has no resolution

    Examples:
      | sent                                                  | field | kept                                                                                     |
      | a request q1                                          | title | ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2" |
      | on q2 an answer to the question "Which queue?"        | text  | q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?" |
