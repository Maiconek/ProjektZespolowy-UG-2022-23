from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Currency)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Account)
admin.site.register(User_Account)
admin.site.register(Transaction)