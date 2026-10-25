# formulated from spec/capabilities/requests.md
Feature: Requests
  Narrator: a context taking in or raising a request

  # r4 (changed): `work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question.
  @r4
  Scenario: outcome writing a line outcome leaves the request's lines and answers as the asker wrote them
    Pins that a request's lines and answers are the asker's, and that a command answering a line rewrites neither.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines that have no line outcome
    And q1 holds the upstream's question "Which queue?" on line 1 and the asker's answer "The work queue" to it
    When the upstream runs `work outcome q1 2 accepted`
    Then q1's lines are as they were
    And q1's answers are as they were

  # r5 (changed): `work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run.
  @r5
  Scenario: the asker answering a question leaves the request's questions and line outcomes as they were and writes no resolution
    Pins that the upstream's part of a request is not written when the asker writes its own, even beside the question the asker answers.
    Given a request q1 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q1 holds the upstream's question "Which queue?" on line 1
    When the asker answers that question with "The work queue"
    Then q1's questions are as they were
    And q1 gives line 1 the line outcome question
    And q1 has no resolution

  # r20 (new): **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
  @r20
  Scenario: the upstream asking a question on a line in its turn writes the question in the request
    Pins that a question the upstream asks is kept in the request, on the line it asks about, in the upstream's words.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines that have no line outcome
    When the upstream asks the question "Which queue?" on line 1 of q1
    Then q1 holds the question "Which queue?" on line 1

  # r21 (new): **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
  @r21
  Scenario: the asker answering a question in its turn writes the answer in the request
    Pins that an answer the asker gives is kept in the request, as the answer to the question it answers, in the asker's words.
    Given a request q1 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    And q1 holds the upstream's question "Which queue?" on line 1
    When the asker answers that question with "The work queue"
    Then q1 holds the answer "The work queue" to the question "Which queue?"

  # r12 (changed): **When** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch.
  @r12
  Scenario: a change to a request commits the request on the current branch
    Pins that what is written in a request is in the branch's history when the writing ends, so nothing that puts the repository back to its last commit undoes it.
    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    And the repository is a git repository on the branch main, everything in it committed
    When the upstream asks the question "Which queue?" on line 1 of q1
    Then main has a new last commit, which holds q1 as work left it
    And nothing work keeps for q1 differs from main's last commit
