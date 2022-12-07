from django import forms
from django.forms import ModelForm
from django.db import models
from .models import Account, Transaction
from UsersApp.models import Category, Subcategory
from django.db.models import Q


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency', 'description']

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id_account', 'id_user', 'converted_amount', 'transaction_date']

    def __init__(self, *, scope = "EXPENSE", owner, **kwargs):
        super(TransactionForm, self).__init__(**kwargs)
        owned_categories = Category.objects.filter(Q(owner=owner) | Q(owner=None))
        if scope == "INCOME":
            self.fields['id_category'].queryset = owned_categories.filter(scope=scope)
        if scope == "EXPENSE":
            self.fields['id_category'].queryset = owned_categories.filter(scope=scope)
        self.fields['id_subcategory'].queryset = Subcategory.objects.filter(id_category__in=self.fields['id_category'].queryset)
        