import json

if __name__ == "__main__":
    json_string = {"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["ec2:StartInstances","ec2:StopInstances"],"Resource":["arn:aws:ec2:us-east-1:" + "821971883038" + ":instance/"+"i-21442234"]},{"Effect":"Allow","Action":"ec2:DescribeInstances","Resource":"*"},{"Effect":"Allow","Action":"ec2:DescribeRegions","Resource":"*"},{"Effect":"Allow","Action":["ec2:RevokeSecurityGroupIngress"],"Resource":["arn:aws:ec2:us-east-1:" + "821971883038" + ":security-group/"+"s-21314124"]},{"Effect":"Allow","Action":["ec2:AuthorizeSecurityGroupIngress"],"Resource":["arn:aws:ec2:" + "us-east-1" + ":" + "821971883038" + ":security-group/"+"s-21314124"]}]}
    json_dump = json.dumps(json_string)
    policy_object = json.loads(json_dump)
    print("json dump: " + json_dump)