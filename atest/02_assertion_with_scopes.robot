*** Settings ***
Resource    resource.resource


*** Test Cases ***
Check Assertion Formatters For Suite And Global
    ${formatters} =    Get Keyword Formatters Scope
    Should Not Be Empty    ${formatters}[Scope.Global]
    Should Not Be Empty    ${formatters}[Scope.Suite]
    Should Be Empty    ${formatters}[Scope.Test]
