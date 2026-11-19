"""The protocol driver of the CLI adapter for scenarios (the domain contract design, §6.2): a request of an operation
with a step's parameters by business name made into the words `spec/adapters/cli.toml` gives it (adapter_cli.argv:
the examples for the parameters a step leaves out), its program run with the `--json` option in the scenario's
repository, and the envelope read back as a `Response`. The Thens' helpers check the envelope: `refused` with the
references it names, `returned` content, and `kept`, the store adapter's check (store_git) that the thing was kept,
and shared when the repository has a remote."""
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import adapter_cli
import domain_envelope
import store_git


@dataclass
class Requested:
    """What one request did: its words, the process, the response read back, and the store's head before it."""
    argv: list
    done: subprocess.CompletedProcess
    response: domain_envelope.Response
    before: object


def request(repo, operation, params=None, without=(), contract_root=None, env=None):
    """Request `operation` of the program `contract_root`'s CLI contract names (default: the repository's own), in
    `repo`, with `params` ({business name: value}) and none of `without`."""
    contract_root = Path(contract_root or repo)
    contract = adapter_cli.read(contract_root)
    assert contract is not None, "no %s under %s" % (adapter_cli.PATH, contract_root)
    words = adapter_cli.argv(contract, operation, params, without)
    program = contract_root / contract.programs[words[0]]
    before = store_git.head(repo)
    done = subprocess.run([sys.executable, str(program), *words[1:], contract.json], cwd=repo, capture_output=True,
                          text=True, env=env)
    try:
        response = domain_envelope.read(done.stdout)
    except ValueError as why:
        raise AssertionError("%s did not print an envelope (%s): %s%s" % (" ".join(words), why, done.stdout,
                                                                          done.stderr)) from None
    return Requested(words, done, response, before)


def refused(requested, *names):
    """The request was refused, its errors naming every one of `names` (business references)."""
    response = requested.response
    named = {n for e in response.errors for n in e["names"]}
    return response.outcome == "refused" and set(names) <= named


def returned(requested):
    """The content of a request that returned it."""
    assert requested.response.outcome == "returned", requested.response
    return requested.response.content


def kept(requested, repo, paths, shared=None):
    """Whether the request kept one commit of `paths` on the branch checked out; with `shared` True or False, also
    whether that commit is (or is not) on the branch's upstream remote."""
    commit = store_git.kept(repo, requested.before, paths)
    if commit is None:
        return False
    return shared is None or store_git.shared(repo, commit) is shared
