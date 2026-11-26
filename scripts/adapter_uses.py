"""The provider operations an adapter spec uses (b637, checking r135, r136, product r35; decision 0138): for each
operation of its parent's driven port that it realises, the set of provider operations used to realise it, of one
provider or several, never one to one. Written in the adapter spec's own spec/index.md as the block list `uses:`, one
entry a pair `<port service>.<operation> → <provider service>.<operation> [of <provider id>]`, several entries of one
port operation its set; the provider id may be left out, any provider the adapter spec holds a contract of then
(`entries`). The port operations it realises are those a port line it `realises:` governs (adapter_annotate's
`governing` over the parent, a port line one of a capability whose area is of kind `port`: `realised`).

Its problems (`problems`, which model_adapter's `path` adds): an entry that does not read; a provider operation no
contract the adapter spec holds declares as `[operations."S.O"]` (of the provider the entry names, when it names one:
r135); a port operation it realises that no entry names (r136). What a provider operation's held contract says governs
it (`governed`) is what product_trace follows a trace into (r35)."""
import re
from pathlib import Path

from model_parse import as_list, frontmatter

OP = r"[a-z0-9][\w-]*\.[a-z0-9][\w-]*"
ENTRY = re.compile(rf"^(?P<port>{OP})\s*(?:→|->)\s*(?P<used>{OP})(?:\s+of\s+(?P<provider>\S+))?$")


def _index(root):
    path = Path(root) / "spec" / "index.md"
    return frontmatter(path.read_text())[0] if path.is_file() else {}


def entries(root):
    """([(port operation, provider operation, provider id or None)], [the text of each entry that does not read])."""
    read, unread = [], []
    for given in as_list(_index(root).get("uses")):
        m = ENTRY.match(str(given).strip())
        if not m:
            unread.append(str(given))
            continue
        provider = m.group("provider")
        read.append((m.group("port"), m.group("used"), provider.partition("@")[0] if provider else None))
    return read, unread


def _ported(parent):
    """{capability name} of the parent's capabilities whose area is of kind `port`."""
    import domain_model
    if not domain_model.exists(parent):
        return set()
    ports = {name for name, area in domain_model.load(parent).areas.items() if area.kind == "port"}
    out = set()
    for path in sorted((Path(parent) / "spec" / "capabilities").glob("*.md")):
        area = str(frontmatter(path.read_text())[0].get("area", "") or path.stem)
        if area in ports:
            out.add(path.stem)
    return out


def realised(root, governing=None):
    """{port operation: [port line id]} of each operation a port line the adapter spec realises governs; `governing`
    the parent's (adapter_annotate's), read when not given."""
    ids = [str(i).strip() for i in as_list(_index(root).get("realises"))]
    parent = Path(root).parent.parent
    ports = _ported(parent)
    ports_ids = [i for i in ids if i.partition("#")[0] in ports]
    if not ports_ids:
        return {}
    if governing is None:
        import adapter_annotate
        governing = adapter_annotate.governing(parent)
    out = {}
    for op, lines in governing.items():
        held = [rid for rid, _ in lines if rid in ports_ids]
        if held:
            out[op] = held
    return out


def held(root):
    """[(provider id, version, {operation: [requirement]})] of each contract the adapter spec holds."""
    import adapter_provider
    return [(provider, str(contract.get("version", "")),
             {op: list(table.get("requirements", [])) for op, table in contract.get("operations", {}).items()})
            for _, provider, contract in adapter_provider.contracts(root)]


def governed(root, port_op, contracts=None):
    """[(requirement, provider id, version, provider operation)] of each requirement a held contract lists under a
    provider operation the adapter spec uses for `port_op`."""
    contracts = held(root) if contracts is None else contracts
    out = []
    for port, used, named in entries(root)[0]:
        if port != port_op:
            continue
        for provider, version, ops in contracts:
            if (named is None or named == provider) and used in ops:
                out += [(req, provider, version, used) for req in ops[used]]
    return out


def problems(root):
    """A file problem for each entry that does not read, each provider operation no held contract declares, and each
    port operation the adapter spec realises that uses no operation."""
    read, unread = entries(root)
    out = ["spec/index.md: uses %r, which is not <port service>.<operation> → <provider service>.<operation> "
           "[of <provider id>]" % text for text in unread]
    contracts = held(root)
    for port, used, named in read:
        if not any((named is None or named == provider) and used in ops for provider, _, ops in contracts):
            out.append("spec/index.md: uses %s → %s, an operation no contract the adapter spec holds%s declares"
                       % (port, used, " of %s" % named if named else ""))
    said = {port for port, _, _ in read}
    out += ["spec/index.md: the port operation %s, which %s governs, uses no operation; name the provider operations "
            "it uses under uses:" % (op, ", ".join(ids)) for op, ids in sorted(realised(root).items()) if op not in said]
    return out
