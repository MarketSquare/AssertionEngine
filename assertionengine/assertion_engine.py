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
from enum import Enum, Flag, IntFlag
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union, cast

from robot.libraries.BuiltIn import BuiltIn  # type: ignore

from .type_converter import is_truthy, type_converter

__version__ = "3.0.3"

AssertionOperator = Enum(
    "AssertionOperator",
    {
        "equal": "==",
        "equals": "==",
        "==": "==",
        "should be": "==",
        "inequal": "!=",
        "!=": "!=",
        "should not be": "!=",
        "less than": "<",
        "<": "<",
        "greater than": ">",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "contains": "*=",
        "not contains": "not contains",
        "*=": "*=",
        "starts": "^=",
        "^=": "^=",
        "should start with": "^=",
        "ends": "$=",
        "should end with": "$=",
        "$=": "$=",
        "matches": "$",
        "validate": "validate",
        "then": "then",
        "evaluate": "then",
    },
)
AssertionOperator.__doc__ = """
    Currently supported assertion operators are:

    |      = Operator =   |   = Alternative Operators =          |              = Description =                                                       | = Validate Equivalent =              |
    | ``==``              | ``equal``, ``equals``, ``should be`` | Checks if returned value is equal to expected value.                               | ``value == expected``                |
    | ``!=``              | ``inequal``, ``should not be``       | Checks if returned value is not equal to expected value.                           | ``value != expected``                |
    | ``>``               | ``greater than``                     | Checks if returned value is greater than expected value.                           | ``value > expected``                 |
    | ``>=``              |                                      | Checks if returned value is greater than or equal to expected value.               | ``value >= expected``                |
    | ``<``               | ``less than``                        | Checks if returned value is less than expected value.                              | ``value < expected``                 |
    | ``<=``              |                                      | Checks if returned value is less than or equal to expected value.                  | ``value <= expected``                |
    | ``*=``              | ``contains``                         | Checks if returned value contains expected value as substring.                     | ``expected in value``                |
    |                     | ``not contains``                     | Checks if returned value does not contain expected value as substring.             | ``expected in value``                |
    | ``^=``              | ``should start with``, ``starts``    | Checks if returned value starts with expected value.                               | ``re.search(f"^{expected}", value)`` |
    | ``$=``              | ``should end with``, ``ends``        | Checks if returned value ends with expected value.                                 | ``re.search(f"{expected}$", value)`` |
    | ``matches``         |                                      | Checks if given RegEx matches minimum once in returned value.                      | ``re.search(expected, value)``       |
    | ``validate``        |                                      | Checks if given Python expression evaluates to ``True``.                           |                                      |
    | ``evaluate``        |  ``then``                            | When using this operator, the keyword does return the evaluated Python expression. |                                      |

    Currently supported formatters for assertions are:
    |     = Formatter =     |                      = Description =                       |
    |  ``normalize spaces`` | Substitutes multiple spaces to single space from the value |
    |       ``strip``       | Removes spaces from the beginning and end of the value     |
    | ``case insensitive``  | Converts value to lower case before comparing              |
    | ``apply to expected`` | Applies rules also for the expected value                  |

    Formatters are applied to the value before assertion is performed and keywords returns a value where rule is
    applied. Formatter is only applied to the value which keyword returns and not all rules are valid for all assertion
    operators. If ``apply to expected`` formatter is defined, then formatters are then formatter are also applied to
    expected value.
    """

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


set_handlers: Dict[AssertionOperator, Tuple[Callable, str]] = {
    AssertionOperator["=="]: (lambda a, b: a == b, "should be"),
    AssertionOperator["!="]: (lambda a, b: a != b, "should not be"),
    AssertionOperator["*="]: (lambda a, b: b.issubset(a), "should contain"),
    AssertionOperator["not contains"]: (
        lambda a, b: not b.issubset(a),
        "should not contain",
    ),
}

T = TypeVar("T")


def apply_formatters(value: T, formatters: Optional[List[Any]]) -> Any:
    if not formatters:
        return value
    for formatter in formatters:
        value = formatter(value)
    return value


def apply_to_expected(expected: Any, formatters: Optional[List[Any]]) -> Any:
    if not formatters:
        return expected
    for formatter in formatters:
        if formatter.__name__ == "_apply_to_expected":
            return apply_formatters(expected, formatters)
    return expected


