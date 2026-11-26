"""drafting's term that breaks a lexicon rule refused when written or reworded into an item, naming the term and every
rule it breaks (r101, r102, b810, b826). Each a `local` handler that takes a step of those scenarios (`mine`) and returns
False on any other. The rule the While part names (`v_t4`, `v_t7`, `v_t11`, `v_t13`, `v_t14`, `v_t19`) picks the
world and the term (`CASES`): readiness_world's codified spec with a capability term of work-queue, or, of `v_t19`, the domain-model
fixture's spec with a vocabulary entry of notes; each term breaks that rule and one other (the rules r1 and r2 the
Givens say it violates) and not a third (r3). The When writes the term with `work line <item> --into <cap> --term`, or
rewords a term the item holds (`GOOD`, written first) into it with `--reword-term`; the Thens read the refusal (an
error exit, no usage error, the item as it was) and the term's word and the rules' codes in what it printed."""
import re
import shutil
import sys
from pathlib import Path

W, B, R = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_readiness_world"))
local = W.local
TAGS = {"r101", "r102"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
SHELFMARK = "- **shelfmark** (thing): a mark on a shelf. It names a place."
STAMP = "- **stamp** (verb, action): to mark a work-item. It is quick."
UNASPECTED = "- **stamp** (verb): to mark a work-item. Frame: agent stamps grobble."     # v_t13 and v_t14 alone
NOVEL = "- **novel** (noun) → object novel. A long book. It tells a story."
# the rule the While part names: (the world, the term, the other rule it breaks, a rule it does not break)
CASES = {"v_t4": ("plain", SHELFMARK, "v_t7", "v_t11"), "v_t7": ("plain", SHELFMARK, "v_t4", "v_t11"),
         "v_t11": ("plain", STAMP, "v_t7", "v_t4"), "v_t13": ("plain", UNASPECTED, "v_t14", "v_t7"),
         "v_t14": ("plain", UNASPECTED, "v_t13", "v_t7"), "v_t19": ("domain", NOVEL, "v_t7", "v_t4")}
GOOD = {"plain": ("work-queue", "shelfnote", "- **shelfnote** (noun): a note kept on a shelf."),
        "domain": ("notebook", "jotting", "- **jotting** (noun) → object note.")}


def _tags(step):
    """The scenario's tags among r101 and r102 (the When is re-keyed by the CLI contract: its text no longer says
    whether it writes or rewords)."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return TAGS & set(found.tags) if found is not None else set()


def mine(step):
    """True when the step is of drafting's scenarios of r101 and r102."""
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and bool(_tags(step))


def _world(step):
    return step.context.setdefault("term_rules", {"code": None, "violated": [], "clear": []})


def _word(bullet):
    return re.match(r"- \*\*(.+?)\*\*", bullet).group(1)


@local("GivenK")
def given_named(step):
    """a term t1, an item i1, a rule r1: what the When writes and the Thens read."""
    return None if mine(step) else False


@local("GivenDoes")
@local("GivenDoesNot")
def given_violates(step):
    """the term t1 violates `v_t4` (the case's rule), violates the rule r1, does not violate the rule r3."""
    if not mine(step):
        return False
    world = _world(step)
    code = next((np.strip("`") for np in step.nps if np.startswith("`")), None)
    if code is not None:
        world["code"] = code
        return None
    rule = re.search(r"\bthe rule (r\d+)", step.text).group(1)
    world["clear" if step.template == "GivenDoesNot" else "violated"].append(rule)
    return None


def _rules(world):
    """{rule instance: its code}: the violated ones the case's rule and the other, the clear one the third."""
    _, _, other, clear = CASES[world["code"]]
    out = dict(zip(world["violated"], (world["code"], other)))
    out.update({r: clear for r in world["clear"]})
    return out


@local("WhenRuns")
@local("WhenRequests")
def write(step):
    """`work line <item> --into <cap> --term <t1>`, or of a reword the good term first and then `--reword-term`."""
    if not mine(step):
        return False
    world = _world(step)
    kind, bullet = CASES[world["code"]][:2]
    capability, good_word, good = GOOD[kind]
    item = world["item"] = re.search(r"\bthe item (i\d+)", step.text).group(1)
    if kind == "plain":
        R.codify(step)
    else:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
    B.write_item(step, item, status="shaped")
    world["word"] = _word(bullet)
    if _tags(step) == {"r102"}:
        B.run_work(step, "line", B.ident(item), "--into", capability, "--term", good, **R.NO_INPUT)
        assert step.context["result"].returncode == 0, step.context["result"].stderr
        args = ["--reword-term", good_word, bullet]
    else:
        args = ["--term", bullet]
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    B.run_work(step, "line", B.ident(item), "--into", capability, *args, **R.NO_INPUT)
    return None


@local("ThenDoes")
@local("ThenDoesNot")
def then(step):
    """refuses this request: an error exit that is no usage error, the item as it was; names the term t1 (its
    word) and the rule r1 (its code); does not name the rule r3."""
    if not mine(step):
        return False
    world, done = _world(step), step.context["result"]
    said = done.stdout + done.stderr
    if step.term in ("refuses", "refuse"):
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        rel = step.context["items"][world["item"]]
        assert (step.repo / rel).read_text() == world["before"], step.text
        return None
    rule = re.search(r"\bthe rule (r\d+)", step.text)
    wanted = _rules(world)[rule.group(1)] if rule else world["word"]
    found = re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(wanted), said) is not None
    assert found == (step.template == "ThenDoes"), (step.text, said)
    return None
