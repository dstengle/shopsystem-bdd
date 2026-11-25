"""An adapter spec in `spec check` (b540, checking r84-r87; decisions 0123, 0124, 0117): a spec whose spec/index.md
says `kind: adapter`, kept nested in its bounded context's spec at `adapters/<name>/`, so that its parent is the spec
two folders up. Its id conforms to the adapter spec id form, the parent's id followed by `/adapter/<name>` (`path`:
the id's path after `bounded-context/`, else a file problem naming the id), its `<name>` the folder that keeps it
(b595, checking r92, else a file problem naming the id); each id under its `realises:` is a live requirement
`<capability>#r<n>` of the parent's spec (`unrealised`); each provider under its `providers:`
(`<bounded context id>[@<version>]`) has its contract held, `provider/<id's path>/<version>/contract.toml` where
`spec obtain` keeps it (contract_obtain's `place`), any version when none is named, a version that does not conform
to the version form (contract_publish's `VERSION`) a file problem naming it, never matched as a pattern (b595,
checking r93) (`uncontracted`). Its `adr/`, the adapter decisions, and `provider/` are accepted as they are; nothing
here reads them further."""
import re

import contract_obtain
import contract_publish
import spec_read
from model_parse import as_list, frontmatter

KIND = "adapter"
NAME = r"[a-z0-9]+(?:-[a-z0-9]+)*"
CONTEXT_PATH = rf"{NAME}(?:\.{NAME})*/{NAME}/{NAME}"     # <owner>/<product>/<context name>; the owner may be a domain
REQ = re.compile(r"^(?P<cap>[a-z0-9]+(?:-[a-z0-9]+)*)#(?P<r>r[1-9]\d*)$")
PROVIDER = re.compile(rf"^(?P<id>bounded-context/{CONTEXT_PATH})(?:@(?P<version>\S+))?$")


def parent_id(root):
    """The id of the bounded context whose spec holds `root` at `adapters/<name>/`, or None."""
    index = root.parent.parent / "spec" / "index.md"
    if root.parent.name != "adapters" or not index.is_file():
        return None
    found = frontmatter(index.read_text())[0].get("id")
    return str(found) if found else None


def path(root, data, ident, problems):
    """The context path of the id `ident` of spec/index.md's frontmatter `data`, or None with its problem added: a
    bounded context's `bounded-context/<owner>/<product>/<context name>`, an adapter spec's its parent's id followed
    by `/adapter/<name>` (its parent's form when no parent spec holds it); an adapter spec's own problems added."""
    ident = str(ident)
    if str(data.get("kind", "")).strip() != KIND:
        m = re.fullmatch(rf"bounded-context/({CONTEXT_PATH})", ident)
        if not m:
            problems.append(f"spec/index.md: id {ident!r} is not bounded-context/<owner>/<product>/<context name>")
        return m and m.group(1)
    parent = parent_id(root)
    head = re.escape(parent) if parent else rf"bounded-context/{CONTEXT_PATH}"
    if not re.fullmatch(rf"{head}/adapter/{NAME}", ident):
        problems.append(f"spec/index.md: id {ident!r} does not conform to the adapter spec id form "
                        f"{parent or 'bounded-context/<owner>/<product>/<context name>'}/adapter/<name>")
        return None
    if not ident.endswith("/adapter/" + root.name):
        problems.append(f"spec/index.md: id {ident!r} does not match the adapter spec: it names no folder "
                        f"adapters/{ident.rpartition('/')[2]}/, the adapter spec is kept at adapters/{root.name}/")
        return None
    problems.extend(unrealised(root, as_list(data.get("realises"))) + uncontracted(root, as_list(data.get("providers"))))
    return ident.partition("/")[2]


def unrealised(root, ids):
    """A problem for each id under `realises:` that names no live requirement of the parent's spec."""
    spec = root.parent.parent / "spec" / "capabilities"
    out = []
    for ident in ids:
        m = REQ.match(str(ident).strip())
        if not m:
            out.append(f"spec/index.md: realises {ident!r}, which is not <capability>#r<n>")
            continue
        file = spec / f"{m.group('cap')}.md"
        live = {q.id for g in spec_read.capability(file).groups for q in g.requirements} if file.is_file() else set()
        if m.group("r") not in live:
            out.append(f"spec/index.md: realises the requirement id {ident}, which no requirement has")
    return out


def uncontracted(root, providers):
    """A problem for each provider under `providers:` whose contract the adapter spec does not hold."""
    out = []
    for given in providers:
        m = PROVIDER.match(str(given).strip())
        if not m:
            out.append(f"spec/index.md: the provider {given!r} is not <bounded context id>[@<version>]")
            continue
        if m.group("version") and not contract_publish.VERSION.fullmatch(m.group("version")):
            out.append(f"spec/index.md: the provider {m.group('id')} has the version {m.group('version')!r}, which "
                       "does not conform to the version form")
            continue
        kept = contract_obtain.place(m.group("id"), m.group("version") or "*")
        if not any(root.glob(kept.as_posix())):
            out.append(f"spec/index.md: the provider {m.group('id')} has no contract the adapter spec holds under "
                       f"{kept.parent.as_posix()}/")
    return out
