import os
import platform
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
        str(ATEST)
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
