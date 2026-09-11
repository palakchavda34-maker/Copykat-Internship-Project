from django.contrib import admin
from django.urls import path, include
from portal.views import (
    home, student_login_page, student_register_page, student_dashboard_page,
    company_login_page, company_register_page, company_dashboard_page,
    internships_page, internship_detail_page
)

urlpatterns = [
    # Frontend Template Routes
    path('', home, name='home'),
    path('student/login/', student_login_page, name='student_login_page'),
    path('student/register/', student_register_page, name='student_register_page'),
    path('student/dashboard/', student_dashboard_page, name='student_dashboard_page'),
    
    path('company/login/', company_login_page, name='company_login_page'),
    path('company/register/', company_register_page, name='company_register_page'),
    path('company/dashboard/', company_dashboard_page, name='company_dashboard_page'),

    path('internships/', internships_page, name='internships_page'),
    path('internships/<int:pk>/', internship_detail_page, name='internship_detail_page'),

    # Admin & Backend REST API Routes
    path('admin/', admin.site.urls),
    path('api/', include('portal.urls')),
]
