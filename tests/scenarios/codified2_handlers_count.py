"""The codified-2 world's handler of the number of Ks compared with a parameter (b240 phase 7): "the number of lines
of the stage s1 is more than `limit`", the Given features_generate4 writes of "the number of Ks that P is more than
`limit`". It records under the scenario's `counts`, the number's noun phrase -> the comparison ("more than
`limit`"); a world that builds the things reads it there and gives the parameter a value that meets it."""
from vocab import handler


@handler("GivenCount")
def count(step):
    step.context.setdefault("counts", {})[step.subject] = step.nps[0]
