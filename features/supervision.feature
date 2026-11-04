# generated from spec/capabilities/supervision.md by features generate; do not edit
Feature: Supervision
  Narrator: the person who started `work run`

  @g1 @r1
  Scenario: `work run` takes every open work-item to green
    Given a remote r1
    And the remote r1 is not unpushable
    And an initiative i1 that is `started`
    And a work-item w1
    And the work-item w1 is open
    And a work-item w2
    And the work-item w2 is not open
    When the person runs `work run` on the initiative i1
    Then `work run` takes the work-item w1
    And `work run` does not take the work-item w2

  @g2 @r2
  Scenario: A drafted work-item gets a research stage
    Given a work-item w1 that is `drafted`
    And the work-item w1 is not waiting
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `research`
    And the stage s1 is for the work-item w1

  @g3 @r3
  Scenario: A researched work-item gets a plan stage
    Given a work-item w1 that is `researched`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `plan`
    And the stage s1 is for the work-item w1

  @g4 @r4
  Scenario: A ready work-item gets an implement stage
    Given a work-item w1 that is `ready`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `implement`
    And the stage s1 is for the work-item w1

  @g5 @r5
  Scenario: A done work-item gets a review stage
    Given a work-item w1 that is `done`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `review`
    And the stage s1 is for the work-item w1

  @g6 @r6
  Scenario: A worker's stage is logged and starts with a worker brief
    Given a stage s1 that is `research`
    And a work-item w1
    And the stage s1 is for the work-item w1
    When `work run` starts the stage s1
    Then `work run` logs the stage s1
    And `work run` names the transcript t1
    And `work run` gives the stage s1 the worker brief w2
    And the worker brief w2 is for the work-item w1

  @g7 @r7
  Scenario: A stage that gives its output makes the next transition
    Given a stage s1 that is `research`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `plan`
    And the stage s3 is for the work-item w1

  @g8 @r8
  Scenario: An empty file set is a researcher's output
    Given a result r1
    And the result r1 is setless
    And a stage s1 that is `research`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `plan`
    And the stage s3 is for the work-item w1

  @g9 @r9
  Scenario: The outcome a result gives makes no transition
    Given a stage s1 that is `research`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And a result r1 that is `BLOCKED`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `plan`
    And the stage s3 is for the work-item w1

  @g10 @r10
  Scenario: A planner's questions make the work-item await an answer
    Given a stage s1 that is `plan`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And a result r1 that is `QUESTION`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the work-item w1 is `awaiting-answer`
    And `work run` asks the question q1
    And the question q1 is on the work-item w1

  @g11 @r11
  Scenario: A researcher's questions go into the planner's brief
    Given a stage s1 that is `research`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And a result r1 that is `QUESTION`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` gives the stage s3 the question q1
    And the stage s3 is `plan`
    And the stage s3 is for the work-item w1

  @g12 @r12
  Scenario: A result with no output makes the work-item await an answer
    Given a result r1
    And the result r1 is outputless
    And a stage s1 that is `plan`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the work-item w1 is `awaiting-answer`
    And `work run` asks the question q1
    And the question q1 is on the work-item w1

  @g13 @r13
  Scenario: A faulty worker's session fails its work-item
    Given a session s1
    And the session s1 is faulty
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the work-item w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`
    And `work run` exits with an error naming the work-item w1

  @g14 @r14
  Scenario: An implementer's branch with a green check is merged
    Given a work-item branch w1
    And the work-item branch w1 is green check
    And a result r1
    And the result r1 is naming
    And a stage s1 that is `implement`
    And a work-item w2
    And the stage s1 is for the work-item w2
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` merges the work-item branch w1
    And `work run` keeps the report r2

  @g15 @r15
  Scenario: An implementer's branch without a green check is not merged
    Given a work-item branch w1
    And the work-item branch w1 is not green check
    And the work-item branch w1 is not flaky
    And a stage s1 that is `implement`
    And a work-item w2
    And the stage s1 is for the work-item w2
    When the session s2 ends the stage s1
    Then `work run` does not merge the work-item branch w1

  @g16 @r16
  Scenario: A merged work-item branch is deleted
    When `work run` merges the work-item branch w1
    Then `work run` deletes the work-item branch w1

  @g17 @r17
  Scenario: A work-item that awaits an answer keeps its branch
    Given a stage s1 that is `implement`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And a result r1 that is `QUESTION`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` keeps the work-item branch w2

  @g18 @r18
  Scenario: An implementer starts on its kept branch
    Given a work-item w1 that is `ready`
    And a work-item branch w2
    And the work-item branch w2 is kept
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `implement`
    And the stage s1 is on the work-item branch w2

  @g19 @r19
  Scenario: A branch the implementer lost fails the work-item
    Given a work-item branch w1
    And the work-item branch w1 is lost
    And a stage s1 that is `implement`
    And a work-item w2
    And the stage s1 is for the work-item w2
    When the session s2 ends the stage s1
    Then the work-item w2 is `failed`

  @g20 @r20
  Scenario: A flaky scenario is run again before the merge
    Given a work-item branch w1
    And the work-item branch w1 is flaky
    And a stage s1 that is `implement`
    And a work-item w2
    And the stage s1 is for the work-item w2
    When the session s2 ends the stage s1
    Then `work run` reruns the scenario s3
    And `work run` merges the work-item branch w1

  @g21 @r21
  Scenario: A worker that changes `.shop/work/` outside its stage directory fails its work-item
    Given a session s1
    And the session s1 is meddling
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the work-item w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`
    And `work run` restores the file f1

  @g22 @r22
  Scenario: A change left uncommitted in the checkout fails the work-item
    Given a session s1
    And the session s1 is littering
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the work-item w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`

  @g23 @r23
  Scenario: Another initiative's changes are left to it
    Given a session s1
    And the session s1 is crossing
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the work-item w1
    When the session s1 ends the stage s2
    Then `work run` starts the stage s3
    And the stage s3 is `plan`
    And the stage s3 is for the work-item w1

  @g24 @r24
  Scenario: Every transition is committed and pushed, and the worktrees are removed
    Given an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` commits the transition t1
    And `work run` pushes the commit c1
    And `work run` removes the worktree w1

  @g25 @r25
  Scenario: A planner's file set is written into the work-item
    Given a stage s1 that is `plan`
    And a work-item w1
    And the stage s1 is for the work-item w1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` gives the work-item w1 the file set f1

  @g26 @r26
  Scenario: `work run` exits successfully when the initiative's work is closed
    Given an initiative i1 that is `started`
    And a work-item w1
    And the work-item w1 is kept in the initiative i1
    And the work-item w1 is closed
    When the person runs `work run` on the initiative i1
    Then `work run` exits successfully
    And `work run` prints the status of the work-item w1

  @g27 @r27
  Scenario: A work-item awaiting an answer gets no worker, and `work run` exits with an error
    Given an initiative i1 that is `started`
    And a work-item w1
    And the work-item w1 is kept in the initiative i1
    And the work-item w1 is `awaiting-answer`
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the work-item w1
    And `work run` does not start the stage s1

  @g28 @r28
  Scenario: `work run` exits with an error while a failed work-item is left
    Given an initiative i1 that is `started`
    And a work-item w1
    And the work-item w1 is kept in the initiative i1
    And the work-item w1 is `failed`
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the work-item w1
    And `work run` does not start the stage s1

  @g29 @r29
  Scenario: `work run` exits with an error while a request is in its asker's turn
    Given a request q1 that is `asker`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the request q1

  @g30 @r30
  Scenario: `work run` with no initiative takes every open initiative
    Given an initiative i1
    And the initiative i1 is open
    And an initiative i2
    And the initiative i2 is not open
    When the person runs `work run`
    Then `work run` takes the initiative i1
    And `work run` exits successfully
    And `work run` does not take the initiative i2

  @g31 @r31
  Scenario: `work run` with no initiative exits with an error while a node awaits an answer
    Given a work-item w1 that is `awaiting-answer`
    And an initiative i1 that is `started`
    When the person runs `work run`
    Then `work run` exits with an error naming the initiative i1

  @g32 @r32
  Scenario: An initiative branch ahead of its remote is pushed first
    Given a work-item w1 that is `drafted`
    And an initiative branch i1
    And the initiative branch i1 is ahead
    And an initiative i2 that is `started`
    When the person runs `work run` on the initiative i2
    Then `work run` pushes the initiative branch i1

  @g33 @r33
  Scenario: A remote that refuses the push fails the work-item before its worker starts
    Given a work-item w1 that is `drafted`
    And a remote r1
    And the remote r1 is unpushable
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then the work-item w1 is `failed`
    And `work run` does not start the stage s1

  @g34 @r34
  Scenario: A remote that refuses the push starts no branch review
    Given a work-item w1 that is `green`
    And a remote r1
    And the remote r1 is unpushable
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the remote r1
    And `work run` does not start the stage s1

  @g35 @r35
  Scenario: `work run` refuses while `.shop/work/` has uncommitted changes
    Given a file f1
    And the file f1 is dirty
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the file f1
    And `work run` changes nothing

  @g36 @r36
  Scenario: `work run` refuses to be started by a worker
    When the worker w1 runs `work run`
    Then `work run` exits with an error naming the worker w1
    And `work run` changes nothing

  @g37 @r37
  Scenario: `work run` refuses a delivery it cannot start
    Given an initiative branch i1
    And the initiative branch i1 is gitless
    And an initiative i2 that is `started`
    When the person runs `work run` on the initiative i2
    Then `work run` exits with an error naming the reason r1
    And `work run` changes nothing

  @g38 @r38
  Scenario: A work-item blocked by an unfinished work-item gets no worker
    Given a work-item w1 that is `drafted`
    And the work-item w1 is waiting
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` does not start the stage s1

  @g39 @r39
  Scenario: A green initiative branch gets a branch review
    Given an initiative i1 that is `started`
    And a work-item w1
    And the work-item w1 is kept in the initiative i1
    And the work-item w1 is `green`
    And an initiative branch i2
    And the initiative branch i2 is not reviewed
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `branch review`
    And the stage s1 is for the initiative i1
    And `work run` gives the stage s1 the review brief r1
    And the review brief r1 is with the commit c1
    And `work run` commits the stage s1
    And `work run` pushes the commit c2
    And `work run` logs the stage s1

  @g40 @r40
  Scenario: A branch read by a kept review gets no branch review
    Given a work-item w1 that is `green`
    And an initiative branch i1
    And the initiative branch i1 is reviewed
    And an initiative i2 that is `started`
    When the person runs `work run` on the initiative i2
    Then `work run` does not start the stage s1

  @g41 @r41
  Scenario: An initiative with no work-item is neither reviewed nor measured
    Given an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` does not start the stage s1
    And `work run` does not start the stage s2

  @g42 @r42
  Scenario: A branch review's findings to fix now get a work-item
    Given a work-item w1 that is `green`
    And a result r1
    And the result r1 is fixing
    And a stage s1 that is `branch review`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` drafts the work-item w2

  @g43 @r43
  Scenario: A branch review that lists nothing to fix is followed by the analysis
    Given a work-item w1 that is `green`
    And a stage s1 that is `branch review`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `analysis`
    And the stage s3 is for the initiative i1
    And `work run` commits the measurement m1
    And `work run` pushes the commit c1
    And `work run` does not draft the work-item w2

  @g44 @r44
  Scenario: An initiative whose delivery is closed is set done
    Given a work-item w1 that is `green`
    And a capability-proposal p1 that is `formulated`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then the initiative i1 is `done`
    And `work run` commits the initiative i1
    And `work run` pushes the commit c1

  @g45 @r45
  Scenario: An initiative that changes only the glossary is set done
    Given a glossary-proposal p1 that is `approved`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then the initiative i1 is `done`

  @g46 @r46
  Scenario: Under a delegation, a question goes to a session of its own
    Given a delegation d1 that is `written`
    And a work-item w1 that is `awaiting-answer`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `answer`
    And the question q1 is on the work-item w1
    And the stage s1 is for the question q1
    And `work run` names the delegation d1

  @g47 @r47
  Scenario: Under a delegation, a glossary-proposal's question is left for the person
    Given a delegation d1 that is `written`
    And a glossary-proposal p1 that is `awaiting-answer`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` does not start the stage s1

  @g48 @r48
  Scenario: Under a delegation, an answer asking for a change makes the work-item ready
    Given a delegation d1 that is `written`
    And a work-item w1 that is `awaiting-answer`
    And a question q1
    And the question q1 is on the work-item w1
    And the question q1 is `review`
    And an answer a1 that is `--change`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `implement`
    And the stage s1 is for the work-item w1

  @g49 @r49
  Scenario: Under a delegation, an answer accepting the work-item makes it done
    Given a delegation d1 that is `written`
    And a work-item w1 that is `awaiting-answer`
    And a question q1
    And the question q1 is on the work-item w1
    And the question q1 is `review`
    And an answer a1 that is `--accept`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `review`
    And the stage s1 is for the work-item w1

  @g50 @r50
  Scenario: Under a delegation, a faulty answering session leaves the question for the person
    Given a delegation d1 that is `written`
    And a session s1
    And the session s1 is faulty
    And a stage s2 that is `answer`
    And a question q1
    And a work-item w1
    And the question q1 is on the work-item w1
    And the stage s2 is for the question q1
    When the session s1 ends the stage s2
    Then the work-item w1 is `awaiting-answer`
    And `work run` commits the stage s2
    And `work run` pushes the commit c1

  @g51 @r51
  Scenario: A request this context is the upstream of gets an intake round
    Given a request q1 that is `open`
    When the person runs `work run`
    Then `work run` starts the stage s1
    And the stage s1 is `intake`
    And the stage s1 is for the request q1

  @g52 @r52
  Scenario: An intake round's question is written in the request
    Given a stage s1 that is `intake`
    And a request q1
    And the stage s1 is for the request q1
    And a result r1 that is `QUESTION`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` asks the question q2
    And the question q2 is on the request q1
    And the request q1 is `awaiting-asker`

  @g53 @r53
  Scenario: An accepted request gets its initiative
    Given a request q1 that is `accepted`
    And the request q1 is unfulfilled
    When the person runs `work run`
    Then `work run` starts the initiative i1

  @g54 @r54
  Scenario: A proposed initiative gets an integrate round
    Given an initiative i1 that is `proposed`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `integrate`
    And the stage s1 is for the initiative i1
    And `work run` gives the stage s1 the round brief r1
    And the round brief r1 is with the request q1
    And the initiative i1 is `started`

  @g55 @r55
  Scenario: A started initiative with nothing drafted gets an integrate round
    Given an initiative i1 that is `started`
    And the initiative i1 is bare
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `integrate`
    And the stage s1 is for the initiative i1

  @g56 @r56
  Scenario: An integrate round with no change list ends `work run` with an error
    Given a result r1
    And the result r1 is listless
    And a stage s1 that is `integrate`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` exits with an error naming the stage s1

  @g57 @r57
  Scenario: An integrate round's change list drafts a capability-proposal
    Given a stage s1 that is `integrate`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` drafts the capability-proposal p1
    And `work run` commits the draft d1
    And `work run` pushes the commit c1

  @g58 @r58
  Scenario: An integrate round's change to the glossary drafts a glossary-proposal
    Given a result r1
    And the result r1 is glossarial
    And a stage s1 that is `integrate`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` drafts the glossary-proposal p1

  @g59 @r59
  Scenario: An integrate round's lines into an upstream are raised
    Given a result r1
    And the result r1 is raising
    And a stage s1 that is `integrate`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` raises the request q1

  @g60 @r60
  Scenario: A proposal whose raised request is not delivered gets no work-item
    Given a capability-proposal p1 that is `formulated`
    And a result r1
    And the result r1 is awaited
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` does not draft the work-item w1

  @g61 @r61
  Scenario: A change list naming an unknown capability ends `work run` with an error
    Given a result r1
    And the result r1 is strange
    And a stage s1 that is `integrate`
    And an initiative i1 that is `started`
    And the stage s1 is for the initiative i1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` exits with an error naming the capability c1
    And `work run` does not draft the capability-proposal p1

  @g62 @r62
  Scenario: Drafts that do not parse are sent back, then asked about
    Given a result r1
    And the result r1 is unparsing
    And a stage s1 that is `integrate`
    And a capability-proposal p1
    And the stage s1 is for the capability-proposal p1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `integrate`
    And the stage s3 is for the capability-proposal p1
    And the capability-proposal p1 is `awaiting-answer`

  @g63 @r63
  Scenario: A redrafted capability-proposal is drafted again
    Given a stage s1 that is `integrate`
    And a capability-proposal p1
    And the stage s1 is for the capability-proposal p1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the capability-proposal p1 is `drafted`
    And `work run` does not draft the capability-proposal p2

  @g64 @r64
  Scenario: A redrafted glossary-proposal is drafted again
    Given a stage s1 that is `integrate`
    And a glossary-proposal p1
    And the stage s1 is for the glossary-proposal p1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the glossary-proposal p1 is `drafted`

  @g65 @r65
  Scenario: A drafted capability-proposal gets a gate round
    Given a capability-proposal p1 that is `drafted`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `gate`
    And the stage s1 is for the capability-proposal p1
    And `work run` gives the stage s1 the round brief r1

  @g66 @r66
  Scenario: A drafted glossary-proposal gets a gate round
    Given a glossary-proposal p1 that is `drafted`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `gate`
    And the stage s1 is for the glossary-proposal p1
    And `work run` gives the stage s1 the round brief r1

  @g67 @r67
  Scenario: A gate round's questions make the capability-proposal await an answer
    Given a session s1
    And the session s1 is not faulty
    And a stage s2 that is `gate`
    And a capability-proposal p1
    And the stage s2 is for the capability-proposal p1
    And a result r1 that is `QUESTION`
    And the stage s2 is with the result r1
    When the session s1 ends the stage s2
    Then the capability-proposal p1 is `awaiting-answer`
    And `work run` asks the question q1
    And the question q1 is on the capability-proposal p1

  @g68 @r68
  Scenario: A gate round with no question asks for the approval of the lines
    Given a stage s1 that is `gate`
    And a capability-proposal p1
    And the stage s1 is for the capability-proposal p1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` asks the question q1
    And the question q1 is on the capability-proposal p1

  @g69 @r69
  Scenario: A gate round with no question asks for the approval of the terms
    Given a stage s1 that is `gate`
    And a glossary-proposal p1
    And the stage s1 is for the glossary-proposal p1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the glossary-proposal p1 is `awaiting-answer`
    And `work run` asks the question q1
    And the question q1 is on the glossary-proposal p1

  @g70 @r70
  Scenario: An answered capability-proposal gets an apply round
    Given a capability-proposal p1 that is `awaiting-answer`
    And a question q1
    And the question q1 is on the capability-proposal p1
    And the question q1 is answered
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `apply`
    And the stage s1 is for the capability-proposal p1
    And `work run` gives the stage s1 the round brief r1

  @g71 @r71
  Scenario: An answered glossary-proposal gets an apply round
    Given a glossary-proposal p1 that is `awaiting-answer`
    And a question q1
    And the question q1 is on the glossary-proposal p1
    And the question q1 is answered
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` starts the stage s1
    And the stage s1 is `apply`
    And the stage s1 is for the glossary-proposal p1

  @g72 @r72
  Scenario: A glossary-proposal with a question unanswered gets no apply round
    Given a glossary-proposal p1 that is `awaiting-answer`
    And a question q1
    And the question q1 is on the glossary-proposal p1
    And the question q1 is not answered
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` does not start the stage s1

  @g73 @r73
  Scenario: An apply round's answers its drafts do not hold go back to integration
    Given a result r1
    And the result r1 is unheld
    And a stage s1 that is `apply`
    And a capability-proposal p1
    And the stage s1 is for the capability-proposal p1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `integrate`
    And the stage s3 is for the capability-proposal p1
    And `work run` does not start the stage s4

  @g74 @r74
  Scenario: A glossary apply round's answers its drafts do not hold go back to integration
    Given a result r1
    And the result r1 is unheld
    And a stage s1 that is `apply`
    And a glossary-proposal p1
    And the stage s1 is for the glossary-proposal p1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `integrate`
    And the stage s3 is for the glossary-proposal p1

  @g75 @r75
  Scenario: An applied glossary-proposal is approved
    Given a stage s1 that is `apply`
    And a glossary-proposal p1
    And the stage s1 is for the glossary-proposal p1
    And a result r1 that is `DONE`
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the glossary-proposal p1 is `approved`
    And `work run` does not start the stage s3

  @g76 @r76
  Scenario: An applied capability-proposal is formulated by `features generate`
    Given a result r1 that is `DONE`
    And a change list c1
    And the result r1 gives the change list c1
    And the change list c1 is codified
    And a stage s1 that is `apply`
    And a capability-proposal p1
    And the stage s1 is for the capability-proposal p1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then `work run` starts the stage s3
    And the stage s3 is `formulate`
    And the stage s3 is for the capability-proposal p1
    And the capability-proposal p1 is `formulated`
    And `work run` commits the feature f1
    And `work run` pushes the commit c2

  @g77 @r77
  Scenario: A capability that is not codified is the formulate round's fault
    Given a result r1 that is `DONE`
    And a change list c1
    And the result r1 gives the change list c1
    And the change list c1 is uncodified
    And a stage s1 that is `apply`
    And a capability-proposal p1
    And the stage s1 is for the capability-proposal p1
    And the stage s1 is with the result r1
    When the session s2 ends the stage s1
    Then the capability-proposal p1 is `approved`
    And `work run` exits with an error naming the capability c2

  @g78 @r78
  Scenario: A faulty round makes no transition and the initiative's other nodes go on
    Given a session s1
    And the session s1 is faulty
    And a stage s2 that is `gate`
    And a capability-proposal p1
    And the stage s2 is for the capability-proposal p1
    And a work-item w1
    And the work-item w1 is open
    And a work-item w2
    And the work-item w2 is not open
    When the session s1 ends the stage s2
    Then the capability-proposal p1 is `drafted`
    And `work run` exits with an error naming the stage s2
    And `work run` takes the work-item w1
    And `work run` does not take the work-item w2

  @g79 @r79
  Scenario: A formulated capability-proposal gets its work-items
    Given a capability-proposal p1 that is `formulated`
    And an initiative i1 that is `started`
    When the person runs `work run` on the initiative i1
    Then `work run` drafts the work-item w1

  @g84 @r84
  Scenario: An implementer's brief gives its work-item branch
    Given a stage s1 that is `implement`
    And a work-item w1
    And the stage s1 is for the work-item w1
    When `work run` starts the stage s1
    Then `work run` gives the stage s1 the worker brief w2
    And the worker brief w2 is with the work-item branch w3
