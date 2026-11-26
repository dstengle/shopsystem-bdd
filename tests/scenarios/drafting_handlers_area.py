"""drafting's capability new on an item placed in the area the person names (drafting r72, b645), or in a driven port
(drafting r85, b701), in a context with a domain model (tests/scripts/fixtures/domain-model/'s spec, whose area `notes`
holds the capability notebook). Each a `local` handler that takes a step of r72's or r85's scenario (`mine`) and
returns False on any other: the capability c1 the new `shelf`, the area a1 the fixture's `notes`, the driven port d1 the
new area `stock`; the item, written at the When, `shaped` with no requirement lines; `work line <item> --capability
shelf --narrator <who> --area notes <purpose>` run on it (`--area stock --port` of the driven port); and the Thens read
the item's `### shelf` block back as committed, its `area:` line naming the area (and its `kind: port` line)."""
import re
import shutil
import sys
from pathlib import Path

W, B = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world"))
local = W.local
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
CAPABILITY, AREA, PORT = "shelf", "notes", "stock"
NARRATOR, PURPOSE = "a person shelving things", "Things kept on a shelf, each found by its name."


def mine(step):
    """True when the step is of drafting's scenario of r72 or r85."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and \
        bool({"r72", "r85"} & set(found.tags))


def _spec(step):
    if not step.context.get("area_spec"):
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        step.context["area_spec"] = True


@local("GivenK")
def given_named(step):
    """a capability c1 (shelf), an area a1 (notes), a driven port d1 (stock): the fixture's spec."""
    if not mine(step) or step.kind not in ("capability", "area", "driven port"):
        return False
    _spec(step)
    return None


@local("WhenRuns")
def draft(step):
    """`work line <item> --capability shelf --narrator <who> --area notes <purpose>` (the request re-keyed by the CLI
    contract); of the driven port, `--area stock --port`."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--capability" not in options:
        return False
    port = "driven port" in step.text
    _spec(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped")
    args = ["--capability", CAPABILITY, "--narrator", NARRATOR] + (["--area", PORT, "--port"] if port else
                                                                   ["--area", AREA] if "--area" in options else [])
    B.run_work(step, "line", B.ident(item), *args, PURPOSE)
    return None


@local("ThenDoes")
def kept(step):
    """the item i1 holds the capability c1, the drafting service keeps it: the item's committed `### shelf` block with
    its narrator, group and purpose; the area a1 holds the capability c1, the drafting service keeps it: that block's
    `area: notes` line, committed with it; the driven port d1 holds it, the drafting service keeps it: `area: stock`
    and `kind: port` after the purpose."""
    if not mine(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    text = W.git(step.repo, "show", "HEAD:%s" % rel)
    block = "### %s\n\nnarrator: %s\ngroup: service\npurpose: %s\n" % (CAPABILITY, NARRATOR, PURPOSE)
    assert block in text + "\n", text
    if "driven port" in step.text:
        assert block + "area: %s\nkind: port\n" % PORT in text + "\n", text
    elif "area" in step.text:
        assert block + "area: %s\n" % AREA in text + "\n", text
    return None
