"""migration-tools' steps for the plugin's upgrades: `migrate status`, `migrate upgrade`, the SessionStart hook and the
upgrade step "work-items named by ids" (r15, r18-r20, r22-r28). A Given builds a repository on the final layout in
`repo` and commits it; the Whens run the real command or the real hook; the Thens read what they left."""
import json
import os
import pathlib
import re
import subprocess
import sys

from pytest_bdd import given, parsers, then, when

from .migration_old import CONTEXT, said

PLUGIN = pathlib.Path(__file__).resolve().parents[2]
WORK = ".shop/work/"


def plugin_version():
    return json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())["version"]


def item(old, rel, name=None, heading=True, extra=""):
    """A work-item at `rel` of the final layout; its heading is `# <name>` unless it has none."""
    name = name or pathlib.PurePosixPath(rel).stem
    text = "---\nid: work-item/%s/%s\nkind: work-item\n%sstatus: drafted\n---\n\n" % (CONTEXT, name, extra)
    old.write(rel, text + ("# %s\n\nBody.\n" % name if heading else "Body.\n"))


def final_layout(old, version=None):
    old.write("spec/index.md", "---\nid: bounded-context/%s\ntitle: shop\n---\n\n# shop\n" % CONTEXT)
    if version:
        old.write(".shop/plugin-version", version + "\n")
    else:
        old.write(".shop/records/.keep", "")


@given(parsers.re(r"a repository on the final layout whose (?:\.shop/plugin-version|plugin version) is 0\.23\.1, with a work-item (?P<rel>\S+)$"))
def _(old, rel):
    final_layout(old, "0.23.1")
    item(old, rel)
    old.commit()


@given(parsers.parse("a repository on the final layout whose .shop/plugin-version is 0.23.1"))
def _(old):
    final_layout(old, "0.23.1")
    old.commit()


@given("a repository on the final layout whose .shop/plugin-version is the plugin's version")
def _(old):
    final_layout(old, plugin_version())
    old.commit()


@given("a repository with .shop/ and no .shop/plugin-version")
def _(old):
    final_layout(old)
    old.commit()


@given(parsers.re(r"a repository with \.shop/ whose \.shop/plugin-version is (?P<version>[\d.]+|the plugin's version)$"))
def _(old, version):
    final_layout(old, plugin_version() if version.startswith("the") else version)
    old.commit()


@given("a repository without .shop/")
def _(old):
    old.write("README.md", "No shop here.\n")
    old.commit()


@given("work-items .shop/work/i10/a.md, .shop/work/i2/b.md and .shop/work/i2/a.md")
def _(old):
    for rel in (".shop/work/i10/a.md", ".shop/work/i2/b.md", ".shop/work/i2/a.md"):
        item(old, rel)
    old.commit()


@given('.shop/work/i1/size-check.md, a work-item with the heading "# size-check", a directory .shop/work/i1/runs/size-check/ '
       'and a line of .shop/work/i1/log.jsonl for size-check')
def _(old):
    item(old, ".shop/work/i1/size-check.md")
    old.write(".shop/work/i1/runs/size-check/1-research/notes.md", "Notes.\n")
    old.write(".shop/work/i1/log.jsonl", json.dumps({"time": "t", "work-item": "size-check", "event": "start"}) + "\n")
    old.commit()


@given(".shop/work/i1/docs.md, a work-item with no heading, whose depends_on names size-check")
def _(old):
    item(old, ".shop/work/i1/docs.md", heading=False, extra="depends_on: [size-check]\n")
    old.commit()


@given(".shop/records/observations.md, which names size-check in its text")
def _(old):
    old.write(".shop/records/observations.md", "We saw that size-check is slow.\n")
    old.commit()


@when(parsers.re(r"the session runs `migrate (?P<sub>status|upgrade)`$"))
def _(run, old, context, sub):
    context["before_log"] = len(old.git("log", "--oneline").stdout.splitlines())
    who = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    context["done"] = run("migrate", sub, cwd=old.root, env=dict(os.environ, **who))


@when("the person starts a session in it")
def _(old, context):
    """Run the SessionStart command of hooks/hooks.json, as the harness does, in the repository."""
    hooks = json.loads((PLUGIN / "hooks/hooks.json").read_text())["hooks"]["SessionStart"]
    command = hooks[0]["hooks"][0]["command"]
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(PLUGIN), PYTHON=sys.executable)
    context["done"] = subprocess.run(command, shell=True, cwd=old.root, env=env, capture_output=True, text=True)


