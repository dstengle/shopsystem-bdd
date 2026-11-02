# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # r219: **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge.
  # placed before @r220
  @r219
  Scenario: a scenario whose failure before a merge would keep the work-item branch from being merged is run again once, alone, before the merge is refused
    Pins that one failing run of a scenario is never enough on its own to refuse a work-item's merge: the scenario gets one more run by itself first, and no more than one.
    Given i1's work-item w1 is ready, accepting thing#r1
    And the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE
    And the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch each time it is run
    When the person runs `work run i1`
    Then "it closes" was run once more, alone, after its run with w1's scenarios and before the merge of w1's branch was refused
    And "it closes" was run no other time

  # r222: **When** the second run of a scenario that r219 makes passes, `work run` shall take the scenario as passing in r4's merge of the work-item branch.
  # placed after @r220
  @r222
  Scenario: a scenario that fails before a merge and passes on its second run, alone, lets the work-item branch be merged
    Pins that a scenario that failed once and then passed by itself counts as passing, so the merge goes ahead as if it had passed the first time.
    Given i1's work-item w1 is ready, accepting thing#r1
    And the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE
    And the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch in its run with w1's scenarios and passes there on its second run, alone
    When the person runs `work run i1`
    Then the initiative branch has the implementer's commit of feature.txt
