"""Handlers of features/design-model-check.feature for the commands that write a file form (b41): `model forms`, which
prints every file form, and `work record`, which writes a record and its index row and commits them. What `work`
wrote and committed is read back by work_queue_handlers' Thens (a record is `.shop/records/<date>-<slug>.md`)."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
H = shared("shop_design_model_check_handlers", "design_model_check_handlers.py")
local = W.local


@handler("WhenRuns", "`model forms`")
def model_forms(step):
    H.run_model(step, "forms")
    step.context["forms_run"] = True


@local("ThenPrints", "file form")
def prints_every_form(step):
    """Every file form of the table, each on its line with its path pattern and what writes it."""
    if not step.context.get("forms_run"):
        return False
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import model_forms as F
    done = step.context["result"]
    lines = done.stdout.splitlines()
    for form in F.FORMS:
        assert any(form.name in line and form.path in line and form.writer in line for line in lines), \
            (form, done.stdout)


@handler("WhenRuns", "`work record`")
def work_record(step):
    """`work record` in the repository, committed first, with a title, a kind, the index row's text and a body kept
    outside the repository."""
    H.base(step.repo, step.context)
    step.context["head"] = W.init(step.repo)
    body = step.fixtures("tmp_path_factory").mktemp("body") / "body.md"
    body.write_text("What was found.\n")
    step.context["result"] = step.run("work", "record", "What was found", "--kind", "analysis", "--summary",
                                      "what was found, in one row", "--body", str(body))
