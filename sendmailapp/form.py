from django import forms
from .models import Patient,Group

#from .tasks import send_review_email_task


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields =('name','gender','dob','email','groups')
        groups =forms.ModelMultipleChoiceField(queryset=Group.objects.all())
        widgets ={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'dob': forms.DateInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'groups':forms.CheckboxSelectMultiple(attrs={'class':'form-check-label'})
        }