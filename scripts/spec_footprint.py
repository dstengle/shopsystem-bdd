"""A line's footprint in grammar 4 (b877): what of the grammar its parse can read, so that a change of the grammar's
sources that leaves it as it was leaves the line's parse as it was, and the parse kept in spec_parse_cache is read
with no compile of the new grammar.

GF's trees of a line are trees of the functions that can take part in one: those whose words the line holds, built
up from what the line can give (`_derived`: a code only where it holds a backticked token that is no word of the
vocabulary) and down from a line's category, `Req` (`_used`). The footprint (`of`) names, of those functions of the
generated module Context, each declaration and linearisation with the linearisation types of their categories, beside
the base grammar's files, the RGL's release, the module headers, the vocabulary's words among the line's tokens (the
literal slot refuses them) and the parse's limit. A function's words are its string literals: it is read as taking
part only where the line holds, of one chain of its literals joined by `++`, a token opening with each word (a
plural's, a genitive's), or, of a literal given to a paradigm alone (`mkN "number"`), with its stem less two
letters; a function of no literal, or whose linearisation picks among forms (a table, a case, variants, a `pre`, a
glued or empty token), is read as taking part in every line. Sources of another shape than spec_rgl writes give no
index (`index` None) and a line's footprint is then the sources' sha. A function is named in the footprint by its
name less its numbers where no other function or category of it reads so (`_canon`), and a parse is
kept with those names (`rename`), so a term that moves another's number moves no parse.
"""
import hashlib
import re
from collections import defaultdict

FUN = re.compile(r"^  ([A-Za-z_][\w']*) : ([^;]+) ;$")
LIN = re.compile(r"^  ([A-Za-z_][\w']*)(?: [A-Za-z_][\w']*)* = (.*) ;$")
LINCAT = re.compile(r"^  ([A-Za-z_][\w']*) = ([^;]+) ;$")
LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"')
ALONE = re.compile(r'\bmk(?:N|N2|N3|PN|A|A2|V|V2|V3|VA|VS|VV)\s+"((?:[^"\\]|\\.)*)"\s*[;)]')     # a paradigm's
UNSURE = re.compile(r'\btable\b|\bcase\b|\bvariants\b|\bpre\b|\bBIND\b|&\+|\\|(?<!\+)\+(?!\+)|\bPredef\b')
BASE_FUN = re.compile(r"([A-Za-z_][\w']*(?:\s*,\s*[A-Za-z_][\w']*)*)\s*:\s*([^;]+);")
IDENT = re.compile(r'"(?:[^"\\]|\\.)*"|[A-Za-z_][\w\'#]*')
DIGITS = re.compile(r"\d+")
JOINED = re.compile(r"^\s*\+\+[\s(]*$")
PREDEF = ("Int", "Float")
START = "Req"
_indexes = {}


class Index:
    """The functions of one set of sources: their signatures, texts and words."""

    def __init__(self):
        self.sig = {}                    # name: (args, result), the base grammar's among them
        self.text = {}                   # a Context function's declaration and linearisation
        self.lincat = {}
        self.always = set()              # functions read as taking part in every line
        self.chains = []                 # (a function, the keys a token must open with, one for each word)
        self.by_key = defaultdict(set)   # a key: the chains that hold it
        self.head = ""
        self.consumers = defaultdict(list)   # a category: the functions of `always` that take it
        self.producers = defaultdict(list)   # a category: the functions of `always` that give it
        self.stripped = {}                   # a text naming only itself and its categories: its numbers `#`
        self.idents = {}                     # a text: the functions and categories of Context it names
        self.zero = []                       # the functions of `always` of no argument
        self.strip = {}                      # a function's or a category's name with its numbers `#`


