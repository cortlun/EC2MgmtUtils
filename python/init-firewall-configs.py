import awsutils

class FirewallRuleConfig:
	def __init__(self, security_group_name, firewall_rule_instances)
		self.security_group_name = security_group_name
		self.firewall_rule_instances = firewall_rule_instances
		self.aws_utils = AwsUtils()
	def open_firewall(self):
		for firewall_rule_instance in self.firewall_rule_instances:
			self.aws_utils.authorize_firewall_privelege(self.security_group_name, firewall_rule_instance.port, firewall_rule_instance.protocol)

class FirewallRuleInstance:
	def __init__(self, port, protocol)
		self.ip = ip
		self.port = port
		self.protocol = protocol

if __name__ == "__main__":
	#Init FirewallRuleInstance objects
	rule_instances = []
	#shell port
	rule_instances.append(FirewallRuleInstance("22", "TCP"))
	#zookeeper port
	rule_instances.append(FirewallRuleInstance("9091", "TCP"))
	#kafka port
	rule_instances.append(FirewallRuleInstance("9092", "TCP"))
	#mongo port
	rule_instances.append(FirewallRuleInstance("9093", "TCP"))
	#web app port
	rule_instances.append(FirewallRuleInstance("9094", "TCP"))
	#add storm port if necessary
	#add nodejs port if necessary
	
	config = FirewallRuleConfig("IOT_SECURITY_GROUP")
	