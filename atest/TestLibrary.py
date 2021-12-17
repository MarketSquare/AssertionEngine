from typing import Optional, Any

from robot.api.deco import keyword
from robotlibcore import DynamicCore

from assertionengine import verify_assertion, AssertionOperator, Formatter


class TestLibrary(DynamicCore):
    def __init__(self):
        self._keyword_formatters = {}
        DynamicCore.__init__(self, [Formatter(self)])

    @keyword
    def is_equal(
        self,
        value: str,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: str = None,
    ):
        formatter = self._keyword_formatters.get(self.is_equal)
        return verify_assertion(
            value, assertion_operator, assertion_expected, "Prefix message", message, formatter
        )

    @keyword
    def is_equal_as_number(
        self,
        integer: int,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
        message: str = None,
    ):
        print(f"integer: '{integer}' and type: {type(integer)}")
        formatter = self._keyword_formatters.get(self.is_equal_as_number)
        return verify_assertion(
            integer, assertion_operator, assertion_expected, "Prefix message", message, formatter
        )

    @keyword
    def Get_keyword_Formatters(self) -> dict:
        return self._keyword_formatters
