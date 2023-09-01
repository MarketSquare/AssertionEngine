*** Settings ***
Resource    resource.resource


*** Test Cases ***
Set Assertion Formatters For Test
    ${formatters} =    Get Keyword Formatters Scope
    FOR    ${key}    IN    @{formatters}
        Should Be Empty    ${formatters}[${key}]
    END
    Set Assertion Formatter Scope
    ...    is EQual SCOPE
    ...    Test
    ...    strip
    ${formatters} =    Get Keyword Formatters Scope
    Should Be Empty    ${formatters}[Scope.Global]
    Should Be Empty    ${formatters}[Scope.Suite]
    Should Not Be Empty    ${formatters}[Scope.Test]

Test Scope Should Be Emptry
    ${formatters} =    Get Keyword Formatters Scope
    FOR    ${key}    IN    @{formatters}
        Should Be Empty    ${formatters}[${key}]
    END

 Set Assertion Formatters For Suite And Global
    ${formatters} =    Get Keyword Formatters Scope
    FOR    ${key}    IN    @{formatters}
        Should Be Empty    ${formatters}[${key}]
    END
    Set Assertion Formatter Scope
    ...    is EQual SCOPE
    ...    Global
    ...    strip
    Set Assertion Formatter Scope
    ...    is EQual SCOPE
    ...    Suite
    ...    normalize spaces
    Set Assertion Formatter Scope
    ...    is EQual SCOPE
    ...    Test
    ...    apply to expected
    ${formatters} =    Get Keyword Formatters Scope
    Should Not Be Empty    ${formatters}[Scope.Global]
    Should Not Be Empty    ${formatters}[Scope.Suite]
    Should Not Be Empty    ${formatters}[Scope.Test]

 Suite And Global State Are In Place
    ${formatters} =    Get Keyword Formatters Scope
    Should Not Be Empty    ${formatters}[Scope.Global]
    Should Not Be Empty    ${formatters}[Scope.Suite]
    Should Be Empty    ${formatters}[Scope.Test]

Correct Formatter Is Appied
    Is Equal Scope    A${SPACE*2}B    equal    A B
    TRY
        Is Equal Scope    A${SPACE*2}B    equal    A${SPACE*4}B
    EXCEPT    Prefix message 'A B' (str) should be 'A${SPACE*4}B' (str)
        Log    Correct error
    END
