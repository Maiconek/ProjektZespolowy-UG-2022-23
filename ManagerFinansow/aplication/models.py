from os import access
from django.db import models
from django.contrib.auth.models import User
import uuid

from UsersApp.models import *

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Account(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    is_shared = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)
    def __str__(self):
        return self.name

    # Obliczenie bilansu konta
    def calculate_balance(self):
        balance = 0
        transactions = Transaction.objects.filter(id_account=self)
        for transaction in transactions:
            balance += transaction.converted_amount
        return balance




class User_Account(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=0)

    def __str__(self):
        return "[{}] - [{}] - {}".format(self.id_user, self.id_account, self.access_level)

class Transaction(models.Model):
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True) #konto z którego dokonano transakcji zostało usunięte ale transakcja ma pozostać 
    id_subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True) #umozliwienie usuniecia kategorii i podkategorii bez usuniecia transakcji
    name = models.CharField(max_length=50)
    is_periodic = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self):
        return "[{}] - {} - {} - {} - {} - {} - {} - {} - {} - {}".format(self.name, self.id_account.name, self.id_user.name, self.id_subcategory.id_category.name ,self.id_subcategory, self.is_periodic, self.amount, self.converted_amount, self.transaction_date, self.description)
