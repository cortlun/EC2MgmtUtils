import awsutils
import json
import os
from os.path import expanduser
from initfirewallconfigs import FirewallRuleConfig, FirewallRuleInstance
import time
    
#A group project object necessary for initializing a group project.
#It currently assumes a single EC2 instance per project.
class GroupProject:
    #Constructor variables are necessary for creating group project objects in AWS
    #Most objects (eg security group, group, instance name, policies, etc.) are derived
    #from project name
    def __init__(self, project_name, members, class_id, admin_user, pub_key, image_id, image_count, instance_type, account_id, region):
        self.image_id = image_id
        self.image_count = image_count
        self.admin_user = admin_user
        self.members = members
        self.project_name = project_name.upper()
        self.out = os.path.join(os.path.expanduser("~"), os.path.join("aws-utils", self.project_name + "_init.out"))
        self.aws_utils = awsutils.AwsUtils()
        self.group_name = self.project_name + "_GROUP"
        self.security_group_name = self.project_name + "_SECURITY_GROUP"
        self.class_id = class_id.upper()
        self.key_name = self.project_name + "_KEY_PAIR"
        self.instance_type = instance_type
        self.security_policy_name = self.project_name + "_SECURITY_POLICY"
        self.pub_key = pub_key
        self.account_id = account_id
        self.region = region
    #Run the sequence of methods necessary to create users, a group, a policy, a key pair, and an instance id.  Please have
    #a private/public key ready to go.  The public key file is necessary for creating the key pair and launching the instance.
    #The private key file is necessary to root into the box.
    def run(self):
        instance_running = 0
        security_group_id = self.create_security_group()
        print("security group id: " + security_group_id)
        self.create_group_and_members()
        print("created group and added members")
        self.import_key_pair()
        print("imported key pair")
        instance_id = self.launch_instance()
        print("instance launched: " + instance_id)
        self.apply_security_policy_to_group(instance_id, security_group_id)
        print("security policy applied")
        elastic_ip = self.get_ip_address()
        print("elastic ip: " + elastic_ip)
        while instance_running == 0:
            json_response = json.loads(self.aws_utils.describe_instance_status(instance_id))
            try:
                instance_state = json_response['InstanceStatuses'][0]['InstanceState']['Name']
                print("instance state: " + instance_state)
                if instance_state == "running":
                    instance_running = 1
                    print("Instance is running!")
                else:
                    raise Exception("")
            except:
                print("Instance is not running.  Sleeping 10 seconds...")
                time.sleep(10)
        self.associate_ip_address(instance_id, elastic_ip)
        print("Associated public ip: " + elastic_ip + ".")
        self.open_ssh_port()
        print("Opened SSH port.  Use your private key and this ip to access your instance: " + elastic_ip)
    #Initialize members and a group for the project.  Add members to that group.
    def create_group_and_members(self):
        json_response = json.loads(self.aws_utils.create_group(self.group_name))
        for member in self.members:
            self.aws_utils.create_user(member.id)
            self.aws_utils.create_access_key(member.id)
            self.aws_utils.add_user_to_group(member.id, self.group_name)
        return json_response['Group']['GroupId']
    #Create a key pair to be used for the new instance(s)
    def import_key_pair(self):
        self.aws_utils.import_key_pair(self.pub_key, self.project_name + "_KEY_PAIR")
    #Launch the instance
    def launch_instance(self):
        instance_json = json.loads(self.aws_utils.run_instances(self.image_id, self.image_count, self.instance_type, self.key_name, self.security_group_name))
        instance_id = instance_json['Instances'][0]['InstanceId']
        return instance_id
    #Create the security group to be attached to the instance and included in the policy.
    def create_security_group(self):
        json_response=json.loads(self.aws_utils.create_security_group(self.security_group_name, "Security group for project " + self.project_name + " in class " + self.class_id))
        security_group_id = json_response["GroupId"]
        #Use this value in the group policy.
        return security_group_id
    #Create the group policy, attach it the group
    def apply_security_policy_to_group(self, instance_id, security_group_id):
        #The below JSON gives the whole group access to start/stop the instance and to authorize and revoke ingress firewall rules.
        json_string = {"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["ec2:StartInstances","ec2:StopInstances"],"Resource":["arn:aws:ec2:us-east-1:" + self.account_id + ":instance/"+instance_id]},{"Effect":"Allow","Action":"ec2:DescribeInstances","Resource":"*"},{"Effect":"Allow","Action":"ec2:DescribeRegions","Resource":"*"},{"Effect":"Allow","Action":["ec2:RevokeSecurityGroupIngress"],"Resource":["arn:aws:ec2:us-east-1:" + self.account_id + ":security-group/"+security_group_id]},{"Effect":"Allow","Action":["ec2:AuthorizeSecurityGroupIngress"],"Resource":["arn:aws:ec2:" + self.region + ":" + self.account_id + ":security-group/"+security_group_id]}]}
        json_dump = json.dumps(json_string)
        policy_arn_object = json.loads(self.aws_utils.create_policy(self.security_policy_name, json_dump))
        #Get the policy arn so that it can be attached to the group
        policy_arn = policy_arn_object['Policy']['Arn']
        #Attach the policy arn to the group
        self.aws_utils.attach_policy_to_group(policy_arn, self.group_name)
    def get_ip_address(self):
        json_response = json.loads(self.aws_utils.allocate_address())
        elastic_ip = json_response['PublicIp']
        return elastic_ip
    def associate_ip_address(self, instance_id, elastic_ip):
        self.aws_utils.associate_address(instance_id, elastic_ip)
    def open_ssh_port(self):
        firewall_rules = []
        firewall_rules.append(FirewallRuleInstance("22", "tcp"))
        firewall_rule_config = FirewallRuleConfig(self.security_group_name, firewall_rules)
        firewall_rule_config.open_firewall()

#Member class to hold individual group members.
class Member:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = self.first_name[:1].lower() + self.last_name.lower()

#Simple main method for initializing a group project.
if __name__ == "__main__":
    members = []
    
    #Initialize group members
    members.append(Member("r", "pi", ""))
    
    #Create group project
    group_project = GroupProject("IOT_PROJECT", members, "SEIS_785", "clunke", "C:\\aws\\keys\\iot_project.pub", "ami-2051294a", "1", "t2.micro", "821971883038", "us-east-1")
    
    #Run the group project
    group_project.run()