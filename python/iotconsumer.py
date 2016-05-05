from kafka import KafkaClient, SimpleConsumer
 
 
kafka_client = KafkaClient("52.70.166.27:9092")
consumer = SimpleConsumer(kafka_client, b"DISCRIMINATOR", b"my_topic")
 
# Start at a specic offset
# consumer.seek(25, 0)
 
for message in consumer:
    print(message)