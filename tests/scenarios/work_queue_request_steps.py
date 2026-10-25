"""features/work-queue.feature's steps of `work request` (r7): the upstream that keeps no request, bound for this feature
with requests_write_steps' own function, and the lines file that is not there."""
from pytest_bdd import given

from .requests_write_steps import upstream_keeps_none


@given("an upstream that keeps no request")
def upstream_without_a_request(repo):
    upstream_keeps_none(repo)


@given("no file lines.md")
def no_lines_file(repo):
    assert not (repo / "lines.md").exists()
