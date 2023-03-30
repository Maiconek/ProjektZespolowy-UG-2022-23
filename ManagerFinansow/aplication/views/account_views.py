from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from aplication.decorators import permission_required_account
from aplication.models import *
from aplication.forms import AccountForm, InviteForm
from aplication.services import prepareTransactions, updateTransactions, sumCurrency
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.db.models import Count
from UsersApp.models import Category

def error404(request, exception):
    return render(request, 'application/error/404.html')

class Home(TemplateView):
    template_name = 'application/home/home-logout.html'

    def get(self, request):
        if request.user.is_authenticated:
            return showAllTransactions(request)
        else:
            return render(request, self.template_name)
        
def save_total(request):
    total = request.GET.get('total')
    if total is not None:
        request.user.profile.total_transactions = int(total)
        request.user.profile.save()

@login_required(login_url='login')
def showAllTransactions(request):
    updateTransactions(Transaction.objects.filter(id_user=request.user.profile))
    transactions = Transaction.objects.filter(id_user=request.user.profile).exclude(
        id_account__in=User_Account.objects.values('id_account').annotate(Count('id')).order_by().filter(id__count__gt=1).values_list('id_account'))
    page_number = request.GET.get('page')
    save_total(request)
    prepared = prepareTransactions(transactions, request.user.profile.currency, page_number, request.user.profile.total_transactions)

    context = {
        'profile': request.user.profile,
        'categories': Category.objects.filter(Q(owner=None) | Q(owner=request.user.profile)),
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
    updateTransactions(Transaction.objects.filter(Q(id_account=account) | Q(Transfer___account_to = account)))
    transactions = Transaction.objects.filter(Q(id_account=account) | Q(Transfer___account_to = account))
    page_number = request.GET.get('page')
    save_total(request)
    prepared = prepareTransactions(transactions, account.currency, page_number, request.user.profile.total_transactions, account)
    categories_alphabetical = Category.objects.filter(Q(owner=None) | Q(owner=request.user.profile)).order_by('name')
    context = {
        'account': account, 
        'categories': categories_alphabetical,
        'daily': prepared[0],  
        'balance': prepared[1],
        'future': prepared[2],
        'count': prepared[3],
        'page_obj': prepared[4],
        'fullAccess': User_Account.objects.get(Q(id_account=account) & Q(id_user=request.user.profile)).access_level == 'FULL',
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
        updateTransactions(Transaction.objects.filter(Q(id_account=account) | Q(Transfer___account_to = account)))
        transactions = Transaction.objects.filter(Q(id_account=account) | Q(Transfer___account_to = account)).filter(transaction_date__lte=today)
        accountAndSum.append((account, sumCurrency(transactions, account.currency, account)))
    
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
@permission_required_account('LIMITED')
def delAccount(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner == request.user.profile:
        account.delete()
    return redirect('all-accounts')

