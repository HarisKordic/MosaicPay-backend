from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, KafkaProducerEndpoint, AccountCrudViewSet,TransactionCrudViewSet,UserCrudViewSet,DocumentCruViewSet,UserRoleCrudViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'test', TestViewSet, basename='test')

schema_view = get_schema_view(
    openapi.Info(
        title="MosaicPay API",
        default_version='v1',
        description="Bringing together different elements of fintech, such as accounts, transactions, and documents, to provide comprehensive payment solutions.",
        contact=openapi.Contact(email="kordicharis18@gmail.com"),
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('kafka-test-post/', KafkaProducerEndpoint.as_view(), name='kafka-test-post'),
    path('account/', AccountCrudViewSet.as_view({'get': 'list', 'post': 'create'}), name='account-list'),
    path('account/<int:pk>/', AccountCrudViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='transaction-detail'),
    path('transaction/', TransactionCrudViewSet.as_view({'get': 'list', 'post': 'create'}), name='transaction-list'),
    path('transaction/<int:pk>/', TransactionCrudViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='transaction-detail'),
    path('user/', UserCrudViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('user/<int:pk>/', UserCrudViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('document/', DocumentCruViewSet.as_view({'get': 'list', 'post': 'create'}), name='document-list'),
    path('document/<int:pk>/', DocumentCruViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='document-detail'),
    path('user-role/', UserRoleCrudViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-role-list'),
    path('user-role/<int:pk>/', UserRoleCrudViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-role-detail'),
    path('swagger/', include(router.urls)),
]
