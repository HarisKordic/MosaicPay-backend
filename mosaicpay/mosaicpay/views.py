from rest_framework import viewsets,status
from .models import Test,Account,Transaction,User,Document,UserRole
from .serializers import TestSerializer,send_message_to_topic,AccountSerializer,AccountSerializerUpdate,TransactionSerializer,TransactionSerializerUpdate,UserSerializer,UserSerializerUpdate,DocumentSerializer,DocumentSerializerUpdate,UserRoleSerializer,UserRoleSerializerUpdate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# TEST
class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

# KAFKA PROCUCER TEST
class KafkaProducerEndpoint(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_OBJECT),
                'topic_name': openapi.Schema(type=openapi.TYPE_STRING),
                'key': openapi.Schema(type=openapi.TYPE_STRING),

            },
            required=['message', 'topic_name'],
        ),
        operation_description="Send a message to a Kafka topic.",
    )
    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        topic_name = request.data.get('topic_name')
        key = request.data.get('key')
        send_message_to_topic(topic_name, message,key=key)
        return Response({"message": "Kafka message produced."})

#ACCOUNT CRUD
class AccountCrudViewSet(viewsets.ModelViewSet):
    account_created_topic_counter=0
    account_deleted_topic_counter=0
    account_updated_topic_counter=0

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        if AccountCrudViewSet.account_created_topic_counter==0:
           send_message_to_topic("account_created", "CREATED AAAAAAAAAAAA")
           AccountCrudViewSet.account_created_topic_counter+=1
        else:
            send_message_to_topic("account_created", "CREATED AAAAAAAAAAAA",is_initial=False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if AccountCrudViewSet.account_updated_topic_counter==0:
           send_message_to_topic("account_updated", "UPDATED AAAAAAAAAAAA")
           AccountCrudViewSet.account_updated_topic_counter+=1
        else:
            send_message_to_topic("account_updated", "UPDATED AAAAAAAAAAAA",is_initial=False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if AccountCrudViewSet.account_deleted_topic_counter==0:
           send_message_to_topic("account_deleted", "DELETED AAAAAAAAAAAA")
           AccountCrudViewSet.account_deleted_topic_counter+=1
        else:
            send_message_to_topic("account_deleted", "DELETED AAAAAAAAAAAA",is_initial=False)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return AccountSerializerUpdate
        return AccountSerializer

#TRANSACTION CRUD
class TransactionCrudViewSet(viewsets.ModelViewSet):
    transaction_created_topic_counter=0
    transaction_deleted_topic_counter=0
    transaction_updated_topic_counter=0
    transaction_state_changed_topic_counter=0


    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):

        if TransactionCrudViewSet.transaction_created_topic_counter==0:
           send_message_to_topic("transaction_created", "CREATED AAAAAAAAAAAA")
           TransactionCrudViewSet.transaction_created_topic_counter+=1
        else: 
           send_message_to_topic("transaction_created", "CREATED AAAAAAAAAAAA",is_initial=False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if TransactionCrudViewSet.transaction_updated_topic_counter==0:
           send_message_to_topic("transaction_updated", "UPDATED AAAAAAAAAAAA")
           TransactionCrudViewSet.transaction_updated_topic_counter+=1
        if TransactionCrudViewSet.transaction_state_changed_topic_counter==0:
             send_message_to_topic("transaction_state_changed", "UPDATED AAAAAAAAAAAA")
             TransactionCrudViewSet.transaction_state_changed_topic_counter+=1
        else: 
           send_message_to_topic("transaction_updated", "UPDATED AAAAAAAAAAAA",is_initial=False)
           send_message_to_topic("transaction_state_changed", "UPDATED AAAAAAAAAAAA",is_initial=False)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if TransactionCrudViewSet.transaction_deleted_topic_counter==0:
           send_message_to_topic("transaction_deleted", "DELETED AAAAAAAAAAAA")
           TransactionCrudViewSet.transaction_deleted_topic_counter+=1
        else:
            send_message_to_topic("transaction_deleted", "DELETED AAAAAAAAAAAA",is_initial=False)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return TransactionSerializerUpdate
        return TransactionSerializer

#USER CRUD
class UserCrudViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserSerializerUpdate
        return UserSerializer

#DOCUMENT CRU
class DocumentCruViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return DocumentSerializerUpdate
        return DocumentSerializer


#USER ROLES CRUD
class UserRoleCrudViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserRoleSerializerUpdate
        return UserRoleSerializer