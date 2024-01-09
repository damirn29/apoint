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
from rest_framework.response import Response
from .serializers import AppointmentSerializer
from rest_framework.filters import SearchFilter
from rest_framework import generics, status
from rest_framework.decorators import api_view, action

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
                return redirect(reverse('appointment_detail', args=[appointment.id]))

            else:
                context['error'] = 'Unfortunately, there are no available seats at the moment. Please choose another doctor or come back later.'
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
        speciality_cardiology = Specialization.objects.get(name='cardiology')
        speciality_orthopedics = Specialization.objects.get(name='orthopedics')

        # Q-объект с операторами AND, OR и NOT
        return Doctor.objects.filter(
            Q(specialization=speciality_cardiology, schedule__available_slots__gt=11) |
            Q(specialization=speciality_orthopedics) &
            ~Q(working_date__gte='2024-01-01')  # Пример NOT (working_date >= '2024-01-01')
        ).distinct()

class AppointViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointSerializer
    filter_backends = [DjangoFilterBackend] #фильтр
    filterset_fields = ['appointment_date', 'appointment_time']


    @action(methods=['get'], detail=True)
    def appoints(self, request, pk=None):
        appoints = Appointment.objects.get(pk=pk)
        return Response({'appoint': appoints})


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['doctor__name', 'doctor__specialization__name', 'patient__name']

    @action(methods=['POST'], detail=True)
    def create_appointment(self, request, pk=None):
        doctor_id = request.data.get('doctor_id')
        schedule_id = request.data.get('schedule_id')
        appointment_date = request.data.get('appointment_date')
        appointment_time = request.data.get('appointment_time')
        patient_id = request.data.get('patient_id')

        if not all([doctor_id, schedule_id, appointment_date, appointment_time, patient_id]):
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(pk=doctor_id)
            schedule = Schedule.objects.get(pk=schedule_id)
            patient = Patient.objects.get(pk=patient_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'Invalid doctor ID'}, status=status.HTTP_404_NOT_FOUND)
        except Schedule.DoesNotExist:
            return Response({'error': 'Invalid schedule ID'}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({'error': 'Invalid patient ID'}, status=status.HTTP_404_NOT_FOUND)

        appointment = Appointment.objects.create(
            doctor=doctor,
            schedule=schedule,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            patient=patient
        )

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def filtered_appointments(request):
    q_object = (
        Q(doctor__specialization__name='Neurologist') &  # AND
        Q(appointment_date__gte='2023-01-08') |  # OR
        ~Q(id='9')  # NOT
    )
    filtered_appointments = Appointment.objects.filter(q_object)
    serializer = AppointmentSerializer(filtered_appointments, many=True)
    return Response(serializer.data)