@then("it exits with an error")
def _(context):
    assert context["done"].returncode != 0


@then("it exits successfully")
def _(context):
    assert context["done"].returncode == 0, said(context)


@then(parsers.parse("migrate prints {version} as the repository's plugin version and the plugin's version as the plugin's"))
def _(context, version):
    out = said(context)
    assert re.search(r"repository.*%s" % re.escape(version), out, re.I), out
    assert re.search(r"plugin.*%s" % re.escape(plugin_version()), out, re.I), out


@then(parsers.parse("migrate prints {version} as the repository's plugin version"))
def _(context, version):
    assert re.search(r"repository.*%s" % re.escape(version), said(context), re.I), said(context)


@then('it prints the pending upgrade step 0.24.0 "work-items named by ids"')
def _(context):
    assert re.search(r'0\.24\.0.*"work-items named by ids"', said(context)), said(context)


@then("migrate says no upgrade step is pending")
def _(context):
    assert "no upgrade step is pending" in said(context), said(context)


@then(parsers.parse("the work-item that was {rel} is {name}"))
def _(old, context, rel, name):
    assert context["done"].returncode == 0, said(context)
    directory = pathlib.PurePosixPath(rel).parent.as_posix()
    now = old.root / directory / (name + ".md")
    assert now.is_file() and not (old.root / rel).exists(), old.git("status", "--porcelain").stdout
    assert "id: work-item/%s/%s\n" % (CONTEXT, name) in now.read_text()


@then(".shop/plugin-version holds the plugin's version")
def _(old):
    assert old.read(".shop/plugin-version").strip() == plugin_version()


@then(parsers.parse('git log has one commit more than before, and it names the upgrade step "work-items named by ids"'))
def _(old, context):
    log = old.git("log", "--format=%B%x00").stdout.split("\0")
    assert len(old.git("log", "--oneline").stdout.splitlines()) == context["before_log"] + 1
    assert "work-items named by ids" in log[0], log[0]


@then("git status shows nothing uncommitted")
def _(old):
    assert old.git("status", "--porcelain").stdout == ""


@then("the plugin's SessionStart hook tells the session nothing")
def _(context):
    assert context["done"].returncode == 0 and context["done"].stdout.strip() == "", said(context)


@then('the plugin\'s SessionStart hook tells the session to offer the person the upgrade from 0.23.1 to the plugin\'s version, '
      'naming the upgrade step "work-items named by ids"')
def _(context):
    out = context["done"].stdout
    assert "offer" in out.lower() and "0.23.1" in out and plugin_version() in out and '"work-items named by ids"' in out, out


@then("it tells the session to run `migrate upgrade` only on the person's yes")
def _(context):
    assert re.search(r"`migrate upgrade`.*only.*yes", context["done"].stdout, re.S), context["done"].stdout


@then("the plugin's SessionStart hook tells the session to tell the person to update the plugin")
def _(context):
    assert re.search(r"tell the person to update the plugin", context["done"].stdout), context["done"].stdout


@then(parsers.parse('.shop/work/i1/size-check.md is now .shop/work/i1/w2.md, its id work-item/<context path>/w2 and its heading "# size-check"'))
def _(old):
    assert not (old.root / WORK / "i1/size-check.md").exists()
    text = old.read(WORK + "i1/w2.md")
    assert "id: work-item/%s/w2\n" % CONTEXT in text and "\n# size-check\n" in text, text


@then('.shop/work/i1/docs.md is now .shop/work/i1/w1.md, its heading "# docs" and its depends_on naming w2')
def _(old):
    assert not (old.root / WORK / "i1/docs.md").exists()
    text = old.read(WORK + "i1/w1.md")
    assert "\n# docs\n" in text and re.search(r"depends_on: \[(work-item/.*/)?w2\]", text), text


@then(".shop/work/i1/runs/size-check/ is now .shop/work/i1/runs/w2/")
def _(old):
    assert not (old.root / WORK / "i1/runs/size-check").exists()
    assert (old.root / WORK / "i1/runs/w2/1-research/notes.md").is_file()


@then("the line of .shop/work/i1/log.jsonl names w2")
def _(old):
    lines = [json.loads(l) for l in old.read(WORK + "i1/log.jsonl").splitlines()]
    assert [l["work-item"] for l in lines] == ["w2"], lines


@then(".shop/records/observations.md still names size-check")
def _(old):
    assert old.read(".shop/records/observations.md") == old.before[".shop/records/observations.md"].decode()
