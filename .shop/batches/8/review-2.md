---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-8/review-2
kind: review
batch: batch-8
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/23
head: 5c046d75c0e50cff51ad747ca2b424f0e13d1c6d
range: cd5c94e7c9262a63d5397dfc503a7d44ea454fdf..5c046d75c0e50cff51ad747ca2b424f0e13d1c6d
result: fix-now
---

# batch-8 review 2

## Verdict

The fix for f1 is right: `push_env` now uses the ssh command git would use and only then adds ssh's batch mode, and tests cover each case. One problem remains. The fix's new test file fails ruff, so `tools check` exits 1 at the head where it exited 0 at the base. This is the fix's own change, so it is to fix now.

## Findings

### f6 Important fix now: the fix's test file fails `tools check` (ruff I001)
- item: b56
- where: tests/scripts/test_push_env.py:3
`tools check` exits 1 at the head and exited 0 at the base. The only complaint is in the file commit c7e5f994 adds for f1:

```
tests/scripts/test_push_env.py:3:1: I001 [*] Import block is un-sorted or un-formatted
```

The import block puts `from shop_files import push_env` in its own section after `import pytest`, and the project's isort settings don't accept that. With this run failing, the batch's review checks are no longer clean, and the failure comes from the fix itself.

Fix: on b56's branch, run `ruff check --fix tests/scripts/test_push_env.py` (or group the imports the way the other `tests/scripts/` files do), then confirm `tools check` exits 0.

### f7 Minor observation: the no-setting test depends on the developer's global git config
- item: -
- where: tests/scripts/test_push_env.py:78
The `repo` fixture clears `$GIT_SSH_COMMAND` and `$GIT_SSH` but not the global config. `git config core.sshCommand` also reads `~/.gitconfig`. On a machine where `core.sshCommand` is set globally, `test_no_ssh_setting_runs_ssh_in_batch_mode` expects `ssh -o BatchMode=yes` and gets the global command instead. To reproduce: run `git config --global core.sshCommand "ssh -i k"`, then run the test.

Hardening: in the fixture, set `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. This does not hold the merge.

## Earlier findings
- f1: fixed
