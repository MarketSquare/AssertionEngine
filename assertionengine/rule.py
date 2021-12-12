import re
from typing import Union, TypeVar


T = TypeVar("T")


def _normalize_spaces(value: T) -> T:
    value = re.sub(r"\s+", " ", value)
    return value.strip()


_STRINGS = {"normalize spaces": _normalize_spaces}
_ALL_RULES = {**_STRINGS}


def apply(rule: Union[str, None], value: T) -> T:
    if rule is None:
        return value
    rule_function = _ALL_RULES.get(rule)
    if not rule_function:
        raise AssertionError(f"Could not find rule for: {rule}")
    return rule_function(value)
