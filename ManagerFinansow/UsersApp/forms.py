from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Category
# Create your forms here.

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

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'image']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'scope']
        

