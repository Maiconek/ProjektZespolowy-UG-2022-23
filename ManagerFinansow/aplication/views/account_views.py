from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from aplication.forms import AccountForm
from django.http import Http404  

def home(request):
    if request.user.is_authenticated:
    # Zalogowany użytkownik
        all_transactions = Transaction.objects.filter(id_user=request.user.profile).order_by('-transaction_date')
        dates = []
        transactions = []
        values = []
        for t in all_transactions:
            if t.transaction_date not in dates:
                dates.append(t.transaction_date)

        for dt in dates:
            values.append(sum(tr.converted_amount for tr in all_transactions if tr.transaction_date == dt))
            transactions.append(reversed([tr for tr in all_transactions if tr.transaction_date == dt]))
            
        daily = zip(dates, transactions, values)
        balance = sum(v for v in values)

        context = {
            'profile': request.user.profile,
            'daily': daily,
            'profile_balance': balance,
        }
        return render(request, 'application/home/home-login.html', context)

    else:
    # Niezalogowany użytkownik
        return render(request, 'application/home/home-logout.html')

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
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    if account.owner != request.user.profile:
        raise Http404
    all_transactions = Transaction.objects.filter(id_account=account).order_by('-transaction_date')
    dates = []
    transactions = []
    values = []
    for t in all_transactions:
        if t.transaction_date not in dates:
            dates.append(t.transaction_date)

    for dt in dates:
        values.append(sum(tr.converted_amount for tr in all_transactions if tr.transaction_date == dt))
        transactions.append(reversed([tr for tr in all_transactions if tr.transaction_date == dt]))
        
    daily = zip(dates, transactions, values)

    context = {'account': account, 'daily': daily, 'dates': dates}
    return render(request, 'application/account/account.html', context)

@login_required(login_url='login')
def joinAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.is_shared == False:
        raise Http404
    context = {'account': account}
    if request.method == 'POST':
        #Dodaj do konta użytkownika
        account.save()
        return redirect('account', pk=account.id)
    return render(request, 'application/account/account-join.html', context)

def error404(request, exception):
    return render(request, 'application/error/404.html')


@login_required(login_url='login')
def delAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner == request.user.profile:
        account.delete()
    return redirect('all-accounts')