def _prepared(out):
    """`out` with what every line's footprint reads computed once."""
    for name in out.always:
        args, result = out.sig[name]
        for arg in set(args):
            out.consumers[arg].append(name)
        out.producers[result].append(name)
    out.zero = [n for n in out.always if not out.sig[n][0]]
    own = set(out.text) | set(out.lincat)
    out.strip = {n: DIGITS.sub("#", n) for n in own}
    for key, text in list(out.text.items()) + list(out.lincat.items()):
        named = {m for m in IDENT.findall(text) if m in own}
        out.idents[key] = named
        if named <= {key, *out.sig.get(key, ((), None))[0], out.sig.get(key, ((), None))[1]}:
            out.stripped[key] = rename(text, {n: out.strip[n] for n in named})
    return out


def _signature(text):
    parts = [p.strip() for p in text.split("->")]
    return tuple(parts[:-1]), parts[-1]


def _base(srcs, out):
    """The base grammar's functions (Base.gf, Time.gf), every one taking part in every line."""
    for name in sorted(srcs):
        if name.endswith(".gf") and not name.endswith("Eng.gf") and name != "Context.gf":
            body = re.sub(r"--[^\n]*", "", srcs[name])
            section = body.split(" fun", 1)[1] if " fun" in body else ""
            for names, typ in BASE_FUN.findall(section):
                for each in names.split(","):
                    out.sig[each.strip()] = _signature(typ)
                    out.always.add(each.strip())


def _words(out, name, body):
    """`name`'s chains read off its linearisation `body`: the literals joined by `++` alone, which a linearisation
    that holds one of them holds whole; each word's key itself, or a paradigm's lone literal's stem less two
    letters."""
    literals = list(LITERAL.finditer(body))
    if not literals or UNSURE.search(LITERAL.sub('"s"', body)) or any(not m.group(1).strip() for m in literals):
        out.always.add(name)
        return
    alone, chains, end = set(ALONE.findall(body)), [], None
    for found in literals:
        if end is None or not JOINED.match(body[end:found.start()]):
            chains.append([])
        loose = found.group(1) in alone
        chains[-1] += [w[:max(1, len(w) - 2)] if loose else w for w in found.group(1).lower().split()]
        end = found.end()
    for keys in chains:
        out.chains.append((name, tuple(keys)))
        for key in keys:
            out.by_key[key].add(len(out.chains) - 1)


def index(srcs, sha):
    """The Index of the sources `srcs` (named `sha`), once a process; None when they are of another shape."""
    if srcs is None:
        return None
    if sha not in _indexes:
        if len(_indexes) >= 4:
            _indexes.clear()
        _indexes[sha] = _read(srcs)
    return _indexes[sha]


def _read(srcs):
    out = Index()
    if "Context.gf" not in srcs or "ContextEng.gf" not in srcs:
        return None
    _base(srcs, out)
    decl, lins, heads = {}, {}, []
    for line in srcs["Context.gf"].split("\n"):
        found = FUN.match(line)
        if found:
            decl[found.group(1)] = line
            out.sig[found.group(1)] = _signature(found.group(2))
        elif line.startswith("  cat ") or line in ("  fun", "}", ""):
            continue
        elif line.startswith(("--", "abstract ", "  flags ")):
            heads.append(line)
        else:
            return None
    section = None
    for line in srcs["ContextEng.gf"].split("\n"):
        if line in ("  lincat", "  lin"):
            section = line.strip()
        elif line in ("}", ""):
            continue
        elif line.startswith(("--", "concrete ")) and section is None:
            heads.append(line)
        elif section == "lincat" and LINCAT.match(line):
            out.lincat[LINCAT.match(line).group(1)] = line
        elif section == "lin" and LIN.match(line):
            name, body = LIN.match(line).groups()
            lins[name] = line
            _words(out, name, body)
        else:
            return None
    if set(decl) != set(lins):
        return None
    out.text = {name: decl[name] + "\n" + lins[name] for name in decl}
    rest = sorted((k, v) for k, v in srcs.items() if k not in ("Context.gf", "ContextEng.gf"))
    out.head = hashlib.sha256(repr((heads, rest)).encode()).hexdigest()
    return _prepared(out)


