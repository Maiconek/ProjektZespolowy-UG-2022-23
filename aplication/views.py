from django.shortcuts import render


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'application/home-login.html')
    else:
        return render(request, 'application/home-logout.html')