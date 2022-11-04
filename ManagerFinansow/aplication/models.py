from os import access
from django.db import models

# Create your models here.
class Currency(models.Model):
    id_currency = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=100)
    access_name = models.CharField(max_length=20) #access_name nazwa aby zdobyć kurs walut

    def __str__(self):
        return "[{}] - {}".format(self.id_currency, self.name)

class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id_subcategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Account(models.Model):
    id_account = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_shared = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    id_currency = models.ForeignKey(Currency, on_delete=models.SET_DEFAULT, default="PLN")
    User_Account = models.ManyToManyField(Account, through='User_Account') 
    image = models.ImageField(null=True, blank=True)
#https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships
#https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/

    def __str__(self):
        return "[{}] - {} - {} - {}".format(self.id_user, self.name, self.email, self.User_Account.all())

class User_Account(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=0)

    def __str__(self):
        return "[{}] - [{}] - {}".format(self.id_user, self.id_account, self.access_level)

class Transaction(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) #konto z którego dokonano transakcji zostało usunięte ale transakcja ma pozostać 
    id_subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True) #umozliwienie usuniecia kategorii i podkategorii bez usuniecia transakcji
    name = models.CharField(max_length=255)
    is_periodic = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "[{}] - {} - {} - {} - {} - {} - {} - {} - {} - {} - {}".format(self.id_transaction, self.id_account.name, self.id_user.name, self.id_subcategory.id_category.name ,self.id_subcategory, self.name, self.is_periodic, self.amount, self.converted_amount, self.transaction_date, self.description)
