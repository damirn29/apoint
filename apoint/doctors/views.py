from django.shortcuts import render
from django.http import HttpResponse
from .models import Specialization, Doctor
from .forms import DoctorАppoint
from patients.models import Patient
from django.shortcuts import get_object_or_404

# Create your views here.
def doctors_spec(request):
    specializations = Specialization.objects.all()
    return render(request, 'spec_list.html', {'specializations': specializations})

def doctors_list(request, spec_name):
    specialization = get_object_or_404(Specialization, name=spec_name)
    doctors = Doctor.objects.filter(specialization=specialization)
    return render(request, 'doctor_list.html', {'doctors': doctors})

def doctors_appoint(request, doctor_name):
    context = {'doctor_name': doctor_name}
    form = DoctorАppoint()
    context['form'] = form

    if request.method == 'POST':
        form = DoctorАppoint(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            birth_date = form.cleaned_data['birth_date']
            gender = form.cleaned_data['gender']
            contact_number = form.cleaned_data['contact_number']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']

            patient = Patient(full_name=full_name, birth_date=birth_date, gender=gender,
                              contact_number=contact_number, address=address, email=email)
            patient.save()

            # Дополнительные действия после сохранения пациента

    return render(request, 'doctor_appoint.html', context)