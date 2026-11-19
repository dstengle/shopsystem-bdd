"""feature-file-tools' capability of one construct (b274): a requirement r1 that uses a construct a Given names
(`the requirement r1 uses `holds-exactly``, `the precondition p1 uses `nothing``) is the construct catalogue's example
of it, the one requirement of the capability c1 in the catalogue's context `grammar/corpus/constructs/` (`prepare`), or
of holds-exactly with `rc-object` or `of-relation` (b315) and of nothing with `rc-subject` b297's line on a response's object (`returned`);
"the step s2 uses `not-condition`" holds when a step of the feature `features generate` wrote reads, in the step
grammar 4, as a tree that uses the construct as `spec constructs` tells it (`uses`). A requirement that uses an
order (b275) is the example of `order-by-every`, and "the scenario s1 has the order counter-example o2" holds when
the feature's Then states the order and its Givens give at least three members distinct values in neither that order
nor its reverse, so that world_order's check of the Then fails on the members printed as given (`counter`). A
requirement that uses `order-by` and a verb while no frame takes `thing` (b298) is the example said with the verb
"return", whose one frame names the collection's kind (`agent returns worktree to agent`), added to the context; one
that uses `order-by-every` and `of-relation` (b328) the example said after "every file in the worktree"."""
import re
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
CODES = ("holds-exactly", "nothing", "order-by", "order-by-every")
# on a response's object (b297): the files a relative clause's, the act one with a recipient, as a feed's "return"
RETURNING = ("- **keep** (verb, state): an agent holds on to a file. Frame: agent keeps file.\n"
             "- **return** (verb, action): an agent hands a thing back to an agent. Frame: agent returns thing to "
             "agent.\n")
RETURNED = {("holds-exactly", "rc-object"): "When the person runs `work start`, `work` shall return a worktree that "
            "holds exactly the files that a session keeps to the person.",
            # b315: the restriction reaches a second thing, the line of a stage
            ("holds-exactly", "of-relation"): "When the person runs `work start`, `work` shall return a worktree that "
            "holds exactly the files that cover the line of a stage to the person.",
            ("nothing", "rc-subject"): "When the person runs `work start`, `work` shall return a worktree that holds "
            "nothing to the person."}
# b298: a verb with no frame on `thing`, and the order-by example said with it
RETURN_WORKTREE = ("- **return** (verb, action): an agent hands a worktree back to an agent. "
                   "Frame: agent returns worktree to agent.\n")
ORDERED_RETURN = ("When the person runs `work start`, `work` shall return a worktree that holds a file, ordered by "
                  "version, in descending order to the person.")
# b300: the order-by-every example said with give
ORDERED_GIVE = ("When the person runs `work start`, `work` shall give every file, ordered by version, in ascending "
                "order to the person.")

# b328: the order-by-every example after every K in a collection, a modifier by the row file | in | worktree
ORDERED_IN = ("When the person runs `work start` on a worktree, `work` shall print every file in the worktree, "
              "ordered by version, in ascending order.")


def construct(w):
    """The code of the construct a Given says the requirement or its precondition uses, or None."""
    used = [o.strip("`") for v, _, o, pos in w["facts"] if v == "use" and pos and isinstance(o, str)]
    if any(w["kinds"].get(o) == "order" for o in used):     # the requirement r1 uses the order o1 (b275)
        return "order-by-every"
    return next((c for c in used if c in CODES), None)


def unthinged(w):
    """True when a Given says no frame takes `thing` and the requirement uses a verb (b298)."""
    return (any(v == "take" and a == ("no", "frame") and o == "`thing`" for v, a, o, _ in w["facts"])
            and any(v == "use" and w["kinds"].get(o) == "verb" for v, _, o, _ in w["facts"]))


def returned(w):
    """The line of b297 the requirement's constructs say, or None."""
    used = {o.strip("`") for v, _, o, pos in w["facts"] if v == "use" and pos and isinstance(o, str)}
    return next((line for codes, line in RETURNED.items() if used.issuperset(codes)), None)


def example(code):
    text = (PLUGIN / "grammar" / "constructs.md").read_text()
    return re.search(r"^## %s\n.*?```construct\n(.*?)\n" % re.escape(code), text, re.DOTALL | re.MULTILINE).group(1)


