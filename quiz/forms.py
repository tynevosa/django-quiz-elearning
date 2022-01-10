from django import forms

from quiz.models import Answer


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

