from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


# Create your views here.
def testmath(request):
    return render(request, 'testmath.html')

# Views
@login_required
def home(request):
    return render(request, "registration/success.html", {})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('quiz:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
