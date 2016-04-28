set IMAGE_ID=
set COUNT=
set INSTANCE_TYPE=
set KEY_NAME=
set SECURITY_GROUP=

aws ec2 run-instances --image-id %IMAGE_ID% --count %COUNT% --instance-type %INSTANCE_TYPE% --key-name %KEY_NAME% --security-groups %SECURITY_GROUP%
