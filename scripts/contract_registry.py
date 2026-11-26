"""The contract registry, a driven port of the specification (b636, contract-registry r1-r3; checking r125-r127;
decision 0139): the one module the specification's contract commands reach it through. `deposit(root, contract,
version)` gives the registry the contract (its text) to keep at the version as this bounded context's published one;
`retrieve(root, context, version)` asks it for the contract of the bounded context `context` (None: this one) at the
version (None: the one published), (version, bytes), a version never deposited refused naming it (`version not
deposited`, through shop_refused's Refused). The adapter wired in is the shop-folder adapter
(contract_registry_folder; decision 0125); `$SHOPSYSTEM_CONTRACT_REGISTRY` names the file of another adapter run in
its place, a stand-in the tests swap in as `$SHOPSYSTEM_WORK_GH` names a stand-in gh (`adapter`)."""
import importlib.util
import os

from shop_refused import Refused

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
    """The contract kept at `version` as this bounded context's published one; what the adapter says it kept."""
    return adapter().deposit(root, contract, version)


def retrieve(root, context=None, version=None):
    """(version, bytes) of the contract of `context` (None: this bounded context) at `version` (None: published)."""
    return adapter().retrieve(root, context, version)


def undeposited(version):
    """The refusal of a retrieve at a version never deposited, naming it (with none, of no contract published)."""
    if version:
        return Refused("no contract is deposited at the version {names}", reason=REASON, names=["version:%s" % version])
    return Refused("no contract is published", reason=REASON)
