from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import AccountForm

# Create your views here.

def home(request):
    if request.user.is_authenticated:
    # Zalogowany użytkownik
        balance = 0
        acc = Account.objects.filter(owner=request.user.profile)
        #Stworzenie słownika z kontami i ich bilansem
        for a in acc:
            balance += a.calculate_balance()

        context = {
            "accounts": acc,
            'profile_balance': balance
        }
        return render(request, 'application/home-login.html', context)

    else:
    # Niezalogowany użytkownik
        return render(request, 'application/home-logout.html')

@login_required(login_url='login')
def allAccounts(request):
    accounts = Account.objects.all()
    user_accounts = accounts.filter(owner=request.user.profile)
    context = {'accounts': user_accounts}
    return render(request, 'application/all-accounts.html', context)

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
    return render(request, 'application/account-form.html', context)

@login_required(login_url='login')
def showAccount(request, pk):
    account = Account.objects.get(id=pk)
    context = {'account': account}
    return render(request, 'application/account.html', context)