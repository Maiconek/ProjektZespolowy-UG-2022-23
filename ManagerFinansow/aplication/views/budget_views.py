from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from aplication.forms import AccountForm
from django.http import Http404  

@login_required(login_url='login')
def budget(request):
    return render(request, 'application/budget.html')