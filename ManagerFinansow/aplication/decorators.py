from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from UsersApp.models import Profile
from .models import Account, User_Account, Transaction
from django.db.models import Q
from functools import wraps

def permission_required_account(access):
    def wrapper(func):
        @wraps(func)
        def blockFromNotAssigned(*args, **kwargs):
            request = args[0]
            pk = kwargs.get('pk', None)
            if pk is not None:
                account = get_object_or_404(Account, id=pk)
                users = account.get_users()
                if request.user.profile not in users:
                    return HttpResponseForbidden()
                if access == 'LIMITED':
                    if User_Account.objects.get(Q(id_account=account) & Q(id_user=request.user.profile)).access_level == 'LIMITED':
                        return HttpResponseForbidden()
            return func(*args, **kwargs)
        return blockFromNotAssigned
    return wrapper

def permission_required_transaction(access):
    def wrapper(func):
        @wraps(func)
        def blockFromNotAssigned(*args, **kwargs):
            request = args[0]
            pk = kwargs.get('pk', None)
            if pk is not None:
                transaction = get_object_or_404(Transaction, id=pk)
                account = transaction.id_account
                users = account.get_users()
                if request.user.profile not in users:
                    return HttpResponseForbidden()
                if access == 'LIMITED':
                    if User_Account.objects.get(Q(id_account=account) & Q(id_user=request.user.profile)).access_level == 'LIMITED':
                        return HttpResponseForbidden()
            return func(*args, **kwargs)
        return blockFromNotAssigned
    return wrapper