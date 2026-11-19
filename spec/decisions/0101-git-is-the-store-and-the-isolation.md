---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/git-is-the-store-and-the-isolation
summary: "To keep a thing is one commit of its named files on the branch checked out, to share it is to push to the upstream remote, and a workspace is a branch with its worktree; U13 retires into this decision."
date: 2026-11-19
status: accepted
tier: check
enforced_by: [tests/scripts/test_store_git.py, tests/scripts/test_vocab_u17.py::test_a_kept_commit_not_shared_fails_the_store_check_unless_the_remote_is_unpushable]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u4-is-checked-after-every-scenario-enforced-by-its-test]
---

# 0101. Git is the store and the isolation

## Decision

To keep a thing is one commit of its named files on the branch checked out; to share it is to push that commit to the branch's upstream remote (else origin), never prompting; a workspace is a branch with its worktree. The store's check after every generated scenario (store_git.unshared, which U13's check became) holds a request's kept commit to its upstream remote. U13 retires into this decision.
