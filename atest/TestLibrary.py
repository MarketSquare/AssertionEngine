from typing import Optional, Any

from robot.api.deco import keyword
from robotlibcore import DynamicCore

from assertionengine import verify_assertion, AssertionOperator


class TestLibrary(DynamicCore):
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
        return verify_assertion(
            value, assertion_operator, assertion_expected, "Prefix message", message
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
        return verify_assertion(
            integer, assertion_operator, assertion_expected, "Prefix message", message
        )
