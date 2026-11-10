"""Handlers of features/design-model-check.feature (design §14.3): `model` run on the repository the Givens build,
and what it printed read back.

A repository starts from what a model check needs to be clean: a codified `spec/index.md` with the typed glossary of
tests/scripts/fixtures/glossary/, the capability `thing` with one requirement group and its scenario, the observation the initiatives cite, and an initiative for each work directory. The
Givens of a condition (design_model_check_handlers_conditions.py) change it so that one rule fires, and keep in
`says` what the output names an instance by (a file, a reference, a code)."""
import os
import re
import sys
from pathlib import Path

from vocab import handler

PATH = "ex.com/prod/ctx"
FIXTURE = (Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "glossary" / "spec" / "index.md").read_text()
TERMS = FIXTURE[FIXTURE.index("## Glossary") + len("## Glossary\n"):].strip() + "\n\n### This repository's\n\n"
INDEX = "---\nid: bounded-context/%s\nlanguage: codified-1\n---\n# ctx\n\n## Glossary\n\n%s" % (PATH, TERMS)
# A statement that parses in the fixture glossary: `cap()` writes it for each requirement a Given gives in 0.29 words.
STATEMENT = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`."
HIDE_CLINGO = 'raise ImportError("clingo is hidden for this test")\n'


def sibling(name):
    """A handler module beside this one, loaded once under the name the others load it by."""
    import importlib.util
    module = "shop_" + name[:-3]
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


def full(kind, name):
    return "%s/%s/%s" % (kind, PATH, name)


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def cap(name, reqs, retired="[]", ident=None):
    """A codified capability file: each line of `reqs` in a group [g<k>] of its own, k its place; a line written as
    `**When** asked, ...` is STATEMENT under its id (or under none), any other line is kept as written."""
    body = []
    for k, line in enumerate(reqs, 1):
        m = re.match(r"- (\[r\d+\] )?\*\*When\*\*", line)
        body += ["### [g%d] line %d" % (k, k), "- %s%s" % (m.group(1) or "", STATEMENT) if m else line]
    return ("---\nid: %s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-1\nrests_on: []\n"
            "retired: %s\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n\n## Not yet\n- None.\n"
            % (ident or full("capability", name), name, retired, name, "\n".join(body)))


def feature(name, *tags):
    """A feature file of the capability `name`, one scenario for each tag line; a tag @r<n> names group g<n> too."""
    out = ["# generated from spec/capabilities/%s.md by features generate; do not edit" % name, "Feature: %s" % name,
           "  Narrator: a client", ""]
    for n, tag in enumerate(tags, 1):
        tag = re.sub(r"@r(\d+)", r"@g\1 @r\1", tag)
        out += ["  " + tag, "  Scenario: it answers %d" % n, "    Given a thing", "    Then it is so", ""]
    return "\n".join(out)


def says(step, key, word):
    step.context.setdefault("says", {})[key] = word


def flag(step, name):
    """`name` when a Given gave it, or the When runs the command with the option (grammar 4's `options`)."""
    given = [o.strip("`") for o, _ in getattr(step, "options", None) or ()]
    return [name] if name in step.context.get("flags", []) + given else []


def base(repo, context):
    """What a model check needs to be clean, wherever a Given has not written it."""
    index = repo / "spec" / "index.md"
    if not index.is_file():
        write(repo, "spec/index.md", INDEX)
    elif "language: codified-" not in index.read_text():       # world_nodes' index: codified, the fixture terms added
        text = index.read_text().replace("\n---\n", "\nlanguage: codified-1\n---\n", 1)
        index.write_text(text.replace("## Glossary\n\n", "## Glossary\n\n" + TERMS, 1))
    if not (repo / "spec" / "capabilities" / "thing.md").is_file():
        write(repo, "spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
        if not (repo / "features" / "thing.feature").is_file():
            write(repo, "features/thing.feature", feature("thing", "@r1"))
    work = repo / ".shop" / "work"
    for directory in sorted(work.iterdir()) if work.is_dir() else ():
        if directory.name != "requests" and not (directory / "initiative.md").is_file() and \
                not context.get("homeless"):
            write(repo, ".shop/work/%s/initiative.md" % directory.name, initiative_text(directory.name))
    live = repo / ".shop" / "requests"
    for path in sorted(live.glob("q*.md")) if live.is_dir() else ():
        text = path.read_text()
        if not re.search(r"^(part_of|source|raised_for): ", text, re.MULTILINE):
            path.write_text(text.replace("\n---\n", "\nsource: [observation/obs-1]\n---\n", 1))
    if (work.is_dir() or live.is_dir()) and not (repo / ".shop" / "records" / "observations.md").is_file():
        write(repo, ".shop/records/observations.md", "# Observations\n\n## %s\nabout: bounded-context/%s\nby: someone"
              "\ndate: 2026-10-15\n\nSeen.\n" % (full("observation", "obs-1"), PATH))


def initiative_text(name, status="started", kind="capability-change", date="2026-10-15", more=""):
    return ("---\nid: %s\ntitle: t\nsummary: s\nkind: %s\nowner-level: ctx\nstatus: %s\npriority: 1\n"
            "source: [observation/obs-1]\ndate: %s\n%s---\n" % (full("initiative", name), kind, status, date, more))


def env_of(step):
    """The environment `model` runs in: clingo hidden from every interpreter where an interpreter condition says so,
    and a python3 on PATH that has it where one is clingoless."""
    found = step.context.get("interpreter")
    if not found:
        return sibling("design_model_check_handlers_cache.py").env(step) if step.context.get("xdg") else None
    repo = step.repo
    write(repo, "hidden/clingo.py", HIDE_CLINGO)
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "SHOPSYSTEM_MODEL_REEXEC",
                                                            "VIRTUAL_ENV")}
    env.update(PYTHONPATH=str(repo / "hidden"), PATH=str(repo / "empty"), PYTHONDONTWRITEBYTECODE="1")
    if found == "clingoless":
        python = write(repo, "bin/python3", '#!/bin/sh\nexec /usr/bin/env -u PYTHONPATH "%s" "$@"\n' % sys.executable)
        python.chmod(0o755)
        env["PATH"] = str(repo / "bin")
    return env


