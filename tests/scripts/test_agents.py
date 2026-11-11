"""The 2.0 agents (design-decision/the-2-0-agents, 0083), checked by reading the agent definitions under agents/:
`pr-reviewer` (opus; no Edit, Write or shell), `architecture-reviewer` (opus; no Edit or Write) and `trial-runner`
(sonnet), and no agent can start an agent. A reviewer's findings are its reply (plan-9 rulings Q2)."""
import pathlib
import unittest

AGENTS = pathlib.Path(__file__).resolve().parents[2] / "agents"
REVIEWERS = ("architecture-reviewer", "pr-reviewer")
AGENTS_2_0 = ("architecture-reviewer", "pr-reviewer", "trial-runner")
SKILLS = AGENTS.parent / "skills"
FORMULATOR = "feature-" + "formulator"     # spelled so, the plan's grep for it finds no file
SHELL = ("Bash",)
EDIT = ("Edit", "NotebookEdit")
WRITE = ("Write",)


def definition(path):
    """The frontmatter of one agent definition: its scalar keys, `tools` as a list and `skills` as a list."""
    lines = path.read_text().splitlines()
    assert lines[0] == "---", "%s has no frontmatter" % path.name
    found, key = {"skills": []}, None
    for line in lines[1:lines.index("---", 1)]:
        if line.startswith("  - ") and key == "skills":
            found["skills"].append(line[4:].strip())
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if key != "skills":
            found[key] = value.strip()
    found["tools"] = [tool.strip() for tool in found.get("tools", "").split(",") if tool.strip()]
    return found


def agents():
    return {path.stem: definition(path) for path in sorted(AGENTS.glob("*.md"))}


class RoleBoundaries(unittest.TestCase):
    def setUp(self):
        self.agents = agents()

    def named(self, name):
        self.assertIn(name, self.agents, "agents/%s.md is missing" % name)
        return self.agents[name]

    def test_the_agents_are_the_2_0_set(self):
        self.assertEqual(sorted(self.agents), list(AGENTS_2_0))

    def test_no_agent_starts_an_agent(self):
        starters = sorted(name for name, one in self.agents.items() if {"Agent", "Task"} & set(one["tools"]))
        self.assertEqual(starters, [])

    def test_no_reviewer_has_edit(self):
        for name in REVIEWERS:
            with self.subTest(agent=name):
                self.assertFalse(set(EDIT) & set(self.named(name)["tools"]))

    def test_pr_reviewer_has_no_write_or_shell(self):
        self.assertFalse(set(EDIT + WRITE + SHELL) & set(self.named("pr-reviewer")["tools"]))

    def test_architecture_reviewer_has_no_write_and_replies_with_its_findings(self):
        """The harness refuses a subagent's Write of a findings file (plan-7 Q1), so the findings are the reply."""
        self.assertFalse(set(EDIT + WRITE) & set(self.named("architecture-reviewer")["tools"]))
        text = (AGENTS / "architecture-reviewer.md").read_text()
        self.assertIn("your reply is the findings", text.lower())
        for old in ("work-item", "initiative", "branch review"):
            with self.subTest(word=old):
                self.assertNotIn(old, text)

    def test_each_agent_names_its_model(self):
        expected = {"architecture-reviewer": "opus", "pr-reviewer": "opus", "trial-runner": "sonnet"}
        for name, model in expected.items():
            with self.subTest(agent=name):
                self.assertEqual(self.named(name).get("model"), model)


if __name__ == "__main__":
    unittest.main()


class CodifiedFlow(unittest.TestCase):
    """The GF conversion's design §13.1-§13.2: no formulator, the raising-a-request skill, and no agent or skill naming
    the formulator."""

    def test_no_feature_formulator_agent(self):
        self.assertFalse((AGENTS / (FORMULATOR + ".md")).exists())

    def test_raising_a_request_checks_every_line_with_model_parse_before_work_request(self):
        text = (SKILLS / "raising-a-request" / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: raising-a-request\n"))
        for words in ("model lexicon", "model parse --file", "work request"):
            self.assertIn(words, text)

    def test_no_agent_or_skill_names_the_formulator(self):
        for path in sorted(AGENTS.glob("*.md")) + sorted(SKILLS.rglob("*.md")):
            with self.subTest(path=path.name):
                self.assertNotIn(FORMULATOR, path.read_text())

    def test_no_doc_names_telingo_as_current(self):
        """Revision 3: `model logic` is one clingo solve of `grammar/check.lp`; telingo is history, kept only under
        `docs/history/` (design model v5, b247), which no current page is."""
        root = AGENTS.parent
        pages = [root / "README.md"] + [path for path in sorted((root / "docs").rglob("*.md"))
                                        if "history" not in path.relative_to(root / "docs").parts[:1]]
        for path in pages:
            with self.subTest(path=str(path.relative_to(root))):
                hits = [line for line in path.read_text().splitlines()
                        if "telingo" in line or "&tel" in line]
                self.assertEqual(hits, [])
