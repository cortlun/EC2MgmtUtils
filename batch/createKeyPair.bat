set KEY=
set KEY_FINGERPRINT=
set KEY_NAME=

aws ec2 create-key-pair --key-name %KEY_NAME% --key-material %KEY% --key-fingerprint %KEY_FINGERPRINT%

