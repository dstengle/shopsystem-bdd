"""capability/role-boundaries r1-r6, checked by reading the agent definitions under agents/."""
import pathlib
import unittest

AGENTS = pathlib.Path(__file__).resolve().parents[2] / "agents"
REVIEWERS = ("bdd-task-reviewer", "bdd-branch-reviewer", "architecture-reviewer")
SPEC_WRITERS = ("capability-writer", "feature-formulator")
SHELL = ("Bash",)
EDIT = ("Edit", "NotebookEdit")


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

    def test_r1_only_initiative_round_starts_an_agent(self):
        starters = sorted(name for name, one in self.agents.items() if {"Agent", "Task"} & set(one["tools"]))
        self.assertEqual(starters, ["initiative-round"])

    def test_r2_no_reviewer_scout_or_planner_has_edit(self):
        for name in REVIEWERS + ("code-scout", "bdd-planner"):
            with self.subTest(agent=name):
                self.assertFalse(set(EDIT) & set(self.named(name)["tools"]))

    def test_r3_spec_writers_have_no_edit_and_no_shell(self):
        for name in SPEC_WRITERS:
            with self.subTest(agent=name):
                self.assertFalse(set(EDIT + SHELL) & set(self.named(name)["tools"]))

    def test_r4_implementer_skills_include_red_green(self):
        self.assertIn("shopsystem-bdd:bdd-red-green", self.named("bdd-implementer")["skills"])

    @unittest.expectedFailure
    def test_r4_implementer_has_no_skill_tool(self):
        # agents/bdd-implementer.md has had the Skill tool since 3ab836c (delivery-5: supervision r12 needs it).
        # r4 says it has none; the line waits on the person's ruling, and this check flips when it is made.
        self.assertNotIn("Skill", self.named("bdd-implementer")["tools"])

    def test_r5_each_agent_names_its_model(self):
        expected = dict.fromkeys(SPEC_WRITERS + ("bdd-planner",) + REVIEWERS, "opus")
        expected.update({"bdd-implementer": "sonnet", "initiative-round": "sonnet", "code-scout": "haiku"})
        for name, model in expected.items():
            with self.subTest(agent=name):
                self.assertEqual(self.named(name).get("model"), model)

    def test_r6_planner_has_no_shell(self):
        self.assertFalse(set(SHELL) & set(self.named("bdd-planner")["tools"]))


if __name__ == "__main__":
    unittest.main()
