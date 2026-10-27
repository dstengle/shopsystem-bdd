"""features/requests.feature, bound to scripts/work and its library scripts/workqueue_request.py: every scenario."""
from pytest_bdd import scenarios

from .requests_flow_steps import *
from .requests_run_steps import *
from .requests_send_steps import *
from .requests_show_steps import *
from .requests_steps import *
from .requests_write_steps import *
from .work_queue_git_steps import *

scenarios("requests.feature")
