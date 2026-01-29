# Assertion Engine

Generic way to create meaningful and easy to use assertions for the [Robot Framework](http://robotframework.org) libraries. This tool is a spin off from the [Browser library](https://robotframework-browser.org/) project, where the Assertion Engine was developed as part of that library.

[![CI](https://github.com/MarketSquare/AssertionEngine/actions/workflows/on-push.yml/badge.svg)](https://github.com/MarketSquare/AssertionEngine)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Supported Assertions

Currently supported assertion operators are:

| Operator | Alternative Operators | Description | Validate Equivalent |
|---|---|---|---|
| `==` | `equal`, `equals`, `should be` | Checks if returned value is equal to expected value. | `value == expected` |
| `!=` | `inequal`, `should not be` | Checks if returned value is not equal to expected value. | `value != expected` |
| `>` | `greater than` | Checks if returned value is greater than expected value. | `value > expected` |
| `>=` |  | Checks if returned value is greater than or equal to expected value. | `value >= expected` |
| `<` | `less than` | Checks if returned value is less than expected value. | `value < expected` |
| `<=` |  | Checks if returned value is less than or equal to expected value. | `value <= expected` |
| `*=` | `contains` | Checks if returned value contains expected value as substring. | `expected in value` |
| (no operator) | `not contains` | Checks if returned value does not contain expected value as substring. | `expected not in value` |
| `^=` | `should start with`, `starts` | Checks if returned value starts with expected value. | `re.search(f"^{expected}", value)` |
| `$=` | `should end with`, `ends` | Checks if returned value ends with expected value. | `re.search(f"{expected}$", value)` |
| `matches` |  | Checks if given RegEx matches minimum once in returned value (supports Python [Regex inline flags](https://docs.python.org/3/library/re.html)). | `re.search(expected, value)` |
| `validate` |  | Checks if given Python expression evaluates to `True`. |  |
| `evaluate` / `then` |  | When using this operator, the keyword returns the evaluated Python expression. |  |

## Supported formatters

| Formatter | Description |
|---|---|
| `normalize spaces` | Substitutes multiple spaces to single space from the value |
| `strip` | Removes spaces from the beginning and end of the value |
| `apply to expected` | Applies rules also for the expected value |
| `case insensitive` | Converts value to lower case |

## Usage

When library developers want to do an assertion inline with the keyword call, AssertionEngine provides automatic validation within a single keyword call. The keyword method should get the `value` (for example from a page, database or any other source) and then use `verify_assertion` from AssertionEngine to perform the validation. The `verify_assertion` method needs three things to perform the assertion: the `value` from the system, an `assertion_operator` describing how the validation is performed and `assertion_expected` which represents the expected value. It is also possible to provide a custom error message and prefix the default error message.

Example:

```python
def keyword(
    arg_to_get_value: str,
    assertion_operator: Optional[AssertionOperator] = None,
    assertion_expected: Any = None,
    message: str = None,
):
    value = method_to_get_value(arg_to_get_value)
    return verify_assertion(
        value,
        assertion_operator,
        assertion_expected,
        "Prefix message",
        message,
    )
```

AssertionEngine provides an interface to define scope for the formatters, but because scoping is a library-specific implementation, it is up to the library to decide how scoping is actually implemented. AssertionEngine `Formatter` class is an [ABC](https://docs.python.org/3/library/abc.html) which provides `get_formatter` and `set_formatter` interface methods for library developers. The AssertionEngine `atest` directory has examples how the interface can be implemented in practice: https://github.com/MarketSquare/AssertionEngine/tree/main/atest

---

For more information about Robot Framework see: http://robotframework.org
For Browser library see: https://robotframework-browser.org/
