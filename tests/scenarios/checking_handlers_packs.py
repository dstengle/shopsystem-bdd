"""Handlers of checking's scenarios of an imported pack's kinds (r104, r105, b609), each a `work_queue_world.local`
that takes only a step of a scenario of its groups (`mine`). The world is the domain-model fixture
(tests/scripts/fixtures/domain-model/: the notes area, its vocabulary, its CLI contract and the notebook capability),
written at the When:

- g104: the pack p1 the context's own `spec/packs/p1.md`, which spec/index.md imports, its term t1 the noun `binder`
  (a word the fixture does not spell), and the element e1 the relation `refers to → binder` of the note; `spec check`
  run, which passes only when the model reads the pack's kind as declared (v_m8 names none).
- g105: spec/index.md importing the plugin's pack `base`, the terms t1 and t2 the first two nouns of
  grammar/packs/base.md and t3 `note`, the fixture's own; `spec lexicon` run, and each term it shows read off its
  rows `  <term>  [pack base]`.

The Givens keep what they say (`world`); the Thens read the run's exit and output."""
import re
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
BASE = ROOT / "grammar" / "packs" / "base.md"
GROUPS = {"g104", "g105"}
OWN = "binder"
RELATION = "  relations: carries → tag (many)\n"


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("packs", {"kinds": {}, "has": [], "lacks": [], "refers": [], "imports": []})


def base_terms():
    return re.findall(r"^- \*\*([^*]+)\*\* \(noun\)", BASE.read_text() if BASE.is_file() else "", re.MULTILINE)


def given_instance(step):
    """a pack p1, a term t1, an element e1."""
    if not mine(step) or step.kind not in ("pack", "term", "element"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """this bounded context imports the pack p1 (or `base`), the pack p1 (or `base`) has the term t1, the element e1
    refers to the term t1."""
    if not mine(step) or step.term not in ("import", "has", "refer"):
        return False
    w = world(step)
    if step.term == "import":
        w["imports"].append(step.names[0] if step.names else step.nps[0].strip("`"))
    elif step.term == "refer":
        w["refers"].append(step.names[1])
    else:
        w["has" if step.template == "GivenDoes" else "lacks"].append(step.names[-1])


def spelled(step):
    """What each term is spelled in the world: a pack of the context's own spells its one term `binder`; `base`'s are
    its first nouns, a term it has not the fixture's `note`."""
    w = world(step)
    if "base" in w["imports"]:
        found = dict(zip(w["has"], base_terms()))
        found.update({t: "note" for t in w["lacks"]})
        return found
    return {t: OWN for t in w["has"]}


def build(step):
    """The fixture copied into the repository, the packs the Givens import written and imported, and each element
    that refers to a term a relation of the note to it."""
    repo, w = step.repo, world(step)
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    words = spelled(step)
    for name in (n for n in w["imports"] if n != "base"):
        (repo / "spec" / "packs").mkdir(exist_ok=True)
        (repo / "spec" / "packs" / ("%s.md" % name)).write_text(
            "---\nsource: ex.com/prod/up\n---\n# %s\n\n## Glossary\n\n%s" % (name, "".join(
                "- **%s** (noun): a thing the pack gives.\n" % words[t] for t in w["has"])))
    index = repo / "spec" / "index.md"
    text = index.read_text()
    assert "imports: [request]\n" in text, text
    index.write_text(text.replace("imports: [request]\n", "imports: [%s]\n" % ", ".join(
        ["request"] + w["imports"]), 1))
    model = repo / "spec" / "model" / "notes.md"
    text = model.read_text()
    assert RELATION in text, text
    refers = "".join("; refers to → %s (many)" % words[t] for t in w["refers"])
    model.write_text(text.replace(RELATION, RELATION.rstrip("\n") + refers + "\n", 1))


def runs(step):
    if not mine(step) or step.term not in ("`spec check`", "`spec lexicon`"):
        return False
    build(step)
    step.context["result"] = step.run(*step.term.strip("`").split())


def then_ok(step):
    """the specification service (the language service) completes this request: the run exits 0."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_prints(step, shown=True):
    """the language service returns the term t1: `spec lexicon` shows it as a term of the pack `base`."""
    if not mine(step) or "result" not in step.context or not step.names:
        return False
    done, word = step.context["result"], spelled(step).get(step.names[0])
    rows = [line.split() for line in done.stdout.splitlines()]
    found = any(" ".join(r[:-2]) == word and r[-2:] == ["[pack", "base]"] for r in rows if len(r) > 2)
    assert found is shown, done.stdout + done.stderr


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_ok)
W.local("ThenPrints")(then_prints)
W.local("ThenPrintsNot")(lambda step: then_prints(step, shown=False))
