from django.contrib import admin
from .models import Patient, MedicalRecord
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient

    def get_export_queryset(self, request):
        return Patient.objects.filter(gender='Male')

    def dehydrate_full_name(self, patient):
        return f"Customized: {patient.full_name}"

    def get_birth_date(self, patient):
        return f"Customized: {patient.birth_date}"

class MedicalRecordResource(resources.ModelResource):
    class Meta:
        model = MedicalRecord

class MedicalRecordInline(admin.StackedInline):
    model = MedicalRecord
    extra = 1

@admin.register(Patient)
class ShowPatients(ImportExportModelAdmin):
    resource_class = PatientResource
    list_display = ['id', 'full_name', 'birth_date', 'gender', 'customized_birth_date']
    list_editable = ['full_name', 'birth_date', 'gender']
    list_filter = ['gender']
    search_fields = ['full_name']

    def customized_birth_date(self, obj):
        return f"Customized: {obj.birth_date}"
    customized_birth_date.short_description = 'Customized Birth Date'

    fieldsets = [
        ('Personal Information', {'fields': ['full_name', 'birth_date', 'gender']}),
        ('Additional Information', {'fields': ['address', 'phone_number']}),
    ]

    inlines = [MedicalRecordInline]

@admin.register(MedicalRecord)
class ShowMedicalRecord(ImportExportModelAdmin):
    resource_class = MedicalRecordResource
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis']
    list_editable = ['diagnosis']
    list_filter = ['doctor']
    search_fields = ['patient__full_name']

    fieldsets = [
        ('Medical Information', {'fields': ['patient', 'doctor', 'visit_date', 'diagnosis']}),
        ('Prescription', {'fields': ['prescription']}),
    ]
