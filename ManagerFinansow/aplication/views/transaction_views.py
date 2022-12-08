from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from aplication.forms import TransactionForm
from datetime import datetime, date
from django.http import Http404  

@login_required(login_url='login')
def addExpense(request, pk=None):
    if pk is not None:
        account = get_object_or_404(Account, id=pk)
        if account.owner != request.user.profile:
            raise Http404
    form = TransactionForm(scope="EXPENSE", owner=request.user.profile, initial={'currency': request.user.profile.currency,
                                                                                'id_account': account if pk is not None else None})
    context = {'form': form, 'option': "add", 'today': date.today().strftime("%Y-%m-%d")}
    if pk is not None:
        context.update({'account': account})
    else:
        context.update({'account': None})

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None, owner=request.user.profile)
        if form.is_valid():
            print(form.cleaned_data)
            transaction = form.save(commit=False)
            transaction.id_user = request.user.profile
            transaction.transaction_date = datetime.now()
            transaction.amount = -form.cleaned_data['amount']
            transaction.converted_amount = -form.cleaned_data['amount']    
            _date = request.POST['date']
            transaction.transaction_date = _date   
            transaction.save()
            return redirect('account', pk=transaction.id_account.id)
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
def addIncome(request, pk=None):
    if pk is not None:
        account = get_object_or_404(Account, id=pk)
        if account.owner != request.user.profile:
            raise Http404
    form = TransactionForm(scope = "INCOME", owner=request.user.profile, initial={'currency': request.user.profile.currency,
                                                                                'id_account': account if pk is not None else None})
    context = {'form': form, 'option': "add", 'today': date.today().strftime("%Y-%m-%d")}
    if pk is not None:
        context.update({'account': account})
    else:
        context.update({'account': None})

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None, scope="INCOME", owner=request.user.profile)
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
                            owner=transaction.id_account.owner, instance=transaction, 
                            initial={'amount': -transaction.amount if transaction.id_category.scope=="EXPENSE" else transaction.amount})
    if form.is_valid():
        form.save(commit=False)
        amnt = form.cleaned_data['amount']
        transaction.amount = -amnt if transaction.id_category.scope=="EXPENSE" else amnt
        transaction.converted_amount = -amnt if transaction.id_category.scope=="EXPENSE" else amnt
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
                            owner=transaction.id_account.owner, instance = transaction,
                            initial={'amount': -transaction.amount if transaction.id_category.scope=="EXPENSE" else transaction.amount})
    if form.is_valid():
        transaction = form.save(commit=False)
        amnt = form.cleaned_data['amount']
        transaction.amount = -amnt if transaction.id_category.scope=="EXPENSE" else amnt
        transaction.converted_amount = -amnt if transaction.id_category.scope=="EXPENSE" else amnt
        _date = request.POST['date']
        transaction.transaction_date = _date
        transaction.save()   
        return redirect('showTransaction', pk=transaction.id)
    return render(request, 'application/transaction/form.html', {
                                                                'form': form, 
                                                                'account': transaction.id_account, 
                                                                'option': "edit", 
                                                                'transaction': transaction})
