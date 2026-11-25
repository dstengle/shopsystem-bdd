"""upgrades' old command lines of an instructions file (b632, r44), each handler a `local` of work_queue_world's table,
imported by the glob after migration_tools_handlers_thens so taken before its handlers: "the instructions file i1
holds the old command line o1" writes `CLAUDE.md` into the given block, its old command lines (a backticked one, a
fenced one of two commands) beside a line that only mentions a name; the Thens read it as `migrate upgrade` left it,
each old command line run as `shop <name>`, the mention left alone, and kept in the upgrade's one commit."""
import re

from scenarios import migration_tools_handlers as M

local = M.local
INSTRUCTIONS = "CLAUDE.md"
OLD = """# CLAUDE.md

- Run `work backlog` to see the items, and `model check` before a commit.
- The work of a session is kept as a record; a spec line is never edited.

```bash
spec check && features generate --check
```
"""
NEW = """# CLAUDE.md

- Run `shop work backlog` to see the items, and `shop spec check` before a commit.
- The work of a session is kept as a record; a spec line is never edited.

```bash
shop spec check && shop features generate --check
```
"""
HOLDS = re.compile(r"the instructions file \w+ holds the old command line \w+$")


def mine(step, what):
    return M.migration(step) and any(re.sub(r"^(the|a|an|this) ", "", np).startswith(what + " ") for np in step.nps)


@local("GivenDoes")
def holds(step):
    if not (M.migration(step) and HOLDS.match(step.text)):
        return False
    M.held(step)[INSTRUCTIONS] = OLD
    return None


@local("ThenDoes")
def changed(step):
    """"changes the old command line o1", which the CLI's spelling says "rewrites" (requested's VERBS)."""
    if not mine(step, "old command line"):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert M.read(step, INSTRUCTIONS) == NEW, M.read(step, INSTRUCTIONS)
    return None


@local("ThenDoes")
def kept(step):
    """"keeps the instructions file i1", which the CLI's spelling says "writes": in the upgrade's one commit."""
    if not mine(step, "instructions file") or step.term not in ("write", "commit", "keep"):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert M.read(step, INSTRUCTIONS) == NEW, M.read(step, INSTRUCTIONS)
    old = step.context["old"]
    assert len(old.git("log", "--oneline").stdout.splitlines()) == step.context["commits"] + 1
    files = old.git("show", "--name-only", "--format=", "HEAD").stdout.split()
    assert INSTRUCTIONS in files, files
    assert old.git("status", "--porcelain").stdout == "", old.git("status", "--porcelain").stdout
    return None
