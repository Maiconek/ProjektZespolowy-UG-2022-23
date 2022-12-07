from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import AccountForm, TransactionForm
from datetime import datetime, date
from django.http import Http404  

# Create your views here.

def home(request):
    if request.user.is_authenticated:
    # Zalogowany użytkownik
        balance = 0
        user_accounts = User_Account.objects.filter(id_user = request.user.profile.id)
        accounts = []
        for ua in user_accounts:
            if ua.id_account.owner == request.user.profile and ua.id_account.is_shared == False:
                accounts.append(ua.id_account)
        all_transactions = Transaction.objects.filter(id_user=request.user.profile).order_by('-transaction_date')
        dates = []
        transactions = []
        for t in all_transactions:
            if t.id_account.is_shared == False:
                transactions.append(t)
                if t.transaction_date not in dates:
                    dates.append(t.transaction_date)
        for acc in accounts:
            balance += acc.calculate_balance()

        context = {
            'profile': request.user.profile,
            'dates': dates,
            "transactions": transactions,
            'profile_balance': balance
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
    context = {'form' : form, 'option': "add"}
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
    context = {'form' : form, 'option': "edit"}
    return render(request, 'application/account/account-form.html', context)

@login_required(login_url='login')
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    if account.owner != request.user.profile:
        raise Http404
    transactions = Transaction.objects.filter(id_account=account).order_by('-transaction_date')
    dates = []
    for t in transactions:
        if t.transaction_date not in dates:
            dates.append(t.transaction_date)
    context = {'account': account, 'transactions': transactions, 'dates': dates}
    return render(request, 'application/account/account.html', context)

@login_required(login_url='login')
def delAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner == request.user.profile:
        account.delete()
    return redirect('all-accounts')


@login_required(login_url='login')
def addExpense(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner != request.user.profile:
        raise Http404
    form = TransactionForm(scope="EXPENSE", owner=account.owner, initial={'currency': account.currency})
    context = {'account': account, 'form': form, 'option': "add", 'today': date.today().strftime("%Y-%m-%d")}

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.id_account=account
            transaction.id_user = request.user.profile
            transaction.transaction_date = datetime.now()
            transaction.amount = -form.cleaned_data['amount']
            transaction.converted_amount = -form.cleaned_data['amount']    
            _date = request.POST['date']
            transaction.transaction_date = _date   
            transaction.save()
            return redirect('account', pk=account.id)
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
def addIncome(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner != request.user.profile:
        raise Http404
    form = TransactionForm(scope = "INCOME", owner=account.owner, initial={'currency': account.currency})
    context = {'account': account, 'form': form, 'option': "add", 'today': date.today().strftime("%Y-%m-%d")}

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None, scope="INCOME")
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.id_account=account
            transaction.id_user = request.user.profile
            transaction.transaction_date = datetime.now()
            transaction.converted_amount = form.cleaned_data['amount']     
            _date = request.POST['date']
            transaction.transaction_date = _date 
            transaction.save()
            return redirect('account', pk=account.id)
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
def duplicate(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    transaction.id = None
    form = TransactionForm(data=request.POST or None, scope = transaction.id_category.scope, 
                            owner=transaction.id_account.owner, instance=transaction)
    if form.is_valid():
        transaction.converted_amount = form.cleaned_data['amount']
        _date = request.POST['date']
        transaction.transaction_date = _date 
        transaction.save()
        return  redirect('account', pk=transaction.id_account.id)
    return render(request, 'application/transaction/form.html', {
                                                                'form': form, 
                                                                'account': transaction.id_account, 
                                                                'option': "add", 
                                                                'transaction': transaction,
                                                                'today': date.today().strftime("%Y-%m-%d")})

@login_required(login_url='login')
def showTransaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    context = {'tr':transaction}
    return render(request, 'application/transaction/show.html', context)

@login_required(login_url='login')
def delTransaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    account = transaction.id_account
    transaction.delete()
    return redirect('account', pk=account.id)

@login_required(login_url='login')
def editTransaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    form = TransactionForm(data=request.POST or None, scope = transaction.id_category.scope, 
                            owner=transaction.id_account.owner, instance = transaction)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.converted_amount = form.cleaned_data['amount']
        _date = request.POST['date']
        transaction.transaction_date = _date
        transaction.save()   
        return redirect('showTransaction', pk=transaction.id)
    return render(request, 'application/transaction/form.html', {
                                                                'form': form, 
                                                                'account': transaction.id_account, 
                                                                'option': "edit", 
                                                                'transaction': transaction})

@login_required(login_url='login')
def joinAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.is_shared == False:
        raise Http404
    #if nie powinieneś mieć dostępu
    #raise Http404
    context = {'account': account}
    if request.method == 'POST':
        #Dodaj do konta użytkownika
        account.save()
        return redirect('account', pk=account.id)
    return render(request, 'application/account/account-join.html', context)

def error404(request, exception):
    return render(request, 'application/error/404.html')