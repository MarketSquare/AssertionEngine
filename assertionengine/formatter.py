import re
from abc import ABC, abstractmethod
from typing import List


def _strip(value: str) -> str:
    return value.strip()


def _normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value)


def _apply_to_expected(value: str) -> str:
    return value


def _case_insensitive(value: str) -> str:
    return value.lower()


FormatRules = {
    "normalize spaces": _normalize_spaces,
    "strip": _strip,
    "apply to expected": _apply_to_expected,
    "case insensitive": _case_insensitive,
}


class Formatter(ABC):
    @abstractmethod
    def get_formatter(self, keyword):
        ...

    @abstractmethod
    def set_formatter(self, keyword, formatter):
        ...

    def normalize_keyword(self, name: str):
        return name.lower().replace(" ", "_")

    def formatters_to_method(self, kw_formatter: List) -> List:
        return [FormatRules[formatter.lower()] for formatter in kw_formatter]
