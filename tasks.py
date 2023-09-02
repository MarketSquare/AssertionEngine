import os
import platform
import re
import shutil
import sys
import zipfile
from pathlib import Path, PurePath

try:
    import robotstatuschecker
    from robot import rebot_cli
    from robot import __version__ as robot_version
    import pytest
except ModuleNotFoundError:
    print("Assuming that this in setup phase and ignoring ModuleNotFoundError")
from invoke import task, Exit


ROOT_DIR = Path(".").parent.resolve()
SRC_DIR = ROOT_DIR / "assertionengine"

ROOT_DIR = Path(os.path.dirname(__file__))
ATEST = ROOT_DIR / "atest"
ATEST_OUTPUT = ATEST / "output"
ZIP_DIR = ROOT_DIR / "zip_results"
DIST = ROOT_DIR / "dist"
ASSERTION_ENGINE = ROOT_DIR / "assertionengine" / "assertion_engine.py"


@task
def deps(ctx):
    """Install dependencies to develop and test project.

    Make sure that Python3 and poetry are installed for you operating system.
    - https://www.python.org/downloads/
    - https://python-poetry.org/docs/#installation
    """
    ctx.run("poetry install")
    ctx.run("pre-commit install -f -t pre-commit")
    ctx.run("pre-commit install -f -t pre-push")
    ctx.run("pre-commit install -f -t pre-merge-commit")


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
    args = [
        "--showlocals",
        "--log-format=%(asctime)s %(levelname)s %(message)s",
        "--log-date-format=%Y-%m-%d %H:%M:%S",
        "--log-level=INFO",
    ]
    if reporter:
        args.append(f"--approvaltests-add-reporter={reporter}")
    if suite:
        args.append(suite)
    status = pytest.main(args)
    raise Exit(status)


@task
def lint_robot(ctx):
    """Lint robot tests with tidy"""
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    atest_folder = Path(__file__).parent.joinpath("atest/")
    command = [
        "robotidy",
        "--lineseparator",
        "unix",
        "--configure",
        "NormalizeAssignments:equal_sign_type=space_and_equal_sign",
        "--configure",
        "NormalizeAssignments:equal_sign_type_variables=space_and_equal_sign",
        str(atest_folder),
    ]
    if in_ci:
        command.insert(1, "--check")
        command.insert(1, "--diff")
    ctx.run(" ".join(command))


@task(lint_robot)
def lint(ctx, error=False):
    """Lint Robot Framework test data and Python code."""
    black_command = (
        "black --config ./pyproject.toml assertionengine/ tasks.py atest/ utest/"
    )
    ruff_command = "ruff assertionengine"

    if error:
        black_command = f"{black_command} --check"
    else:
        ruff_command = f"{ruff_command} --fix"
    print("Run mypy")
    ctx.run("mypy --config-file ./pyproject.toml assertionengine/ utest/")
    print("Run Black")
    ctx.run(black_command)
    print("Run Ruff")
    ctx.run(ruff_command)


@task
def clean_atest(ctx):
    """Cleans atest folder outputs."""
    if ATEST_OUTPUT.exists():
        shutil.rmtree(ATEST_OUTPUT)
    if ZIP_DIR.exists():
        shutil.rmtree(ZIP_DIR)


@task(clean_atest)
def clean(ctx):
    """Cleans temporary files.

    Test results, package files and so on.."""
    if DIST.exists():
        shutil.rmtree(DIST)


@task(clean_atest)
def atest(ctx, zip=None):
    """Runs Robot Framework acceptance tests."""
    args = [
        "robot",
        "--exitonerror",
        "--nostatusrc",
        "--pythonpath",
        ".",
        "--loglevel",
        "TRACE",
        "--report",
        "NONE",
        "--log",
        "NONE",
        "--outputdir",
        str(ATEST_OUTPUT),
        str(ATEST),
    ]
    ctx.run(" ".join(args))
    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Check: {output_xml}")
    robotstatuschecker.process_output(output_xml, verbose=False)
    print("Generate report and log files.")
    rebot_exit = False if zip else True
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=False)
    if zip:
        print(f"Zip file created to: {_create_zip()}")
    print("DONE")
    raise Exit(rc)


def _create_zip():
    zip_dir = ZIP_DIR / "output"
    zip_dir.mkdir(parents=True)
    python_version = platform.python_version()
    zip_name = f"{sys.platform}-rf-{robot_version}-python-{python_version}.zip"
    zip_path = zip_dir / zip_name
    print(f"Creating zip  in: {zip_path}")
    zip_file = zipfile.ZipFile(zip_path, "w")
    for file in ATEST_OUTPUT.glob("**/*.*"):
        file = PurePath(file)
        arc_name = file.relative_to(str(ATEST_OUTPUT))
        zip_file.write(file, arc_name)
    zip_file.close()
    return zip_path


@task
def version(ctx, version):
    text = re.sub(
        r"__version__ = \"\d+\.\d+\.\d+\"",
        f'__version__ = "{version}"',
        ASSERTION_ENGINE.read_text(),
    )
    ASSERTION_ENGINE.write_text(text, encoding="utf-8")
    pyproject_toml = Path("pyproject.toml")
    text = re.sub(
        r"version = \"\d+\.\d+\.\d+\"",
        f'version = "{version}"',
        pyproject_toml.read_text(),
    )
    pyproject_toml.write_text(text, encoding="utf-8")