def verify_assertion(
    value: T,
    operator: Optional[AssertionOperator],
    expected: Any,
    message: str = "",
    custom_message: Optional[str] = None,
    formatters: Optional[list] = None,
) -> Any:
    if operator is None and expected:
        raise ValueError(
            "Invalid validation parameters. Assertion operator is mandatory when specifying expected value."
        )
    if operator is None:
        return value
    expected = apply_to_expected(expected, formatters)
    value = apply_formatters(value, formatters)
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
        raise_error(custom_message, expected, filler, message, text, value)
    return value


def flag_verify_assertion(
    value: Union[IntFlag, Flag],
    operator: Optional[AssertionOperator],
    expected: Any,
    message: str = "",
    custom_message: Optional[str] = None,
) -> Any:
    if not isinstance(value, Flag):
        raise TypeError(f"Verified value was not of type Flag. It was {type(value)}")
    if (operator is None and expected) or (operator and not expected):
        raise ValueError(
            "Invalid validation parameters. Assertion operator and expected value can only be used together."
        )
    if operator is None:
        return value
    if operator is AssertionOperator["then"]:
        return eval_flag(expected[0], value)
    filler = " " if message else ""
    if operator is AssertionOperator["validate"]:
        if not eval_flag(expected[0], value):
            raise_error(
                custom_message,
                expected[0],
                filler,
                message,
                "should validate to true with",
                value,
            )
    else:
        value_set = {flag.name for flag in type(value) if flag in value}
        expected_set = set(expected)
        handler = set_handlers.get(operator)
        if handler is None:
            raise RuntimeError(
                f"{message}{filler}`{operator}` is not a valid assertion operator"
            )
        validator, text = handler
        if not validator(value_set, expected_set):
            raise_error(
                custom_message,
                sorted(expected_set),
                filler,
                message,
                text,
                sorted(value_set),
            )
    return value


def eval_flag(expected, value) -> Any:
    return BuiltIn().evaluate(
        expected, namespace={"value": value, **value._member_map_}
    )


def raise_error(custom_message, expected, filler, message, text, value):
    type_value, type_expected = type_converter(value), type_converter(expected)
    value_quotes, expected_quotes = "'", "'"
    if isinstance(value, str):
        value = repr(value)
        value_quotes = ""
    if isinstance(expected, str):
        expected = repr(expected)
        expected_quotes = ""
    if not custom_message:
        error_msg = (
            f"{message}{filler}{value_quotes}{value}{value_quotes} ({type_value}) "
            f"{text} {expected_quotes}{expected}{expected_quotes} ({type_expected})"
        )
    else:
        error_msg = custom_message.format(
            value=value,
            value_type=type_value,
            expected=expected,
            expected_type=type_expected,
        )
    raise AssertionError(error_msg)


def float_str_verify_assertion(
    value: T,
    operator: Optional[AssertionOperator],
    expected: Any,
    message="",
    custom_message="",
):
    if operator is None:
        return value
    if operator in NumericalOperators:
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
    if len(selected) == 1:
        return selected[0]
    return selected


def list_verify_assertion(
    value: List,
    operator: Optional[AssertionOperator],
    expected: List,
    message="",
    custom_message="",
):
    if operator is None:
        return value
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
        elif operator == AssertionOperator["contains"]:
            if not BuiltIn().evaluate(
                "all(item in value for item in expected)",
                namespace={"value": value, "expected": expected},
            ):
                raise_error(
                    custom_message,
                    expected,
                    " " if message else "",
                    message,
                    "should contain",
                    value,
                )
            return value
        elif operator in [
            AssertionOperator["then"],
            AssertionOperator["validate"],
        ]:
            expected = expected[0]
    return verify_assertion(value, operator, expected, message, custom_message)


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
    if operator in SequenceOperators:
        if operator not in EvaluationOperators and isinstance(expected, str):
            evaluated_expected = ast.literal_eval(expected)
        else:
            evaluated_expected = expected
        return verify_assertion(
            value, operator, evaluated_expected, message, custom_message
        )
    if expected and operator in NumericalOperators:
        for k, v in value.items():
            exp = expected[k]
            verify_assertion(v, operator, exp, message, custom_message)
        return value
    raise AttributeError(
        f"Operator '{operator.name}' is not allowed in this Keyword."
        f"Allowed operators are: {NumericalOperators} and {SequenceOperators}"
    )
