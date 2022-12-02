from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from datetime import datetime
from django.http import Http404  

# Create your views here.

def home(request):
    if request.user.is_authenticated:
    # Zalogowany użytkownik
        balance = 0
        acc = Account.objects.filter(owner=request.user.profile)
        transactions = Transaction.objects.filter(id_user=request.user.profile).order_by('-transaction_date')
        #Stworzenie słownika z kontami i ich bilansem
        for a in acc:
            balance += a.calculate_balance()

        context = {
            "transactions": transactions,
            'profile_balance': balance
        }
        return render(request, 'application/home/home-login.html', context)

    else:
    # Niezalogowany użytkownik
        return render(request, 'application/home/home-logout.html')

@login_required(login_url='login')
def allAccounts(request):
    accounts = Account.objects.all()
    user_accounts = accounts.filter(owner=request.user.profile)
    context = {'accounts': user_accounts}
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
            form.save()
            return redirect('all-accounts')
    context = {'form' : form}
    return render(request, 'application/account/account-form.html', context)

@login_required(login_url='login')
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    if account.owner != request.user.profile:
        raise Http404
    context = {'account': account}
    return render(request, 'application/account/account.html', context)

@login_required(login_url='login')
def addTransaction(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner != request.user.profile:
        raise Http404
    form = TransactionForm()
    context = {'account': account, 'form': form}

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = Transaction(
                id_account=account,
                id_user = request.user.profile,
                id_subcategory = form.cleaned_data['id_subcategory'],
                name = form.cleaned_data['name'],
                is_periodic = form.cleaned_data['is_periodic'],
                amount = form.cleaned_data['amount'],
                converted_amount = form.cleaned_data['amount'],
                transaction_date = datetime.now(),
                description = form.cleaned_data['description']         
            )
            transaction.save()
            return redirect('account', pk=account.id)
    return render(request, 'application/transaction/add.html', context)

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
    context = {'tr':transaction}
    if request.method == 'POST':
        transaction.delete()
        return redirect('account', pk=account.id)
    return render(request, 'application/transaction/del.html', context)

@login_required(login_url='login')
def editTransaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    form = TransactionForm(request.POST or None, instance = transaction)
    if form.is_valid():
        transaction.id_subcategory = form.cleaned_data['id_subcategory']
        transaction.name = form.cleaned_data['name']
        transaction.is_periodic = form.cleaned_data['is_periodic']
        transaction.amount = form.cleaned_data['amount']
        transaction.converted_amount = form.cleaned_data['amount']
        transaction.description = form.cleaned_data['description']  
        transaction.save()   
        return redirect('showTransaction', pk=transaction.id)
    return render(request, 'application/transaction/edit.html', {'form': form})

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