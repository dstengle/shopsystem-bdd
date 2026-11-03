"""`features generate` (design §14.2, §13.4): each group of a codified service capability is one scenario, written
deterministically from its parsed requirements in the Steps grammar.

Instances are named by their kind's letter and a number, in order of first mention; a `given` block's instances are
taken first. Witnesses are chosen by rule: `every K whose A is not v1, v2` gives one instance with the first other
value of A (two when the group also names the kind in the plural, `Ks`) and one instance per excluded value, each
included one getting the Then and each excluded one its negation; `every K that is v` gives an instance with v and one
with the first other value; a condition expands through its `Means:`; an `If` trigger's instance takes the first
value its clause allows. Order: the `given` block, Givens, the When, then one Then (or one per witness) per
requirement in id order. A logic-only group (`spec_tree.logic_only`) has no scenario.
"""
from pathlib import Path

import features_vocab as fv
import spec_grammar
import spec_read
import spec_tree

HEADER = "# generated from spec/capabilities/%s.md by features generate; do not edit"
LETTERS = {"initiative": "i", "work-item": "w", "capability-proposal": "p", "glossary-proposal": "p", "request": "q"}
SIMPLE = {"DoTo": "SDoesTo", "ExitOk": "SExitsOk", "ExitErr": "SExitsErr", "ChangeNothing": "SChangesNothing",
          "CommitPush": "SCommits"}
DETS = ("_An", "_Every", "_The", "_No", "_AtMostOne", "_One", "_Pl", "_Its", "_Named", "_It")


class GenerateError(Exception):
    """A group that cannot be written as a scenario: a requirement or given line that does not parse, or a
    construct with no step."""


class Inst:
    """An instance a scenario names: its kind, name and attribute values; `block` when the given block gave it."""

    def __init__(self, kind, name, values=None, block=False):
        self.kind, self.name, self.values, self.block, self.claimed, self.extra = kind, name, dict(values or {}), \
            block, False, []


