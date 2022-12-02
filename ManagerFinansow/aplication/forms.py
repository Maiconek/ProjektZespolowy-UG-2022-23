from django import forms
from django.forms import ModelForm
from .models import Account, Transaction


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'is_shared', 'description']

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id_account', 'id_user', 'converted_amount', 'transaction_date']
