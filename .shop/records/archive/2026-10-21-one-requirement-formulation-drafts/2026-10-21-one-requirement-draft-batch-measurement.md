---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-one-requirement-draft-batch-measurement
kind: initiative-archive
about: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
date: 2026-10-22
---

# batch-measurement: round-3 draft for decisions 0054/0055/0056 (0.22.0)

The blind feature-formulator's round-3 whole draft of features/batch-measurement.feature, formulated from spec/capabilities/batch-measurement.md for decisions 0054 (a scenario names one requirement), 0055 (exits are successful or errors) and 0056 (a changed main checkout is a fault, so failed), release 0.22.0; written 2026-10-22 and not yet applied to features/ when archived. The round's set is listed in index.md beside this record; the round's reply and review findings are the matching review-finding record review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-one-requirement-formulation.

Archived from `.shop/scratch/drafts/2026-10-21-one-requirement/batch-measurement.feature` (git-ignored scratch), text as it was.

```gherkin
# formulated from spec/capabilities/batch-measurement.md
Feature: Batch measurement
  Narrator: a session measuring a closed batch

  @r1
  Scenario: an archive file's batch runs from the archive commit before it to its own
    A named archive file's batch starts where the previous archive file was added and ends where its own was.
    Given archive file 2026-09-01-slices.md was added by commit A
    And archive file 2026-09-15-slices.md was added by a later commit B
    When the session runs measure batch for 2026-09-15-slices.md
    Then one facts file is written for the batch
    And the batch's window runs from commit A to commit B

  @r2
  Scenario: without an archive file the open batch is measured from the last archive commit to now
    With no archive file, the batch is the work since the last archive, read against the living plan.
    Given the last archive file was added by commit B
    And the repository has one living plan
    When the session runs measure batch with no archive file
    Then the batch's window runs from commit B to now
    And the slices are read from the living plan

  @r3
  Scenario Outline: a given --<option> replaces that end of the batch
    Either end of the batch can be set by hand, as a commit or as an ISO time.
    Given archive file 2026-09-15-slices.md whose batch runs from commit A to commit B
    When the session runs measure batch for 2026-09-15-slices.md with --<option> <value>
    Then the batch's <end> is <value>

    Examples:
      | option | value                | end   |
      | from   | commit C             | start |
      | from   | 2026-09-05T09:00:00Z | start |
      | to     | commit D             | end   |
      | to     | 2026-09-14T18:00:00Z | end   |

  @r4
  Scenario: without --out the facts go under measurements in the archive file's name
    The default place for an archive batch's facts follows the archive file's name.
    Given archive file 2026-09-15-slices.md with dispatches inside its batch
    When the session runs measure batch for 2026-09-15-slices.md with no --out
    Then the facts are written to docs/superpowers/measurements/2026-09-15-slices.json

  @r38
  Scenario: an archive file no commit added is refused
    A batch cannot be bounded by an archive file git has no record of adding.
    Given a file 2026-10-01-slices.md that no commit added
    When the session runs measure batch for 2026-10-01-slices.md
    Then measure batch refuses because the archive file was not added by any commit
    And the refusal names 2026-10-01-slices.md

  @r6
  Scenario: a transcript of an unknown shape is refused and no facts are written
    Measure does not guess at transcripts it does not recognise.
    Given a batch with a transcript that lacks a field measure knows transcripts to have
    When the session runs measure batch for the batch
    Then measure batch refuses because the transcript's shape is not known
    And the refusal names the transcript and what was missing
    And no facts file is written

  @r7
  Scenario: an existing facts file is not written over without --replace
    A facts file already written survives a second run unless replacing is asked for.
    Given the batch's facts file already exists
    When the session runs measure batch for the batch with no --replace
    Then measure batch refuses because the facts file exists
    And the facts file is as it was

  @r6
  Scenario: a batch with no dispatch inside it is refused
    A batch in which nothing was dispatched has nothing to measure.
    Given a batch inside whose window no dispatch started
    When the session runs measure batch for the batch
    Then measure batch refuses because no dispatch was found inside the batch
    And the refusal names the window it searched
    And nothing is written

  @r9
  Scenario Outline: a transcript an Agent tool started is a dispatch only when it starts inside the batch
    Whether such a transcript belongs to the batch is decided by when it started.
    Given a batch running from commit A to commit B
    And a transcript an Agent tool started that starts <when> the batch
    When the session runs measure batch for the batch
    Then the transcript <counted> as a dispatch

    Examples:
      | when   | counted       |
      | inside | is counted    |
      | before | is not counted |
      | after  | is not counted |

  @r10
  Scenario: a request's usage is counted once, and its reasoning is part of its output
    A request repeated across transcript rows is not counted again, and reasoning tokens are shown inside the output figure, not on top of it.
    Given a batch with one dispatch that made one request
    And the request's usage, 500 new input and 1200 output tokens of which 300 are reasoning, appears in three transcript rows
    When the session runs measure batch for the batch
    Then the facts count the request's 500 new input and 1200 output tokens once
    And the facts give its output as 1200, of which 300 reasoning
    And no output figure in the facts is 1500

  @r11
  Scenario: a dispatching session's own requests are the controller's
    The session that dispatched inside the batch has its own requests there counted to the controller.
    Given a session that started a dispatch inside the batch
    And made requests of its own inside the batch
    When the session runs measure batch for the batch
    Then the facts count that session's requests inside the batch as the controller's

  @r12
  Scenario Outline: a dispatch is attributed by its description, then its prompt, else unattributed
    Attribution tries the description first and the prompt second, and admits when neither tells.
    Given a dispatch whose description <description> and whose prompt <prompt>
    When the session runs measure batch for the batch
    Then the facts attribute the dispatch to <attributed>

    Examples:
      | description         | prompt                  | attributed  |
      | names slice 2       | names slice 3           | slice 2     |
      | names batch work    | names slice 3           | batch work  |
      | names no slice      | names slice 3           | slice 3     |
      | names no slice      | names no task or slice  | unattributed |

  @r13
  Scenario: a reviewer's findings are counted as it wrote them
    Critical and Important findings are its lines so marked, and Minor is the count it gives.
    Given a reviewer's reply with 2 lines beginning Critical and 1 line beginning Important
    And the reply gives a count of 4 Minor
    When the session runs measure batch for the batch
    Then the facts count the reviewer's findings as 2 Critical, 1 Important and 4 Minor

  @r14
  Scenario: a commit goes to the implementer running when it was made
    Each commit is credited to the implementer at work at the time and its files are sorted into kinds.
    Given an implementer dispatch running from 10:00 to 10:30
    And a commit made at 10:15 that touched three files
    When the session runs measure batch for the batch
    Then the facts give the commit to that implementer
    And each of its three files is counted as production, test or other

  @r15
  Scenario Outline: each slice's Lands line sits beside the files its dispatches touched
    What a slice said it would land is set against what its dispatches actually touched.
    Given a <batch> whose <source> gives slice 1 the Lands line "2 production, 1 test"
    And slice 1's dispatches touched src/cart.py and tests/test_cart.py
    When the session runs measure batch for the <batch>
    Then the facts give slice 1 the Lands line 2 production, 1 test beside 1 production, 1 test and 0 other files touched

    Examples:
      | batch         | source       |
      | archive batch | archive file |
      | open batch    | living plan  |

  @r16
  Scenario: the facts give the plan's tasks at both ends, its hand-backs and suite record
    The batch plan's task list is taken when the plan was added and again at the batch's end.
    Given a batch plan that had 5 tasks when it was added and 7 tasks at the batch's end
    And the plan has two hand-back entries and a suite record
    When the session runs measure batch for the batch
    Then the facts give the 5 tasks it had when it was added and the 7 it had at the end
    And the facts give both hand-back entries and the suite record

  @r17
  Scenario: the facts hold no prompt, reply or tool content
    What the agents said and did is measured, never copied into the facts.
    Given a batch whose dispatches have prompts, replies and tool calls
    When the session runs measure batch for the batch
    Then the facts hold none of the prompts', replies' or tools' content

  @r18
  Scenario: show prints a facts file as tables
    A facts file can be read without opening the JSON.
    Given a facts file measure wrote
    When the session runs measure show for the file
    Then the facts are printed as tables

  @r19
  Scenario: compare prints two facts files side by side
    Two batches can be read against each other.
    Given two facts files measure wrote
    When the session runs measure compare for the two files
    Then the two files' facts are printed side by side

  @r38
  Scenario: show refuses a file measure did not write as facts
    Show reads only facts files of measure's own making.
    Given a JSON file that is not a facts file measure wrote
    When the session runs measure show for the file
    Then measure refuses because the file is not a facts file measure wrote
    And the refusal names the file

  @r38
  Scenario Outline: the open batch needs --plan when the living plan cannot be found
    Without one slices plan in the repository, measure cannot read the open batch.
    Given a repository with <plans> docs/superpowers/plans/*-slices.md files
    When the session runs measure batch with no archive file and no --plan
    Then measure batch refuses because the living plan cannot be found

    Examples:
      | plans |
      | no    |
      | two   |

  @r38
  Scenario Outline: a batch with no archive before it needs --from
    When nothing marks where the batch began, measure cannot place its start.
    Given <batch> with no archive file added before the batch's end
    When the session runs measure batch for it with no --from
    Then measure batch refuses because the batch has no start

    Examples:
      | batch                                           |
      | the open batch of a repository                  |
      | the batch of the first archive file a commit added |

  @r38
  Scenario Outline: a --<option> that is neither a commit nor an ISO time is refused
    An end of the batch must be something measure can place in time.
    Given a repository with no commit named "last-tuesday"
    When the session runs measure batch with --<option> last-tuesday
    Then measure batch refuses because the value is neither a commit nor an ISO time
    And the refusal names last-tuesday

    Examples:
      | option |
      | from   |
      | to     |

  @r38
  Scenario Outline: git's failures are refused with git's error
    When git cannot answer, measure passes on what git said.
    Given <situation>
    When the session runs measure batch
    Then measure refuses with git's error

    Examples:
      | situation                                                   |
      | --repo names a directory that is not inside a git repository |
      | the current directory is not inside a git repository and no --repo is given |
      | a git command measure batch runs fails                      |

  @r2
  Scenario Outline: the open batch is named by --name, default open
    The open batch's name can be chosen.
    Given an open batch with dispatches inside it
    When the session runs measure batch with no archive file and <name option>
    Then the batch is named <name>

    Examples:
      | name option     | name       |
      | no --name       | open       |
      | --name trial-3  | trial-3    |

  @r4
  Scenario Outline: without --out the open batch's facts go under measurements in its name
    The default place for the open batch's facts follows the open batch's name.
    Given an open batch with dispatches inside it
    When the session runs measure batch with no archive file, <name option> and no --out
    Then the facts are written to docs/superpowers/measurements/<name>.json

    Examples:
      | name option     | name       |
      | no --name       | open       |
      | --name trial-3  | trial-3    |

  @r2
  Scenario Outline: the open batch starts at the last commit that added a file under the archive directory
    The archive directory that marks batch boundaries defaults to the plans archive and can be changed.
    Given the last commit adding a file under <directory> is commit <commit>
    When the session runs measure batch with no archive file and <archive option>
    Then the batch starts at commit <commit>

    Examples:
      | archive option            | directory                     | commit |
      | no --archive-dir          | docs/superpowers/plans/archive | A      |
      | --archive-dir old/plans   | old/plans                     | B      |

  @r15
  Scenario Outline: the facts hold the slices the batch planned and the slices dispatches were attributed to
    An archive batch keeps all its planned slices; the open batch only those that saw work.
    Given a <batch> whose <source> holds slices 1 and 2
    And the only dispatches are attributed to slice 2 and slice 3
    When the session runs measure batch for the <batch>
    Then the facts hold slices <slices>

    Examples:
      | batch         | source       | slices     |
      | archive batch | archive file | 1, 2 and 3 |
      | open batch    | living plan  | 2 and 3    |

  @r14
  Scenario: a commit made while two implementers ran is counted as ambiguous
    Credit for a commit is flagged as uncertain when more than one implementer could have made it.
    Given two implementer dispatches both running at 10:15
    And a commit made at 10:15
    When the session runs measure batch for the batch
    Then the facts count the commit as ambiguous

  @r29
  Scenario Outline: tasks are left uncounted with a note when the batch plan cannot be had
    Without a batch plan to read, the facts say why tasks are missing instead of counting none.
    Given <situation>
    When the session runs measure batch for the batch
    Then the facts leave tasks uncounted
    And the facts hold a note saying why

    Examples:
      | situation                                                   |
      | no dispatch names a ledger and no --tasks is given          |
      | the batch plan is in no commit                              |

  @r31
  Scenario Outline: a reply closing <status> is counted as not done
    The closing status a reply gives is kept, and the stuck ones are counted as not done.
    Given a dispatch whose reply closes with status <status>
    When the session runs measure batch for the batch
    Then the facts give the dispatch the closing status <status>
    And the facts count the dispatch as not done

    Examples:
      | status        |
      | BLOCKED       |
      | PARTIAL       |
      | NEEDS_CONTEXT |

  @r32
  Scenario: the facts record the versions the transcripts name and the window
    The facts say what plugin and harness ran, and when the batch was.
    Given archive file 2026-09-15-slices.md whose batch runs from commit A to commit B
    And its transcripts name plugin version 0.18.0 and harness version 2.1.4
    When the session runs measure batch for 2026-09-15-slices.md
    Then the facts record plugin version 0.18.0 and harness version 2.1.4
    And the facts record the window as the times of commits A and B and as commits A and B

  @r33
  Scenario Outline: a batch starting at a commit gives the files and lines changed to its end
    The size of the change is taken from the batch's start commit to its end commit, or HEAD.
    Given a batch starting at commit A and ending <end>
    When the session runs measure batch for the batch
    Then the facts give the files and lines changed from commit A to <to>

    Examples:
      | end                       | to       |
      | at commit B               | commit B |
      | at 2026-09-14T18:00:00Z   | HEAD     |
      | now                       | HEAD     |

  @r34
  Scenario: the facts count resumed dispatches, the late share of building time without scouts, and starting context
    Building time is the dispatches' own durations added up, scouts aside, and the share after the first branch review is taken of that.
    Given a batch whose dispatches are
      | dispatch      | role          | prompts | starts               | own duration in minutes | starting context |
      | implementer 1 | implementer   | 1       | before any review    | 30                      | 20000            |
      | implementer 2 | implementer   | 1       | with implementer 1   | 30                      | 30000            |
      | review 1      | branch review | 1       | after both           | 10                      | 40000            |
      | fix 1         | implementer   | 2       | after review 1       | 30                      | 10000            |
      | scout 1       | scout         | 1       | after review 1       | 15                      | 50000            |
    And implementer 1 and implementer 2 ran at the same time
    When the session runs measure batch for the batch
    Then the facts count 1 dispatch as resumed
    And the facts give 0.4 as the share of building time from the first branch review on
    And the facts give a mean starting context of 30000 and a summed starting context of 150000

  @r19
  Scenario: compare prints both files' figures with the ratio of the second to the first
    Compare sets each figure, in total and per slice, side by side, with how the second batch differs.
    Given facts file a for batch 2026-09-01 with 2 slices
    And facts file b for batch 2026-09-15 with 2 slices
    When the session runs measure compare for a and b
    Then each figure of both files, in total and per slice, is printed with the ratio of b's to a's

  @r38
  Scenario Outline: a file measure cannot read as its facts is refused
    Compare reads only measure's own facts files, and neither command reads a file that is not JSON.
    Given a file that <file>
    When the session runs measure <command> with the file
    Then measure refuses because the file <reason>
    And the refusal names the file

    Examples:
      | command | file                                              | reason                                |
      | compare | is JSON but not a facts file measure wrote        | is not a facts file measure wrote     |
      | show    | cannot be read as JSON                            | cannot be read as JSON                |
      | compare | cannot be read as JSON                            | cannot be read as JSON                |

  @r38
  Scenario: a refusal says why on stderr and exits with an error
    Every refusal is explained on stderr and ends with an error.
    Given the batch's facts file already exists
    When the session runs measure batch for the batch with no --replace
    Then measure refuses and says why on stderr
    And it exits with an error
```
