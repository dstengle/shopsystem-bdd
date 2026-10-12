import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

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
        base = self.session / "s1" / "subagents" / ("agent-%s" % name)
        self.write(base.with_suffix(".jsonl"), rows)
        base.with_suffix(".meta.json").write_text(json.dumps({"agentType": "shopsystem-bdd:" + role, "description": description, "model": "opus"}))

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
        self.measure()
        before = (self.tmp / "facts.json").read_text()
        done = self.measure(ok=False)
        self.assertEqual(done.returncode, 1)
        self.assertIn("exists", done.stderr)
        self.assertEqual((self.tmp / "facts.json").read_text(), before)
        self.assertEqual(self.measure("--replace")["batch"], "shelf-slices-batch2")

    def test_an_archive_no_commit_added_is_refused(self):
        (self.repo / "stray.md").write_text("x")
        done = self.run_script("batch", "stray.md", "--projects", str(self.projects))
        self.assertEqual(done.returncode, 1)
        self.assertIn("was not added by any commit", done.stderr)

    def test_show_and_compare(self):
        self.measure()
        facts = str(self.tmp / "facts.json")
        shown = self.run_script("show", facts)
        self.assertEqual(shown.returncode, 0, shown.stderr)
        for text in ("plugin 0.12.0", "| tasks planned", "| bdd-implementer", "| controller", "hand-back: 2026-01-02", "Do the reading"):
            self.assertIn(text, shown.stdout)
        compared = self.run_script("compare", facts, facts)
        self.assertEqual(compared.returncode, 0, compared.stderr)
        self.assertRegex(compared.stdout, r"\| dispatches +\| +5 \| +5 \| +1\.0")
        self.assertIn("output per slice", compared.stdout)
        (self.tmp / "other.json").write_text("{}")
        self.assertEqual(self.run_script("show", str(self.tmp / "other.json")).returncode, 1)


if __name__ == "__main__":
    unittest.main()
