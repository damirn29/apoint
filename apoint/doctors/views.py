from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from doctors.doctorSerializer import DoctorSerializer
from doctors.appointSerializer import AppointSerializer
from .models import Specialization, Doctor, Schedule, Appointment
from .forms import DoctorАppoint
from patients.models import Patient
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Count
from rest_framework import generics, viewsets
from django.db.models import Q
from rest_framework.decorators import action


def doctors_spec(request):
    specializations = Specialization.objects.all().annotate(num_doctors=Count('doctor'))
    return render(request, 'spec_list.html', {'specializations': specializations})


def doctors_list(request, spec_name):
    specialization = get_object_or_404(Specialization, name=spec_name)
    doctors = Doctor.objects.filter(specialization=specialization)
    return render(request, 'doctor_list.html', {'doctors': doctors})

def doctors_appoint(request, doctor_name):
    context = {'doctor_name': doctor_name}
    form = DoctorАppoint()
    context['form'] = form

    doctor = get_object_or_404(Doctor, name=doctor_name)

    shedule = Schedule.objects.filter(doctor=doctor)
    context['shedule'] = shedule
    if request.method == 'POST':
        form = DoctorАppoint(request.POST)
        if form.is_valid():
            available_slot = Schedule.objects.filter(doctor=doctor, available_slots__gt=0).order_by('date', 'start_time').first()

            if available_slot is not None:
                available_slot.available_slots -= 1
                available_slot.save()
                patient = Patient(full_name=form.cleaned_data['full_name'],
                                  birth_date=form.cleaned_data['birth_date'],
                                  gender=form.cleaned_data['gender'],
                                  contact_number=form.cleaned_data['contact_number'],
                                  address=form.cleaned_data['address'],
                                  email=form.cleaned_data['email'])
                patient.save()

                appointment = Appointment(patient=patient, doctor=doctor,
                                         schedule=available_slot,
                                         appointment_date=available_slot.date,
                                         appointment_time=available_slot.start_time)
                appointment.save()
                return redirect(reverse('appointment_detail', args=[appointment.id]))  # перенаправление на новую страницу

            else:
                context['error'] = 'К сожалению, в данный момент свободных мест нет. Пожалуйста, выберите другого врача или зайдите позже.'
    return render(request, 'doctor_appoint.html', context)


def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id = appointment_id)
    context = {
        'appointment': appointment
    }
    return render(request, 'appointment_detail.html', context)



class DoctorAPIView(generics.ListAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        speciality = Specialization.objects.get(name='cardiology')
        return Doctor.objects.filter(Q(specialization=speciality) & Q(schedule__available_slots__gt=11)).distinct()

""" class AppointAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointSerializer """

class AppointViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['appointment_date', 'appointment_time']


    @action(methods=['get'], detail=True)
    def appoints(self, request, pk=None):
        appoints = Appointment.objects.get(pk=pk)
        return Response({'appoint': appoints})

