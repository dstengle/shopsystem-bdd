"""A contract obtained from an upstream (b587, checking r81, r82, r88-r90; b591; decision 0117): `spec obtain <bounded
context> [--version V]` reads the upstream's contract kept as published (or the one kept at V) off its GitHub
repository, the `github:` of its bullet under `## Upstreams` in spec/index.md (request_gh's `repo_of`), through
`$SHOPSYSTEM_WORK_GH` (`gh api repos/<r>/contents/.shop/contracts/...`, the raw file), and keeps it, byte for byte, as
`provider/<id's path>/<version>/contract.toml` (`place`: keyed by the whole id, so that two bounded contexts whose
ids end alike never share a folder) in one commit by `shop_files.committed`: the only writer of provider/. It keeps
no context request and opens no issue. An id out of the context id form (migrate init's `FORM`) is refused naming the
id and `id not in the context id form`; a repository GitHub does not serve (`gh api repos/<r>`: missing, private or
not answering) naming the bounded context and `bounded context unreachable`; an upstream with no contract kept, or
none at V, naming the bounded context; a contract kept already at that place is left as it is when the same, and
written again with the upstream's bytes, committed, when another (review f1)."""
import json
from pathlib import Path

from shop_refused import Refused

PROVIDER = Path("provider")
KEPT = ".shop/contracts"
FILE = "contract.toml"
RAW = "Accept: application/vnd.github.raw"
COMMAND = "spec obtain"


def _unreachable(context, why):
    return Refused("the bounded context {names} cannot be reached: bounded context unreachable (%s)" % why,
                   reason="bounded context unreachable", names=["bounded context:%s" % context])


def _reach(root, repo, context):
    """Refused unless GitHub serves the repository `repo` of `context`: one missing, private or not answering is a
    bounded context unreachable, never one with no contract."""
    import batch_gh
    try:
        batch_gh.gh(root, "api", "repos/%s" % repo, command=COMMAND)
    except Refused as err:
        raise _unreachable(context, "gh api repos/%s: %s" % (repo, str(err).strip().splitlines()[-1])) from None


def _api(root, repo, path, context):
    """The text of `path` in `repo` on GitHub, or None when it is not there; another gh failure the bounded context
    unreachable."""
    import batch_gh
    try:
        return batch_gh.gh(root, "api", "-H", RAW, "repos/%s/contents/%s" % (repo, path), command=COMMAND)
    except Refused as err:
        if "404" in str(err) or "Not Found" in str(err):
            return None
        raise _unreachable(context, str(err).strip().splitlines()[-1]) from None


def _none(context, version):
    at = " at the version %s" % version if version else ""
    return Refused("the bounded context {names} has no contract%s" % at, reason="bounded context with no contract",
                   names=["bounded context:%s" % context])


def published(root, context, version=None):
    """(version, text) of the contract `context` keeps as published, or at `version`; refused when it has none."""
    import contract_publish
    import request_gh
    repo = request_gh.repo_of(root, context, COMMAND)
    _reach(root, repo, context)
    if version:
        text = _api(root, repo, "%s/%s/%s" % (KEPT, version, FILE), context)
        if text is None:
            raise _none(context, version)
        return version, text
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
        status = contract_publish.STATUS.search(text or "")
        if status and status.group(1) == "published":
            found = (entry["name"], text)
    if found is None:
        raise _none(context, None)
    return found


def place(context, version):
    """Where a contract of the bounded context `context` at `version` is kept: provider/ keyed by the whole id, the
    id's path after `bounded-context/` (two bounded contexts whose ids end alike each keep their own), then the
    version; `version` may be a glob."""
    return PROVIDER.joinpath(*context.split("/")[1:], version, FILE)


def obtain(root, context, version=None):
    """`spec obtain`: the upstream's contract kept under provider/ and committed; an id out of the context id form
    (migrate init's) refused before anything is read."""
    import shop_files
    from migrate_init import FORM
    if not FORM.fullmatch(context):
        raise Refused("the id {names} is refused: id not in the context id form bounded-context/<domain>/<path>",
                      reason="id not in the context id form", names=["id:%s" % context])
    version, text = published(root, context, version)
    rel = place(context, version).as_posix()
    target = Path(root) / rel
    if target.is_file() and target.read_text(encoding="utf-8") == text:
        print("kept already %s" % rel)
        return 0

    def write():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    shop_files.committed(root, [rel], "spec obtain: the contract of %s at %s" % (context, version), write)
    print("obtained %s" % rel)
    return 0
