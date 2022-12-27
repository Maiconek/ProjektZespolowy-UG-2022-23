from datetime import date, timedelta
from os import access
from django.db import models
from django.contrib.auth.models import User
import uuid

from UsersApp.models import Profile, Currency, Category, Subcategory

class Account(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    is_shared = models.BooleanField(default=False)
    description = models.CharField(max_length=100, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    # Obliczenie bilansu konta
    def calculate_balance(self):
        balance = 0
        today = date.today()
        transactions = Transaction.objects.filter(id_account=self)
        for transaction in transactions:
            if transaction.transaction_date <= today:
                balance += transaction.converted_amount
        return balance

    def get_transactions(self):
        return Transaction.objects.filter(id_account=self).order_by('-transaction_date')

    def get_users(self):
        return Profile.objects.filter(id__in=User_Account.objects.filter(id_account=self.id).values_list('id_user'))

    #wyświetlenie opisu jeśli istnieje
    def print_description(self):
        if self.description!=None:
            return self.description
        else:
            return ""


class User_Account(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=0)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"[{self.id_user}] - [{self.id_account}] - {self.access_level}"

class Invitation(models.Model):
    userFrom = models.ForeignKey(Profile, related_name='from+', on_delete=models.CASCADE)
    userTo = models.ForeignKey(Profile, related_name='to+', on_delete=models.CASCADE)
    access_level = models.IntegerField(default=0)
    id_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"od: {self.userFrom} do: {self.userTo}, konto: {self.id_account}, poziom dostępu: {self.access_level}"

class Transaction(models.Model):
    intervals = {
        'daily': (lambda x : x + timedelta(days=1), 'Codziennie'),
        'weekly': (lambda x : x + timedelta(weeks=1), 'Co tydzień'),
        'biweekly': (lambda x : x + timedelta(weeks=2), 'Co 2 tygodnie')}

    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True) #konto z którego dokonano transakcji zostało usunięte ale transakcja ma pozostać 
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    repeat = models.CharField(null=True, blank=True, choices=tuple([(k, v[1]) for k, v in intervals.items()]), max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def get_next_date(self):
        if self.repeat is None:
            return None
        else:
            return self.intervals.get(self.repeat)[0](self.transaction_date)

    def save(self, *args, **kwargs):
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return (f"{self.id_account.name} - {self.id_user} - {self.id_category} - "
                f"{self.id_subcategory} - {self.repeat} - {self.amount} - "
                f"{self.converted_amount} - {self.transaction_date} - {self.description}")
