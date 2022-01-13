from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View

from authentication.forms import SignUpForm, StudentProfileForm

# Create your views here.

class RegisterView(View):

    def get(self, request):
        user_form = SignUpForm()
        student_profile_form = StudentProfileForm()

        return render(request, 'registration/register.html', {'user_form': user_form, 'student_profile_form': student_profile_form})

    def post(self, request):
        user_form = SignUpForm(request.POST)
        student_profile_form = StudentProfileForm(request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():
            user = user_form.save()
            student_profile = student_profile_form.save(commit=False)
            student_profile.user = user
            student_profile.save()

            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('quiz:category_list')

        return render(request, 'registration/register.html', {'user_form': user_form, 'student_profile_form': student_profile_form})

