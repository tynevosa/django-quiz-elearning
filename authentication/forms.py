from django import forms

from authentication.models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date'}))
    country = forms.CharField(widget=forms.Select(attrs={'id':'countryId','value':'Egypt', 'class':'countries'}))
    city = forms.CharField(widget=forms.Select(attrs={'id':'stateId','class':'states'}))

    class Meta:
        model = StudentProfile
        exclude = ['user']
