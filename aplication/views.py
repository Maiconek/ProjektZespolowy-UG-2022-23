from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import AccountForm

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'application/home-login.html')
    else:
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