from django_filters import FilterSet
from .models import Patient
import django_filters
from django import forms

class PatientFilter(FilterSet):
    class Meta:
        model = Patient
        fields =('groups',)
