from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from aplication.models import *
from django.db.models import Q
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from aplication.services import sumCurrency

@method_decorator(login_required(login_url='login'), name='dispatch')
class Summary(ListView):
    template_name = 'application/summary.html'
    model = Category

    def get_queryset(self):
        currency = self.request.user.profile.currency
        categories = super().get_queryset().filter(Q(owner=self.request.user.profile) | Q(owner=None))
        sum_exp = sumCurrency(Transaction.objects.filter(Q(id_user=self.request.user.profile) & 
                                Q(id_category__in=Category.objects.filter(scope='EXPENSE'))), currency)
        sum_inc = sumCurrency(Transaction.objects.filter(Q(id_user=self.request.user.profile) & 
                                Q(id_category__in=Category.objects.filter(scope='INCOME'))), currency)
        categories_with_sum = []
        for c in categories:
            s_c = sumCurrency(Transaction.objects.filter(Q(id_category=c.id) & Q(id_user=self.request.user.profile)), currency)
            categories_with_sum.append((c, abs(s_c), round(100 * s_c / (sum_exp if c.scope == 'EXPENSE' else sum_inc), 2)))
        return categories_with_sum
