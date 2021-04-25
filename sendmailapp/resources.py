from import_export import resources, fields, widgets
from .models import PatientGroup


class PatientResource(resources.ModelResource):
    class Meta:
        model = PatientGroup