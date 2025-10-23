from rest_framework import generics, permissions, serializers
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema

# Custom permission: Admin or read-only
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# Admin-only JWT serializer
class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_staff:
            raise serializers.ValidationError("Only admin are allowed to log in.")
        return data

# Admin JWT login view
@extend_schema(
    tags=["Admin"],
    summary="Admin Login (JWT Token)",
    description="Allows only admin to log in and obtain JWT access & refresh tokens."
)
class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

# Department list & create
@extend_schema(
    tags=["Admin"],
    summary="List & Create Departments",
    description="Admins can create new departments. Anyone can view the list of departments."
)
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]

# Employee list & create
@extend_schema(
    tags=["Employees"],
    summary="List & Create Employees",
    description="Only admin users can create employees. Returns a list of all employees."
)
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]

# Retrieve a specific employee by UUID
@extend_schema(
    tags=["Employees"],
    summary="Retrieve Employee",
    description="Only admin users can view specific employee details by UUID."
)
class EmployeeRetrieveView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

# Update a specific employee by UUID
@extend_schema(
    tags=["Employees"],
    summary="Update Employee",
    description="Update a specific employee by UUID. Admin only."
)
class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

# Delete a specific employee by UUID
@extend_schema(
    tags=["Employees"],
    summary="Delete Employee",
    description="Delete a specific employee by UUID. Admin only."
)
class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
