from pathlib import Path

import pytest
from invoke import task, Exit


ROOT_DIR = Path(".").parent.resolve()
SRC_DIR = ROOT_DIR / "AssertionEngine"

@task
def deps(ctx):
    """Install dependencies to develop and test project.

    Make sure that Python3 and poetry are installed for you operating system.
    - https://www.python.org/downloads/
    - https://python-poetry.org/docs/#installation
    """
    ctx.run("poetry install")

@task
def utest(ctx, reporter=None, suite=None):
    """Run utest.

    Args:
        reporter: Defines which approval test reporter to use.
                  Must be full path to the diff program.
                  For more details see:
                  https://pypi.org/project/pytest-approvaltests/
                  https://github.com/approvals/ApprovalTests.Python
        suite:    Defines which test suite file to run. Same as: pytest path/to/test.py
                  Must be path to the test suite file
    """
    args = ["--showlocals"]
    if reporter:
        args.append(f"--approvaltests-add-reporter={reporter}")
    if suite:
        args.append(suite)
    status = pytest.main(args)
    raise Exit(status)


@task
def lint(ctx):
    ctx.run("mypy --config-file ./mypy.ini AssertionEngine/ utest/")
    ctx.run("black --config ./pyproject.toml AssertionEngine/")
    ctx.run("isort AssertionEngine/")
    ctx.run("flake8 --config ./.flake8 AssertionEngine/ utest/")
