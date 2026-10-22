import os


def test_env_and_work_item():
    print("PYTEST_ADDOPTS=%r" % os.environ.get("PYTEST_ADDOPTS"))
    print("cwd=%s" % os.getcwd())
    print("argv=%r" % (os.sys.argv,))
