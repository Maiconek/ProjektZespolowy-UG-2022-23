from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from aplication.models import Profile

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('id_currency', 'image', 'user')

    def save(self, commit=True):
        profile = super(NewProfileForm, self).save(commit=False)
        profile.id_currency = self.cleaned_data['id_currency']
        profile.image = self.cleaned_data['image']
        profile.user = self.cleaned_data['user']
        if commit:
            profile.save()
        return profile

