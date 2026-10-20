"""supervision's Then steps about the workers: how each was started, with what tools and brief, where and when it
ran, read from the stand-in claude's record and log.jsonl."""
import os
import pathlib
import re
import uuid

from pytest_bdd import parsers, then

from .conftest import SCRIPTS
from .supervision_world import AGENTS, calls, git, log_lines, option, scripts_in, starts, work_item_of


@then(parsers.parse("each of {names} had code-scout, bdd-planner, bdd-implementer and bdd-task-reviewer as its workers, in that order"))
def four_workers(repo, context, names):
    for name in names.split(" and "):
        agents = [c["agent"] for c in starts(repo) if work_item_of(c) == name]
        assert agents == ["shopsystem-bdd:" + a for a in AGENTS], (name, agents, context["done"].stderr)


@then("no worker was started before the one before it had ended")
def one_at_a_time(repo):
    events = [(c["event"], c["session"]) for c in calls(repo)]
    assert events and events == [e for s in [c["session"] for c in starts(repo)] for e in (("start", s), ("end", s))], events


@then("each worker was started as `claude -p` with a prompt naming its brief file, --agent shopsystem-bdd:<its stage's "
      "agent> and a session id no other worker had")
def started_as(repo):
    started = starts(repo)
    assert [c["agent"] for c in started] == ["shopsystem-bdd:" + a for a in AGENTS], started
    for c in started:
        argv = c["argv"]
        assert argv[0] == "-p" and c["brief_path"] in argv[1] and c["brief_path"].endswith("brief.md"), argv
        assert option(argv, "--agent") == c["agent"], argv
        # the agent is this plugin's: the plugin is loaded from work run's own directory, not an installed copy
        assert option(argv, "--plugin-dir") == str(SCRIPTS.parent), argv
        if c["agent"] == "shopsystem-bdd:bdd-implementer":
            # its skill is not preloaded under --agent: it may load bdd-red-green, and nothing else, with Skill
            assert "Skill(shopsystem-bdd:bdd-red-green)" in option(argv, "--allowedTools").split(","), argv
        uuid.UUID(option(argv, "--session-id"))
    sessions = [option(c["argv"], "--session-id") for c in started]
    assert len(set(sessions)) == len(sessions) == 4, sessions


@then("each brief file names .shop/work/i1/w1.md and spec/capabilities/thing.md to read, and a result file in the "
      "brief's own directory")
def brief_names(repo):
    for c in starts(repo):
        brief, path = c["brief"], c["brief_path"]
        assert ".shop/work/i1/w1.md" in brief and "spec/capabilities/thing.md" in brief, brief
        result = re.search(r"^Result file: (.+)$", brief, re.M).group(1).strip()
        assert os.path.dirname(result) == os.path.dirname(path), (result, path)


@then(parsers.parse("no worker was started for {name} after the {who}"))
def none_after(repo, name, who):
    agent = {"researcher": "code-scout", "implementer": "bdd-implementer"}[who]
    agents = [c["agent"] for c in starts(repo) if work_item_of(c) == name]
    assert agents and agents[-1] == "shopsystem-bdd:" + agent, agents


@then("log.jsonl has, for each of w1's four workers, a start line and then an end line, each with the time, w1, the "
      "stage, the agent and the session id claude was given")
def worker_lines(repo):
    lines = [l for l in log_lines(repo) if "after" not in l]
    sessions = [option(c["argv"], "--session-id") for c in starts(repo)]
    assert len(sessions) == 4, sessions
    for c, session in zip(starts(repo), sessions):
        mine = [l for l in lines if l.get("session") == session]
        assert [l.get("event") for l in mine] == ["start", "end"], (session, lines)
        for l in mine:
            assert set(l) >= {"time", "work-item", "stage", "agent", "session"} and l["work-item"] == "w1", l
            assert l["agent"] == c["agent"].split(":", 1)[1] and l["stage"], l


@then("no worker was started")
def no_worker(repo):
    assert calls(repo) == [], calls(repo)


@then("each worker ran in a worktree of its own, never in the repository's own checkout, and its brief and result file "
      "are under .shop/scratch/ there")
def own_worktrees(repo):
    started = starts(repo)
    places = [c["cwd"] for c in started]
    assert len(set(places)) == len(places) == 4, places
    for c in started:
        assert os.path.dirname(c["cwd"]) == str(repo / ".shop/worktrees"), c["cwd"]
        result = re.search(r"^Result file: (.+)$", c["brief"], re.M).group(1).strip()
        for path in (c["brief_path"], result):
            assert path.startswith(os.path.join(c["cwd"], ".shop/scratch") + os.sep), (path, c["cwd"])


@then("the implementer's brief also names the plugin's scripts directory, the initiative's base commit, its worktree and "
      "its branch work/w1, and the suite record work run made there")
def implementer_brief(repo):
    c = [c for c in starts(repo) if c["agent"] == "shopsystem-bdd:bdd-implementer"][0]
    lines = dict(line.split(": ", 1) for line in c["brief"].splitlines() if re.match(r"^[A-Z][\w ]*: ", line))
    base = git(repo, "log", "--diff-filter=A", "--format=%H", "--", ".shop/work/i1/initiative.md").strip()
    assert lines.get("Scripts") == str(SCRIPTS), lines
    assert lines.get("Base") == base, (lines, base)
    assert (lines.get("Worktree"), lines.get("Branch")) == (c["cwd"], "work/w1"), lines
    assert re.match(r"Suite: 1 passed, 0 failed at [0-9a-f]{7,} in [\d.]+ s$", lines.get("Suite record", "")), lines


