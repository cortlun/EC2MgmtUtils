import awsutils
from Crypto.PublicKey import RSA
	
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
	def run(self):
		self.create_group_and_members()
		self.import_key_pair(self.pub_key, self.security_group_name)
		instance_id = self.launch_instance()
		
		
	#Initialize members and a group for the project.  Add members to that group.
	def create_group_and_members(self):
		self.aws_utils.create_group(self.group_name)
		for member in self.members:
			self.aws_utils.create_user(member.id)
			self.aws_utils.create_access_key(member.id)
			self.aws_utils.add_user_to_group(member.id, self.group_name)
			
	#Create a key pair to be used for the new instance(s)
	def import_key_pair(self):
		with open(self.pub_key, "r") as pub_file:
			key = RSA.importKey(pub_file.read())
			print(key)
		self.aws_utils.import_key_pair(key, project_name + "_KEY_PAIR")
		
	def launch_instance(self):
		instance_json = self.aws_utils.run_instances(self.image_id, self.image_count, self.instance_type, self.key_name, self.security_group_name)
		
		
class Member:
	def __init__(self, first_name, last_name, email):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.id = self.first_name[:1].lower() + self.last_name.lower()

#Simple main method for initializing a group project
if __name__ == "__main__":
	members = []
	
	#Initialize group members
	members.append(Member("Jim", "Boe", "jboe@stthomas.edu"))
	members.append(Member("John", "Doe", "jdoe@stthomas.edu"))
	
	#Create group project
	group_project = GroupProject("IOT_PROJECT", members, "SEIS_785", "clunke", "C:\users\lunk0002\misc\iot.pub", "ami-2051294a", 1, "t2.micro")
	
	#Run the group project
	group_project.run()