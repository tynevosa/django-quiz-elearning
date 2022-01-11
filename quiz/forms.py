from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)

from django.contrib.auth.models import User
from quiz.models import Answer


class SignUpForm(UserCreationForm):
    # TODO:: Add to model new student fields
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


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

