from django.contrib import admin
from django.urls import path, include
from portal.views import health_check

urlpatterns = [
    path('', health_check, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('portal.urls')),
]