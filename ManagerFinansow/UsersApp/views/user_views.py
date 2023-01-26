from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from UsersApp.forms import CustomUserCreationForm, ProfileForm, SetPasswordForm
from UsersApp.models import *
from UsersApp.tokens import account_activation_token
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
            #messages.success(request, 'You are logged in')
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, "registration/login.html", {})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect("login")
    else:
        messages.error(request, 'Activation link is invalid')
    
    return redirect("profile")    


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("registration/activate_account.html", {
        'user' : user.username,
        'domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
        'protocol' : "https" if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"""Dear {user.username}, please go to your email {to_email} and click on 
        received activation link to complete registration.""")
    else:
        messages.error(request, f"""Problem sending email to {to_email}, check if you typed it correctly""")

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'User account was created')
            
            login(request, user)
            print(user)
            return redirect("login")
    context = {"page" : page, 'form': form}
    return render(request, "registration/login.html", context)

def logoutUser(request):
    logout(request)
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



