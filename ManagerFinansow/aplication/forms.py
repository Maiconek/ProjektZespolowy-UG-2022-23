from django import forms
from django.forms import ModelForm
from django.db import models
from .models import Account, Transaction, User_Account, Transfer
from UsersApp.models import Category, Subcategory, Profile, User
from django.db.models import Q


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency', 'description']
        labels = {
            'name' : 'Nazwa',
            'currency' : 'Waluta',
            # 'is_shared' : 'Współdzielone?',
            'description' : 'Opis'
        }

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id_user']
        labels = {
            'id_account' : 'Konto',
            'id_category' : 'Kategoria',
            'id_subcategory' : 'Podkategoria',
            'amount' : 'Kwota',
            'description' : 'Opis',
            'transaction_date' : 'Data',
            'currency' : 'Waluta',
            'repeat' : 'Powtarzanie',
        }

    field_order = ['id_account', 'id_category', 'id_subcategory', 'amount', 'currency', 'transaction_date', 'repeat', 'description']

    def __init__(self, *, scope = "EXPENSE", owner, **kwargs):
        instance = kwargs.get('instance', None)
        if scope == "EXPENSE" and instance is not None:
            initial = kwargs.get('initial', None)
            if initial is not None:
                initial['amount'] = -instance.amount
            else:
                initial = {'amount': -instance.amount}
            kwargs.update(initial = initial)
        super(TransactionForm, self).__init__(**kwargs)

        owned_categories = Category.objects.filter(Q(owner=owner) | Q(owner=None))
        self.fields['id_account'].queryset = Account.objects.filter(id__in=User_Account.objects.filter(id_user=owner).values_list('id_account'))
        if scope == "INCOME" or scope == "EXPENSE":
            self.fields['id_category'].queryset = owned_categories.filter(scope=scope)
        self.fields['id_subcategory'].queryset = Subcategory.objects.filter(id_category__in=self.fields['id_category'].queryset)

    def save(self, commit=True):
        saved = super(TransactionForm, self).save(commit=commit)
        if self.cleaned_data['id_category'].scope == "EXPENSE":
            saved.amount = -saved.amount
        if commit:
            saved.save()
        return saved       

class InviteForm(forms.Form): 
    profile = forms.ModelChoiceField(User.objects.all(), label='Użytkownik')
    access_level = forms.ChoiceField(choices=User_Account.access, label='Poziom dostępu', initial='LIMITED')

    def __init__(self, account=None, **kwargs):
        super(InviteForm, self).__init__(**kwargs)
        if account is not None:
            self.fields['profile'].queryset = User.objects.all().exclude(profile__in=User_Account.objects.filter(id_account=account).values_list('id_user'))

class TransferForm(ModelForm):
    class Meta:
        model = Transfer
        exclude = ['id_user', 'id_account', 'id_category', 'id_subcategory']
        labels = {
                'amount' : 'Kwota',
                'description' : 'Opis',
                'transaction_date' : 'Data',
                'currency' : 'Waluta',
                'repeat' : 'Powtarzanie',
                'account_from': 'Z konta',
                'account_to': 'Na konto'
        }
    
    field_order = ['account_from', 'account_to', 'amount', 'currency', 'transaction_date', 'repeat', 'description']

    def __init__(self, owner, **kwargs):
        super(TransferForm, self).__init__(**kwargs)
        self.fields['account_from'].queryset = Account.objects.filter(id__in=User_Account.objects.filter(id_user=owner).values_list('id_account'))
        self.fields['account_to'].queryset = Account.objects.filter(id__in=User_Account.objects.filter(id_user=owner).values_list('id_account'))

    def save(self, commit=True):
        saved = super(TransferForm, self).save(commit=commit)
        return saved       