from django.db import models


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(default='почта не указана')

    def __str__(self):
        return self.full_name

class MedicalRecord(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    visit_date = models.DateField()
    diagnosis = models.CharField(max_length=255)
    doctor_recommendations = models.TextField()
    prescribed_medications = models.TextField()

    def __str__(self):
        return f"Medical Record {self.id}"