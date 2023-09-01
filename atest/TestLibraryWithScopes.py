import logging
from enum import Enum, auto
from typing import Optional, Any, Callable

from robot.api.deco import keyword
from robotlibcore import DynamicCore

from assertionengine import verify_assertion, AssertionOperator, Formatter

LOG = logging.getLogger(__name__)


class Scope(Enum):
    Global = auto()
    Suite = auto()
    Test = auto()


class LibFormatter(Formatter):
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.keyword_formatters = {
            Scope.Global: {},
            Scope.Suite: {},
            Scope.Test: {},
        }

    def set_formatter(self, kw_str: str, scope: Scope, *formatter: str):
        formatter = self.formatters_to_method(list(formatter))
        self.keyword_formatters[scope][kw_str] = list(formatter)

    def get_formatter(self, kw_str: str):
        LOG.info(self.keyword_formatters)
        LOG.info(kw_str)
        if kw_str in self.keyword_formatters[Scope.Test]:
            return self.keyword_formatters[Scope.Test].get(kw_str)
        if kw_str in self.keyword_formatters[Scope.Suite]:
            return self.keyword_formatters[Scope.Suite].get(kw_str)
        return self.keyword_formatters[Scope.Global].get(kw_str)

    def end_test(self, name, attributes):
        self.keyword_formatters[Scope.Test] = {}

    def end_suite(self, name, attributes):
        self.keyword_formatters[Scope.Suite] = {}


class TestLibraryWithScopes(DynamicCore):
    lib_formatter = LibFormatter()
    ROBOT_LIBRARY_LISTENER = lib_formatter
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        DynamicCore.__init__(self, [])

    @keyword
    def is_equal_Scope(
        self,
        value: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: str = None,
    ):
        formatter = self.lib_formatter.get_formatter(
            self.lib_formatter.normalize_keyword(self.is_equal_Scope.__name__)
        )
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
    def get_keyword_formatters_scope(self) -> dict:
        LOG.info(self.lib_formatter.keyword_formatters)
        data = self.lib_formatter.keyword_formatters
        new_data = {}
        for key, value in data.items():
            new_data[str(key)] = value
        return new_data

    @keyword
    def set_assertion_formatter_scope(
        self, keyword: str, scope: Scope, *formatters: str
    ):
        kw_str = self.lib_formatter.normalize_keyword(keyword)
        self.lib_formatter.set_formatter(kw_str, scope, *formatters)
