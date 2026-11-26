"""An item's `## Requirements` section written back (backlog_section reads it), byte-stable: each capability block in
the capability file's own syntax one heading level down, then the model, adapter, pack, moves, imports and retirements blocks, the universal
block and the index block; a group's text as a capability file holds it (`laid_group`); the requirement ids in file
order (`ids`). Split out of backlog_section, which re-exports what it names here."""
import backlog_adapter
import backlog_area_move
import backlog_import
import backlog_pack
import backlog_retire
from backlog_model import CLOSE as MODEL_CLOSE
from backlog_model import FENCE as MODEL_FENCE

UNIVERSAL, INDEX = "universal", "index"
NEW_FIELDS = ("narrator", "group", "purpose", "area", "kind")  # a new capability's block (`work line --capability`,
REQUIRED = 3                       # b317; its `area:` optional, b645, and after it `kind: port` of a driven port, b701)
FENCE, CLOSE = "```given", "```"
# the blocks of bullets after the pack blocks, in their order: (the Blocks attribute, its module's HEAD, Lines, render)
LISTS = (("moves", backlog_area_move), ("imports", backlog_import), ("retirements", backlog_retire))


def laid_group(group, level="###"):
    """A group's text as in a capability file (`level` its heading): its lines, then its given block."""
    text = "%s [%s] %s" % (level, group.id, group.title) + "".join("\n- [%s] %s" % r for r in group.requirements)
    return text + ("\n\n%s\n%s\n%s" % (FENCE, "\n".join(group.given), CLOSE) if group.given else "")


def render(blocks):
    """The section's text, byte-stable: `read` of it gives `blocks` back."""
    out = []
    for block in blocks:
        parts = ["### %s" % block.capability] + (["language: %s" % block.language] if block.language else [])
        parts += ["\n".join("%s: %s" % f for f in zip(NEW_FIELDS, block.new))] if block.new else []
        retires = "\nretires: [%s]" % ", ".join("%s %s" % p for p in block.retires) if block.retires else ""
        parts += (["retired: [%s]%s" % (", ".join(block.retired), retires)] if block.retired else [])
        parts += ["serves: [%s]" % ", ".join("%s %s" % p for p in block.serves)] if block.serves else []
        parts += ["\n".join(block.terms)] if block.terms else []
        parts += ["\n".join(block.relations)] if block.relations else []
        out.append("\n\n".join(parts + [laid_group(g, "####") for g in block.groups]))
    for model in getattr(blocks, "models", ()):
        parts = ["### %s model" % model.area] + (["%s\n%s\n%s" % (MODEL_FENCE, "\n".join(model.lines), MODEL_CLOSE)]
                                                 if model.lines else [])
        out.append("\n\n".join(parts + (["\n".join(model.terms)] if model.terms else [])))
    out += [backlog_adapter.render(a) for a in getattr(blocks, "adapters", ())]
    out += [backlog_pack.render(a) for a in getattr(blocks, "packs", ())]
    out += [module.render(getattr(blocks, name)) for name, module in LISTS if getattr(blocks, name, None)]
    language, retired = getattr(blocks, "universal_language", None), getattr(blocks, "universal_retired", ())
    if getattr(blocks, "universal", None) or language or retired:
        parts = ["### %s" % UNIVERSAL] + (["language: %s" % language] if language else [])
        parts += ["retired: [%s]" % ", ".join(retired)] if retired else []
        parts += ["\n".join("- [%s] %s" % u for u in blocks.universal)] if blocks.universal else []
        out.append("\n\n".join(parts))
    if getattr(blocks, "upstreams", None):
        out.append("### %s\n\n" % INDEX + "\n".join("- %s" % b for b in blocks.upstreams))
    return "\n\n".join(out)


def ids(blocks):
    """`<capability>#r<n>` of each requirement, in file order."""
    return ["%s#%s" % (b.capability, r) for b in blocks for g in b.groups for r, _ in g.requirements]
