from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, KafkaProducerEndpoint, AccountCrudViewSet,TransactionCrudViewSet,UserCrudViewSet,DocumentCruViewSet,UserRoleCrudViewSet,TransactionChangesLogRViewSet,AccountChangesLogRViewSet, UserRolesCrudViewSet,RegisterViewSet,LoginViewSet,ParseUserFromJwtTokenViewSet,LogoutViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
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
    path('user-roles/', UserRolesCrudViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-roles-list'),
    path('user-roles/<int:pk>/', UserRolesCrudViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-roles-detail'),
    path('transaction-changes-log/', TransactionChangesLogRViewSet.as_view({'get': 'list'}), name='transaction-changes-log-list'),
    path('transaction-changes-log/<int:pk>/', TransactionChangesLogRViewSet.as_view({'get': 'retrieve'}), name='transaction-changes-log-detail'),
    path('account-changes-log/', AccountChangesLogRViewSet.as_view({'get': 'list'}), name='account-changes-log-list'),
    path('account-changes-log/<int:pk>/', AccountChangesLogRViewSet.as_view({'get': 'retrieve'}), name='account-changes-log-detail'),
    path('auth/register',RegisterViewSet.as_view({'post': 'create'}),name='register-list'),
    path('auth/login', LoginViewSet.as_view(), name='login'),
    path('auth/logout', LogoutViewSet.as_view(), name='logout'),
    path('auth/get-user', ParseUserFromJwtTokenViewSet.as_view(), name='get-user'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
