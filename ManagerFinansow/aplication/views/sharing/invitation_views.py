from django.contrib.auth.decorators import login_required
from aplication.forms import InviteForm
from aplication.models import Account, Invitation
from aplication.decorators import permission_required_account
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

@login_required(login_url='login')
@permission_required_account('LIMITED')
def invite(request, pk):
    account = get_object_or_404(Account, id=pk)
    form = InviteForm(account=account)
    if request.method == "POST":
        form = InviteForm(data=request.POST, account=account)
        if form.is_valid():
            invitation = Invitation(
                userFrom = request.user.profile,
                userTo = form.cleaned_data['profile'].profile,
                id_account =account,
                access_level = form.cleaned_data['access_level']
            )
            invitation.save()
            return redirect('account', pk=account.id)
    context = {'account': account, 'form': form}
    return render(request, 'application/account/account-invite.html', context)

@login_required(login_url='login')
def deleteInvitation(request, pk):
    invitation = get_object_or_404(Invitation, id=pk)
    if invitation.userTo.id != request.user.profile.id and invitation.userFrom.id != request.user.profile.id:
        return HttpResponseForbidden()
    invitation.delete()
    return redirect('profile')