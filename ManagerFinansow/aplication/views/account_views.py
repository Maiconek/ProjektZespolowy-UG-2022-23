import copy
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from aplication.decorators import permission_required
from aplication.models import *
from aplication.forms import AccountForm, InviteForm
from django.db.models import Q
from dateutil.relativedelta import relativedelta

def prepareTransactions(all_transactions):
    today = date.today()
    repeating = all_transactions.filter(~Q(repeat=None))
    for tr in repeating:
        _date = tr.transaction_date
        while _date <= today:
            newTransaction = copy.copy(tr)
            newTransaction.id = None
            newTransaction.repeat = None
            newTransaction.save()
            _date = tr.transaction_date = tr.get_next_date()
        tr.save()

    count = 0
    nextMonth = today + relativedelta(months=+1)
    for tr in repeating:
        _date = tr.transaction_date
        while _date <= nextMonth:
            count += 1
            newTransaction = copy.copy(tr)
            _date = tr.transaction_date = tr.get_next_date()

    dates = []; fut_dates = []
    for t in all_transactions:
        if t.transaction_date <= today:
            if t.transaction_date not in dates:
                dates.append(t.transaction_date)
        elif t.transaction_date not in fut_dates:
            fut_dates.append(t.transaction_date)
    count += len(fut_dates) - len(repeating)

    def prepare_transactions_list(dates):
        transactions = []; values = []
        for dt in dates:
            values.append(sum(tr.converted_amount for tr in all_transactions if tr.transaction_date == dt))
            transactions.append(reversed([tr for tr in all_transactions if tr.transaction_date == dt]))
        return transactions, values
        
    transactions = prepare_transactions_list(dates)
    daily = zip(dates, *transactions)
    balance = sum(v for v in transactions[1])
    future = zip(fut_dates, *prepare_transactions_list(fut_dates))
    return daily, balance, future, count

@login_required(login_url='login')
def showAllTransactions(request):
    transactions = Transaction.objects.filter(id_user=request.user.profile).order_by('-transaction_date')
    prepared = list(prepareTransactions(transactions))
    context = {
        'profile': request.user.profile,
        'daily': prepared[0],
        'balance': prepared[1],
        'future': prepared[2],
        'count': prepared[3]
    }
    return render(request, 'application/home/home-login.html', context)

@login_required(login_url='login')
@permission_required
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    users = User_Account.objects.filter(id_account=account).exclude(id_user=request.user.profile)
    transactions = Transaction.objects.filter(id_account=account).order_by('-transaction_date')
    prepared = list(prepareTransactions(transactions))
    context = {
        'account': account, 
        'users': users,
        'daily': prepared[0],  
        'balance': prepared[1],
        'future': prepared[2],
        'count': prepared[3]
    }
    return render(request, 'application/account/account.html', context)

@login_required(login_url='login')
def allAccounts(request):
    user_accounts = User_Account.objects.filter(id_user = request.user.profile.id)
    accounts = []
    for ua in user_accounts:
        accounts.append(Account.objects.get(id=ua.id_account.id))
    context = {'accounts': accounts}
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
