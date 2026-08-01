from django.contrib import admin
from .models import Student, Company, Internship, Application


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'college')
    search_fields = ('name', 'email', 'college')
    list_filter = ('college',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'email', 'location', 'approved')
    search_fields = ('company_name', 'email', 'location')
    list_filter = ('approved', 'location')
    list_editable = ('approved',)


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location', 'stipend', 'created_at')
    search_fields = ('title', 'company__company_name', 'location')
    list_filter = ('location', 'created_at')
    list_select_related = ('company',)
    autocomplete_fields = ('company',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'internship', 'status', 'applied_on')
    search_fields = ('student__name', 'student__email', 'internship__title', 'internship__company__company_name')
    list_filter = ('status', 'applied_on', 'internship__company__company_name')
    list_select_related = ('student', 'internship', 'internship__company')
    autocomplete_fields = ('student', 'internship')
