import awsutils
	
#A group project object necessary for initializing a group project.
#It currently assumes a single EC2 instance per project.
class GroupProject:
	#Constructor variables are necessary for creating group project objects in AWS
	#Most objects (eg security group, group, instance name, policies, etc.) are derived
	#from project name
	def __init__(self, project_name, members, class_id, admin_user, pub_key):
		self.admin_user = admin_user
		self.members = members
		self.project_name = project_name.upper()
		self.aws_utils = awsutils.AwsUtils()
		self.group_name = project_name.upper() + "_GROUP"
		self.security_group_name = self.project_name + "_SECURITY_GROUP"
		self.class_id = class_id.upper()
	def run(self):
		#self.create_group_and_members()
		self.import_key_pair()
	def create_group_and_members(self):
		self.aws_utils.create_group(self.group_name)
		for member in self.members:
			self.aws_utils.create_user(member.id)
			self.aws_utils.create_access_key(member.id)
			self.aws_utils.add_user_to_group(member.id, self.group_name)
	def import_key_pair(self):
		self.aws_utils.import_key_pair(pub_key, project_name + "_KEY_PAIR")
	#def create_security_group(self):
		
	#def launch_instance(self):
		#self.aws_utils.run_instances()
		
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
	group_project = GroupProject("PYTHON_TEST_PROJECT", members, "PYTHON_TEST_CLASS", "clunke", "C:\aws\keys\PYTHON_TEST_PROJECT.pub")
	
	#Run the group project
	group_project.run()