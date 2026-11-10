"""The CLI pack's refusal in a codified-2 feature (b240 phase 15): "`work` shall refuse the command and name X" is
generated as two Thens, "`work` refuses `work decision`" and "`work` names the `--tier` option". A tool refuses a
command when it exits with an error on it (the pack's definition); what it names is in its output or its error: a
code without its backticks, an instance by what a Given said it is named by (`says`), else by its name."""
from vocab import handler


def bare(word):
    return word.strip("`")


def result(step):
    done = step.context.get("result")
    assert done is not None, "no command ran before: %s" % step.text
    return done


@handler("ThenDoes", "refuse")
def refuses(step):
    done = result(step)
    assert done.returncode != 0, (step.text, done.stdout)
    assert done.stderr.strip(), (step.text, "no error")


@handler("ThenDoes", "name")
def names(step):
    done, says = result(step), step.context.get("says", {})
    words = [q.strip('"') for q in step.quoted]
    for np in step.nps:
        words += [bare(w) for w in np.split() if w.startswith("`")]
        words += [says.get(w, w) for w in np.split() if w in step.names]
    assert words, step.text
    for word in words:
        assert word in done.stdout + done.stderr, (word, done.stdout, done.stderr)
