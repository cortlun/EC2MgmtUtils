set POLICY_ARN=
set GROUP_NAME=

aws iam attach-group-policy --policy-arn %POLICY_ARN% --group-name %GROUP_NAME%
