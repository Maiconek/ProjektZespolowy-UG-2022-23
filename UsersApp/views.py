from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, ProfileForm

# Create your views here.
def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('application/base.html')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password) 
        #return user instance or none, jezeli hasło się zgadza to zostaniemy zalogowani

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, "registration/login.html", {})

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')
            
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, 'Error')

    context = {"page" : page, 'form': form}
    return render(request, "registration/login.html", context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logout')
    return redirect("home")


# if request.method == 'POST':
#     form = RegistrationFormTeacher(request.POST)
#     if form.is_valid():
#         new_teacher = form.save(commit=False)
#         new_teacher.user = request.user #get the user object however you want - you 
#             #can pass the user ID to the view as a parameter and do 
#             #User.objects.get(pk=id) or some such, too. 
#         new_teacher.save()
#         form.save_m2m()
