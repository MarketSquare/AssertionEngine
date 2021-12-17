from unittest.mock import MagicMock

import pytest

from assertionengine import Formatter


@pytest.fixture(scope="module")
def formatter():
    ctx = MagicMock()
    ctx.keywords = {"My_Keyword": True}
    return Formatter(ctx)


def test_normalise_keyword_name(formatter: Formatter):
    assert formatter._library_keyword("My Keyword")
    assert formatter._library_keyword("My_KeyworD")
    assert not formatter._library_keyword("Not Keyword")
