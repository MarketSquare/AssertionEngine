from typing import Optional, Any

from assertionengine import verify_assertion, AssertionOperator


class TestLibrary:
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

    def is_equa_as_number(
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
