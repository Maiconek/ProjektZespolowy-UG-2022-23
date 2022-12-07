from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from UsersApp.forms import SubCategoryForm
from UsersApp.models import *

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
