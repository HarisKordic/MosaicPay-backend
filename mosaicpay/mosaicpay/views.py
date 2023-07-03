from rest_framework import viewsets
from .models import Test
from .serializers import TestSerializer
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    from django.shortcuts import redirect

def redirect_to_swagger(request):
     return HttpResponseRedirect('/swagger/')

