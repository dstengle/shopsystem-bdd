# formulated from spec/capabilities/work-queue.md
Feature: Work queue
  Narrator: a person, session or script reading work-items or writing their transitions

  # [r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`.
  @r47
  Scenario: withdraw that leaves every work-item green or withdrawn while a capability-proposal is neither formulated nor withdrawn keeps the initiative started
    Pins that an initiative whose work-items are all green or withdrawn is not ended while one of its capability-proposals is still to be formulated, even with no request holding it open.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    And i1's capability-proposal p1 is formulated and its capability-proposal p2 is approved
    And no request kept in this context names i1
    When the session runs `work withdraw w2`
    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    And .shop/work/i1/initiative.md gives i1's status as started
    And it exits successfully
