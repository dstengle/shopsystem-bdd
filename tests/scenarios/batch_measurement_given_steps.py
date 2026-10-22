"""batch-measurement's Given steps: the log, the stages' sessions, the commits and the measurements a scenario starts
from. They record on the World (batch_measurement_world); nothing is written until the When step flushes it."""
import json

from pytest_bdd import given, parsers

from .batch_measurement_transcripts import raw_session, slim_session
from .batch_measurement_world import git, stamp


@given(parsers.parse("today is {day}"))
def today_is(world, day):
    world.today = day


@given(parsers.parse("the initiative {name} has a log.jsonl"))
def has_log(world, name):
    world.stage("cart-1", "research", "10:00", "10:12", session="s-1")
    world.session("s-1", "cart-1", "research", 14, 3000, 2000, 50000, 0.42)


@given(parsers.parse("the initiative {name} has no log.jsonl"))
def has_no_log(world, name):
    world.has_log = False


@given(parsers.parse("{file} is not of a shape measure knows"))
def not_of_a_shape(world, file):
    if file.startswith("the session.json"):
        world.sessions["s-1"] = ("cart-1", "research", '["not", "a", "session"]')
    else:
        world.transcripts["sessions/s-9.jsonl"] = "this is not a transcript\n"


@given(parsers.parse("the measurement {path} exists"))
def measurement_exists(world, path):
    world.existing = world.repo / path
    world.existing.parent.mkdir(parents=True, exist_ok=True)
    world.existing.write_text("an earlier measurement\n")
    world.before = world.existing.read_text()


@given(parsers.parse("the measurement {path} exists, giving {count:d} stages"))
def measurement_giving(world, path, count):
    measurement_exists(world, path)
    world.existing.write_text("```json\n%s\n```\n" % json.dumps({"totals": {"stages": count}}))


@given(parsers.parse("{name}'s log.jsonl now gives {count:d} stages with a start and an end"))
def log_now_gives(world, name, count):
    world.rows.clear()
    world.has_log = True
    for n in range(count):
        world.stage("cart-%d" % n, "research", "10:%02d" % (n * 10), "10:%02d" % (n * 10 + 5), session="s-%d" % n)


def stage_given(world, item, stage, start, end):
    first = len(world.rows)
    world.stage(item, stage, start, end)
    world.last = (item, stage, range(first, len(world.rows)))


@given(parsers.parse("{name}'s log.jsonl gives work-item {item}'s {stage} stage a start at {start} and an end at {end}"))
def stage_with_end(world, name, item, stage, start, end):
    stage_given(world, item, stage, start, end)


@given(parsers.parse("{name}'s log.jsonl gives work-item {item}'s {stage} stage a start at {start} and no end"))
def stage_without_end(world, name, item, stage, start):
    stage_given(world, item, stage, start, None)


@given(parsers.parse("that stage was run as the agent {agent} in the session {session}"))
def stage_run_as(world, agent, session):
    item, stage, rows = world.last
    for index in rows:
        world.rows[index].update(agent=agent, session=session)
    world.stage_of = {**getattr(world, "stage_of", {}), session: (item, stage)}


@given(parsers.parse("the session {session} took {turns:d} turns, {out:d} output tokens, {new:d} new input tokens "
                     "and {read:d} cache-read tokens, costing {cost:f}"))
def session_took(world, session, turns, out, new, read, cost):
    item, stage, _ = world.last
    world.session(session, item, stage, turns, out, new, read, cost)


@given(parsers.parse("{name}'s log.jsonl gives its first transition at {first} and its last at {last}"))
def transitions_between(world, name, first, last):
    world.log(**{"time": stamp(first), "work-item": "cart-1", "before": "drafted", "after": "researched"})
    world.log(**{"time": stamp(last), "work-item": "cart-1", "before": "researched", "after": "planned"})


@given(parsers.parse("it gives work-item {item}'s {stage} stage a start and an end, run in the session {session}"))
def stage_run_in(world, item, stage, session):
    world.stage(item, stage, "10:00", "10:12", session=session)
    world.stage_of = {**getattr(world, "stage_of", {}), session: (item, stage)}


@given(parsers.parse("it gives work-item {item}'s {stage} stage a start and no end, run in the session {session}"))
def stage_unended(world, item, stage, session):
    world.stage(item, stage, "10:20", None, session=session)
    world.stage_of = {**getattr(world, "stage_of", {}), session: (item, stage)}


@given("the stages' sessions took")
def stages_sessions_took(world, datatable):
    for session, out, new, read, cost in datatable[1:]:
        item, stage = world.stage_of[session]
        world.session(session, item, stage, 1, int(out), int(new), int(read), float(cost))


@given(parsers.parse("the transcript {path} starts inside {name}'s window with {out:d} output tokens, "
                     "{new:d} new input tokens and {read:d} cache-read tokens"))
def transcript_inside(world, path, name, out, new, read):
    world.transcripts[path] = slim_session("s-9", None, "11:00", "12:30", out, new, read)


@given("the directory sessions holds the transcripts")
def directory_holds(world, datatable):
    for session, starts, ends, parent, out, new, read in datatable[1:]:
        where = "sessions/%s/subagents/%s.jsonl" % (parent, session) if parent else "sessions/%s.jsonl" % session
        world.transcripts[where] = slim_session(session, parent or None, starts, ends, int(out), int(new), int(read))


@given(parsers.parse("work-item cart-1's research stage, whose session's reply reads \"{reply}\""))
def stage_with_reply(world, reply):
    world.stage("cart-1", "research", "10:00", "10:12", session="s-1")
    world.session("s-1", "cart-1", "research", 3, 10, 10, 10, 0.01, reply=reply)


@given(parsers.parse("the transcript {path}, starting and ending inside {name}'s window, whose prompt reads "
                     "\"{prompt}\" and whose tool call reads \"{tool}\""))
def transcript_with_content(world, path, name, prompt, tool):
    world.log(**{"time": stamp("09:00"), "work-item": "cart-1", "before": "drafted", "after": "researched"})
    world.log(**{"time": stamp("23:00"), "work-item": "cart-1", "before": "researched", "after": "planned"})
    world.transcripts[path] = raw_session("s-9", "11:00", "11:30", prompt, tool)


@given(parsers.parse("{name}'s log.jsonl gives work-item {item} the transitions"))
def transitions_of(world, name, item, datatable):
    for number, (before, after) in enumerate(datatable[1:]):
        world.log(**{"time": stamp("10:%02d" % number), "work-item": item, "before": before, "after": after})
    world.git_steps.append(lambda: git_init(world))
    world.expected = [tuple(row) for row in datatable[1:]]


def git_init(world):
    repo = world.repo
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    git(repo, "commit", "-q", "--allow-empty", "-m", "start")


@given(parsers.parse("{item}'s work-item branch has the commits {first} and {second}, which its merge brought into "
                     "the initiative branch"))
def branch_commits(world, item, first, second):
    def make():
        repo = world.repo
        git(repo, "checkout", "-q", "-b", "work/" + item)
        git(repo, "commit", "-q", "--allow-empty", "-m", first)
        git(repo, "commit", "-q", "--allow-empty", "-m", second)
        git(repo, "checkout", "-q", "main")
        git(repo, "merge", "-q", "--no-ff", "-m", "merge work/" + item, "work/" + item)
    world.git_steps.append(make)
    world.merged = (first, second)


@given(parsers.parse("the commit {name} was made on the initiative branch itself"))
def own_commit(world, name):
    world.git_steps.append(lambda: git(world.repo, "commit", "-q", "--allow-empty", "-m", name))
