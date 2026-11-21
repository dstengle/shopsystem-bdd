"""drafting's universal conditions, upstream entries and given blocks taken back out of an item or replaced (drafting
r53-r64, b48). Each a `local` handler that takes a step of those scenarios (`mine`) and returns False on any other:
the item, written at the When, holds a `### drafting` block of two groups, each with a given block (g1's the given
block g1), a `### universal` block of two conditions (U1 the universal condition u1) and a `### index` block of two
upstream entries (the first the upstream entry u1), unless a Given says it does not hold u1 or g1; `work line
--remove-universal`, `--replace-universal`, `--remove-upstream`, `--replace-upstream`, `--remove-given` or
`--replace-given` run on it; and the Thens read the item back, as committed, or the refusal and what it names."""
import importlib.util
import re
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
local = W.local

TAGS = {"r%d" % n for n in range(53, 65)}
KINDS = ("universal condition", "upstream entry", "given block")
UP1, UP2 = "bounded-context/example/one", "bounded-context/example/three"
# (kind, name) -> the text the item holds it by; the other piece of each kind is kept beside it
TEXTS = {("universal condition", "u1"): "The drafting service shall never keep a secret.",
         ("universal condition", "u2"): "The drafting service shall never keep a password.",
         ("upstream entry", "u1"): "%s: the parts read, github: ex/one" % UP1,
         ("upstream entry", "u2"): "%s: the parts read, github: ex/three" % UP2,
         ("given block", "g1"): 'the feature file `a` holds "1.0.0"',
         ("given block", "g2"): 'the feature file `a` holds "4.0.0"'}
OTHERS = {"universal condition": "The drafting service shall never keep a token.",
          "upstream entry": "bounded-context/example/two: the parts read, github: ex/two",
          "given block": 'the feature file `b` holds "2.0.0"'}
# the option of each kind and the argument that names the old piece
REMOVE = {"universal condition": ("--remove-universal", "U1"), "upstream entry": ("--remove-upstream", UP1),
          "given block": ("--remove-given", "drafting#g1")}
REPLACE = {k: (o.replace("remove", "replace"), a) for k, (o, a) in REMOVE.items()}
NEW = {"universal condition": "u2", "upstream entry": "u2", "given block": "g2"}


def mine(step):
    """True when the step is of drafting's scenarios of r53-r64."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    return step.context.setdefault("pieces", {"absent": set()})


def _given(text, held=True):
    return "\n\n```given\n%s\n```" % text if held else ""


def _section(world):
    """The item's `## Requirements`: each kind's piece u1 (g1) unless it is absent, and the other beside it."""
    def held(kind):
        return (kind, "u1" if kind != "given block" else "g1") not in world["absent"]
    return ("### drafting\n\n#### [g1] One\n- [r1] When the person runs `work line`, the drafting service shall keep "
            "the item.%s\n\n#### [g2] Two\n- [r2] When the person runs `work ready`, the drafting service shall keep "
            "the item.%s\n\n### universal\n\n%s- [U2] %s\n\n### index\n\n%s- %s" % (
                _given(TEXTS["given block", "g1"], held("given block")), _given(OTHERS["given block"]),
                "- [U1] %s\n" % TEXTS["universal condition", "u1"] if held("universal condition") else "",
                OTHERS["universal condition"],
                "- %s\n" % TEXTS["upstream entry", "u1"] if held("upstream entry") else "", OTHERS["upstream entry"]))


def _kind(step):
    return next((k for k in KINDS if k in step.text), None)


@local("GivenK")
def given_named(step):
    """a universal condition u1, u2; an upstream entry u1, u2; a given block g1, g2: the texts above."""
    if not mine(step) or step.kind not in KINDS:
        return False
    _world(step)
    return None


@local("GivenDoesNot")
def given_absent(step):
    """the item i1 does not hold the universal condition u1 (...): its block written without it."""
    if not mine(step) or step.term not in ("holds", "hold") or _kind(step) is None:
        return False
    _world(step)["absent"].add((_kind(step), step.names[1]))
    return None


@local("WhenRuns")
def change(step):
    """`work line <item> --remove-<piece> <its id>` or `--replace-<piece> <its id> <the new one's text>` (the request
    re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    kind = next((k for k in KINDS if REMOVE[k][0] in options or REPLACE[k][0] in options), None)
    if not mine(step) or kind is None:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    world.update(declared=item, kind=kind)
    B.write_item(step, item, status="shaped", sections={"Requirements": _section(world)})
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    if REMOVE[kind][0] in options:
        args = list(REMOVE[kind])
    else:
        args = list(REPLACE[kind]) + [TEXTS[kind, NEW[kind]]]
    B.run_work(step, "line", B.ident(item), *args)
    return None


def _item_text(step):
    return (step.repo / step.context["items"][_world(step)["declared"]]).read_text()


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][_world(step)["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


def _held(text, kind, name):
    """Whether the item's text holds the piece `name` of `kind`, the other pieces of each kind kept beside it."""
    assert all(o in text for o in OTHERS.values()), text
    return TEXTS[kind, name] in text


def _named(step):
    kind = _kind(step)
    return kind, re.search(r"\b%s ([ug]\d+)" % kind, step.text).group(1)


@local("ThenDoes")
def kept(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the
    universal condition u1 (...): the output names its id; the item i1 holds u2, the drafting service keeps it:
    committed, the old one gone."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    kind, name = _named(step)
    if step.term == "name":
        assert REMOVE[kind][1] in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    text = _done(step) if step.term not in ("holds", "hold") else _item_text(step)
    old = "g1" if kind == "given block" else "u1"
    assert _held(text, kind, name) and not _held(text, kind, old), (step.text, text)
    return None


@local("ThenDoesNot")
def not_kept(step):
    """the item i1 does not hold the universal condition u1 (...); the drafting service does not keep it: committed
    without it, the other pieces kept."""
    if not mine(step) or _kind(step) is None:
        return False
    kind, name = _named(step)
    text = _done(step) if step.term not in ("holds", "hold") else _item_text(step)
    assert not _held(text, kind, name), (step.text, text)
    return None
