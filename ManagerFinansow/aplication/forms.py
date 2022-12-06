from django import forms
from django.forms import ModelForm
from django.db import models
from .models import Account, Transaction
from UsersApp.models import Category


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency', 'description']

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id_account', 'id_user', 'converted_amount', 'transaction_date']
    def __init__(self, *, scope = "EXPENSE", **kwargs):
        super(TransactionForm, self).__init__(**kwargs)
        if scope == "INCOME":
            self.fields['id_category'].queryset = Category.objects.filter(scope=scope)
        if scope == "EXPENSE":
            self.fields['id_category'].queryset = Category.objects.filter(scope=scope)
