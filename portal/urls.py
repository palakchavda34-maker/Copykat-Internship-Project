from django.urls import path
from .views import (
    health_check, dummy_data_overview,
    student_register, StudentLoginAPIView, StudentListCreateAPIView,
    company_register, CompanyLoginAPIView, CompanyListCreateAPIView,
    InternshipListCreateAPIView, InternshipRetrieveUpdateDestroyAPIView,
    ApplicationListCreateAPIView, ApplicationRetrieveAPIView,
    CompanyApplicationListAPIView, ApplicationStatusUpdateAPIView,
    AdminCompanyListAPIView, AdminCompanyApprovalAPIView,
    StudentDashboardAPIView, CompanyDashboardAPIView,
    admin_stats, admin_reject_company,
    admin_delete_student, admin_delete_company
)

urlpatterns = [
    path('', health_check, name='home'),
    # System endpoints
    path('health/', health_check, name='health_check'),
    path('dummy-data/', dummy_data_overview, name='dummy_data_overview'),

    # Student Endpoints
    path('students/register/', student_register, name='student_register'),
    path('students/login/', StudentLoginAPIView.as_view(), name='student_login'),
    path('students/', StudentListCreateAPIView.as_view(), name='student_list_create'),

    # Company Endpoints
    path('companies/register/', company_register, name='company_register'),
    path('companies/login/', CompanyLoginAPIView.as_view(), name='company_login'),
    path('companies/', CompanyListCreateAPIView.as_view(), name='company_list'),

    # Internship Endpoints
    path('internships/', InternshipListCreateAPIView.as_view(), name='internship_list_create'),
    path('internships/<int:pk>/', InternshipRetrieveUpdateDestroyAPIView.as_view(), name='internship_detail'),

    # Application Endpoints
    path('applications/', ApplicationListCreateAPIView.as_view(), name='application_list_create'),
    path('applications/<int:pk>/', ApplicationRetrieveAPIView.as_view(), name='application_detail'),
    path('applications/<int:pk>/status/', ApplicationStatusUpdateAPIView.as_view(), name='application_status_update'),

    # Company Dashboard Endpoints
    path('company/applications/', CompanyApplicationListAPIView.as_view(), name='company_application_list'),
    path('dashboard/student/', StudentDashboardAPIView.as_view(), name='student_dashboard'),
    path('dashboard/company/', CompanyDashboardAPIView.as_view(), name='company_dashboard'),

    # Admin Endpoints
    path('admin/stats/', admin_stats, name='admin_stats'),
    path('admin/companies/', AdminCompanyListAPIView.as_view(), name='admin_company_list'),
    path('admin/companies/<int:pk>/approve/', AdminCompanyApprovalAPIView.as_view(), name='admin_company_approval'),
    path('admin/companies/<int:pk>/reject/', admin_reject_company, name='admin_reject_company'),
    path('admin/students/<int:pk>/', admin_delete_student, name='admin_delete_student'),
    path('admin/companies/<int:pk>/', admin_delete_company, name='admin_delete_company'),
]
