"""A contract published and fetched (b348, checking r73-r80; the contracts design's C-2), through the contract
registry (contract_registry, b636, checking r125, r127; decision 0139): `spec publish [--version V]` deposits the
context's contract (contract_form) at a version with `status = "published"`, the registry keeping it as the published
one and every contract published before it superseded; a version deposited already is refused naming it, and so is
a context with a requirement that does not conform to the language reference, naming each such requirement. With no
version the contract is deposited at the published one's last number one more, else at `1.0.0`. `spec fetch
[--version V]` retrieves the contract published, or the one at V, and prints it, writing nothing; a version no
contract is deposited at is refused naming it."""
import re

import contract_registry
from shop_refused import Refused

VERSION = re.compile(r"[0-9A-Za-z][0-9A-Za-z.+-]*")


def _published(root):
    """The version of the contract published, None while none is."""
    try:
        return contract_registry.retrieve(root)[0]
    except Refused as err:
        if err.reason != contract_registry.REASON:
            raise
        return None


def _deposited(root, version):
    try:
        contract_registry.retrieve(root, None, version)
    except Refused as err:
        if err.reason != contract_registry.REASON:
            raise
        return False
    return True


def _next(latest):
    if not latest:
        return "1.0.0"
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
    """`spec publish`: the contract deposited at `version` and published, the ones published before superseded."""
    import contract_form
    version = version or _next(_published(root))
    if not VERSION.fullmatch(version):
        raise Refused("the version {names} is refused: version not in the version form",
                      reason="version not in the version form",
                      names=["version:%s" % version])
    if _deposited(root, version):
        raise Refused("a contract is kept at the version {names} already", reason="version already published",
                      names=["version:%s" % version])
    out = nonconforming(root)
    if out:
        raise Refused("these requirements do not conform to the language reference: {names}",
                      reason="requirement not in the language", names=["requirement:%s" % i for i in out])
    lines = contract_form.render(root, version).split("\n")    # context, version, then the status
    done = contract_registry.deposit(root, "\n".join(lines[:2] + ['status = "published"'] + lines[2:]), version)
    print("published %s%s" % (done["kept"], "".join("\nsuperseded %s" % p for p in done["superseded"])))
    return 0


def fetch(root, version=None):
    """`spec fetch`: the contract published, or the one at `version`, retrieved and printed; nothing written."""
    try:
        _, data = contract_registry.retrieve(root, None, version)
    except Refused as err:
        if err.reason != contract_registry.REASON:
            raise
        if version is None:
            raise Refused("no contract is published", reason="version not published") from None
        raise Refused("no contract is kept at the version {names}", reason="version not published",
                      names=["version:%s" % version]) from None
    from domain_envelope import Response
    text = data.decode("utf-8")
    print(text, end="")
    return Response("returned", text)
