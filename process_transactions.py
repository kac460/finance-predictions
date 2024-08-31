from calendar import month_name
from os import listdir, path
import csv

_AMOUNT = 'Amount'
_CATEGORY = 'Category'
_TRANSACTIONS_FIRST_ROW = 'Transactions First Row'
_TRANSACTIONS_DIR = 'transactions'
TRANSACTIONS_FILE_SUFFIX = ' - Transactions.csv'
_TRANSACTIONS_FILE_FORMAT = path.join(_TRANSACTIONS_DIR, '{} {}' + TRANSACTIONS_FILE_SUFFIX)
START_YEAR = 2021
START_MONTH_NUM = 1
'''
Returns the column indexes of Amount/Category in the given file
and the row index of the first transactions row
'''
def _get_category_amount_transaction_indexes(filename):
    row_num = 0
    with open(filename) as f:
        for line in f.readlines():
            columns = line.split(',')
            if _AMOUNT in columns and _CATEGORY in columns:
                return {
                    _AMOUNT: columns.index(_AMOUNT),
                    _CATEGORY: columns.index(_CATEGORY),
                    _TRANSACTIONS_FIRST_ROW: row_num + 1
                }
            row_num += 1
    raise Exception(f'Could not find {_AMOUNT} and {_CATEGORY} in {filename}')


def _filename_from_date(year, month_number):
    month = month_name[month_number]
    return _TRANSACTIONS_FILE_FORMAT.format(month, year)


'''
Returns a list of transaction filenames, ordered (asc) by date based on filename
Note - cutoff_month, cutoff_year is an EXCLUSIVE boundary
so if we pass 2022, 11, then the last filename returned would be "October 2022 - Transactions.csv"
'''
def get_transaction_filenames(cutoff_year, cutoff_month):
    is_before_cutoff = lambda y, m: y < cutoff_year or (y==cutoff_year and m < cutoff_month)
    dir_filenames = [
        path.join(_TRANSACTIONS_DIR, filename) 
        for filename in listdir(_TRANSACTIONS_DIR)
    ]
    return list(filter(lambda filename: filename in dir_filenames, [
        _filename_from_date(y, m) 
        for y in range(START_YEAR, cutoff_year+1) 
        for m in range(1, 13)
        if is_before_cutoff(y, m)
    ]))


def category_expenses_for_file(filename):
    print(f'file: {filename}')
    category_expenses = {}
    indexes = _get_category_amount_transaction_indexes(filename)
    first_transaction_row = indexes[_TRANSACTIONS_FIRST_ROW]
    category_column_index = indexes[_CATEGORY]
    amount_column_index = indexes[_AMOUNT]
    with open(filename) as f:
        lines = f.readlines()
        for row in csv.reader(lines[first_transaction_row:]):
            category = row[category_column_index]
            amount = row[amount_column_index]
            category_expenses[category] = category_expenses.get(category, 0) + float(amount.strip('-$"').replace(',', ''))
    return category_expenses


def category_expenses_for_month(year, month_num):
    filename = _filename_from_date(year, month_num)
    return category_expenses_for_file(filename)


def total_expenses_in_file(filename):
    category_expenses = category_expenses_for_file(filename)
    return sum([expense for expense in category_expenses.values()])
