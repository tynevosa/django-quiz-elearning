from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

from quiz.models import Answer, StudentProfile


class StudentProfileForm(forms.ModelForm):
    # # TODO:: Add to model new student fields
    # school = forms.CharField(max_length=100)
    # country = forms.CharField(max_length=100)
    # how_did_you_hear_about_us = forms.CharField(max_length=100)
    # phone_number = forms.CharField(max_length=100)
    # city = forms.CharField(max_length=100)
    # school_type = forms.CharField(max_length=100, widget=forms.Select(choices=StudentProfile.SchoolTypeChoices.choices,  attrs={'class': 'browser-default'}))
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = StudentProfile
        exclude = ['user']
        


class SubmitQuestionAnswer(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('student_answer',)

    student_answer = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols': '40'}), label='Your Answer', max_length=100, min_length=1, required=True)


class QuestionAdminForm(forms.ModelForm):
    body = forms.Textarea(attrs={'class': 'MathJaxSource'})

    def clean(self):
        body = self.cleaned_data.get('body')
        image = self.cleaned_data.get('image')
        if not body and not image:
            raise forms.ValidationError('Ensure one of [body, image] fields is be provided')
        return self.cleaned_data

