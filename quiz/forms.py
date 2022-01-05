from django import forms

class QuestionAdminForm(forms.ModelForm):
    def clean(self):
        body = self.cleaned_data.get('body')
        image = self.cleaned_data.get('image')
        if not body and not image:
            raise forms.ValidationError('Ensure one of [body, image] fields is be provided')
        return self.cleaned_data

