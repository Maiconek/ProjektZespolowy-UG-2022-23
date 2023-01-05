from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from aplication.decorators import permission_required
from aplication.models import *
from aplication.forms import AccountForm, InviteForm
from aplication.services import prepareTransactions, updateTransactions, setCurrency
from django.core.paginator import Paginator


@login_required(login_url='login')
def showAllTransactions(request):
    updateTransactions(Transaction.objects.filter(id_user=request.user.profile))
    transactions = Transaction.objects.filter(id_user=request.user.profile)
    page_number = request.GET.get('page')
    prepared = prepareTransactions(transactions, request.user.profile.currency, page_number, 10)

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
@permission_required
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    users = User_Account.objects.filter(id_account=account).exclude(id_user=request.user.profile)
    updateTransactions(Transaction.objects.filter(id_account=account))
    transactions = Transaction.objects.filter(id_account=account)
    page_number = request.GET.get('page')
    prepared = prepareTransactions(transactions, account.currency, page_number, 10)
    context = {
        'account': account, 
        'users': users,
        'daily': prepared[0],  
        'balance': prepared[1],
        'future': prepared[2],
        'count': prepared[3],
        'page_obj': prepared[4]
    }
    return render(request, 'application/account/account.html', context)

@login_required(login_url='login')
def allAccounts(request):
    user_accounts = User_Account.objects.filter(id_user = request.user.profile.id)
    accounts = []
    accountAndSum = []
    for ua in user_accounts:
        accounts.append(Account.objects.get(id=ua.id_account.id))
    for account in accounts:
        transactions = Transaction.objects.filter(id_account=account)
        updateTransactions(transactions)
        transactions = Transaction.objects.filter(id_account=account).filter(repeat=None)
        transactions = setCurrency(transactions, account.currency)
        accountAndSum.append((account, sum(tr.converted_amount for tr in transactions)))
    
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
            account_user = User_Account(profile.id, account.id, 0)
            account_user.save()
            return redirect('all-accounts')
    context = {'form': form, 'option': "add"}
    return render(request, 'application/account/account-form.html', context)

@login_required(login_url='login')
@permission_required
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
@permission_required
def delAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner == request.user.profile:
        account.delete()
    return redirect('all-accounts')

@login_required(login_url='login')
@permission_required
def invite(request, pk):
    account = get_object_or_404(Account, id=pk)
    form = InviteForm(account=account)
    if request.method == "POST":
        form = InviteForm(data=request.POST, account=account)
        if form.is_valid():
            invitation = Invitation(
                userFrom = request.user.profile,
                userTo = form.cleaned_data['profile'].profile,
                id_account=account
            )
            invitation.save()
            return redirect('account', pk=account.id)
    context = {'account': account, 'form': form}
    return render(request, 'application/account/account-invite.html', context)
