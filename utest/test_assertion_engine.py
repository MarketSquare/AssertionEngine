import sys

import pytest
from approvaltests import verify_all  # type: ignore

from assertionengine import (
    verify_assertion,
    AssertionOperator,
)
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS  # type: ignore


@pytest.mark.skipif(sys.platform == "win32", reason="Works only in Linux")
def test_custom_error():
    results = [
        _validate_operator(
            AssertionOperator["=="],
            "actual",
            "unexpected",
            "partial error",
            "custom message",
        ),
        _validate_operator(
            AssertionOperator["=="],
            "ääööÅÅ",
            "åß∂ƒ©˙∆˚¬…æ",
            "partial error",
            "{value} {value_type} custom message {expected} {expected_type}",
        ),
        _validate_operator(
            AssertionOperator["=="],
            "ääööÅÅ",
            "åß∂ƒ©˙∆˚¬…æ",
            "partial error",
            "{value} custom message {expected}",
        ),
    ]
    verify_all("Test custom error", results)


def test_equals():
    results = [
        _validate_operator(AssertionOperator["=="], "actual", "actual"),
        _validate_operator(
            AssertionOperator["=="], "actual", "unexpected", "partial error"
        ),
        _validate_operator(AssertionOperator["=="], 1, "1"),
        _validate_operator(
            AssertionOperator["equal;normalize spaces"],
            "normalize\x20\x20spaces\x20\x20test",
            "normalize\xa0\xa0spaces\x20\x20test",
        ),
    ]
    verify_all("Test equals", results)


def test_not_equals():
    results = [
        _validate_operator(AssertionOperator["!="], "actual", "expected"),
        _validate_operator(
            AssertionOperator["!="], "actual", "actual", "partial error message"
        ),
    ]
    verify_all("Not equal", results)


def test_contains():
    results = [
        _validate_operator(AssertionOperator["contains"], "actual", "ctua"),
        _validate_operator(AssertionOperator["contains"], "actual", "nope", "custom"),
        _validate_operator(AssertionOperator["*="], "actual", "tual"),
        _validate_operator(AssertionOperator["*="], "actual", "nope"),
    ]
    verify_all("Contains", results)


def test_not_contains():
    results = [
        _validate_operator(AssertionOperator["not contains"], "actual", "xxx"),
        _validate_operator(AssertionOperator["not contains"], "actual", "t", "custom"),
    ]
    verify_all("Not contains", results)


def test_greater():
    results = [
        _validate_operator(AssertionOperator["<"], 1, 2),
        _validate_operator(AssertionOperator["<"], 1, 0, "custom"),
    ]
    verify_all("Greater", results)


def test_less():
    results = [
        _validate_operator(AssertionOperator[">"], 2, 1),
        _validate_operator(AssertionOperator[">"], 2, 3, "custom"),
    ]
    verify_all("Less", results)


def test_greater_or_equal():
    results = [
        _validate_operator(AssertionOperator["<="], 1, 2),
        _validate_operator(AssertionOperator["<="], 1, 0),
        _validate_operator(AssertionOperator["<="], 1, 1),
    ]
    verify_all("greater or equal", results)


def test_less_or_equal():
    results = [
        _validate_operator(AssertionOperator[">="], 2, 2),
        _validate_operator(AssertionOperator[">="], 2, 3),
        _validate_operator(AssertionOperator[">="], 2, 1),
    ]
    verify_all("less or equal", results)


def test_match():
    results = [
        _validate_operator(AssertionOperator["matches"], "Actual", "(?i)actual"),
        _validate_operator(AssertionOperator["matches"], "Actual", "/(\\d)+/"),
        _validate_operator(AssertionOperator["matches"], "Actual", "^Act"),
        _validate_operator(AssertionOperator["matches"], "Actual", "/(\\d)+/"),
        _validate_operator(AssertionOperator["matches"], "Actual", "ual$"),
        _validate_operator(
            AssertionOperator["matches"], "Actual\nmultiline", "(?m)Actual\nmultiline$"
        ),
        _validate_operator(
            AssertionOperator["matches"], "Actual\nmultiline", "/(\\d)+/"
        ),
    ]
    verify_all("match", results)


@pytest.fixture()
def with_suite():
    def ns():
        pass

    ns.variables = lambda: 0
    ns.variables.current = lambda: 0
    ns.variables.current.store = lambda: 0
    EXECUTION_CONTEXTS.start_suite("suite", ns, lambda: 0)
    yield
    EXECUTION_CONTEXTS.end_suite()


def test_validate(with_suite):
    results = [
        _validate_operator(AssertionOperator("validate"), 1, "0 < value < 2"),
        _validate_operator(AssertionOperator("validate"), 1, "value == 'hello'"),
    ]
    verify_all("validate", results)


def test_then(with_suite):
    then_op = AssertionOperator["then"]
    results = [
        verify_assertion(8, then_op, "value + 3") == 11,
        verify_assertion(2, then_op, "value + 3") == 5,
        verify_assertion("René", then_op, "'Hello ' + value + '!'") == "Hello René!",
    ]
    verify_all("then", results)


def test_start_with():
    results = [
        _validate_operator(AssertionOperator["^="], "Hello Robots", "Hello"),
        _validate_operator(AssertionOperator["^="], "Hello Robots", "Robots"),
        _validate_operator(
            AssertionOperator["should start with"], "Hello Robots", "Hello"
        ),
        _validate_operator(
            AssertionOperator["should start with"], "Hello Robots", "Robots"
        ),
        _validate_operator(
            AssertionOperator["^="], "Hel[4,5]?[1-9]+ Robots", "Hel[4,5]?[1-"
        ),
        _validate_operator(AssertionOperator["^="], "Hel[4,5]?[1-9]+ Robots", ".*"),
    ]
    verify_all("start with", results)


def test_ends_with():
    results = [
        _validate_operator(AssertionOperator["$="], "Hello Robots", "Robots"),
        _validate_operator(AssertionOperator["$="], "Hello Robots", "Hello"),
        _validate_operator(
            AssertionOperator["$="], "Hel[4,5]?[1-9]+ Robots", "[1-9]+ Robots"
        ),
        _validate_operator(AssertionOperator["$="], "Hel[4,5]?[1-9]+ Robots", ".*"),
    ]
    verify_all("ends with", results)


def test_invalid_operator():
    results = [
        _validate_operator("foo", "actual", "unexpected", "bar"),
        _validate_operator("foo", "actual", "unexpected"),
    ]
    verify_all("Custom error", results)


def _validate_operator(
    operator: AssertionOperator, actual, expected, message="", custom_message=""
):
    try:
        return verify_assertion(actual, operator, expected, message, custom_message)
    except Exception as error:
        return error


def _method_validator(method, arg=None):
    try:
        if arg is None:
            return method()
        return method(arg)
    except Exception as error:
        return error
