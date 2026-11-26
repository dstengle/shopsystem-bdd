"""A stand-in adapter of the contract registry (b636), which `$SHOPSYSTEM_CONTRACT_REGISTRY` names in checking's
scenarios of g126-g131: each request recorded as one JSON line in the file `$STAND_IN_REGISTRY_CALLS` names (its
operation, the bounded context, the version and the contract deposited), then answered as `$STAND_IN_REGISTRY_REPLY`
says: unset, as the shop-folder adapter beside it answers, so the command behaves as it does with that adapter wired
in; `complete`, the deposit made of the shop-folder adapter and its completion recorded (`completed`) before the reply;
`return`, the stand-in's own contract (`CONTRACT`, unlike any the folder keeps); `refuse`, the retrieve refused at the
version asked, `version not deposited`, whatever the folder holds, and the deposit refused naming its version,
`contract not deposited`, nothing written (b736, checking r134). Loaded by contract_registry from its path."""
import json
import os

import contract_registry_folder as FOLDER
from domain_envelope import Response, error

CONTRACT = 'context = "the stand-in registry"\nversion = "%s"\nstatus = "published"\n'


def _record(operation, context, version, contract=None):
    with open(os.environ["STAND_IN_REGISTRY_CALLS"], "a", encoding="utf-8") as out:
        out.write(json.dumps({"operation": operation, "context": context, "version": version,
                              "contract": contract}) + "\n")


def _reply():
    return os.environ.get("STAND_IN_REGISTRY_REPLY", "")


def deposit(root, contract, version):
    _record("deposit", None, version, contract)
    if _reply() == "refuse":
        return Response("refused", errors=[error("contract not deposited", ["version:%s" % version])])
    done = FOLDER.deposit(root, contract, version)
    if _reply() == "complete" and done.outcome == "done":
        _record("completed", None, version)
    return done


def retrieve(root, context=None, version=None):
    _record("retrieve", context, version)
    if _reply() == "return":
        return Response("returned", (version or "1.0.0", (CONTRACT % (version or "1.0.0")).encode()))
    if _reply() == "refuse":
        return Response("refused", errors=[error("version not deposited", ["version:%s" % version])])
    return FOLDER.retrieve(root, context, version)
