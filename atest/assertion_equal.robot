*** Settings ***
Library     TestLibrary.py


*** Test Cases ***
Set Assertion Formatters
    ${formatters} =    Get Keyword Formatters
    Should Be Empty    ${formatters}
    Set Assertion Formatters
    ...    {"Is Equal": ["strip", "apply to expected"], "get Keyword formatters": ["strip", "normalize spaces"]}
    ${formatters} =    Get Keyword Formatters
    Length Should Be    ${formatters}    2
    FOR    ${formatter}    IN    @{formatters}
        Length Should Be    ${formatters}[${formatter}]    2
    END

Test With Assertion Formatter Apply To Expected
    Set Assertion Formatters
    ...    {"Is Equal": ["normalize spaces", "apply to expected"]}
    Is Equal    A${SPACE*2}B    equal    A${SPACE*4}B

Test Fail With Assertion Formatter Apply To Expected
    [Documentation]    FAIL Prefix message 'A B' (str) should be 'A C' (str)
    Set Assertion Formatters
    ...    {"Is Equal": ["normalize spaces", "apply to expected"]}
    Is Equal    A${SPACE*2}B    equal    A${SPACE*4}C

Setting Assertion Formatters For Not Existing Keyword Should Fail
    [Documentation]    FAIL Could not find keyword from library.
    Set Assertion Formatters    {"Not Here": ["strip", "apply to expected"]}

Setting Assertion Formatters For Not Existing Formatter Should Fail
    [Documentation]    FAIL KeyError: 'not here'
    Set Assertion Formatters    {"Is Equal": ["strip", "not here"]}

Values Are Equal
    Is Equal    1    ==    1
    Is Equal As Number    1    ==    ${1}

Values Are Equal With Formatter
    Set Assertion Formatters    {"Is Equal": ["strip", "normalize spaces"]}
    Is Equal    ${SPACE}${SPACE}1${SPACE}${SPACE}1${SPACE}1${SPACE}${SPACE}    equal
    ...    1${SPACE}1${SPACE}1

Values Are Equal With Formatter For Expected
    Set Assertion Formatters    {"Is Equal": ["strip", "apply to expected"]}
    Is Equal    1${SPACE}1${SPACE}1    equal
    ...    ${SPACE * 2}1${SPACE}1${SPACE}1${SPACE * 2}

Formatter Fails When Value Is Not Corrent Type
    [Documentation]    FAIL AttributeError: 'int' object has no attribute 'strip'
    Set Assertion Formatters    {"Is Equal As Number": ["strip", "normalize spaces"]}
    Is Equal As Number    ${SPACE}1${SPACE}    ==    ${1}

Values Are Equal Fails
    [Documentation]    FAIL Prefix message '1' (str) should be '2' (str)
    Is Equal    1    ==    2

Values Are Equal Fails With Formatter
    [Documentation]    FAIL Prefix message '1 1' (str) should be ' 1 2' (str)
    Set Assertion Formatters    {"Is Equal": ["strip", "normalize spaces"]}
    Is Equal    ${SPACE}1${SPACE}1    ==    ${SPACE}1${SPACE}2

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
    ...    ValueError: Argument 'assertion_operator' got value 'This is wrong' that cannot be converted to AssertionOperator or None.
    ...    Is Equal
    ...    1
    ...    assertion_operator=This is wrong
    ...    assertion_expected=1
