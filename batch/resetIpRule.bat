REM Initialize environment variables
setlocal enableextensions enabledelayedexpansion
set LAST_IP_FILE=C:\Users\43365\Documents\GRADSCHOOLWHADUP\SEIS_635\SEIS_635_TeamProject\EC2Stuff\Scripts\data\lastip.txt
set NERAKA_GROUP_NAME="SEIS_635_NERAKA"
set SOLACE_GROUP_NAME="SEIS_635_SOLACE"
set PALANTHAS_GROUP_NAME="SEIS_635_PALANTHAS"

REM Delete rules for old IP
if exist %LAST_IP_FILE% (
	echo deleting old rules
	set /p LAST_IP=<!LAST_IP_FILE!
	echo Last ip: !LAST_IP!
	aws ec2 revoke-security-group-ingress --group-name %NERAKA_GROUP_NAME% --protocol tcp --port 8080 --cidr !LAST_IP!
	aws ec2 revoke-security-group-ingress --group-name %NERAKA_GROUP_NAME% --protocol tcp --port 22 --cidr !LAST_IP!
	aws ec2 revoke-security-group-ingress --group-name %NERAKA_GROUP_NAME% --protocol icmp --port -1 --cidr !LAST_IP!
	aws ec2 revoke-security-group-ingress --group-name %SOLACE_GROUP_NAME% --protocol tcp --port 1337 --cidr !LAST_IP!
	del %LAST_IP_FILE%
)

REM Get your IP from AWS
for /f "delims=" %%a in ('wget -qO- http://checkip.amazonaws.com') do @set NEW_IP=%%a/32

REM Create new rules
echo creating new rules
echo New IP: %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %NERAKA_GROUP_NAME% --protocol tcp --port 8080 --cidr %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %NERAKA_GROUP_NAME% --protocol tcp --port 22 --cidr %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %NERAKA_GROUP_NAME% --protocol icmp --port -1 --cidr %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %SOLACE_GROUP_NAME% --protocol tcp --port 1337 --cidr %NEW_IP%
aws ec2 authorize-security-group-ingress --group-name %PALANTHAS_GROUP_NAME% --protocol tcp --port 7474 --cidr %NEW_IP%

REM Write IP address to temp file for later deletion
echo %NEW_IP% > %LAST_IP_FILE%
echo done
