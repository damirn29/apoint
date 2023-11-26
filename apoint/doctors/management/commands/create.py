from django.core.management.base import BaseCommand, CommandError
from doctors.models import Doctor, Specialization
from django.core.exceptions import ObjectDoesNotExist
import datetime

class Command(BaseCommand):
    help = 'Create a new doctor'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='The name of the doctor')
        parser.add_argument('specialization', type=str, help='The specialization of the doctor')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        specialization_name = kwargs['specialization']

        try:
            specialization = Specialization.objects.get(name=specialization_name)
        except ObjectDoesNotExist:
            raise CommandError(f'Specialization "{specialization_name}" does not exist.')

        current_date = datetime.date.today()
        doctor = Doctor.objects.create(
            name=name,
            specialization=specialization,
            working_date=current_date
        )

        self.stdout.write(self.style.SUCCESS(f'Doctor {doctor.name} was created successfully'))

# python manage.py create 'Doctor Name' '1'