class Scenario:
    """One group written as Gherkin lines: (keyword, text, block)."""

    def __init__(self, v, cap, group, trees):
        self.v, self.cap, self.group, self.trees = v, cap, group, trees
        self.insts, self.keyed, self.everies, self.counts, self.used = [], {}, {}, {}, set()
        self.plural = {v.of(n[0])[0][2] for t in trees for n in spec_tree.nodes(t)
                       if n[0].endswith("_Pl") and v.of(n[0])[0]}
        self.tids = {(k, t.term): tid for t, k, tid in fv.attributes(v.lex, v.ids)}
        self.block_lines, self.feats, self.extra_givens = [], [], []

    def value(self, node):
        return self.v.of(node[0])[0][1]

    def vid(self, kind, attribute, value):
        return (self.v.ids[("value", value, (kind, attribute))],)

    def inst_np(self, inst):
        return (self.v.kind_id[inst.kind] + "_Inst", ("NameLit", inst.name))

    def new(self, kind, values, reuse=True):
        for inst in self.insts if reuse else ():
            if inst.block and not inst.claimed and inst.kind == kind and all(
                    inst.values.get(a) in (None, x) for a, x in values.items()):
                inst.claimed, inst.extra = True, inst.extra + [(a, x) for a, x in values.items() if a not in inst.values]
                inst.values.update(values)
                return inst
        letter = LETTERS.get(kind, kind[0])
        while "%s%d" % (letter, self.counts.get(letter, 0)) in self.used or letter not in self.counts:
            self.counts[letter] = self.counts.get(letter, 0) + 1
        self.used.add("%s%d" % (letter, self.counts[letter]))
        self.insts.append(Inst(kind, "%s%d" % (letter, self.counts[letter]), values))
        return self.insts[-1]

    def given_block(self):
        for text, block in self.group.given:
            try:
                tree = fv.parse(self.v, "given", text)
            except fv.StepError as err:
                raise GenerateError("%s#%s: the given line %s" % (self.cap, self.group.id, err))
            info, suffix = self.v.of(tree[0])
            names = [n[1] for n in spec_tree.nodes(tree) if n[0] == "NameLit"]
            self.used |= set(names)
            if info and suffix in ("_Given", "_HoldsText", "_HoldsBlock") and info[0] in ("kind", "attribute"):
                values = {info[3]: self.value(tree[2])} if info[0] == "attribute" else {}
                self.insts.append(Inst(info[2], names[0], values, block=True))
            self.block_lines.append(("given", self.v.text(tree), block))

    def constraints(self, cn, out):
        """A kind's CN read into {attribute: ("in"|"out", [values])}; conditions expand through their Means and
        relations are kept under "_rel"."""
        info, suffix = self.v.of(cn[0])
        if info is None or info[0] == "kind":
            return out
        if info[0] == "attribute":
            values = [self.value(n) for n in spec_tree.nodes(cn[1] if suffix == "_Pre" else cn[2])
                      if (self.v.of(n[0])[0] or ("",))[0] == "value"]
            out[info[3]] = ("out" if suffix.endswith("Not") else "in", values)
        elif info[0] == "condition":
            self.condition(info, suffix.endswith("Not"), out)
        elif info[0] == "relation":
            out.setdefault("_rel", []).append((info[1], cn[2]))
        return self.constraints(cn[1], out) if suffix != "_Pre" and len(cn) > 1 else out

    def condition(self, info, negated, out):
        """A condition's Means read as an attribute constraint ("its status is not `done` and not `abandoned`")."""
        term = next(t for t in self.v.lex.of("condition") if t.term == info[1] and info[2] in t.kinds)
        for a in (t.term for t in self.v.lex.of("attribute") if info[2] in t.kinds):
            if "its %s is" % a in term.means:
                mode = "out" if (" is not " in term.means) != negated else "in"
                out[a] = (mode, [w.strip(",.") for w in term.means.split() if w.startswith("`")])
        return out

    def choose(self, kind, cons, n_in):
        """The witnesses' values: [(values, included)]."""
        inc, excl = {}, []
        for a, (mode, values) in ((a, c) for a, c in cons.items() if not a.startswith("_")):
            others = [x for x in next(t for t in self.v.lex.of("attribute") if t.term == a and kind in t.kinds).values
                      if x not in values]
            inc[a] = values[0] if mode == "in" or not others else others[0]
            excl += ([{a: others[0]}] if others else []) if mode == "in" else [{a: x} for x in values]
        return [(dict(inc), True) for _ in range(n_in)] + [(e, False) for e in excl]

    def resolve(self, np, pre):
        """An Inst, a list of (Inst, included), or None (an output NP, kept as written)."""
        info, det = self.v.of(np[0])
        kind, key = info[2], (pre, spec_tree.show(spec_tree.normal(np)))
        last = next((i for i in reversed(self.insts) if i.kind == kind), None)
        if det == "_It" or (det in ("_The", "_Its") and last):
            return last or self.new(kind, {})
        if det == "_Pl" and kind in self.everies:
            return [(i, True) for i, inc in self.everies[kind] if inc]
        if key in self.keyed or (not pre and det not in ("_Every", "_Pl", "_Named")):
            return self.keyed.get(key)
        if det == "_Named":
            self.keyed[key] = Inst(kind, np[1][1])
            self.insts.append(self.keyed[key])
            return self.keyed[key]
        cons = self.constraints(np[1], {}) if isinstance(np[1], tuple) and det != "_Pl" else {}
        if det in ("_Every", "_Pl"):
            got = [(self.new(kind, vals, reuse=False), inc)
                   for vals, inc in self.choose(kind, cons, 2 if kind in self.plural else 1)]
            self.everies.setdefault(kind, got)
        else:
            got = [(self.new(kind, self.choose(kind, cons, 1)[0][0]), True)]
        for term, other in cons.get("_rel", []):
            target = self.resolve(other, True)
            target = target[0][0] if isinstance(target, list) else target
            rid = next(self.v.ids[t.key] for t in self.v.lex.of("relation") if t.term == term)
            self.extra_givens += [(rid + "_Given", ("NameLit", i.name), ("NameLit", target.name)) for i, _ in got]
        self.keyed[key] = got if det in ("_Every", "_Pl") else got[0][0]
        return self.keyed[key]

    def is_np(self, node):
        info, det = self.v.of(node[0]) if isinstance(node, tuple) else (None, "")
        return bool(info) and info[0] == "kind" and det in DETS

    def subst(self, tree, pre, pick=None):
        """The tree with every kind noun phrase replaced by its instance; `pick` = (node, inst) overrides one."""
        if not isinstance(tree, tuple):
            return tree
        if self.is_np(tree):
            got = pick[1] if pick and pick[0] is tree else self.resolve(tree, pre)
            got = got[0][0] if isinstance(got, list) else got
            if got is not None:
                return self.inst_np(got)
        return (tree[0],) + tuple(self.subst(a, pre, pick) for a in tree[1:])

    def precondition(self, atom):
        info, suffix = self.v.of(atom[0])
        if info and info[0] == "attribute" and suffix in ("_Is", "_IsNot"):
            target = next(i for i in self.insts if i.name == self.subst(atom[1], True)[1][1])
            if suffix == "_Is" or info[3] not in target.values:
                mode = "in" if suffix == "_Is" else "out"
                target.values.update(self.choose(info[2], {info[3]: (mode, [self.value(atom[2])])}, 1)[0][0])
        elif info and info[0] == "condition":
            self.resolve(atom[1], True).values.update(
                self.choose(info[2], self.condition(info, suffix.endswith("Not"), {}), 1)[0][0])
        elif atom[0] in ("Holds", "HoldsA"):
            self.extra_givens.append(("SAtom", self.subst(atom, True)))
        elif atom[0] != "IsFree":
            raise GenerateError("%s#%s: no Given for %s" % (self.cap, self.group.id, atom[0]))

    def becomes(self, trig):
        info, suffix = self.v.of(trig[0])
        if info and suffix == "_Becomes":
            inst = self.resolve(trig[1], True)
            attr = next(t for t in self.v.lex.of("attribute") if t.term == info[3] and info[2] in t.kinds)
            source = next((s for s, t, _ in attr.transitions if t == self.value(trig[2])), None)
            if source and info[3] not in inst.values:
                inst.values[info[3]] = source

    def then(self, resp, rid):
        neg, subj, vp = resp[0] == "ShallNot", resp[1], resp[2]
        node = next((n for n in spec_tree.nodes(resp) if self.is_np(n) and self.v.of(n[0])[1] in ("_Every", "_Pl")),
                    None)
        out = []
        for inst, included in self.resolve(node, False) if node else [(None, True)]:
            if neg and not included:
                continue
            pick = (node, inst) if inst else None
            s, args = self.subst(subj, False, pick), [self.subst(a, False, pick) for a in vp[1:]]
            info, suffix = self.v.of(vp[0])
            if vp[0] in ("Do", "Print"):
                out.append(({"Do": "SDoes", "Print": "SPrints"}[vp[0]] + ("" if included and not neg else "Not"),
                            s, *args))
            elif vp[0] in SIMPLE and not neg:
                out.append((SIMPLE[vp[0]], s, *args))
            elif vp[0] == "RefuseErr" and not neg:
                out += [("SExitsErr", s, *args), ("SChangesNothing", s)]
            elif info and info[0] == "attribute" and suffix == "_Set":
                value = args[1] if included else self.vid(info[2], info[3], inst.values[info[3]])
                out.append(("SAtom", (vp[0][:-4] + ("_IsNot" if neg else "_Is"), args[0], value)))
            elif vp[0] in ("Hold", "HoldA") and subj[0] == "NPSubj" and not neg:
                out.append(("SAtom", ("Holds" if vp[0] == "Hold" else "HoldsA", s[1], *args)))
            else:
                raise GenerateError("%s#%s: no Then step for %s" % (self.cap, rid, vp[0]))
        return out

    def lines(self):
        self.given_block()
        when, thens = None, []
        for req, tree in zip(self.group.requirements, self.trees):
            p = spec_tree.parts(tree)
            if p["feat"] is not None and p["feat"][0] == "FeatGiven":
                self.feats += [] if ("SFeat", p["feat"]) in self.feats else [("SFeat", p["feat"])]
            elif p["feat"] is not None:
                self.precondition(p["feat"][1])
            cond = p["cond"]
            while cond is not None:
                self.precondition(cond[1])
                cond = cond[2] if cond[0] == "CondAnd" else None
            if p["trig"] is not None:
                self.becomes(p["trig"])
                when = when or ("STrig", self.subst(p["trig"], True))
            thens += self.then(p["resp"], req.id)
        givens = []
        for inst in self.insts:
            items = inst.extra if inst.block else list(inst.values.items())
            if not inst.block:
                givens.append((self.tids[(inst.kind, items[0][0])] + "_Given", ("NameLit", inst.name),
                               self.vid(inst.kind, *items[0])) if items else
                              (self.v.kind_id[inst.kind] + "_Given", ("NameLit", inst.name)))
                items = items[1:]
            givens += [("SAtom", (self.tids[(inst.kind, a)] + "_Is", self.inst_np(inst), self.vid(inst.kind, a, x)))
                       for a, x in items]
        steps = [("given", t) for t in self.feats + givens + self.extra_givens] + ([("when", when)] if when else [])
        return self.block_lines + [(k, self.v.text(t), None) for k, t in steps + [("then", t) for t in thens]]


