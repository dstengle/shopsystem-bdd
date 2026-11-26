---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-106/review-1
kind: review
batch: batch-106
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/129
head: 310e2c23e1dbcd0ff7559e33b48c100b2677f012
range: d1e7fb9dddd033b9942743d7b750d6a8737de0a0..310e2c23e1dbcd0ff7559e33b48c100b2677f012
result: fix-now
---

# batch-106 review 1

## Verdict

b630 is built: the skills, agents, hook and printed hints now say `shop`'s commands, and every run exited 0. b631 is built for most cases, but one finding needs fixing: `tools` runs itself again without passing on the mark that `shop` sets. As a result, `shop tools` can print the notice, and `tools` can print it twice. The size is within the limit (77 files, +353 -243 against 1000).

## Findings

### f1 Important fix now: `tools` re-runs itself without the mark, so `shop tools refs` prints the notice and `tools refs` prints it twice
- item: b631
- where: scripts/tools:98
b631's note asks for one notice on stderr when a command runs by its old name, and none when `shop` runs it. `adapter_cli_respond.notice` takes `SHOPSYSTEM_BY_SHOP` out of `os.environ` at once. Its docstring says "a command that runs itself again passes it on (`marked`)". `model_check.run_again_with_clingo` does pass it on (`{**adapter_cli_respond.marked(), REEXEC: "1"}`). `tools`' `under()` does not:
```python
os.environ["TOOLS_UNDER"] = python
os.execv(python, [python, os.path.abspath(__file__)] + argv)
```
`under()` runs for `tests-of`, `untested`, `refs` and `map --json`, whenever the project's interpreter is not `sys.executable` (for example a `.venv`). The re-run process starts again at `__main__`, finds no mark and prints the notice. So `shop tools refs <name>` prints `tools: now \`shop tools\`; ...`, against "run by shop, none". And `tools refs <name>` prints it twice, against "one notice". `test_old_names.py` only runs `--help`, which never re-runs, so the suite does not catch it.

Fix: in `under()`, run the new process with `os.execve(python, [...], {**adapter_cli_respond.marked(), "TOOLS_UNDER": python})`, or set `os.environ[adapter_cli_respond.BY_SHOP] = "1"` before the `execv`. Add a test that makes `under` re-run (a `--python` that differs from `sys.executable`) and checks the notice appears exactly once for `tools` and never for `shop tools`.

### f2 Minor observation: some printed hints still say the old names
- item: b630
- where: scripts/tools_map.py:989
b630 asks that a refusal's "run ..." hints say `shop`'s commands. A few were missed:
- `Refused("no map: make one with tools map")` at scripts/tools_map.py:989, two lines below the hint the batch did change.
- `work resolve resolves only an accepted request` at scripts/request_moves.py:239.
- `work commits nothing on a task's branch: run it in the base ...` at scripts/shop_files.py:213.

The chore's check only greps skills, agents and hooks, so it cannot catch these. Reproduction: run `shop tools tests-of x` with no map; it says `make one with tools map`.

### f3 Minor observation: CLAUDE.md's module map does not describe the notice, the mark or the new hook command
- item: b631
- where: CLAUDE.md
- The `scripts/adapter_cli_respond.py` row does not name `notice`, `marked` or `BY_SHOP`.
- The `scripts/shop` row does not say that `shop` sets the mark.
- The `hooks/hooks.json` row still says `migrate status --hook`, although the hook now runs `shop migrate status --hook`.
- The working rules still say `work directive`, `work record` and the like.

Neither chore lists `CLAUDE.md` among its files, so the tasks could not update it. The rows should follow, in b633 or in an item that names `CLAUDE.md`.

### f4 Minor observation: tests/conftest.py hides the notice for the whole suite
- item: b631
- where: tests/conftest.py:7
The new conftest sets `SHOPSYSTEM_BY_SHOP=1` for every test process. Every old-name command a scenario or script test runs therefore behaves as if `shop` ran it. This is the technical call b631's note makes (the scenarios keep the old names until b633), and `test_old_names.py` removes the mark to see the notice, so no test is weakened. The cost is that a stray notice from a re-run process, like the `tools` one above, can never show up in any other test. b633 should take the global mark out once the scenarios say `shop`.
