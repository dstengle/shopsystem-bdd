"""The docs test (the user docs' design, §9): README.md, CHANGELOG.md's newest section and every docs/**/*.md but
docs/history/ kept true. A ```reading block reads as it says in this repository's grammar 4 (every other requirement
line and every Gherkin block is test_docs_lines.py's); a ```console line of a plugin tool names subcommands and
options its argparse knows; every subcommand has its subsection in docs/reference/commands.md, every relative link
resolves, and the example context docs/examples/notes-cli/ passes `model check` and `features generate --check`."""
import pathlib
import re
import subprocess
import sys

import pytest
import spec_grammar4

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain
from docs_testing import (
    COMMANDS,
    EXAMPLE,
    REPO,
    TOOLS,
    blocks_of,
    command_problem,
    console_commands,
    fenced,
    leaves,
    link_problem,
    links,
    pages,
    tool_words,
)
from test_spec_lf_read import reading

PAGES = ("README.md", "docs/index.md", "docs/getting-started.md", "docs/tour.md", "docs/talking-with-claude.md",
         "docs/concepts.md", "docs/writing-requirements.md", "docs/recipes.md", "docs/reference/commands.md",
         "docs/reference/capability-file.md", "docs/reference/design-model.md", "docs/how-it-works.md",
         "docs/troubleshooting.md", "docs/upgrading.md", "CHANGELOG.md", "docs/history/README.md")


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return spec_grammar4.load(REPO)[0]


def test_the_pages_of_the_design_are_there():
    assert [p for p in PAGES if not (REPO / p).is_file()] == []
    assert (EXAMPLE / "spec" / "index.md").is_file(), "docs/examples/notes-cli/ has no spec/index.md"


def test_every_fenced_block_is_closed():
    """A fence left open would hide the rest of its page from every other check."""
    unclosed = []
    for page, text in pages().items():
        opened = sum(1 for line in text.splitlines() if re.match(r"^\s*(```|~~~)", line))
        if opened % 2:
            unclosed.append(page)
    assert unclosed == []


def test_each_reading_block_reads_as_it_says(vocab):
    """(1) A ```reading block is a line, then what grammar 4 reads it as in this repository: its logical form as
    `model parse --form` prints it, or its refusal (grammar/language.md's convention)."""
    wrong = []
    for where, body in blocks_of("reading"):
        line, said = body[0], "\n".join(body[1:])
        got = reading(vocab, line, REPO)
        if got != said:
            wrong.append("%s: %s\n--- the page says:\n%s\n--- grammar 4 reads:\n%s" % (where, line, said, got))
    assert wrong == [], "\n\n".join(wrong)


def test_each_console_command_of_a_plugin_tool_exists():
    """(4) Each `$ ` line of a ```console block whose first word is a plugin tool names subcommands its argparse
    knows and options its subcommand's --help lists. Output lines are not compared."""
    wrong = []
    for where, command in console_commands():
        run = tool_words(command)
        if run and (why := command_problem(*run)):
            wrong.append("%s: $ %s\n  %s" % (where, command, why))
    assert wrong == [], "\n".join(wrong)


def test_the_console_check_knows_a_wrong_command_from_a_right_one():
    assert command_problem("work", ["batch", "start"]) is None
    assert command_problem("work", ["backlog", "--json"]) is None
    assert command_problem("model", ["--root", "x", "parse", "--form", "a line"]) is None
    assert "no subcommand frobnicate" in command_problem("work", ["frobnicate"])
    assert "no option --nope" in command_problem("work", ["backlog", "--nope"])
    assert tool_words("python3 ~/.claude/plugins/x/scripts/model check") == ("model", ["check"])
    assert tool_words("git status") is None


def test_every_subcommand_has_its_subsection_in_the_commands_reference():
    """(5) Every runnable command of every tool, read off its argparse (`work batch start` and its siblings each its
    own), is the start of a heading of docs/reference/commands.md."""
    assert COMMANDS.is_file(), "docs/reference/commands.md is not there"
    headings = [re.sub(r"[`*]", "", m.group(1)).strip()
                for _, line in fenced(COMMANDS.read_text(encoding="utf-8"))[1]
                if (m := re.match(r"^#{2,6}\s+(.*)$", line))]
    missing = [c for tool in TOOLS for c in leaves(tool)
               if not any(re.match(re.escape(c) + r"(?![\w-])", h) for h in headings)]
    assert missing == [], "no subsection in docs/reference/commands.md: " + ", ".join(missing)


def test_every_relative_link_resolves():
    """(5) Every relative link of the pages names a file that is there, and an anchor a docs page has."""
    broken = [why for page, text in pages().items() for _, target in links(text)
              if (why := link_problem(page, target))]
    assert broken == [], "\n".join(broken)


def run_in_example(*command):
    return subprocess.run([sys.executable, *command], cwd=EXAMPLE, capture_output=True, text=True, timeout=900)


def test_the_example_context_passes_model_check():
    """(5) docs/examples/notes-cli/ is a context `model check` finds nothing wrong with."""
    toolchain.require()
    done = run_in_example(str(REPO / "scripts" / "model"), "--root", ".", "check")
    assert done.returncode == 0, done.stdout + done.stderr


def test_the_example_context_features_are_current():
    """(5) docs/examples/notes-cli/'s feature files are what `features generate` writes of its spec."""
    toolchain.require()
    done = run_in_example(str(REPO / "scripts" / "features"), "generate", "--check", "--root", ".")
    assert done.returncode == 0, done.stdout + done.stderr
