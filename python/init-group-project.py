import awsutils
from Crypto.PublicKey import RSA
import json
#Example: http://stackoverflow.com/questions/12344332/parsing-muilti-dimensional-json-array-to-python
	
#A group project object necessary for initializing a group project.
#It currently assumes a single EC2 instance per project.
class GroupProject:
	#Constructor variables are necessary for creating group project objects in AWS
	#Most objects (eg security group, group, instance name, policies, etc.) are derived
	#from project name
	def __init__(self, project_name, members, class_id, admin_user, pub_key, image_id, image_count, instance_type):
		self.image_id = image_id
		self.image_count = image_count
		self.admin_user = admin_user
		self.members = members
		self.project_name = project_name.upper()
		self.aws_utils = awsutils.AwsUtils()
		self.group_name = self.project_name + "_GROUP"
		self.security_group_name = self.project_name + "_SECURITY_GROUP"
		self.class_id = class_id.upper()
		self.key_name = self.project_name + "_KEY_PAIR"
		self.instance_type = instance_type
		self.security_policy_name = self.project_name + "_SECURITY_POLICY"
	#Run the sequence of methods necessary to create users, a group, a policy, a key pair, and an instance id.  Please have
	#a private/public key ready to go.  The public key file is necessary for creating the key pair and launching the instance.
	#The private key file is necessary to root into the box.
	def run(self):
		security_group_id = self.create_security_group()
		self.create_group_and_members()
		self.import_key_pair()
		instance_id = self.launch_instance()
		self.apply_security_policy_to_group(instance_id, security_group_id)
	#Initialize members and a group for the project.  Add members to that group.
	def create_group_and_members(self):
		json_response = json.loads(self.aws_utils.create_group(self.group_name))
		for member in self.members:
			self.aws_utils.create_user(member.id)
			self.aws_utils.create_access_key(member.id)
			self.aws_utils.add_user_to_group(member.id, self.group_name)
		return json_response['GroupId']
	#Create a key pair to be used for the new instance(s)
	def import_key_pair(self):
		with open(self.pub_key, "r") as pub_file:
			key = RSA.importKey(pub_file.read())
			print(key)
		self.aws_utils.import_key_pair(key, project_name + "_KEY_PAIR")
	#Launch the instance
	def launch_instance(self):
		instance_json = json.loads(self.aws_utils.run_instances(self.image_id, self.image_count, self.instance_type, self.key_name, self.security_group_name))
		instance_id = instance_json['Instances']['InstanceId']
		return instance_id
	#Create the security group to be attached to the instance and included in the policy.
	def create_security_group(self):
		json_response = json.loads(self.aws_utils.create_security_group(self.security_group_name, "Security group for project " + self.project_name + " in class " + self.class_id))
		security_group_id = json_response["GroupId"]
		#Use this value in the group policy.
		return security_group_id
	#Create the group policy, attach it the group
	def apply_security_policy_to_group(self, instance_id, security_group_id):
		#The below JSON gives the whole group access to start/stop the instance and to authorize and revoke ingress firewall rules.
		json_string = {"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["ec2:StartInstances","ec2:StopInstances"],"Resource":["arn:aws:ec2:us-east-1:821971883038:instance/"+self.instance_id]},{"Effect":"Allow","Action":"ec2:DescribeInstances","Resource":"*"},{"Effect":"Allow","Action":"ec2:DescribeRegions","Resource":"*"},{"Effect":"Allow","Action":["ec2:RevokeSecurityGroupIngress"],"Resource":["arn:aws:ec2:us-east-1:821971883038:security-group/"+security_group_id]},{"Effect":"Allow","Action":["ec2:AuthorizeSecurityGroupIngress"],"Resource":["arn:aws:ec2:us-east-1:821971883038:security-group/"+security_group_id]}]}
		dump = json.dumps(json_string)
		policy_object = json.loads(json_dump)
		print(json_object)
		policy_arn_object = json.loads(self.aws_utils.create_policy(self.security_policy_name, policy_object))
		#Get the policy arn so that it can be attached to the group
		policy_arn = policy_arn_object['Policy']['ARN']
		#Attach the policy arn to the group
		self.aws_utils.attach_policy_to_group(policy_arn, self.group_name)

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
	members.append(Member("Jim", "Boe", "jboe@stthomas.edu"))
	members.append(Member("John", "Doe", "jdoe@stthomas.edu"))
	
	#Create group project
	group_project = GroupProject("IOT_PROJECT", members, "SEIS_785", "clunke", "C:\users\lunk0002\misc\iot.pub", "ami-2051294a", 1, "t2.micro")
	
	#Run the group project
	group_project.run()