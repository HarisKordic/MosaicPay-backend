from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TestViewSet,KafkaProducerEndpoint

schema_view = get_schema_view(
    openapi.Info(
        title="MosaicPay API",
        default_version='v1',
        description="Bringing together different elements of fintech, such as accounts, transactions, and documents, to provide comprehensive payment solutions.",
        contact=openapi.Contact(email="kordicharis18@gmail.com"),
    ),
    public=True,
)
router = DefaultRouter()
router.register(r'test', TestViewSet, basename='test')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', include(router.urls)),
    path('kafka-test-post/', KafkaProducerEndpoint.as_view(), name='kafka-test-post'),
]
