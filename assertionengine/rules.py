import re
from typing import Any, List, Tuple

from .assertion_engine import AssertionOperator
from .type_converter import is_string


def get_operator_and_rules(
    operator_with_rules: Any,
) -> Tuple[AssertionOperator, Any]:
    """
    This function allows to parse a string like `operator:rule[:rule2][:ruleN]`
    to be separated into the operator itself and its rules.
    """
    match = re.match(r"^[a-zA-Z\s=\!<>*^$]+[^:]", operator_with_rules)
    if match:
        operator = match.group(0)
    else:
        raise ValueError(
            f"`{operator_with_rules}` does not contain any AssertionOperator."
        )
    # try to cast to AssertionOperator
    try:
        operator = AssertionOperator[operator]
    # KeyError is excepted here, since it is handled in the `verify_assertion` function.
    except KeyError:
        pass
    # rules_raw will receive a list of strings in format ':rule'
    rules_raw = re.findall(r"[:][a-z\s]+", operator_with_rules)
    rules = []
    if rules_raw is not None:
        for rule in rules_raw:
            # each rule from `rules_raw` is normalized,
            # i.e. ':', leading and trailing white spaces are stripped
            rules.append(rule.strip(": "))
    return operator, rules


def apply_rules(value: Any, expected: Any, rules: List):
    for rule in rules:
        if rule == "normalize spaces":
            value = _normalize_spaces(value)
            expected = _normalize_spaces(expected)
        if rule == "ignore case":
            value = _normalize_case(value)
            expected = _normalize_case(expected)
    return value, expected


def _normalize_spaces(value: Any) -> Any:
    return re.sub(r"\s+", " ", value) if is_string(value) else value


def _normalize_case(value: Any) -> Any:
    return value.lower() if is_string(value) else value
