from kafka import KafkaConsumer
import json

print("Attepmting to connect to the client")
consumer = KafkaConsumer("iot-queue2", value_deserializer=lambda m: json.loads(m.decode('ascii')), group_id=None, bootstrap_servers=["52.70.166.27:9092"], auto_offset_reset='earliest', enable_auto_commit=True)
for message in consumer:
    print("message found")
    print("message: " + str(message.value))