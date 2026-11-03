"""Shared handlers for running a command and reading what it did (design §14.3): every `WhenRuns` runs the named
command of the plugin in the scenario's repository, on the instances the step names; the Then templates read its exit
status and output. A capability's handler for a (template, term) takes precedence over these fallbacks. Frozen after
layer 2."""
import shlex

from vocab import handler


def bare(word):
    return word.strip("`")


def result(step):
    done = step.context.get("result")
    assert done is not None, "no command ran before: %s" % step.text
    return done


def mentions(step):
    """What a step's noun phrases name in output: instance names, codes without backticks, quoted texts."""
    out = [bare(n) for n in step.names] + [q.strip('"') for q in step.quoted]
    for np in step.nps:
        out += [bare(w) for w in np.split() if w.startswith("`") and bare(w) not in out]
    return out


@handler("GivenFeat")
def feature_given(step):
    step.context.setdefault("flags", []).append(bare(step.term))


@handler("WhenRuns")
def runs(step):
    words = shlex.split(bare(step.command or step.term))
    args = words[1:] + [bare(n) for n in step.names] + step.context.get("flags", [])
    step.context["result"] = step.run(words[0], *args)


@handler("ThenExitsOk")
def exits_ok(step):
    done = result(step)
    assert done.returncode == 0, done.stdout + done.stderr


@handler("ThenExitsErr")
def exits_err(step):
    done = result(step)
    assert done.returncode != 0, done.stdout
    for word in mentions(step):
        assert word in done.stdout + done.stderr, (word, done.stderr)


@handler("ThenPrints")
def prints(step):
    done = result(step)
    for word in mentions(step):
        assert word in done.stdout, (word, done.stdout)


@handler("ThenPrintsNot")
def prints_not(step):
    done = result(step)
    for word in mentions(step):
        assert word not in done.stdout.split(), (word, done.stdout)


@handler("ThenChangesNothing")
def changes_nothing(step):
    runs = step.request.node.__dict__.get("_shop_runs", [])
    assert runs and not runs[-1]["changed"], runs[-1:] or "no command ran"
