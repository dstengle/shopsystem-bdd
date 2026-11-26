"""feature-file-tools' capability of a step that has an ambiguous text (scenarios r48, b733): a requirement that uses
`no-noun`, `rc-object` and `named` ("no file that the `w` stage holds") in the construct catalogue's context with the
rows `file | in | worktree` and `file | in | stage`, so that the code written bare ("no file in `w`") reads two ways
(`prepare`); its Then, every step of the feature `features generate` wrote parsing to one tree in the step grammar 4
under its keyword (`check`)."""
import re

LINE = ("While a worktree holds no file that the `w` stage holds, when the person runs `work start`, `work` shall exit "
        "successfully.")
USED = {"no-noun", "rc-object", "named"}


def mine(w, kind):
    """True when the Givens describe a requirement that uses no-noun, rc-object and named, and a step that has
    something (its ambiguous text, which no Given brings in as a kind)."""
    used = {o.strip("`") for v, a, o, pos in w["facts"] if v == "use" and pos and isinstance(o, str)
            and kind(w, a) == "requirement"}
    return USED <= used and any(v == "has" and pos and kind(w, a) == "step" for v, a, _, pos in w["facts"])


def prepare(step, w, capability, index):
    """The capability of LINE, in the construct catalogue's context given the row `file | in | stage`."""
    capability(step.repo, "### [g1] ambiguous\n- [r1] %s\n" % LINE)
    text = index.read_text().replace("| file | in | worktree |  |\n", "| file | in | worktree |  |\n"
                                     "| file | in | stage |  |\n", 1)
    index.write_text(text)
    w["ambiguous"] = True


def check(repo, name):
    """AssertionError naming each step of the feature `name` that parses to more than one tree."""
    import spec_steps4_code
    text = (repo / "features" / ("%s.feature" % name)).read_text()
    steps, keyword = [], None
    for word, step in re.findall(r"^    (Given|When|Then|And|But) (.*)$", text, re.MULTILINE):
        keyword = keyword if word in ("And", "But") else word.lower()
        steps.append((keyword, step))
    assert steps, text
    ambiguous = [s for k, s in steps if len(spec_steps4_code.readings(repo, k, s)) > 1]
    assert not ambiguous, (ambiguous, text)
