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

from enum import Enum

AssertionOperator = Enum(
    "AssertionOperator",
    {
        "equal": "==",
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
    Enum that defines the ``assertion_operator`` <`AssertionOperator`>.

    Currently supported assertion operators are:

    |      = Operator =   |   = Alternative Operators =       |              = Description =                                         | = Validate Equivalent =              |
    | ``==``              | ``equal``, ``should be``          | Checks if returned value is equal to expected value.                 | ``value == expected``                |
    | ``!=``              | ``inequal``, ``should not be``    | Checks if returned value is not equal to expected value.             | ``value != expected``                |
    | ``>``               | ``greater than``                  | Checks if returned value is greater than expected value.             | ``value > expected``                 |
    | ``>=``              |                                   | Checks if returned value is greater than or equal to expected value. | ``value >= expected``                |
    | ``<``               | ``less than``                     | Checks if returned value is less than expected value.                | ``value < expected``                 |
    | ``<=``              |                                   | Checks if returned value is less than or equal to expected value.    | ``value <= expected``                |
    | ``*=``              | ``contains``                      | Checks if returned value contains expected value as substring.       | ``expected in value``                |
    | ``^=``              | ``should start with``, ``starts`` | Checks if returned value starts with expected value.                 | ``re.search(f"^{expected}", value)`` |
    | ``$=``              | ``should end with``, ``ends``     | Checks if returned value ends with expected value.                   | ``re.search(f"{expected}$", value)`` |
    | ``matches``         |                                   | Checks if given RegEx matches minimum once in returned value.        | ``re.search(expected, value)``       |
    | ``validate``        |                                   | Checks if given Python expression evaluates to ``True``.             |                                      |
    | ``evaluate``        |  ``then``                         | When using this operator, the keyword does return the evaluated Python expression. |                        |


    The assertion keywords will provide an error message if the assertion fails.
    Assertions will retry until ``timeout`` has expired if they do not pass.

    The assertion ``assertion_expected`` value is not converted by the library and
    is used as is. Therefore when assertion is made, the ``assertion_expected``
    argument value and value returned the keyword must have same type. If types
    are not same, assertion will fail. Example `Get Text` always returns a string
    and has to be compared with a string, even the returnd value might look like
    a number.

    Other Keywords have other specific types they return.
    `Get Element Count` always returns an integer.
    `Get Bounding Box` and `Get Viewport Size` can be filtered.
    They return a dictionary without filter and a number when filtered.
    These Keywords do autoconvert the expected value if a number is returned.

    * < less or greater > With Strings*
    Compairisons of strings with ``greater than`` or ``less than`` compares each character,
    starting from 0 reagarding where it stands in the code page.
    Example: ``A < Z``, ``Z < a``, ``ac < dc`
    It does never compare the length of elements. Neither lists nor strings.
    The comparison stops at the first character that is different.
    Examples: ``'abcde' < 'abd'``, ``'100.000' < '2'``
    In Python 3 and therefore also in Browser it is not possible to compare numbers
    with strings with a greater or less operator.
    On keywords that return numbers, the given expected value is automatically
    converted to a number before comparison.


    The getters `Get Page State` and `Get Browser Catalog` return a dictionary. Values of the dictionary can directly asserted.
    Pay attention of possible types because they are evaluated in Python. For example:

    | Get Page State    validate    2020 >= value['year']                     # Compairsion of numbers
    | Get Page State    validate    "IMPORTANT MESSAGE!" == value['message']  # Compairsion of strings

    == The 'then' or 'evaluate' closure ==

    Keywords that accept arguments ``assertion_operator`` and ``assertion_expected``
    can optionally also use ``then`` or ``evaluate`` closure to modify the returned value with
    BuiltIn Evaluate. Actual value can be accessed with ``value``.

    For example ``Get Title  then  'TITLE: '+value``.
    See
    [https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Evaluating%20expressions|
    Builtin Evaluating expressions]
    for more info on the syntax.

    == Examples ==

    | # *Keyword*    *Selector*                    *Key*        *Assertion Operator*    *Assertion Expected*
    | Get Title                                           equal                 Page Title
    | Get Title                                           ^=                    Page
    | Get Style    //*[@id="div-element"]      width      >                     100
    | Get Title                                           matches               \\\\w+\\\\s\\\\w+
    | Get Title                                           validate              value == "Login Page"
    | Get Title                                           evaluate              value if value == "some value" else "something else"
    """
