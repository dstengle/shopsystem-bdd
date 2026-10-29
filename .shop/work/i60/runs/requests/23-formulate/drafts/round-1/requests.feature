# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  # formulates [r65] of spec/capabilities/requests.md
  # [r65] **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.
  @r65
  Scenario Outline: delegate given a request that holds <before> writes the delegation given in the request, in place of any it had
    Pins that a request keeps the delegation delegate was last given, as it was given, and no earlier one beside it.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    And q1 holds <before>
    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    Then q1's delegation is "answer any question on line 1"
    And q1 holds no other delegation
    And it exits successfully

    Examples:
      | before                                              |
      | no delegation                                       |
      | the delegation "answer any question on line 2"      |

  # formulates [r66] of spec/capabilities/requests.md
  # [r66] **When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch.
  @r66
  Scenario: delegate writing a delegation in a request commits the request on the current branch
    Pins that a delegation delegate writes is in the branch's history when it ends, so nothing that puts the repository back to its last commit undoes it.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    And the repository is a git repository on the branch main, everything in it committed
    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    Then main has a new last commit, which holds q1 as work left it
    And nothing work keeps for q1 differs from main's last commit

  # formulates [r67] of spec/capabilities/requests.md
  # [r67] **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
  @r67
  Scenario: delegate given an empty delegation is refused, and nothing changes
    Pins that delegate writes no delegation that names no question a session may answer in the person's place, and leaves the one the request has.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    And q1 holds the delegation "answer any question on line 2"
    When the upstream runs `work delegate`, giving q1 and the delegation ""
    Then the command is refused because the delegation is empty
    And it exits with an error
    And q1 is as it was

  # formulates [r68] of spec/capabilities/requests.md
  # [r68] **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
  @r68
  Scenario Outline: delegate given a request that is <status> is refused, naming <status>, and nothing changes
    Pins that a request whose negotiation has ended takes no new delegation, and that delegate says which status stops it.
    Given a request q1 from the asker ctx-a whose status is <status> and whose turn is the asker's, with one line whose line outcome is <line outcome>
    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    Then the command is refused, naming <status>
    And it exits with an error
    And q1 is as it was

    Examples:
      | status    | line outcome |
      | delivered | accepted     |
      | refused   | refused      |
      | withdrawn | withdrawn    |

  # formulates [r70] of spec/capabilities/requests.md
  # [r70] **When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is.
  @r70
  Scenario Outline: delegate run in the <side>'s turn writes the delegation
    Pins that whose turn it is does not stop delegate from writing a delegation in a request.
    Given a request q1 from the asker ctx-a whose turn is the <side>'s, with one line whose line outcome is question
    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    Then q1's delegation is "answer any question on line 1"
    And it exits successfully

    Examples:
      | side     |
      | upstream |
      | asker    |

  # formulates [r71] of spec/capabilities/requests.md
  # [r71] **When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn.
  @r71
  Scenario: delegate writing a delegation in a request keeps the request's status and turn
    Pins that giving a request a delegation moves it neither along its lifecycle nor to the other side.
    Given a request q1 from the asker ctx-a whose status is awaiting-asker and whose turn is the asker's, with one line whose line outcome is question
    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    Then q1's delegation is "answer any question on line 1"
    And q1's status is awaiting-asker
    And q1's turn is the asker's
