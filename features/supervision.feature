# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  Background:
    Given a git repository with an initiative i1 under .shop/work/, a stand-in claude first on PATH and as $SHOPSYSTEM_WORK_CLAUDE, and tests that pass

  @r1 @r9
  Scenario: `work run` pulls each work-item through research, plan, implementation and review, one worker at a time, until no work-item can make a transition
    Pins the stage-by-stage pull: every work-item reaches `green` through its four workers in order, and no worker starts before the last one ended.
    Given i1's work-items w1 and w2 are drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1 and w2 had code-scout, bdd-planner, bdd-implementer and bdd-task-reviewer as its workers, in that order
    And no worker was started before the one before it had ended
    And w1 and w2 are green
    And it exits 0

  @r2
  Scenario: each worker is a new `claude -p` session of its stage's agent, given one brief naming the work-item, the files to read and where its result goes
    Pins how a worker is started: its stage's agent, a session no other worker had, and one brief that says what to read and where the result goes.
    Given i1's work-item w1 is drafted, under thing
    And every worker gives DONE
    When the person runs `work run i1`
    Then each worker was started as `claude -p` with an input prompt naming its brief, --agent shopsystem-bdd:<its stage's agent> and a session id no other worker had
    And each brief names .shop/work/i1/w1.md and spec/capabilities/thing.md to read, and a result path in the brief's own directory
    And each worker worked in a worktree of its own, never in the repository's own checkout, and its brief and result are under .shop/scratch/ there
    And the implementer's brief also names the plugin's scripts directory, the initiative branch's base, its worktree and its branch work/w1, and how the whole suite `work run` ran there ended

  @r2
  Scenario Outline: a worker is given its stage's tools and no others, the list .shop/delivery.toml gives for the stage where it gives one
    Pins that no worker has every permission: a Bash command outside its stage's list is refused. `{scripts}` stands for the directory of `work run`'s own scripts.
    Given i1's work-item w1 is drafted
    And <tools>
    And every worker gives DONE, the researcher running `git commit -q --allow-empty -m meddle`
    When the person runs `work run i1`
    Then the researcher was given --allowedTools <list>
    And its `git commit -q --allow-empty -m meddle` was <fate>

    Examples:
      | tools                                                                    | list                                                                                                                                                                                                        | fate    |
      | .shop/delivery.toml names no tools                                       | Read,Glob,Grep,Bash(python3 -m pytest*),Bash(python3 {scripts}/features *),Bash(python3 {scripts}/model *),Bash(python3 {scripts}/tools *),Bash(git status*),Bash(git diff*),Bash(git log*),Bash(git show*) | refused |
      | .shop/delivery.toml gives the research stage Read and Bash(git commit *) | Read,Bash(git commit *)                                                                                                                                                                                     | run     |

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

  @r4
  Scenario: an implementer's DONE whose scenarios pass only on a file it left uncommitted is not merged
    Pins that the scenarios and the suite run on the branch, which is what the merge takes: a file the implementer wrote and did not commit is not there.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer writing feature.txt and not committing it
    And the work-item's scenarios pass only where feature.txt is
    When the person runs `work run i1`
    Then the initiative branch does not have the implementer's commit
    And w1 is awaiting-ruling, its question naming `python3 tests.py --work-item w1` and what it printed

  @r5
  Scenario Outline: a researcher that <gives> makes the work-item's transition to awaiting-ruling with <question> as its question
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
      | writes no result                                         | code-scout gave no result file   |
      | writes a result that is not JSON                         | is not a JSON object             |
      | gives QUESTION, its questions the string "Why so?"       | Why so?                          |
      | gives QUESTION, its questions the number 7               | not a list of questions          |

  @r5
  Scenario: a question goes into the work-item's Questions section, before a section that follows it
    Pins where the question is written, so that what follows the Questions section is never read as a question.
    Given i1's work-item w1 is drafted, its file with a Questions section of "Old question?" and then a Rulings section with "Old ruling."
    And the researcher gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then w1's Questions section holds "Old question?" and then "Which module owns the log?", and its Rulings section only "Old ruling."
    And `work run` prints the question "Which module owns the log?" and not "Old ruling."

  @r6
  Scenario: a worker's change to a file under .shop/work/ outside its stage directory is put back
    Pins that only `work run` writes a work-item's status and the initiative's files, while the worker's stage directory keeps what it wrote.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also setting w1's status to green, changing .shop/work/i1/initiative.md and writing notes.md in its stage directory
    When the person runs `work run i1`
    Then .shop/work/i1/initiative.md is as it was
    And log.jsonl's first transition of w1 is from drafted to researched
    And the researcher's notes.md is in its stage directory

  @r6
  Scenario: a file a worker adds under .shop/work/ outside its stage directory is removed
    Pins that .shop/work/ outside the worker's stage directory is as it was before the worker started, new files included.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher also writing .shop/work/i1/w9.md and .shop/work/i2/initiative.md
    When the person runs `work run i1`
    Then .shop/work/i1/w9.md and .shop/work/i2/ are not there
    And w1 is green

  @r6
  Scenario: a file committed under .shop/work/ in the repository's own checkout while a worker works is kept
    Pins that `work run` puts back only what a worker changed, in its worktree or on its branch, and never a change made elsewhere.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, and while the researcher works another session commits .shop/work/i2/initiative.md and a change to .shop/work/i1/initiative.md in the repository's own checkout
    When the person runs `work run i1`
    Then .shop/work/i2/initiative.md and .shop/work/i1/initiative.md are as that session committed them, with nothing under .shop/work/ left uncommitted
    And w1 is green

  @r6
  Scenario Outline: an implementer's commit <change> under .shop/work/ is put back on its branch, the branch is not merged, and the work-item goes to awaiting-ruling naming the file
    Pins that a worker's commit cannot write a status or any other file under .shop/work/ onto the initiative branch.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer committing feature.txt and <change>
    When the person runs `work run i1`
    Then the initiative branch does not have the implementer's commit
    And the branch work/w1 changes nothing under .shop/work/
    And w1 is awaiting-ruling, its question saying <path>

    Examples:
      | change                                          | path                         |
      | setting .shop/work/i1/w1.md's status to green   | .shop/work/i1/w1.md          |
      | deleting .shop/work/i1/initiative.md            | .shop/work/i1/initiative.md  |
      | adding .shop/work/i1/w9.md                      | .shop/work/i1/w9.md          |

  @r7
  Scenario: each transition is a commit of the work-item's file, its stage directories and log.jsonl on the initiative branch, and nothing else
    Pins one commit per transition, and that a transition's commit takes no file but its own.
    Given i1's work-item w1 is drafted
    And README.md has a change that is not committed
    And every worker gives DONE
    When the person runs `work run i1`
    Then the initiative branch has one commit for each transition log.jsonl gives, `work: w1 drafted -> researched` first and `work: w1 done -> green` last
    And each of those commits changes .shop/work/i1/w1.md and .shop/work/i1/log.jsonl, and nothing but them and files under .shop/work/i1/runs/w1/
    And README.md's change is still not committed

  @r8
  Scenario: a worker's start and end are lines in log.jsonl with the time, the work-item, the stage, the agent and the session id
    Pins what `work run` writes of each worker, the session id being the one claude was given.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then log.jsonl has, for each of w1's four workers, a start line and then an end line, each with the time, w1, the stage, the agent and the session id claude was given

  @r9
  Scenario: when no work-item can make a transition, `work run` exits, printing each work-item's status and each open question
    Pins what the person reads when `work run` stops, and that an open question is its own exit.
    Given i1's work-items w1 is drafted and w2 is green
    And the researcher gives QUESTION, asking "Which module owns the log?"
    When the person runs `work run i1`
    Then `work run` prints w1 with awaiting-ruling and the question "Which module owns the log?", and w2 with green
    And it exits 3

  @r9
  Scenario: when every work-item is green or withdrawn, `work run` exits 0, printing each work-item's status
    Pins that a delivery whose work-items all ended well, or were set aside, is no failure; only an open question or a work-item that can make no transition is an exit of its own.
    Given i1's work-items w1 is green and w2 is withdrawn
    When the person runs `work run i1`
    Then `work run` prints w1 with green, and w2 with withdrawn
    And it exits 0

  @r10
  Scenario Outline: `work run` that cannot do what it was asked exits non-zero, says why in one line, and changes nothing
    Pins that `work run` verifies what it was given before any worker starts, and a refused transition is its refusal.
    Given <setup>
    When the person runs `work run <initiative>`
    Then work says in one line that <reason>
    And it exits non-zero
    And no worker was started
    And nothing in the repository has changed, its commits included

    Examples:
      | setup                                                                        | initiative | reason                                                                                    |
      | i1's work-item w1 is drafted                                                 | i9         | the initiative i9 does not exist                                                          |
      | i1's work-item w1 is drafted, though log.jsonl's last transition of w1 is to researched | i1 | .shop/work/i1/w1.md gives its status as drafted, but log.jsonl's last move of w1 is to researched |
      | i1's work-item w1 is drafted, in a directory that is not a git repository     | i1         | not a git repository                                                                      |
      | i1's work-item w1 is drafted, its checkout's HEAD detached                    | i1         | HEAD is detached                                                                          |

  @r4 @r5 @r10
  Scenario Outline: a delivery's worktrees are removed when `work run` exits, whatever the implementer's work came to: <end>
    Pins that `work run` leaves no worktree behind, on a merge, a question or a failure.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer <doing>
    When the person runs `work run i1`
    Then .shop/worktrees/w1 is not there, and git lists no worktree but the repository's own

    Examples:
      | end        | doing                                          |
      | merged     | committing feature.txt                         |
      | a question | committing feature.txt and suite-fail          |
      | BLOCKED    | giving BLOCKED, asking "Is the old reader kept?" |
      | a failure  | deleting its own branch                        |

  @r10
  Scenario: a git command that fails ends `work run` with git's reason in one line and a non-zero exit code
    Pins that a failure of git during a delivery is `work run`'s refusal, never a traceback.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer deleting its own branch
    When the person runs `work run i1`
    Then work says in one line that git merge --ff-only work/w1 failed
    And it exits non-zero

  @r5 @r10
  Scenario: a failure of git after the work-item was claimed makes its transition to awaiting-ruling with the failure as its question
    Pins that no work-item is left claimed, from which no transition follows, when its implementation fails part-way.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer deleting its own branch
    When the person runs `work run i1`
    Then w1 is awaiting-ruling, its question saying git merge --ff-only work/w1 failed
    And it exits non-zero

  @r11
  Scenario: each worker is given this plugin's own directory as its plugin
    Pins that the agents a worker is started as are this plugin's, not those of another copy of it installed on the machine.
    Given i1's work-item w1 is drafted
    And every worker gives DONE
    When the person runs `work run i1`
    Then each of w1's four workers was started with --plugin-dir the directory that holds `work run`'s own scripts

  @r11
  Scenario: when the repository is inside the plugin's own directory, the workers' worktrees are outside it, and gone when `work run` exits
    Pins that `work run` delivering this plugin's own work gives workers writable worktrees: claude refuses every write under a --plugin-dir, so none may lie under the plugin's directory.
    Given i1's work-item w1 is drafted
    And the repository is the plugin: it holds `work run`'s own scripts and agents
    And every worker gives DONE, the implementer writing report.md at the top of its worktree and naming it as its report
    When the person runs `work run i1`
    Then each of w1's four workers worked in a worktree outside the plugin's directory
    And w1 is green
    And .shop/worktrees/w1 is not there, and git lists no worktree but the repository's own

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
    Pins that a worker's writes stay in the worktree it was started in, where acceptEdits allows them, even when .shop/delivery.toml lists a bare Write.
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
    Pins that no worker runs any Python it likes: `{scripts}` stands for the directory of `work run`'s own scripts.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the <who> running `<command>`
    When the person runs `work run i1`
    Then its `<command>` was <fate>

    Examples:
      | who         | command                              | fate    |
      | researcher  | python3 -m pytest --version          | run     |
      | researcher  | python3 {scripts}/features --help    | run     |
      | researcher  | python3 -c pass                      | refused |
      | researcher  | python3 {scripts}/work --help        | refused |
      | planner     | git status                           | refused |
      | implementer | python3 -m pytest --version          | run     |
      | implementer | python3 -c pass                      | refused |
      | implementer | git log -1                           | refused |
      | implementer | python3 {scripts}/work show          | refused |
      | reviewer    | git log -1                           | run     |
      | reviewer    | python3 -c pass                      | refused |

  @r15
  Scenario: a file the worker's result names is copied into the stage directory before its worktree is removed
    Pins that what a worker's result points to is still there for the person and the next worker once its worktree is gone.
    Given i1's work-item w1 is ready
    And every worker gives DONE, the implementer writing report.md at the top of its worktree and naming it as its report
    When the person runs `work run i1`
    Then .shop/work/i1/runs/w1/1-implement/ has report.md, as the implementer wrote it
    And .shop/worktrees/w1 is not there, and git lists no worktree but the repository's own

  @r16
  Scenario: a researcher's DONE with questions puts those questions into the planner's brief
    Pins that what the researcher asked reaches the planner, rather than being asked again.
    Given i1's work-item w1 is drafted
    And every worker gives DONE, the researcher asking "Is a title given twice one book or two?"
    When the person runs `work run i1`
    Then the planner's brief has the researcher's question "Is a title given twice one book or two?"
    And w1 is green

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
    Then the initiative branch has the implementer's commit of feature.txt
    And git lists no branch work/w1

  @r19
  Scenario: a researcher is given the work-item's file set and accepted scenarios, and a limit of 25 turns
    Pins that the researcher starts from the work-item's file set and accepted scenarios, rather than searching the repository for it, and ends within a bounded number of turns.
    Given i1's work-item w1 is drafted, its file set scripts/thing.py and tests/test_thing.py
    And features/thing.feature has the scenario "it answers", tagged @r1, and the scenario "it waits", tagged @r2
    And every worker gives DONE
    When the person runs `work run i1`
    Then the researcher's brief gives scripts/thing.py and tests/test_thing.py as the work-item's file set
    And the researcher's brief names the accepted scenario "it answers" of features/thing.feature, and not "it waits"
    And the researcher was started with --max-turns 25

  @r20
  Scenario: two ready work-items whose claims would not share a file are implemented at the same time, and merged one at a time
    Pins that work-items with no file in common are implemented side by side, while the initiative branch takes one branch at a time, each on top of the one before.
    Given i1's work-items w1 is ready, its file set w1.txt, and w2 is ready, its file set w2.txt
    And every worker gives DONE, each implementer committing a file named for its work-item once two implementers have started
    When the person runs `work run i1`
    Then the implementers of w1 and w2 worked at the same time
    And the initiative branch has both implementers' commits, one after the other, with no merge commit
    And w1 and w2 are green

  @r20
  Scenario Outline: two ready work-items whose claims would share a file are implemented one after the other: <how>
    Pins that two implementers never edit one file: a glob or a directory in a file set covers each tracked file it holds.
    Given the repository has lib/thing_a.py committed
    And i1's work-items w1 is ready, its file set <first>, and w2 is ready, its file set <second>
    And every worker gives DONE, each implementer committing a file named for its work-item
    When the person runs `work run i1`
    Then no implementer was started before the one before it had ended
    And w1 and w2 are green

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
    And w1, w2 and w3 are green
