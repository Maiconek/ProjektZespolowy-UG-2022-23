from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from django.db.models import Q
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from aplication.services import sumCurrency, updateTransactions
from django.db.models import Count

@method_decorator(login_required(login_url='login'), name='dispatch')
class Summary(ListView):
    template_name = 'application/summary.html'
    model = Category
    sum_exp = 0
    sum_inc = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum'] = self.sum_exp + self.sum_inc
        context['sum_exp'] = -self.sum_exp
        context['sum_inc'] = self.sum_inc
        return context

    def get_queryset(self):
        today = date.today()
        currency = self.request.user.profile.currency
        categories = super().get_queryset().filter(Q(owner=self.request.user.profile) | Q(owner=None))
        updateTransactions(Transaction.objects.filter(id_user=self.request.user.profile))
        transactions = Transaction.objects.filter(id_user=self.request.user.profile).exclude(
            id_account__in=User_Account.objects.values('id_account').annotate(Count('id')).order_by().filter(id__count__gt=1).values_list('id_account'))
        self.sum_exp = sumCurrency(transactions.filter(id_category__in=Category.objects.filter(scope='EXPENSE')).filter(transaction_date__lte=today), currency)
        self.sum_inc = sumCurrency(transactions.filter(id_category__in=Category.objects.filter(scope='INCOME')).filter(transaction_date__lte=today), currency)
        categories_with_sum = []
        for c in categories:
            s_c = sumCurrency(transactions.filter(id_category=c.id), currency)
            categories_with_sum.append((c, -s_c if c.scope == 'EXPENSE' else s_c, round(100 * s_c / (self.sum_exp if c.scope == 'EXPENSE' else self.sum_inc), 2)))
        return sorted(categories_with_sum, key=lambda tup: tup[1], reverse=True)
