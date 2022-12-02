"""ManagerFinansow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from aplication.views import *

urlpatterns = [
    path('', home, name='home'),
    path('all-accounts', allAccounts, name='all-accounts'),
    path('create-account', createAccount, name='create-account'),
    path('account/<pk>', showAccount, name='account'),
    path('account/<pk>/transaction-add', addTransaction, name='addTransaction'),
    path('account/transaction/<pk>', showTransaction, name='showTransaction'),
    path('account/transaction-del/<pk>', delTransaction, name='delTransaction'),
    path('account/transaction-edit/<pk>', editTransaction, name='editTransaction'),
    path('account/<pk>/join', joinAccount, name='joinAccount'),
]
