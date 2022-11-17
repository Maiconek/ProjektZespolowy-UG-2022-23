from django.shortcuts import render, redirect
from UsersApp.forms import NewUserForm, NewProfileForm
from django.contrib.auth import login, logout
from django.contrib import messages
from aplication.views import home

# Create your views here.
def profile(request):
    return render(request, 'application/profile.html')

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def register_profile(request):
    user = request.user
    form = NewProfileForm(instance=user)
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            profile = form.save()
            messages.success(request, "Additional data successfuly added." )
            return redirect(home)
        messages.error(request, "Unsuccessful addition of data. Invalid information.")
    form = NewProfileForm
    return render (request=request, template_name="registration/register-next.html", context={"register_form":form})

def register_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect(register_profile)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render (request=request, template_name="registration/register.html", context={"register_form":form})


# if request.method == 'POST':
#     form = RegistrationFormTeacher(request.POST)
#     if form.is_valid():
#         new_teacher = form.save(commit=False)
#         new_teacher.user = request.user #get the user object however you want - you 
#             #can pass the user ID to the view as a parameter and do 
#             #User.objects.get(pk=id) or some such, too. 
#         new_teacher.save()
#         form.save_m2m()