"""A contract published and fetched (b348, checking r73-r80; the contracts design's C-2), through the contract
registry (contract_registry, b636, checking r127, r131; decision 0139): `spec publish [--version V]` deposits the
context's contract (contract_form) at a version with `status = "published"`, the registry keeping it as the published
one and every contract published before it superseded, and keeps it once the registry completes the deposit (r128:
the command's report of the contract kept, a deposit not completed refused naming the version); a version deposited already is refused naming it, and so is
a context with a requirement that does not conform to the language reference, naming each such requirement. With no
version the contract is deposited at the published one's last number one more, else at `1.0.0`, its last number
raised again past each version deposited already (a superseded one higher than the published one among them). `spec fetch
[--version V]` retrieves the contract published, or the one at V, and prints it, writing nothing; a version no
contract is deposited at is refused naming it. Fetch returns the contract the registry returns (r129) and, when the
registry refuses the retrieval, names the version and changes nothing (r130)."""
import re

import contract_registry
from shop_refused import Refused

VERSION = re.compile(r"[0-9A-Za-z][0-9A-Za-z.+-]*")


def _published(root):
    """The version of the contract published, None while none is."""
    reply = contract_registry.retrieve(root)
    return reply.content[0] if reply.outcome == "returned" else None


def _deposited(root, version):
    return contract_registry.retrieve(root, None, version).outcome == "returned"


def _next(latest):
    if not latest:
        return "1.0.0"
    head, number = re.fullmatch(r"(.*?)(\d*)", latest).groups()
    return "%s%d" % (head, int(number or 0) + 1) if number else latest + ".1"


def _default(root):
    """The version `spec publish` takes with none: past the published one and past every version deposited."""
    version = _next(_published(root))
    while _deposited(root, version):
        version = _next(version)
    return version


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
    version = version or _default(root)
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
    reply = contract_registry.deposit(root, "\n".join(lines[:2] + ['status = "published"'] + lines[2:]), version)
    if reply.outcome != "done":     # kept only once the registry completes the deposit (r128)
        raise Refused("the contract registry did not deposit the contract at the version {names}",
                      reason=reply.errors[0]["reason"] if reply.errors else "contract not deposited",
                      names=["version:%s" % version])
    done = reply.content
    print("published %s%s" % (done["kept"], "".join("\nsuperseded %s" % p for p in done["superseded"])))
    return 0


def fetch(root, version=None):
    """`spec fetch`: the contract the registry returns, published or at `version`, printed (r129); a retrieval it
    refuses refused naming the version (r130); nothing written."""
    reply = contract_registry.retrieve(root, None, version)
    if reply.outcome != "returned":
        named = contract_registry.refused_version(reply, version)
        if named is None:
            raise Refused("no contract is published", reason="version not published")
        raise Refused("no contract is kept at the version {names}", reason="version not published",
                      names=["version:%s" % named])
    from domain_envelope import Response
    text = reply.content[1].decode("utf-8")
    print(text, end="")
    return Response("returned", text)
