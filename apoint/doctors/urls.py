from django.contrib import admin
from django.urls import path, include
from doctors.views import doctors_spec, appointment_detail
from . import views
from doctors.views import DoctorAPIView, AppointViewSet
from rest_framework import routers
from .views import AppointmentListCreateView, filtered_appointments

router = routers.SimpleRouter()
router.register(r'appoint', AppointViewSet)
print(router.urls)

urlpatterns = [
    path('', doctors_spec, name='spec-list'),
    path('api/doctors-cardiology/', DoctorAPIView.as_view(), name='api-doctors-cardiology'),
    path('api/v1/', include(router.urls)),
    path('doctors/<spec_name>/', views.doctors_list, name='spec-name'),
    path('<str:doctor_name>/', views.doctors_appoint, name='doctor-name'),
    path('appointment/detail/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('api/appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('api/filtered-appointments/', filtered_appointments, name='filtered-appointments'),
]