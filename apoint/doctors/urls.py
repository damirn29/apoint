from django.contrib import admin
from django.urls import path, include
from doctors.views import doctors_spec
from . import views

urlpatterns = [
    path('', doctors_spec, name='spec-list'),
    path('doctors/<spec_name>/', views.doctors_list, name='spec-name'),
    path('<str:doctor_name>/', views.doctors_appoint, name='doctor-name'),
]