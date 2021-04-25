from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .form import PatientForm

class GroupListView(ListView):
    model = Group
    template_name = 'sendmailapp/grouplist.html'

def groupdetail(request,id):
    group= Group.objects.get(pk=id)
    patients=group.patient_set.all()
    return render(request,'sendmailapp/groupdetail.html',{'group':group,'patients':patients})

class CreateGroup( CreateView):
    model = Group
    fields = '__all__'
    template_name = 'sendmailapp/group-create.html'

class UpdateGroup( UpdateView):
    model = Group
    fields = ('name',)
    template_name = 'sendmailapp/group-update-form.html'

class DeleteGroup( DeleteView):
    model = Group
    template_name = 'sendmailapp/group-delete.html'
    success_url = reverse_lazy('group-list')

class PatientListView(ListView):
    model = Patient
    template_name = 'sendmailapp/patientlist.html'

class CreatePatient( CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'sendmailapp/patient-create.html'

class UpdatePatient( UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'sendmailapp/patient-update-form.html'


class DeletePatient( DeleteView):
    model = Patient
    template_name = 'sendmailapp/patient-delete.html'
    success_url = reverse_lazy('patient-list')
