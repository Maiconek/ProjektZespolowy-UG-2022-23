import copy
from datetime import date
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from currency_converter import CurrencyConverter, ECB_URL

c = CurrencyConverter(ECB_URL, decimal=True, fallback_on_wrong_date=True, fallback_on_missing_rate=True)

def setCurrency(all_transactions, currency):
    for i, tr in enumerate(all_transactions):
        if currency.access_name != tr.currency.access_name:
            all_transactions[i].converted_amount = round(c.convert(tr.amount, tr.currency.access_name, currency.access_name, date=tr.transaction_date), 2)
    return all_transactions

def updateTransactions(all_transactions):
    today = date.today()
    repeating = all_transactions.filter(~Q(repeat=None))
    for tr in repeating:
        _date = tr.transaction_date
        if _date <= today:
            while _date <= today:
                newTransaction = copy.copy(tr)
                newTransaction.id = None
                newTransaction.repeat = None
                newTransaction.save()
                _date = tr.transaction_date = tr.get_next_date()
            tr.save()

def prepareTransactions(all_transactions, currency):
    all_transactions = all_transactions.order_by('-transaction_date')
    all_transactions = setCurrency(all_transactions, currency)
    today = date.today()
    repeating = all_transactions.filter(~Q(repeat=None))
    count = 0
    nextMonth = today + relativedelta(months=+1)
    for tr in repeating:
        _date = tr.transaction_date
        while _date <= nextMonth:
            count += 1
            _date = tr.transaction_date = tr.get_next_date()

    dates = []; fut_dates = []
    for t in all_transactions:
        if t.transaction_date <= today:
            if t.transaction_date not in dates:
                dates.append(t.transaction_date)
        elif t.transaction_date not in fut_dates:
            fut_dates.append(t.transaction_date)
    count += len(fut_dates) - len(repeating)

    def prepare_transactions_list(dates):
        transactions = []; values = []
        for dt in dates:
            values.append(sum(tr.converted_amount for tr in all_transactions if tr.transaction_date == dt))
            transactions.append(reversed([tr for tr in all_transactions if tr.transaction_date == dt]))
        return transactions, values
        
    transactions = prepare_transactions_list(dates)
    daily = zip(dates, *transactions)
    balance = sum(v for v in transactions[1])
    future = zip(fut_dates, *prepare_transactions_list(fut_dates))
    return daily, balance, future, count