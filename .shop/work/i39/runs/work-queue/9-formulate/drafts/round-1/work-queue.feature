  # [r34] **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.
  @r34
  Scenario: list prints each initiative, each request and each work-item under .shop/work/ with its status
    Pins that list reads the whole queue, initiatives that have ended among them, and gives every initiative, request and work-item in it with its status.
    Given an initiative i1 under .shop/work/ that is started, whose work-items w1 is drafted and w2 is ready
    And an initiative i2 under .shop/work/ that is done, whose work-item w3 is green
    And an initiative i3 under .shop/work/ that is abandoned, whose work-item w4 is withdrawn
    And a request q1 under .shop/work/ that is awaiting-upstream
    When the session runs `work list`
    Then work prints i1 with started, i2 with done and i3 with abandoned
    And it prints q1 with awaiting-upstream
    And it prints w1 with drafted, w2 with ready, w3 with green and w4 with withdrawn
    And it exits successfully

  # [r35] **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.
  @r35
  Scenario: list with --json prints each initiative, request and work-item with its status as one JSON object
    Pins that list's result, read by a script, is one JSON object giving every initiative, request and work-item with its status, and nothing besides.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is drafted
    And an initiative i2 under .shop/work/ that is done, whose work-item w2 is green
    And a request q1 under .shop/work/ that is accepted
    When the session runs `work list --json`
    Then work prints one JSON object and nothing else
    And it gives i1 with started, i2 with done, q1 with accepted, w1 with drafted and w2 with green
    And it exits successfully

  # [r39] **While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.
  @r39
  Scenario: list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered
    Pins that an initiative whose own work is green but whose request upstream is not yet delivered shows, in the list, which request it waits on.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green
    And a request q1 that i1 raised into the upstream ctx-up, which is accepted
    When the session runs `work list`
    Then work prints i1 as waiting on q1
    And it exits successfully

  # [r36] **When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`.
  @r36
  Scenario: show of an initiative prints where it stands, for a session to start from
    Pins what show gives a session about one initiative: its proposals and work-items with their statuses and open questions, whether its branch is pushed, the checkout's uncommitted and untracked files, the ledger's last ten lines and its last next: note.
    Given an initiative i1 under .shop/work/ that is started, whose capability-proposal p1 is approved
    And i1's work-item w1 is ready, and its work-item w2 is awaiting-answer with the question "Which reading of r3?" not yet answered
    And the repository is a git repository whose initiative branch i1-delivery has one commit the remote does not have
    And the tracked file spec/index.md has uncommitted changes
    And notes.txt is untracked and git does not ignore it
    And scratch.log is untracked and git ignores it
    And .shop/work/i1/ledger.md has twelve lines, each written by `work note` with its date, whose notes are in turn "next: plan w1", "planned w1", eight notes that do not begin next:, "next: answer w2" and "w1 ready"
    When the session runs `work show i1`
    Then work prints i1's status as started
    And it prints p1 with approved, w1 with ready and w2 with awaiting-answer and the question "Which reading of r3?"
    And it prints i1-delivery and that the remote does not have every commit of it
    And it prints spec/index.md and notes.txt, and nothing about scratch.log
    And it prints the ledger's last ten lines, the eight notes, "next: answer w2" and "w1 ready", and neither of its first two lines
    And it prints the ledger's line whose note is "next: answer w2" as its last line whose note begins next:
    And it exits successfully

  # [r37] **When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions.
  @r37
  Scenario: show of a work-item prints its status and its open questions
    Pins that show, given a work-item's id, gives that work-item's status and the questions on it not yet answered.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is ready
    And i1's work-item w2 is awaiting-answer with the question "Which reading of r3?" not yet answered
    When the session runs `work show w2`
    Then work prints w2's status as awaiting-answer
    And it prints the question "Which reading of r3?"
    And it exits successfully

  # [r38] **Where** `--json` is given, `work show` shall print its result as one JSON object.
  @r38
  Scenario Outline: show of <target> with --json prints its result as one JSON object
    Pins that show's result, read by a script, is one JSON object and nothing besides, whether it is given an initiative or a work-item.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is awaiting-answer with the question "Which reading of r3?" not yet answered
    When the session runs `work show <target> --json`
    Then work prints one JSON object and nothing else
    And it gives <gives>
    And it exits successfully

    Examples:
      | target | gives                                                                                   |
      | i1     | i1's status as started, and w1 with awaiting-answer and the question "Which reading of r3?" |
      | w1     | w1's status as awaiting-answer and the question "Which reading of r3?"                  |
