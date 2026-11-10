"""The codified-2 world's handlers of conformance to a named artifact (b240 phase 4): "the file f1 conforms to the
stage form" and "the file f1 does not conform to the stage form", the Givens features_generate4 writes of "X conforms
to A". Each records under the scenario's `conforms`, (the thing, the artifact) -> whether it conforms; a world that
builds the thing reads it there and writes it to meet the artifact or not."""
from vocab import handler


@handler("GivenDoes", "conform")
def conforms(step):
    step.context.setdefault("conforms", {})[(step.subject, step.nps[0])] = True


@handler("GivenDoesNot", "conform")
def does_not_conform(step):
    step.context.setdefault("conforms", {})[(step.subject, step.nps[0])] = False
