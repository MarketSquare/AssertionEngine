import re
from pathlib import Path

import setuptools

LONG_DESCRIPTION = Path("README.rst").read_text(encoding="utf-8")
CUR_DIR = Path(".")
ASSERTION_ENGINE = CUR_DIR / "AssertionEngine" / "assertion_engine.py"
VERSION = re.search(
    r"(^__version__ = \")(\d+\.\d+\.\d+)(.*\"$)", ASSERTION_ENGINE.read_text()
).group(2)

setuptools.setup(
    name="robotframework-assertion-engine",
    version=VERSION,
    author="Tatu Aalto",
    author_email="aalto.tatu@gmail.com",
    description="Generic way to create meaningful and easy to use assertions for the Robot Framework libraries.",
    keywords="robotframework testing testautomation tool",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/MarketSquare/AssertionEngine",
    project_urls={
        "Bug Tracker": "https://github.com/MarketSquare/AssertionEngine/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha" "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Framework :: Robot Framework",
        "Framework :: Robot Framework :: Tool",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
