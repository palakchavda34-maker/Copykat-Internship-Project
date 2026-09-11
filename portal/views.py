from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.generics import (
    GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    RetrieveAPIView, UpdateAPIView
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from decimal import Decimal, InvalidOperation

from .models import Student, Company, Internship, Application
from .serializers import (
    StudentSerializer, StudentRegisterSerializer, StudentLoginSerializer,
    CompanySerializer, CompanyRegisterSerializer, CompanyLoginSerializer,
    InternshipSerializer,
    ApplicationSerializer, ApplicationStatusSerializer,
    StudentDashboardSerializer, CompanyDashboardSerializer,
    CompanyApprovalSerializer
)


def generate_jwt_tokens(user_id, role, email):
    """Generate JWT tokens for authenticated users."""
    refresh = RefreshToken()
    refresh['user_id'] = user_id
    refresh['role'] = role
    refresh['email'] = email

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ==========================================
# FRONTEND TEMPLATE VIEWS
# ==========================================
def home(request):
    return render(request, 'index.html')

def student_login_page(request):
    return render(request, 'student_login.html')

def student_register_page(request):
    return render(request, 'student_register.html')

def student_dashboard_page(request):
    return render(request, 'student_dashboard.html')

def company_login_page(request):
    return render(request, 'company_login.html')

def company_register_page(request):
    return render(request, 'company_register.html')

def company_dashboard_page(request):
    return render(request, 'company_dashboard.html')

def internships_page(request):
    return render(request, 'internships.html')

def internship_detail_page(request, pk):
    return render(request, 'internship_detail.html', {'pk': pk})


# ==========================================
# SYSTEM / HEALTH CHECKS
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for monitoring and readiness probes."""
    return Response({
        "status": "online",
        "message": "Internship Portal API is running smoothly!"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def dummy_data_overview(request):
    """Return a dashboard-style summary for development and seed data overviews."""
    students = Student.objects.all().values('id', 'name', 'email', 'college')
    companies = Company.objects.all().values('id', 'company_name', 'email', 'location', 'approved')
    internships = Internship.objects.all().values('id', 'title', 'company__company_name', 'location', 'stipend')
    applications = Application.objects.all().values('id', 'student__name', 'internship__title', 'status')

    return Response({
        "summary": {
            "total_students": len(students),
            "total_companies": len(companies),
            "total_internships": len(internships),
            "total_applications": len(applications),
        },
        "students": list(students),
        "companies": list(companies),
        "internships": list(internships),
        "applications": list(applications),
    }, status=status.HTTP_200_OK)


# ==========================================
# STUDENT ENDPOINTS
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])
def student_register(request):
    serializer = StudentRegisterSerializer(data=request.data)
    if serializer.is_valid():
        student = serializer.save()
        tokens = generate_jwt_tokens(student.id, 'student', student.email)
        return Response({
            "message": "Student registered successfully!",
            "student": StudentSerializer(student).data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLoginAPIView(GenericAPIView):
    """Student login endpoint using JWT token generation."""
    serializer_class = StudentLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            if 'non_field_errors' in serializer.errors:
                return Response(
                    {"error": serializer.errors['non_field_errors'][0]},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        student = serializer.validated_data['student']
        tokens = generate_jwt_tokens(student.id, 'student', student.email)
        return Response({
            "message": "Student logged in successfully!",
            "student": StudentSerializer(student).data,
            "tokens": tokens
        }, status=status.HTTP_200_OK)


class StudentListCreateAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'college']
    ordering_fields = ['name', 'email', 'college']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentRegisterSerializer
        return StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            StudentSerializer(student).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


# ==========================================
# COMPANY ENDPOINTS
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])
def company_register(request):
    serializer = CompanyRegisterSerializer(data=request.data)
    if serializer.is_valid():
        company = serializer.save()
        tokens = generate_jwt_tokens(company.id, 'company', company.email)
        return Response({
            "message": "Company registered successfully! Account is pending admin approval.",
            "company": CompanySerializer(company).data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyListCreateAPIView(ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['company_name', 'email', 'location']
    ordering_fields = ['company_name', 'email', 'location', 'approved']
    ordering = ['company_name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyRegisterSerializer
        return CompanySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            CompanySerializer(company).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CompanyLoginAPIView(GenericAPIView):
    serializer_class = CompanyLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            if 'non_field_errors' in serializer.errors:
                return Response(
                    {"error": serializer.errors['non_field_errors'][0]},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        company = serializer.validated_data['company']
        if not company.approved:
            return Response({
                "warning": "Account pending approval.",
                "approved": False,
                "message": "Your company account has not been approved by Admin yet.",
                "company": CompanySerializer(company).data,
            }, status=status.HTTP_403_FORBIDDEN)

        tokens = generate_jwt_tokens(company.id, 'company', company.email)
        return Response({
            "message": "Company logged in successfully!",
            "company": CompanySerializer(company).data,
            "tokens": tokens
        }, status=status.HTTP_200_OK)


class AdminCompanyListAPIView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['company_name', 'email', 'location']
    ordering_fields = ['company_name', 'location', 'approved']
    ordering = ['company_name']


class AdminCompanyApprovalAPIView(UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyApprovalSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch', 'put']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        company = self.get_object()
        serializer = self.get_serializer(company, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        status_text = "approved" if serializer.instance.approved else "rejected"
        return Response({
            "message": f"Company '{serializer.instance.company_name}' has been {status_text}.",
            "company": CompanySerializer(serializer.instance).data
        }, status=status.HTTP_200_OK)


# ==========================================
# INTERNSHIP ENDPOINTS
# ==========================================

class InternshipListCreateAPIView(ListCreateAPIView):
    queryset = Internship.objects.all().order_by('-created_at')
    serializer_class = InternshipSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'company__company_name', 'location']
    ordering_fields = ['stipend', 'created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)

        min_stipend = self.request.query_params.get('min_stipend')
        max_stipend = self.request.query_params.get('max_stipend')

        if min_stipend is not None:
            try:
                queryset = queryset.filter(stipend__gte=Decimal(min_stipend))
            except (InvalidOperation, ValueError):
                raise ValidationError({'min_stipend': 'Enter a valid decimal value.'})

        if max_stipend is not None:
            try:
                queryset = queryset.filter(stipend__lte=Decimal(max_stipend))
            except (InvalidOperation, ValueError):
                raise ValidationError({'max_stipend': 'Enter a valid decimal value.'})

        return queryset


class InternshipRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [AllowAny]


# ==========================================
# APPLICATION ENDPOINTS
# ==========================================

class ApplicationListCreateAPIView(ListCreateAPIView):
    queryset = Application.objects.all().order_by('-applied_on')
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['student__name', 'student__email', 'internship__title', 'internship__company__company_name']
    ordering_fields = ['applied_on', 'status']
    ordering = ['-applied_on']

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        internship_id = self.request.query_params.get('internship_id')
        company_id = self.request.query_params.get('company_id')
        status_param = self.request.query_params.get('status')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if internship_id:
            queryset = queryset.filter(internship_id=internship_id)
        if company_id:
            queryset = queryset.filter(internship__company_id=company_id)
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        return queryset


class ApplicationRetrieveAPIView(RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]


class CompanyApplicationListAPIView(ListAPIView):
    queryset = Application.objects.all().order_by('-applied_on')
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['student__name', 'student__email', 'internship__title']
    ordering_fields = ['applied_on', 'status']
    ordering = ['-applied_on']

    def list(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response(
                {"detail": "company_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company_id')
        status_param = self.request.query_params.get('status')
        if company_id:
            queryset = queryset.filter(internship__company_id=company_id)
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
        return queryset


class StudentDashboardAPIView(GenericAPIView):
    serializer_class = StudentDashboardSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {"detail": "student_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        applications = Application.objects.filter(student=student)
        data = {
            "total_internships_applied": applications.count(),
            "pending_applications": applications.filter(status='Pending').count(),
            "accepted_applications": applications.filter(status='Accepted').count(),
            "rejected_applications": applications.filter(status='Rejected').count(),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyDashboardAPIView(GenericAPIView):
    serializer_class = CompanyDashboardSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response(
                {"detail": "company_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return Response({"detail": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        internships = Internship.objects.filter(company=company)
        applications = Application.objects.filter(internship__company=company)
        data = {
            "total_internships_posted": internships.count(),
            "total_applications_received": applications.count(),
            "pending_applications": applications.filter(status='Pending').count(),
            "accepted_applications": applications.filter(status='Accepted').count(),
            "rejected_applications": applications.filter(status='Rejected').count(),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationStatusUpdateAPIView(UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": f"Application status updated to '{serializer.instance.status}'.",
            "application": ApplicationSerializer(serializer.instance).data
        }, status=status.HTTP_200_OK)


# ==========================================
# ADMIN MANAGEMENT & APPROVAL ENDPOINTS
# ==========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def admin_stats(request):
    """
    GET /api/admin/stats/
    Returns high-level statistics for Admin Dashboard.
    """
    return Response({
        "total_students": Student.objects.count(),
        "total_companies": Company.objects.count(),
        "approved_companies": Company.objects.filter(approved=True).count(),
        "pending_companies": Company.objects.filter(approved=False).count(),
        "total_internships": Internship.objects.count(),
        "total_applications": Application.objects.count(),
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny])
def admin_reject_company(request, pk):
    """
    PUT /api/admin/companies/{id}/reject/
    Rejects or revokes approval for a company account.
    """
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

    company.approved = False
    company.save()

    return Response({
        "message": f"Company '{company.company_name}' approval has been rejected/revoked.",
        "company": CompanySerializer(company).data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def admin_delete_student(request, pk):
    """
    DELETE /api/admin/students/{id}/
    Deletes a student account and cascading data.
    """
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    name = student.name
    student.delete()

    return Response({
        "message": f"Student '{name}' (ID: {pk}) deleted successfully."
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def admin_delete_company(request, pk):
    """
    DELETE /api/admin/companies/{id}/
    Deletes a company account and cascading internships/applications.
    """
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

    name = company.company_name
    company.delete()

    return Response({
        "message": f"Company '{name}' (ID: {pk}) deleted successfully."
    }, status=status.HTTP_200_OK)
