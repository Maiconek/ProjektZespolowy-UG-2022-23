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
    path('account/<uuid:pk>', showAccount, name='account'),
    path('account/<uuid:pk>/del', delAccount, name='delAccount'),
    path('account/<uuid:pk>/edit', editAccount, name='editAccount'),
    path('account/<uuid:pk>/invite', invite, name='invite'),
    path('invitation/<uuid:pk>/join', joinAccount, name='joinAccount'),
    #transactions
    path('account/<uuid:pk>/add/<str:type>', TransactionAdd.as_view(), name='add'),
    path('add/<str:type>', TransactionAdd.as_view(), name='addAccountless'),
    path('account/transaction/<uuid:pk>/<str:accountless>/', showTransaction, name='showTransaction'),
    path('account/transaction-del/<uuid:pk>/<str:accountless>', delTransaction, name='delTransaction'),
    path('account/transaction-edit/<uuid:pk>/<str:accountless>', TransactionEdit.as_view(), name='editTransaction'),
    path('account/transaction-duplicate/<uuid:pk>/<str:accountless>', TransactionDuplicate.as_view(), name='duplicateTransaction'),
    #other
    path('budget', budget, name='budget'),
    path('summary', summary, name='summary'),
]
