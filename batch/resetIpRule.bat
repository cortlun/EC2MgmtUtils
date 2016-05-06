REM Initialize environment variables
setlocal enableextensions enabledelayedexpansion
set LAST_IP_FILE=C:\Users\43365\Documents\GRADSCHOOLWHADUP\SEIS_635\SEIS_635_TeamProject\EC2Stuff\Scripts\data\lastip2.txt
set GROUP_NAME=IOT_PROJECT_SECURITY_GROUP
set NEW_IP=140.209.14.75/32
echo New IP: %NEW_IP%
REM Create new rules
echo creating new rules
aws ec2 authorize-security-group-ingress --group-name %GROUP_NAME% --protocol tcp --port 9092 --cidr %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %GROUP_NAME% --protocol tcp --port 22 --cidr %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %GROUP_NAME% --protocol icmp --port -1 --cidr %NEW_IP%

REM Delete rules for old IP
if exist %LAST_IP_FILE% (
    echo deleting old rules
    set /p LAST_IP=<!LAST_IP_FILE!
    echo Last ip: !LAST_IP!
    aws ec2 revoke-security-group-ingress --group-name %GROUP_NAME% --protocol tcp --port 9092 --cidr !LAST_IP!
    aws ec2 revoke-security-group-ingress --group-name %GROUP_NAME% --protocol tcp --port 22 --cidr !LAST_IP!
    aws ec2 revoke-security-group-ingress --group-name %GROUP_NAME% --protocol icmp --port -1 --cidr !LAST_IP!
    del %LAST_IP_FILE%
)



REM Write IP address to temp file for later deletion
echo %NEW_IP% > %LAST_IP_FILE%
echo done
