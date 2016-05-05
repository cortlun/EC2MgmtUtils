#alternative to kafka-python is pykafka
from kafka import SimpleProducer, KafkaClient

#Example : http://www.giantflyingsaucer.com/blog/?p=5541
class IotProducer:
	def __init__(self, kafka_ip_ports):
		self.kafka_client_string = kafka_ip_ports[0]
		init_flag = 0
		for ip_port in kafka_ip_ports:
			if init_flag == 1:
				kafka_client_string = kafka_client_string + ip_port
			else: 
				init_flag = 1
		self.kafka_client = KafkaClient(self.kafka_client_string)