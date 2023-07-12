from rest_framework import viewsets,status
from .models import Test,Account,Transaction,User,Document,UserRole,TransactionChangesLog,AccountChangesLog,UserRoleUser
from .serializers import TestSerializer,send_message_to_topic,AccountSerializer,AccountSerializerUpdate,TransactionSerializer,TransactionSerializerUpdate,UserSerializer,UserSerializerUpdate,DocumentSerializer,DocumentSerializerUpdate,UserRoleSerializer,UserRoleSerializerUpdate,TransactionChangesLogSerializer ,AccountChangesLogSerializer,UserRolesSerializer,UserRolesSerializerUpdate,UserSerializerRegister
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date,timedelta,datetime
import json
from .helper import convertAccountToJson,convertTransactionToJson,get_partition_key
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from custom_auth import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db.models import Subquery
#REGISTER

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerRegister
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user=User.objects.get(email=serializer.data['email'])
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)


#LOGIN
class LoginViewSet(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),

            },
            required=['email', 'password'],
        ),
        
        operation_description="Login and gain JWT token."
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response('User not found!',status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response('Incorrect password!',status=status.HTTP_401_UNAUTHORIZED)
        
        payload={
            "id":user.user_id,
            "exp":datetime.utcnow().__add__(timedelta(days=30)),
            "iat":datetime.utcnow()
        }
        headers={
        "typ": "JWT",
        "alg": "HS256"
        }

        token=jwt.encode(payload=payload,key='secret',algorithm='HS256',headers=headers)

        response=Response()
        response.set_cookie(key='token', value=token, httponly=False, samesite='None', domain='localhost', path='/')
        response.data={"token":token}
        response.status=status.HTTP_200_OK
        return response

#PARSE USER FROM TOKEN
class ParseUserFromJwtTokenViewSet(APIView):
    def get(self, request):
       token= request.COOKIES.get('token')

       if not token:
           raise AuthenticationFailed('Unauthenticated!')
       try:
           payload=jwt.decode(token,'secret',algorithms=['HS256'])
       except jwt.ExpiredSignatureError:
           raise AuthenticationFailed('Unauthenticated!')
       
       user=User.objects.get(user_id=payload['id'])
       serializer=UserSerializer(user)
       return Response(serializer.data)
    authentication_classes = [JWTAuthentication]

# LOGOUT

class LogoutViewSet(APIView):
    def post(self, request):

        response=Response()
        response.delete_cookie('token')
        response.data='Logout successfull!'
        response.status=status.HTTP_200_OK
        return response
    authentication_classes = [JWTAuthentication]

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

    serializer_class = AccountSerializer

    def get_queryset(self):
        parse_user_view = ParseUserFromJwtTokenViewSet()
        parse_user_response = parse_user_view.get(self.request)

        if parse_user_response.status_code != 200:
            return parse_user_response

        user_data = parse_user_response.data
        user_id = user_data['user_id']
        queryset = Account.objects.filter(user_id=user_id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        key = get_partition_key(serializer.instance.account_id)
        if AccountCrudViewSet.account_created_topic_counter==0:
           send_message_to_topic("account_created", json.loads(json.dumps(convertAccountToJson(serializer.instance))), key)
           AccountCrudViewSet.account_created_topic_counter+=1
        else:
            send_message_to_topic("account_created",  json.loads(json.dumps(convertAccountToJson(serializer.instance))), key, is_initial=False)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        key = get_partition_key(self.get_object().account_id)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if AccountCrudViewSet.account_updated_topic_counter==0:
           send_message_to_topic("account_updated", convertAccountToJson(self.get_object()), key)
           AccountCrudViewSet.account_updated_topic_counter+=1
        else:
            send_message_to_topic("account_updated",convertAccountToJson(self.get_object()), key, is_initial=False)

        #Logging
        changeData = {
            'change_type':  json.dumps(convertAccountToJson(self.get_object())),
            'change_date': date.today(),
            'changed_by_user': self.get_object().user.user_id, # TODO: retrieve user
            'account': self.get_object().account_id
        }

        logSerializer = AccountChangesLogSerializer(data=changeData)
        logSerializer.is_valid(raise_exception=True)
        logSerializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        key = get_partition_key(self.get_object().account_id)
        #Logging
        changeData = {
            'change_type':  json.dumps(convertAccountToJson(self.get_object())),
            'change_date': date.today(),
            'changed_by_user': self.get_object().user.user_id,
            'account': self.get_object().account_id
        }

        logSerializer = AccountChangesLogSerializer(data=changeData)
        logSerializer.is_valid(raise_exception=True)
        logSerializer.save()

        if AccountCrudViewSet.account_deleted_topic_counter==0:
           send_message_to_topic("account_deleted", convertAccountToJson(self.get_object()), key)
           AccountCrudViewSet.account_deleted_topic_counter+=1
        else:
            send_message_to_topic("account_deleted", convertAccountToJson(self.get_object()), key, is_initial=False)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return AccountSerializerUpdate
        return AccountSerializer
    authentication_classes = [JWTAuthentication]


#TRANSACTION CRUD
class TransactionCrudViewSet(viewsets.ModelViewSet):
    transaction_created_topic_counter=0
    transaction_deleted_topic_counter=0
    transaction_updated_topic_counter=0
    transaction_state_changed_topic_counter=0


    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    
    def list(self, request, *args, **kwargs):
        parse_user_view = ParseUserFromJwtTokenViewSet()
        parse_user_response = parse_user_view.get(request)

        if parse_user_response.status_code != 200:
            return parse_user_response

        user_data = parse_user_response.data
        user_id = user_data['user_id']
        
        account_ids = Account.objects.filter(user_id=user_id).values_list('account_id', flat=True)
        # Retrieve the account IDs for the given user and convert the result to a flat list

        queryset = Transaction.objects.filter(account_id__in=account_ids)
        # Filter transactions based on the retrieved account IDs
        serializer = TransactionSerializer(queryset, many=True)
        data = serializer.data

        for i, transaction_data in enumerate(data):
            account_data = queryset[i].account
            account_serializer = AccountSerializer(account_data)
            transaction_data['account'] = account_serializer.data
            document=Document.objects.get(account_id=account_data.account_id)
            document_serializer=DocumentSerializer(document)
            transaction_data['document']=document_serializer.data

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TransactionSerializer(instance)
        data = serializer.data

        account_data = instance.account
        account_serializer = AccountSerializer(account_data)
        data['account'] = account_serializer.data

        return Response(data)
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        key = get_partition_key(serializer.instance.transaction_id)
        if TransactionCrudViewSet.transaction_created_topic_counter==0:
           send_message_to_topic("transaction_created", json.loads(json.dumps(convertTransactionToJson(serializer.instance))), key)
           TransactionCrudViewSet.transaction_created_topic_counter+=1
        else: 
           send_message_to_topic("transaction_created", json.loads(json.dumps(convertTransactionToJson(serializer.instance))), key, is_initial=False)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        key = get_partition_key(self.get_object().transaction_id)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_transaction_state = instance.transaction_state  # Store the old transaction_state
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        new_transaction_state = self.get_object().transaction_state  # Get the new transaction_state
        transaction_state_changed = old_transaction_state != new_transaction_state
        
        if TransactionCrudViewSet.transaction_updated_topic_counter==0:
           send_message_to_topic("transaction_updated",convertTransactionToJson(self.get_object()),key)
           TransactionCrudViewSet.transaction_updated_topic_counter+=1
        else: 
           send_message_to_topic("transaction_updated", convertTransactionToJson(self.get_object()), key, is_initial=False)

        if TransactionCrudViewSet.transaction_state_changed_topic_counter==0 and transaction_state_changed==True:
             send_message_to_topic("transaction_state_changed", convertTransactionToJson(self.get_object()),key)
             TransactionCrudViewSet.transaction_state_changed_topic_counter+=1

        elif TransactionCrudViewSet.transaction_state_changed_topic_counter>=1 and transaction_state_changed==True:
             send_message_to_topic("transaction_state_changed", convertTransactionToJson(self.get_object()), key, is_initial=False)

        #Logging
        changeData = {
            'change_type':  json.dumps(convertTransactionToJson(self.get_object())),
            'change_date': date.today(),
            'changed_by_user': User.objects.get(user_id=1).user_id, # TODO: retrieve user
            'transaction': self.get_object().transaction_id
        }

        logSerializer = TransactionChangesLogSerializer(data=changeData)
        logSerializer.is_valid(raise_exception=True)
        logSerializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        key = get_partition_key(self.get_object().transaction_id)

        #Logging
        changeData = {
            'change_type':  json.dumps(convertTransactionToJson(self.get_object())),
            'change_date': date.today(),
            'changed_by_user': User.objects.get(user_id=1).user_id, # TODO: retrieve user
            'transaction': self.get_object().transaction_id
        }

        logSerializer = TransactionChangesLogSerializer(data=changeData)
        logSerializer.is_valid(raise_exception=True)
        logSerializer.save()

        if TransactionCrudViewSet.transaction_deleted_topic_counter==0:
           send_message_to_topic("transaction_deleted", convertTransactionToJson(self.get_object()), key)
           TransactionCrudViewSet.transaction_deleted_topic_counter+=1
        else:
            send_message_to_topic("transaction_deleted", convertTransactionToJson(self.get_object()), key, is_initial=False)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return TransactionSerializerUpdate
        return TransactionSerializer
    #authentication_classes = [JWTAuthentication]

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
        account_id = kwargs.get('pk')
        instance = Document.objects.get(account_id=account_id)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    authentication_classes = [JWTAuthentication]


#USER ROLE CRUD
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
    authentication_classes = [JWTAuthentication]
    

#USER ROLES CRUD
class UserRolesCrudViewSet(viewsets.ModelViewSet):
    queryset = UserRoleUser.objects.all()
    serializer_class = UserRolesSerializer
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
            return UserRolesSerializerUpdate
        return UserRolesSerializer
    authentication_classes = [JWTAuthentication]

#TRANSACTION CHANGES LOG R
class TransactionChangesLogRViewSet(viewsets.ModelViewSet):
    queryset = TransactionChangesLog.objects.all()
    serializer_class = TransactionChangesLogSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


#ACCOUNT CHANGES LOG R
class AccountChangesLogRViewSet(viewsets.ModelViewSet):
    queryset = AccountChangesLog.objects.all()
    serializer_class = AccountChangesLogSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)