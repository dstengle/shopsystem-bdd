# generated from spec/capabilities/supervision.md by features generate; do not edit
Feature: Supervision
  Narrator: the person who started `work run`

  @g1 @r1
  Scenario: `work run` takes every open work-item to green
    Given a remote r1
    And the remote r1 is not unpushable
    And an initiative i1
    And a work-item w1 that is `drafted`
    And a work-item w2 that is `green`
    And a work-item w3 that is `withdrawn`
    When the person runs `work run` on the initiative i1
    Then the work-item w1 is `green`
    And the work-item w2 is `green`
    And the work-item w3 is `withdrawn`

  @g2 @r2
  Scenario: A drafted work-item gets a research stage
    Given a work-item w1 that is `drafted`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts a `research` stage for the work-item w1

  @g3 @r3
  Scenario: A researched work-item gets a plan stage
    Given a work-item w1 that is `researched`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts a `plan` stage for the work-item w1

  @g4 @r4
  Scenario: A ready work-item gets an implement stage
    Given a work-item w1 that is `ready`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts an `implement` stage for the work-item w1

  @g5 @r5
  Scenario: A done work-item gets a review stage
    Given a work-item w1 that is `done`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts a `review` stage for the work-item w1

  @g6 @r6 @r7
  Scenario: A worker's stage starts with a worker brief and a tool list
    Given a work-item w1 that is `drafted`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` gives a `research` stage for the work-item w1 a worker brief
    And `work run` gives a `research` stage for the work-item w1 a tool list

  @g7 @r8 @r9
  Scenario: A worker's start and end are logged
    Given a stage s1 that is `research`
    And a work-item w1
    And the stage s1 is for the node w1
    When `work run` starts the stage s1
    Then `work run` logs the stage s1
    And `work run` names a transcript

  @g8 @r10
  Scenario: A stage that gives its output makes the next transition
    Given a session s1
    And a stage s2 that is `research`
    And a result r1 that is `DONE`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` starts a `plan` stage for the work-item w1

  @g9 @r11
  Scenario: An empty file set is a researcher's output
    Given a result r1
    And the result r1 is setless
    And a session s1
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` starts a `plan` stage for the work-item w1

  @g10 @r12
  Scenario: The outcome a result gives makes no transition
    Given a session s1
    And a stage s2 that is `research`
    And a result r1 that is `BLOCKED`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` starts a `plan` stage for the work-item w1

  @g11 @r13 @r14
  Scenario: A planner's questions make the work-item await an answer
    Given a session s1
    And a stage s2 that is `plan`
    And a result r1 that is `QUESTION`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `awaiting-answer`
    And `work run` asks a question on the work-item w1

  @g12 @r15
  Scenario: A researcher's questions go into the planner's brief
    Given a session s1
    And a stage s2 that is `research`
    And a result r1 that is `QUESTION`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` gives a `plan` stage for the work-item w1 a question

  @g13 @r16 @r17
  Scenario: A result with no output makes the work-item await an answer
    Given a result r1
    And the result r1 is outputless
    And a session s1
    And a stage s2 that is `plan`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `awaiting-answer`
    And `work run` asks a question on the work-item w1

  @g14 @r18 @r19
  Scenario: A faulty worker's session fails its work-item
    Given a session s1
    And the session s1 is faulty
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`
    And `work run` exits with an error naming the work-item w1

  @g15 @r20 @r21
  Scenario: An implementer's branch with a green check is merged
    Given a result r1
    And the result r1 is naming
    And a work-item branch w2
    And the work-item branch w2 is green check
    And a session s1
    And a stage s2 that is `implement`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` merges the work-item branch w2
    And `work run` keeps a report

  @g16 @r22
  Scenario: An implementer's branch without a green check is not merged
    Given a work-item branch w2
    And the work-item branch w2 is not green check
    And a session s1
    And a stage s2 that is `implement`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` does not merge the work-item branch w2

  @g17 @r23
  Scenario: A merged work-item branch is deleted
    Given a work-item branch w1
    When `work run` merges the work-item branch w1
    Then `work run` deletes the work-item branch w1

  @g18 @r24
  Scenario: A work-item that awaits an answer keeps its branch
    Given a session s1
    And a stage s2 that is `implement`
    And a result r1 that is `QUESTION`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` keeps the work-item branch

  @g19 @r25
  Scenario: An implementer starts on its kept branch
    Given a work-item branch w2
    And the work-item branch w2 is kept
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts an `implement` stage on the work-item branch w2

  @g20 @r26
  Scenario: A branch the implementer lost fails the work-item
    Given a work-item branch w2
    And the work-item branch w2 is lost
    And a session s1
    And a stage s2 that is `implement`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`

  @g21 @r27 @r28
  Scenario: A flaky scenario is run again before the merge
    Given a work-item branch w2
    And the work-item branch w2 is flaky
    And a session s1
    And a stage s2 that is `implement`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` reruns the scenario
    And `work run` merges the work-item branch w2

  @g22 @r29 @r30
  Scenario: A worker that changes `.shop/work/` outside its stage directory fails its work-item
    Given a session s1
    And the session s1 is meddling
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`
    And `work run` restores the file

  @g23 @r31
  Scenario: A change left uncommitted in the checkout fails the work-item
    Given a session s1
    And the session s1 is littering
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `failed`

  @g24 @r32
  Scenario: Another initiative's changes are left to it
    Given a session s1
    And the session s1 is crossing
    And a stage s2 that is `research`
    And a work-item w1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` starts a `plan` stage for the work-item w1

  @g25 @r33
  Scenario: Every transition is committed and pushed
    Given an initiative i1
    And a transition t1
    When the person runs `work run` on the initiative i1
    Then `work run` commits the transition t1 and pushes the commit

  @g26 @r34
  Scenario: A planner's file set is written into the work-item
    Given a session s1
    And a stage s2 that is `plan`
    And a result r1 that is `DONE`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` gives the work-item w1 the file set

  @g27 @r35 @r36
  Scenario: `work run` exits successfully when the initiative's work is closed
    Given a work-item w1 that is `green`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` exits successfully
    And `work run` prints the status of the work-item w1

  @g28 @r37
  Scenario: `work run` exits with an error while a work-item awaits an answer
    Given a work-item w1 that is `awaiting-answer`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the work-item w1

  @g29 @r38 @r39
  Scenario: `work run` exits with an error while a failed work-item is left
    Given a work-item w1 that is `failed`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the work-item w1
    And `work run` does not start a stage for the work-item w1

  @g30 @r40
  Scenario: `work run` exits with an error while a request is in its asker's turn
    Given a request q1 that is `asker`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the request q1

  @g31 @r41 @r42
  Scenario: `work run` with no initiative takes every open initiative
    Given an initiative i1 that is `proposed`
    And an initiative i2 that is `done`
    And an initiative i3 that is `abandoned`
    When the person runs `work run`
    Then `work run` takes the initiative i1
    And `work run` does not take the initiative i2
    And `work run` does not take the initiative i3
    And `work run` exits successfully

  @g32 @r43
  Scenario: `work run` with no initiative exits with an error while a node awaits an answer
    Given a work-item w1 that is `awaiting-answer`
    And an initiative i1
    When the person runs `work run`
    Then `work run` exits with an error naming the initiative i1

  @g33 @r44
  Scenario: An initiative branch ahead of its remote is pushed first
    Given an initiative branch i2
    And the initiative branch i2 is ahead
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` pushes the initiative branch i2

  @g34 @r45 @r46
  Scenario: A remote that refuses the push fails the work-item before its worker starts
    Given a work-item w1 that is `drafted`
    And a remote r1
    And the remote r1 is unpushable
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then the work-item w1 is `failed`
    And `work run` does not start a stage for the work-item w1

  @g35 @r47 @r48
  Scenario: A remote that refuses the push starts no branch review
    Given a work-item w1 that is `green`
    And a remote r1
    And the remote r1 is unpushable
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` does not start a `branch review` stage for the initiative i1
    And `work run` exits with an error naming the remote r1

  @g36 @r49
  Scenario: `work run` refuses while `.shop/work/` has uncommitted changes
    Given a file `.shop/work/i1/notes.md`
    And the file `.shop/work/i1/notes.md` is dirty
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the file `.shop/work/i1/notes.md`
    And `work run` changes nothing

  @g37 @r50
  Scenario: `work run` refuses to be started by a worker
    Given a worker w1
    When the worker w1 runs `work run`
    Then `work run` exits with an error naming the worker w1
    And `work run` changes nothing

  @g38 @r51
  Scenario: `work run` refuses a delivery it cannot start
    Given an initiative branch i2
    And the initiative branch i2 is gitless
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` exits with an error naming the reason
    And `work run` changes nothing

  @g39 @r52
  Scenario: A work-item awaiting an answer gets no worker
    Given a work-item w1 that is `awaiting-answer`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` does not start a stage for the work-item w1

  @g40 @r53
  Scenario: A work-item blocked by an unfinished work-item gets no worker
    Given a work-item w2 that is `awaiting-answer`
    And a work-item w1 that is `drafted`
    And the work-item w1 is blocked by the work-item w2
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` does not start a stage for the work-item w1

  @g41 @r54 @r55 @r56 @r57
  Scenario: A green initiative branch gets a branch review
    Given a work-item w1 that is `green`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts a `branch review` stage for the initiative i1
    And `work run` gives the `branch review` stage a review brief
    And `work run` commits the `branch review` stage and pushes the commit
    And `work run` logs the `branch review` stage

  @g42 @r58
  Scenario: A branch read by a kept review gets no branch review
    Given a work-item w1 that is `green`
    And an initiative branch i2
    And the initiative branch i2 is reviewed
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` does not start a `branch review` stage for the initiative i1

  @g43 @r59 @r60
  Scenario: An initiative with no work-item is neither reviewed nor measured
    Given an initiative i1
    And the initiative i1 is itemless
    When the person runs `work run` on the initiative i1
    Then `work run` does not start a `branch review` stage for the initiative i1
    And `work run` does not start an `analysis` stage for the initiative i1

  @g44 @r61
  Scenario: A branch review's findings to fix now get a work-item
    Given a result r1
    And the result r1 is fixing
    And a session s1
    And a stage s2 that is `branch review`
    And an initiative i1
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` drafts a work-item

  @g45 @r62 @r63 @r64
  Scenario: A branch review that lists nothing to fix is followed by the analysis
    Given a session s1
    And a stage s2 that is `branch review`
    And a result r1 that is `DONE`
    And an initiative i1
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` does not draft a work-item
    And `work run` starts an `analysis` stage for the initiative i1
    And `work run` commits a measurement and pushes the commit

  @g46 @r65 @r66
  Scenario: An initiative whose delivery is closed is set done
    Given a work-item w1 that is `green`
    And a capability-proposal p1 that is `formulated`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then the initiative i1 is `done`
    And `work run` commits the initiative i1 and pushes the commit

  @g47 @r67
  Scenario: An initiative that changes only the glossary is set done
    Given a glossary-proposal p1 that is `approved`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then the initiative i1 is `done`

  @g48 @r68 @r69
  Scenario: Under a delegation, a question goes to a session of its own
    Given a delegation d1 that is `written`
    And a session s1
    And a stage s2 that is `plan`
    And a result r1 that is `QUESTION`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` starts an `answer` stage for the question
    And `work run` names the delegation d1

  @g49 @r70 @r71
  Scenario: Under a delegation, a glossary-proposal's question is left for the person
    Given a delegation d1 that is `written`
    And a session s1
    And a stage s2 that is `gate`
    And a result r1 that is `QUESTION`
    And a glossary-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then `work run` does not start an `answer` stage for the question
    And the glossary-proposal p1 is `awaiting-answer`

  @g50 @r72
  Scenario: Under a delegation, an answer asking for a change makes the work-item ready
    Given a delegation d1 that is `written`
    And an answer a1 that is `--change`
    And a session s1
    And a stage s2 that is `review`
    And a result r1 that is `QUESTION`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then `work run` starts an `implement` stage for the work-item w1

  @g51 @r73
  Scenario: Under a delegation, an answer accepting the work-item makes it done
    Given a delegation d1 that is `written`
    And an answer a1 that is `--accept`
    And a session s1
    And a stage s2 that is `review`
    And a result r1 that is `QUESTION`
    And a work-item w1
    And the stage s2 is with the result r1
    And the stage s2 is for the node w1
    When the session s1 ends the stage s2
    Then the work-item w1 is `green`

  @g52 @r74 @r75
  Scenario: Under a delegation, a faulty answering session leaves the question for the person
    Given a session s1
    And the session s1 is faulty
    And a delegation d1 that is `written`
    And a stage s2 that is `answer`
    And a question q1
    And a work-item w1
    And the question q1 is on the node w1
    And the stage s2 is for the node q1
    When the session s1 ends the stage s2
    Then the work-item w1 is `awaiting-answer`
    And `work run` commits the stage s2 and pushes the commit

  @g53 @r76
  Scenario: A request this context is the upstream of gets an intake round
    Given a request q1 that is `open`
    When the person runs `work run`
    Then `work run` starts an `intake` stage for the request q1

  @g54 @r77 @r78
  Scenario: An intake round's question is written in the request
    Given a session s1
    And a stage s2 that is `intake`
    And a result r1 that is `QUESTION`
    And a request q1
    And the stage s2 is with the result r1
    And the stage s2 is for the node q1
    When the session s1 ends the stage s2
    Then `work run` asks a question on the request q1
    And the request q1 is `awaiting-asker`

  @g55 @r79
  Scenario: An accepted request gets its initiative
    Given a request q1 that is `accepted`
    When the person runs `work run`
    Then `work run` starts an initiative that fulfils the request q1

  @g56 @r80 @r81 @r82
  Scenario: A proposed initiative gets an integrate round
    Given an initiative i1 that is `proposed`
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    When the person runs `work run` on the initiative i1
    Then `work run` starts an `integrate` stage for the initiative i1
    And `work run` gives the `integrate` stage a round brief
    And the initiative i1 is `started`

  @g57 @r83
  Scenario: A started initiative with nothing drafted gets an integrate round
    Given an initiative i1 that is `started`
    And the initiative i1 is bare
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    When the person runs `work run` on the initiative i1
    Then `work run` starts an `integrate` stage for the initiative i1

  @g58 @r84
  Scenario: An integrate round with no change list ends `work run` with an error
    Given an initiative i1
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    And a result r1
    And the result r1 is listless
    And a session s1
    And a stage s2 that is `integrate`
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` exits with an error naming the stage s2

  @g59 @r85 @r86
  Scenario: An integrate round's change list drafts a capability-proposal
    Given an initiative i1
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    And a session s1
    And a stage s2 that is `integrate`
    And a result r1 that is `DONE`
    And a draft d1
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` drafts a capability-proposal
    And `work run` commits the draft d1 and pushes the commit

  @g60 @r87
  Scenario: An integrate round's change to the glossary drafts a glossary-proposal
    Given an initiative i1
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    And a result r1
    And the result r1 is glossarial
    And a session s1
    And a stage s2 that is `integrate`
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` drafts a glossary-proposal

  @g61 @r88
  Scenario: An integrate round's lines into an upstream are raised
    Given an initiative i1
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    And a result r1
    And the result r1 is raising
    And a session s1
    And a stage s2 that is `integrate`
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` raises a request

  @g62 @r89
  Scenario: A proposal whose raised request is not delivered gets no work-item
    Given a capability-proposal p1 that is `formulated`
    And the capability-proposal p1 is held
    And a request q1 that is `open`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` does not draft a work-item

  @g63 @r90 @r91
  Scenario: A change list naming an unknown capability ends `work run` with an error
    Given an initiative i1
    And a request q1 that is `accepted`
    And the initiative i1 fulfils the request q1
    And a result r1
    And the result r1 is strange
    And a session s1
    And a stage s2 that is `integrate`
    And the stage s2 is with the result r1
    And the stage s2 is for the node i1
    When the session s1 ends the stage s2
    Then `work run` does not draft a capability-proposal
    And `work run` exits with an error naming the capability

  @g64 @r92 @r93
  Scenario: Drafts that do not parse are sent back, then asked about
    Given a result r1
    And the result r1 is unparsing
    And a session s1
    And a stage s2 that is `integrate`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then `work run` starts an `integrate` stage for the capability-proposal p1
    And the capability-proposal p1 is `awaiting-answer`

  @g65 @r94 @r95
  Scenario: A redrafted capability-proposal is drafted again
    Given a session s1
    And a stage s2 that is `integrate`
    And a result r1 that is `DONE`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the capability-proposal p1 is `drafted`
    And `work run` does not draft a capability-proposal

  @g66 @r96
  Scenario: A redrafted glossary-proposal is drafted again
    Given a session s1
    And a stage s2 that is `integrate`
    And a result r1 that is `DONE`
    And a glossary-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the glossary-proposal p1 is `drafted`

  @g67 @r97 @r98
  Scenario: A drafted capability-proposal gets a gate round
    Given a capability-proposal p1 that is `drafted`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts a `gate` stage for the capability-proposal p1
    And `work run` gives the `gate` stage a round brief

  @g68 @r99 @r100
  Scenario: A drafted glossary-proposal gets a gate round
    Given a glossary-proposal p1 that is `drafted`
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts a `gate` stage for the glossary-proposal p1
    And `work run` gives the `gate` stage a round brief

  @g69 @r101 @r102
  Scenario: A gate round's questions make the capability-proposal await an answer
    Given a session s1
    And a stage s2 that is `gate`
    And a result r1 that is `QUESTION`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the capability-proposal p1 is `awaiting-answer`
    And `work run` asks a question on the capability-proposal p1

  @g70 @r103
  Scenario: A gate round with no question asks for the approval of the lines
    Given a session s1
    And a stage s2 that is `gate`
    And a result r1 that is `DONE`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then `work run` asks a question on the capability-proposal p1

  @g71 @r104 @r105
  Scenario: A gate round with no question asks for the approval of the terms
    Given a session s1
    And a stage s2 that is `gate`
    And a result r1 that is `DONE`
    And a glossary-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the glossary-proposal p1 is `awaiting-answer`
    And `work run` asks a question on the glossary-proposal p1

  @g72 @r106 @r107
  Scenario: An answered capability-proposal gets an apply round
    Given a capability-proposal p1 that is `awaiting-answer`
    And the capability-proposal p1 is answered
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts an `apply` stage for the capability-proposal p1
    And `work run` gives the `apply` stage a round brief

  @g73 @r108
  Scenario: An answered glossary-proposal gets an apply round
    Given a glossary-proposal p1 that is `awaiting-answer`
    And the glossary-proposal p1 is answered
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` starts an `apply` stage for the glossary-proposal p1

  @g74 @r109
  Scenario: A glossary-proposal with a question unanswered gets no apply round
    Given a glossary-proposal p1 that is `awaiting-answer`
    And the glossary-proposal p1 is not answered
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` does not start an `apply` stage for the glossary-proposal p1

  @g75 @r110 @r111
  Scenario: An apply round's answers its drafts do not hold go back to integration
    Given a result r1
    And the result r1 is unheld
    And a session s1
    And a stage s2 that is `apply`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then `work run` starts an `integrate` stage for the capability-proposal p1
    And `work run` does not start a `formulate` stage for the capability-proposal p1

  @g76 @r112
  Scenario: A glossary apply round's answers its drafts do not hold go back to integration
    Given a result r1
    And the result r1 is unheld
    And a session s1
    And a stage s2 that is `apply`
    And a glossary-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then `work run` starts an `integrate` stage for the glossary-proposal p1

  @g77 @r113 @r114
  Scenario: An applied glossary-proposal is approved
    Given a session s1
    And a stage s2 that is `apply`
    And a result r1 that is `DONE`
    And a glossary-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the glossary-proposal p1 is `approved`
    And `work run` does not start a `formulate` stage for the glossary-proposal p1

  @g78 @r115 @r116 @r117
  Scenario: An applied capability-proposal is formulated by `features generate`
    Given a change list c1
    And the change list c1 is codified
    And a session s1
    And a stage s2 that is `apply`
    And a result r1 that is `DONE`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then `work run` starts a `formulate` stage for the capability-proposal p1
    And the capability-proposal p1 is `formulated`
    And `work run` commits the feature and pushes the commit

  @g79 @r118 @r119
  Scenario: A capability that is not codified is the formulate round's fault
    Given a change list c1
    And the change list c1 is uncodified
    And a session s1
    And a stage s2 that is `apply`
    And a result r1 that is `DONE`
    And a capability-proposal p1
    And the stage s2 is with the result r1
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the capability-proposal p1 is `approved`
    And `work run` exits with an error naming the capability

  @g80 @r120 @r121 @r122
  Scenario: A faulty round makes no transition and the initiative's other nodes go on
    Given a session s1
    And the session s1 is faulty
    And a stage s2 that is `gate`
    And a capability-proposal p1
    And a work-item w1 that is `drafted`
    And a work-item w2 that is `green`
    And a work-item w3 that is `withdrawn`
    And the stage s2 is for the node p1
    When the session s1 ends the stage s2
    Then the capability-proposal p1 is `drafted`
    And `work run` exits with an error naming the stage s2
    And the work-item w1 is `green`
    And the work-item w2 is `green`
    And the work-item w3 is `withdrawn`

  @g81 @r123
  Scenario: A formulated capability-proposal gets its work-items
    Given a capability-proposal p1 that is `formulated`
    And the capability-proposal p1 is not held
    And an initiative i1
    When the person runs `work run` on the initiative i1
    Then `work run` drafts a work-item

  @g86 @r140
  Scenario: A delivery removes the worktrees it made
    Given an initiative i1
    And a worktree w1
    When the person runs `work run` on the initiative i1
    Then `work run` removes the worktree w1
