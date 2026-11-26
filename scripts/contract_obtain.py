"""A contract obtained from an upstream (b587, checking r81, r82, r88-r90; b591; decision 0117), retrieved from the
contract registry (contract_registry, b636, checking r126; decisions 0147, 0149): `spec obtain <bounded context>
[--version V]` retrieves the upstream's contract published (or the one at V) and requests the registry to register it,
byte for byte, for each adapter spec of its provider (b735, checking r137): an adapter spec `adapters/<name>/` whose
`providers:` name the bounded context (`holders`), each at the version it pins the provider at, else the one asked or
published (checking r138). Where and how a registered contract is kept is the registry's adapter's; a register
completed prints what it kept, `obtained <it>`, or `kept already <it>` when it was kept so already (r139), and one
refused is refused naming the adapter spec and `contract not registered`, nothing more requested (r140). It keeps no
context request and opens no issue. In this order: an id out of the context id form (migrate init's `FORM`) is
refused naming the id and `id not in the context id form` (r88); an upstream no upstream entry identifies, outside
the shop, naming the bounded context and `bounded context not an upstream` (r132); an upstream the registry cannot
reach naming the bounded context and `bounded context unreachable` (r89), and one failing `bounded context failing`
(r102, r133); a bounded context no adapter spec has as its provider naming the provider and `no adapter spec has the
provider` (b593, r103: only of an available provider in the context id form, b601); an upstream with no contract
deposited, or none at V, naming the bounded context and the version (r130)."""
from pathlib import Path

import contract_registry
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
    the provider at (`<id>@<version>`, in the version form), else None (b599, checking r138)."""
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
    """`spec obtain`: the upstream's contract registered for each adapter spec of it (at the version it pins, else
    `version`, else the published one), each reply acted on; an id out
    of the context id form (migrate init's) refused before anything is read, then an upstream no upstream entry
    identifies, one GitHub does not serve or one failing (r132, r89, r133), and only then one no adapter spec has as its provider (checking r88, r89 before r103: review f1, b601)."""
    from migrate_init import FORM
    if not FORM.fullmatch(context):
        raise Refused("the id {names} is refused: id not in the context id form bounded-context/<domain>/<path>",
                      reason="id not in the context id form", names=["id:%s" % context])
    held = holders(root, context)
    if not held:
        _reach(root, context)
        raise Refused("the provider {names} is the provider of no adapter spec under %s/: no adapter spec has the "
                      "provider" % ADAPTERS, reason="no adapter spec has the provider", names=["provider:%s" % context])
    texts, replies = {}, []
    for folder, pin in held:
        wanted = pin or version
        if wanted not in texts:
            texts[wanted] = retrieved(root, context, wanted)
        at, text = texts[wanted]
        reply = contract_registry.register(root, text, folder.as_posix(), context, at)
        if reply.outcome != "done":
            raise Refused("the contract registry refused to register the contract of %s at %s for the adapter spec "
                          "{names}: contract not registered" % (context, at), reason=contract_registry.UNREGISTERED,
                          names=["adapter spec:%s" % folder.as_posix()])
        replies.append(reply.content)
    for kept in replies:
        print(("obtained %s" if kept["changed"] else "kept already %s") % kept["kept"])
    return 0
