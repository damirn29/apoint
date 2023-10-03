from django.contrib import admin
from .models import Doctor, Schedule, Appointment, Specialization


@admin.register(Doctor)
class ShowDoctors(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialization']
    list_editable = ['name', 'specialization']

@admin.register(Schedule)
class ShowSchedule(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'available_slots']
    list_editable = ['date', 'start_time', 'end_time', 'available_slots']

@admin.register(Appointment)
class ShowAppointment(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor']
    list_editable = ['patient', 'doctor']

@admin.register(Specialization)
class ShowSpecialization(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']