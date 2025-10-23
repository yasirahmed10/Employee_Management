from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from employees.views import (
    EmployeeListCreateView,
    EmployeeRetrieveView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    DepartmentListCreateView,
    AdminTokenObtainPairView,
    
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT for Admin Login Only
    path('api/admin/login', AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Employee CRUD
    path('api/departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/<uuid:id>/', EmployeeRetrieveView.as_view(), name='employee-retrieve'),
    path('api/employees/<uuid:id>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('api/employees/<uuid:id>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

]
