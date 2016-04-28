set SECURITY_GROUP=
set DESCRIPTION=

aws ec2 create-security-group --group-name %SECURITY_GROUP% --description %DESCRIPTION%
