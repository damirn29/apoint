from django.contrib import admin
from django.urls import path, include
from doctors.views import DoctorAPIView
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('doctors.urls')),
]
