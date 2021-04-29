from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .form import PatientForm, SendMail, GroupForm
from django.http import HttpResponse, HttpResponseRedirect
from tablib import Dataset
from .resources import PatientResource
from .tasks import send_review_email_task
from django.core.mail import send_mail, BadHeaderError
from .filter import PatientFilter

class GroupListView(ListView):
    model = Group
    template_name = 'sendmailapp/grouplist.html'

def groupdetail(request,id):
    group= Group.objects.get(pk=id)
    patients=group.patient_set.all()
    return render(request,'sendmailapp/groupdetail.html',{'group':group,'patients':patients})

class CreateGroup( CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'sendmailapp/group-create.html'

class UpdateGroup( UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'sendmailapp/group-update-form.html'

class DeleteGroup( DeleteView):
    model = Group
    template_name = 'sendmailapp/group-delete.html'
    success_url = reverse_lazy('group-list')

class PatientListView(ListView):
    model = Patient
    template_name = 'sendmailapp/patientlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PatientFilter(self.request.GET,queryset=self.get_queryset())
        return context

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

'''
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
'''


def simple_upload(request):
    if request.method == 'POST':
        patient_resource = PatientResource()
        dataset = Dataset()
        new_patients = request.FILES['myfile']

        imported_data = dataset.load(new_patients.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[5])
            value = Patient.objects.get(pk=data[0])
            groupvalue = value.groups.add(data[5])
            '''
            value = Patient(
                id=data[0],
                name=data[1],
                gender=data[2],
                dob=data[3],
                email=data[4],
                groups=data[5],
            )
            '''
            # groupvalue.save()
    return render(request, 'sendmailapp/index.html')

'''
class ContactView(FormView):
    template_name = 'sendmailapp/form.html'
    form_class = SendMail
'''


def sendemail(request,id):
    form = SendMail()
    if request.method== 'POST':
        form = SendMail(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=id)
            to = [patient.email]
            print(to)
            try:
                send_review_email_task.delay(
                    form.cleaned_data['Subject'],'hello there',form.cleaned_data['Message'] , to)
                return HttpResponseRedirect(reverse('group-list'))
                #return HttpResponse('success')
            except BadHeaderError:
                return HttpResponse('invalid header found')
    return render(request, 'sendmailapp/form.html', {'form': form})



def groupemail(request,id):
    group = Group.objects.get(pk=id)
    patients = group.patient_set.all()
    to = [patient.email for patient in patients]
    print(to)
    form = SendMail()
    if request.method=='POST':
        form = SendMail(request.POST)
        if form.is_valid():
                print(to)
                send_review_email_task.delay(
                    form.cleaned_data['Subject'],'hello there', form.cleaned_data['Message'], to)
                return HttpResponseRedirect(reverse('group-list'))
                #return HttpResponse('success')
    return render(request, 'sendmailapp/form.html', {'form': form})