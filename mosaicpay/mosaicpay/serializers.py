from rest_framework import serializers
from .models import Test,Account,Transaction,User,Document,UserRole,TransactionChangesLog
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from django.conf import settings
import json
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


def create_kafka_topic(topic_name, num_partitions=2, replication_factor=1):
    admin_client = AdminClient({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})
    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )
    topic.config = {
        'cleanup.policy': 'compact', 
        'retention.ms': '86400000' #24 hours retention
    }
    admin_client.create_topics([topic])


def send_message_to_topic(topic_name, message, key, is_initial=True):
    if is_initial==True:
        create_kafka_topic(topic_name=topic_name)
    
    producer = Producer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS
    })
    
    if key==None:
        key="default_key"
    value = json.dumps(message).encode('utf-8')
    producer.produce(topic_name, value=value, key=key)
    producer.flush()


class KafkaMessageSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.DictField()

class KafkaProducerSerializer(serializers.Serializer):
    message = KafkaMessageSerializer()
    topic_name = serializers.CharField()
    key=serializers.CharField()


# ACCOUNT SERIALIZER

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class AccountSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'balance')

# TRANSACTION SERIALIZER

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
class TransactionSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('type', 'amount','transaction_state')

# USER SERIALIZER

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','birthday')

# DOCUMENT SERIALIZER

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
class DocumentSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('url','document_id')

# USER ROLES SERIALIZER

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
class UserRoleSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('user_role_id', 'name')

# TRANSACTION CHANGES LOG SERIALIZER
class TransactionChangesLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionChangesLog
        fields = '__all__'

