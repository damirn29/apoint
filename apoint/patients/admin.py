from django.contrib import admin
from .models import Patient, MedicalRecord

# Register your models here.
@admin.register(Patient)
class ShowPatients(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'birth_date', 'gender']
    list_editable = ['full_name', 'birth_date', 'gender']

@admin.register(MedicalRecord)
class ShowMedicalRecord(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis']
    list_editable = ['diagnosis']