def scenario_text(v, cap, group):
    """A group's scenario, or None for a logic-only group."""
    trees = []
    for req in group.requirements:
        parsed = spec_grammar.parse(v.root, req.text)
        if parsed.tree is None:
            raise GenerateError("%s#%s: %s" % (cap.name, req.id, parsed.refusal))
        trees.append(parsed.tree)
    if spec_tree.logic_only(trees):
        return None
    out = ["  " + " ".join("@" + x for x in [group.id] + [r.id for r in group.requirements]),
           "  Scenario: " + group.title]
    previous = None
    for keyword, text, block in Scenario(v, cap.name, group, trees).lines():
        out.append("    %s %s" % ("And" if keyword == previous else keyword.capitalize(), text))
        previous = keyword
        if block is not None and block.kind == "table":
            out += ["      " + line for line in block.lines]
        elif block is not None:
            out += ['      """'] + [("      " + line).rstrip() for line in block.lines] + ['      """']
    return "\n".join(out)


def generate(root, path):
    """The feature text of one codified capability file."""
    v, cap = fv.load(root), spec_read.capability(path)
    if cap.problems:
        raise GenerateError("; ".join("%s: %s" % (Path(path).name, p) for p in cap.problems))
    out = [HEADER % Path(path).stem, "Feature: %s" % cap.frontmatter.get("title", cap.name),
           "  Narrator: %s" % cap.frontmatter.get("narrator", "")]
    for group in sorted(cap.groups, key=lambda g: int(g.id[1:])):
        text = scenario_text(v, cap, group)
        out += ["", text] if text else []
    return "\n".join(out) + "\n"


def uncodified(root, paths):
    """The refusal of the first capability file of `paths` without `language: codified-1` (§13.4), or None: the 0.29
    reader is gone, so `migrate upgrade` converts it."""
    for path in paths:
        if not spec_read.codified(path):
            return "%s is not codified: run `migrate upgrade`" % Path(path).relative_to(root).as_posix()
    return None
