"""A contract obtained from an upstream (b587, checking r81, r82, r88-r90; b591; decision 0117), retrieved from the
contract registry (contract_registry, b636, checking r126; decision 0139): `spec obtain <bounded context> [--version
V]` retrieves the upstream's contract published (or the one at V) and keeps it, byte for byte, in each adapter spec
of its provider (b593, checking r91; decision 0136): an adapter spec `adapters/<name>/` whose `providers:` name the
bounded context (`holders`), each at the version it pins the provider at, else the one asked or published (b599,
checking r100), where the registry's adapter places it (contract_registry_folder's `place`, which its provider
check, model_adapter's `uncontracted`, reads), in one commit by `shop_files.committed`: the only writer of provider/,
nothing kept at the repository root. It keeps no context request and opens no issue. In this order: an id out of the
context id form (migrate init's `FORM`) is refused naming the id and `id not in the context id form` (r88); an
upstream no upstream entry identifies, outside the shop, naming the bounded context and `bounded context not an
upstream` (r132); an upstream the registry cannot reach naming the bounded context and `bounded context unreachable`
(r89), and one failing `bounded context failing` (r102, r133); a bounded context no adapter spec has as its provider naming the provider and `no adapter spec has the provider` (b593, r103:
only of an available provider in the context id form, b601); an upstream with no contract deposited, or none at V,
naming the bounded context and the version (r130); a contract kept already at that place is left as it is when the same, and written again
with the upstream's bytes, committed, when another (review f1)."""
from pathlib import Path

import contract_registry
from contract_registry_folder import place
from shop_refused import Refused

ADAPTERS = "adapters"


def _none(context, version):
    if not version:
        return Refused("the bounded context {names} has no contract", reason="bounded context with no contract",
                       names=["bounded context:%s" % context])
    return Refused("no contract is deposited for the bounded context and the version {names}",
                   reason="bounded context with no contract",
                   names=["bounded context:%s" % context, "version:%s" % version])


def retrieved(root, context, version):
    """(version, bytes) of the contract of `context` the registry returns, at `version` or published; a retrieval it
    refuses refused naming the bounded context (r82) and the version (r130), nothing written."""
    reply = contract_registry.retrieve(root, context, version)
    if reply.outcome == "returned":
        return reply.content
    raise _none(context, contract_registry.refused_version(reply, version))


def _reach(root, context):
    """Refused when the registry cannot read `context`: no upstream entry identifies it (r132), it cannot be reached
    (r89) or it fails (r133), each before r103 (b601, b736); a retrieve's reply, `version not deposited` among them,
    lets the caller's refusal stand."""
    contract_registry.retrieve(root, context, None)


def holders(root, context):
    """(folder, version) of each adapter spec `adapters/<name>/` whose spec/index.md says `kind: adapter` and whose
    `providers:` name the bounded context `context`, its folder relative to `root`, in name order; the version it pins
    the provider at (`<id>@<version>`, in the version form), else None (b599, checking r100)."""
    import contract_publish
    import model_adapter
    from model_parse import as_list, frontmatter
    out = []
    for index in sorted(Path(root).glob("%s/*/spec/index.md" % ADAPTERS)):
        data = frontmatter(index.read_text())[0]
        if str(data.get("kind", "")).strip() != model_adapter.KIND:
            continue
        named = (model_adapter.PROVIDER.match(str(given).strip()) for given in as_list(data.get("providers")))
        found = next((m for m in named if m and m.group("id") == context), None)
        if found:
            pin = found.group("version")
            pinned = pin if pin and contract_publish.VERSION.fullmatch(pin) else None
            out.append((index.parent.parent.relative_to(root), pinned))
    return out


def obtain(root, context, version=None):
    """`spec obtain`: the upstream's contract kept under provider/ of each adapter spec of it (at the version it
    pins, else `version`, else the published one) and committed; an id out
    of the context id form (migrate init's) refused before anything is read, then an upstream no upstream entry
    identifies, one GitHub does not serve or one failing (r132, r89, r133), and only then one no adapter spec has as its provider (checking r88, r89 before r103: review f1, b601)."""
    import shop_files
    from migrate_init import FORM
    if not FORM.fullmatch(context):
        raise Refused("the id {names} is refused: id not in the context id form bounded-context/<domain>/<path>",
                      reason="id not in the context id form", names=["id:%s" % context])
    held = holders(root, context)
    if not held:
        _reach(root, context)
        raise Refused("the provider {names} is the provider of no adapter spec under %s/: no adapter spec has the "
                      "provider" % ADAPTERS, reason="no adapter spec has the provider", names=["provider:%s" % context])
    texts, rels = {}, {}
    for folder, pin in held:
        wanted = pin or version
        if wanted not in texts:
            texts[wanted] = retrieved(root, context, wanted)
        at, text = texts[wanted]
        rels[(folder / place(context, at)).as_posix()] = text
    changed = [rel for rel, text in rels.items()
               if not ((Path(root) / rel).is_file() and (Path(root) / rel).read_bytes() == text)]
    for rel in rels:
        if rel not in changed:
            print("kept already %s" % rel)
    if not changed:
        return 0

    def write():
        for rel in changed:
            (Path(root) / rel).parent.mkdir(parents=True, exist_ok=True)
            (Path(root) / rel).write_bytes(rels[rel])
    versions = ", ".join(sorted({at for at, _ in texts.values()}))
    shop_files.committed(root, changed, "spec obtain: the contract of %s at %s" % (context, versions), write)
    for rel in changed:
        print("obtained %s" % rel)
    return 0
