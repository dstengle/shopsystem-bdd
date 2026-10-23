# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  Background:
    Given a git repository with an initiative i1 under .shop/work/, a remote the initiative branch can be pushed to, a stand-in claude first on PATH and as $SHOPSYSTEM_WORK_CLAUDE, and tests that pass

  @r1
  Scenario: `work run` pulls each work-item through research, plan, implementation and review, one worker at a time, until no work-item can make a transition
    Pins the stage-by-stage pull: every work-item reaches `green` through its four workers in order, and no worker starts before the last one ended.
    Given i1's work-items w1 and w2 are drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1 and w2 had code-scout, bdd-planner, bdd-implementer and bdd-task-reviewer as its workers, in that order
    And no worker was started before the one before it had ended
    And w1 and w2 are green

  @r2
  Scenario: each worker is a new `claude -p` session of its stage's agent, given one brief naming the work-item, the files to read and where its result goes
    Pins how a worker is started: its stage's agent, a session no other worker had, and one brief that says what to read and where the result goes.
    Given i1's work-item w1 is drafted, under thing
    And every worker gives DONE
    When the person runs `work run i1`
    Then each worker was started as `claude -p` with an input prompt naming its brief, --agent shopsystem-bdd:<its stage's agent> and a session id no other worker had
    And each brief names .shop/work/i1/w1.md and spec/capabilities/thing.md to read, and where the worker's result goes

  @r2
  Scenario Outline: a work-item that is <status> is given a worker of <agent>
    Pins which agent each status starts.
    Given i1's work-item w1 is <status>
    And every worker gives DONE
    When the person runs `work run i1`
    Then the first worker started for w1 was a `claude -p` session of shopsystem-bdd:<agent>

    Examples:
      | status     | agent             |
      | drafted    | code-scout        |
      | researched | bdd-planner       |
      | ready      | bdd-implementer   |
      | done       | bdd-task-reviewer |

  @r3
  Scenario: a worker's outcome DONE makes the work-item's transition to its next status
    Pins the transitions DONE makes, in the lifecycle's order, from where the work-item stands.
    Given i1's work-item w1 is researched
    And every worker gives DONE
    When the person runs `work run i1`
    Then log.jsonl gives w1's transitions from researched to planned, ready, claimed, done and green, in that order

  @r4
  Scenario: an implementer's DONE is merged into the initiative branch when the work-item's scenarios and the whole suite pass on its branch
    Pins that the merge is of the implementer's own commit, tested where that commit is.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And the work-item's scenarios pass only where feature.txt is
    When the person runs `work run i1`
    Then the initiative branch has the implementer's commit of feature.txt

  @r4
  Scenario Outline: an implementer's DONE whose <tests> fail is not merged
    Pins that a failing test keeps the branch out of the initiative branch.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And <tests> fail on the implementer's branch
    When the person runs `work run i1`
    Then the initiative branch does not have the implementer's commit

    Examples:
      | tests                     |
      | the work-item's scenarios |
      | the whole suite           |

  @r4
  Scenario: an implementer's DONE whose scenarios pass only on a file it left uncommitted is not merged
    Pins that the scenarios and the suite run on the branch, which is what the merge takes: a file the implementer wrote and did not commit is not there.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer writing feature.txt and not committing it
    And the work-item's scenarios pass only where feature.txt is
    When the person runs `work run i1`
    Then the initiative branch does not have feature.txt

  @r4
  Scenario: an implementer's DONE whose whole suite fails only on a scenario r43 counts as expected is merged
    Pins that a failure of work another work-item of the initiative has still to do does not keep the work-item branch out of the initiative branch.
    Given i1's work-item w1 is ready, accepting thing#r1, and w2 is awaiting-answer, accepting thing#r2
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And every worker gives DONE, the implementer committing feature.txt
    And the work-item's scenarios pass only where feature.txt is
    When the person runs `work run i1`
    Then the initiative branch has the implementer's commit of feature.txt

  @r5
  Scenario Outline: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer
    Pins that work that fails the tests waits on the person.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And <tests> fail on the implementer's branch
    When the person runs `work run i1`
    Then w1 is awaiting-answer

    Examples:
      | tests                     |
      | the work-item's scenarios |
      | the whole suite           |

  @r5
  Scenario Outline: a researcher that gives <outcome> makes the work-item's transition to awaiting-answer
    Pins that any outcome but DONE stops the work-item for the person.
    Given i1's work-item w1 is drafted
    And the researcher gives <outcome>
    When the person runs `work run i1`
    Then w1 is awaiting-answer

    Examples:
      | outcome                                                  |
      | QUESTION, asking "Which module owns the log?"            |
      | BLOCKED, asking "Is the old reader kept?"                |
      | NEEDS_CONTEXT                                            |

  @r6
  Scenario: a worker's change to a file under .shop/work/ outside its stage directory is put back
    Pins that only `work run` writes the initiative's files, while the worker's stage directory keeps what it wrote.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also changing .shop/work/i1/initiative.md and writing notes.md in its stage directory
    When the person runs `work run i1`
    Then .shop/work/i1/initiative.md is as it was
    And the researcher's notes.md is in its stage directory

  @r6
  Scenario: a file a worker adds under .shop/work/ outside its stage directory is removed
    Pins that .shop/work/ outside the worker's stage directory is as it was before the worker started, new files included.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also writing .shop/work/i1/w9.md and .shop/work/i2/initiative.md
    When the person runs `work run i1`
    Then .shop/work/i1/w9.md and .shop/work/i2/ are not there

  @r6
  Scenario: a file committed under .shop/work/ in the repository's own checkout while a worker works is kept
    Pins that `work run` puts back only what a worker changed, in its worktree or on its branch, and never a change made elsewhere.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and while the researcher works another session commits .shop/work/i2/initiative.md and a change to .shop/work/i1/initiative.md in the repository's own checkout
    When the person runs `work run i1`
    Then .shop/work/i2/initiative.md and .shop/work/i1/initiative.md are as that session committed them, with nothing under .shop/work/ left uncommitted

  @r6
  Scenario Outline: an implementer's commit <change> under .shop/work/ is put back on its branch
    Pins that a worker's commit cannot write a status or any other file under .shop/work/ onto its work-item branch.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt and <change>
    When the person runs `work run i1`
    Then the branch work/w1 changes nothing under .shop/work/

    Examples:
      | change                                          |
      | setting .shop/work/i1/w1.md's status to green   |
      | deleting .shop/work/i1/initiative.md            |
      | adding .shop/work/i1/w9.md                      |

  @r7
  Scenario: each transition is a commit of the work-item's file, its stage directories and log.jsonl on the initiative branch, and nothing else
    Pins one commit per transition, and that a transition's commit takes no file but its own.
    Given i1's work-item w1 is drafted
    And README.md has a change that is not committed
    And every worker gives DONE
    When the person runs `work run i1`
    Then the initiative branch has one commit for each transition log.jsonl gives
    And each of those commits changes .shop/work/i1/w1.md and .shop/work/i1/log.jsonl, and nothing but them and w1's stage directories
    And README.md's change is still not committed

  @r8
  Scenario: a worker's start and end are lines in log.jsonl with the time, the work-item, the stage, the agent and the session id
    Pins what `work run` writes of each worker, the session id being the one claude was given.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then log.jsonl has, for each of w1's four workers, a start line and then an end line, each with the time, w1, the stage, the agent and the session id claude was given

  @r9
  Scenario: when every work-item is green or withdrawn, `work run` exits successfully, printing each work-item's status
    Pins that a delivery whose work-items all ended well, or were set aside, is no failure.
    Given i1's work-items w1 is green and w2 is withdrawn
    When the person runs `work run i1`
    Then `work run` prints w1 with green, and w2 with withdrawn
    And it exits successfully

  @r32
  Scenario: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question
    Pins what the person reads when `work run` stops on a question, and that waiting on the person is an error.
    Given i1's work-items w1 is drafted and w2 is green
    And the researcher gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then `work run` prints w1 with awaiting-answer and the question "Which module owns the log?", and w2 with green
    And it exits with an error

  @r32
  Scenario: `work run` prints a question that has no answer yet, and not one that has an answer
    Pins that an open question is one with no answer yet.
    Given i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer
    And i1's work-item w2 is awaiting-answer, its ## Questions section with "Old question?" and its Answers section "Old answer."
    When the person runs `work run i1`
    Then `work run` prints the question "Which module owns the log?"
    And it prints neither "Old question?" nor "Old answer."
    And it exits with an error

  @r52
  Scenario: when no work-item can make a transition and one is failed, `work run` exits with an error, printing each work-item's status and each fault
    Pins what the person reads when `work run` stops on a fault already recorded, and that a failed work-item is an error.
    Given i1's work-item w1 is failed, its fault recorded as "git merge --ff-only work/w1 failed"
    And i1's work-item w2 is green
    When the person runs `work run i1`
    Then `work run` prints w1 with failed and the fault "git merge --ff-only work/w1 failed", and w2 with green
    And it exits with an error

  @r53
  Scenario: a push that fails after the branch review's commit ends `work run` with an error, saying why
    Pins that a branch review kept only on the machine is an error the person is told of, even when every work-item ended well.
    Given i1's work-items w1 is green and w2 is withdrawn
    And the remote refuses pushes to the initiative branch once the branch reviewer has started
    When the person runs `work run i1`
    Then work says that it cannot push the initiative branch to the remote
    And it exits with an error

  @r54
  Scenario: when `work run` starts and the initiative branch has commits the remote does not have, it pushes the initiative branch before anything else
    Pins that work committed before the delivery, and never pushed, reaches the remote before any worker starts.
    Given i1's work-item w1 is drafted
    And the initiative branch has a commit of notes.txt that the remote does not have
    And every worker gives DONE
    When the person runs `work run i1`
    Then before the researcher was started, the remote's initiative branch had the commit of notes.txt

  @r10
  Scenario Outline: `work run` that cannot do what it was asked exits with an error, says why, and changes nothing
    Pins that `work run` verifies what it was given before any worker starts, and a refused transition is its refusal.
    Given <setup>
    When the person runs `work run <initiative>`
    Then work says that <reason>
    And it exits with an error
    And no worker was started
    And nothing in the repository has changed, its commits included

    Examples:
      | setup                                                                        | initiative | reason                                                                                    |
      | i1's work-item w1 is drafted                                                 | i9         | the initiative i9 does not exist                                                          |
      | i1's work-item w1 is drafted, though log.jsonl's last transition of w1 is to researched | i1 | .shop/work/i1/w1.md gives its status as drafted, but log.jsonl's last transition of w1 is to researched |
      | i1's work-item w1 is drafted, in a directory that is not a git repository     | i1         | not a git repository                                                                      |
      | i1's work-item w1 is drafted, its checkout's HEAD detached                    | i1         | HEAD is detached                                                                          |
      | i1's work-item w1 is drafted, and `work run` is started by a worker of another `work run` | i1 | it was started by a worker of another `work run`                                   |

  @r11
  Scenario: each worker is given this plugin's own directory as its plugin
    Pins that the agents a worker is started as are this plugin's, not those of another copy of it installed on the machine.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four workers was started with --plugin-dir the directory that holds `work run`'s own scripts

  @r12
  Scenario Outline: a worker whose agent lists skills may load each of them, and no other worker may: the <who> loading <skill>, <tools>
    Pins that a `claude -p --agent` worker, whose agent's skills are not preloaded, can load them itself, whatever list .shop/delivery.toml gives its stage.
    Given i1's work-item w1 is drafted
    And <tools>
    And every worker gives DONE, the <who> loading the skill <skill>
    When the person runs `work run i1`
    Then the <who>'s load of the skill <skill> was <fate>

    Examples:
      | who         | skill                        | tools                                                                       | fate    |
      | implementer | shopsystem-bdd:bdd-red-green | .shop/delivery.toml names no tools                                          | run     |
      | implementer | shopsystem-bdd:bdd-red-green | .shop/delivery.toml gives the implement stage Read and Bash(git commit *)   | run     |
      | researcher  | shopsystem-bdd:bdd-red-green | .shop/delivery.toml names no tools                                          | refused |

  @r13
  Scenario Outline: no worker is given a bare Write or Edit tool, so a write outside its worktree is refused: <tools>
    Pins that a worker's writes stay in the worktree it was started in, even when .shop/delivery.toml lists a bare Write.
    Given i1's work-item w1 is drafted
    And <tools>
    And every worker gives DONE, the researcher also writing notes.md into the repository's own checkout
    When the person runs `work run i1`
    Then no worker was given a bare Write or Edit in its --allowedTools
    And the researcher's write into the repository's own checkout was refused, and no notes.md is there

    Examples:
      | tools                                                         |
      | .shop/delivery.toml names no tools                            |
      | .shop/delivery.toml gives the research stage Read and Write   |

  @r14
  Scenario Outline: a worker's Bash runs only python3 -m pytest, the plugin's scripts by path and its stage's git commands: the <who>'s `<command>` is <fate>
    Pins that no worker runs any Python or git command it likes: `{scripts}` stands for the directory of `work run`'s own scripts.
    Given i1's work-item w1 is drafted
    And .shop/delivery.toml names no tools
    And every worker gives DONE, the <who> running `<command>`
    When the person runs `work run i1`
    Then its `<command>` was <fate>

    Examples:
      | who         | command                                 | fate    |
      | researcher  | python3 -m pytest --version             | run     |
      | researcher  | python3 {scripts}/features --help       | run     |
      | researcher  | python3 -c pass                         | refused |
      | researcher  | python3 {scripts}/work --help           | refused |
      | researcher  | git commit -q --allow-empty -m meddle   | refused |
      | planner     | git status                              | refused |
      | implementer | python3 -m pytest --version             | run     |
      | implementer | python3 -c pass                         | refused |
      | implementer | git log -1                              | refused |
      | implementer | python3 {scripts}/work show             | refused |
      | reviewer    | git log -1                              | run     |
      | reviewer    | python3 -c pass                         | refused |

  @r15
  Scenario: a file the worker's result names is copied into the stage directory before its worktree is removed
    Pins that what a worker's result points to is still there for the person and the next worker once its worktree is gone.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer writing report.md at the top of its worktree and naming it as its report
    When the person runs `work run i1`
    Then w1's implementation stage directory has report.md, as the implementer wrote it

  @r16
  Scenario: a researcher's DONE with questions puts those questions into the planner's brief
    Pins that what the researcher asked reaches the planner, rather than being asked again.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher asking "Is a title given twice one book or two?"
    When the person runs `work run i1`
    Then the planner's brief has the researcher's question "Is a title given twice one book or two?"

  @r17
  Scenario: each worker's brief tells it that it starts in its worktree and never changes directory
    Pins that no worker spends its turns on a `cd` that nobody approves under `work run`.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four briefs says that the worker starts in its worktree, the directory it was started in, and never changes directory

  @r18
  Scenario: the work-item branch is deleted when `work run` merges it
    Pins that a merged work-item leaves no branch of its own behind.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    When the person runs `work run i1`
    Then git lists no branch work/w1

  @r19
  Scenario: a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns
    Pins that the researcher starts from the work-item's file set and accepted scenarios, rather than searching the repository for it, and ends within a bounded number of turns.
    Given i1's work-item w1 is drafted, its file set scripts/thing.py and tests/test_thing.py
    And features/thing.feature has the scenario "it answers", tagged @r1, and the scenario "it waits", tagged @r2
    And every worker gives DONE
    When the person runs `work run i1`
    Then the researcher's brief gives scripts/thing.py and tests/test_thing.py as the work-item's file set
    And the researcher's brief names the accepted scenario "it answers" of features/thing.feature, and not "it waits"
    And the researcher was started with a limit of 40 turns

  @r20
  Scenario: two ready work-items whose claims would not share a file are implemented at the same time, and merged one at a time
    Pins that work-items with no file in common are implemented side by side, while the initiative branch takes one branch at a time, each on top of the one before.
    Given i1's work-items w1 is ready, its file set w1.txt, and w2 is ready, its file set w2.txt
    And every worker gives DONE, each implementer committing a file named for its work-item once two implementers have started
    When the person runs `work run i1`
    Then the implementers of w1 and w2 worked at the same time
    And the initiative branch has both implementers' commits, one after the other, with no merge commit

  @r20
  Scenario Outline: two ready work-items whose claims would share a file are implemented one after the other: <how>
    Pins that two implementers never edit one file: a glob or a directory in a file set covers each tracked file it holds.
    Given the repository has lib/thing_a.py committed
    And i1's work-items w1 is ready, its file set <first>, and w2 is ready, its file set <second>
    And every worker gives DONE, each implementer committing a file named for its work-item
    When the person runs `work run i1`
    Then no implementer was started before the one before it had ended

    Examples:
      | how             | first                  | second                 |
      | a file in both  | shared.txt and w1.txt  | shared.txt and w2.txt  |
      | a glob          | lib/thing*.py          | lib/thing_a.py         |
      | a directory     | lib/                   | lib/thing_a.py         |

  @r20
  Scenario: of three ready work-items whose claims would not share a file, no more than two are implemented at the same time
    Pins the limit of two side by side.
    Given i1's work-items w1 is ready, its file set w1.txt, w2 is ready, its file set w2.txt, and w3 is ready, its file set w3.txt
    And every worker gives DONE, each implementer committing a file named for its work-item once two implementers have started
    When the person runs `work run i1`
    Then two implementers worked at the same time, and never three

  @r21
  Scenario: `work run` started by a worker of another `work run` refuses, saying so
    Pins that a worker cannot start a delivery of its own.
    Given i1's work-item w1 is drafted
    When `work run i1` is started by a worker of another `work run`
    Then `work run` refuses, saying that it was started by a worker of another `work run`

  @r22
  Scenario: every pytest command `work run` starts for a work-item, the whole suite's included, is given --work-item with the work-item's name
    Pins that the plugin's option goes to each pytest run `work run` starts for the work-item.
    Given i1's work-item w1 is ready
    And .shop/delivery.toml gives no [tests]
    And every worker gives DONE, the implementer committing feature.txt
    When the person runs `work run i1`
    Then each pytest command `work run` ran for w1, for its scenarios and for the whole suite, was given --work-item w1

  @r22
  Scenario: a worker's own pytest command is given --work-item with its work-item's name
    Pins that a worker's pytest selects the scenarios its work-item accepts without the worker naming them.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer running `python3 -m pytest -q`
    When the person runs `work run i1`
    Then the implementer's `python3 -m pytest -q` ran with --work-item w1

  @r55
  Scenario: a worker's pytest run of a test that is not a scenario runs that test
    Pins that `--work-item` keeps what no work-item can accept, such as a researcher's probe file, instead of refusing the run.
    Given i1's work-item w1 is drafted
    And the repository holds test_probe.py, a test that is not a scenario, which writes probe.ran when it runs
    And every worker gives DONE, the researcher running `python3 -m pytest -q test_probe.py`
    When the person runs `work run i1`
    Then the researcher's `python3 -m pytest -q test_probe.py` ran test_probe.py's test

  @r56
  Scenario: a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused
    Pins that `--work-item` still refuses a run that would show the worker none of its work-item's scenarios.
    Given i1's work-item w1 is ready, accepting other#r1
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And every worker gives DONE, the implementer running `python3 -m pytest -q`
    When the person runs `work run i1`
    Then the implementer's `python3 -m pytest -q` was refused, saying that w1 accepts none of the scenarios it collected

  @r23
  Scenario: when the repository is inside the plugin's own directory, the workers' worktrees are outside it
    Pins that `work run` delivering this plugin's own work gives workers writable worktrees: claude refuses every write under a --plugin-dir, so none may lie under the plugin's directory.
    Given i1's work-item w1 is drafted
    And the repository is the plugin: it holds `work run`'s own scripts and agents
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four workers worked in a worktree in a temporary directory outside the plugin's directory

  @r24
  Scenario: the whole suite is run in the implementer's worktree before it starts, and its brief says how it ended
    Pins that the implementer knows from its brief whether the suite it starts from passes.
    Given i1's work-item w1 is ready
    And every worker gives DONE
    When the person runs `work run i1`
    Then the whole suite was run in the implementer's worktree before the implementer was started
    And the implementer's brief says how that run of the suite ended

  @r25
  Scenario: each worker's brief names the plugin's scripts directory, the initiative branch's base, its worktree and its work-item branch
    Pins what the brief gives every worker so that it need not look for where it is.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four briefs names the plugin's scripts directory, the initiative branch's base, the worker's worktree and its work-item branch

  @r26 @deprecated
  Scenario: a work-item whose transition is to awaiting-ruling keeps its work-item branch (deprecated)
    Deprecated for: a work-item whose transition is to awaiting-answer keeps its work-item branch
    Pins that the implementer's work is still there for the person to rule on.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And the whole suite fails on the implementer's branch
    When the person runs `work run i1`
    Then git lists the branch work/w1, with the implementer's commit of feature.txt

  @r26
  Scenario: a work-item whose transition is to awaiting-answer keeps its work-item branch
    Pins that the implementer's work is still there for the person to answer on.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt
    And the whole suite fails on the implementer's branch
    When the person runs `work run i1`
    Then git lists the branch work/w1, with the implementer's commit of feature.txt

  @r27
  Scenario: when every work-item is green or withdrawn and a commit since the kept branch review is unread, a bdd-branch-reviewer reviews the initiative branch from its base
    Pins that a commit no kept branch review has read, made after one was kept, brings a new review of the whole branch once its work-items are done.
    Given i1's work-item w1 is green and a kept branch review has read every commit on the initiative branch
    And i1's work-item w2 was added after that review and is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then after w2 was green a `claude -p` session of shopsystem-bdd:bdd-branch-reviewer was started, given one brief naming the initiative branch and its base

  @r47
  Scenario: the branch reviewer's directory is copied under .shop/work/i1/runs/branch-review/ when its session ends
    Pins that the branch reviewer's brief and findings are kept in the initiative once its session is over.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and the branch reviewer writes findings.md beside its brief
    When the person runs `work run i1`
    Then a directory under .shop/work/i1/runs/branch-review/ holds the branch reviewer's brief and its findings.md, as it wrote them

  @r48
  Scenario: the branch reviewer's directory under .shop/work/i1/runs/branch-review/ is committed on the initiative branch
    Pins that the branch review is part of the initiative branch's history, not a file left uncommitted in the checkout.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and the branch reviewer writes findings.md beside its brief
    When the person runs `work run i1`
    Then the initiative branch has a commit of the branch reviewer's directory under .shop/work/i1/runs/branch-review/, its findings.md included
    And nothing under .shop/work/i1/runs/branch-review/ is left uncommitted

  @r49
  Scenario: the branch reviewer's start and end are lines in log.jsonl with the time, the stage branch-review, the agent and the session id
    Pins what `work run` writes of the branch reviewer, the session id being the one claude was given.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and the branch reviewer ends
    When the person runs `work run i1`
    Then log.jsonl has, for the branch reviewer, a start line and then an end line, each with the time, the stage branch-review, the agent bdd-branch-reviewer and the session id claude was given

  @r50
  Scenario: while a kept branch review has read every commit on the initiative branch but its own, no branch review is started
    Pins that the commit a branch review is kept in does not by itself bring another review.
    Given i1's work-items w1 is green and w2 is withdrawn
    And a kept branch review has read every commit on the initiative branch, and its own commit is the initiative branch's last
    When the person runs `work run i1`
    Then no session of bdd-branch-reviewer was started

  @r51
  Scenario: a push that cannot be verified before the branch review ends `work run` with an error, saying why, and no branch review is started
    Pins that a branch review is never spent on a branch whose review could not be pushed.
    Given i1's work-items w1 is green and w2 is withdrawn
    And the remote refuses pushes to the initiative branch
    When the person runs `work run i1`
    Then work says that it cannot push the initiative branch to the remote
    And it exits with an error
    And no session of bdd-branch-reviewer was started

  @r28
  Scenario: a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file
    Pins that `.shop/work/` in the main checkout is only what its last commit holds whenever a worker ends, and that a change there is a fault, not a question.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and while the researcher works another session changes .shop/work/i1/initiative.md in the repository's own checkout without committing it
    When the person runs `work run i1`
    Then .shop/work/i1/initiative.md is as its last commit holds it
    And w1 is failed, naming .shop/work/i1/initiative.md

  @r29
  Scenario: the [tests] .shop/delivery.toml gives are run in place of `work run`'s own commands
    Pins that a repository chooses how its work-item's scenarios and its suite are run.
    Given i1's work-item w1 is ready
    And .shop/delivery.toml gives [tests] with `python3 tests.py --work-item w1` for the work-item's scenarios and `python3 tests.py` for the suite
    And every worker gives DONE, the implementer committing feature.txt
    When the person runs `work run i1`
    Then `work run` ran `python3 tests.py --work-item w1` for w1's scenarios and `python3 tests.py` for the suite

  @r30
  Scenario Outline: a stage's [allowed_tools] in .shop/delivery.toml is its worker's list in place of its own, less any bare Write or Edit: <tools>
    Pins that a repository chooses a stage's tools, its Bash commands included, but never a bare Write or Edit.
    Given i1's work-item w1 is drafted
    And .shop/delivery.toml gives the research stage <tools>
    And every worker gives DONE
    When the person runs `work run i1`
    Then the researcher was given --allowedTools <list>

    Examples:
      | tools                        | list                     |
      | Read and Grep                | Read,Grep                |
      | Read and Bash(git commit *)  | Read,Bash(git commit *)  |
      | Read, Write and Edit         | Read                     |

  @r31
  Scenario: a planner's DONE with a `fileset` writes that file set into the work-item as it makes the transition to planned
    Pins that the planner's file set is the work-item's from planned on.
    Given i1's work-item w1 is researched, its file set scripts/thing.py
    And every worker gives DONE, the planner's result giving a `fileset` of scripts/thing.py and tests/test_thing.py
    When the person runs `work run i1`
    Then the commit of w1's transition to planned writes `fileset:` scripts/thing.py and tests/test_thing.py into .shop/work/i1/w1.md

  @r33
  Scenario Outline: every worktree `work run` made is removed when it exits, whatever the implementer's work came to: <end>
    Pins that `work run` leaves no worktree behind, on a merge, a question or a failure.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer <doing>
    When the person runs `work run i1`
    Then git lists no worktree but the repository's own

    Examples:
      | end        | doing                                            |
      | merged     | committing feature.txt                           |
      | a question | committing feature.txt and suite-fail            |
      | BLOCKED    | giving BLOCKED, asking "Is the old reader kept?" |
      | a failure  | deleting its own branch                          |

  @r34
  Scenario Outline: a <who> that changes <path> outside its stage directory makes the work-item's transition to failed, recording the file, its branch unmerged
    Pins that a worker breaking the rule on .shop/work/ is a fault, not a question, and none of its work reaches the initiative branch.
    Given i1's work-item w1 is <status>
    And every worker gives DONE, the <who> <change>
    When the person runs `work run i1`
    Then w1 is failed, recording <path>
    And the initiative branch has none of the branch work/w1's commits

    Examples:
      | who         | status  | change                                                                  | path                         |
      | researcher  | drafted | changing .shop/work/i1/initiative.md                                    | .shop/work/i1/initiative.md  |
      | implementer | ready   | committing feature.txt and .shop/work/i1/w1.md's status set to green    | .shop/work/i1/w1.md          |
      | implementer | ready   | committing feature.txt and the deletion of .shop/work/i1/initiative.md  | .shop/work/i1/initiative.md  |
      | implementer | ready   | committing feature.txt and a new .shop/work/i1/w9.md                    | .shop/work/i1/w9.md          |

  @r35
  Scenario: `work run` verifies that it can push the initiative branch before it starts each worker and the branch reviewer
    Pins that a push that would fail is found before a worker's or the branch reviewer's work is spent.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and the branch reviewer ends
    When the person runs `work run i1`
    Then before each of w1's four workers was started, and before the branch reviewer was started, `work run` had verified that it can push the initiative branch to the remote

  @r36
  Scenario: a question goes into the work-item's ## Questions, before a section that follows it
    Pins where the question is written, so that what follows the Questions section is never read as a question.
    Given i1's work-item w1 is drafted, its file with a ## Questions of "Old question?" and then an Answers section with "Old answer."
    And the researcher gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then w1's ## Questions holds "Old question?" and then "Which module owns the log?", and its Answers section only "Old answer."

  @r37 @deprecated
  Scenario Outline: no worker is started for a work-item that is <status> (deprecated)
    Deprecated for: no worker is started for a work-item that is <status>
    Pins that a work-item waiting on the person, or on a remedy, takes no stage.
    Given i1's work-item w1 is <status>
    And every worker gives DONE
    When the person runs `work run i1`
    Then no worker was started for w1

    Examples:
      | status          |
      | awaiting-ruling |
      | failed          |

  @r37
  Scenario Outline: no worker is started for a work-item that is <status>
    Pins that a work-item waiting on the person, or on a remedy, takes no stage.
    Given i1's work-item w1 is <status>
    And every worker gives DONE
    When the person runs `work run i1`
    Then no worker was started for w1

    Examples:
      | status          |
      | awaiting-answer |
      | failed          |

  @r37
  Scenario: no worker is started for a work-item after its transition to awaiting-answer
    Pins that a question stops the work-item's stages within the delivery that raised it.
    Given i1's work-item w1 is drafted
    And the researcher gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then no worker was started for w1 after the researcher

  @r38
  Scenario: `work run` pushes the initiative branch after each commit it makes on it
    Pins that no committed transition or merge is left only on the machine.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then after each commit `work run` made on the initiative branch, it pushed the initiative branch to the remote
    And the remote's initiative branch is at the initiative branch's head

  @r39
  Scenario: a push that cannot be verified makes the work-item's transition to failed, recording why, before any worker starts
    Pins that a remote that would refuse the work stops it before it is done.
    Given i1's work-item w1 is drafted
    And the remote refuses pushes to the initiative branch
    When the person runs `work run i1`
    Then w1 is failed, recording why the push could not be verified
    And no worker was started

  @r40
  Scenario: a work-item's transition to failed ends `work run` with an error naming the work-item and its fault
    Pins that a fault is reported to the person as the reason the delivery stopped.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also changing .shop/work/i1/initiative.md
    When the person runs `work run i1`
    Then `work run` names w1 and that its researcher changed .shop/work/i1/initiative.md
    And it exits with an error

  @r40
  Scenario: a work-item's transition to failed for a push that cannot be verified ends `work run` with an error naming the work-item and its fault
    Pins that the person learns the work-item and its fault even when the remote refuses every push, that of the failure included.
    Given i1's work-item w1 is drafted
    And the remote refuses pushes to the initiative branch
    When the person runs `work run i1`
    Then `work run` names w1 and that it cannot push the initiative branch to the remote
    And it exits with an error

  @r41
  Scenario Outline: a git command that fails during a stage makes the work-item's transition to failed, recording git's reason: <fault>
    Pins that a failure of git during a delivery is a fault of the work-item, never a traceback or a question.
    Given i1's work-item w1 is ready
    And every worker gives DONE, <doing>
    When the person runs `work run i1`
    Then w1 is failed, recording that <reason>

    Examples:
      | fault      | doing                                                         | reason                                                      |
      | the merge  | the implementer deleting its own branch                       | git merge --ff-only work/w1 failed, with git's reason       |
      | a push     | the remote refusing pushes once the implementer has started   | the push of the initiative branch failed, with git's reason |

  @r42
  Scenario Outline: a worker that ends without a result file `work run` can read makes the work-item's transition to failed, recording how its session ended: <result>
    Pins that a worker leaving no readable result is a fault, not a question, and the person learns how its session ended.
    Given i1's work-item w1 is drafted
    And the researcher's session ends with no error and before its turn limit, <result>
    When the person runs `work run i1`
    Then w1 is failed, recording how the researcher's session ended

    Examples:
      | result                                        |
      | having written no result file                 |
      | having written a result file that is not JSON |

  @r43
  Scenario Outline: before a merge, a failing scenario whose requirement is accepted by <accepted by> is counted as <counted>
    Pins that the suite before a merge expects the failures of work not yet done by another work-item of the initiative, and no other.
    Given i1's work-item w1 is ready, accepting thing#r1, w2 is drafted, w3 is green and w4 is withdrawn
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And thing#r2 is accepted by <accepted by>
    And every worker gives DONE, the implementer committing feature.txt
    When the person runs `work run i1`
    Then the whole suite `work run` ran before w1's merge counted "it waits" as <counted>

    Examples:
      | accepted by     | counted          |
      | w2 only         | expected         |
      | w2 and w1       | expected         |
      | w2 and w3       | expected         |
      | w3 only         | not expected     |
      | w4 only         | not expected     |
      | w1 only         | not expected     |
      | no work-item    | not expected     |

  @r44
  Scenario: each worker's brief tells it to write its result file first with the outcome PARTIAL, and keep it current as it works
    Pins that a worker that stops part-way still leaves a result for `work run` to read, and one that does not claim the work done.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four briefs tells the worker to write its result file first, with the outcome PARTIAL, and keep it current as it works

  @r45
  Scenario Outline: a worker whose session <ending> makes the work-item's transition to failed, whatever its result says
    Pins that a session cut short is a fault even when its result file claims the work done, and the person learns how it ended.
    Given i1's work-item w1 is drafted
    And the researcher's result file gives DONE, its session <ending>
    When the person runs `work run i1`
    Then w1 is failed, recording that the researcher's session <ended>

    Examples:
      | ending                                    | ended                                 |
      | ending in an error                        | ended in an error                     |
      | ending at its turn limit                  | ended at its turn limit               |
      | exiting with an error                     | exited with an error                  |
      | leaving output that holds no JSON result  | left output that holds no JSON result |

  @r46
  Scenario: `work run` started while .shop/work/ in the repository's own checkout has uncommitted changes exits with an error, naming them, and changes nothing
    Pins that `work run` never starts a worker over a change to .shop/work/ that it would put back when the worker ends.
    Given i1's work-item w1 is drafted
    And in the repository's own checkout .shop/work/i1/w1.md is changed and .shop/work/i1/w2.md is added, neither committed
    When the person runs `work run i1`
    Then work's error names .shop/work/i1/w1.md and .shop/work/i1/w2.md
    And it exits with an error
    And no worker was started
    And nothing in the repository has changed, its commits included

  @r57
  Scenario: the brief of a worker for a work-item that has answers holds each answer with the question it answers
    Pins that a worker is told what the person answered, each answer beside its question.
    Given i1's work-item w1 is drafted, its ## Questions section with "Which module owns the log?" and "Is the old reader kept?", and its Answers section with "The queue module." and "No."
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four briefs holds "Which module owns the log?" with "The queue module." and "Is the old reader kept?" with "No."

  @r58
  Scenario: an implementer started for a work-item whose work-item branch was kept works in a worktree on that branch
    Pins that the implementer carries on from the kept branch's commits and does not start again from the base.
    Given i1's work-item w1 is ready, and the branch work/w1 was kept with a commit of kept.txt
    And every worker gives DONE
    When the person runs `work run i1`
    Then the implementer of w1 worked in a worktree on the branch work/w1, with kept.txt in it
