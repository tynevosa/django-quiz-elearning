from django import forms
from django.contrib.auth.forms import UserCreationForm

from authentication.models import StudentProfile, User


class SignUpForm(UserCreationForm):
#profile_year        = blaaa blaa blaaa irrelevant.. You have your own stuff here don't worry about it

    class Meta:
        model = User #this is the "YourCustomUser" that you imported at the top of the file  
        fields = ('email', 'password1', 'password2') #etc etc, other fields you want displayed on the form)
      

class StudentProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date'}))
    country = forms.CharField(widget=forms.Select(attrs={'id':'countryId','value':'Egypt', 'class':'countries'}))
    city = forms.CharField(widget=forms.Select(attrs={'id':'stateId','class':'states'}))

    class Meta:
        model = StudentProfile
        exclude = ['user']
