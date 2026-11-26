"""The shop-folder adapter of the contract registry (b636) reading an upstream's folder on GitHub (b587, b591; moved
from contract_obtain): the upstream's contracts kept as `.shop/contracts/<version>/contract.toml` in the GitHub
repository its `github:` under `## Upstreams` in spec/index.md names (request_gh's `repo_of`), read through
`$SHOPSYSTEM_WORK_GH` (`gh api repos/<r>/contents/...`, the raw file, byte for byte). A repository GitHub does not
serve (missing, private or not answering) is refused naming the bounded context and `bounded context unreachable`
(`reached`, checking r89), and one no upstream entry identifies, before any gh call, naming it and `bounded context
not an upstream` (`listed`, b736, checking r132); another gh failure reading a reached repository naming it and `bounded context failing`
(r102); no contract kept, or none at the version, the reply refused as contract_registry's `version not deposited`, naming the
version asked (`published`)."""
import json
import os
import shlex
import subprocess

import contract_registry
from shop_refused import Refused

KEPT = ".shop/contracts"
FILE = "contract.toml"
RAW = "Accept: application/vnd.github.raw"
COMMAND = "spec obtain"


def _gh(root, *args):
    """gh's output as bytes, its line ends as gh wrote them (b594); a gh that fails refused as batch_gh's `gh`."""
    import batch_gh
    argv = shlex.split(os.environ.get(batch_gh.GH) or "gh")
    try:
        done = subprocess.run([*argv, *args], cwd=root, capture_output=True)
    except OSError as err:
        raise Refused("%s: gh %s failed: %s" % (COMMAND, " ".join(args[:2]), err)) from None
    if done.returncode != 0:
        said = done.stderr.decode(errors="replace").strip() or done.stdout.decode(errors="replace").strip()
        raise Refused("%s: gh %s failed: %s" % (COMMAND, " ".join(args[:2]),
                                               (said or "exit %d" % done.returncode).splitlines()[0]))
    return done.stdout


def _unreachable(context, why):
    return Refused("the bounded context {names} cannot be reached: bounded context unreachable (%s)" % why,
                   reason="bounded context unreachable", names=["bounded context:%s" % context])


def _failing(context, why):
    return Refused("the bounded context {names} fails to answer: bounded context failing (%s)" % why,
                   reason="bounded context failing", names=["bounded context:%s" % context])


def _api(root, repo, path, context):
    """The bytes of `path` in `repo` on GitHub, or None when it is not there; another gh failure, of a repository
    `reached` reached, the bounded context failing (b596, checking r102)."""
    try:
        return _gh(root, "api", "-H", RAW, "repos/%s/contents/%s" % (repo, path))
    except Refused as err:
        if "404" in str(err) or "Not Found" in str(err):
            return None
        raise _failing(context, str(err).strip().splitlines()[-1]) from None


def listed(root, context):
    """Refused, naming the bounded context `context`, unless it is this bounded context or an upstream entry under
    `## Upstreams` of spec/index.md identifies it (checking r132)."""
    import request_gh
    import shop_files
    if context != "bounded-context/" + shop_files.context_path(root) and context not in request_gh.bullets(root):
        raise Refused("no upstream entry under ## Upstreams in spec/index.md identifies the bounded context {names}: "
                      "bounded context not an upstream", reason="bounded context not an upstream",
                      names=["bounded context:%s" % context])


def reached(root, context):
    """The GitHub repository of `context`, refused as unreachable unless GitHub serves it (checking r89): one missing,
    private or not answering is a bounded context unreachable, never one with no contract; one no upstream entry
    identifies refused as not an upstream first (`listed`, r132)."""
    import request_gh
    listed(root, context)
    repo = request_gh.repo_of(root, context, COMMAND)
    try:
        _gh(root, "api", "repos/%s" % repo)
    except Refused as err:
        raise _unreachable(context, "gh api repos/%s: %s" % (repo, str(err).strip().splitlines()[-1])) from None
    return repo


def published(root, context, version=None):
    """The reply of the contract `context` keeps as published, or at `version`: returned, else refused."""
    import contract_registry_folder
    repo = reached(root, context)
    if version:
        text = _api(root, repo, "%s/%s/%s" % (KEPT, version, FILE), context)
        if text is None:
            return contract_registry.undeposited(version)
        return contract_registry.returned(version, text)
    listed = _api(root, repo, KEPT, context)
    try:
        entries = json.loads(listed) if listed else []
    except ValueError:
        raise Refused("%s: gh api printed no JSON listing %s of %s" % (COMMAND, KEPT, repo)) from None
    found = None
    for entry in entries if isinstance(entries, list) else []:
        if entry.get("type") != "dir":
            continue
        text = _api(root, repo, "%s/%s/%s" % (KEPT, entry["name"], FILE), context)
        lines = (text or b"").decode("utf-8", errors="replace").splitlines()
        status = contract_registry_folder.STATUS.search("\n".join(lines))
        if status and status.group(1) == "published":
            found = (entry["name"], text)
    if found is None:
        return contract_registry.undeposited(None)
    return contract_registry.returned(*found)
