# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  @r1
  Scenario Outline: request with <given> writes an open request in the upstream's turn with the lines, asker and <where from> given, and prints its id
    Pins that request takes in what the asker gives it, as an open request for the upstream to answer first, and tells the caller its id.
    Given an upstream that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md <options>`
    Then the upstream keeps one new request, whose status is open and whose turn is the upstream's
    And its lines are the two lines of lines.md and its asker is ctx-a
    And its <where from> <named>
    And work prints that request's id
    And it exits successfully

    Examples:
      | given        | options                 | where from | named         |
      | two --source | --source o1 --source o2 | origins    | are o1 and o2 |
      | --thread     | --thread t1             | job-thread | is t1         |

  @r2
  Scenario Outline: request with a line that <fault> is refused, naming the line, and nothing changes
    Pins that a request holds only lines in the strict form model check holds, and that request says which line is not.
    Given an upstream that keeps no request
    And a file lines.md whose line 1 is in strict EARS and whose line 2 <fault>
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md --source o1`
    Then the command is refused, naming line 2
    And it exits with an error
    And the upstream keeps no request

    Examples:
      | fault                                      |
      | is in none of EARS's patterns              |
      | puts its When clause before a While clause |
      | has an If clause with no then              |
      | has two shalls                             |
      | has two sentences                          |

  @r3
  Scenario: request with neither --source nor --thread is refused, and nothing changes
    Pins that no request is taken in without saying where it comes from.
    Given an upstream that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md`
    Then the command is refused because the request names neither an origin nor a job-thread
    And it exits with an error
    And the upstream keeps no request

  @r4
  Scenario: outcome writing a line outcome leaves the request's lines as the asker wrote them
    Pins that a request's lines are the asker's, written by request alone, and that a command answering a line does not rewrite it.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines that have no line outcome
    When the upstream runs `work outcome q1 2 accepted`
    Then q1's lines are as they were

  @r5
  Scenario: turn passing a request leaves its line outcomes as they were and writes no resolution
    Pins that the upstream's part of a request is written by outcome and resolve alone, and that passing the turn writes none of it.
    Given a request q1 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    When the asker runs `work turn q1`
    Then q1 gives line 1 the line outcome question
    And q1 has no resolution

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

  @r17
  Scenario Outline: turn passing a request to its asker with a line that has <line 2> sets the request's status to awaiting-asker
    Pins that a request the upstream hands back with a line still to negotiate shows that the asker is to answer next, though its other lines are settled.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines, line 1 with the line outcome accepted and line 2 with <line 2>
    When the upstream runs `work turn q1`
    Then q1's status is awaiting-asker

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

  @r10
  Scenario: resolve on an accepted request in the asker's turn writes each accepted line's requirement id and version as the resolution
    Pins that resolve records which requirement holds each accepted line and in which version, even when the turn is the asker's.
    Given a request q1 from the asker ctx-a whose status is accepted and whose turn is the asker's, with three lines whose line outcomes are accepted, accepted and refused
    When the upstream runs `work resolve q1`, giving thing#r3 for line 1 and thing#r4 for line 2, each found in the version 0.26.0
    Then q1's resolution gives line 1 thing#r3 and line 2 thing#r4, each found in 0.26.0
    And it gives line 3 nothing
    And it exits successfully

  @r11
  Scenario: resolve writing a request's resolution sets the request's status to delivered
    Pins that a resolved request shows that what it asked for is delivered.
    Given a request q1 from the asker ctx-a whose status is accepted and whose turn is the asker's, with one line whose line outcome is accepted
    When the upstream runs `work resolve q1`, giving thing#r3 for line 1, found in the version 0.26.0
    Then q1's status is delivered

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

  @r14
  Scenario: status with no initiative prints, with its date, each observation no initiative's or request's source names
    Pins that status shows the observations nothing has taken up yet, and when each was made, and none that an initiative or a request already names.
    Given observations o1, o2 and o3, each with its date
    And an initiative i1 under .shop/work/ that is neither done nor abandoned, whose source is o1
    And a request q1 from the asker ctx-a whose origin is o2
    When the session runs `work status`
    Then work prints o3 with its date
    And it gives neither o1 nor o2 as an observation nothing names
