import os
import shutil
import sys
from pathlib import Path

try:
    import pytest
except ModuleNotFoundError:
    print("Assuming that this in setup phase and ignoring ModuleNotFoundError")
from invoke import task, Exit


ROOT_DIR = Path(".").parent.resolve()
SRC_DIR = ROOT_DIR / "AssertionEngine"

ROOT_DIR = Path(os.path.dirname(__file__))
ATEST = ROOT_DIR / "atest"
ATEST_OUTPUT = ATEST / "output"
ZIP_DIR = ROOT_DIR / "zip_results"


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
def lint_robot(ctx):
    """Lint robot tests with tidy"""
    result = ctx.run("python -m robot.tidy --recursive atest/")
    raise Exit(result.exited)


@task(lint_robot)
def lint(ctx):
    ctx.run("mypy --config-file ./mypy.ini AssertionEngine/ utest/")
    ctx.run("black --config ./pyproject.toml AssertionEngine/")
    ctx.run("isort AssertionEngine/")
    ctx.run("flake8 --config ./.flake8 AssertionEngine/ utest/")


@task
def clean_atest(ctc):
    """Cleans atest folder outputs."""
    if ATEST_OUTPUT.exists():
        shutil.rmtree(ATEST_OUTPUT)
    if ZIP_DIR.exists():
        shutil.rmtree(ZIP_DIR)


@task(clean_atest)
def atest(ctx):
    """Runs Robot Framework acceptance tests."""
    args = [
        "robot",
        "--pythonpath",
        ".",
        "--outputdir",
        str(ATEST_OUTPUT),
        str(ATEST)
    ]
    ctx.run(" ".join(args))
