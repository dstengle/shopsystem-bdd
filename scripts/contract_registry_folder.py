"""The shop-folder adapter of the contract registry (b636, contract-registry r1-r3), the one adapter wired in
(contract_registry; decisions 0124, 0125), which keeps today's folder layouts behind the port. A bounded context's
contracts are kept in its own folder as `.shop/contracts/<version>/contract.toml` (b348), each with `status =
"published"` or `"superseded"` (`kept`): `deposit` writes the contract at its version as the published one and sets
every one published before it superseded, in one commit by `shop_files.committed`. `retrieve` reads this bounded
context's folder, a folder of the same shop that holds the bounded context asked (a `spec/index.md` whose `id` is
it, at the shop's top or one or two folders under it: `hosted`, b622), else the upstream's folder on GitHub
(contract_registry_github); with no version the published contract (the one of the highest version), a version
never deposited refused naming it, `version not deposited`. A contract registered for an adapter spec (b735,
contract-registry r4) is kept in the adapter spec's folder as `provider/<id's path>/<version>/contract.toml` (`place`,
b593), committed, the same bytes kept there already left as they are; `held` reads back what a folder holds there;
`deregister` (b743, contract-registry r5) takes the file its register wrote out again, committed, the folders it
leaves empty with it (pushed commits are never rewritten: history keeps both, the files are as before)."""
import re
from pathlib import Path

import contract_registry
from shop_refused import Refused

KEPT = Path(".shop") / "contracts"
FILE = "contract.toml"
PROVIDER = Path("provider")
STATUS = re.compile(r'^status = "(published|superseded)"$', re.MULTILINE)


def kept(root):
    """{version: (path relative to root, status)} of every contract kept in the context at `root`."""
    out = {}
    for path in sorted((Path(root) / KEPT).glob("*/" + FILE)):
        found = STATUS.search(path.read_text(encoding="utf-8"))
        out[path.parent.name] = (path.relative_to(root).as_posix(), found.group(1) if found else None)
    return out


def order(version):
    """A version's sort key, number by number, a part that is no number after the numbers."""
    return [(0, int(p), "") if p.isdigit() else (1, 0, p) for p in re.split(r"[.+-]", version)]


def place(context, version):
    """Where a contract of the bounded context `context` at `version` is kept in an adapter spec's folder: provider/
    keyed by the whole id, the id's path after `bounded-context/` (two bounded contexts whose ids end alike each keep
    their own), then the version; `version` may be a glob."""
    return PROVIDER.joinpath(*context.split("/")[1:], version, FILE)


def held(folder, provider, version=None):
    """The contracts of `provider` kept in the adapter spec's `folder`, at `version` (None: any), sorted."""
    return sorted(Path(folder).glob(place(provider, version or "*").as_posix()))


def register(root, contract, adapter_spec, provider, version):
    """The contract (its bytes) of `provider` kept at `version` in the adapter spec's folder `adapter_spec` (relative
    to `root`), committed unless the same bytes are kept there already; the reply completed, {"kept": its path,
    "changed": whether it was written}."""
    import shop_files
    rel = (Path(adapter_spec) / place(provider, version)).as_posix()
    target = Path(root) / rel
    if target.is_file() and target.read_bytes() == contract:
        return contract_registry.completed({"kept": rel, "changed": False})

    def write():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contract)
    shop_files.committed(root, [rel], "spec obtain: the contract of %s at %s for %s" % (provider, version,
                                                                                     adapter_spec), write)
    return contract_registry.completed({"kept": rel, "changed": True})


def deregister(root, contract, adapter_spec, provider, version):
    """The contract of `provider` at `version` taken out of the adapter spec's folder `adapter_spec` (relative to
    `root`), committed, the folders under the adapter spec it leaves empty removed; the reply completed, {"kept": its
    path, "changed": whether it was there}. `contract` is the one registered, which the file held."""
    import shop_files
    rel = (Path(adapter_spec) / place(provider, version)).as_posix()
    target = Path(root) / rel
    if not target.is_file():
        return contract_registry.completed({"kept": rel, "changed": False})

    def write():
        target.unlink()
        folder, top = target.parent, Path(root) / adapter_spec
        while folder != top and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            folder = folder.parent
    shop_files.committed(root, [rel], "spec obtain: the contract of %s at %s deregistered for %s" % (
        provider, version, adapter_spec), write)
    return contract_registry.completed({"kept": rel, "changed": True})


def deposit(root, contract, version):
    """The contract (its text) kept at `version` as the published one, every one published before it superseded,
    committed; the reply completed, {"kept": its path, "superseded": the paths set superseded}."""
    import shop_files
    contracts = kept(root)
    if version in contracts:
        raise Refused("a contract is kept at the version {names} already", reason="version already published",
                      names=["version:%s" % version])
    rel = (KEPT / version / FILE).as_posix()
    older = [path for path, status in contracts.values() if status == "published"]

    def write():
        for path in older:
            target = Path(root) / path
            target.write_text(STATUS.sub('status = "superseded"', target.read_text(encoding="utf-8")),
                              encoding="utf-8")
        target = Path(root) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contract, encoding="utf-8")
    shop_files.committed(root, older + [rel], "spec publish: the contract at %s" % version, write)
    return contract_registry.completed({"kept": rel, "superseded": older})


def _local(folder, version):
    contracts = kept(folder)
    if version is None:
        found = sorted((v for v, (_, status) in contracts.items() if status == "published"), key=order)
        if not found:
            return contract_registry.undeposited(None)
        version = found[-1]
    elif version not in contracts:
        return contract_registry.undeposited(version)
    return contract_registry.returned(version, (Path(folder) / contracts[version][0]).read_bytes())


def hosted(root, context):
    """The folder of the same shop that holds the bounded context `context` (its spec/index.md's `id`), or None: the
    shop's top (git's top level of `root`, else `root`) and the folders one or two under it."""
    import subprocess

    from model_parse import frontmatter
    done = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root, capture_output=True, text=True)
    top = Path(done.stdout.strip()) if done.returncode == 0 and done.stdout.strip() else Path(root)
    for pattern in ("spec/index.md", "*/spec/index.md", "*/*/spec/index.md"):
        for index in sorted(top.glob(pattern)):
            try:
                ident = frontmatter(index.read_text(encoding="utf-8"))[0].get("id")
            except (OSError, ValueError):
                continue
            if ident == context:
                return index.parent.parent
    return None


def retrieve(root, context=None, version=None):
    """The reply to a retrieve of the contract of `context` (None: the bounded context at `root`) at `version` (None:
    the published one), read from its folder in the shop, else from its repository on GitHub."""
    if context is None:
        return _local(root, version)
    folder = hosted(root, context)
    if folder is not None:
        return _local(folder, version)
    import contract_registry_github
    return contract_registry_github.published(root, context, version)
