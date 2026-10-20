"""What feature-file-tools' step modules share: the feature files and test modules a Given writes, the
repository's files as they were, and the checks of a refused edit."""
import re


# --- the files a scenario writes ----------------------------------------------------------------------------

NOTE_WITH = '    Given a note\n      """\n      %s\n      """\n'
RULE = "Feature: Rules\n\n  Rule: a rule\n\n    Scenario: Inside\n      Given a step\n"


def feature_text(*scenarios, tags="", background=""):
    head = "%sFeature: Cart\n  Narrator: a shopper\n\n" % (tags + "\n" if tags else "")
    return head + background + "\n".join(scenarios)


def scenario_text(title, tags="", body="    Given a step\n", kind="Scenario"):
    return "%s  %s: %s\n%s" % ("  %s\n" % tags if tags else "", kind, title, body)


def outline_text(title, tags, *tables):
    """A Scenario Outline whose Examples tables are (tag line, number of rows)."""
    out = "%s  Scenario Outline: %s\n    Given <n>\n" % ("  %s\n" % tags if tags else "", title)
    for tag, rows in tables:
        out += "\n%s    Examples:\n      | n |\n%s" % ("    %s\n" % tag if tag else "", "".join("      | %d |\n" % i for i in range(1, rows + 1)))
    return out


def binding(title, feature_name="cart.feature", line=12):
    """A test module whose binding call sits on line `line`."""
    pad = "".join("# filler\n" for _ in range(line - 2))
    return 'from pytest_bdd import scenario\n%s@scenario("%s", "%s")\ndef test_x():\n    pass\n' % (pad, feature_name, title)


def write(repo, name, text):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def snapshot(repo):
    """Every file under `repo`, by path."""
    return {str(p.relative_to(repo)): p.read_text() for p in sorted(repo.rglob("*")) if p.is_file()}


def store(repo, context, path, *scenarios, tags=None, background=None):
    """Write the feature file `path` from what the scenario has told so far: scenarios add up, tags and Background replace."""
    entry = context.setdefault("files", {}).setdefault(path, {"scenarios": [], "tags": "", "background": ""})
    entry["scenarios"].extend(scenarios)
    if tags is not None:
        entry["tags"] = tags
    if background is not None:
        entry["background"] = background
    context["last"] = path
    write(repo, path, feature_text(*entry["scenarios"], tags=entry["tags"], background=entry["background"]))


def titles_in(text):
    return re.findall(r'"([^"]*)"', text)


def tag_line_of(text, title):
    """The line just above `Scenario: <title>`."""
    lines = text.splitlines()
    return lines[lines.index("  Scenario: " + title) - 1]


def refused(run, repo, *args):
    """Run an edit that must be refused: exit 1, nothing on stdout, a reason on stderr, every file as it was."""
    before = snapshot(repo)
    done = run("features", *args)
    assert done.returncode == 1, done.stdout + done.stderr
    assert done.stdout == ""
    assert "Traceback" not in done.stderr
    assert snapshot(repo) == before
    return done.stderr


def rejected(context, code=1):
    result = context["result"]
    assert result.returncode == code, result.stdout + result.stderr
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    return result.stderr
