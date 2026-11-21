"""The operation table of an operation an item's model lines add (b489, batches r92): an operation a model line of the
item declares that the domain model did not hold before the lay, of which the item holds no operation table and does
not withhold it, and the CLI adapter contract holds no table nor lists under `[unexposed]`, given its table as `work
line --expose <service>.<operation>` writes it (adapter_tables' `of`, b482), so the lay raises no v_a1 (`lay`); taken
out again by the unlay once the model no longer declares the operation, put back as the contract at the batch's base
held it (`unlay`)."""
import re
from pathlib import Path

import adapter_tables
import backlog_adapter
import backlog_model

SERVICE = re.compile(r"^service\s+(.+?)\s*$")
OPERATION = re.compile(r"^\s+operation\s+([^(]+?)\s*\(")


def declared(blocks):
    """The operations `<service>.<operation>` the item's model lines declare, in their order."""
    out = []
    for block in getattr(blocks, "models", ()):
        service = None
        for line in block.lines:
            if (found := SERVICE.match(line)):
                service = found.group(1)
            elif (found := OPERATION.match(line)) and service:
                out.append("%s.%s" % (service, found.group(1)))
            elif line.strip() and not line[:1].isspace():
                service = None
    return list(dict.fromkeys(out))


def _held(into):
    """The operations of the domain model at `into`, by `<service>.<operation>`."""
    import domain_model
    if not (Path(into) / "spec" / "model").is_dir():
        return {}
    return {"%s.%s" % (o.service, o.name): o for o in domain_model.read(into).operations()}


def _given(blocks):
    """The operations the item's adapter blocks of the CLI port table or withhold."""
    return {i for b in getattr(blocks, "adapters", ()) if b.port == backlog_adapter.PORT
            for i in [t for t, _ in b.tables] + list(b.withheld)}


def lay(into, blocks, files):
    """The item's model lines laid (backlog_model), then its adapter blocks (backlog_adapter), then the table of each
    operation the model lines add that nothing names in the CLI contract, the contract's path added to `files`."""
    wanted = declared(blocks)
    before = set(_held(into)) if wanted else set()
    backlog_model.lay(into, blocks, files)
    backlog_adapter.lay(into, blocks, files)
    path = backlog_adapter.contract_path(into, backlog_adapter.PORT)
    new = [i for i in wanted if i not in before and i not in _given(blocks)]
    if not new or not path.is_file():
        return
    text = was = path.read_text(encoding="utf-8")
    held = _held(into)
    for ident in new:
        if ident in held and not adapter_tables.table(text, ident) and ident not in adapter_tables.unexposed(text):
            text = adapter_tables.with_table(text, adapter_tables.of(held[ident], text))
    if text != was:
        path.write_text(text, encoding="utf-8")
        files.append(path.relative_to(into).as_posix())


def unlay(into, blocks, files, base=None):
    """The reverse of `lay`'s tables, after the model lines are out (backlog_model's unlay): the adapter blocks put
    back (backlog_adapter), then each operation the model lines declare that the
    model no longer holds and the item names in no adapter block, its table put back as the contract at `base` held
    it, out when it held none or no base is given."""
    backlog_adapter.unlay(into, blocks, files, base)
    path = backlog_adapter.contract_path(into, backlog_adapter.PORT)
    gone = [i for i in declared(blocks) if i not in _given(blocks)]
    if not gone or not path.is_file():
        return
    held = _held(into)
    text = was = path.read_text(encoding="utf-8")
    at_base = backlog_adapter._at_base(path, base) if base else ""
    for ident in [i for i in gone if i not in held]:
        tables = adapter_tables.table(at_base, ident) if at_base else None
        text = adapter_tables.without(text, ident)
        text = adapter_tables.with_table(text, tables) if tables else text
    if text != was:
        path.write_text(text, encoding="utf-8")
        files.append(path.relative_to(into).as_posix())
