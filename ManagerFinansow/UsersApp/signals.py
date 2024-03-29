from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from .models import Profile, Currency

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        currency = Currency.objects.get(access_name="PLN")
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
            currency = currency
        )

        subject = f"Welcome to Cointrol {user.username}!"
        message = f"""
        Hello {user.username}! We are glad thay you've decided to join us! 
        With Cointrol you will be able to control your finances and plan your next expenses.
        We hope that you will have a great time here!\n
        Cointrol Team"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
#post_delete.connect(deleteUser, sender=Profile)