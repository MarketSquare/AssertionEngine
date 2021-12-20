Assertion Engine
================

Generic way to create meaningful and easy to use assertions for the `Robot Framework`_
libraries. This tools is spin off from `Browser library`_ project, where the Assertion
Engine was developed as part of the of library.

.. image:: https://github.com/MarketSquare/AssertionEngine/actions/workflows/on-push.yml/badge.svg
   :target: https://github.com/MarketSquare/AssertionEngine
.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
.. image:: https://github.com/MarketSquare/AssertionEngine/actions/workflows/on-push.yml/badge.svg
   :target: https://github.com/MarketSquare/AssertionEngine/actions/workflows/on-push.yml

Supported Assertions
--------------------

Currently supported assertion operators are:

+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+
| Operator | Alternative Operators     | Description                                                                        | Validate Equivalent              |
+==========+===========================+====================================================================================+==================================+
| ==       | equal, should be          | Checks if returned value is equal to expected value.                               | value == expected                |
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
| matches  |                           | Checks if given RegEx matches minimum once in returned value.                      | re.search(expected, value)       |
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

Usage
-----
When keywords needs to do an assertion


.. _Robot Framework: http://robotframework.org
.. _Browser library: https://robotframework-browser.org/