def built(step):
    """The world the Givens' facts pick, built once before the command (design_model_check_handlers_facts)."""
    step.context.pop("build", lambda _: None)(step)


def run_model(step, *args):
    built(step)
    base(step.repo, step.context)
    step.context["result"] = step.run("model", *args, env=env_of(step), timeout=120)


@handler("WhenRuns", "`model check`")
def model_check(step):
    run_model(step, "check", *flag(step, "--json"))


@handler("WhenRuns", "`model logic`")
def model_logic(step):
    """`model logic` on the capability the When names, or on the requirement, by the id a Given gave it."""
    built(step)
    ids = step.context.get("ids", {})
    run_model(step, "logic", *[ids.get(step.names[0], step.names[0])] if step.names else [])


@handler("WhenRuns", "`model facts`")
def model_facts(step):
    run_model(step, "facts")


@handler("WhenRuns", "`model decisions`")
def model_decisions(step):
    built(step)
    for name in step.names:     # a decisions index the When names exists, current unless a Given made it stale
        if name not in step.context.get("says", {}):
            given_index(step)
    run_model(step, "decisions", *flag(step, "--check"))


@handler("WhenRuns", "`model rules`")
def model_rules(step):
    run_model(step, "rules", *flag(step, "--json"), *flag(step, "--write"), *flag(step, "--check"))


@handler("WhenRuns", "`model rules --write`")
@handler("WhenRuns", "`model rules --check`")
def model_rules_option(step):
    """`model rules` with the option its code names, on the rule catalogue a Given wrote (`grammar/rules.md`)."""
    run_model(step, "rules", step.term.strip("`").split()[-1])


def holding(step):
    """The capability file that holds the requirement: the one its id names (`ids`, as `shelf#r1`), else thing.md."""
    ident = step.context.get("ids", {}).get(step.names[0], "") if step.names else ""
    return str(step.repo / "spec" / "capabilities" / ("%s.md" % ident.split("#")[0] if "#" in ident else "thing.md"))


@handler("WhenRuns", "`model parse`")
def model_parse(step):
    """`model parse` on the capability file that holds the requirement: each of its statements; with the `--form`
    option, design_model_check_handlers_form's; on a fragment, the world of an unfinished line."""
    if flag(step, "--form"):
        return sibling("design_model_check_handlers_form.py").model_parse_form(step)
    if " on the fragment " in step.text:
        step.context.setdefault("facts", []).append("run on fragment")
        step.context["build"] = sibling("design_model_check_worlds.py").build
    built(step)
    run_model(step, "parse", "--file", holding(step))


# What an instance no Given named is printed as, by its kind and number: `model facts` and `model rules` print every
# one, so a trace's f1 and f2 (r1 and r2) are two of them.
PRINTED = {"fact": ['node("capability/', 'node("bounded-context/'], "rule": ["v15a", "w_uncited_obs"]}


def unsaid(step, word, np=""):
    kind = step.kind or " ".join(np.split()[1:-1])
    printed = PRINTED.get(kind)
    return printed[(int(re.sub(r"\D", "", word) or 1) - 1) % len(printed)] if printed else word


def named(step):
    """What the step's noun phrases name in output: codes without backticks, quoted texts, and for an instance what a
    Given said it is named by (else what its kind prints, else its name)."""
    out = [q.strip('"') for q in step.quoted]
    for np in step.nps:
        out += [w.strip("`") for w in np.split() if w.startswith("`")]
        out += [step.context.get("says", {}).get(w) or unsaid(step, w, np) for w in np.split() if w in step.names]
    return out


@handler("ThenPrints", "`model`")
def model_prints(step):
    done = step.context["result"]
    for word in named(step):
        assert word in done.stdout, (word, done.stdout, done.stderr)


@handler("ThenExitsErr", "`model`")
def model_refused(step):
    done = step.context["result"]
    assert done.returncode != 0, done.stdout
    for word in named(step):
        assert word in done.stdout + done.stderr, (word, done.stdout, done.stderr)


@handler("GivenK", "requirement")
def given_requirement(step):
    says(step, step.names[0], "thing#r1")


@handler("GivenK", "decisions index")
def given_index(step):
    write(step.repo, "spec/decisions/d.md", "---\nid: design-decision/%s/d\nstatus: accepted\nsummary: s\n---\n"
          "# d\n\n## Decision\nSo.\n" % PATH)
    base(step.repo, step.context)
    step.run("model", "decisions")
    says(step, step.names[0], "spec/decisions/index.md")


@handler("GivenK", "interpreter")
@handler("GivenK", "scenario")
@handler("GivenK", "feature")
def given_nothing(step):
    pass
