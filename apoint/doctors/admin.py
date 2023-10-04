from django.contrib import admin
from .models import Doctor, Schedule, Appointment, Specialization


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1

@admin.register(Doctor)
class ShowDoctors(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialization']
    list_editable = ['name', 'specialization']
    list_filter = ['specialization']
    inlines = [AppointmentInline] #встроенное редактирование раcписания в таблице doctors

@admin.register(Schedule)
class ShowSchedule(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'available_slots']
    list_editable = ['date', 'start_time', 'end_time', 'available_slots']
    list_filter = ['doctor']
    fieldsets = (
        ('Doctor', {
            'fields': ('doctor', 'available_slots')
        }),
        ('Date', {
            'fields': ('date', 'start_time', 'end_time')
        }),
    )

@admin.register(Appointment)
class ShowAppointment(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor']
    list_editable = ['patient', 'doctor']
    list_filter = ['doctor']

@admin.register(Specialization)
class ShowSpecialization(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']