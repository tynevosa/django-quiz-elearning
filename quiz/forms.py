from django import forms
from elearning import settings

class QuestionAdminForm(forms.ModelForm):
    class Media:
        js = (settings.STATIC_URL + 'quiz/js/choice_toggler.js',)

    def clean(self):
        body = self.cleaned_data.get('body')
        image = self.cleaned_data.get('image')
        if not body and not image:
            raise forms.ValidationError('Ensure one of [body, image] fields is be provided')
        return self.cleaned_data

