# formulated from spec/capabilities/spec-consistency.md
Feature: Spec consistency
  Narrator: the person keeping a spec

  @r1
  Scenario: when the person asks for a consistency pass, model check runs before anything else and its v_t rows are findings
    Pins that the pass starts from what model check already finds, and that those rows reach the person as findings rather than being left out.
    Given model check gives a v_t1 row naming r3 and a v_t2 row naming r7
    When the person asks for a consistency pass
    Then checking-spec-consistency runs model check before it does anything else
    And the pass gives the v_t1 row naming r3 as a finding
    And the pass gives the v_t2 row naming r7 as a finding

  @r2
  Scenario: when the pass starts, it says how many spec-checker dispatches it will make before it dispatches any
    Pins that the person knows the size of the pass, one dispatch a capability and one for the whole context, before any dispatch starts.
    Given a spec with the capabilities orders, payments and refunds
    When the person asks for a consistency pass
    Then checking-spec-consistency says it will make 4 spec-checker dispatches
    And it says so before it dispatches any spec-checker

  @r3
  Scenario: a spec-checker that is dispatched reads only spec/ and features/, never the source
    Pins that a spec-checker judges the spec blind to the code.
    Given a repository with files under spec/, features/ and scripts/
    When checking-spec-consistency dispatches a spec-checker
    Then the spec-checker reads files under spec/ and features/
    And the spec-checker reads no file outside spec/ and features/

  @r4
  Scenario: when a pass in findings mode ends, it has changed nothing but one findings file whose findings name their ids
    Pins that findings mode leaves the spec and the feature files as they were, with every finding written in one file and traceable to its ids.
    Given a consistency pass in findings mode
    And the spec-checkers find a scenario of r3 that shows a status no line asks for
    When the pass ends
    Then the only file the pass changed is one findings file
    And each finding in that file names its ids

  @r28
  Scenario: in fix mode, the pass first proposes a glossary entry for a term cluster and puts it with the line changes that apply it through one gate pass
    Pins that a word used for one thing under several names is settled at the gate as one glossary entry, its avoided words and the lines it rewrites together, with every changed line retired and replaced under a new id.
    Given fix mode is asked for
    And the lines r3 and r7 say cart and the line r5 says basket, for one thing
    When checking-spec-consistency starts fixing
    Then it proposes a glossary entry basket with the Not: word cart
    And it proposes the line changes that say basket in r3 and r7, with r3 and r7 retired and their replacements given new ids
    And it puts the entry and those line changes through one gate pass for the term basket
    And it does so before it rewords any scenario or asks the person any other question

  @r6
  Scenario: in fix mode, once the terms are settled, a scenario using an avoided word is reworded to its line with no further approval
    Pins that a scenario's wording follows its settled line through formulation's small-change path, without the person approving it again.
    Given fix mode is asked for
    And the glossary entry basket with the Not: word cart is settled at the gate
    And the line r9 says basket
    And the scenario of r9 says cart
    When the terms are settled
    Then checking-spec-consistency has the scenario of r9 reworded to say basket, as r9 does, through formulation's small-change path
    And the person is asked for no approval of that rewording

  @r7
  Scenario: in fix mode, a line with two readings becomes one question to the person giving its readings
    Pins that a line with two readings is never decided by the pass: the person is asked once, and the answer goes through integrating-a-proposal's question path.
    Given fix mode is asked for
    And the line r12 has two readings
    When checking-spec-consistency reaches r12
    Then it asks the person one question about r12
    And that question gives both readings of r12
    And the person's answer is integrated through the question path of integrating-a-proposal

  @r8
  Scenario: in fix mode, drift other than a term or a line with two readings is asked about one finding at a time
    Pins that for the rest of the drift the person, not the pass, decides which side is right, and decides them one by one.
    Given fix mode is asked for
    And a finding that the scenario of r4 shows a status r4 does not give
    And a finding that the lines r5 and r6 act on one file without saying which of them wins
    When checking-spec-consistency reaches those findings
    Then it asks the person which side is right for the finding on r4
    And it asks which side is right for the finding on r5 and r6 only after the person has answered about r4

  @r10
  Scenario: when every finding is applied, rejected or written as an observation, fix mode ends with model check printing no v_t row
    Pins that fix mode leaves the spec with no v_t1, v_t2 or v_t3 row once each finding has been dealt with.
    Given fix mode is asked for
    And model check gave a v_t1 row naming r3, found as a finding
    And the finding on the v_t1 row is applied
    And a finding on r5 is rejected
    And a finding on r8 is written as an observation
    When every finding is applied, rejected or written as an observation
    Then checking-spec-consistency ends fix mode
    And model check prints no v_t1, v_t2 or v_t3 row

  @r21
  Scenario: when the pass cannot do what it was asked, it stops, says why and changes nothing
    Pins that a pass that cannot be done leaves the repository as it was and tells the person the reason.
    Given a repository with no spec/ directory
    When the person asks for a consistency pass
    Then the pass is rejected because checking-spec-consistency cannot do what it was asked
    And checking-spec-consistency says why
    And no file is changed

  @r22
  Scenario Outline: a spec-checker writes a finding for a scenario showing behaviour no Behaviour line of its capability asks for
    Pins that observable behaviour a scenario adds beyond its capability's lines is found and traced to its ids.
    Given the capability orders has no Behaviour line that asks for <behaviour>
    And the scenario of r4 in orders shows <behaviour>
    When a spec-checker reads orders and its scenarios
    Then the spec-checker writes a finding for the scenario of r4
    And that finding names r4

    Examples:
      | behaviour                           |
      | an output listing the open orders   |
      | a file written under exports/       |
      | the status shipped                  |

  @r23
  Scenario Outline: a spec-checker writes a finding for two lines that act on one thing without saying which wins
    Pins that two lines acting on one thing with no word on which wins are found, with both their ids.
    Given the line r5 acts on <thing>
    And the line r9 acts on <thing>
    And neither line says which of them wins
    When a spec-checker reads those lines
    Then the spec-checker writes a finding for r5 and r9
    And that finding names r5 and r9

    Examples:
      | thing                    |
      | the file orders.csv      |
      | the status shipped       |
      | the command orders close |

  @r24
  Scenario Outline: a spec-checker writes a finding for a line that leaves to inference which runs, workers or commands it applies to
    Pins that a line whose reach must be guessed is found, with its id.
    Given the line r6 applies to <what> but does not say which
    When a spec-checker reads r6
    Then the spec-checker writes a finding for r6
    And that finding names r6

    Examples:
      | what                  |
      | some runs             |
      | some workers          |
      | some commands         |

  @r25
  Scenario Outline: a spec-checker writes a finding for a scenario that shows another line's response or gives an exit code
    Pins that a scenario shows only the response of the line it names, and that no scenario gives an exit code.
    Given the capability orders has the lines r4 and r8 and the general failure line r21
    And the scenario tagged r4 <shows>
    When a spec-checker reads orders and its scenarios
    Then the spec-checker writes a finding for the scenario of r4
    And that finding names r4

    Examples:
      | shows                                     |
      | shows the response of r8                  |
      | shows the command exiting with an error under r21 |
      | shows the code rejected under r21         |
      | gives an exit code                        |

  @r26
  Scenario Outline: a spec-checker writes a finding for a status or a mode with a way into it or out of it that no line gives
    Pins that every status and mode the lines name is reached and left only by ways a line gives.
    Given the lines name the <kind> <name>
    And the spec shows a way <direction> <name> that no line gives
    When a spec-checker reads the context's Behaviour lines
    Then the spec-checker writes a finding for <name>
    And that finding names the ids of the lines that name <name>

    Examples:
      | kind   | name     | direction |
      | status | shipped  | into      |
      | status | shipped  | out of    |
      | mode   | dry mode | into      |
      | mode   | dry mode | out of    |

  @r27
  Scenario: a spec-checker writes a finding for a word a line depends on that is neither a glossary term nor spelled out in the line
    Pins that a word whose meaning a line relies on is either in the glossary or said in the line itself.
    Given the line r7 depends on the word backorder
    And the glossary has no term backorder
    And r7 does not spell out what a backorder is
    When a spec-checker reads the context's Behaviour lines and the glossary
    Then the spec-checker writes a finding for backorder
    And that finding names r7
