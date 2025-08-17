*** Settings ***
Library    ${CURDIR}\\EmailLibrary.py
Library    String

*** Variables ***
# ${Gmail}    nong.nukhun@gmail.com
# ${pass_mail}    xetl hdth asrc judh
# ${TEST_TEXT}    QXMUW
${Gmail}    Auto.esol2@gmail.com
${pass_mail}    geep ftpm zwmq noer
${TEST_TEXT}    UKURQ



*** Test Cases ***
Find Emails in Text
    [Documentation]    ค้นหาอีเมล์จากข้อความ
    #${TEST_TEXT} =    Encode String To Bytes    ${TEST_TEXT2}    ASCII    errors=replace
    #${emails}=    Read Emails   ${TEST_TEXT}
    
    ${OTP}=    Get OTP From Mail   ${Gmail}   ${pass_mail}    ${TEST_TEXT}
    Log To Console    OTP: ${OTP}

    # ${Check_result}=    Check Is Found      ${emails}
    
    # IF  ${Check_result}
    #     ${otp_gmail}=        GET OTP             ${emails}      
    #     Log To Console    OTP: ${otp_gmail}
    # END

    

*** Keywords ***
GET OTP
    [Arguments]       ${text}
    ${text}=        Get Regexp Matches             ${text}      [0-9]{6}
    RETURN    ${text}[0]

Wait For Mail
    [Arguments]     ${Gmail}   ${pass_mail}     ${search_text}       ${times}=5
    FOR    ${i}    IN RANGE    1    ${times}
        ${emails}=    Read Emails   ${Gmail}   ${pass_mail}    ${search_text}
        ${Check_result}=    Check Is Found      ${emails}
        #Log To Console    OCheck_resultTP: ${Check_result}
        IF  ${Check_result}
            Exit For Loop If    '${Check_result}' != 'Not Found'
        ELSE
            Log to console      Retry Search ${i}
            Sleep   1S
        END
    END
    RETURN    ${emails}

Get OTP From Mail
    [Arguments]     ${Gmail}   ${pass_mail}     ${search_text}       ${times}=5
    FOR    ${i}    IN RANGE    1    ${times}
        ${emails}=    Read Emails   ${Gmail}   ${pass_mail}    ${search_text}
        ${Check_result}=    Check Is Found      ${emails}
        #Log To Console    OCheck_resultTP: ${Check_result}
        IF  ${Check_result}
            Exit For Loop If    '${Check_result}' != 'Not Found'
        ELSE
            Log to console      Retry Search ${i}
            Sleep   1S
        END
    END
    ${text}=        Get Regexp Matches             ${emails}      [0-9]{6}

    RETURN    ${text}[0]

Check Is Found
    [Arguments]     ${messages}
    ${Is_Found}=    Set Variable    True
    ${text}=    Get Substring    ${messages}    0    9
    IF  "${text}" == "Not Found"
        ${Is_Found}=    Set Variable    False
    END

    RETURN    ${Is_Found}
    