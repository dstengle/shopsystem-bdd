  # [r156] **When** `work run` starts a branch review, `work run` shall give the branch reviewer the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less `.shop/`.
  @r156
  Scenario: the branch reviewer is given the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less .shop/
    Pins that the branch reviewer knows which work-item's work or status each commit commits, sees a commit no work-item made as such, and reads the initiative's change without the workflow's own files.
    Given i1's work-items w1 and w2 are drafted
    And every worker gives DONE, each implementer committing a change to src/<work-item>.py, and while w1's implementer works another session commits notes.txt on the initiative branch
    When the person runs `work run i1`
    Then the branch reviewer's brief gives each commit from the initiative branch's base to its head
    And the branch reviewer's brief gives w1 for w1's implementer's commit, the merge of work/w1 and each commit of a transition of w1, and w2 for w2's in the same way
    And the branch reviewer's brief gives none for the commit of notes.txt
    And the branch reviewer's brief gives the change from the initiative branch's base to its head, holding src/w1.py, src/w2.py and notes.txt and nothing under .shop/
