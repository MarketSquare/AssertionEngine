import re
from typing import Any, Union


def _normalize_spaces(value: Any) -> Any:
    value = re.sub(r"\s+", " ", value)
    return value.strip()


_STRINGS = {"normalize spaces": _normalize_spaces}
_ALL_RULES = {**_STRINGS}


def apply_rule(rule: Union[str, None], value: Any) -> Any:
    if rule is None:
        return value
    rule_function = _ALL_RULES.get(rule)
    if not rule_function:
        raise AssertionError(f"Could not find rule for: {rule}")
    return rule_function(value)
