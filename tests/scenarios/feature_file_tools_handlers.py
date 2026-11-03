"""feature-file-tools' handlers (design §14.3): the Givens write feature files and test modules into the scenario's
repository, as the given block holds them or, for a feature file named with no text, as FEATURES below has it; the
command runs through world_run's `WhenRuns`; the Thens read what `features` printed.

Each canned feature file comes with the number of scenarios `features count --by-tag` gives it."""
import textwrap

from vocab import handler

FEATURES = {
    "features/notes.feature": (1, """\
        Feature: Notes
          Scenario: Nested
            Given a note
              \"\"\"
              @slice-9
              Scenario: Phantom
              \"\"\"
        """),
    "features/outline.feature": (3, """\
        @cart
        Feature: Outline
          Scenario Outline: Adding several
            When the shopper adds <n> pens

            Examples:
              | n |
              | 2 |
              | 3 |

            @slow
            Examples:
              | n  |
              | 10 |
        """),
    "features/rule.feature": (1, """\
        Feature: Rules
          Rule: one rule
            Scenario: Under a rule
              Given a step
        """),
    "features/shelf.feature": (1, """\
        # generated from spec/capabilities/shelf.md by features generate; do not edit
        Feature: shelf
          Narrator: a client

          @g1 @r1
          Scenario: Lending
            When the person lends a book
        """),
}


def bare(word):
    return word.strip("`")


def write(step, rel, text, scenarios):
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    step.context.setdefault("scenarios", {})[rel] = scenarios


@handler("GivenK", "feature file")
def given_canned(step):
    rel = bare(step.names[0])
    count, text = FEATURES[rel]
    write(step, rel, textwrap.dedent(text), count)


@handler("GivenCodeText", "feature file")
def given_feature(step):
    text = step.docstring + "\n"
    write(step, bare(step.names[0]), text, sum(line.strip().startswith("Scenario") for line in text.splitlines()))


@handler("GivenCodeText", "test module")
def given_module(step):
    path = step.repo / bare(step.names[0])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(step.docstring + "\n")


def result(step):
    done = step.context["result"]
    assert "Traceback" not in done.stderr, done.stderr
    return done


@handler("ThenPrints", "`features`")
def prints(step):
    out = result(step).stdout
    for np in step.nps:
        if np == "the number of scenarios":
            assert "total %d\n" % sum(step.context["scenarios"].values()) in out, out
        else:
            want = np.strip('"') if np.startswith('"') else bare(np.split()[-1])
            assert want in out, (want, out)


@handler("ThenPrintsNot", "`features`")
def prints_not(step):
    out = result(step).stdout
    for np in step.nps:
        assert bare(np.split()[-1]) not in out, (np, out)
