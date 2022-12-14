from django import forms
from django.forms import ModelForm
from django.db import models
from .models import Account, Transaction, User_Account
from UsersApp.models import Category, Subcategory, Profile, User
from django.db.models import Q


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency','is_shared' ,'description']
        labels = {
            'name' : 'Nazwa',
            'currency' : 'Waluta',
            'is_shared' : 'Współdzielone?',
            'description' : 'Opis'
        }

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id_user', 'converted_amount']
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
        saved.converted_amount = saved.amount
        if commit:
            saved.save()
        return saved       

class InviteForm(forms.Form):
    access = (
        (0, "Edycja, Usuwanie, Zarządzanie transakcjami"),
        (1, "Zarządzanie transakcjami"),
        (2, "Tylko odczyt"),
    )   
    profile = forms.ModelChoiceField(User.objects.all(), label='Użytkownik')
    access_level = forms.ChoiceField(choices=access, label='Poziom dostępu', initial=2)

    def __init__(self, account=None, **kwargs):
        super(InviteForm, self).__init__(**kwargs)
        if account is not None:
            self.fields['profile'].queryset = User.objects.all().exclude(profile__in=User_Account.objects.filter(id_account=account).values_list('id_user'))