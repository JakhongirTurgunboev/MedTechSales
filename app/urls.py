from rest_framework import routers, permissions
from django.urls import path, include
from .views import EmployeeViewSet, ClientViewSet, ProductViewSet, OrderViewSet, EmployeeStatisticsViewSet, \
    EmployeeStatisticsSummaryViewSet, ClientStatisticsViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="MedTech API",
      default_version='v1',
      description="MedTech sales API",
      license=openapi.License(name="The MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('statistics/employee/<int:id>/', EmployeeStatisticsViewSet.as_view({'get': 'list'}), name='employee-statistics'),
    path('employee/statistics/', EmployeeStatisticsSummaryViewSet.as_view({'get': 'list'}), name='employee-statistics-summary'),
    path('statistics/client/<int:id>/', ClientStatisticsViewSet.as_view({'get': 'list'}), name='client-statistics'),
]