def prepare(step, w, write, name, path):
    """The capability `name` whose r1 is the catalogue's example of the construct; True when one was written."""
    code, line = construct(w), returned(w)
    if code is None:
        return False
    index = (PLUGIN / "grammar" / "corpus" / "constructs" / "spec" / "index.md").read_text()
    line, index = line or example(code), index + (RETURNING if line else "")
    if code == "order-by" and unthinged(w):
        line, index = ORDERED_RETURN, index.replace("\n- **give** (verb", "\n%s- **give** (verb" % RETURN_WORKTREE, 1)
    if code == "order-by-every" and unthinged(w):
        line = ORDERED_GIVE
    if code == "order-by-every" and any(v == "use" and o == "`of-relation`" for v, _, o, _ in w["facts"]):
        line = ORDERED_IN
    cap = ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-2\n"
           "rests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n### [g1] %s\n"
           "- [r1] %s\n\n## Not yet\n" % (path, name, name, name, code, line))
    write(step.repo / "spec" / "index.md", index)
    write(step.repo / "spec" / "capabilities" / ("%s.md" % name), cap)
    return True


def uses(step, name):
    """Assert that a step of the feature of `name` uses the construct the Then names."""
    if str(PLUGIN / "scripts") not in sys.path:
        sys.path.insert(0, str(PLUGIN / "scripts"))
    import model_constructs
    import spec_gf
    import spec_rgl_steps
    from model_constructs_table import CONSTRUCTS
    code = step.nps[0].strip("`")
    entry = next(e for e in CONSTRUCTS if e["code"] == code)
    text = (step.repo / "features" / ("%s.feature" % name)).read_text()
    lines = re.findall(r"^\s*(?:Given|When|Then|And) (.*)$", text, re.MULTILINE)
    frames = model_constructs.roles(spec_rgl_steps.load(step.repo)[0])
    found = [line for line in lines for t in spec_rgl_steps.trees(step.repo, line)
             if model_constructs.uses(entry, str(spec_gf.expr(t)), frames)]
    assert found, "no step uses %s:\n%s" % (code, text)


def counter(step, name):
    """Assert that the feature of `name` has an order counter-example (b275)."""
    if str(PLUGIN / "scripts") not in sys.path:
        sys.path.insert(0, str(PLUGIN / "scripts"))
    import features_vocab4
    import spec_lf_order
    import spec_rgl_vocab
    if str(Path(__file__).parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).parent))
    import world_order
    text = (step.repo / "features" / ("%s.feature" % name)).read_text()
    thens = [features_vocab4.step(step.repo, "then", s) for s in re.findall(r"^\s*(?:Then|And) (.*ordered by.*)$",
                                                                            text, re.MULTILINE)]
    order = next((c.order for c in thens if c.order), None)
    assert order, "no Then states an order:\n%s" % text
    term, direction, _ = order
    found = re.findall(r"^\s*(?:Given|And) the %s of the (.+?) \w+ is `[^`]+`$" % re.escape(term), text, re.MULTILINE)
    values = dict(re.findall(r"^\s*(?:Given|And) the %s of the .+? (\w+) is `([^`]+)`$" % re.escape(term), text,
                             re.MULTILINE))
    vocab = spec_rgl_vocab.read(step.repo)
    kinds = {k for k, (one, _) in vocab.nouns.items() if one in found}
    # of a word of two senses (b288), the entry of the members' kind
    entry = next(t for t, ks in vocab.attributes if t.term == term
                 and any(a in ks for k in kinds for a in vocab.ancestors(k)))

    def key(v):
        return spec_lf_order.key(entry, v)
    assert len(set(map(key, values.values()))) >= 3, "fewer than three members of distinct values:\n%s" % text
    given = " ".join(values)
    for way in ("ascending", "descending"):
        try:
            world_order.ordered(given, values, way, key)
        except AssertionError:
            continue
        raise AssertionError("the members are given in %s order:\n%s" % (way, text))
    world_order.ordered(" ".join(sorted(values, key=lambda m: key(values[m]), reverse=direction == "descending")),
                        values, direction, key)
