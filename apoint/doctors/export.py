from import_export import resources
from .models import Doctor

class MyModelResource(resources.ModelResource):
    class Meta:
        model = Doctor
        fields = ('Id', 'name', 'specialization')