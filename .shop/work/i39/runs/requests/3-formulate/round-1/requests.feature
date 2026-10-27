# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  # [r28] **When** an asker raises a request, answers a question or passes the turn, `work` shall do it from the asker's own repository, with no checkout of the upstream's repository.
  @r28
  Scenario Outline: the asker <doing> from its own repository, with no checkout of the upstream's repository
    Pins that an asker writes its part of a request and hands it on without ever holding a copy of the upstream's repository.
    Given a request q1 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q1 holds the upstream's question "Which queue?" on line 1
    And a file lines.md with two lines in strict EARS in the asker ctx-a's repository
    And the asker ctx-a's repository has no checkout of the upstream's repository
    When the asker <does> in its own repository
    Then <the upstream keeps>
    And work made no checkout of the upstream's repository
    And it exits successfully

    Examples:
      | doing                     | does                                                                          | the upstream keeps                                              |
      | raising a request         | runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1` | the upstream keeps a new request from the asker ctx-a           |
      | answering a question      | answers that question with "The work queue"                                   | q1 holds the answer "The work queue" to the question "Which queue?" |
      | passing the turn          | runs `work turn q1`                                                           | q1's turn is the upstream's                                     |

  # [r44] **When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>`, with `--thread <id>` or with `--raised-for <request>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id.
  @r44
  Scenario Outline: request with <given> writes an open request in the upstream's turn with the lines and asker given and <where from>, and prints its id
    Pins that request takes in what the asker gives it, as an open request for the upstream to answer first, and tells the caller its id.
    Given an upstream ctx-u that keeps no request
    And a file lines.md with two lines in strict EARS
    When <role> runs `work request "Show the queue" --from <asker> --lines lines.md <options>` in its own repository
    Then the upstream keeps one new request, whose status is open and whose turn is the upstream's
    And its lines are the two lines of lines.md and its asker is <asker>
    And <where from>
    And work prints that request's id
    And it exits successfully

    Examples:
      | given          | role              | asker | options                 | where from                                  |
      | two --source   | the upstream      | ctx-u | --source o1 --source o2 | its origins are o1 and o2                   |
      | --thread       | the asker ctx-a   | ctx-a | --thread t1             | its job-thread is t1                        |
      | --raised-for   | the asker ctx-a   | ctx-a | --raised-for q7         | it names neither an origin nor a job-thread |

  # [r29] **Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for.
  @r29
  Scenario: request with --raised-for writes in the upstream's request the request it is raised for
    Pins that a request raised to fulfil another request says which one, in the request the upstream keeps.
    Given an upstream ctx-u that keeps no request
    And the asker ctx-a keeps a request q7 from its own asker ctx-b
    And a file lines.md with two lines in strict EARS
    When the asker ctx-a runs `work request "Show the queue" --from ctx-a --lines lines.md --raised-for q7` in its own repository
    Then the upstream keeps one new request
    And it names q7 as the request it is raised for
    And it exits successfully

  # [r19] **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
  # Changed: the asker ctx-a now gives --thread, since r30 refuses --source from an asker that is not the upstream itself.
  @r19
  Scenario: request with --delegation writes the delegation given in the request
    Pins that a request keeps the person's words naming which questions a session may answer in the person's place, as they were given.
    Given an upstream that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1 --delegation "answer any question on line 2"`
    Then the upstream keeps one new request
    And its delegation is "answer any question on line 2"
    And it exits successfully

  # [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
  # Changed: the asker ctx-a now gives --thread, so the empty delegation is the only reason to refuse.
  @r22
  Scenario: request with an empty delegation is refused, and nothing changes
    Pins that a request is not taken in with a delegation that names no question a session may answer in the person's place.
    Given an upstream that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1 --delegation ""`
    Then the command is refused because the delegation is empty
    And it exits with an error
    And the upstream keeps no request

  # [r2] **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing.
  # Changed: the asker ctx-a now gives --thread, so the line is the only reason to refuse.
  @r2
  Scenario Outline: request with a line that <fault> is refused, naming the line, and nothing changes
    Pins that a request holds only lines in the strict form model check holds, and that request says which line is not.
    Given an upstream that keeps no request
    And a file lines.md whose line 1 is in strict EARS and whose line 2 <fault>
    When the asker runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`
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

  # [r45] **If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
  @r45
  Scenario: a request the upstream raises for itself with neither --source nor --thread is refused, and nothing changes
    Pins that a context takes in no request of its own without saying where it comes from.
    Given an upstream ctx-u that keeps no request
    And a file lines.md with two lines in strict EARS
    When the upstream runs `work request "Show the queue" --from ctx-u --lines lines.md` in its own repository
    Then the command is refused because the request names neither an origin nor a job-thread
    And it exits with an error
    And the upstream keeps no request

  # [r30] **If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing.
  @r30
  Scenario: a request from another asker raised with --source is refused, and nothing changes
    Pins that only a context's own requests name origins, even when the other asker also names a job-thread.
    Given an upstream ctx-u that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker ctx-a runs `work request "Show the queue" --from ctx-a --lines lines.md --source o1 --thread t1` in its own repository
    Then the command is refused because an origin belongs to an internal request
    And it exits with an error
    And the upstream keeps no request

  # [r31] **If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, **then** `work request` shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing.
  @r31
  Scenario: a request from another asker raised with neither --raised-for nor --thread is refused, and nothing changes
    Pins that a request from outside the context is not taken in without saying which request or job-thread it serves.
    Given an upstream ctx-u that keeps no request
    And a file lines.md with two lines in strict EARS
    When the asker ctx-a runs `work request "Show the queue" --from ctx-a --lines lines.md` in its own repository
    Then the command is refused because the request names neither a request it is raised for nor a job-thread
    And it exits with an error
    And the upstream keeps no request

  # [r32] **If** the asker given to `work request` is not the bounded-context or product level whose repository raises the request, **then** `work request` shall refuse, naming the asker, and change nothing.
  @r32
  Scenario Outline: request raised from <role>'s repository giving the asker <given asker> is refused, naming the asker, and nothing changes
    Pins that a repository raises requests only as the context or product level it is, and request says which asker it would not take.
    Given an upstream ctx-u that keeps no request
    And a file lines.md with two lines in strict EARS
    When <role> runs `work request "Show the queue" --from <given asker> --lines lines.md --thread t1` in its own repository
    Then the command is refused, naming <given asker>
    And it exits with an error
    And the upstream keeps no request

    Examples:
      | role                 | given asker |
      | the asker ctx-a      | ctx-b       |
      | the product level p1 | ctx-a       |

  # [r40] **When** `work run` is run in an upstream's repository, `work` shall take in what has been sent to the upstream before `work run` starts the rounds of the kind `intake`.
  @r40
  Scenario: run in an upstream's repository takes in what has been sent to it before its intake rounds start
    Pins that the intake rounds of a run see every request sent to the upstream, not only those it took in before.
    Given a request q1 that the asker ctx-a has sent to the upstream ctx-u and that ctx-u has not taken in
    When the upstream runs `work run` in its own repository
    Then ctx-u had taken in q1 when work run started its first round of the kind intake
    And that round is given q1

  # [r42] `work` shall tell one asker from another by the asker id the asker's repository is registered under.
  @r42
  Scenario: requests from repositories registered under different asker ids are taken in as different askers' requests
    Pins that which asker a request comes from is told by the asker id its repository is registered under.
    Given a repository registered under the asker id id-a, which the upstream ctx-u allows for the asker ctx-a, that has sent a request q1 naming the asker ctx-a
    And a repository registered under the asker id id-b, which ctx-u allows for the asker ctx-b, that has sent a request q2 naming the asker ctx-b
    When the upstream takes in what has been sent to it
    Then ctx-u keeps q1 from the asker ctx-a
    And it keeps q2 from the asker ctx-b

  # [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.
  # Changed: the request naming an origin is now the upstream's own, since r30 gives origins only to internal requests.
  @r14
  Scenario: status with no initiative prints, with its date, each observation no initiative's or request's source names
    Pins that status shows the observations nothing has taken up yet, and when each was made, and none that an initiative or a request already names.
    Given observations o1, o2 and o3, each with its date
    And an initiative i1 under .shop/work/ that is neither done nor abandoned, whose source is o1
    And a request q1 whose asker is the upstream itself and whose origin is o2
    When the session runs `work status`
    Then work prints o3 with its date
    And it gives neither o1 nor o2 as an observation nothing names
