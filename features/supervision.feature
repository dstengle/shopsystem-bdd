# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started work run

  Background:
    Given a git repository with an initiative i1 under .shop/work/, a stand-in claude first on PATH and as $SHOPSYSTEM_WORK_CLAUDE, and tests that pass

  @r1 @r9
  Scenario: work run pulls each work-item through research, plan, implementation and review, one worker at a time, until none can move
    Pins the stage-by-stage pull: every work-item reaches green through its four workers in order, and no worker starts before the last one ended.
    Given i1's work-items w1 and w2 are drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1 and w2 had code-scout, bdd-planner, bdd-implementer and bdd-task-reviewer as its workers, in that order
    And no worker was started before the one before it had ended
    And w1 and w2 are green
    And it exits 0

  @r2
  Scenario: each worker is a new claude -p session of its stage's agent, given one brief file naming the work-item, the files to read and the result file
    Pins how a worker is started: its stage's agent, a session no other worker had, and one brief that says what to read and where the result goes.
    Given i1's work-item w1 is drafted, under thing
    And every worker gives DONE
    When the person runs `work run i1`
    Then each worker was started as `claude -p <its brief file>` with --agent shopsystem-bdd:<its stage's agent> and a session id no other worker had
    And each brief file names .shop/work/i1/w1.md and spec/capabilities/thing.md to read, and a result file in the brief's own directory

  @r3
  Scenario: a worker's DONE moves the work-item to its next status
    Pins the moves DONE makes, in the lifecycle's order, from where the work-item stands.
    Given i1's work-item w1 is researched
    And every worker gives DONE
    When the person runs `work run i1`
    Then log.jsonl moves w1 from researched to planned, ready, claimed, done and green, in that order

  @r4
  Scenario: an implementer's DONE is merged into the initiative branch when the work-item's scenarios and the whole suite pass on its branch
    Pins that the merge is of the implementer's own commit, tested where that commit is.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And the work-item's scenarios pass only where feature.txt is
    When the person runs `work run i1`
    Then the initiative branch has the implementer's commit of feature.txt
    And w1 is green

  @r4 @r5
  Scenario Outline: an implementer's DONE whose <tests> fail is not merged, and the work-item goes to awaiting-ruling with the failure as its question
    Pins that a failing test keeps the branch out of the initiative branch and becomes the person's question.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And <tests> fail on the implementer's branch
    When the person runs `work run i1`
    Then the initiative branch does not have the implementer's commit
    And w1 is awaiting-ruling, its question naming `<command>` and what it printed
    And no worker was started for w1 after the implementer

    Examples:
      | tests                     | command                           |
      | the work-item's scenarios | python3 tests.py --work-item w1   |
      | the whole suite           | python3 tests.py                  |

  @r5
  Scenario Outline: a researcher that <gives> puts the work-item to awaiting-ruling with <question> as its question
    Pins that anything but DONE stops the work-item with a question for the person, and no later stage starts.
    Given i1's work-item w1 is drafted
    And the researcher <gives>
    When the person runs `work run i1`
    Then w1 is awaiting-ruling, its question saying <question>
    And no worker was started for w1 after the researcher

    Examples:
      | gives                                                    | question                         |
      | gives QUESTION, asking "Which module owns the log?"      | Which module owns the log?       |
      | gives BLOCKED, asking "Is the old reader kept?"          | Is the old reader kept?          |
      | writes no result file                                    | code-scout gave no result file   |
      | writes a result file that is not JSON                    | is not a JSON object             |

  @r6
  Scenario: a worker's change to a file under .shop/work/ outside its run directory is put back
    Pins that only work run writes a work-item's status and the initiative's files, while the worker's run directory keeps what it wrote.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also setting w1's status to green, changing .shop/work/i1/initiative.md and writing notes.md in its run directory
    When the person runs `work run i1`
    Then .shop/work/i1/initiative.md is as it was
    And log.jsonl's first move of w1 is from drafted to researched
    And the researcher's notes.md is in its run directory

  @r6
  Scenario: a file a worker adds under .shop/work/ outside its run directory is removed
    Pins that .shop/work/ outside the worker's run directory is as it was before the worker started, new files included.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also writing .shop/work/i1/w9.md and .shop/work/i2/initiative.md
    When the person runs `work run i1`
    Then .shop/work/i1/w9.md and .shop/work/i2/ are not there
    And w1 is green

  @r7
  Scenario: each move is a commit of the work-item's file, its run directory and log.jsonl on the initiative branch, and nothing else
    Pins one commit per move, and that a move's commit takes no file but its own.
    Given i1's work-item w1 is drafted
    And README.md has a change that is not committed
    And every worker gives DONE
    When the person runs `work run i1`
    Then the initiative branch has one commit for each move log.jsonl gives, `work: w1 drafted -> researched` first and `work: w1 done -> green` last
    And each of those commits changes .shop/work/i1/w1.md and .shop/work/i1/log.jsonl, and nothing but them and files under .shop/work/i1/runs/w1/
    And README.md's change is still not committed

  @r8
  Scenario: a worker's start and end are lines in log.jsonl with the time, the work-item, the stage, the agent and the session id
    Pins what work run records of each worker, the session id being the one claude was given.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then log.jsonl has, for each of w1's four workers, a start line and then an end line, each with the time, w1, the stage, the agent and the session id claude was given

  @r9
  Scenario: when no work-item can move, work run exits, printing each work-item's status and each open question
    Pins what the person reads when work run stops, and that an open question is its own exit.
    Given i1's work-items w1 is drafted and w2 is green
    And the researcher gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then work run prints w1 with awaiting-ruling and the question "Which module owns the log?", and w2 with green
    And it exits 3

  @r10
  Scenario Outline: work run that cannot do what it was asked exits non-zero, says why in one line, and changes nothing
    Pins that work run checks what it was given before any worker starts, and a refused move is its refusal.
    Given <state>
    When the person runs `work run <initiative>`
    Then work says in one line that <reason>
    And it exits non-zero
    And no worker was started
    And nothing in the repository has changed, its commits included

    Examples:
      | state                                                                        | initiative | reason                                                                                    |
      | i1's work-item w1 is drafted                                                 | i9         | the initiative i9 does not exist                                                          |
      | i1's work-item w1 is drafted, though log.jsonl's last move of w1 is to researched | i1     | .shop/work/i1/w1.md gives its status as drafted, but log.jsonl's last move of w1 is to researched |
      | i1's work-item w1 is drafted, in a directory that is not a git repository     | i1         | not a git repository                                                                      |

  @r4 @r5 @r10
  Scenario Outline: a run's worktrees are removed when the run ends, whatever the implementer's work came to: <outcome>
    Pins that work run leaves no worktree behind, on a merge, a question or a failure.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer <doing>
    When the person runs `work run i1`
    Then .shop/worktrees/w1 is not there, and git lists no worktree but the repository's own

    Examples:
      | outcome    | doing                                          |
      | merged     | committing feature.txt                         |
      | a question | committing feature.txt and suite-fail          |
      | BLOCKED    | giving BLOCKED, asking "Is the old reader kept?" |
      | a failure  | deleting its own branch                        |

  @r10
  Scenario: a git command that fails ends work run with git's reason in one line and a non-zero exit
    Pins that a failure of git mid-run is work run's refusal, never a traceback.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer deleting its own branch
    When the person runs `work run i1`
    Then work says in one line that git merge --ff-only work/w1 failed
    And it exits non-zero
