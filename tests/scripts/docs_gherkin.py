"""The Gherkin blocks of the docs (b263), each read in the context docs_lines gives its block:

- valid Gherkin by the parser pytest-bdd uses (gherkin-official); a block of scenarios with no `Feature:` an excerpt,
  read under one;
- each step one step of the step grammar 4 (features_vocab4), an `And` or `But` under the keyword before it;
- each instance a Given or a When names (`i1`, `s2` ...) brought in by a Given ("an item i1") at or before it; a Then
  may name what the run made;
- a value said in the full form, "the status of the item i1 is `idea`", never the short "the item i1 is `idea`";
- a scenario whose title a feature file of its context has, as that file has it, line for line; a block that says
  `# generated from spec/capabilities/<cap>.md` its Feature and Narrator lines as features/<cap>.feature has them."""
import re

import features_vocab4
from gherkin.parser import Parser

SHORT = re.compile(r"_k_\w+_Is(?:Code|OneOf|NoneOf)?$")
SOURCE = re.compile(r"#\s*generated from spec/capabilities/(\S+)\.md")
STEP = re.compile(r"^(Given|When|Then|And|But)\s+(.*)$")


def gherkin_problem(body):
    """Why a block is not valid Gherkin, or None."""
    text = "\n".join(body)
    if not re.search(r"^\s*Feature:", text, re.MULTILINE):
        text = "Feature: excerpt\n" + text
    try:
        Parser().parse(text)
    except Exception as err:      # the parser's CompositeParserException and its kin
        return "not valid Gherkin: %s" % str(err).replace("\n", "; ")
    return None


def scenarios(body):
    """[(title, [lines from its first tag line to its last step or docstring line])] of a block."""
    out, tags = [], []
    for line in body:
        s = line.strip()
        if s.startswith("@"):
            tags = [s]
        elif s.startswith(("Scenario:", "Example:")):
            out.append((s.split(":", 1)[1].strip(), tags + [s]))
            tags = []
        elif out and s and not s.startswith(("#", "Feature:", "Narrator:")):
            out[-1][1].append(s)
    return out


def steps(lines):
    """[(keyword, text)] of a scenario's steps, `And` and `But` under the keyword before them; a docstring's lines
    passed over."""
    out, keyword, doc = [], None, False
    for s in lines:
        if s.startswith('"""') or s.startswith("```"):
            doc = not doc
            continue
        m = None if doc else STEP.match(s)
        if m:
            keyword = keyword if m.group(1) in ("And", "But") else m.group(1).lower()
            out.append((keyword, m.group(2)))
    return out


def step_problems(root, lines):
    """What is wrong with a scenario's steps in a context: a step of no reading or two, an instance a Given or a
    When names that no Given brought in, a value in the short form."""
    out, brought = [], set()
    for keyword, text in steps(lines):
        try:
            call = features_vocab4.step(root, keyword, text)
        except features_vocab4.StepError as err:
            out.append("%s %s: %s" % (keyword, text, err))
            continue
        if call.template in ("GivenK", "GivenCode", "GivenCodeText"):
            brought.update(call.names)
        elif keyword in ("given", "when"):
            loose = [n for n in call.names if n not in brought]
            if loose:
                out.append("%s %s: names %s, which no Given brought in" % (keyword, text, ", ".join(loose)))
        if call.template.endswith("K_A") and call.tree[0] == "SCond" and SHORT.search(call.tree[1][0]):
            out.append("%s %s: says a value in the short form; say \"the <attribute> of the <kind> <name> is ...\""
                       % (keyword, text))
    return out


def feature_scenarios(root):
    """{title: (the feature file, its scenario's lines)} of every feature file of a context."""
    out = {}
    for f in sorted((root / "features").glob("*.feature")):
        for title, lines in scenarios(f.read_text(encoding="utf-8").splitlines()):
            out.setdefault(title, (f, lines))
    return out


def quote_problems(root, body):
    """Where a block differs from the feature file of its context it quotes."""
    out, known = [], feature_scenarios(root)
    m = SOURCE.search("\n".join(body))
    if m:
        f = root / "features" / ("%s.feature" % m.group(1))
        if not f.is_file():
            return ["names %s, which is not there" % f.relative_to(root)]
        heads = [s.strip() for s in f.read_text(encoding="utf-8").splitlines()[:3]]
        out += ["%r is not %s's" % (s.strip(), f.name) for s in body
                if s.strip().startswith(("Feature:", "Narrator:")) and s.strip() not in heads]
    for title, lines in scenarios(body):
        if title in known and known[title][1] != lines:
            f, have = known[title]
            out.append("Scenario: %s is not as %s has it:\n    the page: %s\n    the file: %s"
                       % (title, f.name, " / ".join(lines), " / ".join(have)))
    return out


def problems(root, body):
    """Every problem of one Gherkin block read in a context."""
    why = gherkin_problem(body)
    if why:
        return [why]
    out = [p for _, lines in scenarios(body) for p in step_problems(root, lines)]
    return out + quote_problems(root, body)
