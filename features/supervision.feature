# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  Background:
    Given a git repository with an initiative i1 under .shop/work/, a remote the initiative branch can be pushed to, a stand-in claude first on PATH and as $SHOPSYSTEM_WORK_CLAUDE, and tests that pass

  @r1
  Scenario: `work run` pulls each work-item through research, plan, implementation and review until no work-item can make a transition
    Pins the pull through the four stages: every work-item reaches `green` through its four workers, in the stages' order.
    Given i1's work-items w1 and w2 are drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1 and w2 had code-scout, bdd-planner, bdd-implementer and bdd-task-reviewer as its workers, in that order
    And w1 and w2 are green

  @r59
  Scenario: when more than one work-item is drafted or researched, their research and plan stages are started at the same time
    Pins that research and planning of different work-items do not wait on each other.
    Given i1's work-items w1 is drafted and w2 is researched
    And every worker gives DONE, the researcher of w1 and the planner of w2 each ending once both have started
    When the person runs `work run i1`
    Then the researcher of w1 and the planner of w2 worked at the same time

  @r60
  Scenario Outline: `work run` runs at most <limit> workers at the same time when .shop/delivery.toml <gives>
    Pins the bound on workers side by side: the repository's number where it gives one, and 4 where it gives none.
    Given i1's work-items w1, w2, w3, w4 and w5 are drafted
    And .shop/delivery.toml <gives>
    And every worker gives DONE, each researcher ending once <limit> workers have started
    When the person runs `work run i1`
    Then <limit> workers worked at the same time, and never more

    Examples:
      | gives                              | limit |
      | gives 2 as its number of workers   | 2     |
      | gives no number of workers         | 4     |

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

  @r3 @deprecated
  Scenario: a worker's outcome DONE makes the work-item's transition to its next status (deprecated)
    Deprecated for: removal
    Pins the transitions DONE makes, in the lifecycle's order, from where the work-item stands.
    Given i1's work-item w1 is researched
    And every worker gives DONE
    When the person runs `work run i1`
    Then log.jsonl gives w1's transitions from researched to planned, ready, claimed, done and green, in that order

  @r4
  Scenario Outline: an implementer whose result gives no question has its branch merged only if the work-item's scenarios and the whole suite pass on it: <case>
    Pins that the merge takes the implementer's committed work only when it passes where that work is, a failure of work another work-item has still to do excepted.
    Given i1's work-item w1 is ready, accepting thing#r1
    And the implementer's result gives no question, the implementer <doing>, and every other worker gives DONE
    And <tests>
    When the person runs `work run i1`
    Then the initiative branch <merged>

    Examples:
      | case                             | doing                                     | tests                                                                                                                                                                                | merged                                      |
      | both pass                        | committing feature.txt                    | the work-item's scenarios pass only where feature.txt is                                                                                                                             | has the implementer's commit of feature.txt |
      | the work-item's scenarios fail   | committing feature.txt                    | the work-item's scenarios fail on the implementer's branch                                                                                                                           | does not have the implementer's commit      |
      | the whole suite fails            | committing feature.txt                    | the whole suite fails on the implementer's branch                                                                                                                                    | does not have the implementer's commit      |
      | a file left uncommitted          | writing feature.txt and not committing it | the work-item's scenarios pass only where feature.txt is                                                                                                                             | does not have feature.txt                   |
      | a failure r43 counts as expected | committing feature.txt                    | the work-item's scenarios pass only where feature.txt is, and the whole suite fails only on "it waits", tagged @r2, while i1's work-item w2, accepting thing#r2, is awaiting-answer | has the implementer's commit of feature.txt |

  @r5 @deprecated
  Scenario Outline: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer (deprecated)
    Deprecated for: removal
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

  @r62
  Scenario: each stage's session.json records the path of the transcript of that stage's session
    Pins that the person can find, from a stage directory, the transcript of the session that did the stage.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then the session.json in each of w1's four stage directories records the path of the transcript of that stage's session

  @r9
  Scenario: when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status
    Pins that a delivery whose work-items all ended well, or were set aside, is no failure while no request this context asked waits on it.
    Given i1's work-items w1 is green and w2 is withdrawn
    And a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's
    When the person runs `work run i1`
    Then `work run` prints w1 with green, and w2 with withdrawn
    And it exits successfully

  @r101
  Scenario: when `work run` ends while a request whose asker is this context is in the asker's turn, it exits with an error, printing the request with its open questions
    Pins that a request this context asked, waiting on this context's own answer, stops the run as something for the person, even when every work-item ended well.
    Given i1's work-item w1 is green
    And a request q2 kept in this context whose asker is this context, awaiting-asker, its turn the asker's, with the question "Which unit is the limit in?" and no answer
    When the person runs `work run i1`
    Then `work run` prints q2 with the question "Which unit is the limit in?"
    And it exits with an error

  @r32
  Scenario: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question
    Pins what the person reads when `work run` stops on a question, and that waiting on the person is an error.
    Given i1's work-items w1 is researched and w2 is green
    And the planner gives QUESTION, asking "Which module owns the log?"
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

  @r15
  Scenario: a field of a worker's result giving a sentence longer than a file name may be is taken as no file
    Pins that text in a result that cannot be a file name neither stops the copy of the files it names nor the work-item.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer writing report.md at the top of its worktree and naming it as its report
    And the implementer's result also gives a field whose value is a sentence of over 255 characters, with spaces, naming no file
    When the person runs `work run i1`
    Then w1's implementation stage directory has report.md, as the implementer wrote it
    And w1 is green

  @r16 @deprecated
  Scenario: a researcher's DONE with questions puts those questions into the planner's brief (deprecated)
    Deprecated for: removal
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
  Scenario: a researcher is given the work-item's file set and accepted scenarios, and a limit of 80 turns
    Pins that the researcher starts from the work-item's file set and accepted scenarios, rather than searching the repository for it, and ends within a bounded number of turns.
    Given i1's work-item w1 is drafted, its file set scripts/thing.py and tests/test_thing.py
    And features/thing.feature has the scenario "it answers", tagged @r1, and the scenario "it waits", tagged @r2
    And every worker gives DONE
    When the person runs `work run i1`
    Then the researcher's brief gives scripts/thing.py and tests/test_thing.py as the work-item's file set
    And the researcher's brief names the accepted scenario "it answers" of features/thing.feature, and not "it waits"
    And the researcher was started with a limit of 80 turns

  @r20
  Scenario: two ready work-items whose claims would share no file are implemented at the same time, each in its own worktree
    Pins that work-items with no file in common are implemented side by side, neither in the other's worktree.
    Given i1's work-items w1 is ready, its file set w1.txt, and w2 is ready, its file set w2.txt
    And every worker gives DONE, each implementer committing a file named for its work-item once two implementers have started
    When the person runs `work run i1`
    Then the implementers of w1 and w2 worked at the same time
    And each of them worked in a worktree of its own

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
  Scenario: of three ready work-items whose claims would share no file, no more are implemented at the same time than .shop/delivery.toml's number of workers
    Pins that implementers side by side stay within the number of workers the repository gives.
    Given i1's work-items w1 is ready, its file set w1.txt, w2 is ready, its file set w2.txt, and w3 is ready, its file set w3.txt
    And .shop/delivery.toml gives 2 as its number of workers
    And every worker gives DONE, each implementer committing a file named for its work-item once two implementers have started
    When the person runs `work run i1`
    Then two implementers worked at the same time, and never three

  @r61
  Scenario: implementers working at the same time have the branches r4 merges merged one at a time, in the order they ended
    Pins that the initiative branch takes one work-item branch at a time, each on top of the one before, first the one whose implementer ended first.
    Given i1's work-items w1 is ready, its file set w1.txt, and w2 is ready, its file set w2.txt
    And each implementer's result gives no question, each implementer committing a file named for its work-item once two implementers have started, w2's implementer ending before w1's, and every other worker gives DONE
    And each work-item's scenarios and the whole suite pass on its branch
    When the person runs `work run i1`
    Then the implementers of w1 and w2 worked at the same time
    And the initiative branch has w2's implementer's commit and then w1's, with no merge commit

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
  Scenario: a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused when a requirement the work-item accepts is not of a guarantees capability
    Pins that one requirement outside a guarantees capability is enough for `--work-item` to refuse a run that shows the worker none of its work-item's scenarios.
    Given spec/capabilities/steady.md is a guarantees capability and spec/capabilities/other.md is not
    And i1's work-item w1 is ready, accepting steady#r1 and other#r1
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And every worker gives DONE, the implementer running `python3 -m pytest -q`
    When the person runs `work run i1`
    Then the implementer's `python3 -m pytest -q` was refused, saying that w1 accepts none of the scenarios it collected

  @r64
  Scenario: a worker's pytest run that collects scenarios, for a work-item every requirement of which is of a guarantees capability, deselects each of them
    Pins that a work-item checked by measurement rather than by scenarios runs no scenario, instead of having its run refused.
    Given spec/capabilities/steady.md is a guarantees capability
    And i1's work-item w1 is ready, accepting steady#r1 and steady#r2
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And every worker gives DONE, the implementer running `python3 -m pytest -q`
    When the person runs `work run i1`
    Then the implementer's `python3 -m pytest -q` was not refused, and deselected "it waits" without running it

  @r65
  Scenario: a worker's pytest run for a work-item every requirement of which is of a guarantees capability, left with no test, exits successfully
    Pins that having no test to run is no failure for a work-item no scenario can show.
    Given spec/capabilities/steady.md is a guarantees capability
    And i1's work-item w1 is ready, accepting steady#r1
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails, and the repository holds no other test
    And every worker gives DONE, the implementer running `python3 -m pytest -q`
    When the person runs `work run i1`
    Then the implementer's `python3 -m pytest -q` exited successfully

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

  @r94
  Scenario: an initiative with no work-item gets no branch review, though its branch holds a commit no kept branch review has read
    Pins that a branch review waits for an initiative to have work-items, whatever its branch holds.
    Given i1 is started, its capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?" and no answer, and i1 has no work-item
    And the initiative branch holds a commit of notes.txt that no kept branch review has read
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
  Scenario: a planner's result with a `fileset` writes that file set into the work-item as it makes the transition to planned
    Pins that the planner's file set is the work-item's from planned on, whatever outcome the planner's result gives.
    Given i1's work-item w1 is researched, its file set scripts/thing.py
    And the planner's result gives a plan, no question and a `fileset` of scripts/thing.py and tests/test_thing.py, and every other worker gives DONE
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
    Given i1's work-item w1 is researched, its file with a ## Questions of "Old question?" and then an Answers section with "Old answer."
    And the planner gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then w1's ## Questions holds "Old question?" and then "Which module owns the log?", and its Answers section only "Old answer."

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
    Given i1's work-item w1 is researched
    And the planner gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then no worker was started for w1 after the planner

  @r63
  Scenario: no worker is started for a work-item whose blocked_by names a work-item that is not green
    Pins that a work-item waits for the work-items it is blocked by to be green.
    Given i1's work-items w1 is drafted, its blocked_by naming w2, and w2 is awaiting-answer
    And every worker gives DONE
    When the person runs `work run i1`
    Then no worker was started for w1

  @r63
  Scenario: a worker is started for a work-item whose blocked_by names a green work-item of another initiative
    Pins that a work-item's blocked_by is read across initiatives, so a blocker that is green in another initiative does not stop its work-item.
    Given i1's work-item w1 is drafted, its blocked_by naming w2
    And an initiative i2 under .shop/work/ whose work-item w2 is green
    And every worker gives DONE
    When the person runs `work run i1`
    Then a worker was started for w1

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

  @r122
  Scenario Outline: when the whole suite is run <run>, a failing scenario whose requirement a capability-proposal that is <status> adds or changes is counted as <counted>
    Pins that every whole-suite run for a work-item expects the failures of requirements a capability-proposal has yet to formulate, and not those of one formulated or withdrawn.
    Given i1's work-item w1 is ready, accepting thing#r1
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And i1's capability-proposal p1 is <status>, <naming>
    And every worker gives DONE, the implementer committing feature.txt
    When the person runs `work run i1`
    Then the whole suite `work run` ran <run> counted "it waits" as <counted>

    Examples:
      | run                                                          | status          | naming                      | counted      |
      | in the implementer's worktree before the implementer started | drafted         | its adds naming thing#r2    | expected     |
      | in the implementer's worktree before the implementer started | approved        | its changes naming thing#r2 | expected     |
      | in the implementer's worktree before the implementer started | formulated      | its adds naming thing#r2    | not expected |
      | in the implementer's worktree before the implementer started | withdrawn       | its changes naming thing#r2 | not expected |
      | in the implementer's worktree before the implementer started | drafted         | its adds naming thing#r3    | not expected |
      | before w1's merge                                            | awaiting-answer | its adds naming thing#r2    | expected     |
      | before w1's merge                                            | merged          | its changes naming thing#r2 | expected     |
      | before w1's merge                                            | formulated      | its changes naming thing#r2 | not expected |
      | before w1's merge                                            | withdrawn       | its adds naming thing#r2    | not expected |
      | before w1's merge                                            | approved        | its changes naming thing#r3 | not expected |

  @r44
  Scenario: each worker's brief tells it to write its result file first with the outcome PARTIAL, and keep it current as it works
    Pins that a worker that stops part-way still leaves a result for `work run` to read, and one that does not claim the work done.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four briefs tells the worker to write its result file first, with the outcome PARTIAL, and keep it current as it works

  @r45
  Scenario Outline: a worker whose session <ending> makes the work-item's transition to failed, recording how the session ended
    Pins that a session cut short is a fault of its work-item, and the person learns how the session ended.
    Given i1's work-item w1 is drafted
    And the researcher's session <ending>
    When the person runs `work run i1`
    Then w1 is failed, recording that the researcher's session <ended>

    Examples:
      | ending                                  | ended                                 |
      | ends in an error                        | ended in an error                     |
      | ends at its turn limit                  | ended at its turn limit               |
      | exits with an error                     | exited with an error                  |
      | leaves output that holds no JSON result | left output that holds no JSON result |

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

  @r111
  Scenario: an initiative that a work-item's transition leaves able to be done is set done before `work run` ends
    Pins that a transition made during a delivery is followed by the transitions it makes possible, even of another node, rather than leaving them to the next `work run`.
    Given i1 is started and its work-item w1 is ready
    And a request q2 kept in this context, whose asker is this context, that names i1 and is delivered
    And every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record
    When the person runs `work run i1`
    Then w1 is green
    And i1's transition to done was made after w1's transition to green, before `work run` exited

  @r128
  Scenario Outline: the <session> for <node> that <ending> is recorded and printed as a fault of <node>, whatever its result says
    Pins that a session cut short, or leaving nothing `work run` can read, is a fault of the node it was started for, of every kind of node, even when its result file claims its stage's output.
    Given <setup>
    And <session ending>, and every other session gives DONE
    When the person runs `work run i1`
    Then `work run` recorded a fault of <node>: that the <session> <ended>
    And `work run` prints <node> with the fault that the <session> <ended>

    Examples:
      | session           | node | setup                                                                                                                                                                                                                            | ending                 | session ending                                                                                                                | ended                              |
      | researcher        | w1   | i1's work-item w1 is drafted                                                                                                                                                                                                     | ends at its turn limit | the researcher's session ends at its turn limit, its result file giving a file set of scripts/thing.py and no question        | ended at its turn limit            |
      | gate round        | p1   | i1's capability-proposal p1 is drafted                                                                                                                                                                                           | ends in an error       | the gate round for p1 ends in an error, its result giving the question "Is a title given twice one book or two?"              | ended in an error                  |
      | apply round       | p1   | i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book."                                       | leaves no result       | the apply round for p1 ends with no error and before its turn limit, having written no result file                            | left no result `work run` can read |
      | integrate round   | i1   | i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose line 1 has the line outcome accepted                                                                                         | ends at its turn limit | the integrate round for i1 ends at its turn limit, its result giving a change list that adds thing#r4 on thing                | ended at its turn limit            |
      | answering session | w1   | i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", and i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer | ends in an error | the session answering w1's question "Which module owns the log?" under the delegation ends in an error, its result file answering "The queue module." | ended in an error |

  @r129
  Scenario Outline: the questions a <who>'s result gives go <where>, and <node> makes its transition from <from> to <to>
    Pins where a stage's questions are sent: a researcher's reach the planner and its work-item moves on to researched, every other stage's reach the person under the node's ## Questions and the node waits on the answers.
    Given <setup>
    And <gives>, and every other session gives DONE
    When the person runs `work run i1`
    Then <sent>
    And <node>'s transition from <from> to <to> was made once the <who> had ended

    Examples:
      | who                   | where                    | node | setup                                                                                                                                                                                                                    | gives                                                                                                                                                       | sent                                                                                                                       | from       | to              |
      | researcher's session  | into the planner's brief | w1   | i1's work-item w1 is drafted                                                                                                                                                                                             | the researcher's result gives a file set of scripts/thing.py and the questions "Is a title given twice one book or two?" and "Is the old reader kept?"     | the planner's brief has the researcher's questions "Is a title given twice one book or two?" and "Is the old reader kept?" | drafted    | researched      |
      | planner's session     | under w1's ## Questions  | w1   | i1's work-item w1 is researched                                                                                                                                                                                          | the planner's result gives a plan, a file set of scripts/thing.py and the questions "Which module owns the log?" and "Is the old reader kept?"              | w1's ## Questions holds "Which module owns the log?" and "Is the old reader kept?"                                         | researched | awaiting-answer |
      | implementer's session | under w1's ## Questions  | w1   | i1's work-item w1 is ready                                                                                                                                                                                               | the implementer's result gives commits of feature.txt on which w1's scenarios and the whole suite pass, and the question "Which module owns the log?"        | w1's ## Questions holds "Which module owns the log?"                                                                       | claimed    | awaiting-answer |
      | reviewer's session    | under w1's ## Questions  | w1   | i1's work-item w1 is done                                                                                                                                                                                                | the reviewer's result gives its findings and the question "Is the old reader kept?"                                                                         | w1's ## Questions holds "Is the old reader kept?"                                                                          | done       | awaiting-answer |
      | formulate round       | under p1's ## Questions  | p1   | i1's capability-proposal p1 is awaiting-answer, its adds naming thing#r4, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book." | the apply round for p1 ends, and the formulate round's result gives a scenario for thing#r4 and the questions "Are returns counted?" and "Is a loan one book or many?" | p1's ## Questions holds "Are returns counted?" and "Is a loan one book or many?"                                           | approved   | awaiting-answer |

  @r130
  Scenario Outline: a <who> whose result gives no question and its stage's output makes the work-item's transition from <from> to <next>
    Pins that a session which delivered its stage's output, and asked nothing, moves its node on to its next status.
    Given i1's work-item w1 is <status>
    And the <who>'s result gives no question and <output>, and every other worker gives DONE
    When the person runs `work run i1`
    Then w1's transition from <from> to <next> was made once the <who>'s session had ended

    Examples:
      | who         | status     | output                                                                  | from       | next       |
      | researcher  | drafted    | a file set of scripts/thing.py                                          | drafted    | researched |
      | planner     | researched | a plan and a file set of scripts/thing.py                               | researched | planned    |
      | implementer | ready      | commits of feature.txt on which w1's scenarios and the whole suite pass | claimed    | done       |
      | reviewer    | done       | its findings                                                            | done       | green      |

  @r131
  Scenario Outline: a <who> whose result gives neither a question nor <missing> puts a question naming it under <node>'s ## Questions and makes <node> awaiting-answer
    Pins that a session which delivered nothing of its stage reaches the person as a question saying what is missing, rather than moving its node on or stopping it as a fault.
    Given <setup>
    And the <who>'s result gives no question and <gives>, and every other session gives DONE
    When the person runs `work run i1`
    Then <node>'s ## Questions holds a question naming <missing> as missing
    And <node> is awaiting-answer

    Examples:
      | who             | node | setup                                                                                                                                                                                                                                                                         | gives                                               | missing                                                  |
      | researcher      | w1   | i1's work-item w1 is drafted                                                                                                                                                                                                                                                  | no file set                                         | the researcher's file set                                |
      | planner         | w1   | i1's work-item w1 is researched                                                                                                                                                                                                                                               | a file set of scripts/thing.py and no plan          | the planner's plan                                       |
      | implementer     | w1   | i1's work-item w1 is ready                                                                                                                                                                                                                                                    | commits of feature.txt on which w1's scenarios fail | commits on which w1's scenarios and the whole suite pass |
      | reviewer        | w1   | i1's work-item w1 is done                                                                                                                                                                                                                                                     | no findings                                         | the reviewer's findings                                  |
      | formulate round | p1   | i1's capability-proposal p1 is awaiting-answer, its adds naming thing#r4, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book.", and the apply round for p1 ends with a change list that adds thing#r4 on thing | no scenario for thing#r4                            | the formulate round's scenario for thing#r4              |

  @r132
  Scenario Outline: a <stage>'s result giving <output> is taken as its stage's output
    Pins what each stage must deliver for `work run` to take its work as done: with it the node goes on, and no question asks for a missing output.
    Given <setup>
    And the <stage>'s result gives <output>, and every other session gives DONE
    When the person runs <run>
    Then `work run` wrote no question naming a missing output
    And <after>

    Examples:
      | stage             | setup                                                                                                                                                                                                                                                                                         | output                                                                                     | run           | after                                                                                       |
      | researcher        | i1's work-item w1 is drafted                                                                                                                                                                                                                                                                  | a file set of scripts/thing.py and no question                                             | `work run i1` | w1's transition to researched was made once the researcher's session had ended              |
      | planner           | i1's work-item w1 is researched                                                                                                                                                                                                                                                               | a plan, a file set of scripts/thing.py and no question                                     | `work run i1` | w1's transition to planned was made once the planner's session had ended                    |
      | implementer       | i1's work-item w1 is ready                                                                                                                                                                                                                                                                    | commits of feature.txt on which w1's scenarios and the whole suite pass, and no question   | `work run i1` | w1's transition to done was made once the implementer's session had ended                   |
      | reviewer          | i1's work-item w1 is done                                                                                                                                                                                                                                                                     | its findings and no question                                                               | `work run i1` | w1's transition to green was made once the reviewer's session had ended                     |
      | answering session | i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", and i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer                                       | the answer "The queue module." and no question                                             | `work run i1` | w1's answer to "Which module owns the log?" is "The queue module."                          |
      | integrate round   | i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted                                                                                                                                                                                                         | a change list that adds thing#r4 on thing, and no question                                 | `work run i1` | i1 has a drafted capability-proposal for thing, its adds naming thing#r4                    |
      | apply round       | i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book."                                                                                                     | a change list that adds thing#r4 on thing, and no question                                 | `work run i1` | p1's transition to approved was made once the apply round had ended                         |
      | formulate round   | i1's capability-proposal p1 is awaiting-answer, its adds naming thing#r4, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."                                                                           | a scenario for thing#r4 and no question                                                    | `work run i1` | p1's transition to formulated was made once the formulate round had ended                   |
      | formulate round   | spec/capabilities/steady.md is a guarantees capability, and i1's capability-proposal p1 is awaiting-answer, its adds naming steady#r4, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."             | no scenario and no question                                                                | `work run i1` | p1's transition to formulated was made once the formulate round had ended                   |
      | intake round      | a request q1 of which this context is the upstream, open, its turn the upstream's, with two lines                                                                                                                                                                                             | a line outcome on q1's line 1 and the question "Which unit is the limit in?" on its line 2 | `work run`    | q1's line 1 has that line outcome and its line 2 the question "Which unit is the limit in?" |
      | gate round        | i1's capability-proposal p1 is drafted                                                                                                                                                                                                                                                        | the question "Is a title given twice one book or two?"                                     | `work run i1` | p1's ## Questions holds "Is a title given twice one book or two?"                           |

  @r133
  Scenario: a researcher whose result gives the outcome BLOCKED with its file set and no question is moved on by its output, not stopped by its outcome
    Pins that the one word a result gives decides no transition: the work-item goes where its output and its questions take it.
    Given i1's work-item w1 is drafted
    And the researcher's result gives the outcome BLOCKED, a file set of scripts/thing.py and no question, and every other worker gives DONE
    When the person runs `work run i1`
    Then w1's transition from drafted to researched was made once the researcher's session had ended
    And w1 made no transition to awaiting-answer

  @r134
  Scenario: when an intake round gives a question, the request's status stays as `work turn` set it
    Pins that the request's status after its intake is the one passing the turn wrote, and `work run` sets no status of its own over it because the round asked something.
    Given a request q1 of which this context is the upstream, open, its turn the upstream's, with two lines
    And the intake round writes a line outcome for q1's line 1, gives the question "Which unit is the limit in?" on q1's line 2 and passes the turn with `work turn`
    When the person runs `work run`
    Then q1 is awaiting-asker, as `work turn` set it when the round passed the turn
    And `work run` made no change to q1's status after the round had ended

  @r95
  Scenario: `work run` started with no initiative runs the integrate, apply and formulate rounds of different initiatives one at a time
    Pins that rounds of these kinds never run side by side across initiatives, whether they are of one kind or of different kinds.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And an initiative i2 under .shop/work/ whose capability-proposal p2 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", and its Answers section with "One book."
    And an initiative i3 under .shop/work/ whose capability-proposal p3 is awaiting-answer, its ## Questions section with "Is the old reader kept?", and its Answers section with "No."
    And every round ends, each round of the kind integrate, apply or formulate ending only after long enough for another round to start beside it
    When the person runs `work run`
    Then a round of the kind integrate was started for i1, and a round of the kind apply for each of p2 and p3
    And no round of the kind integrate, apply or formulate was started before every other round of those kinds had ended

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

  @r100
  Scenario: a question an intake round gives on a line of a request is written in the request
    Pins that a question the upstream raises on a line reaches the request, where the asker reads it, without anyone copying it there by hand.
    Given a request q1 of which this context is the upstream, open, its turn the upstream's, with two lines
    And the intake round writes a line outcome for q1's line 1, gives the question "Which unit is the limit in?" on q1's line 2 and passes the turn with `work turn`
    When the person runs `work run`
    Then q1 holds the question "Which unit is the limit in?" on its line 2

  @r79
  Scenario: a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils
    Pins that the round integrating an initiative works from the lines its upstream accepted, and from no other line of the request.
    Given i1 is proposed and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for i1, given q1's lines 1 and 3, and not line 2

  @r79
  Scenario: a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind
    Pins that only an initiative with a request's accepted lines to work from is integrated, and that one with none blocks no later `work run`.
    Given i1 is proposed and fulfils no request
    And every round ends
    When the person runs `work run i1`
    Then no round of the kind integrate was started for i1
    And i1 is proposed
    And no branch is made for a round
    And nothing under .shop/work/ is left uncommitted
    When the person runs `work run i1` a second time
    Then the second `work run` was not refused

  @r79
  Scenario: a proposed initiative whose fulfils names a request the queue does not hold is given no integrate round, and nothing changes
    Pins that an initiative naming a request with no lines to work from is not integrated, and that it blocks no later `work run`.
    Given i1 is proposed and fulfils the request q9, which the queue does not hold
    And every round ends
    When the person runs `work run i1`
    Then no round of the kind integrate was started for i1
    And i1 is proposed
    And no branch is made for a round
    And nothing under .shop/work/ is left uncommitted
    When the person runs `work run i1` a second time
    Then the second `work run` was not refused

  @r69
  Scenario: when the gate round `work run` started for a capability-proposal ends, the proposal is awaiting-answer
    Pins that a capability-proposal whose gate has been given waits on its answers.
    Given i1's capability-proposal p1 is drafted
    And the gate round gives the question "Is a title given twice one book or two?" on p1, and every round ends
    When the person runs `work run i1`
    Then a round of the kind gate was started for p1
    And p1 is awaiting-answer

  @r70
  Scenario: a capability-proposal whose every question has an answer is given to an apply round with its answers
    Pins that the person's answers reach the round that applies them, without anyone starting it by hand.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?" and "Is the old reader kept?", and its Answers section with "One book." and "No."
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind apply was started for p1, given the answers "One book." and "No."

  @r116
  Scenario: a capability-proposal whose every question from its formulate round has an answer is given to a formulate round with the answers
    Pins that the person's answers to a formulation's questions reach a new formulation of the proposal, without anyone starting it by hand.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."
    And every round ends and every worker gives DONE
    When the person runs `work run i1`
    Then a round of the kind formulate was started for p1, given the answer "One place."

  @r140
  Scenario: an apply round that applies nothing because the proposal's answers give what its drafts do not hold is followed by a new integrate round for the proposal
    Pins that answers asking for what the drafts never held go back to integration, without anyone starting it by hand.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And every other round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for p1 after the apply round had ended

  @r141
  Scenario: an integrate round started for a capability-proposal that has answers is given its questions and answers, the initiative's ledger and the accepted lines of the request
    Pins that a new integration of a proposal works from what the person answered, what the initiative has done so far and the lines its upstream accepted, and from no other line of the request.
    Given i1 is started and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
    And i1's ledger holds the line "integrate round 1 drafted p1"
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And every other round ends
    When the person runs `work run i1`
    Then the integrate round for p1 was given the question "Is a title given twice one book or two?" with its answer "One book, and a book's edition is listed with it."
    And it was given i1's ledger
    And it was given q1's lines 1 and 3, and not line 2

  @r142
  Scenario: a capability-proposal an integrate round drafts anew from its answers is set drafted, the earlier drafts kept where their round wrote them
    Pins that a proposal drafted again goes back through its gate, and that what the first integration drafted is not lost to the second.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, written from the change list of i1's integrate round, whose drafts are kept at .shop/work/i1/runs/i1/2-integrate/drafts/round-1/ with spec/capabilities/thing.md
    And p1's ## Questions section holds "Is a title given twice one book or two?", given by its gate round, and its Answers section "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And the integrate round for p1 writes spec/capabilities/thing.md under its drafts path and gives DONE with a change list that adds thing#r4 and thing#r6 on thing
    And every other round ends
    When the person runs `work run i1`
    Then p1's transition to drafted was made once the integrate round for p1 had ended
    And .shop/work/i1/runs/i1/2-integrate/drafts/round-1/spec/capabilities/thing.md is as the first integrate round wrote it

  @r143
  Scenario: a capability-proposal keeps its status while the integrate round started for it runs
    Pins that a proposal being drafted again shows no new status until its new drafts are there.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And every other round ends
    When the person runs `work run i1`
    Then p1 was awaiting-answer while the integrate round for p1 ran
    And no transition of p1 was made between the start and the end of the integrate round for p1

  @r144
  Scenario: when the apply round `work run` started for a capability-proposal ends having applied its drafts, the proposal is approved
    Pins that a capability-proposal whose drafts have been applied after its answers is approved.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book."
    And the apply round for p1 applies p1's drafts and gives DONE with a change list that adds thing#r4 on thing
    And every other round ends
    When the person runs `work run i1`
    Then p1's transition to approved was made once the apply round had ended

  @r145
  Scenario: when the apply round `work run` started for a capability-proposal ends having applied its drafts, the proposal's adds, changes and removes are written from the change list the round applied
    Pins that the proposal names what was applied after the answers, not what was drafted before them.
    Given i1's capability-proposal p1 is awaiting-answer, its adds naming thing#r4 and thing#r5, its ## Questions section with "Is thing#r5 kept?", given by its gate round, and its Answers section with "No."
    And the apply round for p1 applies p1's drafts and gives DONE with a change list that adds thing#r4 and changes thing#r2 on thing
    And every other round ends and every worker gives DONE
    When the person runs `work run i1`
    Then p1's adds name thing#r4 and not thing#r5, its changes name thing#r2, and its removes name nothing

  @r146
  Scenario: when the apply round `work run` started for a capability-proposal ends having applied its drafts, a formulate round is started for the proposal
    Pins that applied lines go on to be formulated, without anyone starting the round by hand.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book."
    And the apply round for p1 applies p1's drafts and gives DONE with a change list that adds thing#r4 on thing
    And every other round ends
    When the person runs `work run i1`
    Then a round of the kind formulate was started for p1 after the apply round had ended

  @r147
  Scenario: an apply round that applies nothing because the proposal's answers give what its drafts do not hold has given its output
    Pins that an apply round sending the proposal back to integration is not taken as one that left its output out, so the person is asked nothing about a missing change list.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold, and no change list
    And every other round ends
    When the person runs `work run i1`
    Then no question naming the apply round's output as missing was written under p1's ## Questions

  @r148
  Scenario: a capability-proposal an integrate round drafts anew from its answers is the only capability-proposal of the initiative for its capability
    Pins that drafting a proposal again rewrites that proposal and never brings a second one for the same capability beside it.
    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    And i1's capability-proposal p1, for thing, is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    And the integrate round for p1 gives DONE with a change list that adds thing#r4 and thing#r6 on thing
    And every other round ends
    When the person runs `work run i1`
    Then i1 has one capability-proposal for thing, and it is p1

  @r72
  Scenario: a formulated capability-proposal gets one work-item for each capability it adds or changes, accepting every requirement it names on that capability
    Pins that the work-items of a formulated proposal are drafted one a capability, whichever of adds and changes names the requirement.
    Given i1's capability-proposal p1 is formulated, its adds naming thing#r1 and thing#r2, and its changes naming thing#r3 and other#r4
    And every worker gives DONE
    When the person runs `work run i1`
    Then `work add` drafted two work-items in i1, each part of p1: one under thing accepting thing#r1, thing#r2 and thing#r3, and one under other accepting other#r4

  @r136
  Scenario: a formulated capability-proposal whose integrate round raised the lines of a request into an upstream gets no work-item while that request is not delivered
    Pins that work waiting on an upstream does not begin before the upstream delivers it, and that only the proposal those lines came with waits, not the initiative's other proposals.
    Given i1 is started and fulfils the request q1, and i1's capability-proposal p1 is formulated, its adds naming thing#r1, and i1's capability-proposal p2 is formulated, its adds naming other#r4
    And p1 was written by an integrate round that gave the lines of a request into the upstream catalogue: "When a book is listed, the catalogue shall give its edition.", and p2 by an integrate round that gave no lines into an upstream
    And the request q2 in catalogue, with the line "When a book is listed, the catalogue shall give its edition." as its one line, is raised by i1 for q1 and is awaiting-upstream
    And every worker gives DONE
    When the person runs `work run i1`
    Then `work add` drafted no work-item part of p1
    And `work add` drafted one work-item in i1, part of p2: under other accepting other#r4

  @r73
  Scenario: a work-item lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement it accepts
    Pins that a deprecated scenario is retired by the work-item that accepts its replacement's requirement, not by the one that accepts the requirement it was tagged with.
    Given i1's capability-proposal p1 is formulated, its changes naming thing#r2
    And features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it answers", tagged @r5
    And features/thing.feature has the scenario "it used to wait", tagged @deprecated and @r9, deprecated for "it waits"
    And features/thing.feature has the scenario "it used to answer", tagged @deprecated and @r2, deprecated for "it answers"
    And every worker gives DONE
    When the person runs `work run i1`
    Then the work-item drafted for p1 under thing lists "it used to wait" under its ## Retires, and neither "it used to answer", "it waits" nor "it answers"

  @r73
  Scenario: a work-item that accepts a range lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement in the range
    Pins that a range of requirements is read as each requirement in it when the deprecated scenarios a work-item retires are found through their replacements.
    Given i1's capability-proposal p1 is formulated, its changes naming thing#r3-r6
    And features/thing.feature has the scenario "it waits", tagged @r4, and the scenario "it answers", tagged @r8
    And features/thing.feature has the scenario "it used to wait", tagged @deprecated and @r9, deprecated for "it waits"
    And features/thing.feature has the scenario "it used to answer", tagged @deprecated and @r4, deprecated for "it answers"
    And every worker gives DONE
    When the person runs `work run i1`
    Then the work-item drafted for p1 under thing lists "it used to wait" under its ## Retires, and neither "it used to answer", "it waits" nor "it answers"

  @r123
  Scenario: when every work-item is green or withdrawn, one work-item is drafted retiring each deprecated scenario whose replacement's work-item is green
    Pins that deprecated scenarios left behind once their replacements pass are retired by one work-item, under the proposal of the last-drafted work-item among those replacements', and that a scenario whose replacement is not yet green is left.
    Given i1's work-item w1 is green, part of the capability-proposal p1 and accepting thing#r2, and i1's work-item w2, drafted after w1, is green, part of the capability-proposal p2 and accepting other#r4
    And i1's work-item w3 is withdrawn
    And i2's work-item w4 is ready, accepting thing#r7
    And features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it closes", tagged @r7, and features/other.feature has the scenario "it answers", tagged @r4
    And features/thing.feature has the scenario "it used to wait", tagged @deprecated, deprecated for "it waits", and the scenario "it used to close", tagged @deprecated, deprecated for "it closes"
    And features/other.feature has the scenario "it used to answer", tagged @deprecated, deprecated for "it answers"
    And every worker gives DONE
    When the person runs `work run i1`
    Then one work-item was drafted in i1, part of p2, listing "it used to wait" and "it used to answer" under its ## Retires, and not "it used to close"

  @r124
  Scenario: the work-item retiring deprecated scenarios is drafted before the branch review starts and before measure initiative runs
    Pins that the retiring of deprecated scenarios is work of the initiative, drafted before its branch review and its measurement rather than after them.
    Given i1's work-item w1 is green, part of the capability-proposal p1 and accepting thing#r2, and w2 is withdrawn
    And features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it used to wait", tagged @deprecated, deprecated for "it waits"
    And every worker gives DONE, and the branch reviewer's result lists nothing to fix now
    When the person runs `work run i1`
    Then the work-item retiring "it used to wait" was drafted in i1 before `work run` started the branch review of i1
    And it was drafted before `work run` ran `measure initiative` on i1

  @r74
  Scenario: a kept branch review's findings to fix now get one work-item, naming the findings file, under the capability-proposal of the work-item they concern
    Pins that what the branch review says to fix now is drafted as work, under the proposal it belongs to, rather than left for the person to take up.
    Given i1's work-items w1 is green, part of the capability-proposal p1, and w2 is withdrawn
    And every worker gives DONE, and the branch reviewer's result lists two findings to fix now, both concerning w1, in its findings.md
    When the person runs `work run i1`
    Then one work-item was drafted in i1 for the two findings, part of p1, naming the kept branch review's findings.md

  @r121
  Scenario Outline: a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now
    Pins that a branch review with nothing to ask the person counts as finding nothing to fix now, however it ended, so no fix is drafted and the initiative goes on to its measurement.
    Given i1's work-items w1 is green and w2 is withdrawn
    And every worker gives DONE, and the branch reviewer's result gives <outcome>, with no question
    When the person runs `work run i1`
    Then no work-item was drafted in i1 for the kept branch review
    And `work run` ran `measure initiative` on i1 after the branch review was kept

    Examples:
      | outcome       |
      | DONE          |
      | PARTIAL       |
      | BLOCKED       |
      | NEEDS_CONTEXT |

  @r75
  Scenario Outline: an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured>
    Pins that an initiative is measured once its work is done and at least one work-item delivered something, and not when every work-item was withdrawn.
    Given i1's work-items <work-items>
    And every worker gives DONE, and the branch reviewer's result lists nothing to fix now
    When the person runs `work run i1`
    Then `work run` <ran> on i1 after the branch review was kept

    Examples:
      | work-items                          | measured        | ran                         |
      | w1 is green and w2 is withdrawn     | is measured     | ran `measure initiative`    |
      | w1 is withdrawn and w2 is withdrawn | is not measured | ran no `measure initiative` |

  @r97
  Scenario: an initiative with no work-item is not measured
    Pins that an initiative whose work-items are all green or withdrawn only because it has none is not taken for one whose work is done.
    Given i1 is started, its capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?" and no answer, and i1 has no work-item
    When the person runs `work run i1`
    Then `work run` ran no `measure initiative` on i1

  @r98
  Scenario: an implementer started for a work-item that an answer to its reviewer's question returned to ready is given the reviewer's findings and the answer
    Pins that the implementer who takes up a work-item again after its review knows what the reviewer found and what the person answered, without anyone passing either on by hand.
    Given i1's work-item w1 was awaiting-answer on its reviewer's question "Is the old reader kept?", the reviewer having written findings.md beside its brief
    And the answer "No." to "Is the old reader kept?" returned w1 to ready
    And every worker gives DONE
    When the person runs `work run i1`
    Then the implementer of w1 was given the reviewer's findings.md, and the question "Is the old reader kept?" with the answer "No."

  @r76
  Scenario: once `measure initiative` has written the initiative's measurement, a session of analyzing-a-batch writes its analysis record
    Pins that a measured initiative is analysed without anyone starting the analysis by hand.
    Given i1's work-items w1 is green and w2 is withdrawn
    And every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record
    When the person runs `work run i1`
    Then a session of analyzing-a-batch was started for i1 once `measure initiative` had written i1's measurement
    And i1's analysis record is there


  @r76
  Scenario: an analyzing-a-batch session that ends at its turn limit leaves no analysis record of the initiative, even though it wrote an analysis file
    Pins that an analysis cut short is not kept as the initiative's analysis record.
    Given i1's work-items w1 is green and w2 is withdrawn
    And every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes an analysis file of i1 and ends at its turn limit
    When the person runs `work run i1`
    Then a session of analyzing-a-batch was started for i1 once `measure initiative` had written i1's measurement
    And i1's analysis record is not there
  @r77
  Scenario Outline: under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply>
    Pins that a question is weighed against the person's words alone, apart from every other question, and answered only when those words cover it.
    Given i1 fulfils the request q1, which gives the delegation "<delegation>"
    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py or scripts/queue.py own the log?" and no answer
    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice in features/books.feature one book or two?" and no answer
    And each session given a question under the delegation <reply>, and every round ends and every worker gives DONE
    When the person runs `work run i1`
    Then w1's question was given to a session of its own, given the question, the delegation "<delegation>", scripts/log.py and scripts/queue.py, and nothing else
    And p1's question was given to a session of its own, given the question, the delegation "<delegation>", features/books.feature, and nothing else
    And <after>

    Examples:
      | delegation                                                                       | reply                                   | after                                                                     |
      | Please get everything delivered. Do not stop to ask me questions or permission. | answers it                              | w1's question and p1's question each have the session's answer            |
      | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person                | w1's question and p1's question have no answer, w1 and p1 awaiting-answer |

  @r77
  Scenario: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends
    Pins that two questions of one work-item are answered apart, in one `work run`, and that the run keeps every answer its sessions gave instead of losing one to the other.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and "Is a title given twice in features/books.feature one book or two?", each with no answer
    And the session given "Does scripts/log.py own the log?" under the delegation answers "Yes.", the session given "Is a title given twice in features/books.feature one book or two?" answers "One book.", and every round ends and every worker gives DONE
    When the person runs `work run i1`
    Then "Does scripts/log.py own the log?" was given to a session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", scripts/log.py, and nothing else
    And "Is a title given twice in features/books.feature one book or two?" was given to another session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", features/books.feature, and nothing else
    And w1's answer to "Does scripts/log.py own the log?" is "Yes.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And w1's answer to "Is a title given twice in features/books.feature one book or two?" is "One book.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And it exits successfully

  @r78
  Scenario: an answer given by a session started under a delegation is written naming that delegation
    Pins that the person can tell an answer given in their place from one they gave, and under which words of theirs it was given.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer
    And the session answering under the delegation answers "The queue module.", and every worker gives DONE
    When the person runs `work run i1`
    Then w1's answer to "Which module owns the log?" is "The queue module.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."

  @r66
  Scenario: `work run` started with no initiative takes every initiative that is neither done nor abandoned through its transitions, the initiatives side by side and one session of an initiative at a time
    Pins which initiatives a `work run` with no initiative takes, that they do not wait on each other, and that the sessions of one initiative do.
    Given i1's capability-proposal p1 is drafted and i1's work-item w1 is drafted
    And an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted
    And an initiative i3 under .shop/work/ that is done and an initiative i4 under .shop/work/ that is abandoned, each with a work-item that is drafted
    And every round ends and every worker gives DONE, the gate rounds of p1 and p2 each ending once both have started
    When the person runs `work run`
    Then the gate rounds of p1 and p2 ran at the same time
    And no two sessions of i1 ran at the same time
    And no session was started for i3 or i4
    And w1 is green, and p1 and p2 are awaiting-answer

  @r89
  Scenario Outline: when a session started under a delegation to answer a question <ending>, the question is left unanswered for the person
    Pins that an answering session cut short gives no answer in the person's place, even when its result file holds one.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer
    And the session answering under the delegation <ending>, and every worker gives DONE
    When the person runs `work run i1`
    Then w1's question "Which module owns the log?" has no answer
    And w1 is awaiting-answer

    Examples:
      | ending                                                                      |
      | ends in an error, its result file answering "The queue module."             |
      | ends at its turn limit, its result file answering "The queue module."       |
      | ends with no error and before its turn limit, having written no result file |

  @r90
  Scenario Outline: when a session started under a delegation to answer a question <ending>, its stage directory and log lines are committed
    Pins that what an answering session left behind is kept in the initiative's history for the person, though it answered nothing.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer
    And the session answering under the delegation writes notes.md beside its brief and <ending>
    When the person runs `work run i1`
    Then the initiative branch has a commit of the answering session's stage directory, its notes.md included, and of log.jsonl's lines for that session
    And nothing of that stage directory or of log.jsonl is left uncommitted

    Examples:
      | ending                                                               |
      | ends in an error                                                     |
      | ends at its turn limit                                               |
      | ends with no error and before its turn limit, writing no result file |

  @r93
  Scenario: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils
    Pins that an initiative whose integration left nothing behind is integrated again, from the lines its upstream accepted and no other.
    Given i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for i1, given q1's lines 1 and 3, and not line 2

  @r96
  Scenario: an integrate round that ends DONE without a change list ends `work run` with an error naming the round
    Pins that an integration that names no capability to change is reported to the person, even when the round says its work is done.
    Given i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose line 1 has the line outcome accepted
    And the integrate round for i1 gives DONE with no change list
    When the person runs `work run i1`
    Then `work run` names the integrate round of i1
    And it exits with an error

  @r84
  Scenario: when `work run` starts the integrate round of a proposed initiative, the initiative is started
    Pins that an initiative whose integration has begun is no longer proposed.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And every round ends
    When the person runs `work run i1`
    Then i1's transition to started was made when the integrate round for i1 was started

  @r84
  Scenario: when the integrate round `work run` started for a proposed initiative ends DONE, the initiative is started and work run leaves nothing uncommitted
    Pins that the round's stage directory is committed with the initiative's change to started, so a later `work run` finds nothing under .shop/work/ to refuse on.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And the integrate round for i1 gives DONE, and every round ends
    When the person runs `work run i1`
    Then i1's transition to started was made when the integrate round for i1 was started
    And the initiative branch has a commit of the integrate round's stage directory with i1's change to started
    And nothing under .shop/work/ is left uncommitted
    When the person runs `work run i1` a second time
    Then the second `work run` was not refused

  @r91
  Scenario Outline: the drafts of an integrate round that <ending> are kept on the initiative branch
    Pins that what an integrate round drafted is in the initiative's history once the round is over, however it ended.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And the integrate round for i1 writes spec/capabilities/thing.md under its drafts path and <ending>
    And every other round ends
    When the person runs `work run i1`
    Then the initiative branch has a commit of the integrate round's drafts, its spec/capabilities/thing.md as the round wrote it

    Examples:
      | ending                                |
      | gives DONE with a change list naming thing |
      | ends at its turn limit                |

  @r92
  Scenario: an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability
    Pins that the change list is split by capability, each proposal holding that capability's requirement ids and terms and nothing of another's.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And the integrate round for i1 gives DONE with a change list that adds thing#r4 and the term "ledger", changes thing#r2 and removes thing#r3 on thing, and adds other#r1 on other
    And every other round ends
    When the person runs `work run i1`
    Then the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3, and one for other, its adds naming other#r1 and its changes and removes naming nothing

  @r92
  Scenario: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids
    Pins that two initiatives changing one capability each get a capability-proposal of their own, never two proposals sharing one id.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And an initiative i2 under .shop/work/, proposed, that fulfils the request q2, whose line 1 has the line outcome accepted
    And the integrate round for i1 gives DONE with a change list that adds thing#r4 on thing, and the integrate round for i2 gives DONE with a change list that adds thing#r5 on thing
    And every other round ends
    When the person runs `work run`
    Then i1 has one drafted capability-proposal for thing, its adds naming thing#r4, and i2 has one drafted capability-proposal for thing, its adds naming thing#r5
    And the two capability-proposals have different ids

  @r135
  Scenario: the lines an integrate round gives into an upstream are raised with `work request`, raised for the request the initiative fulfils and with its delegation
    Pins that what an integration needs from an upstream reaches that upstream as a request tied to the request it serves and answerable under the same delegation.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted, and which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And the integrate round for i1 gives DONE with a change list that adds thing#r4 on thing, and gives the lines of a request into the upstream catalogue: "When a book is listed, the catalogue shall give its edition."
    And every other round ends
    When the person runs `work run i1`
    Then `work request` was run for the upstream catalogue, with the line "When a book is listed, the catalogue shall give its edition." as its one line
    And the request it wrote in catalogue is raised for q1 and gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."

  @r68
  Scenario: a drafted capability-proposal is given to a gate round whose brief asks for the gate as questions, each a decision with its readings and the recommended reading marked
    Pins that the gate comes back as decisions the person can answer one by one, with the reading to take already marked.
    Given i1's capability-proposal p1 is drafted
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind gate was started for p1
    And the gate round's brief asks for the gate as questions, each a decision with its readings and the recommended reading marked

  @r85
  Scenario: when the gate round `work run` started for a capability-proposal ends, the questions its result gives are written under the proposal's ## Questions
    Pins that the gate a round gives reaches the proposal, where the person answers it, though the round writes nothing on the proposal itself.
    Given i1's capability-proposal p1 is drafted
    And the gate round's result gives the question "Is a title given twice one book or two?", with the readings "One book." and "Two books.", "One book." marked recommended, and every round ends
    When the person runs `work run i1`
    Then p1's ## Questions holds "Is a title given twice one book or two?", with the readings "One book." and "Two books.", "One book." marked recommended

  @r83
  Scenario: when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated
    Pins that a capability-proposal whose lines have been formulated with nothing left to ask is formulated.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."
    And the formulate round for p1 gives DONE with no question
    And every worker gives DONE
    When the person runs `work run i1`
    Then p1's transition to formulated was made once the formulate round had ended

  @r112 @deprecated
  Scenario: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions (deprecated)
    Deprecated for: removal
    Pins that what a formulation could not decide reaches the proposal, where the person answers it.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."
    And the formulate round for p1 gives DONE with the questions "Are returns counted?" and "Is a loan one book or many?"
    When the person runs `work run i1`
    Then p1's ## Questions holds "Are returns counted?" and "Is a loan one book or many?"

  @r113 @deprecated
  Scenario: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer (deprecated)
    Deprecated for: removal
    Pins that a capability-proposal whose formulation asked a question waits on its answer instead of going on to be formulated.
    Given i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book."
    And the apply round for p1 ends, and the formulate round for p1 gives DONE with the question "Are returns counted?"
    When the person runs `work run i1`
    Then p1's transition from approved to awaiting-answer was made once the formulate round had ended
    And p1 is awaiting-answer

  @r86
  Scenario: when a round `work run` started for a capability-proposal ends at its turn limit, the proposal keeps its status
    Pins that a round cut short leaves the proposal where it stood, rather than moving it on as if the round's work were done.
    Given i1's capability-proposal p1 is drafted
    And the gate round's session ends at its turn limit, its result giving the question "Is a title given twice one book or two?" on p1
    When the person runs `work run i1`
    Then a round of the kind gate was started for p1
    And p1 is drafted

  @r87
  Scenario Outline: the <kind> round of <node> that <ending> brings no transition
    Pins that a round cut short moves no node on, whatever it wrote before it stopped.
    Given <setup>
    And the <kind> round for <node> <ending>
    When the person runs `work run i1`
    Then a round of the kind <kind> was started for <node>
    And no transition of any node was made from the <kind> round

    Examples:
      | kind      | node | setup                                                                                                                                                                                       | ending                                                                                     |
      | gate      | p1   | i1's capability-proposal p1 is drafted                                                                                                                                                      | ends in an error, its result giving the question "Is a title given twice one book or two?" |
      | apply     | p1   | i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book." | ends at its turn limit, its result giving a change list that adds thing#r4 on thing        |
      | integrate | i1   | i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose line 1 has the line outcome accepted                                                    | ends with no error and before its turn limit, having written no result file                |

  @r88
  Scenario Outline: the <kind> round of <node> that <ending> ends `work run` with an error naming the round and how it ended
    Pins that the person learns from `work run` itself which round stopped and how.
    Given <setup>
    And the <kind> round for <node> <ending>
    When the person runs `work run i1`
    Then `work run` names the <kind> round of <node> and that it <ended>
    And it exits with an error

    Examples:
      | kind      | node | setup                                                                                                                                                                                       | ending                                                                      | ended                              |
      | gate      | p1   | i1's capability-proposal p1 is drafted                                                                                                                                                      | ends in an error                                                            | ended in an error                  |
      | apply     | p1   | i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book." | ends at its turn limit                                                      | ended at its turn limit            |
      | integrate | i1   | i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose line 1 has the line outcome accepted                                                    | ends with no error and before its turn limit, having written no result file | left no result `work run` can read |

  @r115
  Scenario Outline: when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error
    Pins that one round stopping holds back only its own node, not the rest of the initiative's delivery.
    Given i1's capability-proposal p1 is drafted and i1's work-item w1 is drafted
    And the gate round for p1 <ending>, and every worker gives DONE
    When the person runs `work run i1`
    Then w1 is green
    And it exits with an error

    Examples:
      | ending                                                                      |
      | ends in an error                                                            |
      | ends at its turn limit                                                      |
      | ends with no error and before its turn limit, having written no result file |

  @r81
  Scenario Outline: `work run` started with no initiative, ending with <node> <status>, exits with an error, printing the status of each initiative it took
    Pins that a run over every initiative that stops on a question or a fault is an error, and what the person reads of each initiative.
    Given i1 is started, and i1's <node> is <status>
    And an initiative i2 under .shop/work/, started, none of whose nodes can make a transition and none of which is awaiting-answer or failed
    When the person runs `work run`
    Then `work run` prints i1 with started and i2 with started
    And it exits with an error

    Examples:
      | node                   | status          |
      | work-item w1           | awaiting-answer |
      | capability-proposal p1 | awaiting-answer |
      | work-item w1           | failed          |

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

  @r103
  Scenario: an accepted request this context is the upstream of, that no initiative fulfils, has its initiative started with `work start`
    Pins that an accepted request gets its initiative without anyone running `work start` by hand, and that a request an initiative already fulfils gets no second one.
    Given a request q1 of which this context is the upstream, accepted, that no initiative fulfils
    And a request q2 of which this context is the upstream, accepted, that i1 fulfils
    And every round ends and every worker gives DONE
    When the person runs `work run`
    Then `work start` was run for q1, and an initiative under .shop/work/ fulfils q1
    And `work start` was not run for q2, and i1 is the only initiative that fulfils q2

  @r102
  Scenario: an integrate round is given every requirement id another initiative's kept drafts add that spec/ on the branch it starts from does not hold, whatever that initiative's capability-proposal's status
    Pins that an integration knows the ids other initiatives have drafted and spec/ does not yet hold, however far their proposals have got, and is given no id spec/ already holds.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And spec/capabilities/thing.md on the branch i1's integrate round starts from holds thing#r1, thing#r2 and thing#r5
    And an initiative i2 under .shop/work/, started, whose capability-proposal p2 is formulated
    And i2 keeps a draft of thing adding thing#r4 and thing#r5 at .shop/work/i2/runs/i2/2-integrate/drafts/round-1/spec/capabilities/thing.md
    And an initiative i3 under .shop/work/, started, whose capability-proposal p3 is drafted
    And i3 keeps a draft of other adding other#r1 at .shop/work/i3/runs/i3/2-integrate/drafts/round-2/spec/capabilities/other.md
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind integrate was started for i1, given thing#r4 and other#r1
    And the integrate round for i1 was not given thing#r1, thing#r2 or thing#r5

  @r104
  Scenario: the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes
    Pins that the gate of one capability-proposal raises no question on what another proposal, or the rest of the capability, holds.
    Given the capability thing holds thing#r1, thing#r2 and thing#r3
    And i1's capability-proposal p1 is drafted, its adds naming thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3
    And i1's capability-proposal p2 is drafted, its adds naming other#r1
    And every round ends
    When the person runs `work run i1`
    Then the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2, thing#r3 and the term "ledger"
    And it asks for no question on thing#r1 or on other#r1

  @r107
  Scenario: a change list naming a capability that neither spec/capabilities/ nor the round's drafts have gives no capability-proposal for it, and `work run` exits with an error naming it
    Pins that a change list cannot bring a proposal for a capability that exists nowhere, and that the person learns which capability it named.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    And spec/capabilities/ holds no capability nowhere
    And the integrate round for i1 gives DONE with a change list that adds nowhere#r1 on nowhere, having written no draft of nowhere under its drafts path
    And every other round ends
    When the person runs `work run i1`
    Then i1 has no capability-proposal for nowhere
    And `work run` names the capability nowhere
    And it exits with an error

  @r108
  Scenario Outline: the <kind> round of a capability-proposal is given the path of the kept drafts of the integrate round that wrote the proposal
    Pins that the round weighing or applying a proposal reads the drafts the proposal came from, without anyone pointing it to them by hand.
    Given i1's capability-proposal p1 is <status>
    And p1 was written from the change list of i1's integrate round, whose drafts are kept at .shop/work/i1/runs/i1/2-integrate/drafts/round-1/
    And every round ends
    When the person runs `work run i1`
    Then a round of the kind <kind> was started for p1
    And the <kind> round for p1 was given the path .shop/work/i1/runs/i1/2-integrate/drafts/round-1/

    Examples:
      | kind  | status                                                                                                                   |
      | gate  | drafted                                                                                                                  |
      | apply | awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", and its Answers section with "One book." |

  @r106
  Scenario: once the initiative's measurement and analysis record are written, they are committed on the initiative branch
    Pins that what was measured and analysed of an initiative is in the initiative's history, not left uncommitted in the checkout.
    Given i1's work-items w1 is green and w2 is withdrawn
    And every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record
    When the person runs `work run i1`
    Then the initiative branch has a commit of i1's measurement and i1's analysis record
    And nothing under .shop/records/ is left uncommitted

  @r105
  Scenario Outline: an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>
    Pins that an initiative is set done only when at least one of its work-items is green, even with its branch review, measurement, analysis record and requests closed.
    Given i1 is started and its work-items <work-items>
    And i1's kept branch review lists nothing to fix now, and i1's measurement and analysis record are committed on the initiative branch
    And a request q2 kept in this context, whose asker is this context, that names i1 and is delivered
    And every worker gives DONE
    When the person runs `work run i1`
    Then i1 <status>

    Examples:
      | work-items                          | set             | status      |
      | w1 is green and w2 is withdrawn     | is set done     | is done     |
      | w1 is withdrawn and w2 is withdrawn | is not set done | is not done |

  @r109
  Scenario: an initiative set done is committed on the initiative branch
    Pins that the initiative's being done is in its history, not only in the checkout.
    Given i1 is started and its work-items w1 is green and w2 is withdrawn
    And a request q2 kept in this context, whose asker is this context, that names i1 and is delivered
    And every worker gives DONE, the branch reviewer's result lists nothing to fix now, and the analyzing-a-batch session writes i1's analysis record
    When the person runs `work run i1`
    Then the initiative branch has a commit of i1 with its status done
    And i1's file is not left uncommitted

  @r117
  Scenario: when the gate round `work run` started for a capability-proposal gives no question, one question asking for the approval of the proposal's lines as drafted is written under its ## Questions
    Pins that a gate with nothing to decide still reaches the person as a question to answer, so the proposal's lines are not taken as approved unasked.
    Given i1's capability-proposal p1 is drafted
    And the gate round's result gives no question, and every round ends
    When the person runs `work run i1`
    Then a round of the kind gate was started for p1
    And p1's ## Questions holds one question, asking for the approval of p1's lines as drafted

  @r110
  Scenario: when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits
    Pins that fixing what a branch review found brings a new branch review in the same delivery, rather than leaving the fix unreviewed until the next `work run`.
    Given i1's work-items w1 is green, part of the capability-proposal p1, and w2 is withdrawn
    And every worker gives DONE, the first branch reviewer's result lists two findings to fix now, both concerning w1, in its findings.md, and the second lists nothing to fix now
    When the person runs `work run i1`
    Then one work-item was drafted in i1 for the two findings, and it is green
    And after that work-item turned green a second session of bdd-branch-reviewer was started, before `work run` exited

  @r118
  Scenario: under a delegation, an answer to a reviewer's question that asks for a change makes the work-item ready again
    Pins that a work-item whose review a session answered in the person's place goes back to its implementer when the answer wants it changed, without the person.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
    And the session answering under the delegation answers "No, remove the old reader.", an answer that asks for a change, and every worker gives DONE
    When the person runs `work run i1`
    Then w1's transition from awaiting-answer to ready was made once the session had answered

  @r119
  Scenario: under a delegation, an answer to a reviewer's question that accepts the work-item as it is transitions the work-item to done
    Pins that a work-item whose review a session answered in the person's place moves on as it stands, not back to its implementer, when the answer takes it as it is, without the person.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
    And the session answering under the delegation answers "Yes, keep it as it is.", an answer that accepts the work-item as it is, and every worker gives DONE
    When the person runs `work run i1`
    Then w1's transition from awaiting-answer to done was made once the session had answered

  @r120
  Scenario: under a delegation, the session answering a reviewer's question is asked to say in its result whether its answer asks for a change or accepts the work-item as it is
    Pins that the brief of a session answering a reviewer's question in the person's place asks the session to say which way its answer goes, so that `work run` can tell from the result alone.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
    And the session answering under the delegation answers "Yes, keep it as it is.", and every worker gives DONE
    When the person runs `work run i1`
    Then the brief of the session answering "Is the old reader kept?" asks it to give in its result whether its answer asks for a change or accepts w1 as it is
