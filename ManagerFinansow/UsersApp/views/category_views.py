from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from UsersApp.forms import CategoryForm
from UsersApp.models import *

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