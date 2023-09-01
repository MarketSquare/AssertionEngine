import logging
from typing import Optional, Any, Callable

from robot.api.deco import keyword
from robotlibcore import DynamicCore

from assertionengine import verify_assertion, AssertionOperator, Formatter

LOG = logging.getLogger(__name__)


class LibFormatter(Formatter):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.keyword_formatters = {}

    def set_formatter(self, keyword: Callable, *formatter: str):
        formatter = self.formatters_to_method(list(formatter))
        self.keyword_formatters[keyword] = list(formatter)

    def get_formatter(self, keyword: Callable):
        LOG.info(self.keyword_formatters.get(keyword))
        return self.keyword_formatters.get(keyword)


class TestLibrary(DynamicCore):
    lib_formatter = LibFormatter()
    ROBOT_LIBRARY_LISTENER = lib_formatter
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        DynamicCore.__init__(self, [])

    @keyword
    def is_equal(
        self,
        value: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: str = None,
    ):
        formatter = self.lib_formatter.get_formatter(self.is_equal)
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
        formatter = self.lib_formatter.get_formatter(self.is_equal_as_number)
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
        LOG.info(self.lib_formatter)
        return self.lib_formatter.keyword_formatters

    @keyword
    def set_assertion_formatter(self, keyword: str, *formatters: str):
        kw_method = self.keywords.get(self.lib_formatter.normalize_keyword(keyword))
        self.lib_formatter.set_formatter(kw_method, *formatters)