@then(parsers.parse("the researcher was given --allowedTools {tools}"))
def given_tools(repo, tools):
    c = [c for c in starts(repo) if c["agent"] == "shopsystem-bdd:code-scout"][0]
    assert option(c["argv"], "--allowedTools") == scripts_in(tools), c["argv"]


@then(parsers.parse("its `{command}` was {done}"))
def command_was(repo, command, done):
    events = [(c["event"], c["command"]) for c in calls(repo, ("ran", "refused")) if c["tool"] == "Bash"]
    assert events == [({"run": "ran", "refused": "refused"}[done], scripts_in(command))], events


@then("each of w1's four workers was started with --plugin-dir the directory that holds work run's own scripts")
def plugin_dir(repo):
    started = [c for c in starts(repo) if work_item_of(c) == "w1"]
    assert len(started) == 4, started
    for c in started:
        assert option(c["argv"], "--plugin-dir") == str(SCRIPTS.parent), c["argv"]


@then("each of w1's four workers ran in a worktree outside the plugin's directory")
def outside_plugin(repo):
    started = [c for c in starts(repo) if work_item_of(c) == "w1"]
    assert len(started) == 4, started
    for c in started:
        assert option(c["argv"], "--plugin-dir") == str(repo), c["argv"]
        assert not pathlib.Path(c["cwd"]).resolve().is_relative_to(repo.resolve()), c["cwd"]


@then(parsers.parse("the {who}'s load of the skill {skill} was {done}"))
def skill_was(repo, context, who, skill, done):
    loads = [c["event"] for c in calls(repo, ("ran", "refused")) if c["tool"] == "Skill" and c["command"] == skill]
    assert loads == [{"run": "ran", "refused": "refused"}[done]], (loads, context["done"].stderr)


@then("no worker was given a bare Write or Edit in its --allowedTools")
def no_bare_write(repo):
    started = starts(repo)
    assert started, started
    for c in started:
        tools = option(c["argv"], "--allowedTools").split(",")
        assert "Write" not in tools and "Edit" not in tools, (c["agent"], tools)


@then("the researcher's write into the repository's own checkout was refused, and no notes.md is there")
def write_refused(repo):
    writes = [(c["event"], c["command"]) for c in calls(repo, ("ran", "refused")) if c["tool"] == "Write"]
    assert writes == [("refused", str((repo / "notes.md").resolve()))], writes
    assert not (repo / "notes.md").exists()


@then(parsers.re(r'the planner\'s brief has the researcher\'s question "(?P<question>[^"]+)"$'))
def planner_brief_question(repo, context, question):
    briefs = [c["brief"] for c in starts(repo) if c["agent"] == "shopsystem-bdd:bdd-planner"]
    assert len(briefs) == 1 and question in briefs[0], (briefs, context["done"].stderr)


@then("each of w1's four briefs says that the worker starts in its worktree, the directory it was started in, and never "
      "changes directory")
def brief_says_no_cd(repo):
    started = [c for c in starts(repo) if work_item_of(c) == "w1"]
    assert len(started) == 4, started
    for c in started:
        said = [l for l in c["brief"].splitlines() if c["cwd"] in l and "never change directory" in l]
        assert said, c["brief"]


def researcher(repo):
    started = [c for c in starts(repo) if c["agent"] == "shopsystem-bdd:code-scout"]
    assert len(started) == 1, started
    return started[0]


@then(parsers.parse("the researcher's brief gives {first} and {second} as the work-item's file set"))
def brief_file_set(repo, context, first, second):
    brief = researcher(repo)["brief"]
    given = re.search(r"^File set: (.+)$", brief, re.M)
    assert given and given.group(1).split(", ") == [first, second], (brief, context["done"].stderr)


@then(parsers.re(r'the researcher\'s brief names the accepted scenario "(?P<title>[^"]+)" of (?P<feature>\S+), and not '
                 r'"(?P<other>[^"]+)"$'))
def brief_scenarios(repo, title, feature, other):
    brief = researcher(repo)["brief"]
    assert re.search(r"^Accepted scenarios:\n(?:- .+\n)*- %s: %s$" % (re.escape(feature), re.escape(title)), brief, re.M), brief
    assert other not in brief, brief


@then(parsers.parse("the researcher was started with --max-turns {turns:d}"))
def max_turns(repo, turns):
    argv = researcher(repo)["argv"]
    assert option(argv, "--max-turns") == str(turns), argv


def implementer_spans(repo):
    """Each implementer's work-item, and the places of its start and its end in the stand-in's record."""
    events = calls(repo)
    spans = {}
    for i, c in enumerate(events):
        if c["event"] == "start" and c["agent"] == "shopsystem-bdd:bdd-implementer":
            end = next(j for j, e in enumerate(events) if e["event"] == "end" and e["session"] == c["session"])
            spans[work_item_of(c)] = (i, end)
    return spans


def most_at_once(spans):
    """The most implementers running at one time."""
    return max(len([1 for s, e in spans.values() if s <= i < e]) for i, _ in spans.values())


@then(parsers.parse("the implementers of {first} and {second} ran at the same time"))
def ran_together(repo, context, first, second):
    spans = implementer_spans(repo)
    assert first in spans and second in spans, (spans, context["done"].stderr)
    (s1, e1), (s2, e2) = spans[first], spans[second]
    assert s1 < e2 and s2 < e1, spans


@then("no implementer was started before the one before it had ended")
def implementers_one_at_a_time(repo, context):
    spans = implementer_spans(repo)
    assert len(spans) >= 2 and most_at_once(spans) == 1, (spans, context["done"].stderr)


@then("two implementers ran at the same time, and never three")
def two_at_most(repo, context):
    spans = implementer_spans(repo)
    assert len(spans) >= 3 and most_at_once(spans) == 2, (spans, context["done"].stderr)
