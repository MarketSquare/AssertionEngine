import logging
from typing import Optional, Any, List, Callable

from robot.api.deco import keyword
from robotlibcore import DynamicCore

from assertionengine import verify_assertion, AssertionOperator, Formatter

LOG = logging.getLogger(__name__)


class TestLibrary(DynamicCore):
    def __init__(self):
        self._keyword_formatters = {}
        DynamicCore.__init__(self, [])
        self.formatter = LibFormatter(self)

    @keyword
    def is_equal(
        self,
        value: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: str = None,
    ):
        formatter = self.formatter.get_formatter(self.is_equal)
        LOG.info(formatter)
        return verify_assertion(
            value,
            assertion_operator,
            assertion_expected,
            "Prefix message",
            message,
            formatter,
        )

    @keyword
    def is_equal_as_number(
        self,
        integer: int,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: str = None,
    ):
        LOG.info(f"integer: '{integer}' and type: {type(integer)}")
        formatter = self.formatter.get_formatter(self.is_equal_as_number)
        return verify_assertion(
            integer,
            assertion_operator,
            assertion_expected,
            "Prefix message",
            message,
            formatter,
        )

    @keyword
    def get_keyword_formatters(self) -> dict:
        return self._keyword_formatters

    @keyword
    def set_assertion_formatter(self, keyword: str, *formatters: str):
        kw_method = self.keywords.get(self.formatter.normalize_keyword(keyword))
        self.formatter.set_formatter(kw_method, *formatters)


class LibFormatter(Formatter):
    def __init__(self, library: TestLibrary):
        self.library = library

    def set_formatter(self, keyword: Callable, *formatter: str):
        formatter = self.formatters_to_method(list(formatter))
        self.library._keyword_formatters[keyword] = list(formatter)

    def get_formatter(self, keyword: Callable):
        LOG.info(self.library._keyword_formatters.get(keyword))
        return self.library._keyword_formatters.get(keyword)
