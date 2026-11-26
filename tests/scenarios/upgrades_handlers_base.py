"""upgrades' founding that imports the base pack (r45, b609), each handler a `local` of work_queue_world's table
taken before migration-tools' own: "the upgrades service keeps the bounded context b1" the context scaffold
`migrate init` kept in its one commit (upgrades_handlers_found's `scaffolded`), and "the bounded context b1 imports
`base`" the frontmatter `imports:` of the index file it kept naming the pack."""
import re

from scenarios import migration_tools_handlers as M
from scenarios import requested
from scenarios import upgrades_handlers_found as F

local = M.local

IMPORTS = re.compile(r"^imports: \[(?P<names>[^\]]*)\]$", re.MULTILINE)


def context(np):
    return re.sub(r"^(the|a|an|this) ", "", np).startswith("bounded context")


@local("ThenDoes")
def kept(step):
    """the upgrades service keeps the bounded context b1; the bounded context b1 imports `base`."""
    if not M.migration(step):
        return False
    if step.term in requested.KEEPS and step.nps and context(step.nps[0]):
        return F.scaffolded(step)
    if step.term == "import" and step.subject and context(step.subject):
        assert step.context["done"].returncode == 0, M.said(step)
        index = M.read(step, "spec/index.md")
        found = IMPORTS.search(index.partition("\n---\n")[0])
        names = [n.strip() for n in found.group("names").split(",")] if found else []
        assert step.nps[0].strip("`") in names, index
        return None
    return False
