*** Settings ***
Library           TestLibrary.py

*** Test Cases ***
Values Are Equal
    Is Equal    1    ==    1

Operator With Rules
    Is Equal    normalize${SPACE*4}spaces    equal:normalize spaces    normalize${SPACE}spaces
    Is Equal    IGNORE CASE    should be:ignore case    ignore case
    Is Equal    NORMALIZE${SPACE*4}SPACE AND CASE    ==:normalize spaces:ignore case    normalize space and case

Values Are Equal Fails
    [Documentation]    FAIL Prefix message '1' (str) should be '2' (str)
    Is Equal    1    ==    2

Values Are Equal Fails When No assertion_operator
    Run Keyword And Expect Error
    ...    ValueError: Invalid validation parameters. Assertion operator is mandatory when specifying expected value.
    ...    Is Equal    1    assertion_expected=2

Values Are Equal Fails When No assertion_expected
    Run Keyword And Expect Error
    ...    Prefix message '1' (str) should be 'None' (nonetype)
    ...    Is Equal    1    assertion_operator=equal

Values Are Equal Fails When Invalid assertion_operator
    Run Keyword And Expect Error
    ...    Prefix message `This is wrong` is not a valid assertion operator
    ...    Is Equal    1    assertion_operator=This is wrong    assertion_expected=1
