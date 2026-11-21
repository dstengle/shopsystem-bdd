"""`model forms` (capability design-model-check r55): every file form a bounded context keeps, with its path pattern
and the command that writes it, so that a session writes a file by its command and never copies one to learn its
form. A form no command writes yet names the item of the plugin's backlog that will give it one, or says it is
written by hand; `model forms --check` refuses a form written by hand (design-model-check r324)."""
import json
import sys
from typing import NamedTuple

SCRIPTS = ("work", "spec", "measure", "features", "migrate", "tools")


class Form(NamedTuple):
    name: str
    path: str
    writer: str

    @property
    def command(self):
        """The command line that writes the form (`work idea` as ["work", "idea"]), or None when none does yet."""
        words = self.writer.split()
        return words if words and words[0] in SCRIPTS else None

    @property
    def kind(self):
        """What writes the form: `command`, `item` (the plugin item that will give it one) or `hand`."""
        return "command" if self.command else "item" if self.writer.startswith("plugin item ") else "hand"


FORMS = [
    Form("item", ".shop/backlog/b<n>.md", "work idea"),
    Form("item's requirement line", ".shop/backlog/b<n>.md ## Requirements", "work line"),
    Form("item's chore", ".shop/backlog/b<n>.md ## Chore", "work chore"),
    Form("item's term bullet", ".shop/backlog/b<n>.md ## Requirements", "work line --term"),
    Form("requirement line in spec", "spec/capabilities/<name>.md ## Behaviour", "work batch start"),
    Form("batch plan", ".shop/batches/<n>/plan.md", "work batch start"),
    Form("review record", ".shop/batches/<n>/review-<k>.md", "work batch reviewed"),
    Form("defect", ".shop/batches/<n>/defect-<k>.md", "measure defect"),
    Form("batch measurement", ".shop/records/measurements/<date>-<batch>.md", "measure batch"),
    Form("request", ".shop/requests/q<n>.md", "work request"),
    Form("quote", ".shop/quotes/<n>.md", "work quote"),
    Form("directive", ".shop/directives/<n>.md", "work directive"),
    Form("design-decision", "spec/decisions/<nnnn>-<slug>.md", "work decision"),
    Form("decisions index", "spec/decisions/index.md", "spec decisions"),
    Form("rule catalogue", "grammar/rules.md", "spec rules --write"),
    Form("construct catalogue", "grammar/constructs.md", "spec constructs --write"),
    Form("catalogue entries", "grammar/catalogue-entries.toml", "spec catalogue entry"),
    Form("spec corpus block", "grammar/corpus/spec/<capability>.md", "work batch start"),
    Form("term pack", "spec/packs/<name>.md", "by hand (no command yet)"),
    Form("record", ".shop/records/<date>-<slug>.md", "work record"),
    Form("records index row", ".shop/records/README.md", "work record"),
    Form("feature", "features/<capability>.feature", "features generate"),
    Form("index file", "spec/index.md", "migrate init"),
    Form("universal conditions file", "spec/universal.md", "migrate init"),
    Form("records index", ".shop/records/README.md", "migrate init"),
    Form("plugin version", ".shop/plugin-version", "migrate upgrade"),
    Form("restated ids", "spec/restated.json", "migrate upgrade"),
    Form("capability", "spec/capabilities/<name>.md", "work line --capability"),
    Form("item's model lines", ".shop/backlog/b<n>.md ## Requirements ### <area> model",
         "work line --model"),
    Form("domain model area", "spec/model/<area>.md", "plugin item b398 (no command yet)"),
    Form("vocabulary term", "spec/vocabulary/<area>.md", "plugin item b398 (no command yet)"),
    Form("adapter contract", "spec/adapters/<port>.toml", "work line --expose"),
    Form("adapter contract's requirements", "spec/adapters/<port>.toml, each operation's requirements", "spec annotate"),
    Form("capability moves", "spec/moves.json", "migrate upgrade"),
    Form("universal condition", "spec/universal.md", "work line --universal"),
    Form("upstream entry", "spec/index.md ## Upstreams", "work line --upstream"),
    Form("given block", "spec/capabilities/<name>.md, a group's fenced given", "work line --given"),
    Form("observation", ".shop/records/observations.md ## <id>", "plugin item b475 (no command yet)"),
    Form("delivery settings", ".shop/delivery.toml", "work settings set"),
    Form("design record folder", ".shop/records/<date>-<topic>/design.md", "plugin item b475 (no command yet)"),
    Form("plan record folder", ".shop/records/<date>-<topic>/plan-<k>.md", "plugin item b475 (no command yet)"),
]


def cmd_forms(args):
    """Each form on its line, `<name>  <path>  <writer>` in columns; with --json one object {"forms": [...]}; with
    --check each form written by hand named on stderr and exit 1, else exit 0 and nothing printed."""
    if getattr(args, "check", False):
        hand = [form for form in FORMS if form.kind == "hand"]
        for form in hand:
            print("spec forms: %s (%s) is written by hand: give it a command, or name the plugin item that will"
                  % (form.name, form.path), file=sys.stderr)
        return 1 if hand else 0
    if args.json:
        print(json.dumps({"forms": [dict(form._asdict(), kind=form.kind) for form in FORMS]}))
        return 0
    name = max(len(f.name) for f in FORMS)
    path = max(len(f.path) for f in FORMS)
    for form in FORMS:
        print("%-*s  %-*s  %s" % (name, form.name, path, form.path, form.writer))
    return 0
