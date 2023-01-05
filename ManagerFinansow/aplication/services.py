import copy
from datetime import date
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from currency_converter import CurrencyConverter, ECB_URL
from django.core.paginator import Paginator
#from forex_python.converter import CurrencyRates

#c = CurrencyRates(force_decimal=True)
c = CurrencyConverter(ECB_URL, decimal=True, fallback_on_wrong_date=True, fallback_on_missing_rate=True)

def sumCurrency(all_transactions, currency):
    sum = 0
    for tr in all_transactions:
        if currency.access_name != tr.currency.access_name:
            #tr.converted_amount = round(c.convert(tr.currency.access_name, currency.access_name, tr.amount, tr.transaction_date), 2)
            sum += round(c.convert(tr.amount, tr.currency.access_name, currency.access_name, date=tr.transaction_date), 2)
        else:
            sum += tr.amount
    return sum

def updateTransactions(all_transactions):
    today = date.today()
    repeating = all_transactions.filter(~Q(repeat=None))
    for tr in repeating:
        _date = tr.transaction_date
        if _date <= today:
            while _date < today:
                newTransaction = copy.copy(tr)
                newTransaction.id = None
                newTransaction.repeat = None
                newTransaction.save()
                _date = tr.transaction_date = tr.get_next_date()
            tr.save()

def prepareTransactions(all_transactions, currency, page, size):
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

    dates = sorted(dates, reverse=True)
    fut_dates = sorted(fut_dates, reverse=True)
    count += len(fut_dates) - len(repeating)

    def prepare_transactions_list(dates):
        transactions = []; values = []
        for dt in dates:
            values.append(sumCurrency(all_transactions.filter(transaction_date=dt), currency))
            transactions.append(reversed([tr for tr in all_transactions.filter(transaction_date=dt)]))
        return transactions, values
        
    transactions = prepare_transactions_list(dates)
    daily = zip(dates, *transactions)
    balance = sumCurrency(all_transactions, currency)
    future = zip(fut_dates, *prepare_transactions_list(fut_dates))
    return daily, balance, future, count, page_obj