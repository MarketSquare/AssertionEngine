# Copyright 2021-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast

from robot.libraries.BuiltIn import BuiltIn  # type: ignore

from .data_types import AssertionOperator
from .type_converter import is_truthy, type_converter

__version__ = "0.0.2"

NumericalOperators = [
    AssertionOperator["=="],
    AssertionOperator["!="],
    AssertionOperator[">="],
    AssertionOperator[">"],
    AssertionOperator["<="],
    AssertionOperator["<"],
]

SequenceOperators = [
    AssertionOperator["*="],
    AssertionOperator["validate"],
    AssertionOperator["then"],
    AssertionOperator["=="],
    AssertionOperator["!="],
]

EvaluationOperators = [
    AssertionOperator["validate"],
    AssertionOperator["then"],
]

handlers: Dict[AssertionOperator, Tuple[Callable, str]] = {
    AssertionOperator["=="]: (lambda a, b: a == b, "should be"),
    AssertionOperator["!="]: (lambda a, b: a != b, "should not be"),
    AssertionOperator["<"]: (lambda a, b: a < b, "should be less than"),
    AssertionOperator[">"]: (lambda a, b: a > b, "should be greater than"),
    AssertionOperator["<="]: (lambda a, b: a <= b, "should be less than or equal"),
    AssertionOperator[">="]: (lambda a, b: a >= b, "should be greater than or equal"),
    AssertionOperator["*="]: (lambda a, b: b in a, "should contain"),
    AssertionOperator["not contains"]: (lambda a, b: b not in a, "should not contain"),
    AssertionOperator["matches"]: (lambda a, b: re.search(b, a), "should match"),
    AssertionOperator["^="]: (
        lambda a, b: re.search(f"^{re.escape(b)}", a),
        "should start with",
    ),
    AssertionOperator["$="]: (
        lambda a, b: re.search(f"{re.escape(b)}$", a),
        "should end with",
    ),
    AssertionOperator["validate"]: (
        lambda a, b: BuiltIn().evaluate(b, namespace={"value": a}),
        "should validate to true with",
    ),
}

T = TypeVar("T")


def verify_assertion(
    value: T,
    operator: Optional[AssertionOperator],
    expected: Any,
    message: str = "",
    custom_message: str = "",
) -> Any:
    if operator is None:
        return value
    if operator is AssertionOperator["then"]:
        return cast(T, BuiltIn().evaluate(expected, namespace={"value": value}))
    handler = handlers.get(operator)
    filler = " " if message else ""
    if handler is None:
        raise RuntimeError(
            f"{message}{filler}`{operator}` is not a valid assertion operator"
        )
    validator, text = handler
    if not validator(value, expected):
        if not custom_message:
            error_msg = (
                f"{message}{filler}'{value}' ({type_converter(value)}) "
                f"{text} '{expected}' ({type_converter(expected)})"
            )
        else:
            error_msg = custom_message.format(
                value=value,
                value_type=type_converter(value),
                expected=expected,
                expected_type=type_converter(expected),
            )
        raise AssertionError(error_msg)
    return value


def float_str_verify_assertion(
    value: T,
    operator: Optional[AssertionOperator],
    expected: Any,
    message="",
    custom_message="",
):
    if operator is None:
        return value
    elif operator in NumericalOperators:
        expected = float(expected)
    elif operator in [
        AssertionOperator["validate"],
        AssertionOperator["then"],
    ]:
        expected = str(expected)
    else:
        raise ValueError(f"Operator '{operator.name}' is not allowed.")
    return verify_assertion(value, operator, expected, message, custom_message)


def bool_verify_assertion(
    value: T,
    operator: Optional[AssertionOperator],
    expected: Any,
    message="",
    custom_message="",
):
    if operator and operator not in [
        AssertionOperator["=="],
        AssertionOperator["!="],
    ]:
        raise ValueError(f"Operators '==' and '!=' are allowed, not '{operator.name}'.")

    expected_bool = is_truthy(expected)
    return verify_assertion(value, operator, expected_bool, message, custom_message)


def map_list(selected: List):
    if not selected or len(selected) == 0:
        return None
    elif len(selected) == 1:
        return selected[0]
    else:
        return selected


def list_verify_assertion(
    value: List,
    operator: Optional[AssertionOperator],
    expected: List,
    message="",
    custom_message="",
):
    if operator:
        if operator not in SequenceOperators:
            raise AttributeError(
                f"Operator '{operator.name}' is not allowed in this Keyword."
                f"Allowed operators are: '{SequenceOperators}'"
            )
        if operator in [
            AssertionOperator["=="],
            AssertionOperator["!="],
        ]:
            expected.sort()
            value.sort()
    return verify_assertion(
        map_list(value), operator, map_list(expected), message, custom_message
    )


def dict_verify_assertion(
    value: Dict,
    operator: Optional[AssertionOperator],
    expected: Optional[Dict],
    message="",
    custom_message="",
):
    if operator and operator not in SequenceOperators:
        raise AttributeError(
            f"Operator '{operator.name}' is not allowed in this Keyword."
            f"Allowed operators are: {SequenceOperators}"
        )
    else:
        return verify_assertion(value, operator, expected, message, custom_message)


def int_dict_verify_assertion(
    value: Dict[str, int],
    operator: Optional[AssertionOperator],
    expected: Optional[Dict[str, int]],
    message="",
    custom_message="",
):
    if not operator:
        return value
    elif operator in SequenceOperators:
        if operator not in EvaluationOperators and isinstance(expected, str):
            evaluated_expected = ast.literal_eval(expected)
        else:
            evaluated_expected = expected
        return verify_assertion(
            value, operator, evaluated_expected, message, custom_message
        )
    elif expected and operator in NumericalOperators:
        for k, v in value.items():
            exp = expected[k]
            verify_assertion(v, operator, exp, message, custom_message)
        return value
    else:
        raise AttributeError(
            f"Operator '{operator.name}' is not allowed in this Keyword."
            f"Allowed operators are: {NumericalOperators} and {SequenceOperators}"
        )
