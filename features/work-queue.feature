# formulated from spec/capabilities/work-queue.md
Feature: Work queue
  Narrator: a person, session or script reading work-items or writing their transitions

  @r1 @deprecated
  Scenario: add with --part-of, --under and --accepts writes a drafted work-item with the fields given (deprecated)
    Deprecated for: add with a title, --part-of, --under and --accepts writes a drafted work-item named by its id and prints the id
    Pins where add writes the work-item and that it holds what the command was given, as drafted.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then .shop/work/i1/w1.md is a drafted work-item w1
    And its part_of is capability-proposal/p1, its under is thing and its accepts is thing#r1

  @r1
  Scenario: add with a title, --part-of, --under and --accepts writes a drafted work-item named by its id and prints the id
    Pins that add names the work-item's file by the id it gives it, holds the title and the fields given, and tells the caller that id.
    Given an initiative i1 under .shop/work/
    When the session runs `work add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work prints one id w<n>, and nothing else
    And .shop/work/i1/w<n>.md is a drafted work-item whose id is that w<n>
    And its part_of is capability-proposal/p1, its under is thing and its accepts is thing#r1
    And its `# ` heading is Show the queue

  @r12
  Scenario: add numbers the new work-item one above the highest work-item under .shop/work/, in any initiative and any status
    Pins that ids are numbered across the whole queue, so a work-item in another initiative, or one withdrawn, is never given its id again.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    And an initiative i2 under .shop/work/ whose work-item w2 is green and whose work-item w4 is withdrawn
    When the session runs `work add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work prints w5
    And .shop/work/i1/w5.md is a drafted work-item whose id is w5
    And no other work-item's file has changed

  @r22
  Scenario: start on an accepted request writes a proposed capability-change initiative that fulfils it, sourced from its origins, and prints its id
    Pins that an accepted request is where an initiative begins: start writes one new initiative for it, carrying the request's origins, and tells the caller its id.
    Given an initiative i1 under .shop/work/
    And a request q1 that is accepted, whose origins are o1 and o2
    When the session runs `work start q1`
    Then .shop/work/ has one new initiative, its initiative.md a proposed initiative of kind capability-change
    And it fulfils q1, and its source is o1 and o2
    And work prints that initiative's id
    And .shop/work/i1/ is as it was
    And it exits successfully

  @r25
  Scenario: start commits the initiative it writes on the current branch
    Pins that the initiative start writes is in the branch's history when it ends, so nothing that puts .shop/work/ back to its last commit undoes it.
    Given a request q1 that is accepted, whose origins are o1 and o2
    And the repository is a git repository on the branch main, everything in it committed
    When the session runs `work start q1`
    Then main has a new last commit, which holds the new initiative's initiative.md as work left it
    And nothing under the new initiative's directory under .shop/work/ differs from main's last commit
    And it exits successfully

  @r23
  Scenario Outline: a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    Pins that the command that completes an initiative's work also ends the initiative, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    And <request>
    When the session runs `work withdraw w2`
    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    And .shop/work/i1/initiative.md gives i1's status as done
    And it exits successfully

    Examples:
      | request                                                                                    |
      | no request kept in this context names i1                                                   |
      | a request q1 kept in this context, whose asker is this context, names i1 and is delivered  |
      | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
      | a request q1 kept in this context, whose asker is this context, names i2 and is accepted   |

  @r23
  Scenario: retry that makes an initiative's last open work-item green again sets the initiative to done
    Pins that retry, like withdraw, is a command whose change can complete an initiative, and that it ends the initiative when it does.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is failed
    And .shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed
    And no request kept in this context names i1
    When the session runs `work retry w2`
    Then .shop/work/i1/w2.md gives w2's status as green
    And .shop/work/i1/initiative.md gives i1's status as done
    And it exits successfully

  @r3
  Scenario: show prints each work-item of every initiative with its status
    Pins that show reads every initiative under .shop/work/, and only their work-items.
    Given an initiative i1 under .shop/work/ whose work-items w1 is drafted and w2 is ready
    And an initiative i2 under .shop/work/ whose work-item w3 is claimed and whose capability-proposal p1 is merged
    When the session runs `work show`
    Then work prints w1 with drafted, w2 with ready and w3 with claimed
    And it prints nothing about p1

  @r11
  Scenario: show with --json prints each work-item with its initiative and status as one JSON object
    Pins that show's result, read by a script, is one JSON object giving every work-item's initiative and status.
    Given an initiative i1 under .shop/work/ whose work-items w1 is drafted and w2 is ready
    And an initiative i2 under .shop/work/ whose work-item w3 is claimed
    When the session runs `work show --json`
    Then work prints one JSON object and nothing else
    And it gives w1 in i1 with drafted, w2 in i1 with ready and w3 in i2 with claimed

  @r4
  Scenario: a transition writes the new status into the work-item's file
    Pins that the work-item's file holds its status after a transition.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    When the script makes w1's transition to researched
    Then .shop/work/i1/w1.md gives w1's status as researched

  @r5
  Scenario: a transition appends a line to the initiative's log.jsonl with the time, the work-item, both statuses and who made it
    Pins what each transition writes, and that earlier lines stay.
    Given an initiative i1 under .shop/work/ whose work-item w1 is researched
    And .shop/work/i1/log.jsonl has one line, w1's transition from drafted to researched
    When the script makes w1's transition to planned
    Then .shop/work/i1/log.jsonl has two lines, the first as it was
    And its last line gives the time, w1, researched before, planned after, and the script as who made the transition

  @r6
  Scenario: a transition is refused when the work-item's status in its file is not the last status log.jsonl gives it
    Pins that a file and its log that disagree stop the transition, and the refusal names both.
    Given an initiative i1 under .shop/work/ whose work-item w1 is ready
    And .shop/work/i1/log.jsonl's last line for w1 is its transition to planned
    When the script makes w1's transition to claimed
    Then the transition is refused, naming .shop/work/i1/w1.md, ready and planned
    And .shop/work/i1/w1.md and .shop/work/i1/log.jsonl are as they were

  @r7
  Scenario Outline: a command that cannot be done exits with an error, says why and changes nothing
    Pins that a missing file stops work with its reason, never a traceback, and leaves the files as they were.
    Given <setup>
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work says that <reason>
    And it exits with an error
    And nothing under the repository has changed

    Examples:
      | setup                                                   | reason                                             |
      | a repository with spec/index.md and no initiative i1    | the initiative i1 does not exist                   |
      | an initiative i1 under .shop/work/ and no spec/index.md | spec/index.md, which names the context, is missing |
      | an initiative i1 under .shop/work/ and a spec/index.md with no id | spec/index.md gives no bounded-context id |
      | an initiative i1 under .shop/work/ and a spec/index.md whose id is bounded-context | spec/index.md gives no bounded-context id |

  @r7
  Scenario: a transition of a work-item that does not exist is refused, saying why, and changes nothing
    Pins that a transition the library cannot make is refused with its reason rather than failing on a missing file.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the script makes w1's transition to researched
    Then the transition is refused, naming .shop/work/i1/w1.md
    And nothing under the repository has changed

  @r7
  Scenario Outline: add refuses an initiative that is not one directory entry under .shop/work/, saying why, and changes nothing
    Pins that add writes only inside .shop/work/<initiative>/, whatever it is given.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the session runs `work add <initiative> <name> --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work says that <reason>
    And it exits with an error
    And nothing under the repository has changed

    Examples:
      | initiative | name        | reason                                    |
      | ../../spec | w1          | the initiative ../../spec is not a name   |

  @r7
  Scenario: add refuses a field value with a newline in it, saying why, and changes nothing
    Pins that a value given to add cannot write a second line, a status say, into the work-item.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1` with a newline and `status: ready` in the --part-of value
    Then work says that the value of --part-of has a newline in it
    And it exits with an error
    And nothing under the repository has changed

  @r7
  Scenario: show refuses a file under an initiative that is not UTF-8 text, naming it
    Pins that show stops on a file it cannot read with its reason, never a traceback.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    And .shop/work/i1/w2.md is not UTF-8 text
    When the session runs `work show`
    Then work says that .shop/work/i1/w2.md is not UTF-8 text
    And it exits with an error

  @r7
  Scenario Outline: a transition of a work-item whose file <lacks> is refused, saying why, and changes nothing
    Pins that a transition writes a status only into a work-item whose frontmatter holds one, and logs nothing otherwise.
    Given an initiative i1 under .shop/work/ with a work-item w1 that <lacks>
    When the script makes w1's transition to researched
    Then the transition is refused, naming .shop/work/i1/w1.md
    And nothing under the repository has changed

    Examples:
      | lacks             |
      | has no status     |
      | has no frontmatter |

  @r7
  Scenario Outline: a transition whose log.jsonl <fault> is refused, saying why, and changes nothing
    Pins that a transition is all or nothing: the file and its log line are written together, or neither is.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    And .shop/work/i1/log.jsonl <fault>
    When the script makes w1's transition to researched
    Then the transition is refused, naming <named>
    And nothing under the repository has changed

    Examples:
      | fault                        | named                              |
      | has a line that is not JSON  | line 2 of .shop/work/i1/log.jsonl  |
      | cannot be written            | .shop/work/i1/log.jsonl            |

  @r7
  Scenario: request with a --lines file that does not exist is refused, naming the file, and changes nothing
    Pins that a missing lines file stops request with its reason, never a traceback, and leaves the files as they were.
    Given an upstream that keeps no request
    And no file lines.md
    When the session runs `work request "Show the queue" --from ctx-a --lines lines.md --source o1`
    Then work says that the file lines.md does not exist
    And it exits with an error
    And nothing under the repository has changed

  @r8
  Scenario: retry on a failed work-item transitions it to the status before its transition into failed
    Pins that retry, once the fault is remedied, returns the work-item to the status it had when it failed, not to one before it.
    Given an initiative i1 under .shop/work/ whose work-item w1 is failed
    And .shop/work/i1/log.jsonl gives w1's last transitions as from ready to claimed, then from claimed to failed
    When the session runs `work retry w1`
    Then .shop/work/i1/w1.md gives w1's status as claimed

  @r10
  Scenario: withdraw on a work-item that is neither claimed nor green transitions it to withdrawn
    Pins that withdraw takes a work-item out of the queue by a transition, written in its file and logged.
    Given an initiative i1 under .shop/work/ whose work-item w1 is ready
    And .shop/work/i1/log.jsonl's last line for w1 is its transition to ready
    When the session runs `work withdraw w1`
    Then .shop/work/i1/w1.md gives w1's status as withdrawn
    And .shop/work/i1/log.jsonl's last line is w1's transition from ready to withdrawn

  @r9 @deprecated
  Scenario Outline: `work <command>` commits the change it makes to a work-item on the current branch (deprecated)
    Deprecated for: `work <command>` commits the change it makes to a work-item or a capability-proposal on the current branch
    Pins that what `work add`, `work retry`, `work withdraw` and `work answer` write, the work-item's file and any log line, is in the branch's history when they end, so nothing that puts .shop/work/ back to its last commit undoes it.
    Given <given>
    And the repository is a git repository on the branch main, everything in it committed
    When the session runs `work <args>`
    Then main has a new last commit, which holds <holds>
    And nothing under .shop/work/ differs from main's last commit

    Examples:
      | command  | given                                                                                          | args                                                                        | holds                                                                                                     |
      | add      | an initiative i1 under .shop/work/ with no work-item w1                                        | add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1 | .shop/work/i1/w1.md as work left it                                                                       |
      | retry    | an initiative i1 under .shop/work/ with a work-item w1 that failed in its implementation stage | retry w1                                                                    | .shop/work/i1/w1.md as work left it and .shop/work/i1/log.jsonl with w1's transition from failed as its last line    |
      | withdraw | an initiative i1 under .shop/work/ whose work-item w1 is ready, its last log.jsonl line for w1 its transition to ready | withdraw w1                                                  | .shop/work/i1/w1.md as work left it and .shop/work/i1/log.jsonl with w1's transition from ready to withdrawn as its last line |
      | answer   | an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by an implementer | answer w1 "Use the first reading"                       | .shop/work/i1/w1.md as work left it and .shop/work/i1/log.jsonl with w1's transition from awaiting-answer to ready as its last line |

  @r9
  Scenario Outline: `work <command>` commits the change it makes to a work-item or a capability-proposal on the current branch
    Pins that what `work add`, `work retry`, `work withdraw` and `work answer` write, the work-item's or the capability-proposal's file and any log line, is in the branch's history when they end, so nothing that puts .shop/work/ back to its last commit undoes it.
    Given <given>
    And the repository is a git repository on the branch main, everything in it committed
    When the session runs `work <args>`
    Then main has a new last commit, which holds <holds>
    And nothing under .shop/work/ differs from main's last commit

    Examples:
      | command  | given                                                                                          | args                                                                        | holds                                                                                                     |
      | add      | an initiative i1 under .shop/work/ with no work-item w1                                        | add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1 | .shop/work/i1/w1.md as work left it                                                                       |
      | retry    | an initiative i1 under .shop/work/ with a work-item w1 that failed in its implementation stage | retry w1                                                                    | .shop/work/i1/w1.md as work left it and .shop/work/i1/log.jsonl with w1's transition from failed as its last line    |
      | withdraw | an initiative i1 under .shop/work/ whose work-item w1 is ready, its last log.jsonl line for w1 its transition to ready | withdraw w1                                                  | .shop/work/i1/w1.md as work left it and .shop/work/i1/log.jsonl with w1's transition from ready to withdrawn as its last line |
      | answer   | an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by an implementer | answer w1 "Use the first reading"                       | .shop/work/i1/w1.md as work left it and .shop/work/i1/log.jsonl with w1's transition from awaiting-answer to ready as its last line |
      | answer   | an initiative i1 under .shop/work/ whose capability-proposal p1 is awaiting-answer             | answer p1 "Use the first reading"                                           | .shop/work/i1/p1.md as work left it                                                                       |

  @r13
  Scenario: answer on an awaiting-answer work-item writes the answer with the date under the work-item's Answers
    Pins that the person's answer is kept in the work-item's file, dated, under its `## Answers`.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer
    When the session runs `work answer w1 "Use the first reading"`
    Then .shop/work/i1/w1.md has under its `## Answers` the text "Use the first reading", with the date the command was run

  @r24
  Scenario: answer on an awaiting-answer capability-proposal writes the answer with the date under the proposal's Answers
    Pins that the person's answer to a capability-proposal's question is kept in the proposal's file, dated, under its `## Answers`.
    Given an initiative i1 under .shop/work/ whose capability-proposal p1 is awaiting-answer
    When the session runs `work answer p1 "Use the first reading"`
    Then .shop/work/i1/p1.md has under its `## Answers` the text "Use the first reading", with the date the command was run

  @r14 @deprecated
  Scenario Outline: answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)
    Deprecated for: answer to a researcher's, a planner's or an implementer's question transitions the work-item to the status that stage started from
    Pins that an answer returns the work-item to the stage that asked, whichever stage that was.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by <asker>
    When the session runs `work answer w1 "Use the first reading"`
    Then .shop/work/i1/w1.md gives w1's status as <status>

    Examples:
      | asker              | status     |
      | a researcher       | drafted    |
      | a planner          | researched |
      | an implementer     | ready      |
      | a reviewer         | done       |

  @r14
  Scenario Outline: answer to a researcher's, a planner's or an implementer's question transitions the work-item to the status that stage started from
    Pins that an answer returns the work-item to the stage that asked, for each of the three stages before review.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by <asker>
    When the session runs `work answer w1 "Use the first reading"`
    Then .shop/work/i1/w1.md gives w1's status as <status>
    And it exits successfully

    Examples:
      | asker          | status     |
      | a researcher   | drafted    |
      | a planner      | researched |
      | an implementer | ready      |

  @r26
  Scenario: answer that asks for a change, to a reviewer's question, transitions the work-item to ready
    Pins that a person who wants the reviewed work changed sends the work-item back to implementation.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by a reviewer
    When the session runs `work answer w1 "Rename the flag"`, saying that the answer asks for a change
    Then .shop/work/i1/w1.md gives w1's status as ready
    And it exits successfully

  @r27
  Scenario: answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item to done
    Pins that a person who accepts the reviewed work as it stands ends the work-item's review.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by a reviewer
    When the session runs `work answer w1 "Keep it as it is"`, saying that the answer accepts the work-item as it is
    Then .shop/work/i1/w1.md gives w1's status as done
    And it exits successfully

  @r28
  Scenario: answer to a reviewer's question that says neither whether it asks for a change nor whether it accepts the work-item is refused, and nothing changes
    Pins that an answer to a reviewer is never taken without saying which way it goes, and leaves the work-item awaiting its answer.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by a reviewer
    When the session runs `work answer w1 "Use the first reading"`, saying neither that the answer asks for a change nor that it accepts the work-item as it is
    Then work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item as it is
    And .shop/work/i1/w1.md and .shop/work/i1/log.jsonl are as they were

  @r15
  Scenario Outline: answer with a line break in it is refused, and nothing changes
    Pins that an answer is one line whichever kind of line break would make it two, so that each answer stays one bullet under `## Answers`.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer
    When the session runs `work answer w1` with an answer of two lines broken by <line break>
    Then work exits with an error, saying that an answer is one line
    And .shop/work/i1/w1.md and .shop/work/i1/log.jsonl are as they were

    Examples:
      | line break                          |
      | a newline                           |
      | U+000B, the vertical tab            |
      | U+000C, the form feed               |
      | U+000D, the carriage return         |
      | U+0085, the next-line control       |
      | U+2028, the line separator          |
      | U+2029, the paragraph separator     |

  @r15
  Scenario: an answer of two lines to a work-item not awaiting-answer is refused as more than one line first
    Pins the person's ruling that, of several reasons to refuse an answer, the one-line refusal comes first.
    Given an initiative i1 under .shop/work/ whose work-item w1 is ready
    When the session runs `work answer w1` with an answer of two lines broken by a newline
    Then work exits with an error, saying that an answer is one line
    And .shop/work/i1/w1.md and .shop/work/i1/log.jsonl are as they were

  @r16
  Scenario: status of an initiative prints where it stands, for a session to start from
    Pins what status gives a session about one initiative: its proposals and work-items with their statuses and open questions, whether its branch is pushed, the checkout's uncommitted and untracked files, the ledger's last ten lines and its last next: note.
    Given an initiative i1 under .shop/work/ that is neither done nor abandoned, whose capability-proposal p1 is approved
    And i1's work-item w1 is ready, and its work-item w2 is awaiting-answer with the question "Which reading of r3?" not yet answered
    And the repository is a git repository whose initiative branch i1-delivery has one commit the remote does not have
    And the tracked file spec/index.md has uncommitted changes
    And notes.txt is untracked and git does not ignore it
    And scratch.log is untracked and git ignores it
    And .shop/work/i1/ledger.md has twelve lines, each written by `work note` with its date, whose notes are in turn "next: plan w1", "planned w1", eight notes that do not begin next:, "next: answer w2" and "w1 ready"
    When the session runs `work status i1`
    Then work prints i1's status
    And it prints p1 with approved, w1 with ready and w2 with awaiting-answer and the question "Which reading of r3?"
    And it prints i1-delivery and that the remote does not have every commit of it
    And it prints spec/index.md and notes.txt, and nothing about scratch.log
    And it prints the ledger's last ten lines, the eight notes, "next: answer w2" and "w1 ready", and neither of its first two lines
    And it prints the ledger's line whose note is "next: answer w2" as its last line whose note begins next:
    And it exits successfully

  @r17
  Scenario: status with no initiative prints each initiative that is neither done nor abandoned
    Pins which initiatives status reads when it is given none: every open one, and none that has ended.
    Given an initiative i1 under .shop/work/ that is neither done nor abandoned, whose work-item w1 is drafted
    And an initiative i2 under .shop/work/ that is neither done nor abandoned, whose work-item w2 is ready
    And an initiative i3 under .shop/work/ that is done, whose work-item w3 is green
    And an initiative i4 under .shop/work/ that is abandoned, whose work-item w4 is withdrawn
    When the session runs `work status`
    Then work prints what `work status i1` prints and what `work status i2` prints
    And it prints nothing about i3 or i4

  @r18
  Scenario: status with --json prints its result as one JSON object
    Pins that status's result, read by a script, is one JSON object and nothing besides.
    Given an initiative i1 under .shop/work/ that is neither done nor abandoned, whose work-item w1 is drafted
    When the session runs `work status i1 --json`
    Then work prints one JSON object and nothing else
    And it gives i1's status and w1 with drafted

  @r19
  Scenario: note appends the line, with the date, to the initiative's ledger
    Pins that a note is kept, dated, as the ledger's new last line, and that earlier lines stay.
    Given an initiative i1 under .shop/work/ whose ledger .shop/work/i1/ledger.md has one line
    When the session runs `work note i1 "next: plan w2"`
    Then .shop/work/i1/ledger.md has two lines, the first as it was
    And its last line has the text "next: plan w2", with the date the command was run

  @r20
  Scenario: note commits the ledger on the current branch
    Pins that what note writes is in the branch's history when it ends, so nothing that puts .shop/work/ back to its last commit undoes it.
    Given an initiative i1 under .shop/work/ whose ledger .shop/work/i1/ledger.md has one line
    And the repository is a git repository on the branch main, everything in it committed
    When the session runs `work note i1 "next: plan w2"`
    Then main has a new last commit, which holds .shop/work/i1/ledger.md as work left it
    And nothing under .shop/work/ differs from main's last commit

  @r21
  Scenario Outline: note with a line break in it is refused, and nothing changes
    Pins that a note is one line whichever kind of line break would make it two, so that each note stays one line of the ledger.
    Given an initiative i1 under .shop/work/ whose ledger .shop/work/i1/ledger.md has one line
    And the repository is a git repository on the branch main, everything in it committed
    When the session runs `work note i1` with a line of two lines broken by <line break>
    Then work exits with an error, saying that a note is one line
    And .shop/work/i1/ledger.md is as it was
    And main's last commit is the one it was

    Examples:
      | line break                          |
      | a newline                           |
      | U+000B, the vertical tab            |
      | U+000C, the form feed               |
      | U+000D, the carriage return         |
      | U+0085, the next-line control       |
      | U+2028, the line separator          |
      | U+2029, the paragraph separator     |

  @r30
  Scenario Outline: answer named by its initiative answers the <kind> <name> of that initiative
    Pins that an answer given as <initiative>/<name> goes to the work-item or capability-proposal of that name in that initiative, and to nothing in any other initiative, even one with a capability-proposal of the same name.
    Given an initiative i1 under .shop/work/ whose <other> is awaiting-answer
    And an initiative i2 under .shop/work/ whose <kind> <name> is awaiting-answer
    When the session runs `work answer i2/<name> "Use the first reading"`
    Then .shop/work/i2/<name>.md has under its `## Answers` the text "Use the first reading", with the date the command was run
    And .shop/work/i1/ is as it was
    And it exits successfully

    Examples:
      | kind                | name | other                  |
      | capability-proposal | p1   | capability-proposal p1 |
      | work-item           | w2   | work-item w1           |
