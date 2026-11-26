"""A stand-in adapter of the contract registry (b636), which `$SHOPSYSTEM_CONTRACT_REGISTRY` names in checking's
scenarios of g125-g127: each request recorded as one JSON line in the file `$STAND_IN_REGISTRY_CALLS` names (its
operation, the bounded context, the version and the contract deposited), then made of the shop-folder adapter beside
it, so the command behaves as it does with the adapter wired in. Loaded by contract_registry from its path."""
import json
import os

import contract_registry_folder as FOLDER


def _record(operation, context, version, contract=None):
    with open(os.environ["STAND_IN_REGISTRY_CALLS"], "a", encoding="utf-8") as out:
        out.write(json.dumps({"operation": operation, "context": context, "version": version,
                              "contract": contract}) + "\n")


def deposit(root, contract, version):
    _record("deposit", None, version, contract)
    return FOLDER.deposit(root, contract, version)


def retrieve(root, context=None, version=None):
    _record("retrieve", context, version)
    return FOLDER.retrieve(root, context, version)
