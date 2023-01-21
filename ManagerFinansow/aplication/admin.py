from django.contrib import admin
from .models import *

admin.site.register(Account)
admin.site.register(User_Account)
admin.site.register(Transaction)
admin.site.register(Invitation)