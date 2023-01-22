from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from aplication.models import Invitation, User_Account, Account
from django.views.generic.list import ListView
from UsersApp.models import Profile

@login_required(login_url='login')
def joinAccount(request, pk):
    invitation = get_object_or_404(Invitation, id=pk)
    if invitation.userTo.id != request.user.profile.id:
        return HttpResponseForbidden
    context = {'invitation': invitation}
    if request.method == 'POST':
        account_user = User_Account(request.user.profile.id, invitation.id_account.id, invitation.access_level)
        account_user.save()
        invitation.delete()
        return redirect('account', pk=invitation.id_account.id)
    return render(request, 'application/account/account-join.html', context)

class ManageUsers(ListView):
    template_name = 'application/account/users.html'
    model = Profile

    def get_queryset(self):
        account = get_object_or_404(Account, id=self.kwargs.get('pk', None))
        users = super().get_queryset().filter(id__in=User_Account.objects.filter(id_account=account)
        .exclude(id_user=self.request.user.profile).values_list('id_user'))
        return users

    def get_context_data(self):
        account = get_object_or_404(Account, id=self.kwargs.get('pk', None))
        context = super().get_context_data()
        if account.owner == self.request.user.profile:
            context['owner'] = True
        else:
            context['owner'] = False
        context['account'] = account
        return context

def deleteUserAccount(request, pk, pk1):
    account = get_object_or_404(Account, id=pk)
    user = get_object_or_404(Profile, id=pk1)
    toDel = User_Account.objects.get(id_account=account, id_user=user)
    toDel.delete()
    if user != request.user.profile:
        return redirect('users', pk=account.id)
    else:
        return redirect('all-accounts')

