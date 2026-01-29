Instructions for creating release
=================================

Release is done with poetry and invoke::

   set VERSION 0.3.0
   uv run inv version $VERSION
   git add assertionengine/assertion_engine.py pyproject.toml
   git commit -m "Set version $VERSION"
   git tag -a v$VERSION -m "Release $VERSION"
   git push --tags
   uv build
   uv publish

Then check that Pypi looks good: https://pypi.org/project/robotframework-assertion-engine/

Document release
----------------

Create release notes in GitHub project: https://github.com/MarketSquare/AssertionEngine/releases
