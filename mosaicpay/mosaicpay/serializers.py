from rest_framework import serializers
from .models import Test,Account,Transaction,User,Document,UserRole,TransactionChangesLog,AccountChangesLog,UserRoleUser
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
    
    partition=0
    if key=="partition_1":
        partition=1
    value = json.dumps(message).encode('utf-8')
    producer.produce(topic_name, value=value, key=key, partition=partition)
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
        fields = ('user_id','first_name', 'last_name', 'email','birthday')
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','birthday')

class UserSerializerRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs={
            'password': {'write_only':True}
        }
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
# DOCUMENT SERIALIZER

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
class DocumentSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('url','document_id')

# USER ROLE SERIALIZER

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
class UserRoleSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('user_role_id', 'name')

# USER ROLES SERIALIZER

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleUser
        fields = '__all__'
class UserRolesSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = UserRoleUser
        fields = ('user_role',)

# TRANSACTION CHANGES LOG SERIALIZER
class TransactionChangesLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionChangesLog
        fields = '__all__'

# ACCOUNT CHANGES LOG SERIALIZER
class AccountChangesLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountChangesLog
        fields = '__all__'


