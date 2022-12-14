from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from UsersApp.forms import CustomUserCreationForm, ProfileForm, SetPasswordForm
from UsersApp.models import *
from aplication.models import Invitation

def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")
    
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
            messages.success(request, 'You are logged in')
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
            # user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')
            
            login(request, user)
            print(user)
            return redirect("home")
    context = {"page" : page, 'form': form}
    return render(request, "registration/login.html", context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logout')
    return redirect("home")

def changePassword(request):
    user = request.user
    form = SetPasswordForm(user)
    
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile")
    context = {"form" : form}
    return render(request, "registration/password-change.html", context)

@login_required(login_url='login')
def allProfiles(request):
    profiles = Profile.objects.all()
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    profiles= Profile.objects.filter(username__icontains=search_query)
    context = {'search_query' : search_query, 'profiles' : profiles}

    return render(request, 'application/profiles-list.html', context)


    

@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    context = {'profile': profile, 'mes': Invitation.objects.filter(Q(userTo=profile) | Q(userFrom=profile))}
    return render(request, 'application/profile.html', context)

@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {"form" : form}
    return render(request, "application/edit-profile.html", context)



