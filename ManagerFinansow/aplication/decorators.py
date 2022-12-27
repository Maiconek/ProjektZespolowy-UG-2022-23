from django.shortcuts import get_object_or_404, render
from UsersApp.models import Profile
from .models import Account


def permission_required(func):
    def blockFromNotAssigned(*args, **kwargs):
        request = args[0]
        pk = kwargs.get('pk', None)
        if pk is not None:
            users = get_object_or_404(Account, id=pk).get_users()
            if request.user.profile not in users:
                return render(request, "application/error/404.html")
        return func(*args, **kwargs)
    return blockFromNotAssigned