"""The scenario repository of features/backlog.feature (not a handler module, so the glob does not load it): items
written as files of `.shop/backlog/`, the scenario's item `i<n>` kept as the file `b<n>` (plan 2, D14), and `work`
run in the repository committed first.

An item the scenario names that no Given wrote is written before the command runs (D15): `idea`, `own`, rated
`medium-value`, `medium-urgency`, `medium`, titled `Title of i<n>`. Under `work idea` the item a Then names is the
one the command writes, so nothing is written for it. backlog_handlers.py loads this module by path as
`shop_backlog_world`."""
import re
import sys
from pathlib import Path

BACKLOG = ".shop/backlog"
INDEX = "---\nid: bounded-context/ex.com/prod/ctx\n---\n# ctx\n"
DEFAULTS = {"status": "idea", "provenance": "own", "value": "medium-value", "urgency": "medium-urgency",
            "size": "medium"}
QUESTION = "Which reading holds, the first or the second?"


def W():
    return sys.modules["shop_work_queue_world"]


def ident(name):
    """The item file's name of the scenario's item: `i3` is `b3`."""
    return "b" + re.sub(r"^\D+", "", name)


def item_rel(context, name):
    return context.get("items", {}).get(name)


def fields_of(step, name):
    """The frontmatter fields of an item the scenario wrote, as written."""
    rel = item_rel(step.context, name)
    return {k: W().field(step.repo / rel, k) for k in ("status", *DEFAULTS)} if rel else None


def index(step):
    """spec/index.md, which names the context an item's id is in, written once."""
    path = step.repo / "spec" / "index.md"
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(INDEX)


def write_item(step, name, **fields):
    """Write (or write again) the item `name`: D15's defaults, the fields it had, then `fields`; `sections` (heading ->
    text) are written after the `## Question`, and `request` as a frontmatter line `request: q<n>` (plan 3)."""
    index(step)
    had = step.context.setdefault("item_fields", {}).setdefault(name, dict(DEFAULTS, depends_on=[],
                                                                          title="Title of %s" % name))
    had.update(fields)
    b = ident(name)
    rel = "%s/%s.md" % (BACKLOG, b)
    head = "".join("%s: %s\n" % (k, had[k]) for k in DEFAULTS)
    tail = "request: %s\n" % had["request"] if had.get("request") else ""
    body = "\n## Question\n\n%s\n" % QUESTION if had["status"] == "needs-input" else ""
    body += "".join("\n## %s\n\n%s\n" % kv for kv in had.get("sections", {}).items())
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: item/ex.com/prod/ctx/%s\nkind: item\n%sdepends_on: [%s]\n%s---\n\n# %s\n%s"
                    % (b, head, ", ".join(had["depends_on"]), tail, had["title"], body))
    step.context.setdefault("items", {})[name] = rel
    step.context.setdefault("says", {})[name] = '%s "%s"' % (b, had["title"])   # what `work` names it by (goal 10)
    return path


def ensure_items(step):
    """Before the command runs: write every item the scenario names that no Given wrote (D15), complete a dependency
    given by one half with the world's own item, and give each item a Given made blocked a dependency on an item
    that is not `delivered` (one of the world's own where it has none), and one made not blocked none."""
    for text in W().scenario_texts(step):
        for name in re.findall(r"\bthe item (i\d+)\b", text):
            if not item_rel(step.context, name):
                write_item(step, name)
    for dep in step.context.get("deps", {}).values():
        for half, own in (("on", OWN), ("of", OWN_NEEDING)):
            if dep.get(half) is None:
                write_item(step, own, title=OWN_TITLE)
                dep[half] = own
        add_dependency(step, dep)
    for name, blocked in step.context.get("blocked", {}).items():
        had = step.context["item_fields"][name]["depends_on"]
        open_ = [d for d in had if status_of(step, d) != "delivered"]
        if blocked and not open_:
            write_item(step, OWN, title=OWN_TITLE)
            write_item(step, name, depends_on=had + [ident(OWN)])
        elif not blocked and open_:
            write_item(step, name, depends_on=[d for d in had if d not in open_])


def status_of(step, b):
    """The status of the item file `b<n>`, or None when there is none."""
    path = step.repo / BACKLOG / ("%s.md" % b)
    return W().field(path, "status") if path.is_file() else None


def add_dependency(step, dep):
    """Write the dependency `dep` ({"of": needing item, "on": item}) into its needing item, once."""
    if dep.get("of") is None or dep.get("on") is None:
        return
    if not item_rel(step.context, dep["of"]):
        write_item(step, dep["of"])
    had = step.context["item_fields"][dep["of"]]["depends_on"]
    if ident(dep["on"]) not in had:
        write_item(step, dep["of"], depends_on=had + [ident(dep["on"])])


def heading_of(stdout, line):
    """The state of the `## <state> (<n>)` table a row of `work backlog` lies under."""
    state = None
    for each in stdout.splitlines():
        if each.startswith("## "):
            state = each[3:].split(" (")[0]
        if each == line:
            return state
    return None


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)][1:-1]


def run_work(step, *args, **kwargs):
    """Run `work` in the repository, committed first; keep the result and the commit it started from. `kwargs` go to
    the run (`stdin`, `timeout`)."""
    index(step)
    if args[0] != "idea":
        ensure_items(step)
    step.context["head"] = W().init(step.repo)
    step.context["result"] = step.run("work", *args, **kwargs)
    return step.context["result"]


def row(stdout, name):
    """The table line of `work backlog` whose item cell is the scenario's item `name`, or None."""
    for line in stdout.splitlines():
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)]
        if len(cells) > 2 and cells[2] == ident(name):
            return line
    return None


def title_of(step, name):
    """The `# ` heading of an item's file."""
    text = (step.repo / item_rel(step.context, name)).read_text()
    return re.search(r"^# (.*)$", text, re.MULTILINE).group(1)


def bare(word):
    return word.strip("`")


def changed(step):
    runs = W().runs(step)
    assert runs, "no command ran"
    return runs[-1]["changed"]


def is_item_file(rel):
    return re.fullmatch(r"\.shop/backlog/b[1-9]\d*\.md", rel) is not None


def bind_written(step, name):
    """The file the last run wrote for the item `name`; an item the scenario has not written yet (the trace's name
    for what the command writes) is bound to the item file the run wrote."""
    files = [rel for rel in changed(step) if is_item_file(rel)]
    rel = item_rel(step.context, name)
    if rel is None and files:
        rel = step.context.setdefault("items", {})[name] = files[0]
    assert rel in files, (step.text, files)
    return rel


def in_commits(step, rel):
    head = step.context.get("head")
    assert W().head(step.repo) != head, "no commit was made: %s" % step.text
    files = W().git(step.repo, "diff", "--name-only", head, "HEAD").split()
    assert rel in files, (step.text, files)


def item_file(step, name):
    return Path(step.repo) / item_rel(step.context, name)


# The world's own item, which a dependency the scenario does not set up is on.
OWN = "i90"
OWN_NEEDING = "i91"
OWN_TITLE = "an item the scenario does not name"


def depends_on(path):
    """The `depends_on` of an item's file, as names."""
    return re.findall(r"b[1-9]\d*", W().field(path, "depends_on") or "")


def name_of(context, rel):
    """The scenario's name of the item whose file is `rel`."""
    return next((n for n, r in context.get("items", {}).items() if r == rel), None)
