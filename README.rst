Assertion Engine
================

Generic way to create meaningful and easy to use assertions for the `Robot Framework`_
libraries. This tools is spin off from `Browser library`_ project, where the Assertion
Engine was developed as part of the of library.

.. image:: https://github.com/MarketSquare/AssertionEngine/actions/workflows/on-push.yml/badge.svg
   :target: https://github.com/MarketSquare/AssertionEngine
.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

Supported Assertions
--------------------

Currently supported assertion operators are:

+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| Operator | Alternative Operators     | Description                                                                        | Validate Equivalent              |
+==========+===========================+====================================================================================+==================================+
| ==       | equal, equals, should be  | Checks if returned value is equal to expected value.                               | value == expected                |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| !=       | inequal, should not be    | Checks if returned value is not equal to expected value.                           | value != expected                |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| >        | greater than              | Checks if returned value is greater than expected value.                           | value > expected                 |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| >=       |                           | Checks if returned value is greater than or equal to expected value.               | value >= expected                |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| <        | less than                 | Checks if returned value is less than expected value.                              | value < expected                 |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| <=       |                           | Checks if returned value is less than or equal to expected value.                  | value <= expected                |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| \*=      | contains                  | Checks if returned value contains expected value as substring.                     | expected in value                |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
|          | not contains              | Checks if returned value does not contain expected value as substring.             | expected not in value            |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| ^=       | should start with, starts | Checks if returned value starts with expected value.                               | re.search(f"^{expected}", value) |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| $=       | should end with, ends     | Checks if returned value ends with expected value.                                 | re.search(f"{expected}$", value) |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| matches  |                           | Checks if given RegEx matches minimum once in returned value (supports Python [Regex inline flags](https://docs.python.org/3/library/re.html)). | re.search(expected, value)       |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| validate |                           | Checks if given Python expression evaluates to True.                               |                                  |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| evaluate |  then                     | When using this operator, the keyword does return the evaluated Python expression. |                                  |
+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+

Supported formatters:

+-------------------+------------------------------------------------------------+
| Formatter         | Description                                                |
+===================+============================================================+
| normalize spaces  | Substitutes multiple spaces to single space from the value |
+-------------------+------------------------------------------------------------+
| strip             | Removes spaces from the beginning and end of the value     |
+-------------------+------------------------------------------------------------+
| apply to expected | Applies rules also for the expected value                  |
+-------------------+------------------------------------------------------------+
| case insensitive  | Converts value to lower case                               |
+-------------------+------------------------------------------------------------+

Usage
-----
When library developers wants to do an assertion inline with the keyword call, then AssertionEngine provides
automatic validation within single keyword call. Keyword method should get value, example from page, database
or from anything which the library interacts and then use `verify_assertion` method from AssertionEngine to
perform the validation. The `verify_assertion` methods needs three things to perform the assertion:
`value` from the system, `assertion_operator` how  the validation is performed and `assertion_expected` which
represent the expected value. It is also possible to provide custom error message and prefix the default error
message.

Example library can contain keyword::

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

AssertionEngine provides an interface to define scope for the formatters, but because scoping is a library
specific implementation, it is up to the library to decide how scoping is actually implemented. AssertionEngine
Formatter class is an `ABC <https://docs.python.org/3/library/abc.html>`_ which provides `get_formatter` and
`set_formatter` interface methods for library developers. The AssertionEngine
`atest <https://github.com/MarketSquare/AssertionEngine/tree/main/atest>`_ libraries has examples how interface
can be implemented in practice.

.. _Robot Framework: http://robotframework.org
.. _Browser library: https://robotframework-browser.org/
