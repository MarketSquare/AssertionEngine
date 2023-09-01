from unittest.mock import MagicMock

import pytest

from assertionengine import Formatter
from assertionengine.formatter import FormatRules


class MyFormatter(Formatter):
    def __int__(self):
        self.formatters = {}

    def set_formatter(self, keyword, formatter):
        self.formatters[keyword] = formatter

    def get_formatter(self, keyword):
        return self.formatters.get(keyword)


@pytest.fixture(scope="module")
def formatter():
    return MyFormatter()


def test_normalise_keyword_name(formatter: MyFormatter):
    assert formatter.normalize_keyword("My Keyword") == "my_keyword"
    assert formatter.normalize_keyword("My_KeyworD") == "my_keyword"
    assert formatter.normalize_keyword("KeyWorD") == "keyword"


def test_get_formatter(formatter: MyFormatter):
    assert formatter.formatters_to_method(["strip"]) == [FormatRules["strip"]]
    assert formatter.formatters_to_method(
        ["normalize spaces", "strip", "apply to expected", "case insensitive"]
    ) == [
        FormatRules["normalize spaces"],
        FormatRules["strip"],
        FormatRules["apply to expected"],
        FormatRules["case insensitive"],
    ]
    assert formatter.formatters_to_method(["sTriP"]) == [FormatRules["strip"]]


def test_get_invalid_formatter(formatter: MyFormatter):
    with pytest.raises(KeyError):
        formatter.formatters_to_method(["Foobar"])
