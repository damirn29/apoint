from django.contrib import admin
from django.urls import path, include
from doctors.views import doctors_spec, appointment_detail
from . import views

urlpatterns = [
    path('', doctors_spec, name='spec-list'),
    path('doctors/<spec_name>/', views.doctors_list, name='spec-name'),
    path('<str:doctor_name>/', views.doctors_appoint, name='doctor-name'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
]