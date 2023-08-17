from kafka import KafkaProducer

TOPIC_NAME='test_topic'

KAFKA_SERVER='localhost:9092'

producer=KafkaProducer(bootstrap_servers=KAFKA_SERVER)

producer.send(TOPIC_NAME,b'Hi this is a test')
producer.flush()