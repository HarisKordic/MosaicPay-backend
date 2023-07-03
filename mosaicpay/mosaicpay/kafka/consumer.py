from kafka import KafkaConsumer

TOPIC_NAME='test_topic'

consumer=KafkaConsumer(TOPIC_NAME)
for message in consumer:
    print(message)