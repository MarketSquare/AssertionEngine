from typing import Any

FALSE_STRINGS = {"FALSE", "NO", "OFF", "0", "UNCHECKED", "NONE", ""}


def type_converter(argument: Any) -> str:
    return type(argument).__name__.lower()


def is_truthy(item: Any) -> bool:
    if isinstance(item, bool):
        return item
    if isinstance(item, str):
        return item.upper() not in FALSE_STRINGS
    return bool(item)
