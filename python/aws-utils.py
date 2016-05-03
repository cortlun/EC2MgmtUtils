from subprocess import call
import os
from os.path import expanduser
import urllib.request

userHome = expanduser("~")
iotHome = os.path.join(userHome, "")
logDirectory = os.path.join(iotHome, "logs")

previousIpLocation = os.path.join(iotHome, "lastIp.txt")

class ChildProcessUtils:
    def __init__(self, logFile):
        self.logFile = logFile
        
        
def _spawn_child_process(args):
    call(args)
    
def revoke_firewall_privelege(groupName, port, protocol, ip):
	_spawn_child_process(["aws", "ec2", "revoke-security-group-ingress", "--group-name", groupName, "--protocol", protocol, "--port", port, "--cidr", ip])
	
def authorize_firewall_privelege(groupName, port, protocol, ip):
	previousIp = get_previous_ip();
	if previousIp is not None:
		revoke_firewall_privelege(groupName, port, protocol, previousIp)		
	_spawn_child_process(["aws", "ec2", "authorize-security-group-ingress", "--group-name", groupName, "--protocol", protocol, "--port", port, "--cidr", ip])
	
def authorize_firewall_privelege(groupName, port, protocol):
	previousIp = get_previous_ip()	
	ip = get_current_ip()
	if previousIp is not None:
		revoke_firewall_privelege(groupName, port, protocol, previousIp)		
	_spawn_child_process(["aws", "ec2", "authorize-security-group-ingress", "--group-name", groupName, "--protocol", protocol, "--port", port, "--cidr", ip])

def get_current_ip():
	return urllib.request.urlopen("http://checkip.amazonaws.com").read().decode("utf-8").rstrip("\r\n") + "/32"
	
def log_current_ip():
	with open(previousIpLocation, "w+") as f:
		f.write(get_current_ip())

def get_previous_ip():
	try:
		lines = list(open(previousIpLocation))
		return lines[0]
	except FileNotFoundError:
		return None

if __name__ == "__main__":
	print("Current ip: " + get_current_ip())
	print("Logging current ip." )
	log_current_ip()
	print("Previous ip: " + get_previous_ip())