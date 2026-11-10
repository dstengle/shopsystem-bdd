"""The twins of grammar/language.md's `## Constructs` (b240): each line that grammar 4 reads is also read by the check
and by the step generator, and linearises back to itself, in the fixture (the spec corpus's checks 2 and 4)."""
import pathlib
import re
import sys

import pytest
import test_corpus_spec

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


def twins():
    text = (REPO / "grammar" / "language.md").read_text()
    constructs = text.split("\n## Constructs", 1)[1].split("\n## ", 1)[0]
    found = [b.split("\n", 1) for b in BLOCK.findall(constructs)]
    return [line for line, said in found if not said.startswith("refused:")]


def test_the_constructs_have_twins():
    assert any("conform" in line for line in twins())


@pytest.mark.parametrize("line", twins())
def test_each_twin_is_read_by_the_check_and_the_steps(line):
    toolchain.require()
    wrong, _ = test_corpus_spec.reading(FIXTURE, "twin", "r1", line)
    assert wrong == []
