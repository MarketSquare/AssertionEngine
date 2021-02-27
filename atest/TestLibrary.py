from typing import Optional, Any

from AssertionEngine import verify_assertion, AssertionOperator


class TestLibrary:

    def is_equal(self, value: str, assertion_operator: Optional[AssertionOperator] = None, assertion_expected: Any = None, message: str = None):
        return verify_assertion(
            value, assertion_operator, assertion_expected, "URL", message
        )
