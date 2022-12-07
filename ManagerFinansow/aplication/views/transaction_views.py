from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from aplication.forms import TransactionForm
from datetime import datetime, date
from django.http import Http404  

@login_required(login_url='login')
def addExpense(request, pk):
    account = get_object_or_404(Account, id=pk)
    if account.owner != request.user.profile:
        raise Http404
    form = TransactionForm(scope="EXPENSE", owner=account.owner, initial={'currency': account.currency})
    context = {'account': account, 'form': form, 'option': "add", 'today': date.today().strftime("%Y-%m-%d")}

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None, owner=account.owner)
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
        form = TransactionForm(data=request.POST or None, scope="INCOME", owner=account.owner)
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
