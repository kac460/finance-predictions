from calendar import month_name
from os import listdir
from datetime import date
import csv
from hardcoded_predictions import HARDCODED_PREDICTIONS
from weights_functions import incrementing_weights

AMOUNT = 'Amount'
CATEGORY = 'Category'
TRANSACTIONS_FIRST_ROW = 'Transactions First Row'
'''
Returns the column indexes of Amount/Category in the given file
and the row index of the first transactions row
'''
def get_category_amount_transaction_indexes(filename):
    row_num = 0
    with open(filename) as f:
        for line in f.readlines():
            columns = line.split(',')
            if AMOUNT in columns and CATEGORY in columns:
                return {
                    AMOUNT: columns.index(AMOUNT),
                    CATEGORY: columns.index(CATEGORY),
                    TRANSACTIONS_FIRST_ROW: row_num + 1
                }
            row_num += 1
    raise Exception(f'Could not find {AMOUNT} and {CATEGORY} in {filename}')


TRANSACTION_FILE_FORMAT = '{} {} - Transactions.csv'
START_YEAR = 2021
START_MONTH_NUM = 1

def filename_from_date(year, month_number):
    month = month_name[month_number]
    return TRANSACTION_FILE_FORMAT.format(month, year)


'''
Returns a list of transaction filenames, ordered (asc) by date based on filename
Note - cutoff_month, cutoff_year is an EXCLUSIVE boundary
so if we pass 2022, 11, then the last filename returned would be "October 2022 - Transactions.csv"
'''
def get_transaction_filenames(cutoff_year, cutoff_month):
    is_before_cutoff = lambda y, m: y < cutoff_year or (y==cutoff_year and m < cutoff_month)
    dir_filenames = listdir()
    return list(filter(lambda filename: filename in dir_filenames, [
        filename_from_date(y, m) 
        for y in range(START_YEAR, cutoff_year+1) 
        for m in range(1, 13)
        if is_before_cutoff(y, m)
    ]))


def category_expenses_for_file(filename):
    print(f'file: {filename}')
    category_expenses = {}
    indexes = get_category_amount_transaction_indexes(filename)
    first_transaction_row = indexes[TRANSACTIONS_FIRST_ROW]
    category_column_index = indexes[CATEGORY]
    amount_column_index = indexes[AMOUNT]
    with open(filename) as f:
        lines = f.readlines()
        for row in csv.reader(lines[first_transaction_row:]):
            category = row[category_column_index]
            amount = row[amount_column_index]
            category_expenses[category] = category_expenses.get(category, 0) + float(amount.strip('$"').replace(',', ''))
    return category_expenses


def category_expenses_for_month(year, month_num):
    filename = filename_from_date(year, month_num)
    return category_expenses_for_file(filename)


def weighted_avg(vals, weights):
    assert len(vals) == len(weights)
    return sum([vals[i]*weights[i] for i in range(len(vals))])/sum(weights)


'''
Returns a dictionary in the form
{ category (string): prediction (float) }
'''
def compute_predictions(year, month_num, weights_function=incrementing_weights):
    filenames = get_transaction_filenames(year, month_num)
    if len(filenames) == 0:
        print(f'NO FILES PRE-{month_num}/{year}')
        return None
    category_expenses_for_files = [category_expenses_for_file(filename) for filename in filenames]
    predictions = {}
    # we assume all categories are present in the first category_expenses dict
    for category in category_expenses_for_files[0]:
        category_expenses = [category_expense.get(category, 0) for category_expense in category_expenses_for_files]
        predictions[category] = HARDCODED_PREDICTIONS.get(category, weighted_avg(
            category_expenses,
            weights_function(len(category_expenses))
        ))
    return predictions

def total_expenses_in_file(filename):
    category_expenses = category_expenses_for_file(filename)
    return sum([expense for category, expense in category_expenses.items()])

def print_average_expenses(year, month_num):
    filenames = get_transaction_filenames(year, month_num)
    print("-----------\n")
    print(f'AVERAGE MONTHLY EXPENSE: {sum([total_expenses_in_file(filename) for filename in filenames])/len(filenames)}')
    print("-----------\n")


def main():
    today = date.today()
    final_predictions = compute_predictions(today.year, today.month)
    print_average_expenses(today.year, today.month)

    print("RAW:")
    print(final_predictions)
    print("-----------")
    ORDER_OF_CATEGORIES_COPIED = (
        '''
        Rent	
        Cellphone	
        Car Insurance	
        Internet	
        Electricity/Gas	
        Water	
        Groceries	
        Transportation	
        Health	
        Other Necessity	
        Home	
        Restaurants	
        Entertainment	
        Vacation	
        Gifts	
        Other Non-Necessity	
        '''
    )
    order_of_categories_copied_split = ORDER_OF_CATEGORIES_COPIED.split('\n')
    for category in order_of_categories_copied_split[1:len(order_of_categories_copied_split)-1]:
        print(final_predictions.get(category.strip().replace('\t', '')))



if __name__ == '__main__':
    main()