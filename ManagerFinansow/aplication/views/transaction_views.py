from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from aplication.forms import TransactionForm
from datetime import datetime, date
from django.http import Http404  
from aplication.decorators import permission_required

@login_required(login_url='login')
@permission_required
def addExpense(request, pk=None):
    if pk is not None:
        account = get_object_or_404(Account, id=pk)

    form = TransactionForm(scope="EXPENSE", owner=request.user.profile, 
                            initial={'currency': request.user.profile.currency if pk is None else account.currency,
                                    'id_account': account if pk is not None else None})
    context = {
        'form': form, 
        'option': "add", 
        'today': date.today().strftime("%Y-%m-%d"),
        'accountless': '1' if pk == None else '0', 
        'subcategories': form.fields['id_subcategory'].queryset}

    if pk is not None:
        context.update({'account': account})
    else:
        context.update({'account': None})

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None, owner=request.user.profile)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.id_user = request.user.profile
            transaction.save()
            if pk is not None:
                return redirect('account', pk=transaction.id_account.id)
            else:
                return redirect('login')
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
@permission_required
def addIncome(request, pk=None):
    if pk is not None:
        account = get_object_or_404(Account, id=pk)

    form = TransactionForm(scope = "INCOME", owner=request.user.profile, 
                            initial={'currency': request.user.profile.currency if pk is None else account.currency,
                                    'id_account': account if pk is not None else None})
    context = {
        'form': form, 
        'option': "add", 
        'today': date.today().strftime("%Y-%m-%d"), 
        'accountless': '1' if pk == None else '0', 
        'subcategories': form.fields['id_subcategory'].queryset}

    if pk is not None:
        context.update({'account': account})
    else:
        context.update({'account': None})

    if request.method == "POST":
        form = TransactionForm(data=request.POST or None, scope="INCOME", owner=request.user.profile)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.id_user = request.user.profile
            transaction.save()
            if pk is not None:
                return redirect('account', pk=transaction.id_account.id)
            else:
                return redirect('login')
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
def duplicate(request, pk, accountless=0):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    transaction.id = None
    form = TransactionForm(scope = transaction.id_category.scope, owner=transaction.id_account.owner, instance=transaction, 
                            initial={'amount': -transaction.amount if transaction.id_category.scope=="EXPENSE" 
                            else transaction.amount})
    if request.method == 'POST':
        form = TransactionForm(data=request.POST or None, scope = transaction.id_category.scope, 
                                owner=transaction.id_account.owner, instance = transaction)
        if form.is_valid():
            newTransaction = form.save(commit=False)
            newTransaction.save()
        if accountless == '0':
            return  redirect('account', pk=transaction.id_account.id)
        else:
            return redirect('login')
    context = {
        'form': form, 
        'account': transaction.id_account, 
        'option': "add", 
        'transaction': transaction,
        'accountless': accountless,
        'subcategories': form.fields['id_subcategory'].queryset,
        'today': date.today().strftime("%Y-%m-%d")}
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
def editTransaction(request, pk, accountless=0):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    form = TransactionForm(scope = transaction.id_category.scope, owner=transaction.id_account.owner, instance = transaction,
                            initial={'amount': -transaction.amount if transaction.id_category.scope=="EXPENSE" 
                            else transaction.amount})
    if request.method == 'POST':
        form = TransactionForm(data=request.POST or None, scope = transaction.id_category.scope, 
                                owner=transaction.id_account.owner, instance = transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            return redirect('showTransaction', pk=transaction.id, accountless=accountless)

    context = {
        'form': form, 
        'account': transaction.id_account, 
        'option': "edit", 
        'transaction': transaction,
        'accountless': accountless,
        'subcategories': form.fields['id_subcategory'].queryset}
    return render(request, 'application/transaction/form.html', context)

@login_required(login_url='login')
def showTransaction(request, pk, accountless=0):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    context = {'tr':transaction, 'accountless': accountless}
    return render(request, 'application/transaction/show.html', context)

@login_required(login_url='login')
def delTransaction(request, pk, accountless=0):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    account = transaction.id_account
    transaction.delete()
    if accountless == '0':
        return redirect('account', pk=account.id)
    else:
        return redirect('login')
