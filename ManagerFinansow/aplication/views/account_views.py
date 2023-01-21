from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from aplication.decorators import permission_required_account
from aplication.models import *
from aplication.forms import AccountForm, InviteForm
from aplication.services import prepareTransactions, updateTransactions, sumCurrency
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.http import HttpResponseForbidden

class Home(TemplateView):
    template_name = 'application/home/home-logout.html'

    def get(self, request):
        if request.user.is_authenticated:
            return showAllTransactions(request)
        else:
            return render(request, self.template_name)

@login_required(login_url='login')
def showAllTransactions(request):
    updateTransactions(Transaction.objects.filter(id_user=request.user.profile))
    transactions = Transaction.objects.filter(id_user=request.user.profile)
    page_number = request.GET.get('page')
    prepared = prepareTransactions(transactions, request.user.profile.currency, page_number, 20)

    context = {
        'profile': request.user.profile,
        'daily': prepared[0],
        'balance': prepared[1],
        'future': prepared[2],
        'count': prepared[3],
        'page_obj': prepared[4]
    }
    return render(request, 'application/home/home-login.html', context)

@login_required(login_url='login')
@permission_required_account('FULL')
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    users = User_Account.objects.filter(id_account=account).exclude(id_user=request.user.profile)
    updateTransactions(Transaction.objects.filter(id_account=account))
    transactions = Transaction.objects.filter(id_account=account)
    page_number = request.GET.get('page')
    prepared = prepareTransactions(transactions, account.currency, page_number, 20)
    context = {
        'account': account, 
        'users': users,
        'daily': prepared[0],  
        'balance': prepared[1],
        'future': prepared[2],
        'count': prepared[3],
        'page_obj': prepared[4],
        'fullAccess': User_Account.objects.get(Q(id_account=account) & Q(id_user=request.user.profile)).access_level == 'FULL'
    }
    return render(request, 'application/account/account.html', context)

@login_required(login_url='login')
def allAccounts(request):
    user_accounts = User_Account.objects.filter(id_user = request.user.profile.id)
    today = date.today()
    accounts = []
    accountAndSum = []
    for ua in user_accounts:
        accounts.append(Account.objects.get(id=ua.id_account.id))
    for account in accounts:
        transactions = Transaction.objects.filter(id_account=account)
        updateTransactions(transactions)
        transactions = Transaction.objects.filter(id_account=account).filter(transaction_date__lte=today)
        accountAndSum.append((account, sumCurrency(transactions, account.currency)))
    
    paginator = Paginator(accountAndSum, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'application/account/all-accounts.html', context)

@login_required(login_url='login')
def createAccount(request):
    profile = request.user.profile
    form = AccountForm()

    if request.method == "POST":
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = profile
            account.save()
            account_user = User_Account(profile.id, account.id, 'FULL')
            account_user.save()
            return redirect('all-accounts')
    context = {'form': form, 'option': "add"}
    return render(request, 'application/account/account-form.html', context)

@login_required(login_url='login')
@permission_required_account('LIMITED')
def editAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    form = AccountForm(request.POST or None, instance=account)
    if request.method == "POST":
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            return redirect('account', pk=account.id)
    context = {'form' : form, 'option': "edit", 'account': account}
    return render(request, 'application/account/account-form.html', context)

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

def error404(request, exception):
    return render(request, 'application/error/404.html')

@login_required(login_url='login')
@permission_required_account('LIMITED')
def delAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner == request.user.profile:
        account.delete()
    return redirect('all-accounts')

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

