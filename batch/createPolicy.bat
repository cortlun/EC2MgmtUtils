set POLICY_NAME=
set POLICY_DOCUMENT_PATH=

aws iam create-policy --policy-name %POLICY_NAME% --policy-document=%POLICY_DOCUMENT_PATH%
