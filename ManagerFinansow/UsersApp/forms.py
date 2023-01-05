from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Category, Subcategory

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'username' : 'Nazwa użytkownika',
            'first_name' : 'Imię',
            'email' : 'Email',
            'password1' : 'Hasło',
            'password2': 'Powtórz hasło'
        }

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'image', 'currency']
        labels = {
            'name' : 'Imię',
            'username' : 'Nazwa użytkownika',
            'email' : 'Email',
            'image' : 'Zdjęcie',
            'currency' : 'Waluta'
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'scope']
        labels = {
            'name' : 'Nazwa',
            'scope' : 'Rodzaj'
        }

class SubCategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name']
        labels = {
            'name' : 'Nazwa'
        }
