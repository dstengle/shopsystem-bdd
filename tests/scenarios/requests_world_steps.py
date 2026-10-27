"""The repositories features/requests.feature's scenarios build (requests r28, r30 to r34, r39 to r44): an upstream, a bare
remote it names in `.shop/requests.toml`, and an asker's repository for each asker id registered under that remote. What the
upstream keeps is what its repository holds together with what is sent to it and not yet taken in (decision 0071).

Helpers only; the steps that use them are in requests_steps, requests_write_steps and requests_send_steps. The remote is
read and written with git, as the carrier does, and not through the scripts' modules."""
import json
import re
import subprocess

from .work_queue_git_steps import init

GOOD = ["The queue shall show each item.", "While idle, when a request arrives, the system shall answer it."]


def request_rel(ident):
    return ".shop/work/requests/%s.md" % ident


def sections_of(text):
    """The request's `## <name>` sections, each as its list of entry lines."""
    return {name: [line for line in body.splitlines() if line.strip()]
            for name, body in re.findall(r"(?ms)^## (\w+)\n(.*?)(?=^## |\Z)", text)}


def sibling(repo, name):
    return repo.parent / (repo.name + "-" + name)


def git(path, *args, data=None):
    return subprocess.run(["git", *args], cwd=path, capture_output=True, text=True, input=data, check=True).stdout


def make_repo(path, name):
    """`path` as a git repository whose spec/index.md gives the context `name`."""
    (path / "spec").mkdir(parents=True, exist_ok=True)
    (path / "spec" / "index.md").write_text("---\nid: bounded-context/%s\n---\n# %s\n" % (name, name))
    init(path)


def write_settings(path, text):
    (path / ".shop").mkdir(exist_ok=True)
    (path / ".shop" / "requests.toml").write_text(text)


def write_upstream_settings(repo, context):
    allow = "".join('%s = [%s]\n' % (who, ", ".join('"%s"' % a for a in askers)) for who, askers in context["allow"].items())
    write_settings(repo, '[upstream]\nremote = "%s"\n\n[upstream.allow]\n%s' % (context["remote"], allow))


def upstream(repo, context, name):
    """`repo` as the upstream `name`, naming a new bare remote; nothing is allowed yet."""
    make_repo(repo, name)
    remote = sibling(repo, "remote.git")
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True, capture_output=True)
    context.update(upstream=repo, remote=str(remote), up_name=name, allow={}, askers={})
    write_upstream_settings(repo, context)


def asker_repo(repo, context, name, asker_id=None, allowed=True):
    """The repository of the asker `name`, registered under `asker_id` (default: `name`) on the upstream's remote; the
    upstream allows that asker id for `name` when `allowed`."""
    asker_id = asker_id or name
    path = sibling(repo, asker_id)
    if not path.exists():
        make_repo(path, name)
    write_settings(path, '[asker]\nremote = "%s"\nid = "%s"\n' % (context["remote"], asker_id))
    if allowed:
        context["allow"].setdefault(asker_id, [])
        if name not in context["allow"][asker_id]:
            context["allow"][asker_id].append(name)
        write_upstream_settings(context["upstream"], context)
    context["askers"][name] = path
    context.setdefault("ids", {})[name] = asker_id
    return path


def home(repo, context):
    return context.get("upstream", repo)


def refs(path, remote, prefix):
    """{name below prefix: content} of the refs of `remote` under `prefix`, read by git."""
    names = [line.split()[1][len(prefix):] for line in git(path, "ls-remote", remote, prefix + "*").splitlines()]
    if names:
        git(path, "fetch", "-q", remote, "+%s*:refs/probe/%s*" % (prefix, prefix))
    return {name: git(path, "cat-file", "blob", "refs/probe/%s%s" % (prefix, name)) for name in names}


def put(path, remote, text, ref):
    blob = git(path, "hash-object", "-w", "--stdin", data=text).strip()
    git(path, "push", "-q", "--force", remote, "%s:%s" % (blob, ref))


def send(repo, context, name, item):
    """What the asker `name`'s repository sends: `item` pushed as the next ref of its asker id."""
    path, asker_id = context["askers"][name], context["ids"][name]
    taken = [int(n.rsplit("/", 1)[1]) for n in refs(path, context["remote"], "refs/sent/") if n.startswith(asker_id + "/")]
    put(path, context["remote"], json.dumps(item), "refs/sent/%s/%d" % (asker_id, max(taken, default=0) + 1))


def pending(repo, context):
    """What is sent to the upstream and not taken in: (asker id, number, item), the asker ids' in the order sent."""
    if "remote" not in context:
        return []
    found = [(n.rsplit("/", 1)[0], int(n.rsplit("/", 1)[1]), json.loads(t))
             for n, t in refs(home(repo, context), context["remote"], "refs/sent/").items()]
    return sorted(found, key=lambda i: (i[0], i[1]))


def local_text(repo, context, ident):
    """The text of request `ident` as the upstream's repository keeps it; None when it keeps none."""
    path = home(repo, context) / request_rel(ident)
    return path.read_text() if path.is_file() else None


def rendered(context, item):
    """A request sent, as the file text the upstream keeps it in once taken in."""
    origin = "part_of: %s\n" % item["thread"] if item["thread"] else "source: [%s]\n" % ", ".join(item["sources"]) if item["sources"] else ""
    raised = "raised_for: %s\n" % item["raised_for"] if item["raised_for"] else ""
    return ("---\nid: request/%s/%s\nkind: request\nasker: %s\n%s%sstatus: open\nturn: upstream\n---\n\n# %s\n\n## Lines\n%s\n"
            "## Questions\n\n## Answers\n\n## Outcomes\n\n## Resolution\n"
            % (context["up_name"], item["id"], item["asker"], origin, raised, item["title"],
               "".join("%d. %s\n" % e for e in enumerate(item["lines"], 1))))


def text_of(repo, context, ident):
    """The text of request `ident` as the upstream keeps it, with what is sent about it and not taken in written in."""
    text = local_text(repo, context, ident)
    sent = pending(repo, context)
    for _, _, item in sent:
        if text is None and item["kind"] == "request" and item["id"] == ident:
            text = rendered(context, item)
    assert text is not None, "the upstream keeps no request %s" % ident
    for _, _, item in sent:
        if item["kind"] == "answer" and item["request"] == ident:
            text = re.sub(r"(?m)^## Answers\n", lambda _: "## Answers\n%d. %s\n" % (item["question"], item["text"]), text, count=1) \
                if "## Answers\n" in text else text.rstrip("\n") + "\n\n## Answers\n%d. %s\n" % (item["question"], item["text"])
        elif item["kind"] == "turn" and item["request"] == ident:
            text = text.replace("\nturn: asker\n", "\nturn: upstream\n", 1)
    return text


def kept_ids(repo, context):
    """The names of the requests the upstream keeps or has had sent and not taken in, in order."""
    names = {p.stem for p in (home(repo, context) / ".shop" / "work" / "requests").glob("q*.md")}
    names |= {item["id"] for _, _, item in pending(repo, context) if item["kind"] == "request"}
    return sorted(names, key=lambda n: int(n[1:]))


def publish_kept(repo, context):
    """Publish every request of another asker the upstream keeps, as `work` does after each change to one (decision 0071)."""
    if "remote" in context:
        for path in sorted((home(repo, context) / ".shop" / "work" / "requests").glob("q*.md")):
            text = path.read_text()
            if re.search(r"(?m)^asker: (?!internal|%s$)" % re.escape(context["up_name"]), text):
                put(home(repo, context), context["remote"], text, "refs/published/" + path.stem)
