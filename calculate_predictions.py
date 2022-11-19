from calendar import month_name
from os import listdir
from datetime import date
import csv

HARDCODED_PREDICTIONS = {
    'Rent': 2150,
    'Cellphone': 30,
    'Car Insurance': 85.43,
    'Internet': 59.99
}

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
'''
Returns a list of transaction filenames, ordered (asc) by date based on filename
'''
def get_transaction_filenames():
    transaction_filenames = []
    dir_filenames = listdir()
    end_year = date.today().year
    print(f'end year: {end_year}')
    for year in range(START_YEAR, end_year + 1):
        for month in month_name[1:]:  # first element is empty string -> index 1 for January, 2 for Feb, etc.
            candidate_filename = TRANSACTION_FILE_FORMAT.format(month, year)
            print(candidate_filename)
            if candidate_filename in dir_filenames:
                transaction_filenames.append(candidate_filename)
            else:
                return transaction_filenames
    return transaction_filenames


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


# Returns reverse of [0.5, 0.25, 0.125, ..., 2^(-1*num_weights)]
def exponential_weights(num_weights):
    return [2**(-1*i) for i in reversed(range(1, num_weights+1))]


def weighted_avg(vals, weights):
    assert len(vals) == len(weights)
    return sum([vals[i]*weights[i] for i in range(len(vals))])/sum(weights)


'''
Returns a dictionary in the form
{ category (string): prediction (float) }
'''
def compute_predictions():
    filenames = get_transaction_filenames()
    category_expenses_for_files = [category_expenses_for_file(filename) for filename in filenames]
    predictions = {}
    # we assume all categories are present in the first category_expenses dict
    for category in category_expenses_for_files[0]:
        category_expenses = [category_expense.get(category, 0) for category_expense in category_expenses_for_files]
        predictions[category] = HARDCODED_PREDICTIONS.get(category, weighted_avg(
            category_expenses,
            exponential_weights(len(category_expenses))
        ))
    return predictions

final_predictions = compute_predictions()

def total_expenses_in_file(filename):
    category_expenses = category_expenses_for_file(filename)
    return sum([expense for category, expense in category_expenses.items()])

def print_average_expenses():
    filenames = get_transaction_filenames()
    print("-----------\n")
    print(f'AVERAGE MONTHLY EXPENSE: {sum([total_expenses_in_file(filename) for filename in filenames])/len(filenames)}')
    print("-----------\n")
print_average_expenses()

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