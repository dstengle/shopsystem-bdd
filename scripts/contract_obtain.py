"""A contract obtained from an upstream (b587, checking r81, r82, r88-r90; b591; decision 0117): `spec obtain <bounded
context> [--version V]` reads the upstream's contract kept as published (or the one kept at V) off its GitHub
repository, the `github:` of its bullet under `## Upstreams` in spec/index.md (request_gh's `repo_of`), through
`$SHOPSYSTEM_WORK_GH` (`gh api repos/<r>/contents/.shop/contracts/...`, the raw file), and keeps it, byte for byte, in
each adapter spec of its provider (b593, checking r91; decision 0136): an adapter spec `adapters/<name>/` whose
`providers:` name the bounded context (`holders`), each at the version it pins the provider at, else the one asked
or published (b599, checking r100), as `provider/<id's path>/<version>/contract.toml` under its folder
(`place`: keyed by the whole id, so that two bounded contexts whose ids end alike never share a folder), where its
provider check (model_adapter's `uncontracted`) reads it, in one commit by `shop_files.committed`: the only writer of
provider/, nothing kept at the repository root. It keeps no context request and opens no issue. In this order: an id
out of the context id form (migrate init's `FORM`) is refused naming the id and `id not in the context id form`
(r88); a repository GitHub does not serve (`gh api repos/<r>`: missing, private or not answering, `reached`) naming
the bounded context and `bounded context unreachable` (r89); a bounded context no adapter spec has as its provider
naming the provider and `no adapter spec has the provider` (b593, r94); an upstream with no contract kept, or
none at V, naming the bounded context; a contract kept already at that place is left as it is when the same, and
written again with the upstream's bytes, committed, when another (review f1)."""
import json
import os
import shlex
import subprocess
from pathlib import Path

from shop_refused import Refused

PROVIDER = Path("provider")
ADAPTERS = "adapters"
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


def _reach(root, repo, context):
    """Refused unless GitHub serves the repository `repo` of `context`: one missing, private or not answering is a
    bounded context unreachable, never one with no contract."""
    try:
        _gh(root, "api", "repos/%s" % repo)
    except Refused as err:
        raise _unreachable(context, "gh api repos/%s: %s" % (repo, str(err).strip().splitlines()[-1])) from None


def _api(root, repo, path, context):
    """The bytes of `path` in `repo` on GitHub, or None when it is not there; another gh failure the bounded context
    unreachable."""
    try:
        return _gh(root, "api", "-H", RAW, "repos/%s/contents/%s" % (repo, path))
    except Refused as err:
        if "404" in str(err) or "Not Found" in str(err):
            return None
        raise _unreachable(context, str(err).strip().splitlines()[-1]) from None


def _none(context, version):
    at = " at the version %s" % version if version else ""
    return Refused("the bounded context {names} has no contract%s" % at, reason="bounded context with no contract",
                   names=["bounded context:%s" % context])


def reached(root, context):
    """The GitHub repository of `context`, refused as unreachable unless GitHub serves it (checking r89)."""
    import request_gh
    repo = request_gh.repo_of(root, context, COMMAND)
    _reach(root, repo, context)
    return repo


def published(root, context, version=None, repo=None):
    """(version, bytes) of the contract `context` keeps as published, or at `version`; refused when it has none.
    `repo`, its repository `reached` gave, else reached here."""
    import contract_publish
    repo = repo or reached(root, context)
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
        lines = (text or b"").decode("utf-8", errors="replace").splitlines()
        status = contract_publish.STATUS.search("\n".join(lines))
        if status and status.group(1) == "published":
            found = (entry["name"], text)
    if found is None:
        raise _none(context, None)
    return found


def place(context, version):
    """Where a contract of the bounded context `context` at `version` is kept in an adapter spec's folder: provider/
    keyed by the whole id, the
    id's path after `bounded-context/` (two bounded contexts whose ids end alike each keep their own), then the
    version; `version` may be a glob."""
    return PROVIDER.joinpath(*context.split("/")[1:], version, FILE)


def holders(root, context):
    """(folder, version) of each adapter spec `adapters/<name>/` whose spec/index.md says `kind: adapter` and whose
    `providers:` name the bounded context `context`, its folder relative to `root`, in name order; the version it pins
    the provider at (`<id>@<version>`, in the version form), else None (b599, checking r100)."""
    import contract_publish
    import model_adapter
    from model_parse import as_list, frontmatter
    out = []
    for index in sorted(Path(root).glob("%s/*/spec/index.md" % ADAPTERS)):
        data = frontmatter(index.read_text())[0]
        if str(data.get("kind", "")).strip() != model_adapter.KIND:
            continue
        named = (model_adapter.PROVIDER.match(str(given).strip()) for given in as_list(data.get("providers")))
        found = next((m for m in named if m and m.group("id") == context), None)
        if found:
            pin = found.group("version")
            pinned = pin if pin and contract_publish.VERSION.fullmatch(pin) else None
            out.append((index.parent.parent.relative_to(root), pinned))
    return out


def obtain(root, context, version=None):
    """`spec obtain`: the upstream's contract kept under provider/ of each adapter spec of it (at the version it
    pins, else `version`, else the published one) and committed; an id out
    of the context id form (migrate init's) refused before anything is read, then an upstream GitHub does not serve,
    and only then one no adapter spec has as its provider (checking r88, r89 before r94: review f1)."""
    import shop_files
    from migrate_init import FORM
    if not FORM.fullmatch(context):
        raise Refused("the id {names} is refused: id not in the context id form bounded-context/<domain>/<path>",
                      reason="id not in the context id form", names=["id:%s" % context])
    repo = reached(root, context)
    held = holders(root, context)
    if not held:
        raise Refused("the provider {names} is the provider of no adapter spec under %s/: no adapter spec has the "
                      "provider" % ADAPTERS, reason="no adapter spec has the provider", names=["provider:%s" % context])
    texts, rels = {}, {}
    for folder, pin in held:
        wanted = pin or version
        if wanted not in texts:
            texts[wanted] = published(root, context, wanted, repo)
        at, text = texts[wanted]
        rels[(folder / place(context, at)).as_posix()] = text
    changed = [rel for rel, text in rels.items()
               if not ((Path(root) / rel).is_file() and (Path(root) / rel).read_bytes() == text)]
    for rel in rels:
        if rel not in changed:
            print("kept already %s" % rel)
    if not changed:
        return 0

    def write():
        for rel in changed:
            (Path(root) / rel).parent.mkdir(parents=True, exist_ok=True)
            (Path(root) / rel).write_bytes(rels[rel])
    versions = ", ".join(sorted({at for at, _ in texts.values()}))
    shop_files.committed(root, changed, "spec obtain: the contract of %s at %s" % (context, versions), write)
    for rel in changed:
        print("obtained %s" % rel)
    return 0
