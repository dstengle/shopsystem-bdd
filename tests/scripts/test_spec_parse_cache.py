"""spec_parse_cache: GF's parse of a line kept on disk, shared by processes, keyed by the grammar's sources, the
grammar, the lexicon's words and the text (a hit, a miss and a second process: test_spec_grammar4_cache.py)."""
import spec_parse_cache


def test_the_key_names_everything_the_parse_reads():
    key = spec_parse_cache.key
    base = key("sha", "Req", "a b", {"x"})
    assert len({base, key("sha2", "Req", "a b", {"x"}), key("sha", "Steps", "a b", {"x"}),
                key("sha", "Req", "a c", {"x"}), key("sha", "Req", "a b", {"y"})}) == 5
    assert key("sha", "Req", "a b", {"x", "y"}) == key("sha", "Req", "a b", ["y", "x"])
