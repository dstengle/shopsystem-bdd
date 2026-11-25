"""A contract published and fetched (b348, checking r73-r80; the contracts design's C-2): `spec publish [--version V]`
keeps the context's contract (contract_form) at a version as `.shop/contracts/<version>/contract.toml` with
`status = "published"`, and sets every contract kept as published before it `superseded`, all in one commit; a
version already kept is refused naming it, and so is a context with a requirement that does not conform to the
language reference, naming each such requirement. With no version the contract is kept at the latest kept
version's last number one more, else at `1.0.0`. `spec fetch [--version V]` prints the contract kept as published,
or the one kept at V, writing nothing; a version no contract is kept at is refused naming it."""
import re
from pathlib import Path

from shop_refused import Refused

KEPT = Path(".shop") / "contracts"
FILE = "contract.toml"
STATUS = re.compile(r'^status = "(published|superseded)"$', re.MULTILINE)
VERSION = re.compile(r"[0-9A-Za-z][0-9A-Za-z.+-]*")


def kept(root):
    """{version: (path relative to root, status)} of every contract kept in the context at `root`."""
    out = {}
    for path in sorted((Path(root) / KEPT).glob("*/" + FILE)):
        found = STATUS.search(path.read_text(encoding="utf-8"))
        out[path.parent.name] = (path.relative_to(root).as_posix(), found.group(1) if found else None)
    return out


def _order(version):
    return [(0, int(p), "") if p.isdigit() else (1, 0, p) for p in re.split(r"[.+-]", version)]


def _next(versions):
    if not versions:
        return "1.0.0"
    latest = max(versions, key=_order)
    head, number = re.fullmatch(r"(.*?)(\d*)", latest).groups()
    return "%s%d" % (head, int(number or 0) + 1) if number else latest + ".1"


def nonconforming(root):
    """The id of each requirement of a codified-2 capability that grammar 4 refuses or does not read."""
    import adapter_annotate
    import spec_language
    out = []
    for ident, text in adapter_annotate.requirement_lines(root):
        if spec_language.four(root, ident.split("#")[0]):
            parsed = spec_language.parse(root, text)
            if parsed.refusal or parsed.tree is None:
                out.append(ident)
    return out


def publish(root, version=None):
    """`spec publish`: the contract kept at `version` and published, the ones published before superseded."""
    import contract_form
    import shop_files
    contracts = kept(root)
    version = version or _next(contracts)
    if not VERSION.fullmatch(version):
        raise Refused("the version {names} is not a version", reason="version not a version",
                      names=["version:%s" % version])
    if version in contracts:
        raise Refused("a contract is kept at the version {names} already", reason="version already published",
                      names=["version:%s" % version])
    out = nonconforming(root)
    if out:
        raise Refused("these requirements do not conform to the language reference: {names}",
                      reason="requirement not in the language", names=["requirement:%s" % i for i in out])
    lines = contract_form.render(root, version).split("\n")    # context, version, then the status
    text = "\n".join(lines[:2] + ['status = "published"'] + lines[2:])
    rel = (KEPT / version / FILE).as_posix()
    older = [path for path, status in contracts.values() if status == "published"]

    def write():
        for path in older:
            target = Path(root) / path
            target.write_text(STATUS.sub('status = "superseded"', target.read_text(encoding="utf-8")),
                              encoding="utf-8")
        target = Path(root) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    shop_files.committed(root, older + [rel], "spec publish: the contract at %s" % version, write)
    print("published %s%s" % (rel, "".join("\nsuperseded %s" % p for p in older)))
    return 0


def fetch(root, version=None):
    """`spec fetch`: the contract kept as published, or the one kept at `version`, printed; nothing written."""
    contracts = kept(root)
    if version is None:
        found = [path for path, status in contracts.values() if status == "published"]
        if not found:
            raise Refused("no contract is published", reason="version not published")
        path = found[-1]
    elif version not in contracts:
        raise Refused("no contract is kept at the version {names}", reason="version not published",
                      names=["version:%s" % version])
    else:
        path = contracts[version][0]
    from domain_envelope import Response
    text = (Path(root) / path).read_text(encoding="utf-8")
    print(text, end="")
    return Response("returned", text)
