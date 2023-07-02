from rest_framework import viewsets
from .models import Test
from .serializers import TestSerializer

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
