import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from binding import missing

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "measure"

ARCHIVE = '''# Shelf slices, batch %s

## Slice 8: Ids are made in one place
- Kind: capability
- Scenarios: shelf / An id is made
- Lands: 2 production, 1 test
- Status: green

## Slice 9: Ids are read in one place
- Kind: capability
- Scenarios: shelf / An id is read
- Status: green

## Log
- 2026-01-02 HAND-BACK slice 8 at abc1234: a test the task did not list.
  Evidence: assert 1 == 2.
- 2026-01-02 Suite: 9 passed, 0 failed at abc1234 in 3 s
'''
TASKS = "docs/superpowers/plans/2026-01-02-shelf-batch2-implementation.md"
LEDGER = ".superpowers/sdd/2026-01-02-shelf-batch2-implementation"


def at(hour, minute=0):
    return "2026-01-02T%02d:%02d:00Z" % (hour, minute)


def plus(time, minutes):
    made = datetime.datetime.fromisoformat(time.replace("Z", "+00:00")) + datetime.timedelta(minutes=minutes)
    return made.strftime("%Y-%m-%dT%H:%M:%SZ")


class MeasureTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / "shelf"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.projects = self.tmp / "projects"
        self.session = self.projects / re.sub(r"[^A-Za-z0-9]", "-", str(self.repo))
        (self.session / "s1" / "subagents").mkdir(parents=True)
        self.archive = "docs/superpowers/plans/archive/shelf-slices-batch%s.md"
        self.commit(at(8), {self.archive % 1: ARCHIVE % 1})
        self.commit(at(9), {TASKS: "# Plan\n\n### Task 1: Slice 8. Made\n\n### Task 2: Slice 9. Read\n"})
        self.commit(at(10, 5), {"shelf/ids.py": "a\n", "shelf/names.py": "a\n", "tests/test_ids.py": "a\n",
                                "docs/notes.md": "a\n"})
        self.commit(at(10, 40), {"shelf/read.py": "a\n"})
        self.commit(at(11), {TASKS: "# Plan\n\n### Task 1: Slice 8. Made\n\n### Task 2: Slice 9. Read\n\n### Task 3: Slice 9.1. More\n"})
        self.commit(at(12), {self.archive % 2: ARCHIVE % 2})
        self.rows = []
        self.agent("a1", "bdd-implementer", "slice 8: implement", at(10), at(10, 10), reply="DONE\n\nCommit: abc")
        self.agent("a2", "bdd-implementer", "Do the reading", at(10, 30), at(10, 45),
                   prompt="Read %s/task-2-brief.md and do it." % LEDGER, reply="BLOCKED\n\ntests/test_x.py")
        self.agent("a3", "bdd-task-reviewer", "slice 8: review", at(10, 11), at(10, 20),
                   reply="Needs fixes. Spec Compliance ❌\n- **Important** shelf/ids.py:3 wrong\n- Critical: shelf/ids.py:9 lost\n2 Minor issues")
        self.agent("a4", "bdd-branch-reviewer", "batch 2: branch review", at(11, 10), at(11, 30),
                   reply="Ready to merge: With fixes\nNo Critical or Important issues.")
        self.agent("a5", "code-scout", "Look around", at(9, 30), at(9, 40), reply="Lands: 2 production, 1 test")
        self.agent("a0", "bdd-implementer", "slice 7: implement", at(7), at(7, 30), reply="DONE")
        self.main([(at(9, 20), 100), (at(10, 50), 200), (at(13), 400)])

    def git(self, *args, when=None):
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        if when:
            env.update(GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
        return subprocess.run(("git",) + args, cwd=self.repo, env=env, check=True, capture_output=True, text=True).stdout

    def commit(self, when, files):
        for path, text in files.items():
            target = self.repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "c", when=when)

    def request(self, when, rid, output, text="", tool=None, read=1000, new=50):
        content = [{"type": "text", "text": text}] if text else []
        if tool:
            content.append({"type": "tool_use", "id": rid + "t", "name": tool, "input": {}})
        return {"type": "assistant", "timestamp": when, "requestId": rid, "version": "2.1.0", "effort": "low",
                "message": {"model": "claude-x", "content": content,
                            "usage": {"input_tokens": 10, "cache_creation_input_tokens": new - 10,
                                      "cache_read_input_tokens": read, "output_tokens": output,
                                      "output_tokens_details": {"thinking_tokens": output // 10}}}}

    def write(self, path, rows):
        path.write_text("".join(json.dumps(row) + "\n" for row in rows))

    def agent(self, name, role, description, start, end, prompt="Do it.", reply="DONE", extra=()):
        rows = [{"type": "user", "timestamp": start, "message": {"content": prompt + " Skill at shopsystem-bdd/0.12.0/skills"}},
                self.request(start, name + "1", 5, tool="Bash", read=1000),
                self.request(start, name + "1", 30, tool="Read", read=1000),
                {"type": "user", "timestamp": start, "message": {"content": [{"type": "tool_result", "content": "ok"}]}},
                {"type": "attachment", "timestamp": start}]
        rows += list(extra)
        rows.append(self.request(end, name + "2", 70, text=reply, read=5000))
        self.put(name, role, description, rows)

    def put(self, name, role, description, rows):
        base = self.session / "s1" / "subagents" / ("agent-%s" % name)
        self.write(base.with_suffix(".jsonl"), rows)
        base.with_suffix(".meta.json").write_text(json.dumps({"agentType": "shopsystem-bdd:" + role, "description": description, "model": "opus"}))

    def clear_agents(self):
        for path in (self.session / "s1" / "subagents").iterdir():
            path.unlink()

    def quiet_main(self):
        self.main([(at(13), 400)])

    def lone(self, name, role, description, start, end, ctx=1050, prompts=1, prompt="Do it.", reply="DONE",
             plugin="0.12.0", version="2.1.0"):
        rows = [{"type": "user", "timestamp": start, "message": {"content": "%s Skill at shopsystem-bdd/%s/skills" % (prompt, plugin)}},
                self.request(start, name + "1", 5, read=ctx - 50, new=50)]
        rows += [{"type": "user", "timestamp": start, "message": {"content": "Continue."}} for _ in range(prompts - 1)]
        rows.append(self.request(end, name + "2", 70, text=reply, read=ctx - 50, new=50))
        for row in rows:
            if row["type"] == "assistant":
                row["version"] = version
        self.put(name, role, description, rows)

    def sha(self, hour, minute=0):
        for line in self.git("log", "--all", "--format=%H %cI").splitlines():
            commit, made = line.split()
            if datetime.datetime.fromisoformat(made).strftime("%Y-%m-%dT%H:%M:%SZ") == at(hour, minute):
                return commit
        raise AssertionError("no commit at %s" % at(hour, minute))

    def open_batch(self, *args):
        out = self.tmp / "open.json"
        done = self.run_script("batch", "--projects", str(self.projects), "--out", str(out), *args)
        return done, (json.loads(out.read_text()) if out.exists() else None)

    def numbers(self, value):
        if isinstance(value, dict):
            value = list(value.values())
        if isinstance(value, list):
            return [n for item in value for n in self.numbers(item)]
        return [value] if isinstance(value, (int, float)) and not isinstance(value, bool) else []

    def main(self, turns):
        self.write(self.session / "s1.jsonl", [self.request(when, "m%d" % i, out, tool="Agent") for i, (when, out) in enumerate(turns)])

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT)] + list(args), capture_output=True, text=True, cwd=self.repo)

    def measure(self, *args, ok=True):
        out = self.tmp / "facts.json"
        done = self.run_script("batch", self.archive % 2, "--projects", str(self.projects), "--out", str(out), *args)
        if not ok:
            return done
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(out.read_text())

    def by(self, facts, description):
        return [d for d in facts["dispatches"] if d["description"] == description][0]

    def test_a_batch_runs_from_one_archive_commit_to_the_next(self):
        """an archive file's batch runs from the archive commit before it to its own"""
        facts = self.measure()
        self.assertEqual(facts["window"]["from"], at(8))
        self.assertEqual(facts["window"]["to"], at(12))
        self.assertEqual(facts["batch"], "shelf-slices-batch2")
        self.assertEqual(len(facts["dispatches"]), 5)
        self.assertNotIn("slice 7: implement", [d["description"] for d in facts["dispatches"]])

    def test_a_requests_usage_is_counted_once(self):
        one = self.by(self.measure(), "slice 8: implement")
        self.assertEqual((one["requests"], one["output"], one["tool_calls"]), (2, 100, 2))
        self.assertEqual((one["new_input"], one["cache_read"]), (100, 6000))
        self.assertEqual((one["first_context"], one["peak_context"], one["seconds"]), (1050, 5050, 600))
        self.assertEqual((one["thinking"], one["effort"]), (10, "low"))

    def test_reasoning_is_summed_by_role_and_shown(self):
        facts = self.measure()
        self.assertEqual(facts["roles"]["bdd-implementer"]["thinking"], 20)
        self.assertEqual(facts["summary"]["thinking"], 5 * 10 + 30)
        shown = self.run_script("show", str(self.tmp / "facts.json")).stdout
        self.assertIn("| of which reasoning", shown)
        self.assertRegex(shown, r"\| bdd-implementer +\| +2 \| +low \|")

    def test_attribution_by_description_by_prompt_and_none(self):
        facts = self.measure()
        self.assertEqual([self.by(facts, "slice 8: implement")[k] for k in ("slice", "kind", "attributed")], ["8", "implement", "description"])
        self.assertEqual([self.by(facts, "Do the reading")[k] for k in ("slice", "task", "attributed")], ["9", 2, "prompt"])
        self.assertEqual([self.by(facts, "batch 2: branch review")[k] for k in ("slice", "kind", "attributed")], [None, "branch review", "description"])
        self.assertIsNone(self.by(facts, "Look around")["attributed"])
        self.agent("a7", "spec-round", "spec lending: formulate round 1", at(9, 5), at(9, 15))
        spec = self.by(self.measure("--replace"), "spec lending: formulate round 1")
        self.assertEqual((spec["kind"], spec["attributed"], spec["slice"]), ("spec", "description", None))
        self.assertEqual(facts["summary"]["unattributed"], 1)

    def test_statuses_and_findings_as_replied(self):
        facts = self.measure()
        self.assertEqual(self.by(facts, "Do the reading")["status"], "BLOCKED")
        review = self.by(facts, "slice 8: review")
        self.assertEqual((review["status"], review["findings"]), ("Needs fixes", {"critical": 1, "important": 1, "minor": 2}))
        branch = self.by(facts, "batch 2: branch review")
        self.assertEqual((branch["status"], branch["findings"]["important"]), ("With fixes", 0))
        summary = facts["summary"]
        self.assertEqual((summary["not_done"], summary["reviews"], summary["reviews_clean"], summary["findings_task_review"]), (1, 1, 0, 2))

    def test_commits_and_lands_against_touched(self):
        facts = self.measure()
        self.assertEqual(self.by(facts, "slice 8: implement")["touched"], [2, 1, 1])
        self.assertEqual(len(self.by(facts, "slice 8: implement")["commits"]), 1)
        self.assertEqual((facts["slices"]["8"]["lands"], facts["slices"]["8"]["touched"]), ([2, 1], [2, 1, 1]))
        self.assertEqual((facts["slices"]["9"]["lands"], facts["slices"]["9"]["touched"]), (None, [1, 0, 0]))
        self.assertEqual(facts["slices"]["8"]["by_role"], {"bdd-implementer": 1, "bdd-task-reviewer": 1})

    def test_tasks_hand_backs_suite_and_diff(self):
        facts = self.measure()
        self.assertEqual(facts["tasks"], {"plan": TASKS, "planned": 2, "run": 3})
        self.assertEqual(len(facts["hand_backs"]), 1)
        self.assertEqual(facts["hand_backs"][0]["slice"], "8")
        self.assertIn("Evidence: assert 1 == 2.", facts["hand_backs"][0]["entry"])
        self.assertIn("9 passed", facts["suite"])
        self.assertEqual(facts["summary"]["files_changed"], 7)
        self.assertEqual(facts["plugin_versions"], ["0.12.0"])

    def test_the_controller_is_the_sessions_requests_inside_the_batch(self):
        """a dispatching session's own requests are the controller's"""
        facts = self.measure()
        self.assertEqual((facts["roles"]["controller"]["requests"], facts["roles"]["controller"]["output"]), (2, 300))
        self.assertEqual(facts["roles"]["bdd-implementer"]["dispatches"], 2)
        self.assertEqual(facts["summary"]["output"], 5 * 100 + 300)

    def test_the_share_closing_leaves_scouts_out(self):
        summary = self.measure()["summary"]
        self.assertEqual(summary["closing_share"], round(20 / (10 + 15 + 9 + 20), 2))
        self.assertEqual(summary["span_minutes"], 120.0)

    def test_a_resumed_agent_is_one_dispatch_with_two_prompts(self):
        again = [{"type": "user", "timestamp": at(10, 8), "message": {"content": "Continue with step 2."}},
                 self.request(at(10, 9), "a13", 40)]
        self.agent("a1", "bdd-implementer", "slice 8: implement", at(10), at(10, 10), extra=again)
        facts = self.measure()
        self.assertEqual((self.by(facts, "slice 8: implement")["prompts"], facts["summary"]["resumed"]), (2, 1))

    def test_an_unknown_shape_is_refused_by_name(self):
        """a transcript of an unknown shape is refused and no facts are written"""
        path = self.session / "s1" / "subagents" / "agent-a3.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        del rows[1]["message"]["usage"]
        self.write(path, rows)
        done = self.measure(ok=False)
        self.assertEqual(done.returncode, 1)
        self.assertIn("agent-a3.jsonl:2 has no usage", done.stderr)
        self.assertFalse((self.tmp / "facts.json").exists())

    def test_the_open_batch_and_from_to(self):
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)
        out = self.tmp / "open.json"
        done = self.run_script("batch", "--projects", str(self.projects), "--out", str(out))
        self.assertEqual(done.returncode, 1)
        self.assertIn("no dispatch found between %s" % at(12), done.stderr)
        self.assertFalse(out.exists())
        self.agent("a9", "bdd-implementer", "slice 10: implement", at(12, 30), at(12, 40))
        done = self.run_script("batch", "--projects", str(self.projects), "--out", str(out), "--to", at(14))
        self.assertEqual(done.returncode, 0, done.stderr)
        facts = json.loads(out.read_text())
        self.assertEqual((facts["batch"], facts["window"]["from"], list(facts["slices"])), ("open", at(12), ["10"]))
        self.assertEqual(self.measure("--from", at(6), "--to", at(9, 35))["summary"]["dispatches"], 2)

    def test_a_facts_file_is_not_written_over(self):
        """an existing facts file is not written over without --replace"""
        self.measure()
        before = (self.tmp / "facts.json").read_text()
        done = self.measure(ok=False)
        self.assertEqual(done.returncode, 1)
        self.assertIn("exists", done.stderr)
        self.assertEqual((self.tmp / "facts.json").read_text(), before)
        self.assertEqual(self.measure("--replace")["batch"], "shelf-slices-batch2")

    def test_an_archive_no_commit_added_is_refused(self):
        """an archive file no commit added is refused"""
        (self.repo / "stray.md").write_text("x")
        done = self.run_script("batch", "stray.md", "--projects", str(self.projects))
        self.assertEqual(done.returncode, 1)
        self.assertIn("was not added by any commit", done.stderr)
        self.assertIn("stray.md", done.stderr)


    def test_without_an_archive_file_the_open_batch_is_measured_from_the_last_archive_commit_to_now(self):
        """without an archive file the open batch is measured from the last archive commit to now"""
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)
        self.agent("a9", "bdd-implementer", "slice 8: implement", at(12, 30), at(12, 40))
        done, facts = self.open_batch()
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual((facts["window"]["from"], facts["window"]["from_commit"]), (at(12), self.sha(12)[:7]))
        ended = datetime.datetime.fromisoformat(facts["window"]["to"].replace("Z", "+00:00"))
        self.assertLess(abs((datetime.datetime.now(datetime.timezone.utc) - ended).total_seconds()), 300)
        self.assertEqual(list(facts["slices"]), ["8"])
        self.assertEqual((facts["slices"]["8"]["name"], facts["slices"]["8"]["lands"]), ("Ids are made in one place", [2, 1]))

    def test_a_given_option_replaces_that_end_of_the_batch(self):
        """a given --<option> replaces that end of the batch"""
        c, d = self.sha(10, 5), self.sha(11)
        for option, value, time, commit in (("--from", c, at(10, 5), c[:7]), ("--from", at(9, 5), at(9, 5), None),
                                            ("--to", d, at(11), d[:7]), ("--to", at(11, 30), at(11, 30), None)):
            with self.subTest(option=option, value=value):
                facts = self.measure(option, value, "--replace")
                end = "from" if option == "--from" else "to"
                self.assertEqual((facts["window"][end], facts["window"][end + "_commit"]), (time, commit))
                other = "to" if end == "from" else "from"
                self.assertEqual(facts["window"][other], at(12) if other == "to" else at(8))

    def test_without_out_the_facts_go_under_measurements_in_the_archive_files_name(self):
        """without --out the facts go under measurements in the archive file's name"""
        done = self.run_script("batch", self.archive % 2, "--projects", str(self.projects))
        self.assertEqual(done.returncode, 0, done.stderr)
        written = self.repo / "docs/superpowers/measurements/shelf-slices-batch2.json"
        self.assertEqual(json.loads(written.read_text())["batch"], "shelf-slices-batch2")

    def test_a_batch_with_no_dispatch_inside_it_is_refused(self):
        """a batch with no dispatch inside it is refused"""
        done = self.measure("--from", at(6), "--to", at(7), ok=False)
        self.assertEqual(done.returncode, 1)
        self.assertIn("no dispatch found between %s and %s" % (at(6), at(7)), done.stderr)
        self.assertFalse((self.tmp / "facts.json").exists())
        self.assertFalse((self.repo / "docs/superpowers/measurements").exists())

    def test_a_subagent_transcript_is_a_dispatch_only_when_it_starts_inside_the_batch(self):
        """a transcript an Agent tool started is a dispatch only when it starts inside the batch"""
        for when, start, counted in (("inside", at(9, 50), True), ("before", at(7, 10), False), ("after", at(13), False)):
            with self.subTest(when=when):
                self.agent("x" + when, "bdd-implementer", "straggler " + when, start, plus(start, 9))
                facts = self.measure("--replace")
                self.assertEqual("straggler " + when in [d["description"] for d in facts["dispatches"]], counted)
                self.assertEqual(len(facts["dispatches"]), 5 + counted)
                for path in (self.session / "s1" / "subagents").glob("agent-x*"):
                    path.unlink()

    def test_a_requests_usage_is_counted_once_and_its_reasoning_is_part_of_its_output(self):
        """a request's usage is counted once, and its reasoning is part of its output"""
        self.clear_agents()
        self.quiet_main()
        rows = [{"type": "user", "timestamp": at(10), "message": {"content": "Do it."}}]
        for minute in (2, 3, 4):
            row = self.request(at(10, minute), "same", 1200, new=500, read=2000)
            row["message"]["usage"]["output_tokens_details"]["thinking_tokens"] = 300
            rows.append(row)
        self.put("b1", "bdd-implementer", "slice 8: implement", rows)
        facts = self.measure()
        one = facts["dispatches"][0]
        self.assertEqual((one["requests"], one["new_input"], one["output"], one["thinking"]), (1, 500, 1200, 300))
        self.assertEqual((facts["summary"]["new_input"], facts["summary"]["output"], facts["summary"]["thinking"]), (500, 1200, 300))
        self.assertNotIn(1500, self.numbers(facts))

    def test_a_dispatch_is_attributed_by_its_description_then_its_prompt_else_unattributed(self):
        """a dispatch is attributed by its description, then its prompt, else unattributed"""
        for description, prompt, slice_, by in (("implement slice 2", "Do slice 3.", "2", "description"),
                                                ("batch work", "Do slice 3.", None, "description"),
                                                ("Look around", "Do slice 3.", "3", "prompt"),
                                                ("Look around", "Do the thing.", None, None)):
            with self.subTest(description=description, prompt=prompt):
                self.clear_agents()
                self.lone("w", "bdd-implementer", description, at(10), at(10, 10), prompt=prompt)
                facts = self.measure("--replace")
                one = facts["dispatches"][0]
                self.assertEqual((one["slice"], one["attributed"]), (slice_, by))
                self.assertEqual(facts["summary"]["unattributed"], 0 if by else 1)

    def test_a_reviewers_findings_are_counted_as_it_wrote_them(self):
        """a reviewer's findings are counted as it wrote them"""
        self.clear_agents()
        reply = "Needs fixes.\n- Critical: a.py:1 lost\n- Critical: b.py:2 gone\n- **Important** c.py:3 wrong\n4 Minor issues"
        self.lone("rv", "bdd-task-reviewer", "slice 8: review", at(10), at(10, 10), reply=reply)
        findings = self.measure()["dispatches"][0]["findings"]
        self.assertEqual(findings, {"critical": 2, "important": 1, "minor": 4})

    def test_a_commit_goes_to_the_implementer_running_when_it_was_made(self):
        """a commit goes to the implementer running when it was made"""
        self.clear_agents()
        self.lone("im", "bdd-implementer", "slice 8: implement", at(10, 10), at(10, 30))
        self.commit(at(10, 15), {"shelf/a.py": "a\n", "tests/test_a.py": "a\n", "docs/a.md": "a\n"})
        one = self.measure()["dispatches"][0]
        self.assertEqual(one["commits"], [self.sha(10, 15)[:7]])
        self.assertEqual(one["touched"], [1, 1, 1])

    def test_each_slices_lands_line_sits_beside_the_files_its_dispatches_touched(self):
        """each slice's Lands line sits beside the files its dispatches touched"""
        plan = "# Plan\n\n## Slice 1: Cart\n- Kind: capability\n- Lands: 2 production, 1 test\n"
        for batch, start, end, made in (("archive batch", at(10, 10), at(10, 30), at(10, 15)),
                                        ("open batch", at(12, 10), at(12, 30), at(12, 20))):
            with self.subTest(batch=batch):
                self.clear_agents()
                self.lone("im", "bdd-implementer", "slice 1: implement", start, end)
                self.commit(made, {"src/cart.py": made, "tests/test_cart.py": made})
                if batch == "archive batch":
                    (self.repo / (self.archive % 2)).write_text(plan)
                    facts = self.measure("--replace")
                    (self.repo / (self.archive % 2)).write_text(ARCHIVE % 2)
                else:
                    (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(plan)
                    done, facts = self.open_batch("--replace")
                    self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual((facts["slices"]["1"]["lands"], facts["slices"]["1"]["touched"]), ([2, 1], [1, 1, 0]))

    def test_the_facts_give_the_plans_tasks_at_both_ends_its_hand_backs_and_suite_record(self):
        """the facts give the plan's tasks at both ends, its hand-backs and suite record"""
        plan = "docs/superpowers/plans/2026-01-02-cart-implementation.md"
        tasks = lambda n: "# Plan\n\n" + "".join("### Task %d: Step\n\n" % i for i in range(1, n + 1))
        self.commit(at(9, 15), {plan: tasks(5)})
        self.commit(at(11, 30), {plan: tasks(7)})
        (self.repo / (self.archive % 2)).write_text(ARCHIVE % 2 + "- 2026-01-02 HAND-BACK slice 9 at def5678: another.\n  Evidence: x.\n")
        facts = self.measure("--tasks", plan)
        self.assertEqual(facts["tasks"], {"plan": plan, "planned": 5, "run": 7})
        self.assertEqual([one["slice"] for one in facts["hand_backs"]], ["8", "9"])
        self.assertIn("9 passed", facts["suite"])

    def test_the_facts_hold_no_prompt_reply_or_tool_content(self):
        """the facts hold no prompt, reply or tool content"""
        call = self.request(at(10, 3), "x1", 5, tool="Bash")
        call["message"]["content"][0]["input"] = {"command": "TOOLSECRET"}
        result = {"type": "user", "timestamp": at(10, 4), "message": {"content": [{"type": "tool_result", "content": "RESULTSECRET"}]}}
        self.agent("a8", "bdd-implementer", "slice 9: more", at(10, 2), at(10, 8), prompt="PROMPTSECRET please",
                   reply="DONE\n\nREPLYSECRET", extra=[call, result])
        facts = self.measure()
        self.assertEqual(self.by(facts, "slice 9: more")["status"], "DONE")
        text = json.dumps(facts)
        for secret in ("PROMPTSECRET", "REPLYSECRET", "TOOLSECRET", "RESULTSECRET"):
            self.assertNotIn(secret, text)

    def test_show_prints_a_facts_file_as_tables(self):
        """show prints a facts file as tables"""
        self.measure()
        shown = self.run_script("show", str(self.tmp / "facts.json"))
        self.assertEqual(shown.returncode, 0, shown.stderr)
        for text in ("plugin 0.12.0", "| tasks planned", "| bdd-implementer", "| controller", "hand-back: 2026-01-02", "Do the reading"):
            self.assertIn(text, shown.stdout)

    def test_compare_prints_two_facts_files_side_by_side(self):
        """compare prints two facts files side by side"""
        self.measure()
        facts = str(self.tmp / "facts.json")
        compared = self.run_script("compare", facts, facts)
        self.assertEqual(compared.returncode, 0, compared.stderr)
        self.assertRegex(compared.stdout, r"\| dispatches +\| +5 \| +5 \| +1\.0")
        self.assertIn("output per slice", compared.stdout)

    def test_show_refuses_a_file_measure_did_not_write_as_facts(self):
        """show refuses a file measure did not write as facts"""
        (self.tmp / "other.json").write_text("{}")
        done = self.run_script("show", str(self.tmp / "other.json"))
        self.assertEqual(done.returncode, 1)
        self.assertIn("other.json is not a facts file", done.stderr)

    def test_the_open_batch_needs_plan_when_the_living_plan_cannot_be_found(self):
        """the open batch needs --plan when the living plan cannot be found"""
        for plans, names in (("no", []), ("two", ["a-slices.md", "b-slices.md"])):
            with self.subTest(plans=plans):
                for name in names:
                    (self.repo / "docs/superpowers/plans" / name).write_text(ARCHIVE % 3)
                done, facts = self.open_batch()
                self.assertEqual(done.returncode, 1)
                self.assertIn("needs the living plan: name it with --plan", done.stderr)
                self.assertIsNone(facts)

    def test_a_batch_with_no_archive_before_it_needs_from(self):
        """a batch with no archive before it needs --from"""
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)
        first = self.run_script("batch", self.archive % 1, "--projects", str(self.projects))
        opened = self.run_script("batch", "--projects", str(self.projects), "--archive-dir", "nowhere/archive")
        for batch, done in (("the first archive file", first), ("the open batch", opened)):
            with self.subTest(batch=batch):
                self.assertEqual(done.returncode, 1)
                self.assertIn("give the batch's start with --from", done.stderr)

    def test_a_option_that_is_neither_a_commit_nor_an_iso_time_is_refused(self):
        """a --<option> that is neither a commit nor an ISO time is refused"""
        for option in ("--from", "--to"):
            with self.subTest(option=option):
                done = self.run_script("batch", self.archive % 2, "--projects", str(self.projects), option, "last-tuesday")
                self.assertEqual(done.returncode, 1)
                self.assertIn("last-tuesday", done.stderr)
                self.assertNotIn("Traceback", done.stderr)

    def test_gits_failures_are_refused_with_gits_error(self):
        """git's failures are refused with git's error"""
        plain, empty = self.tmp / "plain", self.tmp / "empty"
        plain.mkdir()
        empty.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=empty, check=True)
        run = lambda cwd, *args: subprocess.run([sys.executable, str(SCRIPT), "batch", "x.md", *args], capture_output=True, text=True, cwd=cwd)
        for situation, done in (("--repo", run(self.repo, "--repo", str(plain))), ("cwd", run(plain)), ("git fails", run(empty))):
            with self.subTest(situation=situation):
                self.assertEqual(done.returncode, 1)
                self.assertTrue(done.stderr.startswith("measure: git "), done.stderr)
                self.assertIn("fatal:", done.stderr)

    def test_the_open_batch_is_named_by_name_default_open(self):
        """the open batch is named by --name, default open"""
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)
        self.agent("a9", "bdd-implementer", "slice 8: implement", at(12, 30), at(12, 40))
        for option, name in (([], "open"), (["--name", "trial-3"], "trial-3")):
            with self.subTest(name=name):
                done = self.run_script("batch", "--projects", str(self.projects), *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                written = self.repo / "docs/superpowers/measurements" / (name + ".json")
                self.assertEqual(json.loads(written.read_text())["batch"], name)

    def test_without_out_the_open_batch_facts_go_under_measurements_in_its_name(self):
        """without --out the open batch's facts go under measurements in its name"""
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)
        self.agent("a9", "bdd-implementer", "slice 8: implement", at(12, 30), at(12, 40))
        for option, name in (([], "open"), (["--name", "trial-3"], "trial-3")):
            with self.subTest(name=name):
                done = self.run_script("batch", "--projects", str(self.projects), *option)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertTrue((self.repo / "docs/superpowers/measurements" / (name + ".json")).exists())

    def test_the_open_batch_starts_at_the_last_commit_that_added_a_file_under_the_archive_directory(self):
        """the open batch starts at the last commit that added a file under the archive directory"""
        self.commit(at(9, 50), {"old/plans/p.md": "x\n"})
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)
        self.agent("a9", "bdd-implementer", "slice 8: implement", at(12, 30), at(12, 40))
        for option, commit in (([], self.sha(12)), (["--archive-dir", "old/plans"], self.sha(9, 50))):
            with self.subTest(option=option):
                done, facts = self.open_batch(*option, "--replace")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(facts["window"]["from_commit"], commit[:7])

    def test_the_facts_hold_the_slices_the_batch_planned_and_the_slices_dispatches_were_attributed_to(self):
        """the facts hold the slices the batch planned and the slices dispatches were attributed to"""
        plan = "# Plan\n\n## Slice 1: A\n\n## Slice 2: B\n"
        (self.repo / (self.archive % 2)).write_text(plan)
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(plan)
        for batch, first, second, expected in (("archive batch", at(10), at(10, 20), ["1", "2", "3"]),
                                               ("open batch", at(12, 10), at(12, 30), ["2", "3"])):
            with self.subTest(batch=batch):
                self.clear_agents()
                self.lone("s2", "bdd-implementer", "slice 2: implement", first, plus(first, 9))
                self.lone("s3", "bdd-implementer", "slice 3: implement", second, plus(second, 9))
                if batch == "archive batch":
                    facts = self.measure("--replace")
                else:
                    done, facts = self.open_batch("--replace")
                    self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(list(facts["slices"]), expected)

    def test_a_commit_made_while_two_implementers_ran_is_counted_as_ambiguous(self):
        """a commit made while two implementers ran is counted as ambiguous"""
        self.clear_agents()
        self.lone("i1", "bdd-implementer", "slice 8: implement", at(10, 10), at(10, 20))
        self.lone("i2", "bdd-implementer", "slice 9: implement", at(10, 12), at(10, 30))
        self.commit(at(10, 15), {"shelf/a.py": "a\n"})
        self.assertEqual(self.measure()["summary"]["ambiguous_commits"], 1)

    def test_tasks_are_left_uncounted_with_a_note_when_the_batch_plan_cannot_be_had(self):
        """tasks are left uncounted with a note when the batch plan cannot be had"""
        self.clear_agents()
        self.lone("w", "bdd-implementer", "slice 8: implement", at(10), at(10, 10))
        cases = (("no ledger", [], "no dispatch names a ledger"),
                 ("in no commit", ["--tasks", "docs/superpowers/plans/ghost.md"], "docs/superpowers/plans/ghost.md is in no commit"))
        for situation, args, why in cases:
            with self.subTest(situation=situation):
                done = self.measure(*args, "--replace", ok=False)
                self.assertEqual(done.returncode, 0, done.stderr)
                facts = json.loads((self.tmp / "facts.json").read_text())
                self.assertIsNone(facts["tasks"])
                self.assertEqual(len(facts["notes"]), 1)
                self.assertIn(why, facts["notes"][0])
                self.assertIn("measure: " + facts["notes"][0], done.stderr)

    def test_a_written_batch_is_reported_in_one_line(self):
        """a written batch is reported in one line"""
        self.clear_agents()
        for i in range(6):
            self.lone("w%d" % i, "bdd-implementer", "slice %d: step" % (8 + i % 2), at(9, 5 * i), at(9, 5 * i + 4))
        done = self.measure(ok=False)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.splitlines(), ["%s: 6 dispatches, 2 slices, %s to %s" % (
            os.path.relpath(self.tmp / "facts.json", self.repo), at(8), at(12))])

    def test_a_reply_closing_status_is_counted_as_not_done(self):
        """a reply closing <status> is counted as not done"""
        for status in ("BLOCKED", "PARTIAL", "NEEDS_CONTEXT"):
            with self.subTest(status=status):
                self.clear_agents()
                self.lone("w", "bdd-implementer", "slice 8: implement", at(10), at(10, 10), reply=status + "\n\nwhy")
                facts = self.measure("--replace")
                self.assertEqual(facts["dispatches"][0]["status"], status)
                self.assertEqual(facts["summary"]["not_done"], 1)

    def test_the_facts_record_the_versions_the_transcripts_name_and_the_window(self):
        """the facts record the versions the transcripts name and the window"""
        self.clear_agents()
        self.quiet_main()
        self.lone("w", "bdd-implementer", "slice 8: implement", at(10), at(10, 10), plugin="0.18.0", version="2.1.4")
        facts = self.measure()
        self.assertEqual((facts["plugin_versions"], facts["harness_versions"]), (["0.18.0"], ["2.1.4"]))
        self.assertEqual(facts["window"], {"from": at(8), "to": at(12), "from_commit": self.sha(8)[:7], "to_commit": self.sha(12)[:7]})

    def test_a_batch_starting_at_a_commit_gives_the_files_and_lines_changed_to_its_end(self):
        """a batch starting at a commit gives the files and lines changed to its end"""
        self.commit(at(12, 10), {"late.py": "a\nb\nc\n"})
        self.agent("a9", "bdd-implementer", "slice 8: implement", at(12, 30), at(12, 40))
        (self.repo / "docs/superpowers/plans/shelf-slices.md").write_text(ARCHIVE % 3)

        def changed(start, end):
            rows = [line.split("\t") for line in self.git("diff", "--numstat", start, end).splitlines()]
            return len(rows), sum(int(a) + int(b) for a, b, _ in rows)

        a, b = self.sha(8), self.sha(12)
        cases = (("at commit B", lambda: self.measure("--replace"), changed(a, b)),
                 ("at an ISO time", lambda: self.measure("--to", at(11, 30), "--replace"), changed(a, "HEAD")),
                 ("now", lambda: self.open_batch("--replace")[1], changed(b, "HEAD")))
        self.assertNotEqual(changed(a, b), changed(a, "HEAD"))
        for end, run, (files, lines) in cases:
            with self.subTest(end=end):
                summary = run()["summary"]
                self.assertEqual((summary["files_changed"], summary["lines_changed"]), (files, lines))

    def test_the_facts_count_resumed_dispatches_the_late_share_of_building_time_without_scouts_and_starting_context(self):
        """the facts count resumed dispatches, the late share of building time without scouts, and starting context"""
        self.clear_agents()
        self.lone("i1", "bdd-implementer", "implementer 1", at(10, 0), at(10, 30), ctx=20000)
        self.lone("i2", "bdd-implementer", "implementer 2", at(10, 0), at(10, 30), ctx=30000)
        self.lone("r1", "bdd-branch-reviewer", "review 1", at(10, 40), at(10, 50), ctx=40000)
        self.lone("f1", "bdd-implementer", "fix 1", at(11, 0), at(11, 30), ctx=10000, prompts=2)
        self.lone("s1", "code-scout", "scout 1", at(11, 0), at(11, 15), ctx=50000)
        summary = self.measure()["summary"]
        self.assertEqual(summary["resumed"], 1)
        self.assertEqual(summary["closing_share"], 0.4)
        self.assertEqual((summary["mean_first_context"], summary["first_context_total"]), (30000, 150000))

    def test_show_prints_the_header_the_tables_the_exceptions_the_hand_backs_and_the_notes(self):
        """show prints the header, the tables, the exceptions, the hand-backs and the notes"""
        self.measure("--tasks", "docs/superpowers/plans/ghost.md")
        shown = self.run_script("show", str(self.tmp / "facts.json")).stdout
        order = ["shelf, batch shelf-slices-batch2", "plugin 0.12.0; harness 2.1.0", "Suite: 9 passed", "| batch ", "| role ", "| slice ",
                 "| not done or not attributed", "Look around", "Do the reading", "hand-back: 2026-01-02", "note: "]
        places = [shown.index(text) for text in order]
        self.assertEqual(places, sorted(places), shown)

    def test_compare_prints_both_files_figures_with_the_ratio_of_the_second_to_the_first(self):
        """compare prints both files' figures with the ratio of the second to the first"""
        facts = self.measure()
        a, b = json.loads(json.dumps(facts)), json.loads(json.dumps(facts))
        a.update(batch="2026-09-01", plugin_versions=["0.17.0"])
        b.update(batch="2026-09-15", plugin_versions=["0.18.0"])
        for key in ("output", "new_input", "cache_read", "agent_minutes"):
            b["summary"][key] = a["summary"][key] * 2
        (self.tmp / "a.json").write_text(json.dumps(a))
        (self.tmp / "b.json").write_text(json.dumps(b))
        shown = self.run_script("compare", str(self.tmp / "a.json"), str(self.tmp / "b.json"))
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertIn("2026-09-01 (0.17.0)", shown.stdout.splitlines()[0])
        self.assertIn("2026-09-15 (0.18.0)", shown.stdout.splitlines()[0])
        cell = lambda n: "{:,}".format(n) if isinstance(n, int) else "%.1f" % n
        for label, key in (("output tokens", "output"), ("new input tokens", "new_input"), ("cache read tokens", "cache_read"),
                           ("agent minutes", "agent_minutes")):
            self.assertRegex(shown.stdout, r"\| %s +\| +%s \| +%s \| +2\.0" % (label, re.escape(cell(a["summary"][key])), re.escape(cell(b["summary"][key]))))
        for label, key in (("output per slice", "output"), ("new input per slice", "new_input"), ("cache read per slice", "cache_read"),
                           ("agent minutes per slice", "agent_minutes")):
            per = [round(f["summary"][key] / f["summary"]["slices"], None if key != "agent_minutes" else 1) for f in (a, b)]
            self.assertRegex(shown.stdout, r"\| %s +\| +%s \| +%s \| +2\.0" % (label, re.escape(cell(per[0])), re.escape(cell(per[1]))))
        self.assertRegex(shown.stdout, r"\| dispatches +\| +5 \| +5 \| +1\.0")

    def test_a_file_measure_cannot_read_as_its_facts_is_refused(self):
        """a file measure cannot read as its facts is refused"""
        self.measure()
        good = str(self.tmp / "facts.json")
        (self.tmp / "other.json").write_text("{}")
        (self.tmp / "broken.json").write_text("not json {")
        for command, name, reason in (("compare", "other.json", "is not a facts file"), ("show", "broken.json", "Expecting value"),
                                      ("compare", "broken.json", "Expecting value")):
            with self.subTest(command=command, name=name):
                path = str(self.tmp / name)
                done = self.run_script(command, good, path) if command == "compare" else self.run_script(command, path)
                self.assertEqual(done.returncode, 1)
                self.assertIn(path, done.stderr)
                self.assertIn(reason, done.stderr)
                self.assertNotEqual("is not a facts file" in done.stderr, name == "broken.json")

    def test_a_refusal_says_why_on_stderr_and_exits_1(self):
        """a refusal says why on stderr and exits with an error"""
        self.measure()
        done = self.measure(ok=False)
        self.assertEqual(done.returncode, 1)
        self.assertRegex(done.stderr, r"^measure: .*exists")
        self.assertEqual(done.stdout, "")


FEATURE = pathlib.Path(__file__).resolve().parents[2] / "features" / "batch-measurement.feature"


class BindingTest(unittest.TestCase):
    def test_every_scenario_has_its_test(self):
        self.assertEqual(missing(FEATURE, MeasureTest), [])


if __name__ == "__main__":
    unittest.main()
