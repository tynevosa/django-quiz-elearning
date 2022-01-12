from django import forms
from authentication.models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = StudentProfile
        exclude = ['user']
