*** Settings ***
Library           TestLibrary.py

*** Test Case ***
Values Are Equal
    Is Equal    1    ==    1

Values Are Equal Fails
    [Documentation]    FAIL Prefix message '1' (str) should be '2' (str)
    Is Equal    1    ==    2
