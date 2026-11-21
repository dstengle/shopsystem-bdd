"""upgrades' ignore file of a founding (b470, r39, r40), each handler a `local` of work_queue_world's table taken
before migration-tools' own: "the ignore file i1 conforms to the ignore file form" writes into the given block one
that names every ignored name as git matches its lines (a leading or a trailing slash no other entry), unless the
block holds one already; "... does not conform ..." one that lacks some of them; the Then that `migrate init` did
not change it reads it byte for byte, out of its one commit and out of what it printed."""
import re

from scenarios import migration_tools_handlers as M

local = M.local
IGNORE = ".gitignore"
CONFORMING = ".venv\n/__pycache__/\n.pytest_cache/\n.ruff_cache\n"
LACKING = "*.log\n.venv\n"      # the interpreter, but no cache
FORM = re.compile(r"the ignore file \w+ (conforms|does not conform) to the ignore file form$")


def mine(step):
    return M.migration(step) and any(re.sub(r"^(the|a|an|this) ", "", np).startswith("ignore file ")
                                     for np in step.nps)


@local("GivenDoes")
@local("GivenDoesNot")
def conforms(step):
    found = FORM.match(step.text) if M.migration(step) else None
    if found is None:
        return False
    M.held(step).setdefault(IGNORE, CONFORMING if found.group(1) == "conforms" else LACKING)
    return None


@local("ThenDoesNot")
def unchanged(step):
    if not mine(step) or step.term != "change":
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert M.read(step, IGNORE) == M.held(step)[IGNORE], M.read(step, IGNORE)
    old = step.context["old"]
    files = old.git("show", "--name-only", "--format=", "HEAD").stdout.split()
    assert IGNORE not in files, files
    assert old.git("status", "--porcelain").stdout == "", old.git("status", "--porcelain").stdout
    assert IGNORE not in M.said(step), M.said(step)
    return None
