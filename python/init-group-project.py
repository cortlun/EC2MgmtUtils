import awsutils
	
class GroupProject:
	def __init__(self, project_name, members, class_id, admin_user):
		self.admin_user = admin_user
		self.members = members
		self.project_name = project_name.upper()
		self.aws_utils = awsutils.AwsUtils()
		self.group_name = project_name.upper() + "_GROUP"
		self.security_group_name = self.project_name + "_SECURITY_GROUP"
		self.class_id = class_id.upper()
	def run(self):
		self.create_group_and_members()
	def create_group_and_members(self):
		self.aws_utils.create_group(self.group_name)
		for member in self.members:
			self.aws_utils.create_user(member.id)
			self.aws_utils.create_access_key(member.id)
			self.aws_utils.add_user_to_group(member.id, self.group_name)
	def launch_instance(self):
		
class Member:
	def __init__(self, first_name, last_name, email):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.id = self.first_name[:1].lower() + self.last_name.lower()
		
if __name__ == "__main__":
	members = []
	#Initialize group members
	members.append(Member("Jim", "Boe", "jboe@stthomas.edu"))
	members.append(Member("John", "Doe", "jdoe@stthomas.edu"))
	group_project = GroupProject("PYTHON_TEST_PROJECT", members, "PYTHON_TEST_CLASS", "clunke")
	group_project.run()