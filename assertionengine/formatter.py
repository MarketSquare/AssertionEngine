import re
from typing import Dict, List

from robot.api.deco import keyword  # type: ignore


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


FormatterTypes = Dict[str, List[str]]


class Formatter:
    def __init__(self, ctx):
        self.ctx = ctx

    @property
    def keyword_formatters(self):
        return self.ctx._keyword_formatters

    @keyword_formatters.setter
    def keyword_formatters(self, formatters: dict):
        self.ctx._keyword_formatters = formatters

    @property
    def keywords(self) -> dict:
        return self.ctx.keywords

    @keyword
    def set_assertion_formatters(self, formatters: FormatterTypes):
        """Set keywords formatters for assertions.

        ``formatters`` is dictionary, where key is the keyword name
        where formatters are applied. Dictionary value is a list of
        formatter which are applied. Using keywords always replaces
        existing formatters for keywords.

        Supported formatter are: `normalize space`, `strip` and
        `apply to expected`.

        Example:
        | `Set Assertion Formatters`    {"Keyword Name": ["strip", "normalize spaces"]}
        """
        if not self._are_library_keywords(formatters):
            raise AssertionError("Could not find keyword from library.")
        formatters_with_methods = {}
        for formatter in formatters:
            formatters_with_methods[
                self._get_library_keyword(formatter)
            ] = self._get_formatters(formatters[formatter])
        self.keyword_formatters = formatters_with_methods

    def _are_library_keywords(self, formatters: dict) -> bool:
        return all([self._library_keyword(item) for item in formatters])

    def _library_keyword(self, name: str) -> bool:
        name = self._normalize_keyword(name)
        if self._get_library_keyword(name):
            return True
        return False

    def _get_library_keyword(self, name: str):
        name = self._normalize_keyword(name)
        for kw in self.keywords:
            kw_normalized = self._normalize_keyword(kw)
            if kw_normalized == name:
                return self.keywords[kw]

    def _normalize_keyword(self, name: str):
        return name.lower().replace(" ", "_")

    def _get_formatters(self, kw_formatter: List) -> List:
        return [FormatRules[formatter] for formatter in kw_formatter]
