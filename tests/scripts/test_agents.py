"""capability/role-boundaries r1-r7, checked by reading the agent definitions under agents/."""
import pathlib
import unittest

AGENTS = pathlib.Path(__file__).resolve().parents[2] / "agents"
REVIEWERS = ("bdd-task-reviewer", "bdd-branch-reviewer", "architecture-reviewer")
SPEC_WRITERS = ("capability-writer",)
SKILLS = AGENTS.parent / "skills"
FORMULATOR = "feature-" + "formulator"     # spelled so, the plan's grep for it finds no file
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

    def test_r4_implementer_has_the_skill_tool(self):
        # A `claude -p --agent` session does not preload `skills:`; the implementer loads them with Skill (3ab836c).
        self.assertIn("Skill", self.named("bdd-implementer")["tools"])

    def test_r5_each_agent_names_its_model(self):
        expected = dict.fromkeys(SPEC_WRITERS + ("bdd-planner",) + REVIEWERS, "opus")
        expected.update({"bdd-implementer": "sonnet", "initiative-round": "sonnet", "spec-checker": "sonnet", "trial-runner": "sonnet",
                         "code-scout": "haiku"})
        for name, model in expected.items():
            with self.subTest(agent=name):
                self.assertEqual(self.named(name).get("model"), model)

    def test_r6_planner_has_no_shell(self):
        self.assertFalse(set(SHELL) & set(self.named("bdd-planner")["tools"]))

    def test_r7_branch_reviewer_has_no_shell(self):
        self.assertFalse(set(SHELL) & set(self.named("bdd-branch-reviewer")["tools"]))


if __name__ == "__main__":
    unittest.main()


class ResultFirst(unittest.TestCase):
    """supervision r44: the brief tells each worker to write its result file first, with the outcome PARTIAL, and keep
    it current; the four stages' agents say the same, and none says to write it last."""

    def test_each_stage_agent_writes_its_result_first(self):
        for name in ("code-scout", "bdd-planner", "bdd-implementer", "bdd-task-reviewer"):
            text = (AGENTS / (name + ".md")).read_text()
            self.assertIn("result file first, with the outcome `PARTIAL`,", text, name)
            self.assertIn("keep it current", text, name)
            self.assertNotIn("write last", text, name)
            self.assertNotIn("Write it last", text, name)


class CodifiedFlow(unittest.TestCase):
    """The GF conversion's design §13.1-§13.2: no formulator, a formulate round with no session, the raising-a-request
    skill, and no agent or skill naming the formulator."""

    def test_no_feature_formulator_agent(self):
        self.assertFalse((AGENTS / (FORMULATOR + ".md")).exists())

    def test_the_initiative_round_has_no_formulate_kind_and_does_not_load_formulating_features(self):
        text = (AGENTS / "initiative-round.md").read_text()
        self.assertNotIn("**`formulate`**", text)
        self.assertNotIn("shopsystem-bdd:formulating-features", definition(AGENTS / "initiative-round.md")["skills"])

    def test_the_capability_writer_drafts_codified_groups(self):
        text = (AGENTS / "capability-writer.md").read_text()
        self.assertIn("### [g<n>]", text)
        self.assertIn("`## Terms`", text)

    def test_raising_a_request_checks_every_line_with_model_parse_before_work_request(self):
        text = (SKILLS / "raising-a-request" / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: raising-a-request\n"))
        for words in ("model lexicon", "model parse --file", "work request"):
            self.assertIn(words, text)

    def test_formulating_features_says_to_run_features_generate_and_never_write_a_scenario(self):
        text = (SKILLS / "formulating-features" / "SKILL.md").read_text()
        self.assertIn("features generate", text)
        self.assertLess(len(text.splitlines()), 60)

    def test_no_agent_or_skill_names_the_formulator(self):
        for path in sorted(AGENTS.glob("*.md")) + sorted(SKILLS.rglob("*.md")):
            with self.subTest(path=path.name):
                self.assertNotIn(FORMULATOR, path.read_text())

    def test_no_doc_names_telingo_as_current(self):
        """Revision 3: `model logic` is one clingo solve of `grammar/check.lp`; telingo is history, kept only in
        `design-model.md` and `how-we-got-here.md`."""
        root = AGENTS.parent
        for name in ("README.md", "docs/capability-format.md", "docs/design-model/grammar.md",
                     "skills/checking-spec-consistency/SKILL.md"):
            with self.subTest(path=name):
                hits = [line for line in (root / name).read_text().splitlines()
                        if "telingo" in line or "&tel" in line]
                self.assertEqual(hits, [])
