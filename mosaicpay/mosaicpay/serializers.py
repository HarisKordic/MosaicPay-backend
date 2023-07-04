from rest_framework import serializers
from .models import Test
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from django.conf import settings
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = AdminClient({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})
    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )
    admin_client.create_topics([topic])


def send_message_to_topic(topic_name, message):
    create_kafka_topic(topic_name=topic_name)
    producer = Producer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS
    })
    producer.produce(topic_name, message.encode('utf-8'))
    producer.flush()


class KafkaProducerSerializer(serializers.Serializer):
    message = serializers.CharField()
    topic_name = serializers.CharField()