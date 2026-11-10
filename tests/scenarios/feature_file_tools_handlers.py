"""feature-file-tools' handlers (design-r2 §4.3, §9.1): the example data writes feature files, test modules and a
capability into the scenario's repository as the given block holds them; a feature file's primitive condition
(`the feature file `features/notes.feature` is nested`) writes the canned file CANNED gives that condition, unless the
example data wrote the file already, when it checks that the file has the condition; a test module's condition checks
the module the example data wrote. The command runs through world_run's `WhenRuns`, `features generate` on a requirement on the capability
that holds it; the Thens read what `features` printed.

Each canned feature file comes with the number of scenarios `features count --by-tag` gives it."""
import re
import textwrap

from vocab import handler

INDEX = "---\nid: bounded-context/ex.com/prod/ctx\n---\n# ctx\n\n## Glossary\n\n"
CANNED = {
    "nested": (1, """\
        Feature: Notes
          Scenario: Nested
            Given a note
              \"\"\"
              @slice-9
              Scenario: Phantom
              \"\"\"
        """),
    "outlined": (3, """\
        @cart
        Feature: Outline
          Scenario Outline: Adding several
            When the shopper adds <n> pens

            Examples:
              | n |
              | 2 |
              | 3 |

            @slow
            Examples:
              | n  |
              | 10 |
        """),
    "sectioned": (1, """\
        Feature: Rules
          Rule: one rule
            Scenario: Under a rule
              Given a step
        """),
}
FEATURE_IS = {
    "deprecating": lambda text: "@deprecated" in text and "Deprecated for: " in text,
    "undeprecated": lambda text: "@deprecated" not in text,
}


def bare(word):
    return word.strip("`")


def write(step, rel, text, scenarios=None):
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if scenarios is not None:
        step.context.setdefault("scenarios", {})[rel] = scenarios


def condition(step):
    return step.text.rsplit(" is ", 1)[1]


def titles(text, pattern):
    return set(re.findall(pattern, text, re.MULTILINE))


@handler("GivenCodeText", "feature file")
def given_feature(step):
    text = step.docstring + "\n"
    write(step, bare(step.names[0]), text, sum(line.strip().startswith("Scenario") for line in text.splitlines()))


@handler("GivenK_C", "feature file")
def feature_is(step):
    rel, word = bare(step.names[0]), condition(step)
    if (step.repo / rel).is_file():
        assert FEATURE_IS[word]((step.repo / rel).read_text()), (rel, word)
    else:
        count, text = CANNED[word]
        write(step, rel, textwrap.dedent(text), count)


@handler("GivenCodeText", "test module")
def given_module(step):
    write(step, bare(step.names[0]), step.docstring + "\n")


def has(step):
    """Every scenario title of the scenario's feature files."""
    return {t for p in (step.repo / "features").rglob("*.feature")
            for t in titles(p.read_text(), r"^\s*Scenario(?: Outline)?: (.*)$")}


MODULE_IS = {
    "resolving": lambda step, text: titles(text, r'scenario\("[^"]+", "([^"]+)"\)') <= has(step),
    "dangling": lambda step, text: bool(titles(text, r'scenario\("[^"]+", "([^"]+)"\)') - has(step)),
    "sweeping": lambda step, text: "scenarios(" in text,
    "partial": lambda step, text: "scenarios(" not in text and bool(
        has(step) - titles(text, r'scenario\("[^"]+", "([^"]+)"\)')),
}


@handler("GivenK_C", "test module")
def module_is(step):
    rel, word = bare(step.names[0]), condition(step)
    assert MODULE_IS[word](step, (step.repo / rel).read_text()), (rel, word)


@handler("GivenCodeText", "capability")
def given_capability(step):
    if not (step.repo / "spec" / "index.md").is_file():
        write(step, "spec/index.md", INDEX)
    write(step, "spec/capabilities/%s.md" % bare(step.names[0]), step.docstring + "\n")


@handler("WhenRuns", "`features generate`")
def generates(step):
    """`features generate` on the capabilities the step names, a requirement (`on the requirement r1`) naming the
    capability whose file holds it."""
    caps = []
    for name in step.names:
        holding = [p.stem for p in sorted((step.repo / "spec" / "capabilities").glob("*.md"))
                   if "- [%s] " % name in p.read_text()] if re.fullmatch(r"r\d+", name) else [bare(name)]
        assert len(holding) == 1, (name, holding)
        caps += holding
    step.context["result"] = step.run("features", "generate", *caps, *step.context.get("flags", []))


def result(step):
    done = step.context["result"]
    assert "Traceback" not in done.stderr, done.stderr
    return done


@handler("ThenPrints", "`features`")
def prints(step):
    out = result(step).stdout
    for np in step.nps:
        if np == "the number of scenarios":
            assert "total %d\n" % sum(step.context["scenarios"].values()) in out, out
        else:
            want = np.strip('"') if np.startswith('"') else bare(np.split()[-1])
            assert want in out, (want, out)


@handler("ThenPrintsNot", "`features`")
def prints_not(step):
    out = result(step).stdout
    for np in step.nps:
        assert bare(np.split()[-1]) not in out, (np, out)


def unoverstated(step):
    """`features does not write the file f1`, f1 overstated (r21): `features generate` wrote the capability's feature,
    which holds the step the Given said it keeps and no step a universal condition entails from it."""
    result(step)
    assert step.context["result"].returncode == 0, step.context["result"].stderr
    kept, entailed = step.context["generated"]
    written = sorted((step.repo / "features").glob("*.feature"))
    assert written, "features generate wrote no feature file"
    texts = [p.read_text() for p in written]
    assert any(kept.search(t) for t in texts), (kept.pattern, texts)
    assert not any(entailed.search(t) for t in texts), (entailed.pattern, texts)
