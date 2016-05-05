#alternative to kafka-python is pykafka
from kafka import SimpleProducer, KafkaClient
import datetime
import time

#Example : http://www.giantflyingsaucer.com/blog/?p=5541
class IotProducer:
    def __init__(self, kafka_ip_ports):
        print("init")
        self.kafka_ip_ports = kafka_ip_ports
        print("set ports")
        self.kafka = KafkaClient(kafka_ip_ports)
        print("opened client")
        self.producer = SimpleProducer(kafka)
        print("created producer")
        self.topic = b'DISCRIMINATOR'
        print("set topic name")
    def enqueue(self, x):
        print("count: " + str(x))
        msg = {"count": x}
        try:
            print("attempting enqueue")
            print_response(self.producer.send_messages(self.topic, msg))
            print ("enqueue succeeded")
        except LeaderNotAvailableError:
            print ("exception")
            time.sleep(1)
            print_response(self.producer.send_messages(topic, msg))
            print("enqueue succeeded")
    def close(self):
        print("shutting down")
        self.kafka.close()

if __name__ == "__main__":
    producer = IotProducer("52.70.166.27:9092")
    for x in range (0,10):
        producer.enqueue(x)
        time.sleep(15)
    producer.close()