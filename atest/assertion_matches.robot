*** Settings ***
Library     TestLibrary.py


*** Test Cases ***
Match No Groups
    ${result} =    Is Equal    Hello World    matches    Hello World
    Should Be Equal    ${result}    Hello World

Match With Group
    ${result} =    Is Equal    Hello World    matches    Hello (World)
    Length Should Be    ${result}    1
    Should Be Equal    ${result}[0]    World

    ${result} =    Is Equal    Hello World    matches    (Hello) (World)
    Length Should Be    ${result}    2
    Should Be Equal    ${result}[0]    Hello
    Should Be Equal    ${result}[1]    World

Match With Named Group
    ${result} =    Is Equal    Hello World    matches    (?P<first>Hello)
    Length Should Be    ${result}    1
    Should Be Equal    ${result['first']}    Hello
