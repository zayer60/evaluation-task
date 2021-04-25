from django import forms
from .models import Patient,Group
from tinymce.widgets import TinyMCE

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


class SendMail(forms.Form):
#    To = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    Message = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))

    class Media:
        js = ('/site_media/static/tiny_mce/tinymce.min.js',)