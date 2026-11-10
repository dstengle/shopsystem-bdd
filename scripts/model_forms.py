"""`model forms` (capability design-model-check r55): every file form a bounded context keeps, with its path pattern
and the command that writes it, so that a session writes a file by its command and never copies one to learn its
form. A form no command writes yet names the item of the plugin's backlog that will give it one, or says it is
written by hand."""
import json
from typing import NamedTuple

SCRIPTS = ("work", "model", "measure", "features", "migrate", "tools")


class Form(NamedTuple):
    name: str
    path: str
    writer: str

    @property
    def command(self):
        """The command line that writes the form (`work idea` as ["work", "idea"]), or None when none does yet."""
        words = self.writer.split()
        return words if words and words[0] in SCRIPTS else None


FORMS = [
    Form("item", ".shop/backlog/b<n>.md", "work idea"),
    Form("item's requirement line", ".shop/backlog/b<n>.md ## Requirements", "work line"),
    Form("item's term bullet", ".shop/backlog/b<n>.md ## Requirements", "work line --term"),
    Form("requirement line in spec", "spec/capabilities/<name>.md ## Behaviour", "work batch start"),
    Form("batch plan", ".shop/batches/<n>/plan.md", "work batch start"),
    Form("review record", ".shop/batches/<n>/review-<k>.md", "work batch reviewed"),
    Form("defect", ".shop/batches/<n>/defect-<k>.md", "measure defect"),
    Form("batch measurement", ".shop/records/measurements/<date>-<batch>.md", "measure batch"),
    Form("request", ".shop/requests/q<n>.md", "work request"),
    Form("quote", ".shop/quotes/<n>.md", "work quote"),
    Form("design-decision", "spec/decisions/<nnnn>-<slug>.md", "work decision"),
    Form("decisions index", "spec/decisions/index.md", "model decisions"),
    Form("rule catalogue", "grammar/rules.md", "model rules --write"),
    Form("record", ".shop/records/<date>-<slug>.md", "work record"),
    Form("records index row", ".shop/records/README.md", "work record"),
    Form("feature", "features/<capability>.feature", "features generate"),
    Form("plugin version", ".shop/plugin-version", "migrate upgrade"),
    Form("restated ids", "spec/restated.json", "migrate upgrade"),
    Form("capability", "spec/capabilities/<name>.md", "plugin item b13 (no command yet)"),
    Form("glossary term", "spec/index.md ## Glossary", "plugin item b13 (no command yet)"),
    Form("relation row", "spec/capabilities/<name>.md ## Relations", "work line --relation"),
    Form("glossary relation row", "spec/index.md ## Relations", "plugin item b13 (no command yet)"),
    Form("universal condition", "spec/universal.md", "work line --universal"),
    Form("upstream entry", "spec/index.md ## Upstreams", "work line --upstream"),
    Form("given block", "spec/capabilities/<name>.md, a group's fenced given", "work line --given"),
    Form("observation", ".shop/records/observations.md ## <id>", "by hand (no command yet)"),
    Form("delivery settings", ".shop/delivery.toml", "by hand (no command yet)"),
]


def cmd_forms(args):
    """Each form on its line, `<name>  <path>  <writer>` in columns; with --json one object {"forms": [...]}."""
    if args.json:
        print(json.dumps({"forms": [form._asdict() for form in FORMS]}))
        return 0
    name = max(len(f.name) for f in FORMS)
    path = max(len(f.path) for f in FORMS)
    for form in FORMS:
        print("%-*s  %-*s  %s" % (name, form.name, path, form.path, form.writer))
    return 0