def _enabled(idx, tokens):
    """The functions of chains the tokens may be of (those of `always` aside)."""
    opens = {t[:k] for t in {t.lower() for t in tokens} for k in range(1, len(t) + 1)}
    out = set()
    for key in opens & idx.by_key.keys():
        for chain in idx.by_key[key]:
            name, keys = idx.chains[chain]
            if name not in out and all(k in opens for k in keys):
                out.add(name)
    return out


def _derived(idx, extra, coded):
    """The categories the functions of `always` and `extra` build up from what the line gives."""
    have = set(PREDEF) | ({"String"} if coded else set())
    consumers = defaultdict(list)
    queue = list(have)
    for name in extra:
        for arg in set(idx.sig[name][0]):
            consumers[arg].append(name)
    for name in list(extra) + idx.zero:
        result = idx.sig[name][1]
        if not idx.sig[name][0] and result not in have:
            have.add(result)
            queue.append(result)
    while queue:
        cat = queue.pop()
        for each in (idx.consumers.get(cat, ()), consumers.get(cat, ())):
            for name in each:
                args, result = idx.sig[name]
                if result not in have and all(a in have for a in args):
                    have.add(result)
                    queue.append(result)
    return have


def _used(idx, extra, have):
    """The functions over derived categories that a tree of a line's category can hold."""
    producers = defaultdict(list)
    for name in extra:
        producers[idx.sig[name][1]].append(name)
    reach, queue, used = {START}, [START], set()
    while queue:
        cat = queue.pop()
        for name in idx.producers.get(cat, []) + producers.get(cat, []):
            if name not in used and all(a in have for a in idx.sig[name][0]):
                used.add(name)
                for arg in idx.sig[name][0]:
                    if arg not in reach:
                        reach.add(arg)
                        queue.append(arg)
    return used


def _canon(names, strip):
    """{name: its canonical name}: its numbers written `#` where no other of `names` reads so, else itself; spec_rgl
    numbers an actor's, an attribute's, a verb's and a row's functions by their place, which a new term moves."""
    stripped = {n: strip[n] for n in names}
    counts = defaultdict(int)
    for each in stripped.values():
        counts[each] += 1
    return {n: (c if counts[c] == 1 else n) for n, c in stripped.items()}


def rename(text, names):
    """`text` (a tree, a function's or a category's text) with each identifier `names` maps renamed; a quoted string
    kept."""
    return IDENT.sub(lambda m: names.get(m.group(0), m.group(0)), text)


def of(idx, sha, text, words, limit):
    """(the footprint of the GF text `text` (its tokens joined by spaces) as a hex digest, {canonical name: name} of
    the functions its trees may hold): the footprint the sources' sha's when there is no index. The footprint reads
    the functions by their canonical names (`_canon`), so a parse kept under it is renamed to this grammar's."""
    tokens = text.split(" ")
    held = sorted(t for t in set(tokens) if t in words)
    if idx is None:
        return hashlib.sha256(repr(("sha", sha, text, held, limit)).encode()).hexdigest(), {}
    coded = any(t.startswith("`") and t not in words for t in tokens)
    enabled = _enabled(idx, tokens)
    own = [n for n in _used(idx, enabled, _derived(idx, enabled, coded)) if n in idx.text]
    cats = {c for n in own for c in idx.sig[n][0] + (idx.sig[n][1],) if c in idx.lincat}
    canon = _canon(set(own) | cats, idx.strip)
    raw = {n for n, c in canon.items() if c == n and DIGITS.search(n)}     # numbered, and kept so: two read alike

    def said(key, text):
        if key in idx.stripped and not idx.idents[key] & raw:
            return idx.stripped[key]
        return rename(text, {n: canon.get(n, n) for n in idx.idents[key]})
    digest = hashlib.sha256()
    for part in [idx.head, text, repr(held), str(limit)] + sorted(said(n, idx.text[n]) for n in own) + \
            sorted(said(c, idx.lincat[c]) for c in cats):
        digest.update(part.encode())
        digest.update(b"\0")
    return digest.hexdigest(), {c: n for n, c in canon.items() if c != n and n in idx.text}
