from subprocess import call
import os
from os.path import expanduser
import urllib.request
from Crypto.PublicKey import RSA

class ChildProcessUtils:
    def __init__(self, log_file):
        self.user_home = os.path.expanduser("~")
        self.aws_utils_home = os.path.join(self.user_home, "awsutils")
        self.log_directory = os.path.join(self.aws_utils_home, "logs")
        self.previous_ip_location = os.path.join(self.aws_utils_home, "last_ip.txt")
        self.log_file = log_file
    def spawn_child_process(self, args):
        call(args)
    
class AwsUtils:
    def __init__(self):
        self.user_home = expanduser("~")
        self.aws_utils_home = os.path.join(self.user_home, "awsutils")
        self.log_directory = os.path.join(self.aws_utils_home, "logs")
        self.previous_ip_location = os.path.join(self.aws_utils_home, "last_ip.txt")
        self.cp_utils = ChildProcessUtils("aws_utils.log")
    def add_user_to_group(self, user_name, group_name):
        self.cp_utils.spawn_child_process(["aws", "iam", "add-user-to-group", "--user-name", user_name, "--group-name", group_name])
    def attach_policy_to_group(self,policy_arn, group_name):
        self.cp_utils.spawn_child_process(["aws", "iam", "attach-group-policy", "--policy-arn", policy_arn, "--group-name", group_name])
    def create_access_key(self,user_name):
        self.cp_utils.spawn_child_process(["aws", "iam", "create-access-key", "--user-name", user_name])
    def create_group(self, group_name):
        self.cp_utils.spawn_child_process(["aws", "iam", "create-group", "--group-name", group_name])
    def create_key_pair(self, key, key_fingerprint, key_name):
        self.cp_utils.spawn_child_process(["aws", "ec2", "create-key-pair", "--key-name", key_name, "--key-material", key, "--key-fingerprint", key_fingerprint])
    def create_policy(self,policy_name, policy_document):
        self.cp_utils.spawn_child_process(["aws", "iam", "create-policy", "--policy-name", policy_name, "--policy-document", policy_document])
    def create_security_group(self,security_group, description):
        self.cp_utils.spawn_child_process(["aws", "ec2", "create-security-group", "--group-name", security_group, "--description", description])
    def create_user(self,user_name):
        self.cp_utils.spawn_child_process(["aws", "iam", "create-user", "--user-name", user_name])
    def import_key_pair(self, public_key_location, key_name):
        with open(public_key_location) as public_key:
            keydata = public_key.read()
        pubkey = RSA.importKey(binPubKey)
        print(pubkey)
    def run_instances(self,image_id, count, instance_type, key_name, security_group):
        self.cp_utils.spawn_child_process(["aws", "ec2", "run-instances", "--image-id", image_id, "--count", count, "--instance-type", instance_type, "--key-name", key_name, "--security-group", security_group])
    def revoke_firewall_privelege(self,group_name, port, protocol, ip):
        self.cp_utils.spawn_child_process(["aws", "ec2", "revoke-security-group-ingress", "--group-name", group_name, "--protocol", protocol, "--port", port, "--cidr", ip])
    def authorize_firewall_privelege(self,group_name, port, protocol, ip):
        previous_ip = get_previous_ip();
        if previous_ip is not None:
            revoke_firewall_privelege(group_name, port, protocol, previous_ip)        
        self.cp_utils.spawn_child_process(["aws", "ec2", "authorize-security-group-ingress", "--group-name", group_name, "--protocol", protocol, "--port", port, "--cidr", ip])
    def authorize_firewall_privelege(self,group_name, port, protocol):
        previous_ip = get_previous_ip()    
        ip = get_my_current_ip()
        if previous_ip is not None:
            revoke_firewall_privelege(group_name, port, protocol, previous_ip)        
        self.cp_utils.spawn_child_process(["aws", "ec2", "authorize-security-group-ingress", "--group-name", group_name, "--protocol", protocol, "--port", port, "--cidr", ip])
    def get_my_current_ip(self):
        return urllib.request.urlopen("http://checkip.amazonaws.com").read().decode("utf-8").rstrip("\r\n") + "/32"
    def log_current_ip(self):
        with open(previous_ip_location, "w+") as f:
            f.write(get_my_current_ip())
    def get_previous_ip(self):
        try:
            lines = list(open(previous_ip_location))
            return lines[0]
        except File_not_found_error:
            return None

if __name__ == "__main__":
    print("Current ip: " + get_my_current_ip())
    print("Logging current ip." )
    log_current_ip()
    print("Previous ip: " + get_previous_ip())