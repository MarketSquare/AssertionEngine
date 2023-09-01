*** Settings ***
Resource    resource.resource


*** Test Cases ***
Check Assertion Formatters For Suite And Global
    ${formatters} =    Get Keyword Formatters Scope
    Should Not Be Empty    ${formatters}[Scope.Global]
    Should Be Empty    ${formatters}[Scope.Suite]
    Should Be Empty    ${formatters}[Scope.Test]

Correct Formatter Is Appied
    Is Equal Scope    ${SPACE*2}A B${SPACE*2}    equal    A B
    TRY
        Is Equal Scope    ${SPACE*2}A B${SPACE*2}    equal    ${SPACE*2}A B${SPACE*2}
    EXCEPT    Prefix message 'A B' (str) should be '${SPACE*2}A B${SPACE*2}' (str)
        Log    Correct error
    END
