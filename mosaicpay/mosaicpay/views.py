from rest_framework import viewsets
from .models import Test
from .serializers import TestSerializer,send_message_to_topic,KafkaProducerSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class KafkaProducerEndpoint(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'topic_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['message', 'topic_name'],
        ),
        operation_description="Send a message to a Kafka topic.",
    )
    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        topic_name = request.data.get('topic_name')
        send_message_to_topic(topic_name, message)
        return Response({"message": "Kafka message produced."})
