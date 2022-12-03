from django.db import models
from django.contrib.auth.models import User
import uuid

from aplication.models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=400, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

#https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships
#https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/

class Currency(models.Model):
    name = models.CharField(max_length=100)
    access_name = models.CharField(max_length=20) #access_name nazwa aby zdobyć kurs walut
    sign = models.CharField(max_length=5) #znak waluty
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self):
        return "[{}] - {} - {}".format(self.name, self.sign, self.access_name)
