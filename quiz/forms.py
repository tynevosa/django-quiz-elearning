from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

from quiz.models import Answer, StudentProfile


class StudentProfileForm(forms.ModelForm):
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

