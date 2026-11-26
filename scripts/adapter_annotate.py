"""`spec annotate` (checking r48-r51, b368): each operation of an adapter contract given the requirements that govern
it, generated from the spec, and the contract checked current.

A requirement governs an operation when its trigger is a request of the operation (model_domain_lines' `requester`
of the requirement's logical form): its lines say what the operation does, its refusals among them, which are so
the operation's outcomes. The CLI adapter's contract (`spec/adapters/cli.toml`, adapter_cli) holds them under each
`[operations."<service>.<operation>"]` table as `requirements = ["<capability>#r<n>: <line>", ...]`, in the order of
the capabilities' names and the requirements' numbers; an operation no requirement governs holds no such key. The
HTTP adapter's OpenAPI document will hold the same lines under each operation's `x-requirements` (b366).

`governing(root)` gives {operation: [(id, line)]}; `annotated(text, governing)` the contract's text with each
operation's requirements written again, every other line kept; `annotate(root, audit)` writes each stale contract,
or with the audit names each and writes nothing (exit 1). `spec check`'s v_a5 and v_a6 read the same facts (model.lp:
`requester`, `contract_op`, `op_holds`)."""
import json
import re
import sys
from pathlib import Path

import adapter_cli
from plumbing.shop_refused import Refused

KEY = "requirements"
HEADER = re.compile(r'^\[operations\."(?P<op>[^"]+)"\]\s*$')


def contracts(root):
    """The adapter contracts of the context at `root` that it holds (their paths from the root)."""
    return [adapter_cli.PATH] if adapter_cli.exists(root) else []


def requirement_lines(root):
    """(id, line) of every requirement of a codified capability, by capability name and number (as `spec check` reads them)."""
    import spec_read
    out = []
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        doc = spec_read.capability(path)
        for g in doc.groups:
            out += [("%s#%s" % (doc.name, q.id), q.text) for q in g.requirements]
    return sorted(out, key=lambda x: (x[0].split("#")[0], int(x[0].split("#r")[1])))


def governing(root):
    """{operation id: [(requirement id, line)]} of every operation some requirement of the context governs."""
    import domain_model
    if not domain_model.exists(root):
        return {}
    import model_domain_lines
    import spec_grammar4
    import spec_language
    import spec_lexicon
    import spec_lf
    lines = model_domain_lines.Lines(domain_model.load(root), spec_lexicon.read(root),
                                    spec_grammar4.sources(root)[0].verbs)
    vocab, out = None, {}
    for ident, text in requirement_lines(root):
        parsed = spec_language.parse(root, text)
        if parsed.tree is None:
            continue
        vocab = vocab or spec_grammar4.load(root)[0]
        for fact in lines.facts(ident, spec_lf.form(vocab, parsed.tree)):
            if fact[0] == "requester" and (ident, text) not in out.setdefault(fact[2], []):
                out[fact[2]].append((ident, " ".join(text.split())))
    return out


def held(contract):
    """{operation id: [requirement id]} of what each operation of a read contract holds."""
    return {ident: list(op.requirements) for ident, op in contract.operations.items()}


def _block(entries):
    if not entries:
        return []
    return ["%s = [" % KEY] + ["  %s," % json.dumps("%s: %s" % e, ensure_ascii=False) for e in entries] + ["]"]


def annotated(text, governs):
    """The contract's text with each `[operations."<id>"]` table's requirements written again from `governs`."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        found = HEADER.match(lines[i])
        out.append(lines[i])
        i += 1
        if not found:
            continue
        body = []
        while i < len(lines) and not lines[i].startswith("["):
            if lines[i].startswith("%s = [" % KEY) or lines[i].startswith("%s=[" % KEY):
                while i < len(lines) and lines[i].rstrip() != "]" and not lines[i].rstrip().endswith("]"):
                    i += 1
                i += 1
                continue
            body.append(lines[i])
            i += 1
        keys = len(body)
        while keys and (not body[keys - 1].strip() or body[keys - 1].lstrip().startswith("#")):
            keys -= 1
        out += body[:keys] + _block(governs.get(found.group("op"), [])) + body[keys:]
    return "\n".join(out)


def stale(root, governs=None, named=()):
    """[(path, text it should hold)] of each adapter contract of `root` (or of those `named`) that is not as annotate
    writes it; a named path that is no adapter contract of the context refused naming it."""
    known = [str(p) for p in contracts(root)]
    for name in named:
        if str(Path(name)) not in known:
            raise Refused("%s is no adapter contract of this bounded context (%s)" % (name, ", ".join(known) or "none"))
    governs = governing(root) if governs is None else governs
    out = []
    for rel in [Path(n) for n in named] or contracts(root):
        text = (Path(root) / rel).read_text(encoding="utf-8")
        want = annotated(text, governs)
        if want != text:
            out.append((str(rel), want))
    return out


def annotate(root, audit=False, named=()):
    """Each stale adapter contract written (`annotated <path>`), each other `current <path>`; with the audit each
    stale one named on stderr, nothing written, exit 1."""
    found = stale(root, named=named)
    if audit:
        for rel, _ in found:
            print("spec annotate: %s is stale: its operations do not hold the requirements that govern them; run "
                  "`spec annotate`" % rel, file=sys.stderr)
        return 1 if found else 0
    for rel, want in found:
        (Path(root) / rel).write_text(want, encoding="utf-8")
        print("annotated %s" % rel)
    for rel in sorted(set(named or map(str, contracts(root))) - {r for r, _ in found}):
        print("current %s" % rel)
    return 0
