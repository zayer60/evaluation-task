from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .form import PatientForm, SendMail
from django.http import HttpResponse
from tablib import Dataset
from .resources import PatientResource

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

class SearchPatient(ListView):
    model = Patient
    context_object_name = 'patient_list'
    template_name = 'sendmailapp/search-patient.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Patient.objects.filter(name__icontains=query)

def export(request):
    patient_resource = PatientResource()
    dataset = patient_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        patient_resource = PatientResource()
        dataset = Dataset()
        new_patients = request.FILES['myfile']

        imported_data = dataset.load(new_patients.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = PatientGroup(
                data[0],
                data[1],
                data[2],
            )
            value.save()

            # result = patient_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'sendmailapp/index.html')



class ContactView(FormView):
    template_name = 'sendmailapp/form.html'
    form_class = SendMail
