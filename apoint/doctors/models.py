from django.db import models
from simple_history.models import HistoricalRecords

class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    working_date = models.DateField()
    contact_number = models.CharField(max_length=20)
    history = HistoricalRecords() # отслеживание истории изменения модели

    def __str__(self):
        return self.name

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_slots = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    history = HistoricalRecords() # отслеживание истории изменения модели

    def __str__(self):
        return f"Schedule {self.id}"

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    history = HistoricalRecords() # отслеживание истории изменения модели

    def __str__(self):
        return f"Appointment {self.id}"