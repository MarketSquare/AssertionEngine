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
    Set Assertion Formatters
    ...    {"Is Equal": ["normalize spaces", "apply to expected"]}
    TRY
        Is Equal    A${SPACE*2}B    equal    A${SPACE*4}C
    EXCEPT    Prefix message 'A B' (str) should be 'A C' (str)
        Log    Error Message correct
    END

Setting Assertion Formatters For Not Existing Keyword Should Fail
    TRY
        Set Assertion Formatters    {"Not Here": ["strip", "apply to expected"]}
    EXCEPT    Could not find keyword from library.
        Log    Error Message Correct
    END

Setting Assertion Formatters For Not Existing Formatter Should Fail
    TRY
        Set Assertion Formatters    {"Is Equal": ["strip", "not here"]}
    EXCEPT    KeyError: 'not here'
        Log    Error Message Correct
    END

Values Are Equal
    Is Equal    1    ==    1
    Is Equal As Number    1    ==    ${1}
    Is Equal    One    Equals    One

Values Are Equal With Formatter
    Set Assertion Formatters    {"Is Equal": ["strip", "normalize spaces"]}
    Is Equal    ${SPACE}${SPACE}1${SPACE}${SPACE}1${SPACE}1${SPACE}${SPACE}    equal
    ...    1${SPACE}1${SPACE}1

Values Are Equal With Case Insensitive Formatter
    Set Assertion Formatters    {"Is Equal": ["case insensitive"]}
    Is Equal    FOOBAR    equal    foobar
    TRY
        Is Equal    FOOBAR    equal    foobaR
    EXCEPT    Prefix message 'foobar' (str) should be 'foobaR' (str)
        Log    Error Message Correct
    END
    Set Assertion Formatters    {"Is Equal": ["case insensitive", "apply to expected"]}
    Is Equal    FOOBAR    equal    foobaR

Values Are Equal With Formatter For Expected
    Set Assertion Formatters    {"Is Equal": ["strip", "apply to expected"]}
    Is Equal    1${SPACE}1${SPACE}1    equal
    ...    ${SPACE * 2}1${SPACE}1${SPACE}1${SPACE * 2}

Formatter Fails When Value Is Not Corrent Type
    Set Assertion Formatters    {"Is Equal As Number": ["strip", "normalize spaces"]}
    TRY
        Is Equal As Number    ${SPACE}1${SPACE}    ==    ${1}
    EXCEPT    AttributeError: 'int' object has no attribute 'strip'
        Log    Error Message Correct
    END

Values Are Equal Fails
    TRY
        Is Equal    1    ==    2
    EXCEPT    Prefix message '1' (str) should be '2' (str)
        Log    Error Message Correct
    END

Values Are Equal Fails Witn Different Spaces
    TRY
        Is Equal    1　1 1    ==    2❤️🥳😀
    EXCEPT    Prefix message '1\\u30001\\u200a1' (str) should be '2❤️🥳😀' (str)
        Log    Error Message Is Correct
    END

Values Are Equal Fails With Formatter
    Set Assertion Formatters    {"Is Equal": ["strip", "normalize spaces"]}
    TRY
        Is Equal    ${SPACE}1${SPACE}1    ==    ${SPACE}1${SPACE}2
    EXCEPT    Prefix message '1 1' (str) should be ' 1 2' (str)
        Log    Error Message Correct
    END

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
