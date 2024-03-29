import copy
from datetime import date
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from currency_converter import CurrencyConverter, ECB_URL
from django.core.paginator import Paginator
from django.db.models import Sum
from aplication.models import Transfer
#from forex_python.converter import CurrencyRates

#c = CurrencyRates(force_decimal=True)
c = CurrencyConverter(ECB_URL, decimal=True, fallback_on_wrong_date=True, fallback_on_missing_rate=True, fallback_on_missing_rate_method='last_known')

def sumCurrency(all_transactions, currency, account=None):
    sum = 0
    today = date.today()
    for tr in all_transactions.filter(~Q(currency=currency)).not_instance_of(Transfer):
        if tr.id_category.scope == 'EXPENSE' and tr.transaction_date < today:
            sum += c.convert(tr.amount, tr.currency.access_name, currency.access_name, date=tr.transaction_date)
        else:
            sum += c.convert(tr.amount, tr.currency.access_name, currency.access_name)
    matchingCurrencySum = all_transactions.filter(Q(currency=currency)).not_instance_of(Transfer).aggregate(Sum('amount'))['amount__sum']
    sum += matchingCurrencySum if matchingCurrencySum is not None else 0
    def transfersAgainstAccount():
        sum = 0
        for tr in all_transactions.instance_of(Transfer):
            amount = c.convert(tr.amount, tr.currency.access_name, currency.access_name) if tr.currency.access_name != currency.access_name else tr.amount
            sum += -amount if tr.account_from == account else amount
        return sum
    sum += transfersAgainstAccount() if account is not None else 0
    return round(sum, 2)

def updateTransactions(all_transactions):
    today = date.today()
    repeating = all_transactions.filter(~Q(repeat=None))
    for tr in repeating:
        _date = tr.transaction_date
        if _date <= today:
            while _date <= today:
                newTransaction = copy.copy(tr)
                newTransaction.id = None
                newTransaction.pk = None
                newTransaction.repeat = None
                newTransaction.save()
                _date = tr.transaction_date = tr.get_next_date()
            tr.save()

def prepareTransactions(all_transactions, currency, page, size, account=None):
    today = date.today()
    paginator = Paginator(all_transactions.filter(transaction_date__lte=today).order_by('-transaction_date'), size)
    page_obj = paginator.get_page(page)
    futureTransactions = all_transactions.filter(transaction_date__gt=today).order_by('-transaction_date')
    
    repeating = all_transactions.filter(~Q(repeat=None))
    count = 0
    nextMonth = today + relativedelta(months=+1)
    for tr in repeating:
        _date = tr.transaction_date
        while _date <= nextMonth:
            count += 1
            _date = tr.transaction_date = tr.get_next_date()

    dates = set([tr.transaction_date for tr in page_obj]); 
    fut_dates = set([tr.transaction_date for tr in futureTransactions])

    dates, fut_dates = sorted(dates, reverse=True), sorted(fut_dates, reverse=True)
    count += len(fut_dates) - len(repeating)

    def prepare_transactions_list(dates):
        transactions = []; values = []
        for dt in dates:
            temp = all_transactions.filter(transaction_date=dt)
            values.append(sumCurrency(temp, currency))
            transactions.append(reversed(temp))
        return transactions, values
        
    transactions = prepare_transactions_list(dates)
    daily = zip(dates, *transactions)
    balance = sumCurrency(all_transactions.filter(transaction_date__lte=today), currency, account)
    future = zip(fut_dates, *prepare_transactions_list(fut_dates))
    return daily, balance, future, count, page_obj