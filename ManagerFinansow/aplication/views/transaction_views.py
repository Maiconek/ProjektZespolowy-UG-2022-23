import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from aplication.models import *
from aplication.forms import TransactionForm
from datetime import date
from django.http import Http404  
from aplication.decorators import permission_required
from django.utils.decorators import method_decorator

class TransactionMixin(object): 
    def get_account(self, id):
        if id is not None:
            account = get_object_or_404(Account, id=id)
            return account

    def get_context_data(self, **kwargs):
        form = kwargs.get('form', None)
        id = kwargs.get('id', None)
        transaction = kwargs.get('transaction', None)
        accountless = kwargs.get('accountless', None)
        context = {}
        if transaction is not None:
            context['account'] = transaction.id_account
            context['transaction'] = transaction
        else:
            context['account'] = self.get_account(id)
        context['form'] = form
        context['today'] = date.today().strftime("%Y-%m-%d")
        context['option'] = kwargs.get('option', None)
        context['subcategories'] = form.fields['id_subcategory'].queryset
        if accountless is None:
            context['accountless'] = '1' if id is None else '0' 
        else:
            context['accountless'] = accountless
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(permission_required, name='dispatch')
class TransactionAdd(View, TransactionMixin):
    template_name = 'application/transaction/form.html'
    form_class = TransactionForm
    
    def get(self, request, type, pk=None):
        account = self.get_account(pk)
        form = self.form_class(
            scope=type.upper(), owner=request.user.profile, 
            initial={'currency': request.user.profile.currency if pk is None else account.currency,
            'id_account': account if pk is not None else None})

        context = self.get_context_data(form=form, id=pk, option='add')
        return render(request, self.template_name, context)
        
    def post(self, request, type, pk=None):
        form = self.form_class(data=request.POST or None, scope = type.upper(), owner=request.user.profile)
        context = self.get_context_data(form=form, id=pk, option='add')
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.id_user = request.user.profile
            transaction.save()
            if pk is not None:
                return redirect('account', pk=transaction.id_account.id)
            else:
                return redirect('login')
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class TransactionEdit(View, TransactionMixin):
    template_name = 'application/transaction/form.html'
    form_class = TransactionForm
    
    def get(self, request, pk, accountless=0):
        transaction = get_object_or_404(Transaction, id=pk)
        form = TransactionForm(scope = transaction.id_category.scope, owner=transaction.id_account.owner, instance = transaction)
        context = self.get_context_data(form=form, transaction=transaction, option='edit', accountless=accountless)
        return render(request, self.template_name, context)
        
    def post(self, request, pk, accountless=0):
        transaction = get_object_or_404(Transaction, id=pk)
        form = TransactionForm(data=request.POST or None, scope = transaction.id_category.scope, 
                                owner=transaction.id_account.owner, instance = transaction)
        context = self.get_context_data(form=form, transaction=transaction, option='edit', accountless=accountless)
        if form.is_valid():
            form.save()
            return redirect('showTransaction', pk=transaction.id, accountless=accountless)
        return render(request, self.template_name, context)

class TransactionDuplicate(TransactionEdit):
    def post(self, request, pk, accountless=0):
        transaction = get_object_or_404(Transaction, id=pk)
        form = TransactionForm(data=request.POST or None, scope = transaction.id_category.scope, 
                                owner=transaction.id_account.owner, instance = transaction)
        context = self.get_context_data(form=form, transaction=transaction, option='edit', accountless=accountless)
        if form.is_valid():
            newTransaction = form.save(commit=False)
            newTransaction.id = None
            newTransaction.save()
            if accountless == '0':
                return  redirect('account', pk=transaction.id_account.id)
            else:
                return redirect('login')
        return render(request, self.template_name, context)

@login_required(login_url='login')
def showTransaction(request, pk, accountless=0):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction.id_account.owner != request.user.profile:
        raise Http404
    context = {'tr':transaction, 'accountless': accountless, 'today':date.today()}
    action = request.GET.get('action')
    if action is not None:
        if action == 'skip':
            transaction.transaction_date = transaction.get_next_date()
            transaction.save()
        if action == 'move':
            if transaction.repeat is not None:
                newTransaction = copy.copy(transaction)
                newTransaction.id = None
                newTransaction.repeat = None
                newTransaction.transaction_date = date.today()
                newTransaction.save()
                transaction.transaction_date = transaction.get_next_date()
                transaction.save()
            else:
                transaction.transaction_date = date.today()
                transaction.save()
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
