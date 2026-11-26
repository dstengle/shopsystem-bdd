"""The contract registry, a driven port of the specification (b636, contract-registry r1-r3; checking r126, r127, r131;
decision 0139): the one module the specification's contract commands reach it through. `deposit(root, contract,
version)` gives the registry the contract (its text) to keep at the version as this bounded context's published one;
`retrieve(root, context, version)` asks it for the contract of the bounded context `context` (None: this one) at the
version (None: the one published). Each answers with its reply, a domain_envelope Response, which the caller handles
(checking r128-r130): a deposit completed (`completed`: done, what was kept), a contract returned (`returned`:
(version, bytes)), a version never deposited refused naming it (`undeposited`: `version not deposited`); a failure
outside the operation's outcomes (an upstream unreachable) is raised as shop_refused's Refused. The adapter wired in is the shop-folder adapter
(contract_registry_folder; decision 0125); `$SHOPSYSTEM_CONTRACT_REGISTRY` names the file of another adapter run in
its place, a stand-in the tests swap in as `$SHOPSYSTEM_WORK_GH` names a stand-in gh (`adapter`)."""
import importlib.util
import os

from domain_envelope import Response, error

ADAPTER = "SHOPSYSTEM_CONTRACT_REGISTRY"
REASON = "version not deposited"


def adapter():
    """The adapter of the port: the module of the file `$SHOPSYSTEM_CONTRACT_REGISTRY` names, else the shop folder's."""
    path = os.environ.get(ADAPTER)
    if not path:
        import contract_registry_folder
        return contract_registry_folder
    spec = importlib.util.spec_from_file_location("contract_registry_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deposit(root, contract, version):
    """The registry's reply to a deposit of the contract at `version` as this bounded context's published one."""
    return adapter().deposit(root, contract, version)


def retrieve(root, context=None, version=None):
    """The registry's reply to a retrieve of the contract of `context` (None: this bounded context) at `version`
    (None: published): returned, (version, bytes), or refused."""
    return adapter().retrieve(root, context, version)


def completed(kept):
    """The reply of a deposit completed: done, with what the adapter kept."""
    return Response("done", kept)


def returned(version, data):
    """The reply of a retrieve answered: returned, the contract's version and bytes."""
    return Response("returned", (version, data))


def undeposited(version):
    """The reply of a retrieve at a version never deposited: refused, naming it (with none, no contract published)."""
    return Response("refused", errors=[error(REASON, ["version:%s" % version] if version else [])])


def refused_version(reply, version=None):
    """The version a refused retrieve is about: the one asked, else the one the refusal names, else None."""
    named = [n.split(":", 1)[1] for e in reply.errors for n in e["names"] if n.startswith("version:")]
    return version or (named[0] if named else None)
