#alternative to kafka-python is pykafka
from kafka import KafkaProducer, KafkaClient
import datetime
import time
import json

#Example : http://www.giantflyingsaucer.com/blog/?p=5541
class IotProducer:
    def __init__(self, kafka_ip_ports):
        print("init: " + kafka_ip_ports)
        self.kafka_ip_ports = kafka_ip_ports
        print("set ports")
        self.producer = KafkaProducer(bootstrap_servers=[kafka_ip_ports], value_serializer=lambda m: json.dumps(m).encode('ascii'))
        #self.producer = KafkaProducer(bootstrap_servers=[kafka_ip_ports])
        print("created producer")
    def enqueue(self, x):
        m = {'hello' : 'world'}
        try:
            print("attempting enqueue")
            self.producer.send('iot-queue2', m)
            print("enqueue succeeded")
        except:
            print("exception")
            time.sleep(1)
            self.producer.send('iot-queue2', m)
            print("enqueue succeeded")
    def close(self):
        print("shutting down")
        self.producer.close()

if __name__ == "__main__":
    producer = IotProducer("52.70.166.27:9092")
    for x in range (0,10):
        producer.enqueue(x)
        time.sleep(15)
    producer.close()