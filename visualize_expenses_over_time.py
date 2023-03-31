import matplotlib.pyplot as plt
from categories import CATEGORIES
from process_transactions import get_transaction_filenames, TRANSACTIONS_FILE_SUFFIX
from os import path
from datetime import date

def main():
    today = date.today()
    for filename in get_transaction_filenames(today.year, today.month):
        month_year = path.split(filename)[1].replace(TRANSACTIONS_FILE_SUFFIX, '')
        print(month_year)

if __name__ == '__main__':
    main()
