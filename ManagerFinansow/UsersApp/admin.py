from django.contrib import admin

from .models import Profile, Currency, Category, Subcategory

admin.site.register(Profile)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Subcategory)