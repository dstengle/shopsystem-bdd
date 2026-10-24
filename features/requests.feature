# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  @r15
  Scenario: outcome in the upstream's turn writes the outcome given as the line outcome of the line named
    Pins that outcome answers the one line it names, with the word it is given, and leaves the other lines as they were.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines that have no line outcome
    When the upstream runs `work outcome q1 2 accepted`
    Then q1 gives line 2 the line outcome accepted
    And q1 gives line 1 no line outcome

  @r16
  Scenario: a side writing a part of a request in the other side's turn is refused, and nothing changes
    Pins that a side writes its part of a request only in its own turn, and a command run out of turn leaves the request as it was.
    Given a request q1 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    When the upstream runs `work outcome q1 1 accepted`
    Then the command is refused because it is the asker's turn
    And it exits with an error
    And q1 is as it was

  @r7
  Scenario Outline: turn passes the request's turn from the <side> to the <other side>
    Pins that turn hands the request to the side that did not have it, whichever side that is.
    Given a request q1 from the asker ctx-a whose turn is the <side>'s, with one line whose line outcome is question
    When the <side> runs `work turn q1`
    Then q1's turn is the <other side>'s

    Examples:
      | side     | other side |
      | upstream | asker      |
      | asker    | upstream   |

  @r18
  Scenario: turn passing a request to its upstream sets the request's status to awaiting-upstream
    Pins that a request the asker hands back shows that the upstream is to answer next.
    Given a request q1 from the asker ctx-a whose status is awaiting-asker and whose turn is the asker's, with one line whose line outcome is question
    When the asker runs `work turn q1`
    Then q1's status is awaiting-upstream

  @r8
  Scenario: the upstream ending its turn with every line accepted, refused or withdrawn and one accepted sets the status to accepted
    Pins that a request is accepted once nothing on it is left to negotiate and the upstream took at least one of its lines.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with three lines whose line outcomes are accepted, refused and withdrawn
    When the upstream runs `work turn q1`
    Then q1's status is accepted

  @r9
  Scenario: the upstream ending its turn with every line refused or withdrawn sets the status to refused
    Pins that a request is refused once nothing on it is left to negotiate and none of its lines was accepted.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines whose line outcomes are refused and withdrawn
    When the upstream runs `work turn q1`
    Then q1's status is refused

  @r12
  Scenario: a command that changes a request commits the request on the current branch
    Pins that what a request command writes is in the branch's history when it ends, so nothing that puts the repository back to its last commit undoes it.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    And the repository is a git repository on the branch main, everything in it committed
    When the upstream runs `work outcome q1 1 accepted`
    Then main has a new last commit, which holds q1 as work left it
    And nothing work keeps for q1 differs from main's last commit

  @r13
  Scenario: show prints each request with its status and whose turn it is
    Pins that show gives every request the context keeps, where it stands and which side is to write next.
    Given a request q1 from the asker ctx-a whose status is open and whose turn is the upstream's
    And a request q2 from the asker ctx-b whose status is awaiting-asker and whose turn is the asker's
    When the session runs `work show`
    Then work prints q1 with open and the upstream's turn
    And it prints q2 with awaiting-asker and the asker's turn
