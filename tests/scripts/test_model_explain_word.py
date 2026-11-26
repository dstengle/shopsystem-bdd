"""model_explain's word before a request's recipient (b751, b756): the frame the kinds of its object and recipient
pick, else the preposition every frame shares, else the first frame's, never nothing."""
import model_explain


class _Vocab:
    def __init__(self):
        self.kinds = {"design-decision": "thing", "shelf": "thing", "keeper": "thing", "agent": "thing", "thing": None}

    def ancestors(self, kind):
        out = []
        while kind is not None and kind not in out:
            out.append(kind)
            kind = self.kinds.get(kind)
        return out


def _explain(frames, kinds):
    ex = model_explain.Explain.__new__(model_explain.Explain)
    ex.vocab, ex.oblique = _Vocab(), {"lodge": frames}
    ex.kind = lambda L, part: kinds[part]
    return ex


def test_the_frame_the_kinds_pick():
    ex = _explain([("with", ("design-decision", "keeper")), ("on", ("design-decision", "shelf"))],
                  {"x": "design-decision", "y": "shelf"})
    assert ex.word("thing#r1", "lodge", ["x", "y"]) == "on"


def test_the_preposition_the_frames_share_when_no_frame_fits():
    ex = _explain([("on", ("design-decision", "agent")), ("on", ("keeper", "agent"))],
                  {"x": "design-decision", "y": None})     # an actor's kind, which no frame reads
    assert ex.word("thing#r1", "lodge", ["x", "y"]) == "on"


def test_the_first_frame_when_no_frame_fits_and_they_differ():
    ex = _explain([("with", ("keeper", "keeper")), ("on", ("shelf", "shelf"))],
                  {"x": "design-decision", "y": "design-decision"})
    assert ex.word("thing#r1", "lodge", ["x", "y"]) == "with"


def test_nothing_of_a_verb_of_no_frame():
    assert _explain([], {"x": "design-decision", "y": "shelf"}).word("thing#r1", "lodge", ["x", "y"]) == ""
