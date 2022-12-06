from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, ProfileForm, CategoryForm, SubCategoryForm
from .models import *

#Create your views here.
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
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')
            
            login(request, user)
            print(user)
            return redirect("home")
        else:
            if form.data['password1'] != form.data['password2']: 
                messages.error(request, 'Hasło powinno być identyczne')
            if len(form.data['password1']) < 8: 
                messages.error(request, 'Hasło powinno mieć przynajmniej 8 znaków')
    context = {"page" : page, 'form': form}
    return render(request, "registration/login.html", context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logout')
    return redirect("home")

@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'application/profile.html', context)


@login_required(login_url='login')
def showCategories(request):
    defaultCategory = Category.objects.filter(owner__isnull=True)
    userCategory = Category.objects.filter(owner=request.user.profile)

    context = {'defaultCategory' : defaultCategory, 'userCategory' : userCategory}
    return render(request, 'application/categories/all-categories.html', context)

@login_required(login_url='login')
def createCategory(request):
    page = "create"
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user.profile
            category.save()
            return redirect('all-categories')
    context = {'form' : form, 'page' : page}
    return render(request, 'application/categories/categoryForm.html', context)

@login_required(login_url='login')
def editCategory(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category.save()
            return redirect('all-categories')
    context = {'form' : form, 'category' : category}
    return render(request, 'application/categories/categoryForm.html', context)

@login_required(login_url='login')
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('all-categories')

@login_required(login_url='login')
def allSubcategories(request, pk):
    category = Category.objects.get(id=pk)
    subcategory = Subcategory.objects.filter(id_category=pk)

    context = {"category" : category, "subcategory" : subcategory}
    return render(request, "application/categories/all-subcategories.html", context)

@login_required(login_url='login')
def createSubcategory(request, pk):
    page = "create"
    form = SubCategoryForm()
    category = Category.objects.get(id=pk)

    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.id_category = category
            subcategory.save()
            return redirect('all-subcategories', pk=str(category.id))
    context = {'form': form, 'category': category, 'page' : page}
    return render(request, "application/categories/subcategories-form.html", context)

@login_required(login_url='login')
def editSubcategory(request, pk, pk2):
    category = Category.objects.get(id=pk)
    subcategory = Subcategory.objects.get(id=pk2)
    form = SubCategoryForm(instance=subcategory)

    if request.method == "POST":
        form = SubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            subcategory.save()
            return redirect('all-subcategories', pk=str(category.id))
    context = {'form': form, 'category': category, 'subcategory' : subcategory}
    return render(request, "application/categories/subcategories-form.html", context)

@login_required(login_url='login')
def deleteSubcategory(request, pk, pk2):
    category = Category.objects.get(id=pk)
    subcategory = Subcategory.objects.get(id=pk2)
    subcategory.delete()
    return redirect('all-subcategories', pk=str(category.id))


# @login_required(login_url='login')
# def allAccounts(request):
#     accounts = Account.objects.all()
#     user_accounts = accounts.filter(owner=request.user.profile)
#     context = {'accounts': user_accounts}
#     return render(request, 'application/all-accounts.html', context)

# if request.method == 'POST':
#     form = RegistrationFormTeacher(request.POST)
#     if form.is_valid():
#         new_teacher = form.save(commit=False)
#         new_teacher.user = request.user #get the user object however you want - you 
#             #can pass the user ID to the view as a parameter and do 
#             #User.objects.get(pk=id) or some such, too. 
#         new_teacher.save()
#         form.save_m2m()
