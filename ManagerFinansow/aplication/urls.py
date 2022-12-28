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
    path('', showAllTransactions, name='home'),
    #accounts
    path('all-accounts', allAccounts, name='all-accounts'),
    path('create-account', createAccount, name='create-account'),
    path('account/<pk>', showAccount, name='account'),
    path('account/<pk>/del', delAccount, name='delAccount'),
    path('account/<pk>/edit', editAccount, name='editAccount'),
    path('account/<pk>/invite', invite, name='invite'),
    path('invitation/<pk>/join', joinAccount, name='joinAccount'),
    #transactions
    path('account/<pk>/add/<str:type>', TransactionAdd.as_view(), name='add'),
    path('add/<str:type>', TransactionAdd.as_view(), name='addAccountless'),
    path('account/transaction/<pk>/<str:accountless>', showTransaction, name='showTransaction'),
    path('account/transaction-del/<pk>/<str:accountless>', delTransaction, name='delTransaction'),
    path('account/transaction-edit/<pk>/<str:accountless>', TransactionEdit.as_view(), name='editTransaction'),
    path('account/transaction-duplicate/<pk>/<str:accountless>', TransactionDuplicate.as_view(), name='duplicateTransaction'),
    #other
    path('budget', budget, name='budget'),
    path('summary', summary, name='summary'),
]
