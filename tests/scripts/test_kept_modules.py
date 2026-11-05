"""No module that 2.0 keeps imports a module of the old workflow (plan 9 of the workflow simplification): the old
queue, `work run`, `measure initiative` and the hooks' initiative text are deleted one by one, and a kept command must
not break because something it imported went with them."""
import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"

KEPT_GLOBS = ("backlog_*.py", "batch_*.py", "conversation_*.py", "intake_moves.py", "readiness_bar.py", "request_*.py",
              "measure_cost.py", "measure_defect.py", "measure_batch*.py", "measure_show.py", "measure_write.py",
              "transcripts.py", "shop_files.py", "spec_*.py", "features*.py", "tools*.py", "model*.py", "migrate*.py",
              "work_items.py")
KEPT_SCRIPTS = ("work", "measure", "conversation_hook", "model", "features", "tools", "migrate")

OLD = {"workqueue", "workqueue_answer", "workqueue_done", "workqueue_list", "workqueue_note", "workqueue_start",
       "workqueue_status", "measure_build", "measure_read", "stub_claude", "migrate_session", "migrate_prompt"}

def old(name):
    return name in OLD or name.startswith("supervise")


def kept_files():
    files = {p for pattern in KEPT_GLOBS for p in SCRIPTS.glob(pattern)}
    files |= {SCRIPTS / name for name in KEPT_SCRIPTS if (SCRIPTS / name).is_file()}
    files |= {p for p in (REPO / "tests" / "scenarios").glob("*.py")
              if not p.name.startswith(("supervision_", "test_supervision", "test_work_queue", "work_queue_handlers"))}
    return sorted(p for p in files if p.stem not in OLD and not p.stem.startswith("supervise"))


def imported(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            yield node.module.split(".")[0]


def test_no_kept_module_imports_an_old_module():
    found = []
    for path in kept_files():
        rel = path.relative_to(REPO).as_posix()
        for name in sorted(set(imported(path))):
            if old(name):
                found.append("%s imports %s" % (rel, name))
    assert not found, "\n".join(found)
