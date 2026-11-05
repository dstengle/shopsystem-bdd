"""batch-measurement's world: the repository a scenario runs `measure show` and `measure compare` in, and the run of
it, in-process, on the scenario's date. What it built for `measure initiative` went with that command (plan 9)."""
import importlib.machinery
import importlib.util
import json
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"

DAY = "2026-10-22"
INITIATIVE = "i7-cart"
MEASUREMENTS = ".shop/records/measurements"


def load_measure():
    sys.path.insert(0, str(SCRIPTS))
    loader = importlib.machinery.SourceFileLoader("measure_script", str(SCRIPTS / "measure"))
    spec = importlib.util.spec_from_loader("measure_script", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class World:
    """What running `measure` in the repository left."""

    def __init__(self, repo):
        self.repo = repo
        self.today = DAY
        self.called = {}            # a scenario's name of a thing (`t1`) -> the name measure gives it in a refusal
        self.code = None
        self.err = ""
        self.out = ""

    def run(self, monkeypatch, capsys, *args):
        """measure's main, in the repository, on the scenario's day; leaves its exit code and what it printed."""
        script = load_measure()
        import measure_write
        monkeypatch.setattr(measure_write, "today", lambda: self.today)
        monkeypatch.chdir(self.repo)
        monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(self.repo / "claude-store"))
        (self.repo / "spec").mkdir(exist_ok=True)
        (self.repo / "spec" / "index.md").write_text("---\nid: bounded-context/ex.com/prod/ctx\n---\n")
        self.code = script.main(list(args))
        seen = capsys.readouterr()
        self.out, self.err = seen.out, seen.err

    def record(self, date=None):
        return self.repo / MEASUREMENTS / ("%s-%s.md" % (date or self.today, INITIATIVE))

    def figures(self):
        """The measurement's figures: the JSON block of the record."""
        text = self.record().read_text()
        return json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
