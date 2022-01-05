from django.shortcuts import render

# Create your views here.
def testmath(request):
    return render(request, 'testmath.html')